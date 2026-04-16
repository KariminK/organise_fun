from dataclasses import dataclass
from data.Lesson import Lesson

@dataclass
class Project(Lesson):
    assigned_students: list[str]

