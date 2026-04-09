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
        print("\c - creates lesson in current group")
        print("\s [lesson_name] - selects lesson in current group")
        print("\ovs [lesson_name] - opens lesson directory in Visual Studio Code")
        print("\of [lesson_name] - opens lesson directory in File Explorer")
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
            elif answer == "\c":
                with open(f"{self.group_dir}/lessons.of", "a") as f:
                    self.create_lesson(f)
            elif answer.startswith("\ovs"):
                lesson_path = self.extract_lesson_path(answer)
                if lesson_path == -1: continue
                if os.path.exists(lesson_path):
                    self.open_in_vs(lesson_path)
                else:
                    self.print_gr("Lesson directory doesn't exist")
            elif answer.startswith("\of"):
                lesson_path = self.extract_lesson_path(answer)
                if lesson_path == -1: continue
                if os.path.exists(lesson_path):
                    self.open_in_file_explorer(lesson_path)
                else:
                    self.print_gr("Lesson directory doesn't exist")
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
        lesson_name = self.input_gr("Enter lessons_name: ")
        material_number = self.input_gr("Enter materials number (eg. 1.12): ")
        file.write(f"{lesson_name};{datetime.date.today()};ONGOING;{material_number}")
        os.mkdir(f"{self.group_dir}/lekcje/{lesson_name.replace(" ", "_")}")
        print(f"Successfully added lesson {lesson_name}")
    
    def extract_lesson_path(self, answer):
        splitted_answer = answer.split(" ")
        if len(splitted_answer) < 2: 
            self.print_gr("No lesson name provided")
            return -1
        lesson_name = splitted_answer[1]
        return f"{self.group_dir}/lekcje/{lesson_name.replace(" ", "_")}"

    def __str__(self):
        return self.name