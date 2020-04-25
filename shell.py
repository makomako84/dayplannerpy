import sys

from API.DayPlanner import DayPlanner

class Shell():
    def shell_main_menu(self):
        if(len(sys.argv) <2): return

        firstarg = sys.argv[1]

        if firstarg == '-calend':
            if(len(sys.argv) < 3) : return
            secondarg = sys.argv[2]
            if secondarg == 'out':
                self.shell_out_tasks()
            elif secondarg == 'add':
                self.shell_add_task()
            elif secondarg == 'find':
                self.shell_find_task()
            elif secondarg == 'del':
                self.shell_del_task()
        # elif firstarg == '-book':
        #     if (len(sys.argv) < 3): return
        #     secondarg = sys.argv[2]
        #     if secondarg == 'out':
        #         self.out_phones()

    def shell_out_tasks(self):
        dayPlanner = DayPlanner()
        for taskstr in dayPlanner.out_tasks():
            print(taskstr)

    def shell_add_task(self):
        ui = {}
        ui["name"] = input("Enter task name: ")
        ui["date"] = input("enter date in form: YYYY-M-D H:M ")
        ui["done"] = True if input("Is task done? y/n ") else False
        dayplanner = DayPlanner()
        dayplanner.add_new_task(ui)

    def shell_find_task(self):
        ui={}
        ui["name"] = input("Enter part of task name: ")
        dayPlanner = DayPlanner()
        res = dayPlanner.find_task_by_name(ui["name"])
        [print(x) for x in res]
        return  res

    def shell_del_task(self):
        dayPlanner = DayPlanner()
        res = dayPlanner.shell_find_task()
        if len(res) > 1:
            print("Create more Accurate request")
        else:
            if(input("Delete? (y)") == "y"):
                self.delete_task(res[0])

# dayPlanner = DayPlanner()
# dayPlanner.shell_del_task()
# print(sys.argv[1])
shell = Shell()
shell.shell_main_menu()
