from repositories.OrganiserRepository import OrganiserRepository
from errors.OrganiserServiceErrors import OrganiserServiceErrors
from data.Group import Group
class OrganiserService:
    def __init__(self, repository: OrganiserRepository):
        self.repository = repository
    
    def list_groups(self):
        return self.repository.load_groups()
    
    def list_students(self, group_name):
        return self.repository.load_students(group_name)

    def create_group(self, group_name):
        if len(group_name) < 3: return OrganiserServiceErrors.GROUP_NAME_TOO_SHORT
        group = Group(group_name, [])
        return self.repository.create_group(group)
    
    def add_student(self, group_name, student_name):
        if len(group_name) < 3 or len(student_name) < 3: return OrganiserServiceErrors.GROUP_NAME_TOO_SHORT
        return self.repository.add_student_to_group(group_name, student_name)