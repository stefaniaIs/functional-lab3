from dataclasses import FrozenInstanceError
from types import MappingProxyType

import pytest

from core import (
    add_grade,
    add_skill,
    freeze,
    grades_average,
    remove_skill,
    top_students,
    update_profile,
    with_skills,
)
from model import CourseResult, Student, make_profile


def build_student() -> Student:
    s = Student(1, "Olena", profile=make_profile(faculty="FEP", group="22"))
    return add_grade(add_grade(s, "FP", 90), "Math", 70)


@pytest.fixture
def student() -> Student:
    return build_student()


def test_add_grade_no_mutation(student: Student) -> None:
    snapshot = build_student()  # незалежна рівна копія (deepcopy не вміє mappingproxy)
    new = add_grade(student, "FP", 100)
    assert student == snapshot
    assert new is not student
    assert new.result_for("FP") == CourseResult("FP", (90, 100))
    assert student.result_for("FP") == CourseResult("FP", (90,))


def test_gpa_recalculated(student: Student) -> None:
    assert student.gpa == 80.0
    assert add_grade(student, "Math", 100).gpa == pytest.approx(86.67)


def test_new_course_created(student: Student) -> None:
    new = add_grade(student, "Physics", 60)
    assert [r.course for r in new.results] == ["FP", "Math", "Physics"]


def test_invalid_grade(student: Student) -> None:
    with pytest.raises(ValueError):
        add_grade(student, "FP", 101)


def test_skills_frozenset(student: Student) -> None:
    s2 = add_skill(student, "  Python ")
    assert s2.skills == frozenset({"python"})
    assert student.skills == frozenset()
    assert remove_skill(s2, "python").skills == frozenset()
    assert isinstance(s2.skills, frozenset)


def test_frozen_dataclass(student: Student) -> None:
    with pytest.raises(FrozenInstanceError):
        student.name = "X"  # type: ignore[misc]


def test_profile_read_only(student: Student) -> None:
    with pytest.raises(TypeError):
        student.profile["faculty"] = "changed"  # type: ignore[index]


def test_make_profile_copies_source() -> None:
    src = {"faculty": "FEP"}
    p = make_profile(**src)
    src["faculty"] = "hacked"
    assert p["faculty"] == "FEP"


def test_update_profile(student: Student) -> None:
    s2 = update_profile(student, group="23")
    assert s2.profile["group"] == "23" and student.profile["group"] == "22"
    assert isinstance(s2.profile, MappingProxyType)


def test_hashability(student: Student) -> None:
    other = add_grade(student, "FP", 50)
    index = {student: "old", other: "new"}
    assert len({student, other}) == 2
    assert index[student] == "old"
    assert hash(student) == hash(build_student())


def test_tuple_of_grades_is_immutable(student: Student) -> None:
    with pytest.raises(AttributeError):
        student.results[0].grades.append(1)  # type: ignore[attr-defined]


def test_top_and_skill_filter(student: Student) -> None:
    other = add_skill(add_grade(Student(2, "B"), "FP", 95), "python")
    assert [s.id for s in top_students([student, other], 1)] == [2]
    assert with_skills([student, other], {"python"}) == (other,)


def test_lru_cache() -> None:
    grades_average.cache_clear()
    grades_average((90, 80))
    grades_average((90, 80))
    info = grades_average.cache_info()
    assert info.hits == 1 and info.misses == 1


def test_freeze_deep() -> None:
    f = freeze({"a": [1, {"b": {2}}]})
    assert isinstance(f, MappingProxyType)
    assert f["a"] == (1, MappingProxyType({"b": frozenset({2})}))
