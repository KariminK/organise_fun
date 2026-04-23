from data.Group import Group
from data.Lesson import Lesson
from errors.GroupServiceErrors import GroupErrors
from repositories.GroupRepository import GroupRepository
from errors.RepositoryErrors import RepositoryErrors
import datetime

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

class GroupService:
    def __init__(self, repository: GroupRepository):
        self.group = None
        self.repository = repository
    
    def set_group(self, group: Group):
        self.group = group
        self.repository.set_group_path(group)

    def create_lesson(self, lesson_name, material_number):
        if len(lesson_name) < 3:
            return GroupErrors.LESSON_NAME_TOO_SHORT
        if not is_float(material_number):
            return GroupErrors.MATERIAL_NUMBER_NOT_DECIMAL
        new_lesson = Lesson.create(lesson_name, material_number)
        self.repository.create_lesson(new_lesson)
    
    def delete_lesson(self, lesson_name):
        if len(lesson_name) < 3: return GroupErrors.INVALID_LESSON_NAME

        result = self.repository.delete_lesson(Lesson(lesson_name, "", "", ""))
        
        return result
    
    def end_lesson(self, lesson_name):
        if len(lesson_name) < 3: return GroupErrors.INVALID_LESSON_NAME

        lesson = self.repository.select_lesson(lesson_name)
        
        if lesson == RepositoryErrors.NOT_FOUND:
            return RepositoryErrors.NOT_FOUND
        
        return self.repository.change_lesson_status(lesson_name, datetime.date.today())
    
    def list_lessons(self):
        return self.repository.load_lessons()

    def open_in_file(self, lesson_name):
        if len(lesson_name) < 3: return GroupErrors.INVALID_LESSON_NAME

        lesson = self.repository.select_lesson(lesson_name)
        
        if lesson == RepositoryErrors.NOT_FOUND:
            return RepositoryErrors.NOT_FOUND
                
        return self.repository.open_lesson_in_f(lesson)

    def open_in_vs(self, lesson_name):
        if len(lesson_name) < 3: return GroupErrors.INVALID_LESSON_NAME

        lesson = self.repository.select_lesson(lesson_name)
        
        if lesson == RepositoryErrors.NOT_FOUND:
            return RepositoryErrors.NOT_FOUND
        return self.repository.open_lesson_in_vs(lesson)