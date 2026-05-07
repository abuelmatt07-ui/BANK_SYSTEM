

import importlib
import os

from tkinter import *
win = Tk()
win.title("Bank")
win.geometry("434x250")
win.attributes("-topmost", True)

win.config(bg="#44444E")
headerColor = "#37353E"

#WINDOW FUNCTIONS --------------------------------------------------------
def Exit(event):
    win.destroy()
win.bind("<Escape>", Exit)

def ClearWin():
   for widget in win.winfo_children():
    widget.destroy()



#FRONT-END FUNCTIONS ------------------------------------------


def UpdateCurDisplay(newDisplay):
    global currentDisplay

    Current.config(text=f"Current: {newDisplay}$")

def ErrorStable(error, position = 6):
    global Err
    global Container

    Err.destroy()
    Err = Label(Container, text=f"Invalid: {error}", fg="Red", bg="#1e1e1e")
    Err.grid(row=position, column=0, columnspan=10, sticky="ew")

def Notif(text, position = 6):
    global Err
    global Container

    Err = Label(Container, text=f"{text}", fg="#72BAA9", bg="#1e1e1e")
    Err.grid(row=position, column=0, columnspan=10, sticky="ew")



#BACK-END FUNCTIONS --------------------------------------------

def GetIn():
    global Amount
    return Amount.get()

def Cret():

    global Err

    Err = Label(Container)


    invalidChars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', 
                    '-', '+', '=', '{', '}', '[', ']', '|', '\\', ':', 
                    ';', '"', "'", '<', '>', ',', '.', '?', '/', '`', '~', '_']

    name = UserNameIn.get().strip()
    password = UserPassIn.get()
    global Amount 
    amount = Amount.get().strip()

    if not name or not password or not amount:
        ErrorStable("Fill all fields.", 6)
        return
    
    for char in invalidChars:
        if char in name:
            ErrorStable("Numbers & Letters\nfor Username Only.", 6)
            return
        
    if " " in name:
        ErrorStable("No Space on Username Allowed.", 6)
        return

    try:
        amount = int(amount)
    except ValueError:
        ErrorStable("Amount must be number.", 6)
        return

    if amount < 0:
        ErrorStable("Cannot be negative.", 6)
        return

    os.makedirs("USERS", exist_ok=True)

    path = f"USERS/user_{name}.py"
    if os.path.exists(path):
        ErrorStable("User already exists.", 6)
        return

    with open(path, "w") as f:
        f.write(f"amount = {amount}\npassword = \"{password}\"")

    BackToLog()
    Notif("Account Created!", 6)

def Depo():
    global Err
    amount = GetIn()
    

    loc = f"USERS.user_{Name}"
    userAcc = importlib.import_module(loc)
    importlib.reload(userAcc)
    curAmount = getattr(userAcc, "amount")
    userPass = getattr(userAcc, "password")



    try:
        Err.destroy()

        if amount == "":
            ErrorStable("Please Enter Amount.")
            return

        if int(amount) < 0:
            ErrorStable("Positive numbers only.")
            return

        curAmount += int(amount)
        
        with open(f"USERS/user_{Name}.py", "w") as f:
            f.write(f"amount = {curAmount}\npassword = \"{userPass}\"")

        UpdateCurDisplay(curAmount)

    except ValueError:
        ErrorStable("Needs to be valid number/amount.")


def Withdraw():
    global Err
    global Name
    amount = GetIn()

    


    loc = f"USERS.user_{Name}"
    userAcc = importlib.import_module(loc)
    importlib.reload(userAcc)
    curAmount = getattr(userAcc, "amount")
    userPass = getattr(userAcc, "password")

    try:
        Err.destroy()
        if amount == "":
            ErrorStable("Please Enter Amount.")
            return

        if int(amount) < 0:
            ErrorStable("Positive numbers only.")
            return

        if (curAmount - int(amount)) >= 0:
            curAmount -= int(amount)
        else:
            ErrorStable("Insufficient Funds.")
        
        with open(f"USERS/user_{Name}.py", "w") as f:
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
    CheckName = f"USERS.user_{UserNameIn.get()}"
    PassInCompare = UserPassIn.get()

    if not UserNameIn or not PassInCompare:
        ErrorStable("Please fill all fields.", 6)
        return

    try:
        userAccount = importlib.import_module(CheckName)
        getPass = getattr(userAccount, "password")
        Err.destroy()

        if PassInCompare == getPass:
            AccountCurrentAmmount = getattr(userAccount, "amount")
            ClearWin()
            Main(name, AccountCurrentAmmount)
        else:
            ErrorStable("Please Check Password.", 6)
    except ModuleNotFoundError:
        ErrorStable("Please Check Username.", 6)


def BackToLog():
    ClearWin()
    Log()










#PAGES ------------------------------------------------------------------------------------------------------


def Register():

    ClearWin()

    win.columnconfigure(1, weight=1)
    win.rowconfigure(1, weight=1)

    global UserNameIn
    global UserPassIn
    global Amount

    global headerColor

    


    global Container
    Container = Frame(bg="#1e1e1e", pady=20, padx=50)
    Container.grid(row=1, column=1, sticky="ns")
    Container.columnconfigure(1, weight=1)


    Err = Label(Container)

    LogHead = Label(win, text="FalawanExpress", padx=193, bg=headerColor, fg="white", font=("Times", 20, "italic"), pady=10)
    LogHead.grid(row=0, column=0, columnspan=2, sticky="ew", )

    NameLabel = Label(Container, text="Username:", bg="#1e1e1e", fg="white")
    NameLabel.grid(row=2, column=0,sticky="ew")
    UserNameIn = Entry(Container, highlightthickness=2, highlightbackground="grey", bg="#1e1e1e", fg="white")
    UserNameIn.grid(row=2, column=1, sticky="ew")

    PassLabel = Label(Container, text="Password:", bg="#1e1e1e", fg="white")
    PassLabel.grid(row=3, column=0,sticky="ew")
    UserPassIn = Entry(Container, highlightthickness=2, highlightbackground="grey", bg="#1e1e1e", fg="white")
    UserPassIn.grid(row=3, column=1, sticky="ew")

    Amount = Label(Container, text="Initial Deposit:", bg="#1e1e1e", fg="white")
    Amount.grid(row=4, column=0,sticky="ew")
    Amount = Entry(Container, highlightthickness=2, highlightbackground="grey", bg="#1e1e1e")
    Amount.grid(row=4, column=1, sticky="ew")

    UserNameIn.focus_set()

    Button(Container, text="Register", command=Cret).grid(columnspan=2, sticky="e")


    Back = Button(Container, text="Back", command=BackToLog)
    Back.grid(row=5)










def Log():

    win.columnconfigure(1, weight=1)
    win.rowconfigure(1, weight=1)

    global UserNameIn
    global UserPassIn 

    global headerColor


    global Container
    Container = Frame(bg="#1e1e1e", pady=20, padx=50)
    Container.grid(row=1, column=1, sticky="ns")
    Container.columnconfigure(1, weight=1)


    Err = Label(Container)

    LogHead = Label(win, text="FalawanExpress", padx=193, bg=headerColor, fg="white", font=("Times", 20, "italic"), pady=10)
    LogHead.grid(row=0, column=0, columnspan=2, sticky="ew", )

    NameLabel = Label(Container, text="Username:", bg="#1e1e1e", fg="white")
    NameLabel.grid(row=2, column=0,sticky="ew")
    UserNameIn = Entry(Container, highlightthickness=2, highlightbackground="grey", bg="#1e1e1e", fg="white")
    UserNameIn.grid(row=2, column=1, sticky="ew")

    PassLabel = Label(Container, text="Password:", bg="#1e1e1e", fg="white")
    PassLabel.grid(row=3, column=0,sticky="ew")
    UserPassIn = Entry(Container, highlightthickness=2, highlightbackground="grey", bg="#1e1e1e", fg="white", show="*")
    UserPassIn.grid(row=3, column=1, sticky="ew")

    EnterBut = Button(Container, text="Login", command=LogCheck)   
    EnterBut.grid(row=4, column=0, columnspan=2, sticky="ew")

    UserNameIn.focus_set()

    RegisterCont = Frame(Container, bg="#1e1e1e")
    RegisterCont.grid(column=0, row=5, columnspan=2)

    Ques = Label(RegisterCont, text="or", bg="#1e1e1e", fg="white")
    Ques.grid(column=0, row=5, sticky="e")

    Button(RegisterCont, text="Create an Account NOW!", command=Register).grid(column=1, row=5)
    





def Main(user, amount):

    win.columnconfigure(1, weight=1)

    global Container
    Container = Frame(bg="#1e1e1e", pady=20, padx=50)
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

    global headerColor
 

    Name = user
    currentDisplay = amount


    Back = Button(Container, text="Logout", command=BackToLog)
    Back.grid(row=5)


    head = Label(win, text=f"Welcome back, {Name}!", padx=193, bg=headerColor, fg="white", font=("Times", 20, "italic"), pady=10)
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





