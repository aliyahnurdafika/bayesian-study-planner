from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD


def build_model():
    ''' Constructs the structure of the Bayesian network. '''
    edges = [
        ("Concept1Difficulty", "Mastery"),
        ("Concept2Difficulty", "Mastery"),
        ("Concept3Difficulty", "Mastery"),
        ("Mastery", "Stress"),
        ("DaysRemaining", "Stress"),
        ("Mastery", "ExamSuccess"),
        ("Stress", "ExamSuccess"),
    ]

    model = DiscreteBayesianNetwork(edges)

    return model


def add_prior_cpds(model):
    '''     
    Adds conditional probability distributions for the root nodes.

    Concept 1 Difficulty: easy, medium, hard
    Concept 2 Difficulty: easy, medium, hard
    Concept 3 Difficulty: easy, medium, hard
    Days Remaining: few, moderate, many
    '''
    cpd_concept1 = TabularCPD(variable="Concept1Difficulty", variable_card=3,
        values=[[1 / 3], [1 / 3], [1 / 3],],
        state_names={"Concept1Difficulty": ["easy", "medium", "hard"]}
    )

    cpd_concept2 = TabularCPD(variable="Concept2Difficulty", variable_card=3,
        values=[[1 / 3], [1 / 3], [1 / 3],], 
        state_names={"Concept2Difficulty": ["easy", "medium", "hard"]}
    )

    cpd_concept3 = TabularCPD(variable="Concept3Difficulty", variable_card=3,
        values=[[1 / 3], [1 / 3], [1 / 3],],
        state_names={"Concept3Difficulty": ["easy", "medium", "hard"]}
    )

    cpd_days_remaining = TabularCPD(variable="DaysRemaining", variable_card=3,
        values=[[1 / 3], [1 / 3],[1 / 3],],
        state_names={"DaysRemaining": ["few", "moderate", "many"]}
    )

    model.add_cpds(cpd_concept1, cpd_concept2, cpd_concept3, cpd_days_remaining)


def add_mastery_cpd(model):
    '''
    Adds the conditional probability distribution for the Mastery variable.

    Mastery depends on the difficulty of the three concepts.
    Mastery: low, medium, high

    Assumption:
    Harder concepts make lower mastery more likely, while easier concepts make higher mastery more likely.
    '''

    cpd_mastery = TabularCPD(variable="Mastery", variable_card=3,
        values=[
            # Mastery = low
            [
                # Concept 1 = easy
                0.05, 0.08, 0.15,   # Concept 2 = easy,   Concept 3 = easy, medium, hard
                0.08, 0.15, 0.25,   # Concept 2 = medium, Concept 3 = easy, medium, hard
                0.15, 0.25, 0.50,   # Concept 2 = hard,   Concept 3 = easy, medium, hard

                # Concept 1 = medium
                0.08, 0.15, 0.25,   # Concept 2 = easy,   Concept 3 = easy, medium, hard
                0.15, 0.25, 0.50,   # Concept 2 = medium, Concept 3 = easy, medium, hard
                0.25, 0.50, 0.70,   # Concept 2 = hard,   Concept 3 = easy, medium, hard

                # Concept 1 = hard
                0.15, 0.25, 0.50,   # Concept 2 = easy,   Concept 3 = easy, medium, hard
                0.25, 0.50, 0.70,   # Concept 2 = medium, Concept 3 = easy, medium, hard
                0.50, 0.70, 0.80,   # Concept 2 = hard,   Concept 3 = easy, medium, hard
            ],

            # Mastery = medium
            [
                0.15, 0.22, 0.35,
                0.22, 0.35, 0.50,
                0.35, 0.50, 0.35,

                0.22, 0.35, 0.50,
                0.35, 0.50, 0.35,
                0.50, 0.35, 0.22,

                0.35, 0.50, 0.35,
                0.50, 0.35, 0.22,
                0.35, 0.22, 0.15,
            ],

            # Mastery = high
            [
                0.80, 0.70, 0.50,
                0.70, 0.50, 0.25,
                0.50, 0.25, 0.15,

                0.70, 0.50, 0.25,
                0.50, 0.25, 0.15,
                0.25, 0.15, 0.08,

                0.50, 0.25, 0.15,
                0.25, 0.15, 0.08,
                0.15, 0.08, 0.05,
            ],
        ],

        evidence=["Concept1Difficulty", "Concept2Difficulty", "Concept3Difficulty"],
        evidence_card=[3, 3, 3],
        state_names={
            "Mastery": ["low", "medium", "high"],
            "Concept1Difficulty": ["easy", "medium", "hard"],
            "Concept2Difficulty": ["easy", "medium", "hard"],
            "Concept3Difficulty": ["easy", "medium", "hard"],
        }
    )
    model.add_cpds(cpd_mastery)


def add_stress_cpd(model):
    '''
    Adds the conditional probability distribution for the Stress variable.

    Stress depends on Mastery and Days Remaining.
    Stress: low, medium, high

    Assumption:
    Lower mastery and fewer days remaining make higher stress more likely.
    '''
    cpd_stress = TabularCPD(variable="Stress", variable_card=3,
        values=[
            # Stress = low
            [
                0.05, 0.15, 0.30,   # Mastery = low,    Days Remaining = few, moderate, many
                0.15, 0.30, 0.60,   # Mastery = medium, Days Remaining = few, moderate, many
                0.30, 0.60, 0.75,   # Mastery = high,   Days Remaining = few, moderate, many
            ],

            # Stress = medium
            [
                0.20, 0.35, 0.45,
                0.35, 0.45, 0.30,
                0.45, 0.30, 0.20,
            ],

            # Stress = high
            [
                0.75, 0.50, 0.25,
                0.50, 0.25, 0.10,
                0.25, 0.10, 0.05,
            ],
        ],
        evidence=["Mastery", "DaysRemaining"], evidence_card=[3, 3],
        state_names={
            "Stress": ["low", "medium", "high"],
            "Mastery": ["low", "medium", "high"],
            "DaysRemaining": ["few", "moderate", "many"],
        }
    )
    model.add_cpds(cpd_stress)


def add_exam_success_cpd(model):
    '''
    Adds the conditional probability distribution for the ExamSuccess variable.

    Exam Success depends on Mastery and Stress.
    Exam Success: low, medium, high

    Assumption:
    Higher mastery and lower stress make higher exam success more likely.
    '''
    cpd_exam_success = TabularCPD(variable="ExamSuccess", variable_card=3,
        values=[
            # ExamSuccess = low
            [
                0.40, 0.65, 0.80,   # Mastery = low,    Stress = low, medium, high
                0.15, 0.25, 0.45,   # Mastery = medium, Stress = low, medium, high
                0.05, 0.10, 0.20,   # Mastery = high,   Stress = low, medium, high
            ],

            # ExamSuccess = medium
            [
                0.40, 0.25, 0.15,
                0.35, 0.50, 0.40,
                0.15, 0.25, 0.40,
            ],

            # ExamSuccess = high
            [
                0.20, 0.10, 0.05,
                0.50, 0.25, 0.15,
                0.80, 0.65, 0.40,
            ],
        ],
        evidence=["Mastery", "Stress"], evidence_card=[3, 3],
        state_names={
            "ExamSuccess": ["low", "medium", "high"],
            "Mastery": ["low", "medium", "high"],
            "Stress": ["low", "medium", "high"],
        }
    )
    model.add_cpds(cpd_exam_success)


def create_bayesian_model():
    model = build_model()

    add_prior_cpds(model)
    add_mastery_cpd(model)
    add_stress_cpd(model)
    add_exam_success_cpd(model)

    return model