import os
from data.Group import Group
from errors.RepositoryErrors import RepositoryErrors

class OrganiserRepository:
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.file_path = os.path.join(self.dir_path, "groups.of")
        pass
    
    def exists(self):
        return os.path.exists(self.file_path)

    def add_student_to_group(self, group_name, student_name):
        with open(self.file_path, "r+") as f:
            group_lines = f.readlines(0)
            f.seek(0)
            for group_line in group_lines:
                if not group_line or group_line == "":
                    continue

                splitted_group = group_line.split(";")
                if len(splitted_group) < 2: return RepositoryErrors.INVALID_FILE_FORMAT
                
                name, students_string = splitted_group

                if name == group_name:
                    students = students_string.strip().split(",")
                    if students_string.strip() != "":
                        students.append(student_name)
                        new_group = Group(name, students)
                        f.write(f"{new_group.name};{",".join(new_group.student_names)}\n")
                    else:
                        f.write(f"{name};{student_name}\n")
                else:
                    f.write(group_line)

    def load_students(self, group_name):
        if not self.exists():
            return []

        with open(self.file_path) as f:
            groups = []
            for group_line in f:
                splitted_group = group_line.strip().split(";")
                if len(splitted_group) < 2: return RepositoryErrors.INVALID_FILE_FORMAT
                name, student_string = splitted_group
                if name == group_name:
                    return student_string.strip().split(",")

    def load_groups(self):
        if not self.exists():
            return []
        
        with open(self.file_path) as f:
            groups = []
            for group_line in f:
                splitted_group = group_line.strip().split(";")
                if len(splitted_group) < 2: return RepositoryErrors.INVALID_FILE_FORMAT
                name, student_string = splitted_group
                groups.append(Group(name, student_string.split(",")))
            return groups
    def create_group(self, group: Group):
        with open(self.file_path, "a") as f:
            student_string = ",".join(group.student_names)
            f.write(f"{group.name};{student_string}\n")
            group_dir = os.path.join(self.dir_path, "grupa_" + group.safe_name())
            lesson_dir = os.path.join(group_dir, "lekcje")
            materials_dir = os.path.join(group_dir, "materialy")
            projects_dir = os.path.join(group_dir, "projekty")
            os.mkdir(group_dir)
            os.mkdir(materials_dir)
            os.mkdir(lesson_dir)
            os.mkdir(projects_dir)
            return True