from dataclasses import dataclass

@dataclass
class Group:
    name: str
    def safe_name(self):
        return self.name.replace(" ", "_").lower()