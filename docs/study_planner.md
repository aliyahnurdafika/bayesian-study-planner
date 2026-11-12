# Study Planner

## Overview
This document describes how `study_planner.py` converts user input into a recommended study action using Bayesian inference and expected utility.

The workflow is:

```text
User Input
    ↓
Evidence Preparation (Concept 1, 2, 3 Difficulty and Exam Date)
    ↓
Bayesian Inference
    ↓
Expected Utility
    ↓
Best Action
    ↓
Calendar Integration
```

The three possible actions are:

```text
Intensive Study → 5 hours
Light Review    → 1 hour
Rest            → 0 hours
```

---

## User Input and Evidence

The planner asks the user for:

```text
Concept 1 difficulty
Concept 2 difficulty
Concept 3 difficulty
Exam date
```

Concept difficulty must be one of:

```text
easy
medium
hard
```

The exam date must use `YYYY-MM-DD` format and cannot be in the past. The number of days remaining before the exam is then calculated and categorized as `DaysRemaining`.

---

## Bayesian Inference

Inference is performed using pgmpy's `BeliefPropagation`. Two queries are required for:

The first calculates the marginal distributions, which describe the predicted student condition.

```text
P(Mastery | evidence)
P(Stress | evidence)
P(ExamSuccess | evidence)
```

The second calculates the joint distribution since the utility of each study action depends on the combination of `ExamSuccess` and `Stress`.

```text
P(ExamSuccess, Stress | evidence)
```

---

## Utility Design

The planner uses handcrafted utility values to represent how desirable each action is under different combinations of `ExamSuccess` and `Stress`.

There are nine possible combinations and the values are design assumptions. Higher utility values indicate that an action is more desirable for a given condition.

The intended pattern is:

```text
Lower ExamSuccess 
→ Intensive Study becomes more desirable

Moderate ExamSuccess
→ Light Review becomes more desirable

Higher ExamSuccess
→ Rest becomes more desirable

Higher Stress
→ Intensive Study becomes less desirable
→ Rest becomes more desirable
```

---

## Expected Utility
For each action:

```text
Expected Utility = sum of P(ExamSuccess, Stress | evidence) × Utility
```

For example, the expected utility of `Intensive Study` considers:

```text
P(low success, low stress) × utility
+
P(low success, medium stress) × utility
+
...
+
P(high success, high stress) × utility
```

The same calculation is performed separately for another actions.

---

## Action Selection

After calculating the expected utility of all three actions, the planner selects the action with the highest value.

Example:

```text
Intensive Study: 4.973
Light Review:    5.692
Rest:            3.896
```

The recommended action is therefore:

```text
Light Review
```

---

## Calendar Handoff
After an action is selected, `study_planner.py` passes the recommendation to `calendar_integration.py`.

```text
Recommended Action
        ↓
Study Planner
        ↓
Calendar Integration
```

For `Intensive Study` or `Light Review`, the user can choose whether to add the recommendation to Google Calendar.

For `Rest`, no study session is added.
