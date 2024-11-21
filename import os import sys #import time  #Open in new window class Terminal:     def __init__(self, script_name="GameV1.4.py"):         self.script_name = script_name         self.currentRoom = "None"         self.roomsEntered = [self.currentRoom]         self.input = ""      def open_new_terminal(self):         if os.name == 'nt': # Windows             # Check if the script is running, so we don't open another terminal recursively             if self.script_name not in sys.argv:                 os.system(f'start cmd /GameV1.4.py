import os
import sys
#import time

#Open in new window
class Terminal:
    def __init__(self, script_name="GameV1.4.py"):
        self.script_name = script_name
        self.currentRoom = "None"
        self.roomsEntered = [self.currentRoom]
        self.input = ""

    def open_new_terminal(self):
        if os.name == 'nt': # Windows
            # Check if the script is running, so we don't open another terminal recursively
            if self.script_name not in sys.argv:
                os.system(f'start cmd /k python {self.script_name}')
        elif os.name == 'posix':  # Linux, macOS
            if self.script_name not in sys.argv:
                os.system(f'xterm -e python {self.script_name} &')

    def user_input(self):
        print("What do you do?")
        self.input = input("> ").strip().lower()

    # Clear the terminal screen
    # Function is clear_screen()
    @staticmethod
    def clear_screen():
        # For Windows
        if os.name == 'nt':
            os.system('cls')
        # For macOS and Linux
        else:
            os.system('clear')

    # Room entrance tracker
    # Function to check if a room has been entered multiple times
    def check_room_event(self, room):
        # Check if the player has entered the room before
        if room in self.roomsEntered:
            return True
        return False

    def proceed(self, room):
        # Record the player's entry into a new room
        self.currentRoom = room
        self.roomsEntered.append(room)

    def get_current_room(self):
        return self.currentRoom

    def get_rooms_entered(self):
        return self.roomsEntered

T = Terminal()  # Create an instance of the Terminal class
T.open_new_terminal()  # Call the method to open a new terminal



#Tell the player the commands at the beginning of the game
class Commands:
    def __init__(self):
        self.commands = ""

    def tell_commands(self):
        self.commands = "To = Allows you to move to the room or direction stated.\nExamine = Look at an object stated.\nInteract = Pick up or touch an object\nUse = use an object you have interacted with to collect\nOn = Prompted after Use; asks what you want to use your object on.\n\n\nPRESS ENTER TO PROCEED"
        print(self.commands)

C = Commands()



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

G = Greeter()



#Starting the Game
C.tell_commands()
input()
T.clear_screen()
G.ask_name()
T.clear_screen()
G.greet()
input()
T.clear_screen()


while True:

#Entrance Hall
    T.currentRoom = "Entrance Hall"
    while T.currentRoom == "Entrance Hall":
        print("You stand before an Entrance Hall of cobble and wood.\nUnlike the rest of the house, the floors here are stone,with towering pillars of marble sprouting out.\nThe cobble walls crumble around you, spider webs seem to devour every dark corner of the room, and chunks of stone litter the ground.\nA single red carpet runs below your feet and up a grandiose spruce staircase, leading left and right.\nIts red fabric runs like fine wine flowing down the landing.\n\n\nThe room is illuminated only by dim, flickering lanterns that hang from the ceiling. A wooden balcony overlooks the room below.\nYou clutch the note in your hand, then pocket it.\nThe room is eerily quiet, apart from the sound of your own short breathing and the creaking of manor.\n\n\nTwo doors line the right wall, to the Game Room and Lounge, and one sits on the left wall leading to a Dining Room.")
        T.user_input()
        if "" in T.user_input():
            print()
