from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner("Courtney")

dog = Pet("Buddy", "Dog")
cat = Pet("Milo", "Cat")

owner.add_pet(dog)
owner.add_pet(cat)

dog.add_task(Task("Walk", "08:00", "daily"))
dog.add_task(Task("Feed", "09:00"))
cat.add_task(Task("Vet Visit", "08:00"))

scheduler = Scheduler(owner)

print("\n--- Today's Schedule ---")
for pet_name, task in scheduler.sort_by_time():
    print(f"{task.time} - {pet_name}: {task.description}")

conflicts = scheduler.detect_conflicts()
if conflicts:
    print("\n⚠️ Conflicts detected:")
    for c1, c2 in conflicts:
        print(f"{c1[0]} and {c2[0]} both have tasks at {c1[1].time}")
