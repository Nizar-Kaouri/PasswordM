import random
import datetime
import pyperclip
import stdiomask as stdiomask
import typer
import string
import os

app = typer.Typer()

master_password = "admin"

def encrypt(data, shift):
    encrypted = ""
    for i in range (len(data)):
        char = data[i]
        if (char.isupper()):
            encrypted += chr((ord(char) + shift - 65) % 26 + 65 )
        elif (char.islower()):
            encrypted += chr((ord(char) + shift - 97) % 26 + 97 )
        elif (char.isdigit()):
            number = (int(char) + shift) % 10
            encrypted += str(number)
        else:
            encrypted += char
    return encrypted

def decrypt(data, shift):
    decrypted = ""
    for i in range (len(data)):
        char = data[i]
        if (char.isupper()):
            decrypted += chr((ord(char) - shift - 65) % 26 + 65 )
        elif (char.islower()):
            decrypted += chr((ord(char) - shift - 97) % 26 + 97 )
        elif (char.isdigit()):
            number = (int(char) - shift) % 10
            decrypted += str(number)
        else:
            decrypted += char
    return decrypted

def generator(password_length):
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    numbers = string.digits
    symbols = string.punctuation
    password = lower + upper + numbers + symbols
    temp = random.sample(password, password_length)
    password = "".join(temp)
    return password

def kopieren(x):
    shift = 5
    file = open("passwords.txt", 'r')
    zeilen = file.readlines()
    for rows in zeilen:
        column = rows.split('|')
        titel = decrypt(column[0],shift)
        if x.lower() in titel.lower():
            print("Benutzername:" + decrypt(column[1],shift))
            pyperclip.copy(decrypt(column[2][column[2].index('')+1:],shift))
            print("Password copied to clipboard.")

    file.close()

@app.command()
def add(titel: str, name: str, password_length: int):
    shift =  5
    file = open("passwords.txt", 'a')
    password = generator(password_length)
    pyperclip.copy(password)
    file.write(encrypt(titel,shift) + " | " + encrypt(name,shift) + " | " + encrypt(password,shift) + "\n")
    print("Password generated and copied to Clipboard")
    file.close()

@app.command()
def display():
    shift = 5
    master_password_input = stdiomask.getpass()
    if master_password_input == master_password:
        file = open("passwords.txt", 'r')
        for i in file:
            data = i.split("|")
            print(decrypt(data[0],shift) + "|"+ decrypt(data[1],shift) + "|"+ decrypt(data[2],shift))
        file.close()
    else:
        print("Access Denied . Wrong Master Password. ")

@app.command()
def delete(x):
    shift = 5
    with open("passwords.txt", "r+") as file:
        print("Press Y for Yes or else for No.")
        choice = input("Do you really want to delete: " + str(x) +"\n")
        if choice == "y":
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if encrypt(x,shift) not in line:
                    file.write(line)
            file.truncate()
            print("Done.")
        else:
            print("Cancelled.")

@app.command()
def copy(x):
    if not os.path.isfile("timestamp.txt"):
        timefile = open("timestamp.txt", 'w')
        timefile.write("2021-06-11 18:42:16.058009")
        timefile.close()
    timefile = open("timestamp.txt", 'r')
    timestampstr = timefile.readline()
    timestamp = datetime.datetime.strptime(timestampstr,"%Y-%m-%d %H:%M:%S.%f")
    timedelta = datetime.datetime.now() - timestamp
    if timedelta > datetime.timedelta(minutes=1):
        master_password_input = stdiomask.getpass()
        if master_password == master_password_input:
            timefile = open("timestamp.txt", 'w')
            timefile.write(str(datetime.datetime.now()))
            kopieren(x)
        else:
            print("Access denied.")
    else:
        timefile = open("timestamp1.txt", 'w')
        timefile.write(str(datetime.datetime.now()))
        kopieren(x)

@app.command()
def clear():
    print("Press Y for Yes or else for No.")
    choice = input("Do you really want to clear all your passwords ? \n ")
    if choice == "y":
        os.remove("passwords.txt")
        print("All passwords cleared.")
    else:
        print("Canceled.")

if __name__ == "__main__":
    app()