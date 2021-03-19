# this is not primary file

from tkinter import *
from tkcalendar import  Calendar, DateEntry
from API.DayPlanner import DayPlanner
from datetime import datetime, date, timedelta
from pydispatch import dispatcher

DATE_PICKED = 'date-picked'

class DatePicker(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.button = Button(master, text="Pick date")
        self.button['command'] = self.date_picker_window
        self.picked_date = None

    def date_picker_window(self):
        def apply_selection():
            self.picked_date = cal.selection_get()
            dispatcher.send(signal=DATE_PICKED, sender=self)
            cal.master.destroy()

        top = Toplevel(self.master)
        mindate = date(year=2015, month=1, day=1)
        maxdate = date.today() + timedelta(days=60)
        selecteddate = date.today()
        if self.picked_date != None:
            selecteddate = self.picked_date


        cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                       mindate=mindate, maxdate=maxdate, disabledforeground='red',
                       cursor="hand1", year=selecteddate.year, month=selecteddate.month, day=selecteddate.day)
        cal.pack(fill="both", expand=True)
        b = Button(top, text="ok", command=apply_selection)
        b.pack()
    def pack(self):
        self.button.pack()

class GUI(Frame):

    def __init__(self, master):
        Frame.__init__(self,master)

        # vars
        self.currentDateStr = StringVar()
        self.currentDateStr.set(date.today())

        # Frames
        self.frame_today_list = Frame(master)
        self.frame_buttons_holder = Frame(master)

        self.label_current_date = Label(self.frame_today_list, width=25, textvariable=self.currentDateStr)
        self.label_output = Label(self.frame_today_list,width=100)
        self.listbox_tasks = Listbox(self.frame_today_list,width=100,height=25)
        self.button_output = Button(self.frame_buttons_holder, text="Out")
        self.date_picker = DatePicker(self.frame_buttons_holder)

        # configurate
        self.button_output['command'] = self.update_listbox_tasks

        # pack
        self.frame_today_list.pack()
        self.frame_buttons_holder.pack()

        self.label_current_date.pack(side=TOP)
        self.listbox_tasks.pack(side=TOP)
        self.button_output.pack()
        self.date_picker.pack()

        # events
        dispatcher.connect(self.date_picked_handler, signal=DATE_PICKED, sender=dispatcher.Any)

        self.update_listbox_tasks()

    def update_listbox_tasks(self):
        dp = DayPlanner()
        self.listbox_tasks.delete(0, END)
        currentdate = datetime.strptime(self.currentDateStr.get(), "%Y-%m-%d").date()
        for task in dp.get_tasks_filtered_by_date(currentdate):
            self.listbox_tasks.insert(0, task.__str__())

    def date_picked_handler(self,sender):
        self.currentDateStr.set(sender.picked_date)
        self.update_listbox_tasks()



root = Tk()
gui = GUI(root)
root.mainloop()