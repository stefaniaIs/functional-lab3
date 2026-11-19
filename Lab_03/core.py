"""Pure-оновлення та бізнес-функції. Кожна функція повертає НОВИЙ Student."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence, Set
from dataclasses import replace
from functools import lru_cache
from types import MappingProxyType
from typing import Any

from model import CourseResult, Student


@lru_cache(maxsize=1024)
def grades_average(grades: tuple[int, ...]) -> float:
    """Чиста функція з кешем: tuple хешований, тож може бути ключем lru_cache."""
    return round(sum(grades) / len(grades), 2) if grades else 0.0


def recalc_gpa(student: Student) -> Student:
    """Перерахунок середнього балу по всіх оцінках усіх курсів."""
    all_grades = tuple(g for r in student.results for g in r.grades)
    return replace(student, gpa=grades_average(all_grades))


def add_grade(student: Student, course: str, grade: int) -> Student:
    """Додає оцінку (створює курс, якщо його ще нема) і перераховує gpa."""
    if not 0 <= grade <= 100:
        raise ValueError(f"grade must be in 0..100, got {grade}")
    if student.result_for(course) is None:
        results = student.results + (CourseResult(course, (grade,)),)
    else:
        results = tuple(
            r.with_grade(grade) if r.course == course else r for r in student.results
        )
    return recalc_gpa(replace(student, results=results))


def add_skill(student: Student, skill: str) -> Student:
    return student.with_skill(skill.strip().lower())


def remove_skill(student: Student, skill: str) -> Student:
    return replace(student, skills=student.skills - {skill})


def update_profile(student: Student, **changes: str) -> Student:
    """Новий read-only профіль = копія старого + зміни."""
    return replace(student, profile=MappingProxyType({**student.profile, **changes}))


def top_students(students: Sequence[Student], n: int = 3) -> tuple[Student, ...]:
    return tuple(sorted(students, key=lambda s: (-s.gpa, s.id))[:n])


def with_skills(students: Iterable[Student], needed: Set[str]) -> tuple[Student, ...]:
    """Студенти, що мають ВСІ потрібні навички (операція підмножини frozenset)."""
    return tuple(s for s in students if needed <= s.skills)


def faculty(profile: Mapping[str, str]) -> str:
    return profile.get("faculty", "unknown")


def freeze(obj: Any) -> Any:
    """Глибоке заморожування: dict->MappingProxyType, set->frozenset, list->tuple."""
    if isinstance(obj, Mapping):
        return MappingProxyType({k: freeze(v) for k, v in obj.items()})
    if isinstance(obj, (set, frozenset)):
        return frozenset(freeze(x) for x in obj)
    if isinstance(obj, (list, tuple)):
        return tuple(freeze(x) for x in obj)
    return obj
