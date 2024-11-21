import os
import sys
import time

#Open in new window
def open_new_terminal():
    if os.name == 'nt': # Windows
        # Check if the script is running, so we don't open another terminal recursively
        if 'GameV1.3.py' not in sys.argv:
            os.system('start cmd /k python GameV1.3.py')
    elif os.name == 'posix':  # Linux, macOS
        if 'GameV1.3.py' not in sys.argv:
            os.system('xterm -e python GameV1.3.py &')

open_new_terminal()



#Clear the terminal screen
    #Fuction is clear_screen()
def clear_screen():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For macOS and Linux
    else:
        os.system('clear')



# Room entrance tracker
currentRoom = "None"
roomsEntered = [currentRoom]

# Function to check if a room has been entered multiple times
def check_room_event(room):
    global roomsEntered
    # Check if the player has entered the room before
    if room in roomsEntered:
        return True
    return False

def proceed(room):
    global roomsEntered, currentRoom
    # Record the player's entry into a new room
    currentRoom = room
    roomsEntered.append(room)

def get_current_room():
    global currentRoom
    return currentRoom

def get_rooms_entered():
    global roomsEntered
    return roomsEntered


#Tell the player the commands at the beginning of the game
class Commands:
    def __init__(self):
        self.commands = ""

    def tell_commands(self):
        self.commands = print("To = Allows you to move to the room or direction stated.\nExamine = Look at an object stated.\nInteract = Pick up or touch an onject\nUse = use an object you have interacted with to collect\nOn = Prompted after Use; askes what you want to use your object on.\n\n\nPRESS ENTER TO PROCEED")

commands = Commands()


#Greet at beginning of game
class Greeter:
    def __init__(self):
        self.name = ""
    def ask_name(self):
        self.name = input("What is your name?\n")
    def greet(self):
        print(f"Dearest {self.name},\n"
              "\n"
              "It has been awhile since we last spoke, hasn't it? 10 years, I reckon.\n"
              "10 years too long. Not a day has gone by that I haven't wanted to speak to you,\n"
              "share an idea, a revelation, a new discovery, but nothing felt big enough…\n"
              "Nothing seems to warrant contacting you again, especially considering the terms of our last conversation.\n"
              "But this time I find myself having encountered something extraordinary.\n"
              "A development in my genetic research that could change our very world.\n"
              "And we are far too wise to hang on to old grudges when science is involved.\n"
              "\n"
              "So I invite you, old friend, to visit me at my mansion so we may discuss this new discovery.\n"
              "For I feel your input would be most valuable.\n"
              "I have attached the address to the back of this letter, along with some money to get you here.\n"
              "And if you can’t make it, keep it. But I do wish to see you again.\n"
              "\n"
              "Sincerely,\n"
              "\n"
              "Dr. Elias's Finch\n"
              "\n\n\n"
              "PRESS ENTER TO PROCEED")

greeter = Greeter()



#Starting the Game
commands.tell_commands()
input()
clear_screen()
greeter.ask_name()
clear_screen()
greeter.greet()
input()
clear_screen()



#Entrance Hall
currentRoom = "Entrance Hall"
if currentRoom == "Entrance Hall":
    if check_room_event("Entrance Hall"):
        print("You stand before an Entrance Hall of cobble and wood. The floors here are stone, with towering pillars of marble sprouting out.\nThe cobble walls crumble around you, spider webs seem to devour every dark corner of the room, and chunks of stone litter the ground.\nA single red carpet runs below your feet and up a grandiose spruce staircase, leading left and right.\nThe room is illuminated only by dim, flickering lanterns that hang from the ceiling. A wooden balcony overlooks the room below.\nTwo doors sit along the left and right walls.")
    else:
        print("You stand before an Entrance Hall of cobble and wood.\nUnlike the rest of the house, the floors here are stone,with towering pillars of marble sprouting out.\nThe cobble walls crumble around you, spider webs seem to devour every dark corner of the room, and chunks of stone litter the ground.\nA single red carpet runs below your feet and up a grandiose spruce staircase, leading left and right.\nIts red fabric runs like fine wine flowing down the landing. A wooden balcony overlooks the room below.\nThe room is illuminated only by dim, flickering lanterns that hang from the ceiling.\nYou clutch the note in your hand, then pocket it.\nThe room is eerily quiet, apart from the sound of your own short breathing and the creaking of manor.\nTwo doors sit along the left and right walls.")
