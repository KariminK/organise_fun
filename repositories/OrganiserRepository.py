import os
from data.Group import Group

class OrganiserRepository:
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.file_path = os.path.join(self.dir_path, "groups.of")
        pass
    
    def exists(self):
        return os.path.exists(self.file_path)

    def load_groups(self):
        if not self.exists():
            return []
        
        with open(self.file_path) as f:
            groups = []
            for line in f:
                if(len(line.strip()) > 0):
                    groups.append(Group(line.strip()))
            return groups
    def create_group(self, group: Group):
        with open(self.file_path, "a") as f:
            f.write(group.name + "\n")
            group_dir = os.path.join(self.dir_path, "grupa_" + group.safe_name())
            lesson_dir = os.path.join(group_dir, "lekcje")
            materials_dir = os.path.join(group_dir, "materialy")
            projects_dir = os.path.join(group_dir, "projekty")
            os.mkdir(group_dir)
            os.mkdir(materials_dir)
            os.mkdir(lesson_dir)
            os.mkdir(projects_dir)
            return True