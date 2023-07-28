from Detector import main_app
from create_classifier import train_classifer
from create_dataset import start_capture
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox,PhotoImage
from datetime import timedelta
from datetime import datetime
import tkcalendar

from database import getAttendance, initDatabase, insertOrUpdate
from export import export_csv
#from PIL import ImageTk, Image
#from gender_prediction import emotion,ageAndgender
names = set()

class MainUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        initDatabase()
        self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.title("Face Attendance System")
        self.resizable(False, False)
        self.geometry("500x250")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        self.active_id = None
        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageExport, PageThree, PageFour):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
            frame = self.frames[page_name]
            frame.tkraise()

    def on_closing(self):

        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            f =  open("nameslist.txt", "a+")
            for i in names:
                    f.write(i+" ")
            self.destroy()


class StartPage(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            #load = Image.open("homepagepic.png")
            #load = load.resize((250, 250), Image.ANTIALIAS)
            render = PhotoImage(file='homepagepic.png')
            img = tk.Label(self, image=render)
            img.image = render
            img.grid(row=0, column=1, rowspan=4, sticky="nsew")
            label = tk.Label(self, text="        Home Page        ", font=self.controller.title_font)
            label.grid(row=0, sticky="ew")
            button1 = tk.Button(self, text="   Add a User  ", fg="#263942", bg="#ffffff",command=lambda: self.controller.show_frame("PageOne"))
            button2 = tk.Button(self, text="   Attendance  ",command=lambda: self.controller.show_frame("PageFour"))
            button3 = tk.Button(self, text="Quit", command=self.on_closing)
            button4 = tk.Button(self, text=" Export Report ", command=lambda: self.controller.show_frame("PageExport"))
            
            button1.grid(row=1, column=0, ipady=3, ipadx=7)
            button2.grid(row=2, column=0, ipady=3, ipadx=2)
            button4.grid(row=3, column=0, ipady=3, ipadx=32)
            button3.grid(row=3, column=1, ipady=3, ipadx=32)


        def on_closing(self):
            if messagebox.askokcancel("Quit", "Are you sure?"):
                global names
                with open("nameslist.txt", "w") as f:
                    for i in names:
                        f.write(i + " ")
                self.controller.destroy()
        

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #ID
        tk.Label(self, text="Enter the ID", font='Helvetica 12 bold').grid(row=0, column=0, pady=10, padx=5)
        self.id = tk.Entry(self, borderwidth=1, font='Helvetica 11')
        self.id.grid(row=0, column=1, pady=10, padx=10)
        #Name
        tk.Label(self, text="Enter the name", font='Helvetica 12 bold').grid(row=1, column=0, pady=10, padx=5)
        self.user_name = tk.Entry(self, borderwidth=1, font='Helvetica 11')
        self.user_name.grid(row=1, column=1, pady=10, padx=10)

        self.buttoncanc = tk.Button(self, text="Cancel", bg="#ffffff", fg="#263942", command=lambda: controller.show_frame("StartPage"))
        self.buttonext = tk.Button(self, text="Next", fg="#ffffff", bg="#263942", command=self.start_training)
        self.buttoncanc.grid(row=2, column=0, pady=10, ipadx=5, ipady=4)
        self.buttonext.grid(row=2, column=1, pady=10, ipadx=5, ipady=4)
    def start_training(self):
        global names
        if self.user_name.get() == "None" or self.id.get() == "None":
            messagebox.showerror("Error", "ID cannot be 'None'")
            return
        elif len(self.user_name.get()) == 0:
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        
        name = self.user_name.get()
        id = self.id.get()
        names.add(name)

        insertOrUpdate(id,name)
        self.controller.active_name = name
        self.controller.active_id = id
        self.controller.show_frame("PageThree")


class PageExport(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        tk.Label(self, text="Enter time start(dd/mm/yy)", font='Helvetica 12 bold').grid(row=0, column=0, pady=10, padx=5)
        self.date1 = tkcalendar.DateEntry(self)
        self.date1.set_date(datetime.today().replace(day=1))
        self.date1.grid(row=1, column=0, padx=10,pady=10)

        tk.Label(self, text="Enter time end(dd/mm/yy)", font='Helvetica 12 bold').grid(row=0, column=1, pady=10, padx=5)
        self.date2 = tkcalendar.DateEntry(self)
        self.date2.grid(row=1, column=1, padx=10,pady=10)

        self.buttoncanc = tk.Button(self, text="Cancel", bg="#ffffff", fg="#263942", command=lambda: controller.show_frame("StartPage"))
        self.buttonext = tk.Button(self, text="Next", bg="#ffffff", fg="#263942", command=self.start_export)
        self.buttoncanc.grid(row=2, column=0, pady=10, ipadx=5, ipady=4)
        self.buttonext.grid(row=2, column=1, pady=10, ipadx=5, ipady=4)
        
    
    def start_export(self):
       
        start = self.date1.get_date().strftime("%Y-%m-%d %H:%M:%S")
        end = self.date2.get_date().strftime("%Y-%m-%d %H:%M:%S")
        result = getAttendance(start, end)
        
        try:
            export_csv(result)
            messagebox.showinfo("SUCCESS", "Export success!")

        except:
            messagebox.showerror("ERROR", "Please try again")





class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.numimglabel = tk.Label(self, text="Number of images captured = 0", font='Helvetica 12 bold', fg="#263942")
        self.numimglabel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        self.capturebutton = tk.Button(self, text="Capture Data Set", fg="#ffffff", bg="#263942", command=self.capimg)
        self.trainbutton = tk.Button(self, text="Train The Model", fg="#ffffff", bg="#263942",command=self.trainmodel)
        self.capturebutton.grid(row=1, column=0, ipadx=5, ipady=4, padx=10, pady=20)
        self.trainbutton.grid(row=1, column=1, ipadx=5, ipady=4, padx=10, pady=20)

    def capimg(self):
        self.numimglabel.config(text=str("Captured Images = 0 "))
        messagebox.showinfo("INSTRUCTIONS", "We will Capture 100 pic of your Face.")
        x = start_capture(self.controller.active_id)
        self.controller.num_of_images = x
        self.numimglabel.config(text=str("Number of images captured = "+str(x)))

    def trainmodel(self):
        if self.controller.num_of_images < 100:
            messagebox.showerror("ERROR", "No enough Data, Capture at least 100 images!")
            return
        train_classifer()
        messagebox.showinfo("SUCCESS", "The modele has been successfully trained!")
        self.controller.show_frame("PageFour")


class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Face Recognition", font='Helvetica 16 bold')
        label.grid(row=0,column=0, sticky="ew")
        button1 = tk.Button(self, text="Start Attendance", command=self.openwebcam, bg="#ffffff", fg="#263942")
        #button2 = tk.Button(self, text="Emotion Detection", command=self.emot, fg="#ffffff", bg="#263942")
        #button3 = tk.Button(self, text="Gender and Age Prediction", command=self.gender_age_pred, fg="#ffffff", bg="#263942")
        button4 = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        button1.grid(row=1,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        #button2.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        #button3.grid(row=2,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button4.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)

    def openwebcam(self):
        main_app()
    #def gender_age_pred(self):
     #  ageAndgender()
    #def emot(self):
     #   emotion()



app = MainUI()
app.iconphoto(False, tk.PhotoImage(file='icon.ico'))
app.mainloop()

