from pawpal_system import Task, Pet, Owner, Scheduler

def test_task_completion():
    task = Task("Feed", "09:00")
    task.mark_complete()
    assert task.completed is True

def test_add_task():
    pet = Pet("Buddy", "Dog")
    pet.add_task(Task("Walk", "08:00"))
    assert len(pet.tasks) == 1

def test_sorting():
    owner = Owner("Test")
    pet = Pet("Dog", "Dog")

    pet.add_task(Task("Late", "12:00"))
    pet.add_task(Task("Early", "08:00"))

    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    sorted_tasks = scheduler.sort_by_time()
    assert sorted_tasks[0][1].description == "Early"

def test_conflicts():
    owner = Owner("Test")
    pet1 = Pet("Dog", "Dog")
    pet2 = Pet("Cat", "Cat")

    task1 = Task("Walk", "08:00")
    task2 = Task("Feed", "08:00")

    pet1.add_task(task1)
    pet2.add_task(task2)

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    scheduler = Scheduler(owner)

    assert len(scheduler.detect_conflicts()) > 0
