# main.py

import json
from code.send_email import send_email
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API"))

# === Generate summary from Groq ===
def groq_generate_summary(transcript_path):
    with open(transcript_path, 'r') as file:
        full_data = json.load(file)

    discussion = full_data["meeting"]["discussion"]

    transcript_text = "\n".join([f"{entry['speaker']}: {entry['message']}" for entry in discussion])

    prompt = f"""
    You are a smart meeting assistant.

    Here is the meeting transcript:

    {transcript_text}

    Summarize the meeting and output strictly in JSON format:
    {{
      "overall_summary": "...",
      "attendees": [
        {{
          "name": "...",
          "email": "",  # leave blank if unsure
          "summary": "...",
          "tasks": ["..."]
        }}
      ]
    }}
    Only return valid JSON.
    """

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    text = response.choices[0].message.content.strip()
    try:
        return json.loads(text)
    except Exception as e:
        print("❌ Error parsing Groq response:", e)
        print("Response content:\n", text)
        return {}

# === Helper to merge email addresses ===
def merge_emails(attendees, participants):
    email_lookup = {p["name"]: p["email"] for p in participants}

    for person in attendees:
        name = person.get("name")
        person["email"] = person.get("email") or email_lookup.get(name)

    return attendees

# === Main Execution ===
if __name__ == "__main__":
    transcript_path = "code/trail_meeting.json"
    summary_data = groq_generate_summary(transcript_path)

    if not summary_data:
        print("Summary generation failed or returned empty.")
        exit(1)

    with open(transcript_path, "r") as f:
        original_data = json.load(f)

    participants = original_data["meeting"]["participants"]
    attendees = merge_emails(summary_data.get("attendees", []), participants)
    overall = summary_data.get("overall_summary", "")

    for person in attendees:
        name = person.get("name")
        email = person.get("email")

        if not email:
            print(f"⚠️ No email found for {name}, skipping...")
            continue

        summary = person.get("summary", "")
        tasks = person.get("tasks", [])

        message = f"""
Hi {name},

Here’s your summary from the Full Stack Python Project meeting:

=== Overall Summary ===
{overall}

=== Your Discussion Summary ===
{summary}

=== Assigned Tasks ===
{chr(10).join(['- ' + task for task in tasks]) if tasks else 'None'}

Regards,  
Team AIReactor
""".strip()

        send_email(
            subject="Your Meeting Summary: Full Stack Python Project",
            content=message,
            to_addresses=[email]
        )
