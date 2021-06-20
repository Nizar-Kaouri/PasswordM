import random                                                                                                           # Module, um zufällige chars zu generieren
import datetime                                                                                                         # Module, um die Timestamps zu speichern
import pyperclip                                                                                                        # Module, um Passwords zu kopieren
import stdiomask as stdiomask                                                                                           # Module, um das Master-Password nicht im KLartext zu zeigen
import typer                                                                                                            # Module, für die Kommandozeilen im CMD
import string                                                                                                           # Module enthalten die benötigten Buchstaben/Zahlen/Symbole
import os                                                                                                               # System Module, um die txt Files zu überprüfen/löschen

app = typer.Typer()                                                                                                     # Wir definieren ein Typer Objekt für die Kommandozeilen


master_password = "admin"                                                                                               # Ein Master Password, dass nur der Benutzer kennt.

def encrypt(data, shift):                                                                                               # Funktion, um Daten zu verschlüsseln
    encrypted = ""
    for i in range (len(data)):
        char = data[i]                                                                                                  # Datei in chars verteilen
        if (char.isupper()):                                                                                            # jede Buchstabe wird um eine bestimmte Zahl 'Shift'
            encrypted += chr((ord(char) + shift - 65) % 26 + 65 )                                                       # im Alphabet weitergeschoben
        elif (char.islower()):
            encrypted += chr((ord(char) + shift - 97) % 26 + 97 )
        elif (char.isdigit()):
            number = (int(char) + shift) % 10
            encrypted += str(number)
        else:
            encrypted += char
    return encrypted                                                                                                    # Verschlüsselte Datai ausgeben

def decrypt(data, shift):                                                                                               # Funktion, um Daten zu entschlüsseln
    decrypted = ""
    for i in range (len(data)):
        char = data[i]                                                                                                  # Datei in chars verteilen
        if (char.isupper()):                                                                                            # jede Buchstabe wird um eine bestimmte Zahl 'Shift'
            decrypted += chr((ord(char) - shift - 65) % 26 + 65 )                                                       # im Alphabet zurückgeschoben
        elif (char.islower()):
            decrypted += chr((ord(char) - shift - 97) % 26 + 97 )
        elif (char.isdigit()):
            number = (int(char) - shift) % 10
            decrypted += str(number)
        else:
            decrypted += char
    return decrypted                                                                                                    # Enstchlüsselte Datei ausgeben

def generator(password_length):                                                                                         # Funktion, um ein Password zu generieren
    lower = string.ascii_lowercase                                                                                      #Klein-Buchstaben
    upper = string.ascii_uppercase                                                                                      #Groß-Buchstaben
    numbers = string.digits                                                                                             #Zahlen
    symbols = string.punctuation                                                                                        #Zeichen
    password = lower + upper + numbers + symbols
    temp = random.sample(password, password_length)                                                                     # Die Character zufällig generieren und
    password = "".join(temp)                                                                                            # zu einem String 'Password' zusammen addieren
    return password

def kopieren(x):                                                                                                        # Funktion, um ein Password von einem txt File zu kopieren,
    shift = 5                                                                                                           # dadurch kann man den Benutzernamen zeigen lassen/ Password kopieren.
    file = open("passwords.txt", 'r')
    zeilen = file.readlines()
    for rows in zeilen:                                                                                                 # Loop, um den Titel und das entsprechende Password zu finden
        column = rows.split('|')
        titel = decrypt(column[0],shift)
        if x.lower() in titel.lower():
            print("Benutzername:" + decrypt(column[1],shift))                                                           # Password entschlüsselt und kopiert
            pyperclip.copy(decrypt(column[2][column[2].index(''):],shift))
            print("Password copied to clipboard.")

    file.close()

@app.command()
def add(titel: str, name: str, password_length: int):                                                                   # add + Titel + Benutzername + Länge des Passwortes
    shift =  5
    file = open("passwords.txt", 'a')
    password = generator(password_length)                                                                               # Ein Password mit der Generator-Funktion erstellen
    pyperclip.copy(password)                                                                                            # Das Password zum Clipboard kopieren
    file.write(encrypt(titel,shift) + " "*(25-len(encrypt(titel,shift))) + "|" +
                encrypt(name,shift) + " "*(25-len(encrypt(name,shift)))+ "|" +
               encrypt(password,shift) + " "*(4-len(encrypt(name,shift))) +"\n")             # Das Password verschlüsseln

    print("Password generated and copied to Clipboard")                                                                 # in einem txt File mit Titel und Benutzername speichern
    file.close()

@app.command()
def display():                                                                                                          # display
    shift = 5
    master_password_input = stdiomask.getpass()                                                                         # Der Benutzer wird nach einem Master-Password gefragt
    if master_password_input == master_password:                                                                        # Bei richtiger Eingabe werden alle Passwörter auf dem Bildschirm angezeigt
        file = open("passwords.txt", 'r')
        for i in file:
            data = i.split("|")
            print(decrypt(data[0],shift) + " "*(25-len(data[0])) + "|" +                                                # Format : TITEL | BENUTZERNAME | PASSWORD
                  decrypt(data[1],shift) + " "*(25-len(data[1])) + "|" +
                  decrypt(data[2],shift) + " "*(4-len(data[2])))
        file.close()
    else:
        print("Access Denied . Wrong Master Password. ")                                                                # Bei falscher Eingabe --> Ablehnungsnachricht

@app.command()
def delete(x):                                                                                                          # delete + TITEL
    shift = 5
    with open("passwords.txt", "r+") as file:
        print("Press Y for Yes or else for No.")                                                                        # Nach einer Bestätigung fragen
        choice = input("Do you really want to delete: " + str(x) +"\n")
        if choice == "y":                                                                                               # Wenn Ja wird die Zeile, die den Titel enthält, gelöscht
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if encrypt(x.lower(),shift) not in line.lower():
                    file.write(line)
            file.truncate()
            print("Done.")
        else:
            print("Cancelled.")                                                                                         # Wenn nicht, abgesagt

@app.command()
def copy(x):                                                                                                            # copy + TITEL
    if not os.path.isfile("timestamp.txt"):                                                                             # Es wird geprüft, ob ein file mit Timestamps schon existiert
        timefile = open("timestamp.txt", 'w')                                                                           # Wenn keines existiert, wird eins mit einem Default Timestamp ertstellt
        timefile.write("2021-06-11 18:42:16.058009")                                                                    # Sonst wird diese If-Anweisung übersprungen
        timefile.close()
    timefile = open("timestamp.txt", 'r')
    timestampstr = timefile.readline()
    timestamp = datetime.datetime.strptime(timestampstr,"%Y-%m-%d %H:%M:%S.%f")                                         # Anfangs-Timestamp erstellt und gespeichert
    timedelta = datetime.datetime.now() - timestamp                                                                     # Differenz zwischen Anfangs-Timestamp und NOW-Timestamp
    if timedelta > datetime.timedelta(minutes=1):                                                                       # Wenn die Differenz größer als die erlaubte Periode ist,
        master_password_input = stdiomask.getpass()                                                                     # wird es nach einem Master-Password gefragt
        if master_password == master_password_input:
            timefile = open("timestamp.txt", 'w')
            timefile.write(str(datetime.datetime.now()))                                                                # Neues NOW-Timestamp ertstellen
            kopieren(x)                                                                                                 # Die Kopieren-Funktion laufen lassen
        else:
            print("Access denied.")
    else:
        timefile = open("timestamp1.txt", 'w')                                                                          # Wenn die Differenz kleiner als die erlaubte Periode ist
        timefile.write(str(datetime.datetime.now()))                                                                    # Neues NOW-Timestamp ertstellen
        kopieren(x)                                                                                                     # Die Kopieren-Funktion laufen lassen

@app.command()
def clear():                                                                                                            # clear
    print("Press Y for Yes or else for No.")                                                                            # Nach einer Bestätigung fragen
    choice = input("Do you really want to clear all your passwords ? \n ")
    if choice == "y":                                                                                                   # Wenn Ja, das txt File löschen
        os.remove("passwords.txt")
        print("All passwords cleared.")
    else:
        print("Canceled.")                                                                                              # Sonst abgesagt


@app.command()
def change(x):
    shift = 5
    new_password = stdiomask.getpass("New Password: ")
    file = open("passwords.txt", 'r')
    zeilen = file.readlines()
    file.close()
    os.remove("passwords.txt")
    file = open("passwords.txt", 'a')
    for rows in zeilen:
        column = rows.split('|')
        titel = decrypt(column[0], shift)
        if x.lower() in titel.lower():
            rows = rows.replace(column[2]," "+encrypt(new_password,shift) + "\n")
            print("Done.")
        file.write(rows)





if __name__ == "__main__":
    app()