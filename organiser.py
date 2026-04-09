from os import path
from group import Group


class Organiser:
    def __init__(self, dir):
        self.dir = dir or "."
        self.groups = []
        if path.exists("./groups.of"):
            self.load_group_data()
            self.select_group()
        else:
            answer = self.inputOf(f"organise_fun(#): No groups file found! should I create one? (Y/N):")
            if answer == "Y":
                self.create_groups_file()
                self.load_group_data()
                self.select_group()
            else:
                exit()
    def printOf(self, text):
        print(f"organise_fun(#): {text}")
    def inputOf(self, text):
        return input(f"organise_fun(#): {text}")
    def create_groups_file(self):
        with open("./groups.of", "w") as f:
            self.printOf("File created!")
            answer = ""
            while True:
                answer = self.inputOf("Enter new group name or type 'exit' to end: ")
                if answer == "exit": 
                    print("-"*15)
                    break
                f.write(f"{answer};")
                self.printOf(f"{answer} group added successfully!")

    def load_group_data(self):
        with open("./groups.of") as f:
            group_names = f.read().split(";")[:-1]
            for name in group_names:
                self.groups.append(Group(name, self.dir))
    def select_group(self):
        for i in range(len(self.groups)):
            print(f"({i}) {self.groups[i]}")
        selected_group_index = self.inputOf(f" Select group index (0 - {len(self.groups) - 1}): ")
        try:
            if int(selected_group_index) >= 0 and int(selected_group_index) < len(self.groups):
                self.groups[int(selected_group_index)].select_group()
            else:
                self.printOf("Invalid group index!")
        except ValueError:
            print("Invalid index entered")