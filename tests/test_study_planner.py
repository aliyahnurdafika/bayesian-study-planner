from src.bayesian_model import create_bayesian_model
from src.study_planner import run_inference, choose_best_action, categorize_days


def test_intensive_study_scenario():
    model = create_bayesian_model()

    evidence = {
        "Concept1Difficulty": "hard",
        "Concept2Difficulty": "hard",
        "Concept3Difficulty": "hard",
        "DaysRemaining": "moderate",
    }

    result, joint_distribution = run_inference(model, evidence)
    best_action, expected_utilities = choose_best_action(joint_distribution)

    expected_output = "Intensive Study"

    assert best_action == expected_output


def test_light_review_scenario():
    model = create_bayesian_model()

    evidence = {
        "Concept1Difficulty": "medium",
        "Concept2Difficulty": "medium",
        "Concept3Difficulty": "medium",
        "DaysRemaining": "moderate",
    }

    result, joint_distribution = run_inference(model, evidence)
    best_action, expected_utilities = choose_best_action(joint_distribution)

    expected_output = "Light Review"

    assert best_action == expected_output


def test_rest_scenario():
    model = create_bayesian_model()

    evidence = {
        "Concept1Difficulty": "easy",
        "Concept2Difficulty": "easy",
        "Concept3Difficulty": "easy",
        "DaysRemaining": "few",
    }

    result, joint_distribution = run_inference(model, evidence)
    best_action, expected_utilities = choose_best_action(joint_distribution)

    expected_output = "Rest"

    assert best_action == expected_output


def test_categorize_days():
    assert categorize_days(2) == "few"
    assert categorize_days(5) == "moderate"
    assert categorize_days(10) == "many"

# Run: python3 -m pytest tests/test_study_planner.py