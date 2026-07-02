# PawPal+ (Module 2 Project)

**PawPal+** is a smart pet care management system that helps owners stay on top of daily routines — feedings, walks, medications, vet appointments, and supplies — using algorithmic scheduling and a visual board-view UI.

---

## Features

- **Pet profiles** — store name, species, breed, age, vet name, vet phone, and breed/species notes per pet
- **Task scheduling** — add tasks with time, due date, frequency (once / daily / weekly), priority (high / medium / low), and optional dose amount
- **Board view** — Today Board and Weekly Board show tasks as color-coded cards (red = high, orange = medium, yellow = low, green = done), one row per pet/day
- **Mark tasks done** — checkbox on each card marks the task complete; daily and weekly tasks automatically schedule the next occurrence
- **Conflict detection** — warns when two tasks are scheduled at the same time
- **Supply tracking** — tracks quantity bought, daily usage, and warns when stock is running low (configurable lead time)
- **Medical conditions** — record diagnosis date, medication, dose, and notes per condition per pet
- **Data persistence** — all data is saved to `data.json` so the app remembers everything between restarts
- **4-Week list view** — expandable day-by-day task list for the next 28 days

---

## UI Formatting

PawPal+ uses a kanban-style board view built with Streamlit and custom HTML/CSS.

### Board layout

Tasks are displayed as cards arranged in rows (one row per pet) and columns (one card per task). This makes it easy to scan all pets and their upcoming tasks at a glance without scrolling through a long list.

### Card design

Each card is built using `st.container(border=True)` with an inner `st.markdown(unsafe_allow_html=True)` block for custom styling:

- **Colored top strip** — a 5px horizontal bar at the top of each card signals priority at a glance
- **Priority badge** — a colored pill label (e.g. `HIGH`, `MEDIUM`, `LOW`) appears on each pending task card
- **Done checkbox** — `st.checkbox` inside the container marks the task complete without leaving the card
- **Details expander** — `st.expander("Details")` inside the same container shows pet name, vet info, dose, and medical conditions

### Color coding

| State | Strip color | Badge color |
|-------|-------------|-------------|
| High priority | Red `#dc3545` | Red |
| Medium priority | Orange `#fd7e14` | Orange |
| Low priority | Yellow `#ffc107` | Yellow |
| Completed | Green `#28a745` | Green — text is struck through |

### Horizontal scrolling

When a pet has many tasks, the card row scrolls horizontally. This is enabled by injecting a CSS rule targeting Streamlit's internal `div[data-testid="stHorizontalBlock"]` via `st.markdown(unsafe_allow_html=True)`.

### Libraries used

- **Streamlit** — UI framework (`st.container`, `st.columns`, `st.checkbox`, `st.expander`, `st.tabs`, `st.form`)
- **Custom HTML/CSS** — injected via `st.markdown(unsafe_allow_html=True)` for card styling, color strips, badges, and horizontal scroll

---

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sort by time | `Scheduler.sort_by_time()` | Uses `sorted()` with a lambda on the `time` string (HH:MM format sorts correctly as a string) |
| Filter by pet / status | `Scheduler.filter_tasks(pet_name, completed)` | Returns only matching (Pet, Task) pairs |
| Today's schedule | `Scheduler.get_todays_schedule()` | Pending tasks for today, sorted by time |
| Schedule range | `Scheduler.get_schedule_range(days)` | Returns dict of `{date: [(pet, task)...]}` for N days ahead |
| Conflict detection | `Scheduler.detect_conflicts()` | Flags any two tasks sharing the same time and due date; returns warning strings |
| Recurring tasks | `Task.mark_complete()` + `Scheduler.mark_task_complete()` | Daily tasks reschedule +1 day, weekly tasks +7 days using `timedelta` |
| Priority-first sort | `Scheduler.sort_by_priority_then_time()` | Sorts high → medium → low, then by time within each group. Alternative to time-first sort for owners who want critical tasks grouped at the top. |
| Suggest next task | `Scheduler.suggest_next_task()` | Scores every pending task using `priority_weight × (1 + days_overdue)` (high=3, medium=2, low=1) and returns the highest-scoring `(pet, task)` pair |
| Overdue tasks | `Scheduler.get_overdue_tasks()` | Returns all incomplete tasks whose `due_date` is before today, sorted by most overdue first |

---

## 🖥️ Sample CLI Output

Running `python main.py`:

```
====================================================
  TODAY'S SCHEDULE for Jordan
====================================================
  [todo] 07:30  Biscuit     Morning walk          [high]
  [todo] 08:00  Mochi       Feeding               [high]
  [todo] 08:00  Biscuit     Feeding               [high]
  [todo] 10:00  Mochi       Vet appointment       [high]
  [todo] 17:00  Biscuit     Evening walk          [medium]
  [todo] 18:00  Mochi       Playtime              [medium]

PRIORITY-FIRST SCHEDULE:
  [high  ] 07:30  Biscuit     Morning walk
  [high  ] 08:00  Mochi       Feeding
  [high  ] 08:00  Biscuit     Feeding
  [high  ] 10:00  Mochi       Vet appointment
  [medium] 17:00  Biscuit     Evening walk
  [medium] 18:00  Mochi       Playtime

CONFLICT CHECK:
  [!] Conflict at 08:00 on 2026-07-02: Mochi's 'Feeding', Biscuit's 'Feeding'

SUPPLY CHECK:
  Biscuit: Low supply: Kibble - only 0 days left (grams)

MARKING 'Morning walk' complete for Biscuit...
  Biscuit now has 4 tasks (added tomorrow's recurrence)

SUGGESTED NEXT TASK:
  -> Mochi: 'Feeding' at 08:00 [high] due 2026-07-02

OVERDUE TASKS:
  No overdue tasks.
```

---

## 📸 Demo Walkthrough

1. **Launch the app** — run `streamlit run app.py`. The sidebar loads your saved data automatically (or prompts you to enter your name if starting fresh).
2. **Add a pet** — fill in the pet's name, species, breed, age, vet details, and any breed notes in the sidebar form. Click **Add Pet** — the form clears and the pet appears immediately.
3. **Schedule tasks** — go to the **Add Task / Supply** tab. Pick a pet, describe the task (e.g. "Morning walk"), set the time, due date, frequency, and priority. Daily and weekly tasks will auto-reschedule when marked done.
4. **View the Today Board** — the **Today Board** tab shows one row per pet. Each task appears as a color-coded card (red = high priority, orange = medium, yellow = low). Pending tasks come first sorted by time; completed tasks appear at the end in green with strikethrough text.
5. **Mark a task done** — tick the **Done** checkbox on any card. The card turns green, moves to the end of the row, and if the task is daily or weekly the next occurrence is added automatically.
6. **Check conflicts and supply warnings** — conflict warnings and low-supply alerts appear at the top of the Today Board so nothing is missed.
7. **Weekly view** — the **Weekly Board** tab shows the same card layout but organized by day for the next 7 days.
8. **4-Week list** — the **4-Week List** tab shows an expandable table for each day over the next 28 days.
9. **Pet health** — the **Pets & Health** tab shows full profiles including medical conditions. Add a new condition directly from the expander; the form clears after saving.
10. **Data persists** — close and reopen the app. All pets, tasks, supplies, and conditions reload from `data.json` automatically.

---

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Run with verbose output:
python -m pytest -v
```

### What the tests cover

| Test | What it verifies |
|------|-----------------|
| `test_task_mark_complete` | `mark_complete()` sets `completed = True` |
| `test_add_task_increases_count` | Adding a task increases the pet's task list length |
| `test_sort_by_time` | Tasks are returned in chronological (HH:MM) order |
| `test_daily_recurrence` | Marking a daily task done creates a new task for the next day |
| `test_conflict_detection` | Scheduler flags two tasks at the same time on the same date |

### Test output

```
============================= test session starts =============================
platform win32 -- Python 3.14.0, pytest-9.0.3, pluggy-1.6.0
collecting ... collected 5 items

tests/test_pawpal.py::test_task_mark_complete PASSED                     [ 20%]
tests/test_pawpal.py::test_add_task_increases_count PASSED               [ 40%]
tests/test_pawpal.py::test_sort_by_time PASSED                           [ 60%]
tests/test_pawpal.py::test_daily_recurrence PASSED                       [ 80%]
tests/test_pawpal.py::test_conflict_detection PASSED                     [100%]

============================== 5 passed in 0.08s ==============================
```

**Confidence level: ★★★★☆** — Core scheduling behaviors are fully verified. Time format validation and edge cases like empty pet lists or duplicate supply entries are areas for future testing.

---

## Data Persistence

PawPal+ automatically saves all data to `data.json` so nothing is lost between sessions.

### What gets saved

Every object in the system serializes itself via a `to_dict()` method:

```
Owner → pets[]
  └── Pet → tasks[], supplies[], medical_conditions[]
        ├── Task → description, time, due_date, frequency, priority, completed, dose_amount
        ├── Supply → name, quantity_bought, daily_amount, bought_date, unit, reminder_days_before
        └── MedicalCondition → name, date_diagnosed, medication, dose, notes
```

### When data is saved

`save_to_json(owner)` is called in `app.py` after every user action:
- Marking a task done
- Adding a new pet
- Adding a new task or supply
- Adding a medical condition

### When data is loaded

On startup, `app.py` calls `load_from_json()`. If `data.json` exists it reconstructs the full `Owner` object via `from_dict()` on each class. If the file is missing (first run), the app starts fresh.

### Why `data.json` is in `.gitignore`

The file contains personal pet data specific to each user. Committing it would overwrite another user's data when they pull the repo. Each user's `data.json` lives only on their own machine.

---

## Getting started

### Setup

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

### Run the CLI demo

```bash
python main.py
```
