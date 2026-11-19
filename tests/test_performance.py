"""Порівняння часу: мутабельна (dict/list/set) vs незмінна модель.

Запуск: pytest -q --durations=5
"""

from core import add_grade, add_skill
from model import Student
from mutable_legacy import add_grade_inplace, add_skill_inplace, make_student

N = 2000


def test_perf_mutable_before() -> None:
    s = make_student(1, "A")
    for i in range(N):
        add_grade_inplace(s, f"c{i % 10}", i % 100)
        add_skill_inplace(s, f"s{i % 20}")
    assert len(s["skills"]) == 20


def test_perf_immutable_after() -> None:
    s = Student(1, "A")
    for i in range(N):
        s = add_skill(add_grade(s, f"c{i % 10}", i % 100), f"s{i % 20}")
    assert len(s.skills) == 20
