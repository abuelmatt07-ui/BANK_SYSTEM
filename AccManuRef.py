import importlib

userin = input("Username: ")


loc = f"USERS.{userin}"


try:
    cal = importlib.import_module(loc)
    num = getattr(cal, "cur")

except:

    acc = int(input("Money: "))

    with open(f"USERS/{userin}.py", "a") as f:
        f.write(f"cur = {acc}")

    cal = importlib.import_module(loc)
    num = getattr(cal, "cur")


print(num)







