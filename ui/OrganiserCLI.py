from services.GroupService import GroupService
from services.OrganiserService import OrganiserService
from errors.OrganiserServiceErrors import OrganiserServiceErrors
from errors.GroupServiceErrors import GroupErrors
from errors.RepositoryErrors import RepositoryErrors
import os

class OrganiserCLI:
    def __init__(self, group_service: GroupService, organiser_service: OrganiserService ):
        self.group_service = group_service
        self.organiser_service = organiser_service

    def print(self, text):
        if self.group_service.group:
            print(f"organise_fun({self.group_service.group.name}): {text}")
        else:
            print(f"organise_fun(#): {text}")
    
    def input(self, text):
        if self.group_service.group:
            return input(f"organise_fun({self.group_service.group.name}): {text}")
        else:
            return input(f"organise_fun(#): {text}")
        
    def print_help(self):
        print()
        print("HELP".center(50, "-"))
        print()
        print("groups".center(50, "-"))
        print("\\lg - prints groups ")
        print("\\sg - select group")
        print("\\cg - create group")
        print("-"*50)
        print()
        print("lessons".center(50, "-"))
        print("\\ll - prints lessons in current group")
        print("\\cl - creates lesson in current group")
        print("\\dl [lesson_name] - deletes lesson in current group")
        print("\\el [lesson_name] - mark lesson as ended in current group")
        print("\\ovs [lesson_name] - opens lesson directory in Visual Studio Code")
        print("\\of [lesson_name] - opens lesson directory in File Explorer")
        print("-"*50)
        print()
        print("projects".center(50, "-"))
        print("\\lp - prints projects in current group")
        print("\\cp - creates project in current group")
        print("\\opnf [project_name] - opens teacher's project directory in File Explorer")
        print("\\opsf [project_name] [student_name] - opens student's project directory in File Explorer")
        print("-"*50)
        print()
        print("misc".center(50, "-"))
        print("\\q - exits")
        print("\\! [command] - execs sys commands")
        print("-"*50)
        print()

    def print_groups(self, groups): 
        for i in range(len(groups)):
            print(f"({i}) {groups[i].name}")

    def create_group(self):
        group_name = self.input("Enter group name: ")
        result = self.organiser_service.create_group(group_name)
        if result == OrganiserServiceErrors.GROUP_NAME_TOO_SHORT:
            self.print("Group name must be at least 3 characters length")
        if result == True:
            self.print(f"Group {group_name} created successfully")
    
    def select_group(self):
        groups = self.organiser_service.list_groups()

        if len(groups) == 0:
            answer = ""
            while answer.upper() != "N":
                answer = self.input("You don't have any group. Would you like to create one now? (Y/N): ")
                if answer.upper() == "Y": 
                    self.create_group()
                    return;
        
        self.print_groups(groups)
        
        while True:
            answer = self.input(f"Choose group index to select (0 - {len(groups) - 1}): ")
            if not answer.isdigit():
                self.print(f"Index must be a number in range (0 - {len(groups) - 1})")
                continue
            index = int(answer)
            if index < 0 or index >= len(groups):
                self.print(f"Index must be in range from 0 to {len(groups) - 1}")
                continue
            
            selected_group = groups[index]
            self.group_service.set_group(selected_group)
            break

    def create_lesson(self):
        lesson_name = self.input("Enter lesson name: ")
        material_number = self.input("Enter material number (eg. 1.12): ")

        result = self.group_service.create_lesson(lesson_name, material_number)
        
        if result == GroupErrors.LESSON_NAME_TOO_SHORT:
            self.print("Lesson's name must have at least 3 characters length")
        elif result == GroupErrors.MATERIAL_NUMBER_NOT_DECIMAL:
            self.print("Material number must be decimal (eg. 1.12)")
        else:
            self.print(f"Lesson {lesson_name} created successfully!")
    
    def delete_lesson(self, answer):
        splitted_answer = answer.strip().split(" ")

        if len(splitted_answer) < 2:
            self.print("You must provide lesson name")
            return
        
        lesson_name = " ".join(splitted_answer[1:])
        print(lesson_name)

        self.group_service.delete_lesson(lesson_name)

    def end_lesson(self, answer):
        splitted_answer = answer.strip().split(" ")

        if len(splitted_answer) < 2:
            self.print("You must provide lesson name")
            return
        
        lesson_name = " ".join(splitted_answer[1:])
        
        result = self.group_service.end_lesson(lesson_name)

        if result == GroupErrors.INVALID_LESSON_NAME:
            self.print("Invalid lesson name provided")
        else:
            self.print("Lesson deleted successfully")

    def list_lessons(self):
        lessons = self.group_service.list_lessons()

        if lessons == RepositoryErrors.INVALID_FILE_FORMAT:
            self.print("CRITICAL ERROR! LESSON FILE IS CORRUPTED!")
            return
        elif lessons == RepositoryErrors.FILE_NOT_EXIST:
            self.print("Lessons file doesn't exist!")
            return
        if len(lessons) == 0:
            self.print("<No lessons to display>")
            return
        print()
        print("Name".center(40, " "), "Created at", "Ended At", "Material number", sep="\t")
        print()
        for lesson in lessons:
            print(lesson.name.center(40, " "), lesson.created_at,lesson.ended_at,"",lesson.material_number, sep="\t")

    def open_lesson_in_f(self, answer):
        splitted_answer = answer.strip().split(" ")

        if len(splitted_answer) < 2:
            self.print("You must provide lesson name")
            return
        
        lesson_name = " ".join(splitted_answer[1:])

        self.group_service.open_in_file(lesson_name)

    def open_lesson_in_vs(self, answer):
        splitted_answer = answer.strip().split(" ")

        if len(splitted_answer) < 2:
            self.print("You must provide lesson name")
            return
        
        lesson_name = " ".join(splitted_answer[1:])

        self.group_service.open_in_vs(lesson_name)
    
    def exec_system(self, answer):
        splitted_answer = answer.split(" ")
        if len(splitted_answer) < 2:
            self.print("Provide command to execute!")
            return
        os.system(" ".join(splitted_answer[1:]).strip())

    def run(self):
        os.system("clear")
        self.print("Welcome to organise_fun!")

        while True:
            answer = self.input("")
            if answer == "\\h":
                self.print_help()
            elif answer.startswith("\!"):
                self.exec_system(answer)
            elif answer == "\\q":
                exit()
            elif answer == "\\cg":
                self.create_group()
            elif answer == "\\lg":
                groups = self.organiser_service.list_groups()
                self.print_groups(groups)
            elif answer == "\\sg":
                self.select_group()
            elif not self.group_service.group:
                self.print("You have to select group by using \"\\sg\" first!")
                continue
            if answer == "\\cl":
                self.create_lesson()
            elif answer == "\\ll":
                self.list_lessons()
            elif answer.startswith("\\dl"):
                self.delete_lesson(answer)
            elif answer.startswith("\\el"):
                self.end_lesson(answer)
            elif answer.startswith("\\of"):
                self.open_lesson_in_f(answer)
            elif answer.startswith("\\ovs"):
                self.open_lesson_in_vs(answer)