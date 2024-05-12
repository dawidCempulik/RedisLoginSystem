import redis
import os
import hashlib

redis_host = os.environ.get("REDIS_HOST")
redis_port = os.environ.get("REDIS_PORT")
redis_password = os.environ.get("REDIS_PASSWORD")

if redis_host is None or redis_port is None or redis_password is None:
    print("Environment variables not set. Aborting!")
    exit()


r = redis.Redis(
  host=redis_host,
  port=redis_port,
  password=redis_password,
  decode_responses=True)

name = ""


def exit_program():
    print("Goodbye")
    exit()


def welcome_form() -> int:
    print("Welcome to our very advanced system!\nWould you like to log in or register?")
    while True:
        print("1. Register")
        print("2. Log in")
        print("exit. Exit the program\n")
        choice = input("Choice: ").strip()

        if choice == "1":
            return 1
        if choice == "2":
            return 2
        if choice.upper() == "EXIT":
            exit_program()

        print("That is not an option!")


def register_form():
    print("Register form\n")
    while True:
        login = input("Login: ").strip()
        if r.exists(login):
            print("That login is not available. Choose a different one")
            continue

        password = input("Password: ").strip()
        global name
        name = input("Your name: ").strip()

        r.hset(login, mapping={
            "name": name,
            "password": hashlib.md5(password.encode()).hexdigest()
        })

        print("You have been registered!")
        break


def login_form():
    print("Login form")
    print("If you want to exit the program type exit\n")
    while True:
        login = input("Login: ").strip()
        if login.upper() == "EXIT":
            exit_program()
        password = input("Password: ").strip()
        if password.upper() == "EXIT":
            exit_program()

        if not r.exists(login):
            print("Your login or password is incorrect!")
            continue

        if r.hget(login, "password") != hashlib.md5(password.encode()).hexdigest():
            print("Your login or password is incorrect!")
            continue

        global name
        name = r.hget(login, "name")

        print("You have been logged in!")
        break


def program():
    while True:
        choice = welcome_form()

        if choice == 1:
            register_form()
        elif choice == 2:
            login_form()

        print("Hello ", name)
        print("Now that you're logged in there are so many things you can do! Look!")
        print("1. Log out")
        print("exit. Exit the program")

        choice = input("Choice: ").strip()
        if choice == "1":
            continue
        elif choice.upper() == "EXIT":
            exit_program()


program()
