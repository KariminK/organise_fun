import os, datetime

class Group:
    def __init__(self, name, dir):
        self.name = name
        self.dir = dir or "."
        self.group_dir = f"{self.dir}/grupa_{self.name.replace(" ", "_")}"
        if not os.path.exists(self.group_dir):
            self.create_group_dir()
    
    def select_group(self):
        if not os.path.exists(f"{self.group_dir}/lessons.of"): 
            self.create_lessons_file()
        self.display_actions()

    def print_gr(self, text):
        print(f"organise_fun({self.name}): {text}")

    def input_gr(self, text):
        return input(f"organise_fun({self.name}): {text}")

    def create_lessons_file(self):
        with open(f"{self.group_dir}/lessons.of", "w") as f:
            while True:
                answer = self.input_gr("Do you want to add first lesson? (Y/N): ").upper()
                if answer == "Y":
                    self.create_lesson(f)
                    break
                elif answer == "N":
                    break

    def create_group_dir(self):
        os.mkdir(self.group_dir)
        os.mkdir(f"{self.group_dir}/lekcje")
        os.mkdir(f"{self.group_dir}/materialy")
        os.mkdir(f"{self.group_dir}/projekty")
    
    def print_help(self):
        print()
        print("HELP".center(50, "-"))
        print("\l - prints lessons and projects in current group")
        print("\ll - prints lessons in current group")
        print("\lp - prints projects in current group")
        print("\cl - creates lesson in current group")
        print("\cp - creates project in current group")
        print("\ovs [lesson_name] - opens lesson directory in Visual Studio Code")
        print("\of [lesson_name] - opens lesson directory in File Explorer")
        print("\opnf [project_name] - opens teacher's project directory in File Explorer")
        print("\opsf [project_name] [student_name] - opens student's project directory in File Explorer")
        print("\q - exits")
        print("\! [command] - execs sys commands")
        print("-"*50)
        print()

    def display_actions(self):
        while True:
            answer = self.input_gr("")
            if answer == "\h":
                self.print_help()
            elif answer == "\q":
                exit()
            elif answer == "\ll":
                with open(f"{self.group_dir}/lessons.of") as f:
                    self.list_lessons(f)
            elif answer == "\cl":
                with open(f"{self.group_dir}/lessons.of", "a") as f:
                    self.create_lesson(f)
            elif answer == "\cp":
                with open(f"{self.group_dir}/projekty/projects.of", "a") as f: 
                    self.create_project(f)
            elif answer.startswith("\ovs"):
                lesson_path = self.extract_path(answer, "lesson", "")
                if lesson_path == -1: continue
                if os.path.exists(lesson_path):
                    self.open_in_vs(lesson_path)
                else:
                    self.print_gr("Lesson directory doesn't exist")
            elif answer.startswith("\of"):
                lesson_path = self.extract_path(answer, "lesson", "")
                if lesson_path == -1: continue
                if os.path.exists(lesson_path):
                    self.open_in_file_explorer(lesson_path)
                else:
                    self.print_gr("Lesson directory doesn't exist")
            elif answer.startswith("\opnf"):
                project_path = self.extract_path(answer, "project", "projekt_nauczyciel")
                if project_path == -1: continue
                if os.path.exists(project_path):
                    self.open_in_file_explorer(project_path)
                else:
                    self.print_gr("Project directory doesn't exist")
            elif answer.startswith("\opsf"):
                splitted_answer = answer.split(" ")
                if len(splitted_answer) < 3:
                    self.print_gr("Provide both project name and student name")
                    continue
                project_path = self.extract_path(answer, "project", f"projekty_uczniow/projekt_{splitted_answer[2]}")
                if project_path == -1: continue
                if os.path.exists(project_path):
                    self.open_in_file_explorer(project_path)
                else:
                    self.print_gr("Project directory doesn't exist")
            elif answer.startswith("\!"):
                command = answer.split(" ")[1]
                os.system(command)
    def list_lessons(self, file):
        print()
        print("Name".center(40, " "), "Created at", "Ended At", "Materials number", sep="\t")
        print()
        for lessonLine in file:
            lesson = lessonLine.split(";")
            print(lesson[0].center(40, " "), lesson[1], lesson[2], "", lesson[3], sep="\t")
        print()

    def open_in_vs(self, dir):
        os.system(f"code {dir}")
    def open_in_file_explorer(self, dir):
        os.system(f"xdg-open {dir}")

    def create_lesson(self, file):
        lesson_name = self.input_gr("Enter lesson's name: ")
        material_number = self.input_gr("Enter materials number (eg. 1.12): ")
        file.write(f"{lesson_name};{datetime.date.today()};ONGOING;{material_number}")
        os.mkdir(f"{self.group_dir}/lekcje/{lesson_name.replace(" ", "_")}")
        print(f"Successfully added lesson {lesson_name}")
    
    def assign_student_to_project(self, project_name, file):
        while True:
            answer = self.input_gr("Enter student's name (or type \"exit\" to exit): ")
            
            if answer.lower() == "exit": return

            student_name = answer.replace(" ", "_")
            student_project_dir = f"{self.group_dir}/projekty/{project_name.replace(" ", "_")}/projekty_uczniow/projekt_{student_name}";
            os.mkdir(student_project_dir)
            file.write(f"{student_name};{student_project_dir}\n")
            self.print_gr(f"Student {student_name} assigned successfully")

    def create_project(self, file):
        project_name = self.input_gr("Enter project's name: ")
        project_dir = f"{self.group_dir}/projekty/{project_name.replace(" ", "_")}";
        os.mkdir(f"{project_dir}")
        os.mkdir(f"{project_dir}/projekt_nauczyciel")
        os.mkdir(f"{project_dir}/projekty_uczniow")
        file.write(f"{project_name};{datetime.date.today()};ONGOING\n")
        self.print_gr("Project directory created successfully")
        while True:
                answer = self.input_gr("Do you want to assign students now? (Y/N): ").upper()
                if answer == "Y":
                    with open(f"{project_dir}/project.of", "a") as f:
                        self.assign_student_to_project(project_name, f)
                    break
                elif answer == "N":
                    break

    def extract_path(self, answer, type, path_end):
        splitted_answer = answer.split(" ")
        if len(splitted_answer) < 2: 
            self.print_gr(f"No {type} name provided")
            return -1
        lesson_name = splitted_answer[1]
        return f"{self.group_dir}/{'lekcje' if type == 'lesson' else "projekty"}/{lesson_name.replace(" ", "_")}/{path_end}"

    def __str__(self):
        return self.name