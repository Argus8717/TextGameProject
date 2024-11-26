
import os
import sys
import time
import threading
import json

class Gameloop:
    def __init__(self, script_name="GameV1.6.py"):
        self.script_name = script_name
        #Tracking visible to player
        self.currentRoom = ""
        self.roomsEntered = []
        self.inventory = []
        #Hidden tracking
        self.roomEntryCounts = {'Trophy Room':0, 'Long Hallway':0}
        self.interactions = []
        self.input = ""
        self.monster = "Unknown"
        self.roomDescribe = ""

        #Initialization of state to copy game attributes
        self.state = {
            "currentRoom": self.currentRoom,
            "roomsEntered": self.roomsEntered,
            "roomEntryCounts": self.roomEntryCounts,
            "inventory": self.inventory,
            "interactions": self.interactions,
            "monster": self.monster,
            "description": self.roomDescribe
        }


    def save_game(self, filename = "savegame.json"):
        try:
            #Update game state before saving
            self.state = {
                "currentRoom": self.currentRoom,
                "roomsEntered": self.roomsEntered,
                "roomEntryCounts": self.roomEntryCounts,
                "inventory": self.inventory,
                "interactions": self.interactions,
                "monster": self.monster,
                "description": self.roomDescribe
            }
            with open(filename, "w") as file:
                json.dump(self.state, file, indent=4)
            print("Game saved successfully! You may close this window.")
        except Exception as e:
            print(f"An error occurred while saving the game: {e}")
        finally:
            # Exit the program after saving
            sys.exit(0)

    def load_game(self, filename = "savegame.json"):
        try:
            with open(filename, "r") as file:
                loaded_state = json.load(file)

                # Update the instance attributes with the loaded state
                self.currentRoom = loaded_state.get("currentRoom", "None")
                self.roomsEntered = loaded_state.get("roomsEntered", [])
                self.roomEntryCounts = loaded_state.get("roomEntryCounts", {"Trophy Room": 0})
                self.inventory = loaded_state.get("inventory", [])
                self.interactions = loaded_state.get("interactions", [])
                self.monster = loaded_state.get("monster", "")
                self.roomDescribe = loaded_state.get("description", "")

                print("Game loaded successfully!")
        except FileNotFoundError:
            print("No save file found. Starting a new game.")
        except Exception as e:
            print(f"An error occurred while loading the game: {e}")

    def open_new_terminal(self):
        if os.name == 'nt':  # Windows
            if self.script_name not in sys.argv:
                os.system(f'start cmd /k python {self.script_name}')
        elif os.name == 'posix':  # Linux, macOS
            if self.script_name not in sys.argv:
                os.system(f'xterm -e python {self.script_name} &')



    def user_input(self):
        print("What do you do?")
        self.input = input("> ").strip().lower()
        return self.input

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
    def check_room_event(self, room, moves_ago):
        # If for instance you're checking if a number is in the index -2 or further moves_ago needs to be 2.
        # Check the portion of the list before the last `moves_ago` items.

        cutoff = len(self.roomsEntered) - moves_ago
        if cutoff < 0:
            cutoff = 0  # Ensure no negative slicing.
        return room in self.roomsEntered[:cutoff]

    def proceed(self, room):
        # Record the player's entry into a new room
        self.currentRoom = room
        self.roomsEntered.append(room)
        # Game halfway indicator
        if len(self.roomsEntered) == 30:
            if self.currentRoom == "Entrance Hall" or self.currentRoom == "Game Room" or self.currentRoom == "Lounge" or self.currentRoom == "Lower Library" or self.currentRoom == "Dining Room" or self.currentRoom == "Kitchen" or self.currentRoom == "Supply Closet" or self.currentRoom == "Guest Bathrooms" or self.currentRoom == "Upper Landing" or self.currentRoom == "Trophy Room":
                print("***  A grandfather clock chime rings throughout the house. It must be 12:00! Where is Elias?  ***")
            elif "Elias Found" not in self.interactions:
                print("***  Its getting late, you should find Elias soon.  ***")
            else:
                print()
        # Update the room entry count
        if room not in self.roomEntryCounts:
            self.roomEntryCounts[room] = 0
        self.roomEntryCounts[room] += 1
        # Room descriptor
        print(self.roomDescribe)

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def add_to_interactions(self, interaction):
        self.interactions.append(interaction)

    def get_current_room(self):
        return self.currentRoom

    def get_rooms_entered(self):
        return self.roomsEntered
#Cody Lincoln
    def monster(self):
        if len(G.roomsEntered) >= 70:
            self.monster = "Chimera"
            print("")
        else:
            self.monster = "Silas"
            print("")
        return self.monster

G = Gameloop()  # Create an instance of the Gameloop class
G.open_new_terminal()  # Call the method to open a new terminal

class ChaseGame:
    def __init__(self, start_time): #defining the base for variables
        self.time_left = start_time
        self.is_caught = False
        self.timer_thread = None
        self.lock = threading.Lock()
        self.turns_taken = 0 #based number for turns
        self.monster = ()


    def add_time(self, seconds):
        self.time_left += seconds
        print(f"{seconds} seconds added!")

    def subtract_time(self, seconds):
        self.time_left -= seconds
        if self.time_left < 0:
            self.time_left = 0
        print(f"{seconds} seconds subtracted!")

    def show_time(self):
        mins, secs = divmod(self.time_left, 60)
        print(f"Time left: {mins:02}:{secs:02}", end="\r")

    def start_chase(self):
        while self.time_left > 0:
            self.show_time()
            time.sleep(1)
            self.time_left -= 1
            if self.time_left == 0:
                self.is_caught = True
                break


        if self.is_caught:
            print("You're thrown to the ground", G.monster, "hovers over you and raises their hand, everything goes black")
        else:
            if G.monster=="Chimera":
                print("You run out the front and down the path from which you came,\n"
                      "from the woods you turn to see the front doors totally gone left with a singular wall and a familiar face from the 2nd story window.\n"
                      "you stop catching a breath then continue cautiously down the path")
            else:
                print("You run out the front and down the path from which you came,\n"
                        "from the woods you turn to see the front doors totally gone left with a singular wall and a familiar face from the 2nd story window.\n"
                        "You turn to your friend and smile he returns the smile with a look of relief and you both continue down the path together not ready to let each other go.")

    def start_timer_thread(self):
        self.timer_thread = threading.Thread(target=self.start_chase)
        self.timer_thread.daemon = True
        self.timer_thread.start()

def timed_game_decisions(timer, stage=1):
    actions_stage_1 = {
        "1": {"action": "Scalpel", "time_change": 5,"response": "\nIt manages to scrape your foe not doing much for you"},
        "2": {"action": "Chair", "time_change": 15,"response": "\nIt hits them straight in the head leaving them temporarily dazed"},
        "3": {"action": "Blanket", "time_change": 10,"response": "\nIt covers their vision temporarily and they aggressively rip it off"},
    }

    actions_stage_2 = {
        "1": {"action": "Move shelf", "time_change": 20,"response": "\nYou shove the shelf in the way hoping to slow them down"},
        "2": {"action": "Speed up", "time_change": 5,"response": "\nThe adrenaline pumping through you accelerates you forward"},
        "3": {"action": "Throw tarp", "time_change": 30,"response": "\nYou grab a worn tarp and throw it up hoping to slow them down."},
    }

    actions_stage_3 = {
        "1": {"action": "Left", "time_change": 0,"response": "\nYou run down the hall to the left"},
        "2": {"action": "Right", "time_change": -5,"response": "\nYou pass by the creature from earlier who reaches out and attempts to grab you.\nDodging him leaving you with nothing but a scratch you continue to spring down the hall"},
    }

    actions_stage_4 = {
        "1": {"action": "Speed up", "time_change": 5,"response": "\nThe adrenaline pumping through you accelerates you forward"},
        "2": {"action": "Look ahead", "time_change": 0,"response": "\nYou bring yourself to a light jog and take a minute to look ahead"},
        "3": {"action": "Grab something", "time_change": 0,"response": "\nYou spot a tool not to far ahead and grab it"},
    }

    actions_stage_5 = {
        "1": {"action": "Run out", "time_change": 5,"response": "\nYou bolt out from the closet slamming the door behind you"},
        "2": {"action": "board off the basement", "time_change": 10,"response": "\nYou grab a spare piece of wood that would be used for a shelf and place it within the handle boarding off the basement and run out"},
        "3": {"action": "Grab supplies", "time_change": -5,"response": "\nYou spot some cleaning supplies and grab a mop. Is this actually useful?"},
    }

    actions_stage_6 = {
        "1": {"action": "Run out", "time_change": 5,"response": "\nYour anxiety makes itself known and compels you to leave"},
        "2": {"action": "Grab knife", "time_change": 10,"response": "\nYou sprint to the knife block and grab the largest knife then run out of the kitchen"},
        "3": {"action": "Attempt to shatter a window", "time_change": -5,"response": "\nYou pound your fist into the window hoping and pleading with the window that it breaks, it doesn’t"},
    }

    actions_stage_7 = {
        "1": {"action": "Throw chair", "time_change": 10,"response": "\nYou chuck the chair and hit them leaving them stunned and sprint out"},
        "2": {"action": "Push the table", "time_change": -5,"response": "\nYou attempt to ram the table into them, it being too heavy it does nothing for you and you sprint out in fear."},
        "3": {"action": "Sprint out", "time_change": 0,"response": "\nYou bolt out of the dining room not thinking twice"},
        "4": {"action": "Throw something", "time_change": 15,"response": "\nYou throw the knife/tool striking them right in the head and run ou"}
    }

    actions_stage_8 = {
        "1": {"action": "Run towards Game Room", "time_change": 0,"response": "\nRunning towards the game room the game room is no longer the game room but rather another long hall."},
        "2": {"action": "Attempt to run up the stairs", "time_change": -5,"response": "\nRunning towards the stairs you get knocked of your feet and into a long hall"},
        "3": {"action": "Bash the window", "time_change": -5,"response": "\nYou grab something and attempt to bash the window,it's no use."},
    }

    actions_stage_9 = {
        "1": {"action": "Speed up", "time_change": 5,"response": "\nThe adrenaline pumping through you accelerates you forward"},
        "2": {"action": "Turn around", "time_change": 20,"response": "\nYou see a figure running towards you at full speed fills you with adrenaline"},
        "3": {"action": "Throw something", "time_change": 0,"response": "\nYou choose to discard something random in your inventory, it misses"},
    }

    actions_stage_10 = {
        "1": {"action": "Speed up", "time_change": 5,"response": "\nThe adrenaline pumping through you accelerates you forward"},
        "2": {"action": "Knock over pallet", "time_change": 15,"response": "\nYou throw the pallet to the ground behind you slowing them down"},
        "3": {"action": "Keep running", "time_change": 10,"response": "\nYou keep running forward your longing for a escape fueling you"},
    }


    stage_texts = {
        1: "As you back away and reach closer and closer to a dead end your options become limited.\n As you look around the room there's various objects you can throw",
        2: "You sprint past them running down the long hall from which you came.\n You look ahead and see a couple options ahead of you.",
        3: "Sprinting down the hallway it starts moving back and forth and suddenly the path before you isn't so straight forward",
        4: "Finally reaching a clear space the hallway starts to straighten itself back out.",
        5: "Continuing forward you egress from the basement and end up in the supply closet.\n Hearing thudding and banging coming closer and closer.",
        6: "You stand within the kitchen taking in what's around you",
        7: "Standing on the far end of the dining room you look ahead and see a large figure within the entrance of the kitchen\n breathing furiously and heavily",
        8: "You stand in the main entry hall with the front door being blocked,\n you look upstairs and see them deformed with the creature standing at the top of them with a smile on his face",
        9: "The long familiar hallway only seems to be getting longer and longer as you hear aggressive huffing and thumping behind you only getting closer and closer.",
        10: "You think you can see the end of the hallway\n you also see some sort of pallet up ahead.",
    }

    stages = {
        1: actions_stage_1,
        2: actions_stage_2,
        3: actions_stage_3,
        4: actions_stage_4,
        5: actions_stage_5,
        6: actions_stage_6,
        7: actions_stage_7,
        8: actions_stage_8,
        9: actions_stage_9,
        10: actions_stage_10
    }

    while timer.time_left > 0:
        # Display narrative text between stages
        print("\n" + stage_texts.get(stage, ""))

        print("\n What do you do?:")
        actions = stages[stage]

        # Display the available actions for the current stage
        for key, value in actions.items():
            print(f"{key}. {value['action']}")

        choice = input("Enter your choice (1-4): ").strip()

        if choice in actions:
            print(f"\nYou chose to: {actions[choice]['action']}")
            time_change = actions[choice]["time_change"]
            if time_change > 0:
                timer.add_time(time_change)
            else:
                timer.subtract_time(abs(time_change))

            timer.turns_taken=+1
        else:
            print("\nInvalid choice, try again.")


        # Show updated time after decision
        timer.show_time()

        # Move to the next stage after a valid decision
        if stage == 1:
            stage = 2
        elif stage == 2:
            stage = 3
        elif stage == 3:
            stage = 4
        elif stage == 4:
            stage = 5
        elif stage == 5:
            stage = 6
        elif stage == 6:
            stage = 7
        elif stage == 7:
            stage = 8   #one ending here
        elif stage == 8:
            stage = 9
        elif stage == 9:
            stage = 10  #one ending here
        else:
            break

    timer.start_chase()

#if __name__ == "__main__":
    #initial_time = 15
    #timer = ChaseGame(initial_time)
    #timer.start_timer_thread()
    #game_decisions(timer)


#Tell the player the commands at the beginning of the game
class Commands:
    def __init__(self):
        self.commands = ""

    def tell_commands(self):
        self.commands = "To = Allows you to move to the room or direction stated.\nExamine = Look at an object stated.\nInteract = Pick up or touch an object\nUse = use an object you have interacted with to collect\nType 'quit' at any time to save and exit the game.\n\n\n"
        print(self.commands)
        print("Inventory =", G.inventory)

C = Commands()

#Benjamin Hall

#Greet at beginning of game
class Startup:
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

S = Startup()
def dialog_options(options):
    print("\nChoose an option:")
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")

    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(options):
                return choice - 1
            else:
                print("Invalid choice. Please choose a valid option.")
        except ValueError:
            print("Please enter a number corresponding to your choice.")


# Function for the servant dialog scene
def servant_dialog():
    print("M-My name does not matter. My daughter is Jane. She is trapped. They won't let her go. I-I have to save her.")
    print("Stay here, help him. Cater them. So she lives.")

    options = [
        'What do you mean “them?”',
        "What do you mean your daughter is trapped?",
        "Why did everybody else leave?"
    ]
    choice = dialog_options(options)

    if choice == 0:
        print("Them. Them! Who are them? Who are t-they!” The woman’s voice rises… \n “He, HE IS EVIL. The other, the other… He is kinder, but yet, no. \nI will show no sympathy. They took her from me. \n Elias. And his godforsaken father.")
    elif choice == 1:
        print('"They caged her. In the basement. I-I-I hear her cry at night. They… They torture her. I hear her beg them through the floor, from the kitchen. S-she calls my name”\n The woman sheds a tear, and begins to mock in a whimper what you assume is Jane’s voice,\n “Mommy, mommy please… You said they were nice… You said Silas was kind, that Elias was kind. Mommy! Help me…”')
    elif choice == 2:
        print('“They, they were afraid. Rightfully so. Elias, was changing… Meaner, more brash. H-he was not the man who I knew before.” She sucks in a breath, as if greedy for air, as if to say more, but she does not.')



#Starting the Game
C.tell_commands()
print("PRESS ENTER TO PROCEED OR TYPE LOAD TO LOAD YOUR PREVIOUS GAME")
load_input = input().strip().lower()
if "load" in load_input:
    if __name__ == "__main__":
        G.load_game()
        print("\nCurrent Room:", G.currentRoom, "\nRooms Entered:", G.roomsEntered, "\n")
        print(G.roomDescribe)
else:
    G.clear_screen()
    S.ask_name()
    G.clear_screen()
    S.greet()
    input()
    G.clear_screen()
    C.tell_commands()
    G.roomDescribe = "You stand before an entrance hall of cobble and wood.\nUnlike the rest of the house, the floors here are stone, with towering pillars of marble sprouting out.\nThe cobble walls crumble around you, spider webs seem to devour every dark corner of the room, and chunks of stone litter the ground.\nA single red carpet runs below your feet and up a grandiose spruce staircase, leading left and right.\nIts red fabric runs like fine wine flowing up to the landing.\n\n\nThe room is illuminated only by dim, flickering lanterns that hang from the ceiling. A wooden balcony overlooks the room you are in.\nYou clutch the note in your hand, then pocket it.\nThe room is eerily quiet, apart from the sound of your own short breathing and the creaking of the manor.\n\n\nTwo doors line the right wall, to the game room and lounge, and one sits on the left wall leading to a dining room.\n"
    G.proceed("Entrance Hall")

while True:
#Entrance Hall


    while G.currentRoom == "Entrance Hall":
        G.user_input()
        if "to landing" in G.input or "to stairs" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = "Up the stairs there is a small alcove contain some trophies that branches into more rooms. \nFurther up is the balcony which overlooks the entrance hall. \n\n\nThere are doors to the master bedroom, the study, and a long hallway.\nOtherwise, the balcony is mostly bare. \n"
            G.proceed("Upper Landing")
        elif "to game" in G.input or "to game room" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = "You enter the mansion's game room, immediately taking in the sharp aroma of alcohol and pool chalk. \nThe small square room has an open archway in the back that leads into a lounge. \n\n\nIn the front of the room lies a couch, a tv sitting on a stand across from it, buzzing static. \nA large red-felted pool table behind the couch displays a losing game of solids against stripes. \nA broken cue is discarded upon the table, snapped in half. \nA dartboard hangs from a wall behind the pool table, with some darts still scattered upon the floor and pinned into the wall.\n"
            G.proceed("Game Room")
        elif "to lounge" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = "You enter the lounge, the faint smell of firewood pricking your nose. \nScattered across the room, but all facing a central fireplace, are a few armchairs, a coffee table, and a large painting of what looks like Elias, but older. \n\n\nA door leads into the library and an archway opens up into the game room.\n"
            G.proceed("Lounge")
        elif "to dining" in G.input or "to dining room" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = "You enter the dining room. \nRich wooden floors and rugged stone walls line the room. \nA long, dark oak table stretches out in the center of the room, surrounded by carved wooden chairs. \nCandles hang along the wall and on the table, emanating an eerie glow. \n\n\nFood lines the table, the smell of meat and wine fills the air. \nAt the head of the table, sits a finished meal of steak and wine, and next to it, a half-eaten messy abomination of what you think used to be chicken, torn to shreds.\n"
            G.proceed("Dining Room")
        elif "examine pillar" in G.input:
            print("Large and crumbling ornate pillars supports the manor, carved with intricate patterns and words in another language.\n")
        elif "examine stone" in G.input:
            print("The large stones that litter the ground appear to have fallen from a large faded mural on the ceiling. \nYou can only make out the remains of a large star. \nSmaller stones sit akin to the large.\n")
        elif "examine door" in G.input:
            print("The mahogany door you came through towers over you. \nYou try to turn the large silver handle, but it doesn't budge. \nYou will need a key.\n")
        elif "examine carpet" in G.input:
            print("The carpet is old and worn, moreso in the areas that intersect the paths to the left and right doors. \nIt strikes you as odd, for Elias has always been a tidy man.\n")
        elif "interact stone" in G.input:
            if "Stone" not in G.inventory:
                print("You pick up a stone off the ground.\n")
                G.add_to_inventory("Stone")
            elif "Stone" in G.inventory:
                print("You already picked up the stone.\n")
        elif "quit" in G.input:
            G.save_game()
            break
        else:
            print("Invalid input, try something like 'to game room', 'examine stone', or 'interact door'.\n")

    while G.currentRoom == "Game Room":
        G.user_input()
        if "back" in G.input or "to entrance" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = "You go back into the entrance hall; the floors here are stone, with towering pillars of marble sprouting out.\nThe cobble walls crumble around you, spider webs seem to devour every dark corner of the room, and chunks of stone litter the ground.\nA single red carpet runs below your feet and up a grandiose spruce staircase, leading left and right.\nIts red fabric runs like fine wine flowing up to the landing.\n\n\nThe room is illuminated only by dim, flickering lanterns that hang from the ceiling. A wooden balcony overlooks the room you are in.\nThe room is eerily quiet, apart from the sound of your own short breathing and the creaking of the manor.\n\n\nTwo doors line the right wall, to the game room and lounge, and one sits on the left wall leading to a dining room.\n"
            G.proceed("Entrance Hall")
        elif "to lounge" in G.input or "to archway" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = "You enter the lounge, the faint smell of firewood pricking your nose. \nScattered across the room, but all facing a central fireplace, are a few armchairs, a coffee table, and a large painting of what looks like Elias, but older. \n\n\nA door leads into the library and an archway opens up into the game room behind you.\n"
            G.proceed("Lounge")
        elif "examine pool" in G.input or "examine table" in G.input:
            print("You see a game of pool, with stripes having an apparent winning position. You notice the 8 Ball is missing, and find it in one of the pockets. You look towards the broken cue. It seems like the solids player was having a bad day.")
        elif "interact cue" in G.input:
            if "Cue" not in G.inventory:
                print("You grab one of the broken halves of the pool cue.")
                G.add_to_inventory("Cue")
            elif "Cue" in G.inventory:
                print("You already picked up the cue.")
        elif "examine couch" in G.input:
            print("The couch is a deep maroon leather stitched with ivory. \nYou sit upon it, and surprisingly, you sink into it as if it were plush. \nYou feel like you tune on a good show and stay here for hours. \n")
        elif "examine tv" in G.input:
            print("A fancy black old television upon an ivory stand. \nIt displays a buzzing static.\n")
        elif "examine dart" in G.input or "examine board" in G.input:
            print("A large round dart board, a game of blue versus yellow. \nBlue has a dart in the green circle surrounding the bullseye, with one more in the red 18 section of the red and green inner ring, another in the white 15 inner ring section, and a final dart in the outer black 13 section. \nYellow has two darts immersed into the wall, and one bullseye.\n")
        elif "interact couch" in G.input:
            print("You rifle through the couch, and find a leaflet on the rules for darts, and a tv remote.")
        elif "interact remote" in G.input:
            if "Game Room Remote" not in G.interactions:
                print("You click the remote, and Frankenstein begins playing. \nYou watch as Victor shocks his creation, shouting his iconic line, 'It's Alive!'\n")
                G.add_to_interactions("Game Room Remote")
            elif "Game Room Remote" in G.interactions:
                print("You click the tv remote, turning it back to static.")
        elif "interact leaflet" in G.input or "interact rules" in G.input:
            print("You open the leaflet, it reads:\nPlayers should stand 7ft 9in from the dart board, with both feet on the ground. \nPlayers should hold the dart in their dominant hand, and throw it straight without too much force. \nThe dart board has 20 numbered sections, with the bullseye in the center. The bullseye's outer ring is worth 25 points, and the inner circle is worth 50 points. \nThe black and white outer and inner rings are worth the point value displayed, and the outer red and green ring is worth double points, while the inner is worth triple. \nPlayers take turns throwing 3 darts per turn. \nYou start with 501 points, and the goal is to reduce your score to zero, but the last dart thrown must land in a double or the bullseye.\n")
        elif "quit" in G.input:
            G.save_game()
            break
        else:
            print("Invalid input, try something like 'to lounge', 'examine pool table', or 'interact cue'.\n")

    while G.currentRoom == "Lounge":
        G.user_input()
        if "back" in G.input or "to entrance" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = "You go back into the entrance hall, "
            G.proceed("Entrance Hall")
        elif "to library" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = "You enter the Library, and the scent of old wood and paper fills the air. \nTowering bookshelves line the walls, and a giant balcony looks over you. \n\n\nYou notice main shelving units on the left, right, and center. \nA single table sits in solitude next to the center bookshelves. \n\n\nThe door behind you leads to the lounge, and another in the back leads to the guest bathrooms.\n"
            G.proceed("Lower Library")
        elif "to game room" in G.input or "to archway" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = ""
            G.proceed("Game Room")
        elif "examine fireplace" in G.input:
            if "Hedda Gabler Lever" in G.interactions:
                print("The fireplace is a classic gray brick, with a metal holder holding ashen wood, and a fire prod stuck inside. \n\n\nYou see behind the fireplace is an old lockbox with a combination lock. \nThere are colored tiles, Green, Black, Red, and White, with sliders to input numbers.\n")
                print("You may input any four numbers ranging from 1 to 99 in each slot with a space between each number. \nWhat would you like to input?\n")
                lockbox_input = input("> ")
                if "25 13 54 15" in lockbox_input:
                    print("You hear a click, and lift the lid of the box. Inside you find a small bronze key, and pocket it.\n")
                    G.add_to_inventory("Bronze Key")
                elif "25 13 54 15" not in lockbox_input:
                    print("The lockbox does not open.\n")
            elif "Hedda Gabler Lever" not in G.interactions:
                print("The fireplace is a classic gray brick, with a metal holder holding ashen wood, and a fire prod stuck inside. \nOddly, you see no vent to channel the smoke, and the fireplace seems more shallow than you would expect.\n")
        elif "examine painting" in G.input:
            print("As you walk closer, you notice the painting isn't actually of Elias, but rather of his Father, Silas. \nAlthough sitting regally in a fine armchair, he seems roughened up. Middle aged with a stubble covered face and crooked nose; he looks weary, this was probably painted close to his death.\n")
        elif "interact painting" in G.input:
            if "Note: '6'" not in G.inventory:
                print("You lift up the painting, and a note falls to the ground. Picking it up to read, it simply says '6'.")
                G.add_to_inventory("Note: '6'")
            elif "Note: '6'" in G.inventory:
                print("You already found a note here that read: '6'\n")
        elif "interact prod" in G.input:
            print("As you pick up the fire prod, the weak metal turns to ash in your hands.\n")
        elif "examine armchair" in G.input:
            if "Shopping list: 'Botany Book, Bucket, Painting, and Boar Head Mantle'" not in G.inventory:
                print("You scavenge through the armchairs, only finding some loose change and an old shopping list that reads:\nBotany Book, Bucket, Painting, and Boar Head Mantle. \n")
                G.add_to_inventory("Shopping list: 'Botany Book, Bucket, Painting, and Boar Head Mantle'")
            elif "Shopping list: 'Botany Book, Bucket, Painting, and Boar Head Mantle'" in G.inventory:
                print("This is where you found the shopping list.\n")
        elif "examine table" in G.input:
            print("Scattered atop the coffee table are a variety of pages, appearing to be torn from various books. \nThe table also seems to be burnt in areas, with holes pokes through some of the pages and through the table. \nThe legible pages include a ripped up children's book on learning to read, a page from Elias’s favorite book: 'Hedda Gabler', and an excerpt from the poem “On Being Human.” \nThe except reads: Far richer they! I know the senses' witchery\nGuards us like air, from heavens too big to see;\nImminent death to man that barb'd sublimity\nAnd dazzling edge of beauty unsheathed would be.\nYet here, within this tiny, charmed interior,\nThis parlour of the brain, their Maker shares\nWith living men some secrets in a privacy\nForever ours, not theirs.\n")
        elif "quit" in G.input:
            G.save_game()
            break
        else:
            print("Invalid input, try ")

    while G.currentRoom == "Lower Library":
        G.user_input()
        if "back" in G.input or "to lounge" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = "You go back into the lounge, the faint smell of firewood pricking your nose. \nScattered across the room, but all facing a central fireplace, are a few armchairs, a coffee table, and a large painting of what looks like Elias, but older. \n\n\nThe door behind you leads into the library and an archway opens up into the game room.\n"
            G.proceed("Lounge")
        elif "to bathroom" in G.input or "to guest" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = "You enter the Guest Bathrooms, what would be a pristine room, if not for the giant blood stains all over the floor, the mirror, the walls, everywhere. \nEven the toilets in the stall. \nIt is horrifying, appalling. \nYou lurch forward, but stop yourself before hurling up your dinner.\n\n\nThe door behind you goes back into the library.\n"
            G.proceed("Guest Bathrooms")
        elif "examine balcony" in G.input or "examine above" in G.input or "examine upper" in G.input:
            if "Balcony Man" not in G.interactions:
                print("You hear a faint gurgle and look up towards the balcony, noticing what looks like a man peering over at you. \nAll you see is pale white skin before he disappears with a blur.\n")
                G.add_to_interactions("Balcony Man")
            elif "Balcony Man" in G.interactions:
                print("The man you once saw on the floor above you is gone.")
        elif "examine table" in G.input:
            print("Atop the table you see a book of mythical creatures, a book about genetic limits, opened to a page about how man reacts to various torture, and a note written in a dirty scrawl not typical of Elias that reads: \n'I have discovered something new, something grand, something that extends the limits of man beyond death, beyond age, beyond mortal comprehension... Beyond life.'\n")
        elif "examine left" in G.input:
            print("Walking over to the left bookshelves, you see books scattered across the floor in what seems to be the remnants of a fight.")
        elif "examine right" in G.input:
            print("Along the right shelves, you notice a couple of classic literature books poking out from the book rack:\n'Fall of the House of Usher' and 'Hedda Gabler.'\n")
            G.add_to_interactions("Bookshelf")
        elif "examine center" in G.input:
            print("Along the center shelves, you take note of a couple books that seem more used than the others, titled:\n'Basics of Mycology', 'Occult: Into the Unknown', and 'Botany Knowledge for Beginners'.\n")
            G.add_to_interactions("Bookshelf")
        elif "interact hedda gabler" in G.input:
            if "Hedda Gabler Lever" not in G.interactions:
                print("As you attempt to grab the book, it doesn't pull out all the way. \nInstead, it shifts out slightly and you hear a click, and the slide of stone against stone coming from the lounge.\n")
                G.add_to_interactions("Hedda Gabler Lever")
            elif "Hedda Gabler Lever" in G.interactions:
                print("You already pulled this book lever.\n")
        elif "interact botany" in G.input or "interact beginners" in G.input:
            if "Note: '2'" not in G.inventory:
                print("As you open the book, a note falls out. \nIt reads: '2'\n")
                G.add_to_inventory("Note: '2'")
            elif "Note: '2'" in G.inventory:
                print("You already found a note here that read: '2'\n")
        elif "interact house" in G.input or "interact basics" in G.input or "interact mycology" in G.input or "interact occult" in G.input:
            print("You open the book and thumb through it. \nNothing appears out of the ordinary.\n")
        elif "quit" in G.input:
            G.save_game()
            break
        else:
            if "Bookshelf" in G.interactions:
                print("Invalid input, try 'interact botany knowledge for beginners' or 'examine table' or 'to guest bathrooms'")
            elif "Bookshelf" not in G.interactions:
                print("Invalid input, try 'examine table' or 'to guest bathrooms'")


    while G.currentRoom == "Dining Room":
        G.user_input()
        if "back" in G.input or "to entrance" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = ""
            G.proceed("Entrance Hall")
        elif "to kitchen" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = "You walk into the manors kitchen. \nGranite counter-tops and wooden shelves line the walls, holding copper pots, cast-iron skillets, and other rustic kitchenware. \nA large fridge is wedged between the counters and cabinets, and a small island floats in the middle of the room, wooden bar stools propped against it. \nStrange beakers and scientific devices line up atop the bar. \nBehind you is the door to the dining room and there is a door to a supply closet on the far wall."
            G.proceed("Kitchen")
        elif "examine table" in G.input:
            if "Apple" in G.inventory and "Knife" in G.inventory:
                print("There is nothing underneath the table.\n")
            elif "Apple" in G.inventory:
                print("Underneath the table, you find a steak knife has fallen to the floor.\n")
            elif "Knife" in G.inventory:
                print("Underneath the table lies an apple which glistens in the candlelight.\n")
            else:
                print("Underneath the table lies an apple which glistens in the candlelight.\nA steak knife has also fallen to the floor.\n")
        elif "interact apple" in G.input:
            if "Apple" not in G.inventory:
                print("You pick up the apple.\n")
                G.add_to_inventory("Apple")
            elif "Apple" in G.inventory:
                print("You already picked up the apple.\n")
        elif "interact knife" in G.input or "interact steak knife" in G.input:
            if "Knife" not in G.inventory:
                print("You grab the knife.\n")
                G.add_to_inventory("Knife")
            elif "Knife" in G.inventory:
                print("You already picked up the knife.\n")
        elif "interact candle" in G.input:
            if "Candle" not in G.inventory:
                print("You pick up a candle, holding it by the brass chamberstick in your left hand.\n")
                G.add_to_inventory("Candle")
            elif "Candle" in G.inventory:
                print("You already picked up a candle.\n")
        elif "quit" in G.input:
            G.save_game()
            break
        else:
            print("Invalid input, try ")

    while G.currentRoom == "Kitchen":
        G.user_input()
        if "back" in G.input or "to dining" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = ""
            G.proceed("Dining Room")
        elif "to supply" in G.input or "to closet" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = ""
            G.proceed("Supply Closet")
        elif "examine bar" in G.input:
            print("Along the bar, next to some strange scientific tools, a few sealed beakers lie with strange labels like 'thymidine', and 'ethidium bromide'.\n")
        elif "examine counter" in G.input or "examine cabinet" in G.input or "examine counter-top" in G.input:
            print("Inside the cabinets and atop the counters, among the standard silverware and cutlery. \nYou also notice a small blood stain, and bloody hand-prints gripping the counter beside it.")
            if "Painkillers" not in G.inventory:
                print("You find a small bottle of painkillers.\n")
            else:
                print("\n")
        elif "examine fridge" in G.input:
            print("You open the rustic fridge door, and inside lies an array of elegant food. \nSteaks, caviar, truffles, and more. \nAmong these sit some odd foods, what look like strange meats with leathery skins or cuts of beef with sharp, mangy black fur still attached. \nAll of this accompanied by the most foul smell imaginable, like sulfur and rotting fungus.\n")
        elif "interact beaker" in G.input:
            print("It would be wiser not to touch these...")
        elif "interact painkiller" in G.input or "interact bottle" in G.input:
            if "Painkillers" not in G.inventory:
                print("You pick up the bottle of painkillers.\n")
                G.add_to_inventory("Painkillers")
        elif "quit" in G.input:
            G.save_game()
            break
        else:
            print("Invalid input, try ")

    while G.currentRoom == "Upper Landing":
        G.user_input()
        if "back" in G.input or "to entrance" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = "You go back down into the entrance hall; the floors here are stone, with towering pillars of marble sprouting out.\nThe cobble walls crumble around you, spider webs seem to devour every dark corner of the room, and chunks of stone litter the ground.\nA single red carpet runs below your feet and up a grandiose spruce staircase, leading left and right.\nIts red fabric runs like fine wine flowing up to the landing.\n\n\nThe room is illuminated only by dim, flickering lanterns that hang from the ceiling. A wooden balcony overlooks the room you are in.\nThe room is eerily quiet, apart from the sound of your own short breathing and the creaking of the manor.\n\n\nTwo doors line the right wall, to the game room and lounge, and one sits on the left wall leading to a dining room.\n"
            G.proceed("Entrance Hall")
        elif "to alcove" in G.input or "to small" in G.input or "to trophy" in G.input:
            G.clear_screen()
            C.tell_commands()
            if G.roomEntryCounts['Trophy Room'] == 0:
                G.roomDescribe = "You turn into the small hallway that parts from the stairs to find the trophy room. \nA few hunting trophies hang from high on the walls including: a lion, a deer, a wolf, and a boar.\nDoors leading to the servant's quarters and upper library are also found in the hallway.\n\n\nA circular red carpet sits on the floor, and shelves full of gold and silver metal line the walls. You take note of a few awards: The Genetic Research Excellence Award for Elias Finch, The Genomic Innovation Award for Elias Finch, The Genetic Education and Outreach Award for Elias & Silas Finch, The Mendel Award for Silas Finch, and the Stem Cell Genetics Award for Silas Finch.\n"
            elif G.roomEntryCounts['Trophy Room'] == 1:
                G.roomDescribe = "You turn into the small hallway that parts from the stairs to find the trophy room. \nA few hunting trophies hang from high on the walls including: a lion, a deer, a wolf, and a boar.\nDoors leading to the servant's quarters and upper library are also found in the hallway.\n\n\nA square red carpet lays down exhausted on the floor, shelves full of silver and gold metal line the walls. \nYou take note of a few awards: The Jean and Fabric Research Excellence Award for Elias Finch, The Genomal Innovation Award for Elias Finch, The Genetic Outreach Award for Silas Finch, The Mendel Award for Silas Finch, and the Mycology Award for Silas Finch. \nLittle mushrooms grow out of the Mycology award. \nYou feel a little lightheaded.\n"
            elif G.roomEntryCounts['Trophy Room'] >= 2:
                G.roomDescribe = "You turn into the small hallway that parts from the stairs to find the trophy room. \nA few hunting trophies hang from high on the walls including: a lion, a deer, a wolf, and a boar.\nDoors leading to the servant's quarters and upper library are also found in the hallway.\n\n\nA circular red mushroom cap grows out of the floor like a carpet, shelves full of gold, silver, and purple metal line the walls. \nYou take note of a few awards: The Deoxyribonucleic acid Award for Elias Hemlock, The Genome Intantiator Award for Elias Finch, The Genetic Mycology Award for Elias & Silas Finch, The Limb Splicer Award for Silas Finch, and the Medieval Torture Award for Silas Finch. \nMushrooms grow out of the trophies and the walls. \nYou feel lightheaded, a purple mist clouds your vision.\n"
            G.proceed("Trophy Room")
        elif "to master" in G.input or "to bedroom" in G.input:
            if "Bronze Key" in G.inventory:
                G.clear_screen()
                C.tell_commands()
                G.roomDescribe = ""
                G.proceed("Master Bedroom")
            elif "Bronze Key" not in G.inventory:
                print("You will need a key to enter this room.\n")
        elif "to long" in G.input or "to hallway" in G.input:
            if "Silver Key" in G.inventory:
                G.clear_screen()
                C.tell_commands()
                G.roomDescribe = "You step into a dimly lit hallway. \nThe air is thick with dust, and you can smell the faint scent of mildew. \nCracked stone walls are lined with faded tapestries, their patterns obscured by cobwebs. \nThe wooden floor creaks underfoot, each step echoing faintly. \nA flickering lantern at the far end casts long, wavering shadows, and three doorways line the wall, numbered 1, 2, and 3. \nA small thin and tall table sits on the adjacent wall. \nAtop it, a book, and a painting of Silas and somebody else, with two candles dimly flickering next to it.\n\n\nThe door behind you leads back into the upper landing.\n"
                G.proceed("Long Hallway")
            elif "Bronze Key" in G.inventory:
                print("You don't have the right key to enter this room.\n")
            else:
                print("You will need a key to enter this room.")
        elif "quit" in G.input:
            G.save_game()
            break
        else:
            print("Invalid input, try 'to hallway' or 'to master'.\n")

    while G.currentRoom == "Trophy Room":
        G.user_input()
        if "to servant's" in G.input or "to quarters" in G.input:
            if "Bronze Key" in G.inventory:
                G.clear_screen()
                C.tell_commands()
                if "Servant Question" not in G.interactions:
                    G.roomDescribe = "You walk into the servants quarters, the lights here are dim and flickering. \nBunk beds line one wall, dressers the other. You can hear the sound of running water from the bathrooms.\nThe door to the trophy room is behind you, and you may examine the bathroom.\n"
                    G.proceed("Servant's Quarters")
                elif "Servant Question" in G.interactions:
                    G.roomDescribe = ""
                    G.proceed("Servant's Quarters")
            elif "Bronze Key" not in G.inventory:
                print("You will need a key to enter this room.\n")
        elif "back" in G.input or "to landing" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = ""
            G.proceed("Upper Landing")
        elif "to library" in G.input or "to upper" in G.input:
            if "Bronze Key" in G.inventory:
                G.clear_screen()
                C.tell_commands()
                G.roomDescribe = ""
                G.proceed("Upper Library")
            elif "Bronze Key" not in G.inventory:
                print("You will need a key to enter this room.\n")
        elif "examine award" in G.input or "examine shelf" in G.input or "examine shelves" in G.input:
            print("Each shelf is filled to the brim with various trophies and awards attributed to Elias and his father.\n")
        elif "interact boar" in G.input:
            if "Note: '4'" not in G.inventory:
                print("You lift the boar's head. A note with the letter '4' on it falls out from behind it.\n")
                G.add_to_inventory("Note: '4'")
            elif "Note: '4'" in G.inventory:
                print("You already found a note behind the boar's head. \nIt read: '4'\n")
        elif "interact lion" in G.input or "interact deer" in G.input or "interact wolf" in G.input:
            print("There is nothing odd about this hunting trophy.\n")
        elif "quit" in G.input:
            G.save_game()
            break
        else:
            print("Invalid input, try 'to upper library' or 'interact deer head'.\n")

    while G.currentRoom == "Servant's Quarters":
        G.user_input()
        if "back" in G.input or "to trophy" in G.input:
            G.clear_screen()
            C.tell_commands()
            if G.roomEntryCounts['Trophy Room'] == 0:
                G.roomDescribe = "You turn and go back into the trophy room. \nA few hunting trophies hang from high on the walls including: a lion, a deer, a wolf, and a boar.\nDoors leading to the servant's quarters and upper library are also found in the hallway.\n\n\nA circular red carpet sits on the floor, and shelves full of gold and silver metal line the walls. You take note of a few awards: The Genetic Research Excellence Award for Elias Finch, The Genomic Innovation Award for Elias Finch, The Genetic Education and Outreach Award for Elias & Silas Finch, The Mendel Award for Silas Finch, and the Stem Cell Genetics Award for Silas Finch.\n"
            elif G.roomEntryCounts['Trophy Room'] == 1:
                G.roomDescribe = "You turn and go back into the trophy room. \nA few hunting trophies hang from high on the walls including: a lion, a deer, a wolf, and a boar.\nDoors leading to the servant's quarters and upper library are also found in the hallway.\n\n\nA square red carpet lays down exhausted on the floor, shelves full of silver and gold metal line the walls. \nYou take note of a few awards: The Jean and Fabric Research Excellence Award for Elias Finch, The Genomal Innovation Award for Elias Finch, The Genetic Outreach Award for Silas Finch, The Mendel Award for Silas Finch, and the Mycology Award for Silas Finch. \nLittle mushrooms grow out of the Mycology award. \nYou feel a little lightheaded.\n"
            elif G.roomEntryCounts['Trophy Room'] >= 2:
                G.roomDescribe = "You turn and go back into the trophy room. \nA few hunting trophies hang from high on the walls including: a lion, a deer, a wolf, and a boar.\nDoors leading to the servant's quarters and upper library are also found in the hallway.\n\n\nA circular red mushroom cap grows out of the floor like a carpet, shelves full of gold, silver, and purple metal line the walls. \nYou take note of a few awards: The Deoxyribonucleic acid Award for Elias Hemlock, The Genome Intantiator Award for Elias Finch, The Genetic Mycology Award for Elias & Silas Finch, The Limb Splicer Award for Silas Finch, and the Medieval Torture Award for Silas Finch. \nMushrooms grow out of the trophies and the walls. \nYou feel lightheaded, a purple mist clouds your vision.\n"
            G.proceed("Trophy Room")
        elif "examine bunk" in G.input or "examine bed" in G.input:
            if "Note: 'I will not die here. If you read this, Jane, I love you.'" not in G.inventory:
                print("The beds are neatly made and devoid of personal objects, apart from a note you find tucked under a pillow that reads: \n'I will not die here. If you read this, Jane, I love you.'\n")
                G.add_to_inventory("Note: 'I will not die here. If you read this, Jane, I love you.'")
            elif "Note: 'I will not die here. If you read this, Jane, I love you.'" in G.inventory:
                print("This is where you found the note that read: 'I will not die here. If you read this, Jane, I love you.'\n")
        elif "examine dresser" in G.input:
            if "Jane's Locket" not in G.inventory:
                print("The dressers are packed tight with servants' clothes and some jewelry. \nYou do find an old locket of what looks like a young child. Engraved 'Jane.'\n")
                G.add_to_inventory("Jane's Locket")
            elif "Jane's Locket" in G.inventory:
                print("The dressers are packed tight with servants' clothes and some jewelry. \n")
        elif "examine bathroom" in G.input:
            if "Servant Question" not in G.interactions:
                G.clear_screen()
                print("As you walk towards the bathroom, towards the running water, you realize you can hear what sounds almost like, weeping… \nYou cautiously approach the door, and begin to turn the handle. \nWhen it stops. \nYou freeze, and right as you open your mouth to speak, the door slams open. You stumble backwards, and a woman stands in front of you. \nShe wears a traditional maid’s garb, with a bandage haphazardly wrapped around her arm, blood leaking through. \nHer eyes are sunken and bloodshot from tears, and she stands meekly, shaking with fear.\n\n\nShe Speaks: 'J-J-Jane? No. Who are you? What are you doing here… how did you get here…'\n")
                print("PRESS ENTER TO PROCEED")
                input()
                G.clear_screen()
                print("You begin to ask what she means, but before you can say anything she cuts you off… \n'No. Nonononononono. You have to leave. Only we remain. Me and Jane. Only us. Everybody else left. \nWho are you? Tell me… Who are you!'\n")
                print("PRESS ENTER TO PROCEED")
                input()
                G.clear_screen()
                print("'I am {}, who are you? What is going on here?'\n".format(S.name))
                print("PRESS ENTER TO PROCEED")
                input()
                G.clear_screen()
                servant_dialog()
                print("\n")
                servant_dialog()
                print("PRESS ENTER TO PROCEED")
                input()
                G.clear_screen()
                G.add_to_interactions("Servant Question")
                print("The woman braces to answer another question. \nSuddenly, her face turns white, the color draining from her face. \nHer eyes roll back, and she begins to cough. She drops to the floor, and begins to gasp and wheeze. \nShe claws at the ground, then at her throat, as blood gurgles out. Her eyes, her mouth, her ears, you watch as blood begins to seep out like puss to a wound. \nYou stumble back, horrified, as she begins to convulse, and her body begins to wither and scrunch in front of you. \nYou turn tail and run out the door, sprinting towards the trophy room, and as you do so, you hear the snap of bones, the crunching and squelching of muscles, and a strange clicking. \nWhen you peek back into the room, the woman is gone. \nInstead, a single finger seems to grow out of the floor where she stood, three mushrooms surround it.\n")
                print("You feel sick… \nIt takes everything you have to resolve yourself… Maybe you were just seeing things… This is all a dream… It has to be… \nEither way, you must find Elias. \nHe must have an explanation for all of this, right?\n")
                print("PRESS ENTER TO PROCEED\n")
                input()
                G.clear_screen()
                C.tell_commands()
                if G.roomEntryCounts['Trophy Room'] == 0:
                    G.roomDescribe = "You've ended up back in the trophy room. \nA few hunting trophies hang from high on the walls including: a lion, a deer, a wolf, and a boar.\nDoors leading to the servant's quarters and upper library are also found in the hallway.\n\n\nA circular red carpet sits on the floor, and shelves full of gold and silver metal line the walls. You take note of a few awards: The Genetic Research Excellence Award for Elias Finch, The Genomic Innovation Award for Elias Finch, The Genetic Education and Outreach Award for Elias & Silas Finch, The Mendel Award for Silas Finch, and the Stem Cell Genetics Award for Silas Finch.\n"
                elif G.roomEntryCounts['Trophy Room'] == 1:
                    G.roomDescribe = "You've ended up back in the trophy room. \nA few hunting trophies hang from high on the walls including: a lion, a deer, a wolf, and a boar.\nDoors leading to the servant's quarters and upper library are also found in the hallway.\n\n\nA square red carpet lays down exhausted on the floor, shelves full of silver and gold metal line the walls. \nYou take note of a few awards: The Jean and Fabric Research Excellence Award for Elias Finch, The Genomal Innovation Award for Elias Finch, The Genetic Outreach Award for Silas Finch, The Mendel Award for Silas Finch, and the Mycology Award for Silas Finch. \nLittle mushrooms grow out of the Mycology award. \nYou feel a little lightheaded.\n"
                elif G.roomEntryCounts['Trophy Room'] >= 2:
                    G.roomDescribe = "You've ended up back in the trophy room. \nA few hunting trophies hang from high on the walls including: a lion, a deer, a wolf, and a boar.\nDoors leading to the servant's quarters and upper library are also found in the hallway.\n\n\nA circular red mushroom cap grows out of the floor like a carpet, shelves full of gold, silver, and purple metal line the walls. \nYou take note of a few awards: The Deoxyribonucleic acid Award for Elias Hemlock, The Genome Intantiator Award for Elias Finch, The Genetic Mycology Award for Elias & Silas Finch, The Limb Splicer Award for Silas Finch, and the Medieval Torture Award for Silas Finch. \nMushrooms grow out of the trophies and the walls. \nYou feel lightheaded, a purple mist clouds your vision.\n"
                G.proceed("Trophy Room")
            elif "Servant Question" in G.interactions:
                print("This is where that girl Jane's mother told you some valuable information. \nThat is, before she died in front of you.\n")
        elif "quit" in G.input:
            G.save_game()
            break
        else:
            print("Invalid input, try 'examine bathroom' or 'examine dresser'.\n")

    while G.currentRoom == "Upper Library":
        G.user_input()
        if "back" in G.input or "to trophy" in G.input:
            G.clear_screen()
            C.tell_commands()
            if G.roomEntryCounts['Trophy Room'] == 0:
                G.roomDescribe = "You turn and go back into the trophy room. \nA few hunting trophies hang from high on the walls including: a lion, a deer, a wolf, and a boar.\nDoors leading to the servant's quarters and upper library are also found in the hallway.\n\n\nA circular red carpet sits on the floor, and shelves full of gold and silver metal line the walls. You take note of a few awards: The Genetic Research Excellence Award for Elias Finch, The Genomic Innovation Award for Elias Finch, The Genetic Education and Outreach Award for Elias & Silas Finch, The Mendel Award for Silas Finch, and the Stem Cell Genetics Award for Silas Finch.\n"
            elif G.roomEntryCounts['Trophy Room'] == 1:
                G.roomDescribe = "You turn and go back into the trophy room. \nA few hunting trophies hang from high on the walls including: a lion, a deer, a wolf, and a boar.\nDoors leading to the servant's quarters and upper library are also found in the hallway.\n\n\nA square red carpet lays down exhausted on the floor, shelves full of silver and gold metal line the walls. \nYou take note of a few awards: The Jean and Fabric Research Excellence Award for Elias Finch, The Genomal Innovation Award for Elias Finch, The Genetic Outreach Award for Silas Finch, The Mendel Award for Silas Finch, and the Mycology Award for Silas Finch. \nLittle mushrooms grow out of the Mycology award. \nYou feel a little lightheaded.\n"
            elif G.roomEntryCounts['Trophy Room'] >= 2:
                G.roomDescribe = "You turn and go back into the trophy room. \nA few hunting trophies hang from high on the walls including: a lion, a deer, a wolf, and a boar.\nDoors leading to the servant's quarters and upper library are also found in the hallway.\n\n\nA circular red mushroom cap grows out of the floor like a carpet, shelves full of gold, silver, and purple metal line the walls. \nYou take note of a few awards: The Deoxyribonucleic acid Award for Elias Hemlock, The Genome Intantiator Award for Elias Finch, The Genetic Mycology Award for Elias & Silas Finch, The Limb Splicer Award for Silas Finch, and the Medieval Torture Award for Silas Finch. \nMushrooms grow out of the trophies and the walls. \nYou feel lightheaded, a purple mist clouds your vision.\n"
            G.proceed("Trophy Room")

    while G.currentRoom == "Long Hallway":
        if G.roomEntryCounts ['Long Hallway'] == 1:
            G.user_input()
            if "examine book" in G.input:
                print("The page reads: 'I see him now, the firstborn of my arrogance. What was meant to surpass death has birthed a godless mockery of life. The servant… I cannot even recall his name. He was so eager to assist, so willing to become. Now he is more shadow than man, his form broken, reshaped by my hubris. His arms, stretched and blackened, carve reality as though the walls themselves obey his will. His face... oh, God, his face… Crushed, leaking, alive in defiance of all reason.' - Dr. Finch\n")
            elif "examine painting" in G.input:
                print("This painting is very similar to the first one you saw, only, it shows two people now.\nThe other, a beautiful woman, must have been Silas' wife.\n")
            elif "to 1st room" in G.input:
                if G.roomEntryCounts ['Mystery Room'] == 0:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "You enter what seems to be a spare bedroom. \nIt is small and unadorned, its pale stone walls bare except for a single, crooked picture frame. \nA simple wardrobe leans against one wall, a twin bed rests against another, its blanket neatly folded but faded with age. \nThe wooden floor shows signs of wear, with scratches hinting at furniture once rearranged. A single window with thin, yellowed curtains lets in a sliver of pale moonlight. \nThe room seems to be filled with a pale yellow mist, what seem like particles of dust floating around the room.\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts ['Mystery Room'] == 1:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom is dim, with a heavy, oppressive atmosphere. \nThe walls are painted a dull, peeling green, and mushrooms pop out at odd angles, spewing a deep red gas when you get too close. \nThe bed, larger than the one in the other room, is covered in a faded quilt, its edges worn from years of use, and its top covered in a thin layer of red mold. \nThe wooden floor creaks underfoot, and the only light comes from a small, dusty lamp on a bedside table. \nA single, cracked window looks out into the night, the faintest moonlight spilling in. \nSomething is very wrong...\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts ['Mystery Room'] == 2:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom feels alive, pulsing with an eerie, unnatural energy. \nFungal growths carpet the floors and climb the walls, their spongy surfaces slick with moisture. \nPatches of bioluminescent mushrooms emit a faint, sickly green glow, casting shifting shadows across the room. \nHemlock plants grow from the cracks in the floorboards, and invade a nearby dresser. \nTheir delicate leaves brush against your shoes as you walk. \nItems inexplicably float in the air, emerging from an open chest at the end of a bed. \nThe items spin slowly as if caught in an unseen current. \nThe atmosphere hums with a faint, low vibration, and the air is heavy with the earthy, acrid scent of decay and poison. \nYou feel sick... \nWhat has he done? How has he made such a monster...\n"
                    G.proceed("Mystery Room")
            elif "to 2nd room" in G.input:
                if G.roomEntryCounts ['Mystery Room'] == 0:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "You enter what seems to be a spare bedroom. \nIt is small and unadorned, its pale stone walls bare except for a single, crooked picture frame. \nA simple wardrobe leans against one wall, a twin bed rests against another, its blanket neatly folded but faded with age. \nThe wooden floor shows signs of wear, with scratches hinting at furniture once rearranged. A single window with thin, yellowed curtains lets in a sliver of pale moonlight. \nThe room seems to be filled with a pale yellow mist, what seem like particles of dust floating around the room.\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts ['Mystery Room'] == 1:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom is dim, with a heavy, oppressive atmosphere. \nThe walls are painted a dull, peeling green, and mushrooms pop out at odd angles, spewing a deep red gas when you get too close. \nThe bed, larger than the one in the other room, is covered in a faded quilt, its edges worn from years of use, and its top covered in a thin layer of red mold. \nThe wooden floor creaks underfoot, and the only light comes from a small, dusty lamp on a bedside table. \nA single, cracked window looks out into the night, the faintest moonlight spilling in. \nSomething is very wrong...\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts ['Mystery Room'] == 2:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom feels alive, pulsing with an eerie, unnatural energy. \nFungal growths carpet the floors and climb the walls, their spongy surfaces slick with moisture. \nPatches of bioluminescent mushrooms emit a faint, sickly green glow, casting shifting shadows across the room. \nHemlock plants grow from the cracks in the floorboards, and invade a nearby dresser. \nTheir delicate leaves brush against your shoes as you walk. \nItems inexplicably float in the air, emerging from an open chest at the end of a bed. \nThe items spin slowly as if caught in an unseen current. \nThe atmosphere hums with a faint, low vibration, and the air is heavy with the earthy, acrid scent of decay and poison. \nYou feel sick... \nWhat has he done? How has he made such a monster...\n"
                    G.proceed("Mystery Room")
            elif "to 3rd room" in G.input:
                if G.roomEntryCounts ['Mystery Room'] == 0:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "You enter what seems to be a spare bedroom. \nIt is small and unadorned, its pale stone walls bare except for a single, crooked picture frame. \nA simple wardrobe leans against one wall, a twin bed rests against another, its blanket neatly folded but faded with age. \nThe wooden floor shows signs of wear, with scratches hinting at furniture once rearranged. A single window with thin, yellowed curtains lets in a sliver of pale moonlight. \nThe room seems to be filled with a pale yellow mist, what seem like particles of dust floating around the room.\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts ['Mystery Room'] == 1:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom is dim, with a heavy, oppressive atmosphere. \nThe walls are painted a dull, peeling green, and mushrooms pop out at odd angles, spewing a deep red gas when you get too close. \nThe bed, larger than the one in the other room, is covered in a faded quilt, its edges worn from years of use, and its top covered in a thin layer of red mold. \nThe wooden floor creaks underfoot, and the only light comes from a small, dusty lamp on a bedside table. \nA single, cracked window looks out into the night, the faintest moonlight spilling in. \nSomething is very wrong...\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts ['Mystery Room'] == 2:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom feels alive, pulsing with an eerie, unnatural energy. \nFungal growths carpet the floors and climb the walls, their spongy surfaces slick with moisture. \nPatches of bioluminescent mushrooms emit a faint, sickly green glow, casting shifting shadows across the room. \nHemlock plants grow from the cracks in the floorboards, and invade a nearby dresser. \nTheir delicate leaves brush against your shoes as you walk. \nItems inexplicably float in the air, emerging from an open chest at the end of a bed. \nThe items spin slowly as if caught in an unseen current. \nThe atmosphere hums with a faint, low vibration, and the air is heavy with the earthy, acrid scent of decay and poison. \nYou feel sick... \nWhat has he done? How has he made such a monster...\n"
                    G.proceed("Mystery Room")
            elif "back" in G.input or "to upper" in G.input or "to landing" in G.input:
                print("The door you once came from is locked. \nHow could that be?\n")
        elif G.roomEntryCounts ['Long Hallway'] == 2:
            G.user_input()
            if "examine book" in G.input:
                print("")
            elif "to 1st room" in G.input:
                if G.roomEntryCounts ['Mystery Room'] == 0:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "You enter what seems to be a spare bedroom. \nIt is small and unadorned, its pale stone walls bare except for a single, crooked picture frame. \nA simple wardrobe leans against one wall, a twin bed rests against another, its blanket neatly folded but faded with age. \nThe wooden floor shows signs of wear, with scratches hinting at furniture once rearranged. A single window with thin, yellowed curtains lets in a sliver of pale moonlight. \nThe room seems to be filled with a pale yellow mist, what seem like particles of dust floating around the room.\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts ['Mystery Room'] == 1:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom is dim, with a heavy, oppressive atmosphere. \nThe walls are painted a dull, peeling green, and mushrooms pop out at odd angles, spewing a deep red gas when you get too close. \nThe bed, larger than the one in the other room, is covered in a faded quilt, its edges worn from years of use, and its top covered in a thin layer of red mold. \nThe wooden floor creaks underfoot, and the only light comes from a small, dusty lamp on a bedside table. \nA single, cracked window looks out into the night, the faintest moonlight spilling in. \nSomething is very wrong...\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts ['Mystery Room'] == 2:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom feels alive, pulsing with an eerie, unnatural energy. \nFungal growths carpet the floors and climb the walls, their spongy surfaces slick with moisture. \nPatches of bioluminescent mushrooms emit a faint, sickly green glow, casting shifting shadows across the room. \nHemlock plants grow from the cracks in the floorboards, and invade a nearby dresser. \nTheir delicate leaves brush against your shoes as you walk. \nItems inexplicably float in the air, emerging from an open chest at the end of a bed. \nThe items spin slowly as if caught in an unseen current. \nThe atmosphere hums with a faint, low vibration, and the air is heavy with the earthy, acrid scent of decay and poison. \nYou feel sick... \nWhat has he done? How has he made such a monster...\n"
                    G.proceed("Mystery Room")
            elif "to 2nd room" in G.input:
                if G.roomEntryCounts ['Mystery Room'] == 0:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "You enter what seems to be a spare bedroom. \nIt is small and unadorned, its pale stone walls bare except for a single, crooked picture frame. \nA simple wardrobe leans against one wall, a twin bed rests against another, its blanket neatly folded but faded with age. \nThe wooden floor shows signs of wear, with scratches hinting at furniture once rearranged. A single window with thin, yellowed curtains lets in a sliver of pale moonlight. \nThe room seems to be filled with a pale yellow mist, what seem like particles of dust floating around the room.\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts ['Mystery Room'] == 1:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom is dim, with a heavy, oppressive atmosphere. \nThe walls are painted a dull, peeling green, and mushrooms pop out at odd angles, spewing a deep red gas when you get too close. \nThe bed, larger than the one in the other room, is covered in a faded quilt, its edges worn from years of use, and its top covered in a thin layer of red mold. \nThe wooden floor creaks underfoot, and the only light comes from a small, dusty lamp on a bedside table. \nA single, cracked window looks out into the night, the faintest moonlight spilling in. \nSomething is very wrong...\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts ['Mystery Room'] == 2:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom feels alive, pulsing with an eerie, unnatural energy. \nFungal growths carpet the floors and climb the walls, their spongy surfaces slick with moisture. \nPatches of bioluminescent mushrooms emit a faint, sickly green glow, casting shifting shadows across the room. \nHemlock plants grow from the cracks in the floorboards, and invade a nearby dresser. \nTheir delicate leaves brush against your shoes as you walk. \nItems inexplicably float in the air, emerging from an open chest at the end of a bed. \nThe items spin slowly as if caught in an unseen current. \nThe atmosphere hums with a faint, low vibration, and the air is heavy with the earthy, acrid scent of decay and poison. \nYou feel sick... \nWhat has he done? How has he made such a monster...\n"
                    G.proceed("Mystery Room")
            elif "to 3rd room" in G.input:
                if G.roomEntryCounts ['Mystery Room'] == 0:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "You enter what seems to be a spare bedroom. \nIt is small and unadorned, its pale stone walls bare except for a single, crooked picture frame. \nA simple wardrobe leans against one wall, a twin bed rests against another, its blanket neatly folded but faded with age. \nThe wooden floor shows signs of wear, with scratches hinting at furniture once rearranged. A single window with thin, yellowed curtains lets in a sliver of pale moonlight. \nThe room seems to be filled with a pale yellow mist, what seem like particles of dust floating around the room.\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts ['Mystery Room'] == 1:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom is dim, with a heavy, oppressive atmosphere. \nThe walls are painted a dull, peeling green, and mushrooms pop out at odd angles, spewing a deep red gas when you get too close. \nThe bed, larger than the one in the other room, is covered in a faded quilt, its edges worn from years of use, and its top covered in a thin layer of red mold. \nThe wooden floor creaks underfoot, and the only light comes from a small, dusty lamp on a bedside table. \nA single, cracked window looks out into the night, the faintest moonlight spilling in. \nSomething is very wrong...\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts ['Mystery Room'] == 2:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom feels alive, pulsing with an eerie, unnatural energy. \nFungal growths carpet the floors and climb the walls, their spongy surfaces slick with moisture. \nPatches of bioluminescent mushrooms emit a faint, sickly green glow, casting shifting shadows across the room. \nHemlock plants grow from the cracks in the floorboards, and invade a nearby dresser. \nTheir delicate leaves brush against your shoes as you walk. \nItems inexplicably float in the air, emerging from an open chest at the end of a bed. \nThe items spin slowly as if caught in an unseen current. \nThe atmosphere hums with a faint, low vibration, and the air is heavy with the earthy, acrid scent of decay and poison. \nYou feel sick... \nWhat has he done? How has he made such a monster...\n"
                    G.proceed("Mystery Room")
            elif "back" in G.input or "to upper" in G.input or "to landing" in G.input:
                print("The door you once came from is locked. \nThis keeps getting weirder and weirder...\n")
        elif G.roomEntryCounts ['Long Hallway'] == 3:
            G.user_input()
            if "examine book" in G.input:
                print("")
        elif G.roomEntryCounts ['Long Hallway'] == 4:
            G.user_input()
            if "examine book" in G.input:
                print("")
