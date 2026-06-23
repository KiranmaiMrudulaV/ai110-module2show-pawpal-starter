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

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
