# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Add two new algorithmic capabilities to the `Scheduler` class in `pawpal_system.py`:
1. `suggest_next_task()` — score every pending task using a weighted urgency formula (`priority_weight × (1 + days_overdue)`) and return the highest-scoring `(pet, task)` pair.
2. `get_overdue_tasks()` — return all incomplete tasks whose `due_date` is before today, sorted by most overdue first.

Also update `main.py` to demonstrate both methods in the CLI output, and add both to the Smarter Scheduling table in `README.md`.

**What did the agent do?**

1. Read `pawpal_system.py` to understand the existing `Scheduler` class structure and where to insert the new methods.
2. Added `suggest_next_task()` above `mark_task_complete()` — loops all tasks, computes a score for each pending task using `priority_weight × (1 + days_overdue)`, and tracks the best.
3. Added `get_overdue_tasks()` directly after — filters for tasks where `due_date < today` and `completed == False`, then sorts by days overdue descending.
4. Read `main.py` and appended two new print blocks after the mark-complete demo: one calling `suggest_next_task()` and one calling `get_overdue_tasks()`.
5. Updated the Smarter Scheduling table in `README.md` with one row for each new method.

**What did you have to verify or fix manually?**

- Confirmed the urgency scoring formula matched the intended logic: a task overdue by 0 days still gets a base score of `weight × 1`, not `weight × 0`.
- Verified `get_overdue_tasks()` excludes completed tasks — important because completed daily tasks stay in the list with their old `due_date`.
- Checked that the `Optional` return type annotation on `suggest_next_task()` was already imported at the top of the file (it was, via `from typing import Optional`).

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | | |
| **Prompt** | | |
| **Response summary** | | |
| **What was useful** | | |
| **Problems noticed** | | |
| **Decision** | | |

**Which approach did you use in your final implementation and why?**

<!-- Your conclusion -->
