import time
import SpeechRecognition as sr
import sqlite3
import re
import schedule
import os.path
from os import path
import os
import pyautogui
import requests
from datetime import datetime
import webbrowser
import pyperclip
import Webhook
from sys import platform

#keyboard = Controller()

#listener = sr.Recognizer()
#listener.dynamic_energy_threshold = True
# listener.energy_threshold=40000
#listener.pause_threshold = 0.8
#40000
# print(sr.Microphone.list_microphone_names())
# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))


# def logic():
    # waitForCamera = True
    # while waitForCamera:
    #     try:
    #         with sr.Microphone() as source:
    #             listener.adjust_for_ambient_noise(source, duration=0.2)
    #             print('listening...')
    #             # webhook = Webhook.from_url(
    #             #     "https://discord.com/api/webhooks/806264854133342238/iS2kNDCwCko32tivh4bYpsKlwqdWkLwBNbCo6HZ3kWSZoz_0lbWEQvpIKfXL_0_9a3QL",
    #             #     adapter=RequestsWebhookAdapter())
    #             # webhook.send("waiting to turn camera")
    #             voice = listener.listen(source, phrase_time_limit=5)
    #             Gettext = listener.recognize_google(voice)#change language  language='es-US'
    #             Gettext = Gettext.lower()
    #             print("converting voice to text: " + Gettext)
    #             if (Gettext.find("Luis") != -1 or Gettext.find("lewis") != -1 or Gettext.find("louis") != -1 or Gettext.find("good morning") != -1):
    #             # if 'Louis' in Gettext:
    #                 print("KeyWordDetected " +Gettext)
    #
    #                 webhook = Webhook.from_url(
    #                     "https://discord.com/api/webhooks/806264854133342238/iS2kNDCwCko32tivh4bYpsKlwqdWkLwBNbCo6HZ3kWSZoz_0lbWEQvpIKfXL_0_9a3QL",
    #                     adapter=RequestsWebhookAdapter())
    #                 webhook.send("Prof. Said: " + Gettext)
    #                 break
    #     except:
    #         print('no sound detected...trying again')
    # return True
#def zoomAccount(Username, Password):
def detectOS():
    if platform == "darwin":
        return platform
    elif platform == "win32":
        return platform
    #return platform

def OpenZoom(GetOS):
    if GetOS == "darwin":
        os.System("open /Applications/Zoom.app")
    elif GetOS == "win32":
        OpenZoom = os.getenv('AppData')
        ZoomLocation = '\\Zoom\\bin\\Zoom.exe'
        OpenZoom = OpenZoom + ZoomLocation
        if(path.exists(OpenZoom)):
            os.startfile(OpenZoom)
        else:
            print("You might not have zoom installed on your computer")


def createDB():
    conn = sqlite3.connect('Attend_Class.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE Attend_Class(class_name text, class_link text, class_passcode text, start_time text, end_time text, day text)''')
    conn.commit()
    conn.close()
    print("Created Attend_Class Database")

def remove_DB():
    if(path.exists("Attend_Class.db")):
        os.remove('Attend_Class.db')
        print(" ")
        print('Old Database was remove')
        print(" ")
        time.sleep(2)
    else:
        print(" ")
        print('Database does not exists')
        print(" ")
        time.sleep(2)
def DB_exists():
    if(path.exists("Attend_Class.db")):
        return True
    else:
        return False

def validate_day(inp):
    days = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]

    if inp.lower() in days:
        return True
    else:
        return False

def validate_input(regex,inp):
    if not re.match(regex,inp):
        return False
    return True

def add_DB():
    if(not(path.exists("Attend_Class.db"))):
            createDB()
    op = int(input("1. Add class\n2. Done adding\nEnter option : "))
    class_passcode='no_passcode'
    while(op==1):
        class_name = input("Enter name of the class : ")
        class_link = input("Enter your link or meeting ID : ")
        checkPasscode = input("does your class has a passcode?(yes/no): ")
        if(checkPasscode.lower()=='yes'):
            class_passcode = input("Enter your class pascode : ")
        start_time = input("Enter class start time in 24 hour format: (HH:MM) ")
        while not(validate_input("\d\d:\d\d",start_time)):
            print("Invalid input, try again")
            start_time = input("Enter class start time in 24 hour format: (HH:MM) ")

        end_time = input("Enter class end time in 24 hour format: (HH:MM) ")
        while not(validate_input("\d\d:\d\d",end_time)):
            print("Invalid input, try again")
            end_time = input("Enter class end time in 24 hour format: (HH:MM) ")

        day = input("Enter day (Monday/Tuesday/Wednesday..etc) : ")
        while not(validate_day(day.strip())):
            print("Invalid input, try again")
            end_time = input("Enter day (Monday/Tuesday/Wednesday..etc) : ")


        conn = sqlite3.connect('Attend_Class.db')
        c=conn.cursor()

        # Insert a row of data
        c.execute("INSERT INTO Attend_Class VALUES ('%s','%s','%s','%s','%s','%s')"%(class_name, class_link,class_passcode, start_time, end_time, day))

        conn.commit()
        conn.close()

        print("Class added to database\n")

        op = int(input("1. Add class\n2. Done adding\nEnter option : "))

def view_DB():
    if(path.exists("Attend_Class.db")):
        conn = sqlite3.connect('Attend_Class.db')
        c=conn.cursor()
        for row in c.execute('SELECT * FROM Attend_Class'):
            print(row)
        conn.close()
        time.sleep(5)
    else:
        print(" ")
        print("No DATABASE to display")
        print(" ")
        time.sleep(2)
        #cleanConsole()

def cleanConsole(getOS):
    if getOS == "Darwin":
        clear = lambda: os.system('clear')

    elif getOS == "win32":
        clear = lambda: os.system('cls')
    clear()


def sched():
    if(path.exists("Attend_Class.db")):
        conn = sqlite3.connect('Attend_Class.db')
        c=conn.cursor()
        for row in c.execute('SELECT * FROM Attend_Class'):
            #schedule all classes
            name = row[0]
            class_link = row[1]
            class_passcode = row[2]
            start_time = row[3]
            end_time = row[4]
            day = row[5]

            if day.lower()=="monday":
                schedule.every().monday.at(start_time).do(joinclass,name,class_link,class_passcode,start_time,end_time)
                print("Scheduled class '%s' on %s at %s"%(name,day,start_time))
            if day.lower()=="tuesday":
                schedule.every().tuesday.at(start_time).do(joinclass,name,class_link,class_passcode,start_time,end_time)
                print("Scheduled class '%s' on %s at %s"%(name,day,start_time))
            if day.lower()=="wednesday":
                schedule.every().wednesday.at(start_time).do(joinclass,name,class_link,class_passcode,start_time,end_time)
                print("Scheduled class '%s' on %s at %s"%(name,day,start_time))
            if day.lower()=="thursday":
                schedule.every().thursday.at(start_time).do(joinclass,name,class_link,class_passcode,start_time,end_time)
                print("Scheduled class '%s' on %s at %s"%(name,day,start_time))
            if day.lower()=="friday":
                schedule.every().friday.at(start_time).do(joinclass,name,class_link,class_passcode,start_time,end_time)
                print("Scheduled class '%s' on %s at %s"%(name,day,start_time))
            if day.lower()=="saturday":
                schedule.every().saturday.at(start_time).do(joinclass,name,class_link,class_passcode,start_time,end_time)
                print("Scheduled class '%s' on %s at %s"%(name,day,start_time))
            if day.lower()=="sunday":
                schedule.every().sunday.at(start_time).do(joinclass,name,class_link,class_passcode,start_time,end_time)
                print("Scheduled class '%s' on %s at %s"%(name,day,start_time))

        while True:
            # Checks whether a scheduled task
            # is pending to run or not
            schedule.run_pending()
            if not schedule.jobs:
                break
            time.sleep(1)
    elif(not(path.exists("Attend_Class.db"))):
        print(" ")
        print("Please create your database first")
        print(" ")
        time.sleep(2)
        #cleanConsole()



def joinclass(class_name,class_link,class_passcode, start_time, end_time):
    print('Opening Zoom...')
    OpenZoom(detectOS())
    time.sleep(5)
    classStatus = False
    time.sleep(5)
    #Join with Zoom account
    zoomAccount = pyautogui.locateOnScreen('resources\\join.png', confidence=.8)
    if(not(zoomAccount==None)):
        pyautogui.moveTo(zoomAccount)
        pyautogui.click()
    #join as a guess
    if(zoomAccount == None):
        loginBtn = pyautogui.locateOnScreen('resources\\no_login_join.png', confidence=.8)
        pyautogui.moveTo(loginBtn)
        pyautogui.click()
    time.sleep(3)
    pyperclip.copy(class_link)
    pyautogui.hotkey('ctrl', 'v')
    print("entering class link/ID...")
    time.sleep(3)
    startclass = pyautogui.locateOnScreen('resources\\start_class.png', confidence=.8)
    pyautogui.moveTo(startclass)
    pyautogui.click()
    time.sleep(3)
    if(not(class_passcode == 'no_passcode')):
        print("typing passcode...")
        pyautogui.write(class_passcode)
        time.sleep(3)
        pyautogui.press('enter')
        time.sleep(6)
    print('check for waiting room..')
    check_if_waiting_room = pyautogui.locateOnScreen('resources\\waiting_for_host.png', confidence=.8)
    while(not(check_if_waiting_room == None)):
        classStatus= False
        print('waiting for host to let me in')
        check_if_waiting_room = pyautogui.locateOnScreen('resources\\waiting_for_host.png', confidence=.8)
        time.sleep(4)
    if check_if_waiting_room == None:
        print("in class!")
        classStatus = True
        Webhook.class_status(class_name,classStatus, start_time, end_time)


    leave_class = datetime.strptime(end_time, '%H:%M')
    while(True):
        if(datetime.now().hour == leave_class.hour and datetime.now().minute == leave_class.minute):
            print('leaving class...')
            pyautogui.hotkey('alt', 'q')
            pyautogui.press('enter')
            break
    print('class ended')
def Title():
    print('\tZOOM BOT')
    print(' ')



if __name__ == "__main__":
    try:
        while(True):
            #break
            cleanConsole(detectOS())
            #print (os.getcwd())
            #OpenZoom()
            Title()

            if(DB_exists()):
                op = int(input(("1. Modify\n2. View Database\n3. Remove Database\n4. Start Bot\n5. Exit\nEnter option : ")))
            else:
                op = int(input(("1. Create Database\n2. View Database\n3. Remove Database\n4. Start Bot\n5. Exit\nEnter option : ")))

            if (op == 1):
                add_DB()
            if (op == 2):
                view_DB()
            if(op==3):
                remove_DB()
            if (op == 4):
                sched()
            if(op==5):
                break;

    except KeyboardInterrupt:
        print("Closing program..")
        exit(0)
