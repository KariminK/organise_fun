import os
# from organiser import Organiser

# os.system("clear")
# print("organise_fun(#): Welcome to organise_fun!")

# main_organiser = Organiser(".")

from ui.OrganiserCLI import OrganiserCLI
from services.GroupService import GroupService
from services.OrganiserService import OrganiserService
from repositories.GroupRepository import GroupRepository
from repositories.OrganiserRepository import OrganiserRepository

group_repo = GroupRepository(os.path.join(os.path.curdir, "build"))
organiser_repo = OrganiserRepository(os.path.join(os.path.curdir, "build"))

group_service = GroupService(group_repo)
organiser_service = OrganiserService(organiser_repo)

cli = OrganiserCLI(group_service, organiser_service)

cli.run()