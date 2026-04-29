
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


def GetIn():
    global Name
    global Amount
    return Name.get(), Amount.get()


def UpdateCurDisplay(newDisplay):
    global currentDisplay

    Current = Label(win, text=f"Current: {newDisplay}", highlightthickness=1, highlightbackground="Green", padx=170)
    Current.grid(row=4, column=0, columnspan=2, sticky="ew")


def Cret():
    global Name
    global Amount

    name = Name.get()
    amount = int(Amount.get())


    with open(f"USERS/{name}.py", "w") as cret:
        cret.write(f"amount = {amount}")


def Depo():
    name, amount = GetIn()


    loc = f"USERS.{name}"
    userAcc = importlib.import_module(loc)
    importlib.reload(userAcc)
    curAmount = getattr(userAcc, "amount")



    curAmount += int(amount)

    with open(f"USERS/{name}.py", "w") as f:
        f.write(f"amount = {curAmount}")

    UpdateCurDisplay(curAmount)


def Withdraw():
    name, amount = GetIn()


    loc = f"USERS.{name}"
    userAcc = importlib.import_module(loc)
    importlib.reload(userAcc)
    curAmount = getattr(userAcc, "amount")

    if (curAmount - int(amount)) >= 0:
        curAmount -= int(amount)


    with open(f"USERS/{name}.py", "w") as f:
        f.write(f"amount = {curAmount}")

    UpdateCurDisplay(curAmount)








currentDisplay = "None"



head = Label(win, text="BANK", highlightthickness=1, highlightbackground="grey")
head.grid(row=0, column=0, columnspan=10, sticky="ew")



tex1 = Label(win, text="Username ⬇️", highlightthickness=1, highlightbackground="grey")
tex1.grid(row=1, column=0, sticky="ew")

tex2 = Label(win, text="Amount ⬇️", highlightthickness=1, highlightbackground="grey")
tex2.grid(row=1, column=1, sticky="ew")



Name = Entry(win, highlightthickness=1, highlightbackground="grey")
Name.grid(row=2, column=0, sticky="ew")

Amount = Entry(win, highlightthickness=1, highlightbackground="grey")
Amount.grid(row=2, column=1, sticky="ew")



Dep = Button(text="Deposit", command=Depo)
Dep.grid(row=3, column=0, sticky="ew")

Wit = Button(text="Withdraw", command=Withdraw)
Wit.grid(row=3, column=1, sticky="ew")



Current = Label(win, text=f"Current: {currentDisplay}", highlightthickness=1, highlightbackground="Green", padx=170)
Current.grid(row=4, column=0, columnspan=2, sticky="ew")






win.mainloop()





