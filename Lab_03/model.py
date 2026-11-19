"""Варіант 3. Незмінна модель студентської успішності."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from types import MappingProxyType
from typing import NamedTuple


class CourseResult(NamedTuple):
    """Результат з одного курсу: оцінки зберігаються в tuple."""

    course: str
    grades: tuple[int, ...] = ()

    def average(self) -> float:
        return sum(self.grades) / len(self.grades) if self.grades else 0.0

    def with_grade(self, grade: int) -> CourseResult:
        return self._replace(grades=self.grades + (grade,))


def make_profile(**kwargs: str) -> Mapping[str, str]:
    """Read-only профіль. Спершу копіюємо dict, щоб назовні не лишилось посилання."""
    return MappingProxyType(dict(kwargs))


@dataclass(frozen=True, slots=True)
class Student:
    id: int
    name: str
    results: tuple[CourseResult, ...] = ()
    skills: frozenset[str] = frozenset()
    # MappingProxyType не хешується, тому профіль виключено з __hash__
    # (але він бере участь у __eq__ - рівні об'єкти все одно мають рівні хеші).
    profile: Mapping[str, str] = field(default_factory=make_profile, hash=False)
    gpa: float = 0.0  # середній бал, перераховується при кожному pure update

    def result_for(self, course: str) -> CourseResult | None:
        return next((r for r in self.results if r.course == course), None)

    def with_skill(self, skill: str) -> Student:
        return replace(self, skills=self.skills | {skill})
