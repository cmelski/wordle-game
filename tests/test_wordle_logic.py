from wordle_logic import evaluate_guess


def test_all_green():
    assert evaluate_guess("CRANE", "CRANE") == ["G", "G", "G", "G", "G"]


def test_all_gray():
    assert evaluate_guess("CRANE", "BLOOM") == ["⬛", "⬛", "⬛", "⬛", "⬛"]


def test_mixed_colors():
    assert evaluate_guess("CRANE", "REACT") == ["Y", "Y", "G", "Y", "⬛"]


def test_duplicate_letters():
    assert evaluate_guess("APPLE", "ALLEY") == ["G", "Y", "⬛", "Y", "⬛"]
