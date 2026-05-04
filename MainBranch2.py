

import importlib

from tkinter import *
win = Tk()
win.title("Bank Prototype")
win.geometry("434x250")
win.attributes("-topmost", True)

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

    Current = Label(win, text=f"Current: {newDisplay}", highlightthickness=1, highlightbackground="Green", padx=170)
    Current.grid(row=4, column=0, columnspan=2, sticky="ew")

def ErrorStable(error, position = 5):
    global Err

    Err = Label(win, text=f"{error}", fg="Red")
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
            ErrorStable("Negative numbers are not allowed as a request!")
            return

        curAmount += int(amount)
        
        with open(f"USERS/{Name}.py", "w") as f:
            f.write(f"amount = {curAmount}\npassword = \"{userPass}\"")

        UpdateCurDisplay(curAmount)

    except ValueError:
        ErrorStable("Needs to be valid number/amount!")


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
            ErrorStable("Negative numbers are not allowed as a request!")
            return

        if (curAmount - int(amount)) >= 0:
            curAmount -= int(amount)
        
        with open(f"USERS/{Name}.py", "w") as f:
            f.write(f"amount = {curAmount}\npassword = \"{userPass}\"")

        UpdateCurDisplay(curAmount)

    except ValueError:
        ErrorStable("Needs to be valid number/amount!")


def LogCheck():
    global UserPassIn
    global UserNameIn
    global Err

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
            ErrorStable("Please Check Password.", 4)
    except ModuleNotFoundError:
        ErrorStable("Please Check Username.", 4)












#PAGES ------------------------------------------------------------------------------------------------------

def Log():

    global UserNameIn
    global UserPassIn

    LogHead = Label(win, text="Log In", highlightthickness=2, highlightbackground="grey", padx=193)
    LogHead.grid(row=0, column=0, columnspan=2,sticky="ew")

    NameLabel = Label(win, text="Username ⬇️", highlightthickness=2, highlightbackground="grey")
    NameLabel.grid(row=1, column=0,sticky="ew")
    UserNameIn = Entry(win, highlightthickness=2, highlightbackground="grey")
    UserNameIn.grid(row=2, column=0, sticky="ew")

    PassLabel = Label(win, text="Password ⬇️", highlightthickness=2, highlightbackground="grey")
    PassLabel.grid(row=1, column=1,sticky="ew")
    UserPassIn = Entry(win, highlightthickness=2, highlightbackground="grey")
    UserPassIn.grid(row=2, column=1, sticky="ew")

    EnterBut = Button(win, text="Enter", command=LogCheck)   
    EnterBut.grid(row=3, column=0, columnspan=2, sticky="ew")






    # while True:
    #     name = input("Username: ")

    #     userAcc = importlib.import_module(f"USERS.{name}")
    #     userPass = getattr(userAcc, "password")

    #     inPass = input("Password: ")

    #     if inPass == userPass:
    #         UserAmount = getattr(userAcc, "amount")
    #         Main(name, UserAmount)
    #         break
    #     else:
    #         print("Check Name or Password!")

    







def Main(user, amount):
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

    head = Label(win, text="BANK", highlightthickness=1, highlightbackground="grey")
    head.grid(row=0, column=0, columnspan=10, sticky="ew")

    tex2 = Label(win, text="Amount ⬇️", highlightthickness=1, highlightbackground="grey")
    tex2.grid(row=1, column=0, columnspan=2, sticky="ew")

    Amount = Entry(win, highlightthickness=2, highlightbackground="grey")
    Amount.grid(row=2, column=0, columnspan=2, sticky="ew")

    Dep = Button(win, text="Deposit", command=Depo)
    Dep.grid(row=3, column=0, sticky="ew")

    Wit = Button(win, text="Withdraw", command=Withdraw)
    Wit.grid(row=3, column=1, sticky="ew")

    Current = Label(win, text=f"Current: {currentDisplay}", highlightthickness=1, highlightbackground="Green", padx=170)
    Current.grid(row=4, column=0, columnspan=2, sticky="ew")

    Err = Label(win)






#SYSTEM STARTS ----------------------------------------------------------------------***********


Log()
# Main("user1", 100)










            



win.mainloop()





