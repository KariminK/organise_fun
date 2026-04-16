from dataclasses import dataclass
from datetime import date

@dataclass
class Lesson:
    name: str
    created_at: str
    ended_at: str
    material_number: str
    
    @staticmethod
    def create(name: str, material_number: str):
        return Lesson(
            name=name,
            created_at=date.today(),
            ended_at="ONGOING",
            material_number=material_number
        )
    def safe_name(self):
        return self.name.replace(" ", "_").lower()