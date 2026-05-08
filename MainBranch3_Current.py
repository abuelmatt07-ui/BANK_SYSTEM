

import importlib
import os
from tkinter import *
import datetime

win = Tk()
win.title("Bank")
win.geometry("500x400")
win.attributes("-topmost", True) # MAKES WINDOW APPEAR ON THE TOP WHEN RAN




win.config(bg="#44444E") # CONTROLS BACKGROUND COLOR
headerColor = "#37353E" # CONTROLS HEADER COLOR
Column = 500 # COLUMN/MENU WIDTH







#WINDOW FUNCTIONS --------------------------------------------------------
def Exit(event): # MAKES ESC AN ALTERNATIVE CLOSE FOR WINDOW
    win.destroy()
win.bind("<Escape>", Exit)



def ClearWin(): # CLEARS WINDOW. USED FOR PAGE TRANSITIONS(LOGIN PAGE TO MAIN MENU PAGE)
   for widget in win.winfo_children():
    widget.destroy()



#FRONT-END FUNCTIONS ------------------------------------------

def UpdateCurDisplay(newDisplay): # FORCE UPDATES CURRENT IN MAIN MENU
    global currentDisplay
    Current.config(text=f"Current: {newDisplay}$")



def ErrorStable(error, position = 10): # USED AS A TEMPLATE FOR USER INPUT ERROR (POSITION IS FOR ROW OF THE LABEL)
    global Err
    global Container
    Err.destroy()
    Err = Label(Container, text=f"Invalid: {error}", fg="Red", bg="#1e1e1e")
    Err.grid(row=position, column=0, columnspan=10, sticky="ew")




def Notif(text, position = 6): # SAME AS EERORSTABLE BUT GREEN
    global Err
    global Container
    Err = Label(Container, text=f"{text}", fg="#72BAA9", bg="#1e1e1e")
    Err.grid(row=position, column=0, columnspan=10, sticky="ew")

#BACK-END FUNCTIONS ---------------------------------------

def GetIn(): # GETS THE INPUT FROM THE AMOUNT ENTRY AND RETURNS IT FOR STORING OF VARIABLE
    global Amount
    return Amount.get()

def AccessAccount(Name): # GETS PASSWORD AND AMMOUNT INSIDE THE LOC(LOCATION) THAT HAS THE USERNAME
    loc = f"USERS.user_{Name}"
    userAcc = importlib.import_module(loc)
    importlib.reload(userAcc)
    curAmount = getattr(userAcc, "amount")
    userPass = getattr(userAcc, "password")

    return curAmount, userPass

def Record(name, amount, total, type): # SAVES THE TRANSACTION ON THE USERS TXT FILE
    with open(f"UserRecords/user_record_{name}.txt", "a") as rec:
        now = datetime.datetime.now()
        rec.write(f"{type} ~ {amount} ~ {total} ~ {now}\n")


def BackToLog(): # CLEANS THE WINDOW AND OPENS LOGIN PAGE
    ClearWin()
    Log()



#PAGE FUNCTIONS ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def Cret(): # CREATING A USER ACCOUNT ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    global Err
    global Amount

    Err = Label(Container)

    # INVALID CHARACTERS/STRINGS FOR USER INPUT - RELATED TO USER NAMES DUE TO POSSIBLE SYNTAX ERRORS FOR FILE NAMES (EX. NAME.NAME.PY)
    invalidChars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', 
                    '-', '+', '=', '{', '}', '[', ']', '|', '\\', ':', 
                    ';', '"', "'", '<', '>', ',', '.', '?', '/', '`', '~', '_']
    
    name = UserNameIn.get().strip()
    password = UserPassIn.get().strip()
    amount = Amount.get().strip()

    if not name or not password or not amount:
        ErrorStable("Fill all fields.", 6)
        return
    
    for char in invalidChars:
        if char in name: # CHECKS IF CHAR FROM INVALID CHARACTERS IS IN NAME
            ErrorStable("Numbers & Letters for Username Only.", 6)
            return
        
    if " " in name:
        ErrorStable("No Space on Username Allowed.", 6)
        return
    
    try:
        amount = int(amount)
        if amount < 0:
            ErrorStable("Cannot be negative.", 6)
            return
    except ValueError:
        ErrorStable("Amount must be number.", 6)
        return



    os.makedirs("USERS", exist_ok=True) # CHECKS IF USERS FOLDER EXISTS AND CREATES ONE IF NOT



    path = f"USERS/user_{name}.py" # MAKES A POINTER FOR USERNAMED FILE


    if os.path.exists(path): # CHECKS IF USER WITH SAME NAME ALREADY EXISTS
        ErrorStable("Username already taken.", 6)
        return

    with open(path, "w") as f:
        f.write(f"amount = {amount}\npassword = \"{password}\"")


    Record(name, amount, amount, "Opened Account") # DOUBLE AMOUNT BECAUSE ACCOUNT IS ONLY CREATED. NO DEPOSIT MADE OR WITHDRAW
    BackToLog()
    Notif("Account Created!", 6)



def Depo(): # DEPOSIT INTO ACCOUNT ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    global Err
    amount = GetIn()
    
    curAmount, userPass = AccessAccount(Name)


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


        Record(Name, amount, curAmount, "Deposit")
        UpdateCurDisplay(curAmount)

    except ValueError:
        ErrorStable("Needs to be valid number/amount.")


def Withdraw(): # WITHDRAW FROM ACCOUNT -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    global Err
    global Name
    amount = GetIn()

    curAmount, userPass = AccessAccount(Name)


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

            with open(f"USERS/user_{Name}.py", "w") as f:
                f.write(f"amount = {curAmount}\npassword = \"{userPass}\"")

            Record(Name, amount, curAmount, "Withdraw")


        else:
            ErrorStable("Insufficient Funds.")


        UpdateCurDisplay(curAmount)

    except ValueError:
        ErrorStable("Needs to be valid number/amount.")




def LogCheck(): # CHECKS IF ENTRY BY USER IS VALID ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
            importlib.reload(userAccount)
            AccountCurrentAmmount = getattr(userAccount, "amount")
            ClearWin()
            Main(name, AccountCurrentAmmount)
        else:
            ErrorStable("Please Check Password.", 6)
    except ModuleNotFoundError:
        ErrorStable("Please Check Username.", 6)





Toggle = 0 # TOOGLE SWITCH

def ShowRecords(): # DISPLAYS USER'S TRANSACTIONS (USED IN MAIN PAGE) ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    global Name
    global Toggle
    global ContFrame
    global Cont

    global Records

    # (1) WHEN THE SYSTEM FIRST RUNS, THE STARTS AS OFF. BUT WHEN THE FUNCTION IS CALLED -

    if Toggle == 0: # (2) IT CHECKS IF IT IS OFF, IF IT IS OFF IT THE LINES BELOW RUN AND -
        Toggle = 1 # (3) IT ENABLES THE TOGGLE

        try:
            with open(f"UserRecords/user_record_{Name}.txt", "r") as File:
                pass
        except FileNotFoundError:
            ErrorStable("No Records Found.")
            return
            

        Records.config(text="Hide")

        ContFrame = Frame(Container, bg="#1e1e1e", pady=20)
        ContFrame.grid(columnspan=2, sticky="ew")
        ContFrame.columnconfigure(0, weight=1)

        Cont = Listbox(ContFrame, highlightthickness=2, highlightbackground="grey")
        Cont.grid(columnspan=2, sticky="ew")

        with open(f"UserRecords/user_record_{Name}.txt", "r") as File:
            
            for count, lines in enumerate(File, start=1):
                Type, Request, Total, Time = lines.split(" ~ ")
                if Type == "Deposit" or Type == "Opened Account":
                    Arrow = "<"
                elif Type == "Withdraw":
                    Arrow = ">"
                else:
                    Arrow = "?"

                Cont.insert("end", f"TX #{count:>3} | {Type:^15} {Arrow}    {f"{Request}$":<9}-- TOTAL: {f'{Total}$':<9} | TIME: {Time}")
    
    else: # BUT IF THE TOGGLE IS ALREADY ON, IT DELETES THE DISPLAY/BOX AND TURNS THE TOGGLE BACK OFF
        ContFrame.destroy()
        Cont.destroy()
        Records.config(text="History")
        Toggle = 0










#PAGES ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# HOW THEY WORK IS THAT EACH FUNCTION/PAGE, WHEN CALLED WILL OPEN THE INDIVIDUAL PAGES. WHEN REGISTER FUNCTION IS CALLED, THE REGISTER PAGE SHOWS UP.


def Register(): # REGISTER PAGE ====================================================================================================================================================================================

    ClearWin()

    win.columnconfigure(1, weight=1)
    win.rowconfigure(1, weight=1)

    global UserNameIn
    global UserPassIn
    global Amount
    global Column

    global headerColor



    global Container
    Container = Frame(bg="#1e1e1e", pady=20, padx=50, width=Column)
    Container.grid(row=1, column=1, sticky="ns")
    Container.columnconfigure(1, weight=1)
    Container.grid_propagate(False)


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






def Log(): # LOGIN PAGE ====================================================================================================================================================================================

    win.columnconfigure(1, weight=1)
    win.rowconfigure(1, weight=1)

    global UserNameIn
    global UserPassIn 

    global headerColor
    global Column


    global Container
    Container = Frame(bg="#1e1e1e", pady=20, padx=50, width=Column)
    Container.grid(row=1, column=1, sticky="ns")
    Container.columnconfigure(1, weight=1)
    Container.grid_propagate(False)


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
    win.bind("<Return>", lambda event: LogCheck())

    UserNameIn.focus_set()

    RegisterCont = Frame(Container, bg="#1e1e1e")
    RegisterCont.grid(column=0, row=5, columnspan=2)

    Ques = Label(RegisterCont, text="or", bg="#1e1e1e", fg="white")
    Ques.grid(column=0, row=5, sticky="e")

    Button(RegisterCont, text="Create an Account NOW!", command=Register).grid(column=1, row=5)
    





def Main(user, amount): # MAIN MENU PAGE ====================================================================================================================================================================================

    win.columnconfigure(1, weight=1)

    global Column

    global Container
    Container = Frame(bg="#1e1e1e", pady=20, padx=50, width=Column)
    Container.grid(row=1, column=1, sticky="ns")
    Container.columnconfigure(1, weight=1)
    Container.grid_propagate(False)


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

    global Records
    global ContFrame
    global Cont

    ContFrame = Frame()
    Cont = Listbox()

    global headerColor
 

    Name = user
    currentDisplay = amount


    Back = Button(Container, text="Logout", command=BackToLog)
    Back.grid(row=5)

    Records = Button(Container, text="History", command=ShowRecords)
    Records.grid(row=5, column=1, sticky="e")


    head = Label(win, text=f"Welcome back, {Name}!", padx=193, bg=headerColor, fg="white", font=("Times", 20, "italic"), pady=10)
    head.grid(row=0, column=0, columnspan=2, sticky="ew")

    tex2 = Label(Container, text="Amount:", bg="#1e1e1e", fg="white")
    tex2.grid(row=1, column=0, sticky="ew")

    Amount = Entry(Container, highlightthickness=2, highlightbackground="grey", bg="#1e1e1e", fg="white")
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

Log() # IT ALL STARTS FROM THIS FUNCTION


win.mainloop()