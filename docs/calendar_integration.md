# Google Calendar Integration

## Overview

This document explains what `calendar_integration.py` does and how to run it. The script connects the project to Google Calendar and creates study-session events based on the action selected through the expected utility calculation.

---

## Workflow

```text
Student input (3 Concept difficulties + exam date)
    ↓
Bayesian Network
    ↓
Mastery / Stress / Exam Success
    ↓
Expected utility
    ↓
Recommended action
    ↓
Google Calendar Integration
```

---

## Project Structure

```text
bayesian-study-planner/
├── docs/
├── src/
├── tests/
├── .gitignore
├── credentials.json
├── README.md
├── requirements.txt
└── token.json
```

**Note:** `credentials.json` and `token.json` exist only on the local machine and are excluded from Git through `.gitignore` because they contain application authorization information and user access data, respectively.

---

## Requirements

Install the project dependencies from the repository root:

```bash
python3 -m pip install -r requirements.txt
```

The Google Calendar integration uses:

- `google-api-python-client`
- `google-auth-httplib2`
- `google-auth-oauthlib`

A Google Cloud project with the **Google Calendar API enabled** is also required.

---

## Google Cloud Setup

The project uses OAuth 2.0 to authorize access to Google Calendar.

The Google Cloud configuration used for this project is:

- Google Calendar API enabled
- OAuth user type: **External**
- OAuth application status: **Testing**
- OAuth client type: **Desktop App**
- The Google account used for testing is added under **Test users**

After creating the Desktop App OAuth client, Google provides a JSON credentials file.

The downloaded file is renamed to:

```text
credentials.json
```

---

## `credentials.json`

`credentials.json` identifies the application to Google's OAuth system.

Conceptually:

```text
credentials.json
        ↓
Identifies the Bayesian Study Planner
        ↓
Allows the Google OAuth login process to begin
```

---

## `token.json`

After the first successful OAuth login, Google authorization information is stored locally in:

```text
token.json
```

Saving `token.json` prevents the user from having to complete the Google login flow every time the planner runs.

---

## Input

`calendar_integration.py` is called by `study_planner.py` after the recommended action has been selected.

It receives:

```text
- Recommended action
- Study duration
- Exam date
```

## Output

The Calendar behavior depends on the selected recommended action:

```text
Study Plan: 
Intensive Study → creates a 5-hour study event
Light Review    → creates a 1-hour study event
Rest            → no study event is created
```

For a study action, the event is added to the user's Google Calendar and includes:

```text
- action
- study duration
- exam date
- start and end time
- America/Vancouver time zone
```

Example:

```text
Study Plan: Light Review

Recommended action: Light Review
Study duration: 1 hour(s)
Exam date: 2026-11-10
```

The study session starts one hour after the planner is run. After the event is successfully created, the program prints a link to the Google Calendar event.