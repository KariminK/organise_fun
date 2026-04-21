from dataclasses import dataclass

@dataclass
class Group:
    name: str
    student_names: list[str]
    def safe_name(self):
        return self.name.replace(" ", "_").lower()