

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

def ErrorStable(error):
    global Err

    Err = Label(win, text=f"Error: {error}", fg="Red")
    Err.grid(row=5, column=0, columnspan=10, sticky="ew")



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
            f.write(f"amount = {curAmount}\npassword = {userPass}")

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
            f.write(f"amount = {curAmount}\npassword = {userPass}")

        UpdateCurDisplay(curAmount)

    except ValueError:
        ErrorStable("Needs to be valid number/amount!")






#PAGES ------------------------------------------------------------------------------------------------------

def Log():
    while True:
        name = input("Username: ")

        userAcc = importlib.import_module(f"USERS.{name}")
        userPass = getattr(userAcc, "password")

        inPass = input("Password: ")

        if inPass == userPass:
            UserAmount = getattr(userAcc, "amount")
            Main(name, UserAmount)
            break
        else:
            print("Check Name or Password!")

    







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

    Amount = Entry(win, highlightthickness=1, highlightbackground="grey")
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










            



win.mainloop()





