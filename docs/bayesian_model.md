# Bayesian Model
This document describes the Bayesian Network used in the study planner, including its variables, dependencies, probability distributions, and model assumptions.

## Overview
`bayesian_model.py` defines the Bayesian Network used to estimate the student's **Mastery**, **Stress**, and **Exam Success** based on concept difficulty and the number of days remaining before the exam.

The model contains seven variables:

```text
Concept1Difficulty
Concept2Difficulty
Concept3Difficulty
DaysRemaining
Mastery
Stress
ExamSuccess
```

The structure is:

```text
Concept1Difficulty ─┐
Concept2Difficulty ─┼──> Mastery ───────> ExamSuccess
Concept3Difficulty ─┘        │                ↑
                             ↓                │
DaysRemaining ────────────> Stress ───────────┘
```

---

## Variables and States

Each variable is discrete and has three possible states.

| Variable | States | Description |
|---|---|---|
| `Concept1Difficulty` | easy, medium, hard | Difficulty of the first concept |
| `Concept2Difficulty` | easy, medium, hard | Difficulty of the second concept |
| `Concept3Difficulty` | easy, medium, hard | Difficulty of the third concept |
| `DaysRemaining` | few, moderate, many | Time remaining before the exam |
| `Mastery` | low, medium, high | Overall mastery level across the three concepts |
| `Stress` | low, medium, high | Estimated student stress level |
| `ExamSuccess` | low, medium, high | Estimated likelihood of exam success |

`DaysRemaining` is categorized as:

```text
few       → 0–2 days
moderate  → 3–7 days
many      → 8 or more days
```

The four root nodes (`Concept1Difficulty`, `Concept2Difficulty`, `Concept3Difficulty`, and `DaysRemaining`) use a uniform prior distribution before user input, meaning that each possible state is treated as equally likely:

```text
1/3
1/3
1/3
```

When the planner is run, the user provides the observed states for the three concept difficulties and the exam date. The exam date is then converted into the `DaysRemaining` state. These observed values are used as evidence for Bayesian inference.

The model assumes that concept difficulty affects the student's overall mastery. Mastery and the number of days remaining before the exam influence stress. Exam success is then estimated from both mastery and stress.

---

## CPD Design

The model uses handcrafted Conditional Probability Distributions (CPDs). 

### Mastery

`Mastery` is determined by the difficulty of the three concepts.

The CPD assumes that harder concepts make lower mastery more likely, while easier concepts make higher mastery more likely. The three concept difficulties are treated as contributing to the student's overall mastery.

### Stress

`Stress` is determined by `Mastery` and `DaysRemaining`.

The CPD assumes that lower mastery and fewer days remaining make higher stress more likely. Both factors contribute to the student's stress level.

### Exam Success

`ExamSuccess` is determined by `Mastery` and `Stress`.

The CPD assumes that higher mastery increases the likelihood of exam success, while higher stress decreases it.

## Unit Tests
To check each function involved in constructing the Bayesian Network.

Run:
```bash
python tests/test_bayesian_model.py
```