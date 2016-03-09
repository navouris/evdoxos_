__author__ = 'nma'
''' this is a version of the gui_evdoxos program to use a local db instead of the website'''

from tkinter import *
from tkinter.scrolledtext import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.ttk import *
from tkinter.font import Font
#from evdoxos_extract import search_for_unis, search_for_departments, find_courses
import evdoxos_search

# I installed all the above with sudo apt-get python3-tk

url1 = 'https://service.eudoxus.gr/public/departments'

class UniViewer(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
        parent.option_add("*TCombobox*Listbox*Font", self.myfont)

    def initUI(self):
        self.evdoxos = 'https://service.eudoxus.gr/public/departments'
        self.university =''
        self.department = ''
        self.depts = ""
        self.parent.title("Greek Univesity Search Tool")
        self.style = Style()
        self.style.theme_use("default")
        self.style.configure('.', font=('Arial', 10), background ="#5f0808", foreground="#ffffff")
        self.pack(fill=BOTH, expand=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)
        self.myfont = Font(family="Arial",size=10)
        # the University Selector
        l1 = Label(text='Επιλογή Πανεπιστημίου') #.grid(row=0, column=0)
        l1.pack(fill=BOTH, expand=1)
        self.UniList = Combobox(width = 40, textvariable=self.university)
        self.UniList.configure(font=('Arial', 12), background ="#ffffff", foreground="#000000")
        #UniList.grid(row=0, column=1, columnspan=4, sticky=N+S+E+W, padx=10)
        self.UniList.pack(fill=BOTH, expand=1)
        self.UniList.bind('<<ComboboxSelected>>', self.on_value_change)
        unis = evdoxos_search.get_uni_list()
        out = ""
        for u in unis:
            out += u[1]+"; "
        self.UniList['values'] =  unis
        self.UniList.current(0)
        l2 = Label(text='Επιλογή Τμήματος') #.grid(row=0, column=7)
        l2.pack(fill=BOTH, expand=1)
        self.DeptList = Combobox(textvariable=self.department, width = 40, postcommand = self.on_value_change)
        self.DeptList.configure(font=('Arial', 12), background ="#ffffff", foreground="#000000")
        self.DeptList.pack(fill=BOTH, expand=1)
        #DeptList.grid(row=0, column=8, columnspan=4, sticky=N+S+E+W, padx=10)
        self.DeptList.bind('<<ComboboxSelected>>', self.change_selected_dept)
        # self.DeptList['values'] =  self.depts
        # print("self.depts = ", self.depts)
        #self.DeptList.current(0)

        # lbl = Label(self, text="Grades:")
        # lbl.grid(sticky=W, pady=4, padx=5)

        # lbl = Label(self, text="Average\n Grade:")
        # lbl.grid(row=3, column=3, pady=5)

        self.textPad = ScrolledText(self)
        self.textPad.configure(font=('Arial', 12))
        self.textPad.configure(background = 'light yellow')
        self.textPad.grid(row=2, column=0, columnspan=12, rowspan=10, padx=5, pady=5, sticky=E+W+S+N)

        wbtn = Button(self, text="Word\n Image...", command=self.word_cloud)
        wbtn.grid(row=1, column=2, padx=4, pady=4, sticky=N)

        obtn = Button(self, text="Προγραμμα\n Σπουδών...", command=self.find_courses)
        obtn.grid(row=1, column=3, padx=4, pady=4, sticky=N)

        abtn = Button(self, text="Save...",command=self.save_command)
        abtn.grid(row=2, column=3, padx=4, pady=4, sticky=N)

        # cbtn = Button(self, text="APA refs", command=self.apa_refs)
        # cbtn.grid(row=3, column=3, padx=4, pady=4, sticky=N)

        hbtn = Button(self, text="Help", command=self.about_command)
        hbtn.grid(row=4, column=3, padx=4, pady=4, sticky=S)

        # obtn = Button(self, text="OK")
        # obtn.grid(row=5, column=3)

        # menubar = Menu(self.parent)
        # self.parent.config(menu=menubar)
        #
        # fileMenu = Menu(menubar)
        #
        # submenu = Menu(fileMenu)
        # submenu.add_command(label="Student")
        # submenu.add_command(label="New Student")
        #
        # fileMenu.add_cascade(label='Import', menu=submenu, underline=0)
        # fileMenu.add_command(label="Open...", command=self.open_command)
        # fileMenu.add_separator()
        # fileMenu.add_command(label="Exit", underline=0, command=self.onExit)
        #
        # menubar.add_cascade(label="File", underline=0, menu=fileMenu)

    def on_value_change(self, event=None):
        u = self.UniList.get()
        print (u)
        try:
            d = evdoxos_search.get_dept_list(u)
            print (d)
            self.depts = d
            # for depart in d:
            #     f.write(depart+";"+d[depart]+"\n")
            self.DeptList['values'] =  [x[1] for x in d]
            self.DeptList.current(0)
            print("from db, found", d)
        except IOError:
            print ("error in getting departments")

    def change_selected_dept(self, event=None):
        self.department = self.DeptList.get()

    def find_courses(self):
        u = self.UniList.get()
        d = self.DeptList.get()
        if len(u)<5 or len(d)<5:
            showinfo("Προσοχή!", "Πρέπει πρώτα να ορίσετε Πανεπιστήμιο \n και Τμήμα ")
            return
       # elif askyesno("Πρόγραμμα", "Να προχωρήσει η αναζήτηση των μαθημάτων του Τμήματος {}\n"  \
       #                            "του Πανεπιστημίου {}".format(d,u)):
        else:
            u_id = evdoxos_search.get_uni_id(u)
            for x in self.depts:
                print (d, x)
                if x[1] == d:
                    d_id = x[0]
                    break
            data_to_display = self.pretty_print(evdoxos_search.dept_program(u_id,d_id))
            self.textPad.delete('1.0', END)
            self.textPad.insert('1.0', data_to_display)
        # else:
        #     return

    def pretty_print(self, text_to_print):
        out = ""
        for line in text_to_print.split("\n"):
            print(line)
            if "Eξάμηνο " in line:
                if ":0" in line:
                    out += "Μαθήματα που διδάσκονται εκτός εξαμήνων" + '\n'
                else :
                    out += line + "\n"
                out += 15*"_" + '\n'
            elif ";" in line:
                out += '\t'+line.split(';')[2]+'\n'
            else:
                out += line + '\n'
        return out

    def word_cloud(self):
        u = self.UniList.get()
        d = self.DeptList.get()
        if len(u)<5 or len(d)<5:
            showinfo("Προσοχή!", "Πρέπει πρώτα να ορίσετε Πανεπιστήμιο \n και Τμήμα ")
            return
        elif askyesno("Πρόγραμμα", "Να προχωρήσει η εικονική αναπαράσταση του Προγράμματος Σπουδών του Τμήματος {}\n"  \
                                   "του Πανεπιστημίου {}".format(d,u)):
            u_id = evdoxos_search.get_uni_id(u)
            for x in self.depts:
                print (d, x)
                if x[1] == d:
                    d_id = x[0]
                    break
            evdoxos_search.dept_word_cloud(d_id)
        # report.print()
        # if len(url) < 5:
        #     showinfo("Δεν έχει βρεθεί ιστοσελίδα του Τμήματος ")
        #     return
        # data = self.textPad.get('1.0', 'end-1c')
        # if len(data)> 5:
        #     showinfo("Μηπως επιθυμειτε να σωσετε πρωτα τη σελιδα; ")
        # else:
        #     apa =


    def onExit(self):
        self.parent.destroy()

    def about_command(self):
        label = showinfo("About", """Evdoxos Search is an application to extract information from\
         the eudoxus.gr web site \n by N Avouris""")

    def save_command(self):
        data = self.textPad.get('1.0', 'end-1c')
        if len(data)<5:
            label = showinfo("Warning", "There is no file to be saved")
        else:
            file = asksaveasfile(mode='w')
            if file != None:
        # slice off the last character from get, as an extra return is added
            #data = self.textPad.get('1.0', 'end-1c')
                file.write(data)
                file.close()

def main():
    root = Tk()
    root.geometry("800x700+100+50")
    app = UniViewer(root)
    root.mainloop()

if __name__ == '__main__':
    main()