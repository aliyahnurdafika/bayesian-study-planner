from src.bayesian_model import build_model, add_prior_cpds, add_mastery_cpd, add_stress_cpd, add_exam_success_cpd, create_bayesian_model

def test_build_model_nodes():
    model = build_model()
    expected_nodes = {
        "Concept1Difficulty",
        "Concept2Difficulty",
        "Concept3Difficulty",
        "Mastery",
        "DaysRemaining",
        "Stress",
        "ExamSuccess",
    }
    assert set(model.nodes()) == expected_nodes


def test_build_model_edges():
    model = build_model()
    expected_edges = {
        ("Concept1Difficulty", "Mastery"),
        ("Concept2Difficulty", "Mastery"),
        ("Concept3Difficulty", "Mastery"),
        ("Mastery", "Stress"),
        ("DaysRemaining", "Stress"),
        ("Mastery", "ExamSuccess"),
        ("Stress", "ExamSuccess"),
    }
    assert set(model.edges()) == expected_edges


def test_add_prior_cpds():
    model = build_model()
    add_prior_cpds(model)

    cpd = model.get_cpds("Concept1Difficulty")
    expected_output = [1 / 3, 1 / 3, 1 / 3]

    assert cpd.get_values().flatten().tolist() == expected_output


def test_add_mastery_cpd():
    model = build_model()
    add_mastery_cpd(model)

    cpd = model.get_cpds("Mastery")

    assert cpd.variable == "Mastery"
    assert cpd.variable_card == 3


def test_add_stress_cpd():
    model = build_model()
    add_stress_cpd(model)

    cpd = model.get_cpds("Stress")

    assert cpd.variable == "Stress"
    assert cpd.variable_card == 3


def test_add_exam_success_cpd():
    model = build_model()
    add_exam_success_cpd(model)

    cpd = model.get_cpds("ExamSuccess")

    assert cpd.variable == "ExamSuccess"
    assert cpd.variable_card == 3


def test_create_bayesian_model():
    model = create_bayesian_model()

    assert model.check_model() is True

# Run: python3 -m pytest tests/test_bayesian_model.py