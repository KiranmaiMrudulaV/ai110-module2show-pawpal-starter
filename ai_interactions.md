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

**Task:** Add a priority-first sort method to the `Scheduler` class.

| | Option A — Vague prompt | Option B — Specific prompt |
|-|------------------------|---------------------------|
| **Model / tool used** | ChatGPT (GPT-4o) | ChatGPT (GPT-4o) |
| **Prompt** | "add a sorting feature to my pet scheduler" | Pasted the existing `sort_by_time()` method as context, explained that tasks is a list of `(Pet, Task)` tuples, and asked for a new method `sort_by_priority_then_time` sorting high → medium → low, then by time within each group |
| **Response summary** | Returned a working `sort_by_priority_then_time` method using `priority_order` dict and `sorted()` with a tuple key. No explanation of how it fits into the existing class structure. | Returned the same method but with `pair[1].priority.lower()` for safety against mixed-case input, and a clear explanation of each sort level. Output matched the exact structure of the existing codebase. |
| **What was useful** | Quick — no setup needed. The core logic was correct. | More accurate and robust. The `.lower()` call handles edge cases. The explanation confirmed the logic was right before adding it to the code. |
| **Problems noticed** | Did not know the actual class structure so it assumed a simpler setup. The result would need adjustments if the codebase differed from its assumptions. | None — the output matched the existing code directly and was ready to use. |
| **Decision** | Not used — too generic without knowing the actual code structure. | Used — matched the codebase exactly and required no changes. |

**Which approach did you use in your final implementation and why?**

Option B (specific prompt with context) was used. Providing the existing `sort_by_time()` method as context gave ChatGPT enough information to produce a method that fit directly into the codebase without modification. The vague prompt produced a structurally similar result, but because it had no context about the `(Pet, Task)` tuple structure or the existing class design, it would have required more manual review and adjustment to integrate safely. The key lesson: the more specific the prompt, the less work is needed after the AI responds.
