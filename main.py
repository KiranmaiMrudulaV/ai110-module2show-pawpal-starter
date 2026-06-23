from datetime import date
from pawpal_system import Owner, Pet, Task, Supply, Scheduler


def main():
    owner = Owner(name="Jordan")

    mochi = Pet(name="Mochi", species="cat", breed="Persian", age=3,
                vet_name="Dr. Smith", vet_phone="555-1234",
                breed_info="Persians need daily grooming.")

    biscuit = Pet(name="Biscuit", species="dog", breed="Labrador", age=5,
                  vet_name="Dr. Smith", vet_phone="555-1234")

    mochi.add_task(Task(description="Feeding", time="08:00", frequency="daily", priority="high"))
    mochi.add_task(Task(description="Playtime", time="18:00", frequency="daily", priority="medium"))
    mochi.add_task(Task(description="Vet appointment", time="10:00", frequency="once", priority="high"))

    biscuit.add_task(Task(description="Morning walk", time="07:30", frequency="daily", priority="high"))
    biscuit.add_task(Task(description="Feeding", time="08:00", frequency="daily", priority="high"))
    biscuit.add_task(Task(description="Evening walk", time="17:00", frequency="daily", priority="medium"))

    biscuit.add_supply(Supply(name="Kibble", quantity_bought=500, daily_amount=50,
                               bought_date=date(2026, 6, 15), unit="grams"))

    owner.add_pet(mochi)
    owner.add_pet(biscuit)

    scheduler = Scheduler(owner=owner)

    print("=" * 52)
    print(f"  TODAY'S SCHEDULE for {owner.name}")
    print("=" * 52)
    for pet, task in scheduler.get_todays_schedule():
        status = "done" if task.completed else "todo"
        print(f"  [{status}] {task.time}  {pet.name:10s}  {task.description:20s}  [{task.priority}]")

    print("\nCONFLICT CHECK:")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for w in conflicts:
            print(f"  [!] {w}")
    else:
        print("  No conflicts detected.")

    print("\nSUPPLY CHECK:")
    for pet in owner.pets:
        for warning in pet.check_supplies():
            print(f"  {pet.name}: {warning}")

    print("\nMARKING 'Morning walk' complete for Biscuit...")
    scheduler.mark_task_complete("Biscuit", "Morning walk")
    print(f"  Biscuit now has {len(biscuit.tasks)} tasks (added tomorrow's recurrence)")


if __name__ == "__main__":
    main()
