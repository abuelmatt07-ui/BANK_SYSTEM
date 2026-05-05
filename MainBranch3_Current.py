

import importlib

from tkinter import *
win = Tk()
win.title("Bank")
win.geometry("434x250")
win.attributes("-topmost", True)

win.config(bg="#1e1e1e")

#WINDOW FUNCTIONS --------------------------------------------------------
def Exit(event):
    win.destroy()
win.bind("<Escape>", Exit)

def ClearMain():
   for widget in win.winfo_children():
    widget.destroy()



#FRONT-END FUNCTIONS ------------------------------------------


def UpdateCurDisplay(newDisplay):
    global currentDisplay

    Current.config(text=f"Current: {newDisplay}$")

def ErrorStable(error, position = 6):
    global Err
    global Container

    Err = Label(Container, text=f"Invalid: {error}", fg="Red", bg="#1e1e1e")
    Err.grid(row=position, column=0, columnspan=10, sticky="ew")



#BACK-END FUNCTIONS --------------------------------------------

def GetIn():
    global Amount
    return Amount.get()

def Cret():
    global Name
    global Amount

    name = Name.get()
    amount = int(Amount.get())


    with open(f"USERS/{name}.py", "w") as cret:
        cret.write(f"amount = {amount}")


def Depo():
    global Err
    amount = GetIn()
    

    loc = f"USERS.{Name}"
    userAcc = importlib.import_module(loc)
    importlib.reload(userAcc)
    curAmount = getattr(userAcc, "amount")
    userPass = getattr(userAcc, "password")



    try:
        Err.destroy()

        if int(amount) < 0:
            ErrorStable("Positive numbers only.")
            return

        curAmount += int(amount)
        
        with open(f"USERS/{Name}.py", "w") as f:
            f.write(f"amount = {curAmount}\npassword = \"{userPass}\"")

        UpdateCurDisplay(curAmount)

    except ValueError:
        ErrorStable("Needs to be valid number/amount.")


def Withdraw():
    global Err
    global Name
    amount = GetIn()

    


    loc = f"USERS.{Name}"
    userAcc = importlib.import_module(loc)
    importlib.reload(userAcc)
    curAmount = getattr(userAcc, "amount")
    userPass = getattr(userAcc, "password")

    try:
        Err.destroy()

        if int(amount) < 0:
            ErrorStable("Positive numbers only.")
            return

        if (curAmount - int(amount)) >= 0:
            curAmount -= int(amount)
        else:
            ErrorStable("Insufficient Funds.")
        
        with open(f"USERS/{Name}.py", "w") as f:
            f.write(f"amount = {curAmount}\npassword = \"{userPass}\"")

        UpdateCurDisplay(curAmount)

    except ValueError:
        ErrorStable("Needs to be valid number/amount.")


def LogCheck():
    global UserPassIn
    global UserNameIn
    global Err

    Err = Label(win)

    name = UserNameIn.get()
    CheckName = f"USERS.{UserNameIn.get()}"
    PassInCompare = UserPassIn.get()

    try:
        userAccount = importlib.import_module(CheckName)
        getPass = getattr(userAccount, "password")
        Err.destroy()

        if PassInCompare == getPass:
            AccountCurrentAmmount = getattr(userAccount, "amount")
            ClearMain()
            Main(name, AccountCurrentAmmount)
        else:
            ErrorStable("Please Check Password.", 5)
    except ModuleNotFoundError:
        ErrorStable("Please Check Username.", 5)


def BackToLog():
    ClearMain()
    Log()










#PAGES ------------------------------------------------------------------------------------------------------

def Log():

    win.columnconfigure(1, weight=1)
    win.rowconfigure(1, weight=1)

    global UserNameIn
    global UserPassIn


    global Container
    Container = Frame(bg="#1e1e1e", pady=20, padx=30)
    Container.grid(row=1, column=1, sticky="ns")
    Container.columnconfigure(1, weight=1)


    Err = Label(Container)

    LogHead = Label(win, text="FranzExpress", padx=193, bg="#0D1A63", fg="white", font=("Times", 20, "italic"), pady=10)
    LogHead.grid(row=0, column=0, columnspan=2, sticky="ew", )

    NameLabel = Label(Container, text="Username:", bg="#1e1e1e", fg="white")
    NameLabel.grid(row=2, column=0,sticky="ew")
    UserNameIn = Entry(Container, highlightthickness=2, highlightbackground="grey", bg="#1e1e1e", fg="white")
    UserNameIn.grid(row=2, column=1, sticky="ew")

    PassLabel = Label(Container, text="Password:", bg="#1e1e1e", fg="white")
    PassLabel.grid(row=3, column=0,sticky="ew")
    UserPassIn = Entry(Container, highlightthickness=2, highlightbackground="grey", bg="#1e1e1e", fg="white")
    UserPassIn.grid(row=3, column=1, sticky="ew")

    EnterBut = Button(Container, text="Enter", command=LogCheck)   
    EnterBut.grid(row=4, column=0, columnspan=2, sticky="ew")

    UserNameIn.focus_set()





def Main(user, amount):

    win.columnconfigure(1, weight=1)

    global Container
    Container = Frame(bg="#1e1e1e", pady=20, padx=30)
    Container.grid(row=1, column=1, sticky="ns")
    Container.columnconfigure(1, weight=1)


    global currentDisplay
    global head
    global tex1
    global tex2
    global Amount
    global Dep
    global Wit
    global Current
    global Err
    global Name
 

    Name = user
    currentDisplay = amount


    Back = Button(Container, text="Logout", command=BackToLog)
    Back.grid(row=5)


    head = Label(win, text=f"Welcome, {Name}!", padx=193, bg="#0D1A63", fg="white", font=("Times", 20, "italic"), pady=10)
    head.grid(row=0, column=0, columnspan=2, sticky="ew")

    tex2 = Label(Container, text="Amount:", bg="#1e1e1e", fg="white")
    tex2.grid(row=1, column=0, sticky="ew")

    Amount = Entry(Container, highlightthickness=2, highlightbackground="grey", bg="#1e1e1e")
    Amount.grid(row=1, column=1, sticky="ew")

    Dep = Button(Container, text="Deposit", command=Depo)
    Dep.grid(row=2, column=0, sticky="ew", columnspan=2)

    Wit = Button(Container, text="Withdraw", command=Withdraw)
    Wit.grid(row=3, column=0, sticky="ew", columnspan=2)

    Current = Label(Container, text=f"Current: {currentDisplay}$", fg="#72BAA9", bg="#1e1e1e")
    Current.grid(row=4, column=0, columnspan=2, sticky="ew")

    Err = Label(Container)

    Amount.focus_set()






#SYSTEM STARTS ----------------------------------------------------------------------***********



Log()










            



win.mainloop()





