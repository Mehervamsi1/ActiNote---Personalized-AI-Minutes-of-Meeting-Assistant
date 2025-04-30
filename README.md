# ActiNote---Personalized-AI-Minutes-of-Meeting-Assistant

🔍 Project Overview
ActiNote is an intelligent meeting assistant that:

Parses Microsoft Teams meeting transcripts

Extracts key summaries and action items

Maps participants to their organizational emails

Sends personalized follow-up emails to each participant

Integrates with Microsoft Graph API for secure and automated email delivery

🏗️ Tech Stack

Layer	Technology
Backend	Python 3.12, asyncio, requests
Email API	Microsoft Graph API + Azure Identity
Auth	OAuth 2.0 (Client Credentials flow)
Env Mgmt	python-dotenv
Deployment	GitHub + Codespaces/VS Code (initial)
📚 Core Features
✅ Meeting Transcript Parsing
Ingests structured Microsoft Teams transcripts

Extracts participant names and discussion flow

✅ Action Item Detection
Uses static/dynamic prompts (or simple logic) to extract individual action points

✅ Email Personalization
Matches participant names to organizational emails (via mock DB or future directory service)

Customizes emails with individual summaries and action items

✅ Microsoft Graph Email Sending
Sends HTML-formatted follow-up emails to each participant

Authenticates using Client Credentials (no user interaction required)

Add support for calendar integration via Microsoft Graph API

Replace mock DB with live directory lookup or SharePoint user list

UI dashboard for uploading transcripts and monitoring email status

📬 Use Case
Ideal for teams using Microsoft 365 & Teams who want:

Instant, AI-curated meeting summaries

Action item tracking

Personalized follow-up without manual effort

