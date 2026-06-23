from dataclasses import dataclass, field
from datetime import date
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
        pass  # TODO

    def needs_reorder(self) -> bool:
        pass  # TODO


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
        pass  # TODO


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
        pass  # TODO

    def list_tasks(self) -> list:
        pass  # TODO

    def get_pending_tasks(self) -> list:
        pass  # TODO

    def add_supply(self, supply: Supply) -> None:
        pass  # TODO

    def check_supplies(self) -> list:
        pass  # TODO


@dataclass
class Owner:
    name: str
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass  # TODO

    def get_all_tasks(self) -> list:
        pass  # TODO


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def sort_by_time(self, tasks: list = None) -> list:
        pass  # TODO

    def filter_tasks(self, pet_name: str = None, completed: bool = None) -> list:
        pass  # TODO

    def get_todays_schedule(self) -> list:
        pass  # TODO

    def get_weekly_schedule(self) -> dict:
        pass  # TODO

    def get_schedule_range(self, days: int) -> dict:
        pass  # TODO

    def detect_conflicts(self) -> list:
        pass  # TODO

    def mark_task_complete(self, pet_name: str, task_desc: str) -> bool:
        pass  # TODO
