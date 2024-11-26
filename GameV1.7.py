import os
import sys
import time
import threading
import json


# Main Game Functions to track player decisions
# Ben & Ryne
class Gameloop:
    def __init__(self, script_name="GameV1.7.py"):
        self.script_name = script_name
        # Tracking visible to player
        self.currentRoom = ""
        self.roomsEntered = []
        self.inventory = ["Silver Key", "Knife"]
        # Hidden tracking
        self.roomEntryCounts = {'Trophy Room': 0, 'Long Hallway': 0, 'Mystery Room': 0}
        self.interactions = []
        self.input = ""
        self.monster = ""
        self.roomDescribe = ""

        # Initialization of state to copy game attributes
        self.state = {
            "currentRoom": self.currentRoom,
            "roomsEntered": self.roomsEntered,
            "roomEntryCounts": self.roomEntryCounts,
            "inventory": self.inventory,
            "interactions": self.interactions,
            "monster": self.monster,
            "description": self.roomDescribe
        }

    # Game Save Feature I/O
    # Ryne
    def save_game(self, filename="savegame.json"):
        # Ensures save state is availible and updated correctly
        try:
            # Update game state before saving
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

    def load_game(self, filename="savegame.json"):
        # Ensures save file is found and loaded correctly
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

    # Opens the terminal in a new tab
    # Ben
    def open_new_terminal(self):
        if os.name == 'nt':  # Windows
            if self.script_name not in sys.argv:
                os.system(f'start cmd /k python {self.script_name}')
        elif os.name == 'posix':  # Linux, macOS
            if self.script_name not in sys.argv:
                os.system(f'xterm -e python {self.script_name} &')

    # Prompts & Defines user imput
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

    # Checks if a certain room was entered so many moves ago
    # Ryne Gall
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
                print(
                    "***  A grandfather clock chime rings throughout the house. It must be 12:00! Where is Elias?  ***")
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

    # Trackers for initialized lists and dictionaries
    def add_to_inventory(self, item):
        self.inventory.append(item)

    def add_to_interactions(self, interaction):
        self.interactions.append(interaction)

    def get_current_room(self):
        return self.currentRoom

    def get_rooms_entered(self):
        return self.roomsEntered

    # Determines what monster you face during chase at game end
    def determine_monster(self):
        if len(G.roomsEntered) >= 60:
            self.monster = "Chimera"
        else:
            self.monster = "Silas"
        return self.monster


G = Gameloop()  # Create an instance of the Gameloop class
G.open_new_terminal()  # Call the method to open a new terminal


# Cody
# I was helped by my father throughout this, gave me the general idea for it.
# Class for defining functions in chase scenes
class ChaseGame:
    def __init__(self, start_time):  # defining the base for variables
        self.time_left = start_time
        self.is_caught = False
        self.timer_thread = None
        self.lock = threading.Lock()
        self.turns_taken = 0  # based number for turns
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

        print(f"Time left: {secs:02}", end="                                                        \r")

    def start_chase(self):
        while self.time_left > 0:
            self.show_time()
            time.sleep(1)
            self.time_left -= 1
            if self.turns_taken >= 10:
                break
            elif self.time_left == 0:
                self.is_caught = True
                break

        # Choices during chappends when you fail
        if self.is_caught:
            print("You're thrown to the ground", G.monster,
                  "hovers over you and raises their hand, everything goes black.\n\n\n\n\nGAME OVER")

        else:
            if G.monster == "Chimera":
                print("You run out the front and down the path from which you came.\n"
                      "From the woods you turn to see the front doors totally gone left with a singular wall and a familiar face from the 2nd story window.\n"
                      "You stop catching a breath then continue cautiously down the path.\n\n\n\n\nYOU ESCAPED")

            else:
                print("You run out the front and down the path from which you came.\n"
                      "From the woods you turn to see the front doors totally gone left with a singular wall and a familiar face from the 2nd story window.\n"
                      "You turn to your friend and smile he returns the smile with a look of relief and you both continue down the path together not ready to let each other go.\n\n\n\n\nYOU ESCAPED")

    def start_timer_thread(self):
        self.timer_thread = threading.Thread(target=self.start_chase)
        self.timer_thread.daemon = True
        self.timer_thread.start()


def timed_game_decisions(timer, stage=1):
    actions_stage_1 = {
        "1": {"action": "Scalpel", "time_change": 5,
              "response": "\nIt manages to scrape your foe not doing much for you"},
        "2": {"action": "Chair", "time_change": 15,
              "response": "\nIt hits them straight in the head leaving them temporarily dazed"},
        "3": {"action": "Blanket", "time_change": 10,
              "response": "\nIt covers their vision temporarily and they aggressively rip it off"},
    }

    actions_stage_2 = {
        "1": {"action": "Move shelf", "time_change": 20,
              "response": "\nYou shove the shelf in the way hoping to slow them down"},
        "2": {"action": "Speed up", "time_change": 5,
              "response": "\nThe adrenaline pumping through you accelerates you forward"},
        "3": {"action": "Throw tarp", "time_change": 30,
              "response": "\nYou grab a worn tarp and throw it up hoping to slow them down."},
    }

    actions_stage_3 = {
        "1": {"action": "Left", "time_change": 0, "response": "\nYou run down the hall to the left"},
        "2": {"action": "Right", "time_change": -5,
              "response": "\nYou pass by the creature from earlier who reaches out and attempts to grab you.\nDodging him leaving you with nothing but a scratch you continue to spring down the hall"},
    }

    actions_stage_4 = {
        "1": {"action": "Speed up", "time_change": 5,
              "response": "\nThe adrenaline pumping through you accelerates you forward"},
        "2": {"action": "Look ahead", "time_change": 0,
              "response": "\nYou bring yourself to a light jog and take a minute to look ahead"},
        "3": {"action": "Grab something", "time_change": 0,
              "response": "\nYou spot a tool not to far ahead and grab it"},
    }

    actions_stage_5 = {
        "1": {"action": "Run out", "time_change": 5,
              "response": "\nYou bolt out from the closet slamming the door behind you"},
        "2": {"action": "board off the basement", "time_change": 10,
              "response": "\nYou grab a spare piece of wood that would be used for a shelf and place it within the handle boarding off the basement and run out"},
        "3": {"action": "Grab supplies", "time_change": -5,
              "response": "\nYou spot some cleaning supplies and grab a mop. Is this actually useful?"},
    }

    actions_stage_6 = {
        "1": {"action": "Run out", "time_change": 5,
              "response": "\nYour anxiety makes itself known and compels you to leave"},
        "2": {"action": "Grab knife", "time_change": 10,
              "response": "\nYou sprint to the knife block and grab the largest knife then run out of the kitchen"},
        "3": {"action": "Attempt to shatter a window", "time_change": -5,
              "response": "\nYou pound your fist into the window hoping and pleading with the window that it breaks, it doesn’t"},
    }

    actions_stage_7 = {
        "1": {"action": "Throw chair", "time_change": 10,
              "response": "\nYou chuck the chair and hit them leaving them stunned and sprint out"},
        "2": {"action": "Push the table", "time_change": -5,
              "response": "\nYou attempt to ram the table into them, it being too heavy it does nothing for you and you sprint out in fear."},
        "3": {"action": "Sprint out", "time_change": 0,
              "response": "\nYou bolt out of the dining room not thinking twice"},
        "4": {"action": "Throw something", "time_change": 15,
              "response": "\nYou throw the knife/tool striking them right in the head and run ou"}
    }

    actions_stage_8 = {
        "1": {"action": "Run towards Game Room", "time_change": 0,
              "response": "\nRunning towards the game room the game room is no longer the game room but rather another long hall."},
        "2": {"action": "Attempt to run up the stairs", "time_change": -5,
              "response": "\nRunning towards the stairs you get knocked of your feet and into a long hall"},
        "3": {"action": "Bash the window", "time_change": -5,
              "response": "\nYou grab something and attempt to bash the window,it's no use."},
    }

    actions_stage_9 = {
        "1": {"action": "Speed up", "time_change": 5,
              "response": "\nThe adrenaline pumping through you accelerates you forward"},
        "2": {"action": "Turn around", "time_change": 20,
              "response": "\nYou see a figure running towards you at full speed fills you with adrenaline"},
        "3": {"action": "Throw something", "time_change": 0,
              "response": "\nYou choose to discard something random in your inventory, it misses"},
    }

    actions_stage_10 = {
        "1": {"action": "Keep running", "time_change": 10,
              "response": "\nYou keep running forward your longing for a escape fueling you"},
        "2": {"action": "Knock over pallet", "time_change": 15,
              "response": "\nYou throw the pallet to the ground behind you slowing them down"},
    }

    stage_texts = {
        1: "As you back away and reach closer and closer to the exit your options become limited.\n As you look around the room there's various objects you can throw",
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

    # Chase Stages
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

        choice = input("\n\nEnter your choice (1-4): ").strip()

        if choice in actions:
            print(f"\nYou chose to: {actions[choice]['action']}")
            time_change = actions[choice]["time_change"]
            if time_change > 0:
                timer.add_time(time_change)
            else:
                timer.subtract_time(abs(time_change))

            timer.turns_taken += 1
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
            stage = 8
        elif stage == 8:
            stage = 9
        elif stage == 9:
            stage = 10  # one ending here
        else:
            break

    timer.start_chase()


# if __name__ == "__main__":
# initial_time = 15
# timer = ChaseGame(initial_time)
# timer.start_timer_thread()
# game_decisions(timer)

# Benjamin Hall

# Tell the player the commands at the beginning of the game
class Commands:
    def __init__(self):
        self.commands = ""

    def tell_commands(self):
        self.commands = "To = Allows you to move to the room or direction stated.\nExamine = Look at an object stated.\nInteract = Pick up or touch an object\nType 'quit' at any time to save and exit the game.\n\n\n"
        print(self.commands)
        print("Inventory:", G.inventory, "\n")


C = Commands()


# Benjamin Hall

# Greet at beginning of game
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

    # Ensures input is a number and in the range availible
    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(options):
                return choice - 1
            else:
                print("Invalid choice. Please choose a valid option.")
        except ValueError:
            print("Please enter a number corresponding to your choice.")


# Cody Lincoln
# Function for the servant dialog scene / chase code ends
def servant_dialog():
    print(
        "M-My name does not matter. My daughter is Jane. She is trapped. They won't let her go. I-I have to save her.")
    print("Stay here, help him. Cater them. So she lives.")

    options = [
        'What do you mean “them?”',
        "What do you mean your daughter is trapped?",
        "Why did everybody else leave?"
    ]
    choice = dialog_options(options)
    if choice == 0:
        print(
            "\nThem. Them! Who are them? Who are t-they!” The woman’s voice rises… \n“He, HE IS EVIL. The other, the other… He is kinder, but yet, no. \nI will show no sympathy. They took her from me. \nElias. And his godforsaken father.")
    elif choice == 1:
        print(
            '"\nThey caged her. In the basement. I-I-I hear her cry at night. They… They torture her. I hear her beg them through the floor, from the kitchen. S-she calls my name”\nThe woman sheds a tear, and begins to mock in a whimper what you assume is Jane’s voice,\n “Mommy, mommy please… You said they were nice… You said Silas was kind, that Elias was kind. Mommy! Help me…”')
    elif choice == 2:
        print(
            '“\nThey, they were afraid. Rightfully so. Elias, was changing… Meaner, more brash. H-he was not the man who I knew before.”\nShe sucks in a breath, as if greedy for air, as if to say more, but she does not.')


# Options for monster encounter
# having the print on different lines within code would mess with each attributes of each option :) -Cody
def monster_encounter():
    print("As panic sets in options narrow when his malformed, sagging eye locks onto you with chilling intent.\n")
    print(
        "The very air around you feels alive, pressing against your chest and pulling at your limbs, urging you to choose before it's too late.")
    options = [
        'Run',
        "Hide",
        "Fight"
    ]
    choice = dialog_options(options)
    if choice == 0:
        print("You spin on your heel, heart hammering in your chest, and bolt down the hallway. \nEach step sends tremors through the pulsating floor, slick with blood and fungus. \nThe servant’s grotesque, disjointed frame skitters after you, his claws raking against the walls and ceiling, \nspreading his gross disease along the walls. \nAhead, the hallway bends and warps, opening into surreal vistas of past confrontations.")
        print("PRESS ENTER TO PROCEED\n")
        input()
        G.clear_screen()
        print("On your side, you see a younger Elias confronting Silas in a dimly lit laboratory. \n'You’re blinded by ambition!' Elias shouts, his voice trembling with fury. \n'What you call progress is nothing but madness!' Silas responds coldly, his eyes burning with zeal.\n'Madness births gods, Elias. And I will ascend beyond them.'\n")
        print("PRESS ENTER TO PROCEED\n")
        input()
        G.clear_screen()
        print("The hallway twists and bends, the walls warping as if alive. \nYou hear the servant’s wet, clicking groan reverberating through the narrow, shifting space. \nThe floor cracks beneath you, giving way to a vast chasm filled with writhing tendrils of flesh and bone. \nYou leap, narrowly avoiding the grasping appendages that snap at your legs, \nthe stench of decay suffocating you. In the distance, you catch a glimpse of a door, \njust a sliver of hope. Behind you, the servant lets out a guttural roar, \nthe walls fracturing and folding into grotesque corridors of flesh. \nYou veer sharply into an adjacent path, another vision flaring before you. \nSilas looms over Elias, his face a mask of detached cruelty. \n'You’ll thank me when you see what we’ve created together.'\n")
        print("PRESS ENTER TO PROCEED\n")
        input()
        G.clear_screen()
        print("As you stumble forward, the servant’s blackened claws rake against the walls, \ngouging deep furrows as it moves, causing the stone to bleed an oily ichor. \nEach strike seems to cause the manor to tremble with a low, rumbling growl. \nWith another wet, unnatural click, the servant’s swings its arm forward, \nsending a mass of raking limbs growing across the wall towards you.\n")
        print("PRESS ENTER TO PROCEED\n")
        input()
        G.clear_screen()
        print("You dodge, throwing yourself to the side as the claw swipes past, \nbut the force of the blow sends a violent tremor through the floor. Cracks explode in the walls, \nrevealing gaping mouths and grotesque, twitching limbs reaching for you from within. \nThe floor beneath you buckles, and you feel the ground shift under your feet, threatening to swallow you whole.\n")
        print("PRESS ENTER TO PROCEED\n")
        input()
        G.clear_screen()
        print("You push harder, your lungs burning, your heart thudding painfully in your chest. \nA flash of light beckons in the distance… a door. \nYou race toward it, your breath ragged, but the servant is too close. \nWith a scream of horror, you dive forward, slamming into the door just as the servant’s claw brushes your skin, \nripping through the back of your shirt. The door slams shut with a deafening bang, \ncutting off the relentless clicking and the sound of the servant’s roars, \nleaving only a lingering sense of dread in the heavy silence.\n")
        print("PRESS ENTER TO PROCEED\n")
        input()
        G.clear_screen()
        G.add_to_interactions("Journal Chase")
        C.tell_commands()
        G.roomDescribe = "There is a small alcove a short bit down the stairs that branches to more rooms. \nFurther down is the entrance hall. \nAcross the balcony is the door to the master bedroom.\n"
        G.proceed("Upper Landing")
    elif choice == 1:
        print("You dart into a nearby room, the door creaking ominously as you slam it shut it behind you. \nThe room is small and claustrophobic, lit faintly by a pulsating, bioluminescent fungus clinging to the walls. \nA cracked wardrobe leans in the corner, and the faint sound of your own breath is deafening in the stifling air. \nYou press yourself into the shadows, crouching behind an overturned chair, your heart pounding \nas the grotesque figure approaches.\n")
        print("PRESS ENTER TO PROCEED\n")
        input()
        G.clear_screen()
        print("The servant’s jagged claws scrape along the door as it swings open with a groan. \nThe air thickens with the acrid scent of rot, and your vision blurs as spores waft into the room. \nHis disjointed frame stumbles in, the warped sound of wet clicking echoing unnervingly. \nHis sagging eye scans the room, his grotesque form jerking in unnatural motions as he searches.\n")
        print("PRESS ENTER TO PROCEED\n")
        input()
        G.clear_screen()
        print("Every scrape of his claws sends tremors through the decayed wood. \nHe lingers by the wardrobe, one claw dragging across its surface, carving jagged lines into the wood. \nThen he turns suddenly, the hanging eye twitching as if sensing something unseen. \nYou hold your breath, pressing further into the shadows as his gaze lingers inches from your hiding spot.\n")
        print("PRESS ENTER TO PROCEED\n")
        input()
        G.clear_screen()
        print("Finally, after what feels like an eternity, he lets out a distorted groan and lumbers back into the hallway, \nhis twisted body disappearing into the flickering light.You exhale shakily and notice something glinting on the desk by the window. \nA folded note, faintly dusted with spores, catches your attention. It’s written in a hurried, jagged script:\n\n\n")
        print("PRESS ENTER TO PROCEED\n")
        input()
        G.clear_screen()
        print("   'I have spent my life chasing answers to questions we dare not ask. \n   Death is not an end; it is a failure. \n   A failure of the body to endure, of the mind to persist, of the self to surpass its limitations. \n   It is an insult to our potential, a reminder of our fragility. \n   Why should the spark of consciousness, the one miracle we truly possess, \n   be snuffed out like a candle in the wind?\n")
        print("PRESS ENTER TO PROCEED\n")
        input()
        G.clear_screen()
        print("   I seek to cure death not for myself, nor for any single person, but for the principle. \n   To transcend our frailty is to declare dominion over nature itself. \n   To die is to accept that we are small, transient, and insignificant. \n   But what if we are not? \n   What if we could grow beyond the narrow boundaries of what we are told is possible? \n   What if humanity could become something greater?\n")
        print("PRESS ENTER TO PROCEED\n")
        input()
        G.clear_screen()
        print("   I will not let the universe dictate our fate. \n   I will prove that we can endure. \n   That we can reign eternal.'\n   ~ Dr. Silas Finch\n\n\n")
        print("PRESS ENTER TO PROCEED\n")
        input()
        G.clear_screen()
        print("As you fold the note, a shiver runs down your spine. \nSilas's intentions, while shrouded in twisted logic, stemmed from a very human desire. \nThe air in the room feels heavier with this knowledge, and you slip quietly back into the hallway, \nthen to the landing, your resolve questioning under the weight of his revelation.\n")
        print("PRESS ENTER TO PROCEED\n")
        input()
        G.clear_screen()
        G.add_to_interactions("Journal Chase")
        C.tell_commands()
        G.roomDescribe = "There is a small alcove a short bit down the stairs that branches to more rooms. \nFurther down is the entrance hall. \nAcross the balcony is the door to the master bedroom.\n"
        G.proceed("Upper Landing")
    elif choice == 2:
        print(
            'Gripping your knife, you face the monstrous servant, your pulse pounding with terror and resolve. \nAs he lunges, you strike, a desperate, wild action that tears into the fleshy growths writhing across his frame. \nHe recoils, emitting a deafening, wet groan, his limbs twitching violently. \nWith a swipe of his blackened claws, he catches your shoulder with sickening precision. \nPain blooms hot and sharp, a blinding agony that floods your senses as blood splatters across the walls. \nThe moment your skin rends, you feel something worse… Fingers, grotesque and malformed, sprout from the wound, \nwrithing and tearing deeper, as if the pain itself is clawing to consume you from the inside.\n')
        print("PRESS ENTER TO PROCEED\n")
        input()
        G.clear_screen()
        print("You gasp, choking on the searing pain, but your grip tightens around your weapon. \nYou cannot stop. You cannot let him win. With sheer will, you force your body forward, slamming the knife into the servant once again. \nHe stumbles back, his disjointed limbs faltering, a deep, wet wheeze escaping from his throat. \nThen, his eye. That sagging, malformed orb locks onto yours.\n")
        print("PRESS ENTER TO PROCEED\n")
        input()
        G.clear_screen()
        print("For a single, horrifying moment, your thoughts splinter, like the jagged cracks of a broken mirror. \nHis essence floods into your mind, a torrent of despair, rage, and pain so intense it drowns out your every sense. \nHis thoughts are not his own, but a patchwork of horrors and regrets from a thousand twisted souls. \nYou hear whispers, feel their suffocating anguish clutch at your very being. \nThe world around you begins to bend, to warp, shifting into something... else.\n")
        print("PRESS ENTER TO PROCEED\n")
        input()
        G.clear_screen()
        print("You see something, but you don't see it. It’s not a place, nor a time, but a feeling. \nThe sense of being trapped somewhere endless, surrounded by the bodies of those you once loved, \ntheir eyes hollow, their faces twisted in agony. Their voices scream without sound. \nIt’s all crushing. Suffocating.\n")
        print("PRESS ENTER TO PROCEED\n")
        input()
        G.clear_screen()
        print("A sharp, sudden twist of your body snaps you back to reality. \nThe vision shatters like glass, but the terror lingers in your bones, clawing at the edges of your sanity. \nYou get up and run, throwing yourself around corners, down corridors that seem to stretch endlessly, \neach turn more disorienting than the last. \nThe manor itself seems to shift around you, trying to trap you, to confuse you, but you won’t let it. \nNot now. Not while you still have breath in your lungs.\n")
        print("PRESS ENTER TO PROCEED\n")
        input()
        G.clear_screen()
        print("At last, you reach a door. \nWith a desperate, almost hysterical strength, you hurl it open, slamming it behind you. \nThe sound of the servant’s claws scraping against the wood echoes in the dark, \n when you finally collapse against the door, gasping for breath.\n")
        print("PRESS ENTER TO PROCEED\n")
        input()
        G.clear_screen()
        print("You don’t know what you saw, but you feel it still.\n")
        print("PRESS ENTER TO PROCEED\n")
        input()
        G.clear_screen()
        G.add_to_interactions("Journal Chase")
        C.tell_commands()
        G.roomDescribe = "There is a small alcove a short bit down the stairs that branches to more rooms. \nFurther down is the entrance hall. \nAcross the balcony is the door to the master bedroom.\n"
        G.proceed("Upper Landing")
    return choice


# Benjamin Hall

# Starting the Game / Main game loop

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

# Benjamin and Ryne
# This is the main game loop

# Determines whether to trigger game end
stop_all = False
# stop_all determines whether the game continues to run. It is changed to true at each end of the story.
while not stop_all:

    # Occurs when the room is the entrance hall
    while G.currentRoom == "Entrance Hall":
        # After each room description through the G.roomDescribe function an input is required
        G.user_input()
        # Each input is then scanned for key phrases which include the commands listed at the top of the terminal screen.
        if "to landing" in G.input or "to stairs" in G.input:
            G.clear_screen()
            C.tell_commands()
            # Determines if an action has been taken, generating a different output conditionally
            if "Journal Chase" not in G.interactions:
                G.roomDescribe = "Up the stairs there is a small alcove contain some trophies that branches into more rooms. \nFurther up is the balcony which overlooks the entrance hall.\n\n\nThere are doors to the master bedroom and a long hallway.\nOtherwise, the balcony is mostly bare. \n"
            else:
                G.roomDescribe = "Up the stairs there is a small alcove contain some trophies that branches into more rooms. \nFurther up is the balcony which overlooks the entrance hall.\n\n\nThere is a door to the master bedroom.\nOtherwise, the balcony is mostly bare.\n"
            G.proceed("Upper Landing")
        elif "to game" in G.input or "to game room" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = "You enter the mansion's game room, immediately taking in the sharp aroma of alcohol and pool chalk. \nThe small square room has an open archway in the back that leads into a lounge. \n\n\nIn the front of the room lies a couch, a tv sitting on a stand across from it, buzzing static. \nA large red-felted pool table behind the couch displays a losing game of solids against stripes. \nA broken cue is discarded upon the table, snapped in half. \nA dartboard hangs from a wall behind the pool table, with some darts still scattered upon the floor and pinned into the wall.\n\n\nThe door behind you leads to the entrance hall.\n"
            G.proceed("Game Room")
        elif "to lounge" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = "You enter the lounge, the faint smell of firewood pricking your nose. \nScattered across the room, but all facing a central fireplace, are a few armchairs, a coffee table, and a large painting of what looks like Elias, but older. \n\n\nA door leads into the library, another to the entrance hall, and an archway opens up into the game room.\n"
            G.proceed("Lounge")
        elif "to dining" in G.input or "to dining room" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = "You enter the dining room. \nRich wooden floors and rugged stone walls line the room. \nA long, dark oak table stretches out in the center of the room, surrounded by carved wooden chairs. \nCandles hang along the wall and on the table, emanating an eerie glow. \n\n\nFood lines the table, the smell of meat and wine fills the air. \nAt the head of the table, sits a finished meal of steak and wine, and next to it, a half-eaten messy abomination of what you think used to be chicken, torn to shreds.\n\n\nThere is a door leading to the kitchen and one behind you going back to the entrance hall.\n"
            G.proceed("Dining Room")
        elif "examine pillar" in G.input:
            print(
                "\nLarge and crumbling ornate pillars supports the manor, carved with intricate patterns and words in another language.\n")
        elif "examine stone" in G.input:
            print(
                "\nThe large stones that litter the ground appear to have fallen from a large faded mural on the ceiling. \nYou can only make out the remains of a large star. \nSmaller stones sit akin to the large.\n")
        elif "examine door" in G.input:
            print(
                "\nThe mahogany door you came through towers over you. \nYou try to turn the large silver handle, but it doesn't budge. \nYou will need a key.\n")
        elif "examine carpet" in G.input:
            print(
                "\nThe carpet is old and worn, moreso in the areas that intersect the paths to the left and right doors. \nIt strikes you as odd, for Elias has always been a tidy man.\n")
        elif "interact stone" in G.input:
            # Ensures that items within the inventory cannot be picked up again.
            if "Stone" not in G.inventory:
                print("\nYou pick up a stone off the ground.\n")
                G.add_to_inventory("Stone")
            elif "Stone" in G.inventory:
                print("\nYou already picked up the stone.\n")
        # If the input is to quit the game the stop_all is triggered, breaking the main loop
        elif "quit" in G.input:
            G.save_game()
            stop_all = True
            break
        # If the input is scanned and has no corresponding output, an error message is printed and actions are recommended.
        else:
            print("\nInvalid input, try 'to game room', 'examine stone', or 'interact door'.\n")

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
            G.roomDescribe = "You enter the lounge, the faint smell of firewood pricking your nose. \nScattered across the room, but all facing a central fireplace, are a few armchairs, a coffee table, \nand a large painting of what looks like Elias, but older. \n\n\nA door leads into the library, another to the entrance hall, and an archway opens up into the game room behind you.\n"
            G.proceed("Lounge")
        elif "examine pool" in G.input or "examine table" in G.input:
            print(
                "\nYou see a game of pool, with stripes having an apparent winning position. You notice the 8 Ball is missing, and find it in one of the pockets. \nYou look towards the broken cue. It seems like the solids player was having a bad day.\n")
        elif "interact cue" in G.input:
            if "Cue" not in G.inventory:
                print("\nYou grab one of the broken halves of the pool cue.\n")
                G.add_to_inventory("Cue")
            elif "Cue" in G.inventory:
                print("\nYou already picked up the cue.\n")
        elif "examine couch" in G.input:
            print(
                "\n couch is a deep maroon leather stitched with ivory. \nYou sit upon it, and surprisingly, you sink into it as if it were plush. \nYou feel like you tune on a good show and stay here for hours. \n")
        elif "examine tv" in G.input:
            print("\nA fancy black old television upon an ivory stand. \nIt displays a buzzing static.\n")
        elif "examine dart" in G.input or "examine board" in G.input:
            print(
                "\nA large round dart board, a game of blue versus yellow. \nBlue has a dart in the green circle surrounding the bullseye, with one more in the red 18 section of the red and green inner ring, another in the white 15 inner ring section, and a final dart in the outer black 13 section. \nYellow has two darts immersed into the wall, and one bullseye.\n")
        elif "interact couch" in G.input:
            print("\nYou rifle through the couch, and find a leaflet on the rules for darts, and a tv remote.\n")
        elif "interact remote" in G.input:
            if "Game Room Remote" not in G.interactions:
                print(
                    "\nYou click the remote, and Frankenstein begins playing. \nYou watch as Victor shocks his creation, shouting his iconic line, 'It's Alive!'\n")
                G.add_to_interactions("Game Room Remote")
            elif "Game Room Remote" in G.interactions:
                print("Y\nou click the tv remote, turning it back to static.\n")
        elif "interact leaflet" in G.input or "interact rules" in G.input:
            print(
                "\nYou open the leaflet, it reads:\nPlayers should stand 7ft 9in from the dart board, with both feet on the ground. \nPlayers should hold the dart in their dominant hand, and throw it straight without too much force. \nThe dart board has 20 numbered sections, with the bullseye in the center. The bullseye's outer ring is worth 25 points, and the inner circle is worth 50 points. \nThe black and white outer and inner rings are worth the point value displayed, and the outer red and green ring is worth double points, while the inner is worth triple. \nPlayers take turns throwing 3 darts per turn. \nYou start with 501 points, and the goal is to reduce your score to zero, but the last dart thrown must land in a double or the bullseye.\n")
        elif "quit" in G.input:
            G.save_game()
            stop_all = True
            break
        else:
            print("\nInvalid input, try something like 'to lounge', 'examine pool table', or 'interact cue'.\n")

    while G.currentRoom == "Lounge":
        G.user_input()
        if "back" in G.input or "to entrance" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = "You go back into the entrance hall; the floors here are stone, with towering pillars of marble sprouting out.\nThe cobble walls crumble around you, spider webs seem to devour every dark corner of the room, and chunks of stone litter the ground.\nA single red carpet runs below your feet and up a grandiose spruce staircase, leading left and right.\nIts red fabric runs like fine wine flowing up to the landing.\n\n\nThe room is illuminated only by dim, flickering lanterns that hang from the ceiling. A wooden balcony overlooks the room you are in.\nThe room is eerily quiet, apart from the sound of your own short breathing and the creaking of the manor.\n\n\nTwo doors line the right wall, to the game room and lounge, and one sits on the left wall leading to a dining room.\n"
            G.proceed("Entrance Hall")
        elif "to library" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = "You enter the library, and the scent of old wood and paper fills the air. \nTowering bookshelves line the walls, and a giant balcony looks over you. \n\n\nYou notice main shelving units on the left, right, and center. \nA single table sits in solitude next to the center bookshelves. \n\n\nThe door behind you leads to the lounge, and another in the back leads to the guest bathrooms.\n"
            G.proceed("Lower Library")
        elif "to game room" in G.input or "to archway" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = "You enter the mansion's game room, immediately taking in the sharp aroma of alcohol and pool chalk.\n\n\nIn the front of the room lies a couch, a tv sitting on a stand across from it, buzzing static. \nA large red-felted pool table behind the couch displays a losing game of solids against stripes. \nA broken cue is discarded upon the table, snapped in half. \nA dartboard hangs from a wall behind the pool table, with some darts still scattered upon the floor and pinned into the wall.\n\n\nThe archway behind you leads to the lounge, while the door goes to the entrance hall.\n"
            G.proceed("Game Room")
        elif "examine fireplace" in G.input:
            if "Hedda Gabler Lever" in G.interactions:
                print(
                    "\nThe fireplace is a classic gray brick, with a metal holder holding ashen wood, and a fire prod stuck inside. \n\n\nYou see behind the fireplace is an old lockbox with a combination lock. \nThere are colored tiles, Green, Black, Red, and White, with sliders to input numbers.\n")
                print(
                    "You may input any four numbers ranging from 1 to 99 in each slot with a space between each number. \nWhat would you like to input?\n")
                lockbox_input = input("> ")
                if "25 13 54 15" in lockbox_input:
                    print(
                        "\nYou hear a click, and lift the lid of the box. Inside you find a small bronze key, and pocket it.\n")
                    G.add_to_inventory("Bronze Key")
                elif "25 13 54 15" not in lockbox_input:
                    print("\nThe lockbox does not open.\n")
            elif "Hedda Gabler Lever" not in G.interactions:
                print(
                    "\nThe fireplace is a classic gray brick, with a metal holder holding ashen wood, and a fire prod stuck inside. \nOddly, you see no vent to channel the smoke, and the fireplace seems more shallow than you would expect.\n")
        elif "examine painting" in G.input:
            print(
                "\nAs you walk closer, you notice the painting isn't actually of Elias, but rather of his Father, Silas. \nAlthough sitting regally in a fine armchair, he seems roughened up. \nMiddle aged with a stubble covered face and crooked nose; he looks weary, this was probably painted close to his death.\n")
        elif "interact painting" in G.input:
            if "Note: '6'" not in G.inventory:
                print(
                    "\nYou lift up the painting, and a note falls to the ground. Picking it up to read, it simply says '6'.")
                G.add_to_inventory("Note: '6'")
            elif "Note: '6'" in G.inventory:
                print("\nYou already found a note here that read: '6'\n")
        elif "interact prod" in G.input:
            print("\nAs you pick up the fire prod, the weak metal turns to ash in your hands.\n")
        elif "examine armchair" in G.input:
            if "\nShopping list: 'Botany Book, Bucket, Painting, and Boar Head Mantle'" not in G.inventory:
                print(
                    "\nYou scavenge through the armchairs, only finding some loose change and an old shopping list that reads:\nBotany Book, Bucket, Painting, and Boar Head Mantle. \n")
                G.add_to_inventory("Shopping list: 'Botany Book, Bucket, Painting, and Boar Head Mantle'")
            elif "\nShopping    list: 'Botany Book, Bucket, Painting, and Boar Head Mantle'" in G.inventory:
                print("This is where you found the shopping list.\n")
        elif "examine table" in G.input:
            print(
                "\nScattered atop the coffee table are a variety of pages, appearing to be torn from various books. \nThe table also seems to be burnt in areas, with holes pokes through some of the pages and through the table. \nThe legible pages include a ripped up children's book on learning to read, \na page from Elias’s favorite book: 'Hedda Gabler', and an excerpt from the poem “On Being Human.” \nThe except reads:\n\n   Far richer they! I know the senses' witchery\n   Guards us like air, from heavens too big to see;\n   Imminent death to man that barb'd sublimity\n   And dazzling edge of beauty unsheathed would be.\n   Yet here, within this tiny, charmed interior,\n   This parlour of the brain, their Maker shares\n   With living men some secrets in a privacy\n   Forever ours, not theirs.\n")
        elif "quit" in G.input:
            G.save_game()
            stop_all = True
            break
        else:
            print("\nInvalid input, try 'examine fireplace' or 'interact painting'\n")

    while G.currentRoom == "Lower Library":
        G.user_input()
        if "back" in G.input or "to lounge" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = "You go back into the lounge, the faint smell of firewood pricking your nose. \nScattered across the room, but all facing a central fireplace, are a few armchairs, a coffee table, \nand a large painting of what looks like Elias, but older. \n\n\nThe door behind you leads into the library, another to the entrance hall, and an archway opens up into the game room.\n"
            G.proceed("Lounge")
        elif "to bathroom" in G.input or "to guest" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = "You enter the Guest Bathrooms, what would be a pristine room, if not for the giant blood stains all over the floor, the mirror, the walls, everywhere. \nEven the toilets in the stall. \nIt is horrifying, appalling. \nYou lurch forward, but stop yourself before hurling up your dinner.\n\n\nThe door behind you goes back into the library.\n"
            G.proceed("Guest Bathrooms")
        elif "examine balcony" in G.input or "examine above" in G.input or "examine upper" in G.input:
            if "Balcony Man" not in G.interactions:
                print(
                    "\nYou hear a faint gurgle and look up towards the balcony, noticing what looks like a man peering over at you. \nAll you see is pale white skin before he disappears with a blur.\n")
                G.add_to_interactions("Balcony Man")
            elif "Balcony Man" in G.interactions:
                print("\nThe man you once saw on the floor above you is gone.")
        elif "examine table" in G.input:
            print(
                "\nAtop the table you see a book of mythical creatures, a book about genetic limits, opened to a page about how man reacts to various torture,\nand a note written in a dirty scrawl not typical of Elias that reads: \n\n'I have discovered something new, something grand, something that extends the limits of man beyond death, beyond age, beyond mortal comprehension... Beyond life.'\n")
        elif "examine left" in G.input:
            print(
                "\nWalking over to the left bookshelves, you see books scattered across the floor in what seems to be the remnants of a fight.\n")
        elif "examine right" in G.input:
            print(
                "\nAlong the right shelves, you notice a couple of classic literature books poking out from the book rack:\n'Brave New World,''Fall of the House of Usher' and 'Hedda Gabler.'\n")
            G.add_to_interactions("Bookshelf")
        elif "examine center" in G.input:
            print(
                "\nAlong the center shelves, you take note of a couple books that seem more used than the others, titled:\n'Basics of Mycology', 'Occult: Into the Unknown', and 'Botany Knowledge for Beginners'.\n")
            G.add_to_interactions("Bookshelf")
        elif "interact hedda" in G.input:
            if "Hedda Gabler Lever" not in G.interactions:
                print(
                    "\nAs you attempt to grab the book, it doesn't pull out all the way. \nInstead, it shifts out slightly and you hear a click, and the slide of stone against stone coming from the lounge.\n")
                G.add_to_interactions("Hedda Gabler Lever")
            elif "Hedda Gabler Lever" in G.interactions:
                print("\nYou already pulled this book lever.\n")
        elif "interact botany" in G.input or "interact beginners" in G.input:
            if "Note: '2'" not in G.inventory:
                print("\nAs you open the book, a note falls out. \nIt reads: '2'\n")
                G.add_to_inventory("Note: '2'")
            elif "Note: '2'" in G.inventory:
                print("\nYou already found a note here that read: '2'\n")
        elif "interact house" in G.input or "interact fall" in G.input or "interact basics" in G.input or "interact mycology" in G.input or "interact occult" in G.input:
            print("\nYou open the book and thumb through it. \nNothing appears out of the ordinary.\n")
        elif "quit" in G.input:
            G.save_game()
            stop_all = True
            break
        else:
            if "Bookshelf" in G.interactions:
                print(
                    "Invalid input, try 'interact botany knowledge for beginners' or 'examine table' or 'to guest bathrooms'\n")
            elif "Bookshelf" not in G.interactions:
                print("\nInvalid input, try 'examine table' or 'to guest bathrooms'\n")

    while G.currentRoom == "Guest Bathrooms":
        G.user_input()
        if "back" in G.input or "to library" in G.input or "to lower library" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = "You go back into the library, and the scent of old wood and paper fills the air. \nTowering bookshelves line the walls, and a giant balcony looks over you. \n\n\nYou notice main shelving units on the left, right, and center. \nA single table sits in solitude next to the center bookshelves. \n\n\nThe door behind you leads to the guest bathrooms, and another to the lounge.\n"
            G.proceed("Lower Library")
        elif "examine mirror" in G.input:
            print("\nOn the mirror, a message is written in blood: 'HELP ME'\n")
        elif "examine toilet" in G.input:
            if "Toilet Note" not in G.inventory:
                print(
                    "\nIn the toilet, floating in the water, you find a note. \nYou reach your hand inside, and lift the sopping wet note, careful to not damage it. \nThe letters are mostly blotched, but you can make out the words: \n'It was a mistake', 'Why is he doing this to me', and 'If you find this...'\n")
                G.add_to_inventory("Toilet Note")
            elif "Toilet Note" in G.inventory:
                print(
                    "\nThis is where you found a damaged note with the writings: \n'It was a mistake', 'Why is he doing this to me', and 'If you find this...'\n")
        elif "quit" in G.input:
            G.save_game()
            stop_all = True
            break
        else:
            print("\nInvalid input, try 'to library' or 'examine mirror'.\n")

    while G.currentRoom == "Dining Room":
        G.user_input()
        if "back" in G.input or "to entrance" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = "You go back into the entrance hall; the floors here are stone, with towering pillars of marble sprouting out.\nThe cobble walls crumble around you, spider webs seem to devour every dark corner of the room, and chunks of stone litter the ground.\nA single red carpet runs below your feet and up a grandiose spruce staircase, leading left and right.\nIts red fabric runs like fine wine flowing up to the landing.\n\n\nThe room is illuminated only by dim, flickering lanterns that hang from the ceiling. A wooden balcony overlooks the room you are in.\nThe room is eerily quiet, apart from the sound of your own short breathing and the creaking of the manor.\n\n\nTwo doors line the right wall, to the game room and lounge, and one sits on the left wall leading to a dining room.\n"
            G.proceed("Entrance Hall")
        elif "to kitchen" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = "You walk into the manors kitchen. \nGranite counter-tops and wooden shelves line the walls,\nholding copper pots, cast-iron skillets, and other rustic kitchenware. \nA large fridge is wedged between the counters and cabinets, \nand a small island floats in the middle of the room, wooden bar stools propped against it. \nStrange beakers and scientific devices line up atop the bar. \n\n\nBehind you is the door to the dining room and there is a door to a supply closet on the far wall.\n"
            G.proceed("Kitchen")
        elif "examine table" in G.input:
            if "Apple" in G.inventory and "Knife" in G.inventory:
                print("\nThere is nothing underneath the table.\n")
            elif "Apple" in G.inventory:
                print("\nUnderneath the table, you find a steak knife has fallen to the floor.\n")
            elif "Knife" in G.inventory:
                print("\nUnderneath the table lies an apple which glistens in the candlelight.\n")
            else:
                print(
                    "\nUnderneath the table lies an apple which glistens in the candlelight.\nA steak knife has also fallen to the floor.\n")
        elif "interact apple" in G.input:
            if "Apple" not in G.inventory:
                print(
                    "\nYou pick up the apple and hold the apple to your mouth, promptly biting into it. \nYou are instantly disgusted as the taste and smell of rot assaults your senses. \n \nThe inside of the apple is filled with fungus and leaks a foul red goo nYou toss it to the floor, gagging.\n")
                G.add_to_inventory("Apple")
            elif "Apple" in G.inventory:
                print("\nYou already picked up the apple.\n")
        elif "interact knife" in G.input or "interact steak knife" in G.input:
            if "Knife" not in G.inventory:
                print("\nYou grab the knife.\n")
                G.add_to_inventory("Knife")
            elif "Knife" in G.inventory:
                print("\nYou already picked up the knife.\n")
        elif "interact candle" in G.input:
            if "Candle" not in G.inventory:
                print("\nYou pick up a candle, holding it by the brass chamberstick in your left hand.\n")
                G.add_to_inventory("Candle")
            elif "Candle" in G.inventory:
                print("\nYou already picked up a candle.\n")
        elif "quit" in G.input:
            G.save_game()
            stop_all = True
            break
        else:
            print("\nInvalid input, try 'interact candle' or 'to kitchen'.\n")

    while G.currentRoom == "Kitchen":
        G.user_input()
        if "back" in G.input or "to dining" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = "You go back into the dining room. \nRich wooden floors and rugged stone walls line the room. \nA long, dark oak table stretches out in the center of the room, surrounded by carved wooden chairs. \nCandles hang along the wall and on the table, emanating an eerie glow. \n\n\nFood lines the table, the smell of meat and wine fills the air. \nAt the head of the table, sits a finished meal of steak and wine, and next to it, a half-eaten messy abomination of what you think used to be chicken, torn to shreds.\n\n\nThere is a door leading to the entrance hall and one behind you to the kitchen.\n"
            G.proceed("Dining Room")
        elif "to supply" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = "\nYou enter the Supply closet, a dingy little room filled with cleaning supplies. \nYou notice a mop and bucket. \nThere is not really much to see. \n\n\nBut perhaps most important, and very concerning, what you do see is a blood stain leading to a hatch. \nMost likely to a basement.\n\n\nThere is a door behind you to the kitchen.\n"
            G.proceed("Supply Closet")
        elif "examine bar" in G.input:
            print(
                "\nAlong the bar, next to some strange scientific tools, a few sealed beakers lie with strange labels like 'thymidine', and 'ethidium bromide'.\n")
        elif "examine counter" in G.input or "examine cabinet" in G.input or "examine counter-top" in G.input:
            print(
                "\nInside the cabinets and atop the counters, among the standard silverware and cutlery. \nYou also notice a small blood stain, and bloody hand-prints gripping the counter beside it.")
            if "Painkillers" not in G.inventory:
                print("\nYou find a small bottle of painkillers.\n")
            else:
                print("\n")
        elif "examine fridge" in G.input:
            print(
                "\nYou open the rustic fridge door, and inside lies an array of elegant food. \nSteaks, caviar, truffles, and more. \nAmong these sit some odd foods, what look like strange meats with leathery skins or cuts of beef with sharp, mangy black fur still attached. \nAll of this accompanied by the most foul smell imaginable, like sulfur and rotting fungus.\n")
        elif "interact beaker" in G.input:
            print("\nIt would be wiser not to touch these...")
        elif "interact painkiller" in G.input or "interact bottle" in G.input:
            if "Painkillers" not in G.inventory:
                print("\nYou pick up the bottle of painkillers.\n")
                G.add_to_inventory("Painkillers")
        elif "quit" in G.input:
            G.save_game()
            stop_all = True
            break
        else:
            print("\nInvalid input, try 'examine fridge' or 'to supply closet'.\n")

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
                G.roomDescribe = "You enter the Master bedroom, and a giant Alaskan king canopy bed greets you. \nIts sheets are a deep black with blankets a deep mahogany red. \nThe furniture is of the same color, all opulent and grand in design. \nBut what strikes your eye is none of the grandiose, but a simple leather bound journal laying atop the bed.\n"
                G.proceed("Master Bedroom")
            elif "Bronze Key" not in G.inventory:
                print("/nYou will need a key to enter this room.\n")
        elif "to long" in G.input or "to hallway" in G.input:
            if "Journal Chase" not in G.interactions:
                if "Silver Key" in G.inventory:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "You step into a dimly lit hallway. \nThe air is thick with dust, and you can smell the faint scent of mildew. \nCracked stone walls are lined with faded tapestries, their patterns obscured by cobwebs. \nThe wooden floor creaks underfoot, each step echoing faintly. \nA flickering lantern at the far end casts long, wavering shadows.\nA small thin and tall table sits on the adjacent wall. \nAtop it, a book, and a painting of Silas and somebody else, with two candles dimly flickering next to it.\n\n\nThe door behind you leads back into the upper landing.There are three doors ahead, numbered 1, 2, and 3.\n"
                    G.proceed("Long Hallway")
                elif "Bronze Key" in G.inventory:
                    print("\nYou don't have the right key to enter this room.\n")
                else:
                    print("\nYou will need a key to enter this room.")
            elif "Journal Chase" in G.interactions:
                print("\nThere used to be a door there, now there isn't.\n")
        elif "quit" in G.input:
            G.save_game()
            stop_all = True
            break
        else:
            print("\nInvalid input, try 'to hallway' or 'to master'.\n")

    while G.currentRoom == "Master Bedroom":
        G.user_input()
        if "back" in G.input or "to landing" in G.input or "to upper" in G.input:
            G.clear_screen()
            C.tell_commands()
            if "Journal Chase" not in G.interactions:
                G.roomDescribe = "There is a small alcove branching into more rooms. \nFurther up is the balcony which overlooks the entrance hall downstairs.\n\n\nThe door you came from leads to the master bedroom and one on the other end leads to a long hallway.\nOtherwise, the balcony is mostly bare. \n"
            else:
                G.roomDescribe = "There is a small alcove branching into more rooms. \nFurther up is the balcony which overlooks the entrance hall downstairs.\n\n\nThe door you came from leads to the master bedroom.\nOtherwise, the balcony is mostly bare.\n"
            G.proceed("Upper Landing")
        elif "examine bed" in G.input or "examine furniture" in G.input:
            print(
                "\nYou scavenge the Furniture and Bed, and find... Nothing... Absolutely nothing but clothes and sheets. \nThis room is extremely clean. \nYou even search the restroom in the corner of the room, and yet, nothing.\n")
        elif "examine journal" in G.input or "interact journal" in G.input:
            print("\nThe journal is padlocked shut by a combination code with four digits.\n")
            print(
                "\nYou may input any four numbers ranging from 0 to 9 in each slot with a space between each number. \nWhat would you like to input?\n")
            padlock_input = input("> ")
            if padlock_input == "2 9 6 4":
                print(
                    "\nThe padlock clicks open. \nYou flip through the journal, finding various pages with detailed scriptures and writings made by Silas entailing various gene experiments he's done.\n\n\nIn the back of the book is a compartment containing a silver key.\nYou pocket it.\n")
                G.add_to_inventory("Silver Key")
            else:
                print("\nThe padlock remains locked.\n")
        elif "quit" in G.input:
            G.save_game()
            stop_all = True
            break
        else:
            "/nInvalid input, try 'examine journal' or 'to landing'.\n"

    while G.currentRoom == "Trophy Room":
        G.user_input()
        if "to servant's" in G.input or "to quarters" in G.input or "to servants" in G.input:
            if "Bronze Key" in G.inventory:
                G.clear_screen()
                C.tell_commands()
                if "Servant Question" not in G.interactions:
                    G.roomDescribe = "You walk into the servants quarters, the lights here are dim and flickering. \nBunk beds line one wall, dressers the other. You can hear the sound of running water from the bathrooms.\n\n\nThe door to the trophy room is behind you, and you may examine the bathroom.\n"
                    G.proceed("Servant's Quarters")
                elif "Servant Question" in G.interactions:
                    G.roomDescribe = "You walk into the servants quarters, the lights here are dim and flickering. \nBunk beds line one wall, dressers the other. \nYou can hear the sound of running water from the bathrooms. \nWhere the woman once stood, there are a few mushrooms growing out of the floorboards.\n\n\nThe door to the trophy room is behind you."
                    G.proceed("Servant's Quarters")
            elif "Bronze Key" not in G.inventory:
                print("\nYou will need a key to enter this room.\n")
        elif "back" in G.input or "to landing" in G.input or "to upper landing" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = "The small alcove you came from holds trophies and doors to more rooms. \nFurther up is the balcony which overlooks the entrance hall downstairs.\n"
            if "Journal Chase" not in G.interactions:
                print(
                    "\n\nThere are doors to the master bedroom and a long hallway.\nOtherwise, the balcony is mostly bare. \n")
            else:
                print("\n\nThere is a door to the master bedroom.\nOtherwise, the balcony is mostly bare.\n")
            G.proceed("Upper Landing")
        elif "to library" in G.input or "to upper library" in G.input:
            if "Bronze Key" in G.inventory:
                G.clear_screen()
                C.tell_commands()
                G.roomDescribe = "You walk into the upper library, meeting the pleasant smell of parchment and leather. \nThere are fewer shelves here than upstairs, though there is also less floor space with the lower library floor seen below. \nOnly on the left and right, while a couch overlooks the balcony to the lower library.\n\n\nThe door behind you goes back into the trophy room.\n"
                G.proceed("Upper Library")
            elif "Bronze Key" not in G.inventory:
                print("\nYou will need a key to enter this room.\n")
        elif "examine award" in G.input or "examine shelf" in G.input or "examine shelves" in G.input:
            print(
                "\nEach shelf is filled to the brim with various trophies and awards attributed to Elias and his father.\n")
        elif "interact boar" in G.input:
            if "Note: '4'" not in G.inventory:
                print("\nYou lift the boar's head. A note with the letter '4' on it falls out from behind it.\n")
                G.add_to_inventory("Note: '4'")
            elif "Note: '4'" in G.inventory:
                print("\nYou already found a note behind the boar's head. \nIt read: '4'\n")
        elif "interact lion" in G.input or "interact deer" in G.input or "interact wolf" in G.input:
            print("\nThere is nothing odd about this hunting trophy.\n")
        elif "quit" in G.input:
            G.save_game()
            stop_all = True
            break
        else:
            print("\nInvalid input, try 'to upper library' or 'interact deer head'.\n")

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
                print(
                    "The beds are neatly made and devoid of personal objects, apart from a note you find tucked under a pillow that reads: \n'I will not die here. If you read this, Jane, I love you.'\n")
                G.add_to_inventory("Note: 'I will not die here. If you read this, Jane, I love you.'")
            elif "Note: 'I will not die here. If you read this, Jane, I love you.'" in G.inventory:
                print(
                    "This is where you found the note that read: 'I will not die here. If you read this, Jane, I love you.'\n")
        elif "examine dresser" in G.input:
            if "Jane's Locket" not in G.inventory:
                print(
                    "\nThe dressers are packed tight with servants' clothes and some jewelry. \nYou do find an old locket of what looks like a young child. Engraved 'Jane.'\n")
                G.add_to_inventory("Jane's Locket")
            elif "Jane's Locket" in G.inventory:
                print("\nThe dressers are packed tight with servants' clothes and some jewelry. \n")
        elif "examine bathroom" in G.input:
            if "Servant Question" not in G.interactions:
                G.clear_screen()
                print(
                    "As you walk towards the bathroom, towards the running water, you realize you can hear what sounds almost like, weeping… \n\n\nYou cautiously approach the door, and begin to turn the handle. \n\n\nThe water stops running. \n\n\nYou freeze, and right as you open your mouth to speak, the door slams open. You stumble backwards, and a woman stands in front of you. \nShe wears a traditional maid’s garb, with a bandage haphazardly wrapped around her arm, blood leaking through. \nHer eyes are sunken and bloodshot from tears, and she stands meekly, shaking with fear.\n\n\nShe Speaks: 'J-J-Jane? No. Who are you? What are you doing here… how did you get here…'\n")
                print("PRESS ENTER TO PROCEED\n")
                input()
                G.clear_screen()
                print(
                    "You begin to ask what she means, but before you can say anything she cuts you off… \n'No. Nonononononono. You have to leave. Only we remain. Me and Jane. Only us. Everybody else left. \nWho are you? Tell me… Who are you!'\n")
                print("PRESS ENTER TO PROCEED\n")
                input()
                G.clear_screen()
                print("'I am {}, who are you? What is going on here?'\n".format(S.name))
                print("PRESS ENTER TO PROCEED\n")
                input()
                G.clear_screen()
                servant_dialog()
                print("\n")
                servant_dialog()
                print("PRESS ENTER TO PROCEED\n")
                input()
                G.clear_screen()
                G.add_to_interactions("Servant Question")
                print(
                    "The woman braces to answer another question. \nSuddenly, her face turns white, the color draining from her face. \nHer eyes roll back, and she begins to cough. She drops to the floor, and begins to gasp and wheeze. \nShe claws at the ground, then at her throat, as blood gurgles out. Her eyes, her mouth, her ears, you watch as blood begins to seep out like puss to a wound. \nYou stumble back, horrified, as she begins to convulse, and her body begins to wither and scrunch in front of you. \nYou turn tail and run out the door, sprinting towards the trophy room, and as you do so, you hear the snap of bones, the crunching and squelching of muscles, and a strange clicking. \nWhen you peek back into the room, the woman is gone. \nInstead, a single finger seems to grow out of the floor where she stood, three mushrooms surround it.\n")
                print(
                    "You feel sick… \nIt takes everything you have to resolve yourself… Maybe you were just seeing things… This is all a dream… It has to be… \nEither way, you must find Elias. \nHe must have an explanation for all of this, right?\n")
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
                print(
                    "\nThis is where that girl Jane's mother told you some valuable information. \nThat is, before she died in front of you.\n")
        elif "quit" in G.input:
            G.save_game()
            stop_all = True
            break
        else:
            print("\nInvalid input, try 'examine bathroom' or 'examine dresser'.\n")

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
        elif "examine left" in G.input:
            print(
                "\nAlong the left shelves, you notice a couple of family journals poking out from the book rack titled: 'Hemlocke',\n'Silas Finch: a Biography', and 'Finch Manor Mysteries'.\n")
        elif "examine right" in G.input:
            print(
                "\nOddly, the right shelves seem empty compared to the rest, apart from around two dozen books. \nAmong them, two pique your interest:\nA blank book with a solid red cover, and one titled 'Numquam Mori' in what seems like a dirtier, scrawling version of Elias's handwriting.\n")
        elif "examine couch" in G.input or "examine balcony" in G.input:
            # May include a new character here in later versions or in later personal projects/DLCs
            print(
                "\nNothing seems out of the ordinary for the couch and balcony except for a few mushroom spores growing out of the floor nearby.\n")
        elif "interact hemlocke" in G.input:
            print(
                "\nYou thumb through the book. It seems to be about the nature of the poisonous plant, Hemlock, reading: \n'Most of the time, hemlock is only poisonous if ingested. However, you should still be careful when handling poison hemlock. In people with sensitive skin, dermatitis can develop.' \nAs you shut the book, you notice a small mark on your skin. \nYou do a double take, and it is gone...\n\n\nYou find it odd the book is named incorrectly compared to the plant.\n")
        elif "interact silas" in G.input or "interact biography" in G.input:
            print(
                "\nOddly, most of the pages of the book are inked out, but the couple you take note of read about Silas pioneering his family's genetic research, how he wishes his son would inherit it, and one even mentions you, and how glad he is that you met his son’s acquaintance.\n")
        elif "interact finch" in G.input or "interact manor" in G.input:
            print(
                "\nYou flip through the pages, most are about the construction of the house, and a particular spot you take interest in is one describing the basement which has been torn out but there is a clear spot for it.\n")
        elif "interact blank" in G.input or "interact red" in G.input:
            print(
                "\nYou open the blank book and… Nothing. Every single page is blank, except for the last. With four simple words printed right in the center: 'I did not die'.\n")
        elif "interact numquam" in G.input or "interact mori" in G.input or "interact rewritten" in G.input:
            print(
                "\nAs you search through the contents of the book, although mostly in Latin you find a small entry in the margins, written in scrawled english: 'The side effects may be unpleasant, but so far, I have succeeded in my primary goal.\n I know it is forbidden, but human subjects are what I need.'\n")
        elif "quit" in G.input:
            G.save_game()
            stop_all = True
            break
        else:
            print("\nInvalid input, try 'examine left shelves' or 'to trophy room'.")

    while G.currentRoom == "Long Hallway":
        if G.roomEntryCounts['Long Hallway'] == 1:
            G.user_input()
            if "examine book" in G.input:
                print(
                    "\nThe book is open to a page which reads:\n   'I see him now, the firstborn of my arrogance. What was meant to surpass death has birthed a godless mockery of life. \n   The servant… I cannot even recall his name. He was so eager to assist, so willing to become. \n   Now he is more shadow than man, his form broken, reshaped by my hubris. His arms, stretched and blackened, \ncarve reality as though the walls themselves obey his will.\n   His face... oh, God, his face… Crushed, leaking, alive in defiance of all reason.' \n   - Dr. Finch\n")
            elif "examine painting" in G.input:
                print(
                    "\nThis painting is very similar to the first one you saw, only, it shows two people now.\nThe other, a beautiful woman, must have been Silas' wife.\n")
            elif "to 1st room" in G.input:
                if G.roomEntryCounts['Mystery Room'] == 0:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "You enter what seems to be a spare bedroom. \nIt is small and unadorned, its pale stone walls bare except for a single, crooked picture frame. \nA simple wardrobe leans against one wall, a twin bed rests against another, its blanket neatly folded but faded with age. \nThe wooden floor shows signs of wear, with scratches hinting at furniture once rearranged.\nA single window with thin, yellowed curtains lets in a sliver of pale moonlight. \nThe room seems to be filled with a pale yellow mist, what seem like particles of dust floating around the room.\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts['Mystery Room'] == 1:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom is dim, with a heavy, oppressive atmosphere. \nThe walls are painted a dull, peeling green, and mushrooms pop out at odd angles, spewing a deep red gas when you get too close. \nThe bed, larger than the one in the other room, is covered in a faded quilt, its edges worn from years of use, \nand its top covered in a thin layer of red mold. The wooden floor creaks underfoot, and the only light comes from a small, dusty lamp on a bedside table. \nA single, cracked window looks out into the night, the faintest moonlight spilling in. \nSomething is very wrong...\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts['Mystery Room'] == 2:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom feels alive, pulsing with an eerie, unnatural energy. \nFungal growths carpet the floors and climb the walls, their spongy surfaces slick with moisture. \nPatches of bioluminescent mushrooms emit a faint, sickly green glow, casting shifting shadows across the room. \nHemlock plants grow from the cracks in the floorboards, and invade a nearby dresser. \nTheir delicate leaves brush against your shoes as you walk. \nItems inexplicably float in the air, emerging from an open chest at the end of a bed. \nThe items spin slowly as if caught in an unseen current. \nThe atmosphere hums with a faint, low vibration, and the air is heavy with the earthy, acrid scent of decay and poison. \nYou feel sick... \nWhat has he done? How has he made such a monster...\n"
                    G.proceed("Mystery Room")
            elif "to 2nd room" in G.input:
                if G.roomEntryCounts['Mystery Room'] == 0:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "You enter what seems to be a spare bedroom. \nIt is small and unadorned, its pale stone walls bare except for a single, crooked picture frame. \nA simple wardrobe leans against one wall, a twin bed rests against another, its blanket neatly folded but faded with age. \nThe wooden floor shows signs of wear, with scratches hinting at furniture once rearranged. A single window with thin, yellowed curtains lets in a sliver of pale moonlight. \nThe room seems to be filled with a pale yellow mist, what seem like particles of dust floating around the room.\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts['Mystery Room'] == 1:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom is dim, with a heavy, oppressive atmosphere. \nThe walls are painted a dull, peeling green, and mushrooms pop out at odd angles, spewing a deep red gas when you get too close. \nThe bed, larger than the one in the other room, is covered in a faded quilt, its edges worn from years of use, and its top covered in a thin layer of red mold. \nThe wooden floor creaks underfoot, and the only light comes from a small, dusty lamp on a bedside table. \nA single, cracked window looks out into the night, the faintest moonlight spilling in. \nSomething is very wrong...\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts['Mystery Room'] == 2:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom feels alive, pulsing with an eerie, unnatural energy. \nFungal growths carpet the floors and climb the walls, their spongy surfaces slick with moisture. \nPatches of bioluminescent mushrooms emit a faint, sickly green glow, casting shifting shadows across the room. \nHemlock plants grow from the cracks in the floorboards, and invade a nearby dresser. \nTheir delicate leaves brush against your shoes as you walk. \nItems inexplicably float in the air, emerging from an open chest at the end of a bed. \nThe items spin slowly as if caught in an unseen current. \nThe atmosphere hums with a faint, low vibration, and the air is heavy with the earthy, acrid scent of decay and poison. \nYou feel sick... \nWhat has he done? How has he made such a monster...\n"
                    G.proceed("Mystery Room")
            elif "to 3rd room" in G.input:
                if G.roomEntryCounts['Mystery Room'] == 0:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "You enter what seems to be a spare bedroom. \nIt is small and unadorned, its pale stone walls bare except for a single, crooked picture frame. \nA simple wardrobe leans against one wall, a twin bed rests against another, its blanket neatly folded but faded with age. \nThe wooden floor shows signs of wear, with scratches hinting at furniture once rearranged. A single window with thin, yellowed curtains lets in a sliver of pale moonlight. \nThe room seems to be filled with a pale yellow mist, what seem like particles of dust floating around the room.\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts['Mystery Room'] == 1:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom is dim, with a heavy, oppressive atmosphere. \nThe walls are painted a dull, peeling green, and mushrooms pop out at odd angles, spewing a deep red gas when you get too close. \nThe bed, larger than the one in the other room, is covered in a faded quilt, its edges worn from years of use, and its top covered in a thin layer of red mold. \nThe wooden floor creaks underfoot, and the only light comes from a small, dusty lamp on a bedside table. \nA single, cracked window looks out into the night, the faintest moonlight spilling in. \nSomething is very wrong...\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts['Mystery Room'] == 2:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom feels alive, pulsing with an eerie, unnatural energy. \nFungal growths carpet the floors and climb the walls, their spongy surfaces slick with moisture. \nPatches of bioluminescent mushrooms emit a faint, sickly green glow, casting shifting shadows across the room. \nHemlock plants grow from the cracks in the floorboards, and invade a nearby dresser. \nTheir delicate leaves brush against your shoes as you walk. \nItems inexplicably float in the air, emerging from an open chest at the end of a bed. \nThe items spin slowly as if caught in an unseen current. \nThe atmosphere hums with a faint, low vibration, and the air is heavy with the earthy, acrid scent of decay and poison. \nYou feel sick... \nWhat has he done? How has he made such a monster...\n"
                    G.proceed("Mystery Room")
            elif "back" in G.input or "to upper" in G.input or "to landing" in G.input:
                print("\nThe door you once came from is locked. \nHow could that be?\n")
            elif "quit" in G.input:
                G.save_game()
                stop_all = True
                break
            else:
                print("\nInvalid input, try 'examine book' or 'to 1st room'.\n")
        elif G.roomEntryCounts['Long Hallway'] == 2:
            G.user_input()
            if "examine book" in G.input:
                print(
                    "\nThe book is now open to a new page:\n    'Fungus blooms where thought should dwell. Hemlock, the plant of death, sprouts from his ruined skull as if to mock my ambitions. \n   The air rots in his wake, thick with the stench of decay. He drags his twisted claws along the walls,\nand with each motion, something unspeakable is birthed: \n   masses of limbs, pulsing fungi, blood made flesh. His creations writhe in agony, yet they live. They serve.' \n   - Dr. Finch\n")
            elif "to 1st room" in G.input:
                if G.roomEntryCounts['Mystery Room'] == 0:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "You enter what seems to be a spare bedroom. \nIt is small and unadorned, its pale stone walls bare except for a single, crooked picture frame. \nA simple wardrobe leans against one wall, a twin bed rests against another, its blanket neatly folded but faded with age. \nThe wooden floor shows signs of wear, with scratches hinting at furniture once rearranged. A single window with thin, yellowed curtains lets in a sliver of pale moonlight. \nThe room seems to be filled with a pale yellow mist, what seem like particles of dust floating around the room.\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts['Mystery Room'] == 1:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom is dim, with a heavy, oppressive atmosphere. \nThe walls are painted a dull, peeling green, and mushrooms pop out at odd angles, spewing a deep red gas when you get too close. \nThe bed, larger than the one in the other room, is covered in a faded quilt, its edges worn from years of use, and its top covered in a thin layer of red mold. \nThe wooden floor creaks underfoot, and the only light comes from a small, dusty lamp on a bedside table. \nA single, cracked window looks out into the night, the faintest moonlight spilling in. \nSomething is very wrong...\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts['Mystery Room'] == 2:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom feels alive, pulsing with an eerie, unnatural energy. \nFungal growths carpet the floors and climb the walls, their spongy surfaces slick with moisture. \nPatches of bioluminescent mushrooms emit a faint, sickly green glow, casting shifting shadows across the room. \nHemlock plants grow from the cracks in the floorboards, and invade a nearby dresser. \nTheir delicate leaves brush against your shoes as you walk. \nItems inexplicably float in the air, emerging from an open chest at the end of a bed. \nThe items spin slowly as if caught in an unseen current. \nThe atmosphere hums with a faint, low vibration, and the air is heavy with the earthy, acrid scent of decay and poison. \nYou feel sick... \nWhat has he done? How has he made such a monster...\n"
                    G.proceed("Mystery Room")
            elif "to 2nd room" in G.input:
                if G.roomEntryCounts['Mystery Room'] == 0:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "You enter what seems to be a spare bedroom. \nIt is small and unadorned, its pale stone walls bare except for a single, crooked picture frame. \nA simple wardrobe leans against one wall, a twin bed rests against another, its blanket neatly folded but faded with age. \nThe wooden floor shows signs of wear, with scratches hinting at furniture once rearranged. A single window with thin, yellowed curtains lets in a sliver of pale moonlight. \nThe room seems to be filled with a pale yellow mist, what seem like particles of dust floating around the room.\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts['Mystery Room'] == 1:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom is dim, with a heavy, oppressive atmosphere. \nThe walls are painted a dull, peeling green, and mushrooms pop out at odd angles, spewing a deep red gas when you get too close. \nThe bed, larger than the one in the other room, is covered in a faded quilt, its edges worn from years of use, and its top covered in a thin layer of red mold. \nThe wooden floor creaks underfoot, and the only light comes from a small, dusty lamp on a bedside table. \nA single, cracked window looks out into the night, the faintest moonlight spilling in. \nSomething is very wrong...\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts['Mystery Room'] == 2:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom feels alive, pulsing with an eerie, unnatural energy. \nFungal growths carpet the floors and climb the walls, their spongy surfaces slick with moisture. \nPatches of bioluminescent mushrooms emit a faint, sickly green glow, casting shifting shadows across the room. \nHemlock plants grow from the cracks in the floorboards, and invade a nearby dresser. \nTheir delicate leaves brush against your shoes as you walk. \nItems inexplicably float in the air, emerging from an open chest at the end of a bed. \nThe items spin slowly as if caught in an unseen current. \nThe atmosphere hums with a faint, low vibration, and the air is heavy with the earthy, acrid scent of decay and poison. \nYou feel sick... \nWhat has he done? How has he made such a monster...\n"
                    G.proceed("Mystery Room")
            elif "to 3rd room" in G.input:
                if G.roomEntryCounts['Mystery Room'] == 0:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "You enter what seems to be a spare bedroom. \nIt is small and unadorned, its pale stone walls bare except for a single, crooked picture frame. \nA simple wardrobe leans against one wall, a twin bed rests against another, its blanket neatly folded but faded with age. \nThe wooden floor shows signs of wear, with scratches hinting at furniture once rearranged. A single window with thin, yellowed curtains lets in a sliver of pale moonlight. \nThe room seems to be filled with a pale yellow mist, what seem like particles of dust floating around the room.\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts['Mystery Room'] == 1:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom is dim, with a heavy, oppressive atmosphere. \nThe walls are painted a dull, peeling green, and mushrooms pop out at odd angles, spewing a deep red gas when you get too close. \nThe bed, larger than the one in the other room, is covered in a faded quilt, its edges worn from years of use, and its top covered in a thin layer of red mold. \nThe wooden floor creaks underfoot, and the only light comes from a small, dusty lamp on a bedside table. \nA single, cracked window looks out into the night, the faintest moonlight spilling in. \nSomething is very wrong...\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts['Mystery Room'] == 2:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom feels alive, pulsing with an eerie, unnatural energy. \nFungal growths carpet the floors and climb the walls, their spongy surfaces slick with moisture. \nPatches of bioluminescent mushrooms emit a faint, sickly green glow, casting shifting shadows across the room. \nHemlock plants grow from the cracks in the floorboards, and invade a nearby dresser. \nTheir delicate leaves brush against your shoes as you walk. \nItems inexplicably float in the air, emerging from an open chest at the end of a bed. \nThe items spin slowly as if caught in an unseen current. \nThe atmosphere hums with a faint, low vibration, and the air is heavy with the earthy, acrid scent of decay and poison. \nYou feel sick... \nWhat has he done? How has he made such a monster...\n"
                    G.proceed("Mystery Room")
            elif "back" in G.input or "to upper" in G.input or "to landing" in G.input:
                print("\nThe door you once came from is locked. \nThis keeps getting weirder and weirder...\n")
            elif "quit" in G.input:
                G.save_game()
                stop_all = True
                break
            else:
                print("\nInvalid input, try 'examine book' or 'to 2nd room'.\n")
        elif G.roomEntryCounts['Long Hallway'] == 3:
            G.user_input()
            if "examine book" in G.input:
                print(
                    "\nAgain, the page is different:\n   'He moves through the manor like a phantom, reshaping it with every step. \n   Doors appear where none should exist; corridors stretch into infinite darkness. \n   I no longer know where I am. \n   He is no longer human, not in any conventional sense, but something remains. Something vast. \n   The servant does not die. Not in the way we understand death. \n   He suffers, yes, his form a grotesque distortion, but it endures, it survives. \n   How many times have I asked the question: Can we break the chains of mortality? \n   Can we cheat death? \n   Twist it into a new shape? \n   The answer, I see now, is yes.' \n   - Dr. Finch\n")
            elif "to 1st room" in G.input:
                if G.roomEntryCounts['Mystery Room'] == 0:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "You enter what seems to be a spare bedroom. \nIt is small and unadorned, its pale stone walls bare except for a single, crooked picture frame. \nA simple wardrobe leans against one wall, a twin bed rests against another, its blanket neatly folded but faded with age. \nThe wooden floor shows signs of wear, with scratches hinting at furniture once rearranged. A single window with thin, yellowed curtains lets in a sliver of pale moonlight. \nThe room seems to be filled with a pale yellow mist, what seem like particles of dust floating around the room.\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts['Mystery Room'] == 1:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom is dim, with a heavy, oppressive atmosphere. \nThe walls are painted a dull, peeling green, and mushrooms pop out at odd angles, spewing a deep red gas when you get too close. \nThe bed, larger than the one in the other room, is covered in a faded quilt, its edges worn from years of use, and its top covered in a thin layer of red mold. \nThe wooden floor creaks underfoot, and the only light comes from a small, dusty lamp on a bedside table. \nA single, cracked window looks out into the night, the faintest moonlight spilling in. \nSomething is very wrong...\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts['Mystery Room'] == 2:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom feels alive, pulsing with an eerie, unnatural energy. \nFungal growths carpet the floors and climb the walls, their spongy surfaces slick with moisture. \nPatches of bioluminescent mushrooms emit a faint, sickly green glow, casting shifting shadows across the room. \nHemlock plants grow from the cracks in the floorboards, and invade a nearby dresser. \nTheir delicate leaves brush against your shoes as you walk. \nItems inexplicably float in the air, emerging from an open chest at the end of a bed. \nThe items spin slowly as if caught in an unseen current. \nThe atmosphere hums with a faint, low vibration, and the air is heavy with the earthy, acrid scent of decay and poison. \nYou feel sick... \nWhat has he done? How has he made such a monster...\n"
                    G.proceed("Mystery Room")
            elif "to 2nd room" in G.input:
                if G.roomEntryCounts['Mystery Room'] == 0:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "You enter what seems to be a spare bedroom. \nIt is small and unadorned, its pale stone walls bare except for a single, crooked picture frame. \nA simple wardrobe leans against one wall, a twin bed rests against another, its blanket neatly folded but faded with age. \nThe wooden floor shows signs of wear, with scratches hinting at furniture once rearranged. A single window with thin, yellowed curtains lets in a sliver of pale moonlight. \nThe room seems to be filled with a pale yellow mist, what seem like particles of dust floating around the room.\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts['Mystery Room'] == 1:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom is dim, with a heavy, oppressive atmosphere. \nThe walls are painted a dull, peeling green, and mushrooms pop out at odd angles, spewing a deep red gas when you get too close. \nThe bed, larger than the one in the other room, is covered in a faded quilt, its edges worn from years of use, and its top covered in a thin layer of red mold. \nThe wooden floor creaks underfoot, and the only light comes from a small, dusty lamp on a bedside table. \nA single, cracked window looks out into the night, the faintest moonlight spilling in. \nSomething is very wrong...\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts['Mystery Room'] == 2:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom feels alive, pulsing with an eerie, unnatural energy. \nFungal growths carpet the floors and climb the walls, their spongy surfaces slick with moisture. \nPatches of bioluminescent mushrooms emit a faint, sickly green glow, casting shifting shadows across the room. \nHemlock plants grow from the cracks in the floorboards, and invade a nearby dresser. \nTheir delicate leaves brush against your shoes as you walk. \nItems inexplicably float in the air, emerging from an open chest at the end of a bed. \nThe items spin slowly as if caught in an unseen current. \nThe atmosphere hums with a faint, low vibration, and the air is heavy with the earthy, acrid scent of decay and poison. \nYou feel sick... \nWhat has he done? How has he made such a monster...\n"
                    G.proceed("Mystery Room")
            elif "to 3rd room" in G.input:
                if G.roomEntryCounts['Mystery Room'] == 0:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "You enter what seems to be a spare bedroom. \nIt is small and unadorned, its pale stone walls bare except for a single, crooked picture frame. \nA simple wardrobe leans against one wall, a twin bed rests against another, its blanket neatly folded but faded with age. \nThe wooden floor shows signs of wear, with scratches hinting at furniture once rearranged. A single window with thin, yellowed curtains lets in a sliver of pale moonlight. \nThe room seems to be filled with a pale yellow mist, what seem like particles of dust floating around the room.\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts['Mystery Room'] == 1:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom is dim, with a heavy, oppressive atmosphere. \nThe walls are painted a dull, peeling green, and mushrooms pop out at odd angles, spewing a deep red gas when you get too close. \nThe bed, larger than the one in the other room, is covered in a faded quilt, its edges worn from years of use, and its top covered in a thin layer of red mold. \nThe wooden floor creaks underfoot, and the only light comes from a small, dusty lamp on a bedside table. \nA single, cracked window looks out into the night, the faintest moonlight spilling in. \nSomething is very wrong...\n"
                    G.proceed("Mystery Room")
                elif G.roomEntryCounts['Mystery Room'] == 2:
                    G.clear_screen()
                    C.tell_commands()
                    G.roomDescribe = "This bedroom feels alive, pulsing with an eerie, unnatural energy. \nFungal growths carpet the floors and climb the walls, their spongy surfaces slick with moisture. \nPatches of bioluminescent mushrooms emit a faint, sickly green glow, casting shifting shadows across the room. \nHemlock plants grow from the cracks in the floorboards, and invade a nearby dresser. \nTheir delicate leaves brush against your shoes as you walk. \nItems inexplicably float in the air, emerging from an open chest at the end of a bed. \nThe items spin slowly as if caught in an unseen current. \nThe atmosphere hums with a faint, low vibration, and the air is heavy with the earthy, acrid scent of decay and poison. \nYou feel sick... \nWhat has he done? How has he made such a monster...\n"
                    G.proceed("Mystery Room")
            elif "back" in G.input or "to upper" in G.input or "to landing" in G.input:
                print("\nThe door you once came from is locked. \nYou must escape this hallway at some point.\n")
            elif "quit" in G.input:
                G.save_game()
                stop_all = True
                break
            else:
                print("\nInvalid input, try 'examine book' or 'to 3rd room'.\n")
        elif G.roomEntryCounts['Long Hallway'] == 4:
            print("\nThe book beckons you toward it now.\n")
            print("PRESS ENTER TO PROCEED\n")
            input()
            G.clear_screen()
            print(
                "\nYou reach out to it, hemlock scaling against your hand as you grab it to read. \nNow the book flies through pages, which all read the same lines: \n\n   'Elias. My son. My blood. \n   He is young, strong, untainted by the ravages of time or the imperfections that plague older subjects. \n   His genetic makeup is ideal. \n   A pristine canvas for the masterpiece I am destined to create. \n   He does not understand the magnitude of my work, the legacy I am building. \n   But he will. In time, he will see that this is not cruelty but destiny. \n   To experiment on him is not to harm, it is to grant him the gift of eternity. \n   He will resist, of course. He is his mother’s son, too bound to sentiment and fear. \n   But once the procedure is complete, he will thank me. \n   They all will. \n   Silas will be my proof, my triumph, the ultimate symbol of life perfected. \n   He will carry the weight of my ambition, as any worthy heir should.' \n   - Dr. Finch\n\n\n")
            print("PRESS ENTER TO PROCEED\n")
            input()
            G.clear_screen()
            print(
                "\nA realization dawns upon you as you close the journal shut. \nYou look towards the cover as it seems to twist and morph, now reading simply a name: 'Dr. Silas Finch' \n\n\nThe walls stretch and twist unnaturally, and the once-numbered doors have multiplied into a maddening array of infinite options. \nSome flicker in and out of existence, their frames weeping viscous, red fluid. \nA cold wind brushes against your skin, despite there being no source, and a low, resonant, moan hum seems to emanate from the very bones of the manor.\n")
            print("PRESS ENTER TO PROCEED\n")
            input()
            G.clear_screen()
            print(
                "\nSuddenly, a familiar faint clicking sound emanates, louder and more erratic. \nFrom the depths of the hallway's infinite shadows, he emerges. \n\n\nThe servant steps forward, his disjointed frame jerking with each motion. \nHis jagged, blackened fingers scrape against the walls as he moves, carving deep, pulsing gouges that birth horrific forms. \nFrom the gouges spill grotesque amalgamations: limbs twisting unnaturally, fungi blooming in vibrant but sickening colors, and patches of flesh that writhe and pulsate with grotesque vitality. \n\n\nAs his claws drag, the hallway reacts violently. \nWalls convulse and bulge outward as if struggling to contain the abominations growing within. \nFungal blooms burst open, spilling a mix of spores and slick, crimson ichor onto the ground. \nThe air feels thicker, each breath burning your lungs and leaving your mind hazy with dread.\n")
            print("PRESS ENTER TO PROCEED\n")
            input()
            G.clear_screen()
            print(
                "\nThe servant’s single, sagging eye fixates on you, his grotesque, dislocated mouth parting to emit a guttural, wet click that echoes through the hall, bouncing endlessly as if the manor itself mocks your fear.\n\n\nThe hallway stretches and multiplies, rooms appearing without reason or pattern. \nTheir doors twist and shift, never settling, each one promising horrors untold. \nAnd with a jerk so quick, the servant appears in front of you, head to head with you. \nHis face, you see now, pale and gaunt, barely human. \nHis jaw, dislocated on the right, with hemlock vines snapping it shut as it droops, producing a sharp click. \nHis eye, still moving and twitching, despite hanging out of its socket. \nHis brain, held in place by his open skull like a goblet, shrived and blackened, with strange fungal growths spiraling out.")
            print("PRESS ENTER TO PROCEED\n")
            input()
            G.clear_screen()
            print(
                "\nThe servant lunges forward, its movements a grotesque blur of jagged angles and unnatural speed. \nHis blackened claws scrape against the pulsating walls, sending cascades of blood and fungal spores into the air. \nThe walls themselves seem to writhe in response, opening grotesque mouths and clawing appendages that snap and writhe at you as you flee. \nThe servant’s wet, clicking groan reverberates through the hallway, its distorted cadence growing louder with every step. \nHis dislocated mouth twists into a grotesque frown as he slams his claws into the ground, sending tremors rippling beneath your feet. \nThe floor cracks open, revealing glimpses of writhing masses of flesh and limbs below, threatening to swallow you whole.")
            print("PRESS ENTER TO PROCEED\n")
            input()
            G.clear_screen()
            monster_encounter()

    while G.currentRoom == "Mystery Room":
        if G.roomEntryCounts['Mystery Room'] == 1:
            G.user_input()
            if "to hallway" in G.input:
                G.clear_screen()
                C.tell_commands()
                G.roomDescribe = "You step back into the dimly lit hallway. \nBut it is different, instead of dust, the air is thick with a purple miasma, and the smell of rot fills the air. \nStrange fungi grow out of the cracked stone walls, and the flickering lantern has been replaced by a torch that casts no shadows. \nAtop the table is only the book. \n\n\nThere is a door at the end of the hall to the upper landing and three doorways line the wall, numbered 1, 2, and 3 including the one you just came from."
                G.proceed("Long Hallway")
            elif "examine bed" in G.input:
                print(
                    "\nThe bed is a light pink contrasting the deep red of the master bedroom. \nIt brings a life to the manor that wasn't there before...\n")
            elif "examine wardrobe" in G.input:
                if "Alyssia's Note" not in G.inventory:
                    print(
                        "\nA tall, narrow wardrobe stands in the corner. \nIts door is slightly ajar, revealing glimpse of moth-eaten clothing within. \nInside the pocket of an old blouse, you find a note that reads: \n\n\n   'I’ve watched Elias change.\n   He used to be so full of life, full of love, but now he is consumed by his obsession. \n   The spark in his eyes has dimmed, replaced by a coldness that I can’t reach. \n   He’s lost in his research, in his pursuit of something that might not even be possible.' \n   - Alyssia Finch\n")
                    G.add_to_inventory("Alyssia's Note")
                elif "Alyssia's Note" in G.inventory:
                    print("\nThis is where you found the note from Alyssia.")
            elif "examine picture" in G.input:
                print(
                    "\nHanging slightly askew on the wall, the frame contains a black-and-white photograph of an unfamiliar family. \nThe glass is cracked, distorting their faces. You can just make out the face of who must be Silas's wife, Alyssia Finch. \nShe must have moved into this room a while before then...")
            elif "quit" in G.input:
                G.save_game()
                stop_all = True
                break
            else:
                print("\nInvalid input, try 'examine wardrobe' or 'to hallway'.\n")
        elif G.roomEntryCounts['Mystery Room'] == 2:
            G.user_input()
            if "to hallway" in G.input:
                G.clear_screen()
                C.tell_commands()
                G.roomDescribe = "You step into the hallway again. \nThe air is still thick with that purple miasma, rot still permeates your nose, and fungus still sprouts from the walls. \nBut this time, there is no lantern or torch, yet you can see into the room perfectly. \nThere is no table this time, only the book, suspended, floating in the air. \nIndecipherable whispers and clicking sounds pierces your thoughts. \nIt makes your head ache. \nThe air seems heavier here, and something writhes just beneath the floorboards. \nYou wonder just how grave the consequences of Elias’s actions may become. \n\n\nThe door to the upper landing is at the far end of the hall and three doorways line the wall, numbered 1, 2, and 3 including the one you came from.\n"
                G.proceed("Long Hallway")
            elif "examine bed" in G.input:
                if "Red Spores" not in G.interactions:
                    print(
                        "\nYou start to rifle through the sheets, but as you touch the red mold, it seems to stick to your fingers. \nAs you brush your hands on your shirt, mushrooms start to grow out of the dust on your shirt. \nThey begin spewing a gross red gas, making you feel woozy. \nAfter a few seconds, they fade, melting into a red substance that stains your clothing.\n")
                    G.add_to_interactions("Red Spores")
                elif "Red Spores" in G.interactions:
                    print("\nYou refuse to touch those sheets again.\n")
            elif "examine window" in G.input:
                if "Window Note" not in G.inventory:
                    print(
                        "\nYou approach the window, as you do, you notice a mirror next to the bedside you never saw before. \nOn the windowsill, is a note that reads: \n   'My father’s obsession consumes him, leaving little room for reason. \n   I’ve seen the fear in his eyes, hidden behind a mask of triumph. \n   He calls it 'progress,' but at what cost? \n   The whispers he dismisses as echoes are unnatural, chilling. \n   He’s tampering with forces beyond comprehension, \n   and I fear he’s unraveling not just the code of life but the fragile boundary between man and monstrosity.'\n - Elias Finch\n")
                elif "Window Note" in G.inventory:
                    print("\nThis is where you found the note from Elias.\n")
            elif "examine mirror" in G.input:
                if "Mirror Mirror" not in G.interactions:
                    print(
                        "\nA large, ornate mirror sits next to the bedside, its frame intricately carved with floral patterns. \nThe glass is slightly cloudy, and when you look closely, you notice the reflection appears a few seconds delayed. \nAs you explore this phenomenon, the air begins to thicken, heavy with the stench of decay. \nA faint, wet clicking sound echoes, and from the debts of the mirror, a grotesque figure emerges.\n\n\nIt looks like a man in old servant's garb, yet his arms and fingers are blackened and sharpened to a point. \nHis head seems to have been bashed in, as his skin hangs off his skull. \nOne of his eyes is missing, the other hanging out of its socket. \nHis mouth has been dislocated, and his brain is poking out of his skull. \nA gross myriad of fungi and hemlock flowers grow out of his head and swirl out of his flash.\n\n\nHis single hanging eye focuses on you as a distorted, clicking groan escapes his dislocated mouth. \nThe room warps unnaturally, stretching and twisting as if responding to his presence. \nHe vanishes into the shadows before you can react, leaving the room eerily still.\n\n\nOddly, you do not feel afraid...\n")
                    G.add_to_interactions("Mirror Mirror")
                elif "Mirror Mirror" in G.interactions:
                    print("\nThis is where you had the encounter with that creature.\n")
            elif "quit" in G.input:
                G.save_game()
                stop_all = True
                break
            else:
                print("\nInvalid input, try 'examine bed' or 'to hallway'.\n")
        elif G.roomEntryCounts['Mystery Room'] == 3:
            G.user_input()
            if "to hallway" in G.input:
                G.clear_screen()
                C.tell_commands()
                G.roomDescribe = "You step into the hallway once more, but it is no longer recognizable. \nThe air is suffocating, filled with the choking, acrid stench of decay. \nThe floor beneath you pulses as if alive, each step met with the sickening squelch of flesh-like growths. \nThe table is still gone, and the book still floats, surrounded by a wreath of constricting hemlock. \nAs you near, whispers crawl into your mind, overlapping and indecipherable, their tone desperate yet commanding.\n"
                G.proceed("Long Hallway")
            elif "examine bed" in G.input:
                if "Muscle Bed" not in G.interactions:
                    print(
                        "\nThe bed appears deceptively normal at first glance... \nA weathered wooden frame with a tattered mattress and a thin blanket draped haphazardly over it. \nHowever, the wood seems oddly textured, its surface marked with vein-like patterns that pulse faintly in the dim light. \nYou reach out to rifle through the sheet, and that's when the transformation begins. \nWith a sickening creak, the wooden frame splinters and shifts, twisting into fleshy, jointed limbs that writhe and claw at the air. \nThe mattress sinks and folds in on itself, revealing sinewy muscle-like strands beneath the fabric. \nThe blanket slithers to the floor like discarded skin, leaving behind a grotesque, living construct of squirming arms and legs, twitching in unison. \nThen, before your very eyes, the bed begins to bleed, and along with it, the walls. \nAn eerie, clicking hum befalls the room, and there is something almost calming about it...\n")
                    G.add_to_interactions("Muscle Bed")
                elif "Muscle Bed" in G.interactions:
                    print("\nThe bed is normal looking once again, but has blood red sheets.\n")
            elif "examine dresser" in G.input:
                if "Warped Dresser" not in G.interactions:
                    print(
                        "\nThis warped piece of furniture seems to have grown from the floor itself, its drawers tangled with vines and bristling with toxic foliage. \nA faint rustling comes from inside, as if something is moving. \nWhen you open it, a purple mist rushes past you, sending you into a fit of coughing. \nOnce you recover, you swear you can see the servant, its body  sagging, its plant-infested form barely visible in the dim light. \nHis head tilted unnaturally as if observing you. \nBut when you blink, with the creaking of strained flesh, he is gone. \nA fragment of the past, of which does not concern as much as it should.\n")
                    G.add_to_interactions("Warped Dresser")
                elif "Warped Dresser" in G.interactions:
                    print("\nThe dresser, much like the thing you saw, has vanished.\n")
            elif "examine chest" in G.input:
                if "Flying Chest" not in G.interactions:
                    print(
                        "\nThe chest is made of dark, warped wood, with iron bands corroded by time and strange stains seeping into the grain. \nIts surface is adorned with carved symbols that seem to shift subtly. \nThe air around it feels colder, and faint whispers can be heard when you draw close. \nThe lid is ajar, and items such as pens, paper, and other trinkets fly out. \nAlongside these items is a note, when you snatch it from the air, the rest of the items clatter to the floor with an unnerving echo.\nThe note reads: \n   'I have faced death once before, stood on the precipice and stared into its abyss. \n   It was then that I made my choice. \n   To wrest my existence back from its cold, unyielding grip. \n   That day, I proved it could be done. I became more than man; I became the master of my own fate. \n   The world fears death, yet I stand as proof that it can be beaten. \n   I will do it again, not just for myself but for humanity. No one should fear the darkness I’ve escaped. \n   Immortality is no longer a question of if. It is a question of how far I am willing to go. \n   And I am willing to go as far as it takes.'\n - Dr. Finch \n\nYou wonder just what Elias is talking about...\n")
                    G.add_to_inventory("Floating Note")
                    G.add_to_interactions("Flying Chest")
                elif "Flying Chest" in G.interactions:
                    print(
                        "\nThe chest is shut and doesn't seem to want to budge.\nThe items which were inside now lie on the floor.\nThis is where you found the floating note with words from a Dr. Finch.\n")
            elif "quit" in G.input:
                G.save_game()
                stop_all = True
                break
            else:
                print("\nInvalid input, try 'examine dresser' or 'to hallway'.\n")

    while G.currentRoom == "Supply Closet":
        G.user_input()
        if "back" in G.input or "to kitchen" in G.input:
            G.clear_screen()
            C.tell_commands()
            G.roomDescribe = ""
            G.proceed("Kitchen")
        elif "interact bucket" in G.input or "examine bucket" in G.input or "examine mop" in G.input:
            if "Note: '9'" not in G.inventory:
                print("\nYou look into the bucket holding the mop, and see a slip of note paper. It reads: '9'\n")
                G.add_to_inventory("Note: '9'")
            elif "Note: '9'" in G.inventory:
                print("\nThis is where you found the note that read: '9'.\n")
        elif "examine hatch" in G.input or "interact hatch" in G.input:
            if "Silver Key" in G.inventory:
                G.clear_screen()
                C.tell_commands()
                G.roomDescribe = "You grip the cold metal handle of the basement hatch. \nThe lock clicks with a metallic snap, echoing throughout the quiet room. \nAs you push the heavy hatch open, the hinges groan, the sound cutting through the air like a warning. A rush of damp, musty air greets you, the darkness below seeming to breathe in your hesitation. \nYou descend a rusty ladder, and look before you.\n\n"
                G.proceed("Basement")
            elif "Bronze Key" in G.inventory:
                print("\nYou don't have the right key to open the hatch.\n")
            else:
                print("\nYou will need a key to open the hatch.\n")
        elif "quit" in G.input:
            G.save_game()
            stop_all = True
            break
        else:
            print("\nInvalid input, try 'examine bucket' or 'to kitchen'.\n")

    while G.currentRoom == "Basement":
        G.determine_monster()
        print(
            "\nYou stand in a cramped hallway, and you can hear water dripping in the distance. \nEvery step echos as you walk, reverberating throughout the space. \nYou near a light flickering on your right, and find a cell. \nThe stone walls glisten with moisture, and the room is only illuminated by the dwindling wick of a candle. \nThe floor is uneven, strewn with old straw and the faint smell of mildew. \nA heavy iron door with rusted bars locks the cell. \nNearby, a small wooden bucket sits in the corner, its purpose grimly apparent. \nInside, on a small old cot, you see a little girl.\n\n")
        print("\nYou grab the handle and open the cell, coming face-to-face with the little girl. \nDead...\n\n")
        print("PRESS ENTER TO PROCEED\n")
        input()
        G.clear_screen()
        if "Jane's Locket" in G.inventory:
            print(
                "\nThis must be Jane. \nYou place the locket in her hands, and fold them onto her chest. \nYou close her cold, unblinking eyes, and walk out of the room. \nYou feel numb...\n\n")
            print("PRESS ENTER TO PROCEED\n")
            input()
            G.clear_screen()
            if G.monster == "Chimera":
                print(
                    "\nYou peer into the cell, and it appears a mess. \nStraw is scattered all over, the bed appears burnt and scratched, and the walls are covered in long, thick serrations. \nIn the corner of the room, you see it… \nNot quite animal, not quite human. \nA Chimera, a mismatch of man and monster. \nA dog-like creature with patches of human skin, black leathery scales, and black fur lining its body. \nAcid drips from its mouth, seeming to burn the floor beneath it. \nIt tries to suck in its saliva, but fails, and just ends up gagging and spitting the acid back up. \nIts eyes are sewn shut, but it pricks its ears at you, and sniffs the air. \nIt makes a noise between a strangled cry and a moaning growl.\n\n")
                print(
                    "\nBefore you stands your once friend now the one thing that stands in your only way to freedom and ultimately survival.\n No longer himself he's growling but not out of anger, out of fear, almost like he's trying to scare you away not for his sake but rather yours, he looks at you with a painful plea in his face and slowly approaches you. \n\n")
            elif G.monster == "Silas":
                print(
                    "\nYou peer into the cell, and that's when you see him. \nElias, broken and starved, sits atop a small cot. \nHis face is gaunt, his body thin and frail, and a strange tube pumps chemicals into his wrist. \n'Elias!' you shout, and he turns to you, and offers only but a weak smile. \nYou practically rip the door off its hinges, hoisting him under your shoulder. \n'We have to leave, now!' \nYou begin to walk towards the ladder you entered through, but it is already too late...\n\n")
                print(
                    "\nA roughened up middle aged man with a scrubby face stands in your way.\nWearing a worn out apron covered in various substances, primary blood, with a basic white tee and long khaki pants.\nHe stares you down with hate filled curiosity.\nYou turn over to your beloved friend who seems disoriented and very clearly unwell. \nKnowing that he isn’t going to do much help you grab him and run.\n\n")
        elif "Jane's Locket" not in G.inventory:
            print(
                "\nYou walk up to the little girl, probably once full of life.\nHer eyes stare cold and unfeeling. \nYou close the cell door, and walk out of the room, feeling numb...\n\n")
            print(
                "\nYou press forward, still shaken from the experience, but determined to find your friend. \nTo your left, you approach another light, and dread what you will find.\n\n")
            print("PRESS ENTER TO PROCEED\n")
            input()
            G.clear_screen()
            if G.monster == "Chimera":
                print(
                    "\nYou peer into the cell, and it appears a mess. \nStraw is scattered all over, the bed appears burnt and scratched, and the walls are covered in long, thick serrations. \nIn the corner of the room, you see it… \nNot quite animal, not quite human. \nA Chimera, a mismatch of man and monster. \nA dog-like creature with patches of human skin, black leathery scales, and black fur lining its body. \nAcid drips from its mouth, seeming to burn the floor beneath it. \nIt tries to suck in its saliva, but fails, and just ends up gagging and spitting the acid back up. \nIts eyes are sewn shut, but it pricks its ears at you, and sniffs the air. \nIt makes a noise between a strangled cry and a moaning growl.\n\n")
                print(
                    "\nBefore you stands your once friend now the one thing that stands in your only way to freedom and ultimately survival.\n No longer himself he's growling but not out of anger, out of fear, almost like he's trying to scare you away not for his sake but rather yours, he looks at you with a painful plea in his face and slowly approaches you. \n\n")
            elif G.monster == "Silas":
                print(
                    "\nYou peer into the cell, and that's when you see him. \nElias, broken and starved, sits atop a small cot. \nHis face is gaunt, his body thin and frail, and a strange tube pumps chemicals into his wrist. \n'Elias!' you shout, and he turns to you, and offers only but a weak smile. \nYou practically rip the door off its hinges, hoisting him under your shoulder. \n'We have to leave, now!' \nYou begin to walk towards the ladder you entered through, but it is already too late...\n\n")
                print(
                    "\nA roughened up middle aged man with a scrubby face stands in your way.\nWearing a worn out apron covered in various substances, primary blood, with a basic white tee and long khaki pants.\nHe stares you down with hate filled curiosity.\nYou turn over to your beloved friend who seems disoriented and very clearly unwell. \nKnowing that he isn’t going to do much help you grab him and run.\n\n")
        print("***  Timed sequence approaching  ***\n\n")
        print("***  Type a number to input your response to each prompt  ***\n\n")
        print("PRESS ENTER TO PROCEED\n")
        input()
        print("\n\n\n\n")
        initial_time = 15
        timer = ChaseGame(initial_time)
        timer.start_timer_thread()
        timed_game_decisions(timer)
        stop_all = True
    if stop_all:
        break
