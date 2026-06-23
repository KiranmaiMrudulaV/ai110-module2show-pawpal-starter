from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional


@dataclass
class MedicalCondition:
    name: str
    date_diagnosed: date
    medication: str
    dose: str
    notes: str = ""


@dataclass
class Supply:
    name: str
    quantity_bought: float
    daily_amount: float
    bought_date: date
    unit: str
    reminder_days_before: int = 3

    def days_remaining(self) -> int:
        from datetime import date
        days_used = (date.today() - self.bought_date).days
        quantity_left = self.quantity_bought - (days_used * self.daily_amount)
        if quantity_left <= 0:
            return 0
        return int(quantity_left / self.daily_amount)


    def needs_reorder(self) -> bool:
        return self.days_remaining() <= self.reminder_days_before



@dataclass
class Task:
    description: str
    time: str
    due_date: date = field(default_factory=date.today)
    frequency: str = "once"
    priority: str = "medium"
    completed: bool = False
    dose_amount: str = ""

    def mark_complete(self) -> Optional["Task"]:
        self.completed = True
        if self.frequency == "daily":
            return Task(
                description=self.description,
                time=self.time,
                frequency=self.frequency,
                due_date=self.due_date + timedelta(days=1),
                priority=self.priority,
                dose_amount=self.dose_amount,
            )
        elif self.frequency == "weekly":
            return Task(
                description=self.description,
                time=self.time,
                frequency=self.frequency,
                due_date=self.due_date + timedelta(weeks=1),
                priority=self.priority,
                dose_amount=self.dose_amount,
            )
        return None


@dataclass
class Pet:
    name: str
    species: str
    breed: str = ""
    age: int = 0
    vet_name: str = ""
    vet_phone: str = ""
    breed_info: str = ""
    tasks: list = field(default_factory=list)
    supplies: list = field(default_factory=list)
    medical_conditions: list = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def list_tasks(self) -> list:
        return self.tasks

    def get_pending_tasks(self) -> list:
        return [t for t in self.tasks if not t.completed]

    def add_supply(self, supply: Supply) -> None:
        self.supplies.append(supply)

    def check_supplies(self) -> list:
        warnings = []
        for supply in self.supplies:
            if supply.needs_reorder():
                warnings.append(
                    f"Low supply: {supply.name} - only {supply.days_remaining()} days left ({supply.unit})"
                )
        return warnings



@dataclass
class Owner:
    name: str
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_all_tasks(self) -> list:
        result = []
        for pet in self.pets:
            for task in pet.tasks:
                result.append((pet, task))
        return result



class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def sort_by_time(self, tasks: list = None) -> list:
        if tasks is None:
            tasks = self.owner.get_all_tasks()
        return sorted(tasks, key=lambda pair: pair[1].time)

    def filter_tasks(self, pet_name: str = None, completed: bool = None) -> list:
        results = self.owner.get_all_tasks()
        if pet_name is not None:
            results = [(p, t) for p, t in results if p.name.lower() == pet_name.lower()]
        if completed is not None:
            results = [(p, t) for p, t in results if t.completed == completed]
        return results

    def get_todays_schedule(self) -> list:
        today = date.today()
        todays = [
            (p, t) for p, t in self.owner.get_all_tasks()
            if not t.completed and t.due_date == today
        ]
        return self.sort_by_time(todays)


    def get_schedule_range(self, days: int) -> dict:
        today = date.today()
        schedule = {}
        for i in range(days):
            day = today + timedelta(days=i)
            tasks_that_day = [
                (p, t) for p, t in self.owner.get_all_tasks()
                if t.due_date == day
            ]
            schedule[day] = self.sort_by_time(tasks_that_day)
        return schedule


    def detect_conflicts(self) -> list:
        time_map = {}
        for pet, task in self.owner.get_all_tasks():
            key = (task.time, task.due_date)
            time_map.setdefault(key, []).append((pet, task))

        warnings = []
        for (t, d), entries in time_map.items():
            if len(entries) > 1:
                names = [f"{p.name}'s '{tk.description}'" for p, tk in entries]
                warnings.append(f"Conflict at {t} on {d}: {', '.join(names)}")
        return warnings


    def mark_task_complete(self, pet_name: str, task_desc: str) -> bool:
        for pet in self.owner.pets:
            if pet.name.lower() == pet_name.lower():
                for task in pet.tasks:
                    if task.description.lower() == task_desc.lower() and not task.completed:
                        next_task = task.mark_complete()
                        if next_task:
                            pet.add_task(next_task)
                        return True
        return False

