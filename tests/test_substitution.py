import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from src.ast import Var, Const, Predicate, Forall, Exists, And, Implies
from src.substitution import (
    free_variables_formula,
    substitute_formula,
)


def test_free_variables_simple():
    f = Predicate("P", (Var("x"), Const("a")))
    assert free_variables_formula(f) == {"x"}


def test_free_variables_under_quantifier():
    f = Forall("y", Predicate("P", (Var("x"), Var("y"))))
    assert free_variables_formula(f) == {"x"}


def test_substitute_does_not_capture():
    body = Predicate("P", (Var("x"), Var("y")))
    formula = Forall("y", body)

    result = substitute_formula(formula, "x", Var("y"))

    assert isinstance(result, Forall)
    assert result.var != "y"
    assert isinstance(result.body, Predicate)
    assert result.body.terms[0] == Var("y")
    assert result.body.terms[1] == Var(result.var)


def test_substitute_skips_bound_var():
    formula = Forall("x", Predicate("P", (Var("x"),)))
    result = substitute_formula(formula, "x", Const("a"))
    assert result == formula


def test_substitute_existing_var_in_predicate():
    formula = Predicate("P", (Var("x"), Var("y")))
    result = substitute_formula(formula, "x", Const("a"))
    assert result == Predicate("P", (Const("a"), Var("y")))


def test_substitute_into_implies():
    formula = Implies(
        Predicate("P", (Var("x"),)),
        Predicate("Q", (Var("x"),)),
    )
    result = substitute_formula(formula, "x", Const("a"))
    assert result == Implies(
        Predicate("P", (Const("a"),)),
        Predicate("Q", (Const("a"),)),
    )


def test_capture_avoidance_in_exists():
    formula = Exists("y", Predicate("P", (Var("x"), Var("y"))))
    result = substitute_formula(formula, "x", Var("y"))
    assert isinstance(result, Exists)
    assert result.var != "y"