from repositories.OrganiserRepository import OrganiserRepository
from errors.OrganiserServiceErrors import OrganiserServiceErrors
from data.Group import Group
class OrganiserService:
    def __init__(self, repository: OrganiserRepository):
        self.repository = repository
    
    def list_groups(self):
        result = self.repository.load_groups()
        return result
    
    def create_group(self, group_name):
        if len(group_name) < 3: return OrganiserServiceErrors.GROUP_NAME_TOO_SHORT

        group = Group(group_name)
        result = self.repository.create_group(group)
        return result