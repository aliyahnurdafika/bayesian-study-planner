# Bayesian Study Planner

## Overview

This project uses a Bayesian Network to recommend study actions based on concept difficulty, student mastery, stress level, days remaining before an exam, and expected exam success.

The system will compare possible study actions using expected utility and schedule the selected action through the Google Calendar API.

The actions are:
```text
Intensive Study → 5 hours
Light Review    → 1 hour
Rest            → no study event
```

## Project Structure

```text
bayesian-study-planner/
├── docs/
│   ├── bayesian_model.md
│   ├── calendar_integration.md
│   └── study_planner.md
│
├── src/
│   ├── bayesian_model.py
│   ├── calendar_integration.py
│   └── study_planner.py
│
├── tests/
│   ├── test_bayesian_model.py
│   └── test_study_planner.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

## File Description

- `bayesian_model.py`: Defines the Bayesian Network structure and handcrafted Conditional Probability Distributions (CPDs).
- `study_planner.py`: Collects user input, performs Bayesian inference, calculates expected utilities, selects the recommended action, and connects the result to the Calendar integration.
- `calendar_integration.py`: Handles Google Calendar authorization and creates study-session events based on the recommendation produced by the study planner.

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required libraries:

```bash
python3 -m pip install -r requirements.txt
```

## Google Calendar Integration
1. Create your own Google Cloud project in https://console.cloud.google.com/
2. Enable the Google Calendar API
3. Create an OAuth 2.0 Desktop App client. 
4. Download the credentials file and place it in the project root as:
```text
credentials.json
```
5. On the first authorized run, the application will open the Google authorization process and automatically create:
```text
token.json
```

Both `credentials.json` and `token.json` should be located in the project root folder.

## How to Run

Run the Bayesian Study Planner

```bash
python3 -m src.study_planner
```

## Unit Tests

Run all unit tests:

```bash
python3 -m pytest
```

Run an individual test file:

```bash
python3 -m pytest tests/test_bayesian_model.py
python3 -m pytest tests/test_study_planner.py
```