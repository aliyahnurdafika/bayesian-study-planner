from datetime import date, datetime

from pgmpy.inference import BeliefPropagation
from src.bayesian_model import create_bayesian_model
from src.calendar_integration import create_study_event

# Duration in hours for each action
ACTIONS = {
    "Intensive Study": 5,
    "Light Review": 1,
    "Rest": 0,
}

# (ExamSuccess, Stress) combination states.
# ExamSuccess and Stress are the two variables that determine the expected utility of each action (Intensive Study, Light Review, Rest).
STATE_COMBINATIONS = [
    ("low", "low"), ("low", "medium"), ("low", "high"),
    ("medium", "low"), ("medium", "medium"), ("medium", "high"),
    ("high", "low"), ("high", "medium"), ("high", "high"),
]

# Handcrafted utility values.
# Higher values mean the action is more desirable.
UTILITY_TABLE = {
    "Intensive Study": [
        15, 12.5, 10,
        7.5, 5, 2.5,
        0, -2.5, -5,
    ],

    "Light Review": [
        4.5, 5.5, 4.5,
        7, 8, 7,
        4.5, 5.5, 4.5,
    ],

    "Rest": [
        -6, -2, 2,
        0, 4, 8,
        6, 10, 14,
    ],
}


def get_difficulty(concept_name):
    valid_choices = ["easy", "medium", "hard"]

    difficulty = input(f"{concept_name} difficulty (easy/medium/hard): ").strip().lower()

    while difficulty not in valid_choices:
        print("Please enter easy, medium, or hard.")
        difficulty = input(f"{concept_name} difficulty: ").strip().lower()

    return difficulty


def get_exam_date():
    '''
    Gets and validates the exam date entered by the user.
    The date must use YYYY-MM-DD format and cannot be in the past.
    '''
    while True:
        exam_date_text = input("Exam date (YYYY-MM-DD): ").strip()

        try:
            exam_date = datetime.strptime(exam_date_text, "%Y-%m-%d").date()
            if exam_date < date.today():
                print("Please enter today or a future date.")
                continue
            return exam_date

        except ValueError:
            print("Please use the format YYYY-MM-DD.")


def categorize_days(days_remaining):
    if days_remaining <= 2:
        return "few"

    if days_remaining <= 7:
        return "moderate"

    return "many"


def get_user_evidence():
    print("\nEnter your current study conditions:")

    concept1 = get_difficulty("Concept 1")
    concept2 = get_difficulty("Concept 2")
    concept3 = get_difficulty("Concept 3")

    exam_date = get_exam_date()

    days_remaining = (exam_date - date.today()).days

    evidence = {
        "Concept1Difficulty": concept1,
        "Concept2Difficulty": concept2,
        "Concept3Difficulty": concept3,
        "DaysRemaining": categorize_days(days_remaining),
    }

    return evidence, exam_date, days_remaining


def run_inference(model, evidence):
    ''' Runs inference on the Bayesian model given the evidence provided by the user. '''
    inference = BeliefPropagation(model)

    # Marginal probabilities:
    # P(Mastery | evidence), P(Stress | evidence), P(ExamSuccess | evidence)
    result = inference.query(variables=["Mastery", "Stress", "ExamSuccess"], evidence=evidence, joint=False, show_progress=False)

    # Joint probability:
    # P(ExamSuccess, Stress | evidence)
    joint_distribution = inference.query(variables=["ExamSuccess", "Stress"], evidence=evidence, joint=True, show_progress=False)

    return result, joint_distribution


def calculate_expected_utility(joint_distribution, utility_values):
    '''
    Calculates the expected utility of one action.
    Each ExamSuccess and Stress probability is multiplied by the corresponding utility value, then all values are summed.
    '''
    expected_utility = 0

    for state, utility in zip(STATE_COMBINATIONS, utility_values):
        exam_success, stress = state
        probability = joint_distribution.get_value(ExamSuccess=exam_success, Stress=stress)
        expected_utility += probability * utility

    return expected_utility


def choose_best_action(joint_distribution):
    ''' Compares the expected utilities of all actions and selects the action with the highest value. '''
    intensive_utility = calculate_expected_utility(joint_distribution, UTILITY_TABLE["Intensive Study"])
    light_utility = calculate_expected_utility(joint_distribution, UTILITY_TABLE["Light Review"])
    rest_utility = calculate_expected_utility(joint_distribution, UTILITY_TABLE["Rest"])

    expected_utilities = {
        "Intensive Study": intensive_utility,
        "Light Review": light_utility,
        "Rest": rest_utility,
    }

    best_action = max(expected_utilities, key=expected_utilities.get)

    return best_action, expected_utilities


def main():
    model = create_bayesian_model()
    print("Checking model...")
    print("Model valid:", model.check_model())

    evidence, exam_date, days_remaining = (get_user_evidence())
    result, joint_distribution = run_inference(model, evidence)
    best_action, expected_utilities = (choose_best_action(joint_distribution))
    print("\nExam Date:", exam_date)
    print("Days Remaining:", days_remaining)
    print("Time Category:", evidence["DaysRemaining"])

    print("\nMastery:")
    print(result["Mastery"])

    print("\nStress:")
    print(result["Stress"])

    print("\nExam Success:")
    print(result["ExamSuccess"])

    print("\nExpected Utilities:")
    print(
        f"Intensive Study: "
        f"{expected_utilities['Intensive Study']:.3f}"
    )
    print(
        f"Light Review: "
        f"{expected_utilities['Light Review']:.3f}"
    )
    print(
        f"Rest: "
        f"{expected_utilities['Rest']:.3f}"
    )

    print("\nRecommended Action:")
    print(best_action)
    print("Duration:", ACTIONS[best_action], "hour(s)")

    # Calendar integration
    if best_action == "Rest":
        create_study_event(best_action, ACTIONS[best_action], exam_date)
    else:
        add_to_calendar = input("\nAdd this recommendation to Google Calendar? (y/n): ").strip().lower()

        if add_to_calendar == "y":
            create_study_event(best_action, ACTIONS[best_action], exam_date)
        else:
            print("Calendar event was not created.")

if __name__ == "__main__":
    main()