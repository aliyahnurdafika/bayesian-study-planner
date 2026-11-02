# Bayesian Study Planner

A personalized Bayesian study planning system with Google Calendar integration.

## Overview

This project uses a Bayesian Network to recommend study actions based on factors such as concept difficulty, student mastery, stress level, days remaining before an exam, and expected exam success.

The system will compare possible study actions using expected utility and schedule the selected action through the Google Calendar API.

## Project Structure

```text
bayesian-study-planner/
├── src/
│   ├── calendar_integration.py
│   └── study_planner.py
├── .gitignore
├── README.md
└── requirements.txt
```

## File Description
`calendar_integration.py`: handles authentication and communication with Google Calendar, including creating study-session events selected by the study planner.

## Setup

Install the required libraries:

```bash
python3 -m pip install -r requirements.txt
```

## How to Run

1. Create and activate venv

```bash
python3 -m venv .venv
source .venv/bin/activate
```