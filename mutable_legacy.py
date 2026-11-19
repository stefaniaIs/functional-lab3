"""МУТАБЕЛЬНА версія «до» переходу на immutability (для порівняння часу).

Тут усе змінюється in-place: list.append, set.add, dict[...] = ...
"""

from __future__ import annotations

from typing import Any

MutableStudent = dict[str, Any]


def make_student(sid: int, name: str) -> MutableStudent:
    return {"id": sid, "name": name, "results": {}, "skills": set(), "gpa": 0.0}


def add_grade_inplace(s: MutableStudent, course: str, grade: int) -> None:
    s["results"].setdefault(course, []).append(grade)
    grades = [g for gs in s["results"].values() for g in gs]
    s["gpa"] = round(sum(grades) / len(grades), 2)


def add_skill_inplace(s: MutableStudent, skill: str) -> None:
    s["skills"].add(skill.strip().lower())
