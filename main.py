from core import add_grade, add_skill, freeze, top_students, update_profile
from model import Student, make_profile


def main() -> None:
    s0 = Student(1, "Олена", profile=make_profile(faculty="ФЕП", group="ФеП-22"))
    s1 = add_grade(add_grade(s0, "ФП", 90), "ФП", 80)
    s2 = add_skill(add_grade(s1, "Матан", 70), "Python")
    s3 = update_profile(s2, group="ФеП-23")
    print("Початковий:", s0)
    print("Після оновлень:", s3)
    print("s0 не змінився:", s0.results == () and s0.gpa == 0.0)
    b = add_grade(Student(2, "Богдан"), "ФП", 95)
    print("Top:", [s.name for s in top_students([s3, b])])
    print("freeze:", freeze({"tags": {"a"}, "marks": [1, 2], "meta": {"k": [3]}}))


if __name__ == "__main__":
    main()
