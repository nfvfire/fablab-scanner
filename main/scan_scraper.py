import traceback
from datetime import datetime
import csv
from operator import index
import json
import pytz
from random import randint
import sys
sys.path.append('/opt/scanner/')
import display

# create a timezone object for Europe/Paris
tz = pytz.timezone('Europe/Paris')

# define the admin card that checks everybody out
admin = "20704000379845"

# create the list of users in the Fablab
users = []

# path to the directory of the project
path = "/opt/scanner/"

# path to the shared Folder on the NAS Synology
path2 = "/mnt/synology/Database/"

# define a debug function without terminal output 
def print_to_file(text_to_display):
    with open(f"{path}debug.txt", "a") as file:
        file.write(str(text_to_display) + "\n")

# define a function that loads the users from "today's" JSON file into the user list
def json_load_users():
    global users
    try:
        with open(f"{path}Stats_Openlabs/"+current_date + ".json", "r") as json_file:
            users = json.loads(json_file.read())
    except:
        print_to_file("File doesn't exist")
        users = []

# define a function that dumps the users from the user list into "today's" JSON file
def json_dump_users():
    with open(f"{path}Stats_Openlabs/"+current_date + ".json", "w") as write_file:
        write_file.write(json.dumps(users, indent=4))

    print_to_file(users)

# create an overwrite function, that checks everybody with gone = 0 out, to be used at noon and in the evening, triggered by the admin card
def timelimit():
    json_load_users()
    for user in users:
        if user['gone'] == False:
            user['time_dif'] = str(datetime.now() - datetime(year, month, day, hour=user['time'][0], minute=user['time'][1]))
            user['gone'] = True
    json_dump_users()

# getting the data from the barcode scanner
fp = open('/dev/hidraw0', 'rb')

# create a translator function for the scanner data
def hid2ascii(car):
    conv_table = {
        0:['', ''],
        4:['a', 'A'],
        5:['b', 'B'],
        6:['c', 'C'],
        7:['d', 'D'],
        8:['e', 'E'],
        9:['f', 'F'],
        10:['g', 'G'],
        11:['h', 'H'],
        12:['i', 'I'],
        13:['j', 'J'],
        14:['k', 'K'],
        15:['l', 'L'],
        16:['m', 'M'],
        17:['n', 'N'],
        18:['o', 'O'],
        19:['p', 'P'],
        20:['q', 'Q'],
        21:['r', 'R'],
        22:['s', 'S'],
        23:['t', 'T'],
        24:['u', 'U'],
        25:['v', 'V'],
        26:['w', 'W'],
        27:['x', 'X'],
        28:['y', 'Y'],
        29:['z', 'Z'],
        30:['1', '!'],
        31:['2', '@'],
        32:['3', '#'],
        33:['4', '$'],
        34:['5', '%'],
        35:['6', '^'],
        36:['7' ,'&'],
        37:['8', '*'],
        38:['9', '('],
        39:['0', ')'],
        40:['\n', '\n'],
        41:['\x1b', '\x1b'],
        42:['\b', '\b'],
        43:['\t', '\t'],
        44:[' ', ' '],
        45:['_', '_'],
        46:['=', '+'],
        47:['[', '{'],
        48:[']', '}'],
        49:['\\', '|'],
        50:['#', '~'],
        51:[';', ':'],
        52:["'", '"'],
        53:['`', '~'],
        54:[',', '<'],
        55:['.', '>'],
        56:['/', '?'],
        100:['\\', '|'],
        103:['=', '='],
        }

    return conv_table[car][0]

# create the list where the numbers scanned by the barcode scanner will be stored
code = []
display.init()
# main loop where everything happens
while True:
    # use try/except to restart the program if there's a problem
    try:
        # read the number of the barcode with the max length
        while len(code) < 14:
            # fp.read reads the usb port of the barcode scanner
            buffer = fp.read(8) 
            car = buffer[2]
            # transform the car to an ascii char if it's not 0
            if car != 0: 
                char = hid2ascii(car)
                # add the char to the final code of 14 characters if it's not a void character
                if char != '\n':
                    code.append(char)
        # write the code as a str in the scan variable and free the "code" list for the next scan
        scan = "".join(code)
        # reinitialize the temporary code list
        code = []
        
        # after getting the right code define the current time variables
        year = datetime.now().year
        month = datetime.now().month
        day = datetime.now().day
        minute = datetime.now().minute
        hour = datetime.now().hour
        current_date = str(datetime.now())[0:10]

        # check if it's the admin card to check out everybody at noon and in the evening, then restart the main loop
        if scan == admin:
            timelimit()
            display.admin()
            continue

        # read the database csv from the NAS, and split on ";" the line
        with open(f"{path2}db.csv", "r") as read_file:
            csv_file = csv.reader(read_file, delimiter=";")
            # define a variable to check if the user is in the current database
            db_found = False
            # loop through the csv list
            for row in csv_file:
                # if current rows first value (BARCODE) is equal to input, give back the other values (NAME, SURNAME, EMAIL, AGE, CITY)
                if scan == row[0]:
                    db_found = True
                    user_age = year - int(row[3][6:10])
                    user_city = row[4]
                    user_name = row[1]
                    user_surname = row[2]
                    user_mail = row[5]
                    # step out of the loop if found
                    break
            # define a variable to search for the user in the list of users already in the Lab
            user_found = False
            # define a variable if the card is scanned another time too fast
            too_fast = False
            # if they are the first person to scan, skip the process to check for the user
            if len(users) == 0:
                    time = (hour, minute)
                    time_dif = ""
                    gone = False
            else:
                # look for the code in the new csv and overwrite it or create it
                # We check if the user is in the list
                for key, user in enumerate(users):
                    # It's the second time they scan ? they aren't already gone?
                    if scan == user['code'] and user['gone'] == False: 
                        user_found = True
                        user_name = user['name']
                        # if they scan for the second time in under 2 minutes, the person's data is not treated
                        if user['time'][0] == hour and minute - user['time'][1] < 2:
                            too_fast = True
                            pass
                        else:
                            gone = True
                            users[key]["time_dif"] = str(datetime.now() - datetime(year, month, day, hour=user['time'][0], minute=user['time'][1]))
                            users[key]["gone"] = gone
                            

            # If we don't find the user we add it with default values
            if not user_found:
                time = (hour, minute)
                time_dif = ""
                gone = False
                    
                if not db_found:
                    user_age = "ANONYME"
                    user_city = "ANONYME"
                    user_name = "ANONYME"
                    user_surname = "ANONYME"
                    user_mail = "ANONYME"



                users.append({
                    'code' : scan,
                    'name' : user_name,
                    'surname' : user_surname,
                    'email' : user_mail,
                    'age' : user_age,
                    'city' : user_city,
                    'time' : time,
                    'time_dif' : time_dif,
                    'gone' : gone
                    })

        # display different messages depending on the 
        if gone:
            display.goodbye(user_name)
        elif not too_fast:
            display.welcome(user_name)
        elif too_fast:
            display.error()
        json_dump_users()
    except BaseException as ex:
        print_to_file(traceback.format_exc())
