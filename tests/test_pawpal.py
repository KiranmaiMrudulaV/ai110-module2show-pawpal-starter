from datetime import date, timedelta
from pawpal_system import Owner, Pet, Task, Supply, Scheduler


def make_scheduler():
    owner = Owner(name="Test Owner")
    rex = Pet(name="Rex", species="dog")
    luna = Pet(name="Luna", species="cat")

    rex.add_task(Task(description="Walk", time="09:00", frequency="daily"))
    rex.add_task(Task(description="Feed", time="07:00", frequency="daily"))
    luna.add_task(Task(description="Feed", time="07:00", frequency="daily"))
    luna.add_task(Task(description="Play", time="15:00", frequency="weekly"))

    owner.add_pet(rex)
    owner.add_pet(luna)
    return Scheduler(owner=owner)


def test_task_mark_complete():
    task = Task(description="Walk", time="09:00")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_count():
    pet = Pet(name="Buddy", species="dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task(description="Walk", time="08:00"))
    assert len(pet.tasks) == 1


def test_sort_by_time():
    scheduler = make_scheduler()
    sorted_tasks = scheduler.sort_by_time()
    times = [t.time for _, t in sorted_tasks]
    assert times == sorted(times)


def test_daily_recurrence():
    owner = Owner(name="Alice")
    pet = Pet(name="Max", species="dog")
    today = date.today()
    pet.add_task(Task(description="Walk", time="08:00", frequency="daily", due_date=today))
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner)

    scheduler.mark_task_complete("Max", "Walk")
    assert len(pet.tasks) == 2
    assert pet.tasks[0].completed is True
    assert pet.tasks[1].due_date == today + timedelta(days=1)


def test_conflict_detection():
    scheduler = make_scheduler()
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) >= 1
    assert any("07:00" in c for c in conflicts)
