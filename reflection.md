# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Core user actions a pet owner should be able to perform:
1. Add a pet with details (name, breed, species, age, and any ongoing medical conditions).
2. Schedule recurring reminders for a pet — feedings, walks, medications, vet appointments.
3. Store vet/doctor contact info and medication details tied to a specific pet.
4. View today's task list showing everything that needs to happen for all pets.

Classes and responsibilities:
- **Task** — holds a single care activity (description, time, frequency, priority, completion status).
- **Pet** — stores pet profile info and owns a list of Tasks.
- **Owner** — holds the owner's name and a list of Pets; provides access to all tasks across pets.
- **Scheduler** — the "brain" that retrieves tasks from the Owner's pets and organises/prioritises them.

**b. Design changes**

The board view was not part of the original design. The initial UI displayed tasks as a vertical list, but that layout did not feel right — it was hard to get a quick visual overview of all pets and their tasks at once. Switching to a board view (rows = pets, columns = tasks) made the information much more accessible and easier to scan at a glance. This change was added after the core logic was already working, as an iterative improvement to the UI layer.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler sorts tasks primarily by time. For pets, almost every task is high priority — feeding, medication, walks, and vet appointments all need to happen on time. It is difficult to think of a genuinely low-priority pet care task. Because everything is urgent, sorting by time makes the most sense: it ensures the owner always sees what needs to happen next, regardless of the priority label, so nothing is missed during the day.

**b. Tradeoffs**

The conflict detection checks for tasks scheduled at the exact same time. It does not account for tasks that overlap in duration — for example, a 30-minute walk and a 15-minute feeding both starting at 08:00 would be flagged as a conflict even though some tasks can be done simultaneously (such as walking two dogs at once or feeding multiple pets at the same time). This tradeoff is reasonable because most pet care tasks are short and time-specific, so exact-time matching catches the most common scheduling mistakes without over-complicating the logic.

---

## 3. AI Collaboration

**a. How you used AI**

AI was used across all phases of the project: brainstorming the UML diagram, generating class skeletons, implementing scheduling logic, building the Streamlit UI, and debugging errors. The most effective prompts were specific and descriptive — for example, "I want the input fields to clear after I add a pet" produced a direct solution, while vague prompts like "fix the form" did not. Describing the board view in plain language ("rows = pets, columns = tasks, color-coded by priority") was enough for AI to translate the idea into working code. When debugging, pasting the exact error message always got a faster and more accurate fix than describing the problem in general terms.

**b. Judgment and verification**

When building the task completion interaction, AI suggested using a drag-and-drop interface (via the `streamlit-sortables` library). I chose a checkbox instead. Drag-and-drop would have required an external library, additional state management, and more complex event handling — all for a feature that a simple checkbox handles just as well. The checkbox is simpler to implement, easier to understand, and less likely to break. I verified the choice by thinking through what a pet owner actually needs: a quick, reliable way to mark a task done, not a fancy UI gesture.

---

## 4. Testing and Verification

**a. What you tested**

Five core behaviors were tested:
1. **Task completion** — `mark_complete()` sets the task's status to done.
2. **Task addition** — adding a task to a Pet increases its task count.
3. **Sort by time** — tasks are returned in chronological order.
4. **Daily recurrence** — marking a daily task complete creates a new task for the following day.
5. **Conflict detection** — the Scheduler correctly identifies two tasks scheduled at the same time.

Sort by time was the most important test. If sorting were broken, the board would display tasks in a random order instead of chronological order, making it confusing for a pet owner trying to follow their daily routine.

**b. Confidence**

The core scheduling behaviors work correctly and are covered by tests. However, there are untested areas: the app does not track a pet's birthday or end-of-life date, there is no dedicated owner profile section, and time input is not validated — entering "9am" instead of "09:00" would cause unexpected behavior. These are the areas that would be tested and addressed in the next iteration.

---

## 5. Reflection

**a. What went well**

The pet profiles feature came together well. Each pet holds its own tasks, supplies, medical conditions, and vet contact details in one place. Being able to open a pet's profile and see everything about that animal in a single view — health history, upcoming tasks, supply levels — felt like a complete and useful feature.

**b. What you would improve**

In the next iteration, I would add a pet's date of birth and an end-of-life date field to track the pet's age and lifespan more accurately. I would also add a dedicated owner profile section so the owner's personal details and preferences are separate from the pet data, rather than just a name field in the sidebar.

**c. Key takeaway**

The most important thing I learned was how to build a system from UML all the way to a working application — iteratively adding features, testing at each stage, and identifying and correcting bugs as they appeared. Starting with a clear design and building incrementally made it possible to keep the codebase organized even as new features were added throughout the project.
