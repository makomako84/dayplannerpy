from tkinter import *
from tkcalendar import  Calendar, DateEntry
from API.DayPlanner import DayPlanner
import  datetime
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
        mindate = datetime.date(year=2015, month=1, day=1)
        maxdate = datetime.date.today() + datetime.timedelta(days=60)
        today = datetime.date.today()
        cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                       mindate=mindate, maxdate=maxdate, disabledforeground='red',
                       cursor="hand1", year=today.year, month=today.month, day=today.day)
        cal.pack(fill="both", expand=True)
        b = Button(top, text="ok", command=apply_selection)
        b.pack()
    def pack(self):
        self.button.pack()

class GUI(Frame):

    def date_picked_handler(self,sender):
        self.currentDate.set(sender.picked_date)

    def __init__(self, master):
        Frame.__init__(self,master)

        # vars
        self.currentDate = StringVar()
        self.currentDate.set(datetime.date.today())

        # Frames
        self.frame_today_list = Frame(master)
        self.frame_buttons_holder = Frame(master)

        self.label_current_date = Label(self.frame_today_list, width=25, textvariable=self.currentDate)
        self.label_output = Label(self.frame_today_list,width=100)
        self.listbox_tasks = Listbox(self.frame_today_list,width=100,height=25)
        self.button_output = Button(self.frame_buttons_holder, text="Out")
        self.date_picker = DatePicker(self.frame_buttons_holder)


        self.button_output['command'] = self.out_calend


        self.frame_today_list.pack()
        self.frame_buttons_holder.pack()

        self.label_current_date.pack(side=TOP)
        self.listbox_tasks.pack(side=TOP)
        self.button_output.pack()
        self.date_picker.pack()

        dispatcher.connect(self.date_picked_handler, signal=DATE_PICKED, sender=dispatcher.Any)

    def update_listbox(self):
        pass

    def out_calend(self):
        dp = DayPlanner()
        self.listbox_tasks.delete(0, END)
        for task in dp.out_tasks():
            self.listbox_tasks.insert(0, task.__str__())



root = Tk()
gui = GUI(root)
root.mainloop()