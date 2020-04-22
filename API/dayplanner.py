import  sys
from lxml import etree
from datetime import  datetime

class Task:
    name = None
    date = None
    description = None
    done = False

    def __init__(self, name):
        self.name = name

    def parseXML(self):
        pass
    def getXML(self):
        root = etree.Element('Task')

        name = etree.SubElement(root,'Name')
        name.text = self.name

        date = etree.SubElement(root,'Date')
        date.text = str(self.date)

        description = etree.SubElement(root,'Description')
        description.text = self.description

        if self.done:
            etree.SubElement(root,'Done')

        print(etree.tostring(root))
        return root

    def __str__(self):
        return self.name

class Phone:
    name = None
    num = None
    description = None

    def __init__(self,name):
        self.name = name

    def parseXML(self):
        pass

    def __str__(self):
        return  self.name

class DayPlanner:
    tasks = []
    phones =[]

    def __init__(self):
        self.tasks.append(Task(name='newTask'))
        self.tasks.append(Task(name='LearnPy'))
        self.phones.append(Phone(name='Boris'))
        self.phones.append(Phone(name='Life'))

        self.shell_main_menu()
    def shell_main_menu(self):
        if(len(sys.argv) <2): return

        firstarg = sys.argv[1]

        if firstarg == '-calend':
            if(len(sys.argv) < 3) : return
            secondarg = sys.argv[2]
            if secondarg == 'out':
                self.out_tasks()
        elif firstarg == '-book':
            if (len(sys.argv) < 3): return
            secondarg = sys.argv[2]
            if secondarg == 'out':
                self.out_phones()

    def out_tasks(self):
        print(*self.tasks, sep='\n')
    def out_phones(self):
        print(*self.phones, sep='\n')

    def create_new_task(self):
        tree = etree.parse('data.xml')
        root = tree.getroot()
        # tasks = ET.SubElement(root,'tasks')
        tasks = root.find('tasks')
        newTask = Task('do job')
        newTask.date = datetime.now()
        tasks.append(newTask.getXML())
        print(etree.tostring(root, pretty_print=True))

        tree.write('data.xml', pretty_print=True)

    def craete_new_phone(self):
        pass
    def read_from_XML(self):
        pass
    def save_to_XML(self):
        pass

dayPlanner = DayPlanner()

# print(sys.argv[1])
dayPlanner.create_new_task()