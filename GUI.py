from tkinter import *
from tkcalendar import  Calendar, DateEntry
from API.DayPlanner import DayPlanner
import  datetime

class DatePicker(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.button = Button(master, text="Pick date")
        self.button['command'] = self.date_picker

    def date_picker(self):
        def print_sel():
            print(cal.selection_get())
            cal.master.destroy()

        top = Toplevel(self.master)
        mindate = datetime.date(year=2015, month=1, day=1)
        maxdate = datetime.date.today() + datetime.timedelta(days=60)
        today = datetime.date.today()
        cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                       mindate=mindate, maxdate=maxdate, disabledforeground='red',
                       cursor="hand1", year=today.year, month=today.month, day=today.day)
        cal.pack(fill="both", expand=True)
        b = Button(top, text="ok", command=print_sel)
        b.pack()
    def pack(self):
        self.button.pack()
    def apply_selected(self):
        pass

class GUI():

    def __init__(self, master):
        self.__master = master
        self.label_output = Label(master,width=100)
        self.button_output = Button(master, text="Out")
        self.date_picker = DatePicker(master)

        self.button_output['command'] = self.out_calend

        self.label_output.pack()
        self.button_output.pack()
        self.date_picker.pack()

    def out_calend(self):
        dp = DayPlanner()
        self.label_output['text'] = dp.out_tasks()



root = Tk()
gui = GUI(root)
root.mainloop()