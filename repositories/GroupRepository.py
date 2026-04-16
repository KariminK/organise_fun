import os, shutil

from data.Lesson import Lesson
from errors.RepositoryErrors import RepositoryErrors
from data.Group import Group

class GroupRepository:
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.file_path = os.path.join(self.dir_path, "lessons.of")
    def set_group_path(self, group: Group):
        self.dir_path = os.path.join(self.dir_path, f"grupa_{group.safe_name()}")
    def create_lesson(self, lesson: Lesson):
        with open(self.file_path, "a") as f:
            f.write(f"{lesson.name};{lesson.created_at};ONGOING;{lesson.material_number}\n")
        lesson_path = os.path.join(self.dir_path, "lekcje", lesson.safe_name())
        os.mkdir(lesson_path)
    def delete_lesson(self, lesson: Lesson):
        lesson_path = os.path.join(self.dir_path, "lekcje", lesson.safe_name())
        if not os.path.exists(lesson_path):
            return RepositoryErrors.DIRECTORY_NOT_EXIST
        
        with open(self.file_path, "r+") as f:
            lesson_lines = f.readlines()
            f.seek(0)
            f.truncate()

            for lesson_line in lesson_lines:
                if not lesson_line.strip() or lesson_line == "":
                    continue
                splitted_lesson = lesson_line.strip().split(";")
                if len(splitted_lesson) < 4: return RepositoryErrors.INVALID_FILE_FORMAT
                if not splitted_lesson[0] == lesson.name:
                    f.write(lesson_line.strip() + "\n")
        shutil.rmtree(lesson_path)
        return lesson
    def load_lessons(self):
        if not os.path.exists(self.file_path): return RepositoryErrors.FILE_NOT_EXIST
        with open(self.file_path) as f:
            lesson_lines = f.readlines()

            lessons = []

            for lesson_line in lesson_lines:
                if not lesson_line.strip(): continue

                splitted_lesson = lesson_line.split(";")
                if(len(splitted_lesson) < 4): return RepositoryErrors.INVALID_FILE_FORMAT
                
                name, created_at, ended_at, material_number = splitted_lesson

                lesson = Lesson(name, created_at, ended_at, material_number)

                lessons.append(lesson)
            
            return lessons
    def open_lesson_in_f(self, lesson):
        lesson_path = os.path.join(self.dir_path, "lekcje", lesson.safe_name())
        os.system(f"xdg-open {lesson_path}")
    def open_lesson_in_vs(self, lesson):
        lesson_path = os.path.join(self.dir_path, "lekcje", lesson.safe_name())
        os.system(f"code {lesson_path}")