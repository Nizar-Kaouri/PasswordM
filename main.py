import random                                                                                                  # Module um zufälligen chars to generieren
import datetime                                                                                                # Module um die Timestamps zu speichern
import pyperclip                                                                                               # Module um Passwords zu copieren
import stdiomask as stdiomask                                                                                  # Module um das Master-Password nicht im KLartext zu zeigen
import typer                                                                                                   # Module für die Kommandozeilen in CMD
import string                                                                                                  # Module enthält die benötigte Buchstaben/Zahlen/Symbole
import os                                                                                                      # System Module um die txt Files zu checken/löschen

app = typer.Typer()                                                                                            # Wir definieren ein Typer Objekt für die Kommandozeilen

master_password = "admin"                                                                                      # Ein Master Password, das nur der Benutzer kennt.

def generator(password_length):                                                                                # Function um ein Password zu generieren
    lower = string.ascii_lowercase                                                                             # Das Password kann Groß/Klein-Buchstaben, Zahlen und Zeichen enthalten
    upper = string.ascii_uppercase
    numbers = string.digits
    symbols = string.punctuation
    password = lower + upper + numbers + symbols
    temp = random.sample(password, password_length)                                                             # Die Character in einer zufälliger Weise generieren, und dann
    password = "".join(temp)                                                                                    # in einem String zusammen addieren
    return password

def copieren(x):                                                                                                # Function um ein Password von einem txt File zu copieren,
    file = open("passwords.txt", 'r')                                                                           # dadurch kann man den Benutzernamen zeigen und password copieren.
    zeilen = file.readlines()
    for rows in zeilen:
        column = rows.split('|')                                                                                # Loop um den Titel und das entsprechende Password zu finden
        titel = column[0]
        if x.lower() in titel.lower():
            print("Benutzername:" + column[1])
            pyperclip.copy(column[2][column[2].index('')+1:])                                                   # Password copiert
            print("Password copied to clipboard.")

    file.close()

@app.command()                                                                                                  #       add + Titel + Benutzername + Länge des Passwortes
def add(titel: str, name: str, password_length: int):
    file = open("passwords.txt", 'a')
    password = generator(password_length)                                                                       # Ein Password mit der Generator- Function erstellen
    pyperclip.copy(password)                                                                                    # Das Password zum Clipboard copieren
    file.write(titel + " | " + name + " | " + password + "\n")                                                  # Das Password in einem txt File mit Titel und Benutzername speichern
    print("Password generated and copied to Clipboard")
    file.close()

@app.command()                                                                                                  # display
def display():
    master_password_input = stdiomask.getpass()                                                                 # Der Benutzer wird nach einem Master-Password gefragt
    if master_password_input == master_password:                                                                # Wenn richtig eingegeben , werden alle Passwörter im Bildschirm gezeigt
        file = open("passwords.txt", 'r')                                                                       # Format : TITEL | BENUTZERNAME | PASSWORD
        text = file.read()
        print(text)
        file.close()
    else:
        print("Access Denied . Wrong Master Password. ")                                                        # wenn falsch eingegeben --> Ablehnungsnachricht

@app.command()                                                                                                  #        delete + TITEL
def delete(x):
    with open("passwords.txt", "r+") as file:                                                                   # Nach einer Bestätigung fragen
        print("Press Y for Yes or else for No.")
        choice = input("Do you really want to delete: " + str(x) +"\n")
        if choice == "y":                                                                                       # Wenn Ja wird die Ziele, die den Titel enthält, gelöscht
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if x not in line:
                    file.write(line)
            file.truncate()
            print("Done.")
        else:
            print("Cancelled.")                                                                                 # Wenn nicht, abgesagen

@app.command()                                                                                                  #        copy + TITEL
def copy(x):
    if not os.path.isfile("timestamp.txt"):                                                                     # Es wird geprüft ob ein file mit Passwörtern schon existiert
        timefile = open("timestamp.txt", 'w')                                                                   # Wenn keins existiert, wird eins ertstellt
        timefile.write("2021-06-11 18:42:16.058009")                                                            # Sonst wird diese If-Anweisung übersprungen
        timefile.close()
    timefile = open("timestamp.txt", 'r')
    timestampstr = timefile.readline()                                                                          # Anfangs-Timestamp
    timestamp = datetime.datetime.strptime(timestampstr,"%Y-%m-%d %H:%M:%S.%f")                                 # Anfangs-Timestamp speichern
    timedelta = datetime.datetime.now() - timestamp                                                             # Differenz zwischen Anfangs-Timestamp und NOW-Timestamp
    if timedelta > datetime.timedelta(minutes=1):                                                               # Wenn die Differenz größer als die erlaubte periode ist,
        master_password_input = stdiomask.getpass()                                                             # wird es nach einem Master-Password gefragt
        if master_password == master_password_input:
            timefile = open("timestamp.txt", 'w')
            timefile.write(str(datetime.datetime.now()))                                                        # wird ein neues NOW-Timestamp ertstellt
            copieren(x)                                                                                         # und dann die Copieren-Fuction laufen lassen
        else:
            print("Access denied.")
    else:
        timefile = open("timestamp.txt", 'w')                                                                   # wenn die Differenz kleiner als die erlaubte periode ist
        timefile.write(str(datetime.datetime.now()))                                                            # wird ein neues NOW-Timestamp ertstellt
        copieren(x)                                                                                             # und dann die Copieren-Fuction laufen lassen

@app.command()                                                                                                  #        clear
def clear():
    print("Press Y for Yes or else for No.")                                                                    # Nach einer Bestätigung fragen
    choice = input("Do you really want to clear all your passwords ? \n ")
    if choice == "y":                                                                                           # Wenn Ja, das txt File löschen
        os.remove("passwords.txt")
        print("All passwords cleared.")
    else:
        print("Canceled.")                                                                                      # Wenn nicht --> absagen

if __name__ == "__main__":
    app()