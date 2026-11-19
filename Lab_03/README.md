# Лабораторна робота №3 — Незмінні структури даних

**Варіант 3. Студентська успішність.** Іщенко Стефанія, ФеП-22.

## Модель (`model.py`)
| Сутність | Як заморожено |
|---|---|
| `CourseResult(course, grades)` | `NamedTuple`; оцінки — `tuple[int, ...]` |
| `Student(id, name, results, skills, profile, gpa)` | `@dataclass(frozen=True, slots=True)` |
| `results` | `tuple[CourseResult, ...]` замість list |
| `skills` | `frozenset[str]` замість set |
| `profile` | `MappingProxyType` над **копією** dict (`make_profile`) |

## Pure-оновлення (`core.py`)
- `add_grade(student, course, grade)` — конкатенація tuple + `replace`, автоматично `recalc_gpa`;
- `add_skill` / `remove_skill` — операції `frozenset` (`|`, `-`);
- `update_profile(**changes)` — новий `MappingProxyType`;
- `recalc_gpa` — перерахунок середнього; `grades_average` кешується `@lru_cache` (ключ — хешований tuple);
- `top_students`, `with_skills` (підмножина frozenset), `freeze(obj)` — глибоке заморожування.

## Хешованість
`MappingProxyType` **не хешується**, тому поле `profile` оголошене з `field(hash=False)`:
воно бере участь у `==`, але не в `__hash__`. Контракт «рівні об'єкти ⇒ рівні хеші»
зберігається, і `Student` можна класти в `set` / використовувати як ключ `dict`
(перевіряє `test_hashability`).

## Тести
- `tests/test_immutability.py` — немутація, `FrozenInstanceError`, read-only профіль,
  копіювання джерела профілю, хешованість, `lru_cache` (`cache_info`), `freeze`.
- `tests/test_performance.py` — та сама послідовність з 2000 оновлень у мутабельній
  (`mutable_legacy.py`) та незмінній моделі.

## Порівняння часу (`pytest -q --durations=5`)
```
0.07s call  tests/test_performance.py::test_perf_immutable_after
0.03s call  tests/test_performance.py::test_perf_mutable_before
```

## Висновок
Незмінність дає референтну прозорість, безпечне спільне використання об'єктів і
можливість хешувати/кешувати (`lru_cache`, ключі dict). Ціна — створення нових
об'єктів на кожне оновлення: на 2000 оновленнях незмінна модель ~2× повільніша
(десятки мілісекунд — для навчальних і більшості бізнес-задач несуттєво).
Також `deepcopy` не працює з `mappingproxy`, але для незмінних об'єктів він і не потрібен.

## Запуск
```bash
pip install -r requirements.txt
pytest -q --durations=5
mypy . && black --check . && ruff check .
python main.py
```
