from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List


@dataclass
class Task:
    description: str
    time: str  # "HH:MM"
    frequency: str = "once"  # once, daily, weekly
    completed: bool = False

    def mark_complete(self):
        self.completed = True

    def next_occurrence(self):
        if self.frequency == "once":
            return None

        base_time = datetime.strptime(self.time, "%H:%M")

        if self.frequency == "daily":
            next_time = base_time + timedelta(days=1)
        elif self.frequency == "weekly":
            next_time = base_time + timedelta(weeks=1)
        else:
            return None

        return Task(self.description, next_time.strftime("%H:%M"), self.frequency)


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        self.tasks.append(task)


@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        self.pets.append(pet)

    def get_all_tasks(self):
        all_tasks = []
        for pet in self.pets:
            for task in pet.tasks:
                all_tasks.append((pet.name, task))
        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def sort_by_time(self):
        return sorted(
            self.owner.get_all_tasks(),
            key=lambda x: datetime.strptime(x[1].time, "%H:%M")
        )

    def filter_tasks(self, completed=None, pet_name=None):
        tasks = self.owner.get_all_tasks()

        if completed is not None:
            tasks = [t for t in tasks if t[1].completed == completed]

        if pet_name:
            tasks = [t for t in tasks if t[0] == pet_name]

        return tasks

    def detect_conflicts(self):
        times = {}
        conflicts = []

        for pet_name, task in self.owner.get_all_tasks():
            if task.time in times:
                conflicts.append((times[task.time], (pet_name, task)))
            else:
                times[task.time] = (pet_name, task)

        return conflicts

    def complete_task(self, task: Task, pet: Pet):
        task.mark_complete()

        new_task = task.next_occurrence()
        if new_task:
            pet.add_task(new_task)
