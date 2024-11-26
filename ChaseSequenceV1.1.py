import os
import sys
import threading
import time

#Open in new window
class Terminal:
    def __init__(self, script_name="main.py"):
        self.script_name = script_name
        self.currentRoom = "None"
        self.roomsEntered = [self.currentRoom]
        self.roomEntryCounts = {}
        self.inventory = []
        self.interactions = ["Hedda Gabler Lever"]
        self.input = ""
        self.monster = ""
        self.mop= False
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
        # Update the room entry count
        if room not in self.roomEntryCounts:
            self.roomEntryCounts[room] = 0
        self.roomEntryCounts[room] += 1

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def add_to_interactions(self, interaction):
        self.interactions.append(interaction)

    def get_current_room(self):
        return self.currentRoom

    def get_rooms_entered(self):
        return self.roomsEntered

T = Terminal()  # Create an instance of the Gameloop class
T.open_new_terminal()  # Call the method to open a new terminal
def monster(self):
    if len(T.roomsEntered) >= 70:
        self.monster= "Chimera"
        print("")
    else:
        self.monster = "Silas"
        print("")
    return self.monster

class ChaseGame:
    def __init__(self, start_time): #defining the base for variables
        self.time_left = start_time
        self.is_caught = False
        self.timer_thread = None
        self.lock = threading.Lock()
        self.turns_taken = 0 #based number for turns
        self.monster = ()


    def add_time(self, seconds):
        """Add seconds to the countdown timer."""
        self.time_left += seconds
        print(f"{seconds} seconds added!")

    def subtract_time(self, seconds):
        """Subtract seconds from the countdown timer."""
        self.time_left -= seconds
        if self.time_left < 0:
            self.time_left = 0
        print(f"{seconds} seconds subtracted!")

    def show_time(self):
        """Display the current time left in the chase."""
        mins, secs = divmod(self.time_left, 60)
        print(f"Time left: {mins:02}:{secs:02}", end="\r")

    def start_chase(self):
        """Start the chase sequence."""
        while self.time_left > 0:
            self.show_time()
            self.time.sleep(1)
            self.time_left -= 1
            if self.time_left == 0:
                self.is_caught = True
                break


        if self.is_caught:
            print("You're thrown to the ground", monster, "hovers over you and raises their hand, everything goes black")
        else:
            if monster==("Chimera"):
                print("You run out the front and down the path from which you came,\n"
                      "from the woods you turn to see the front doors totally gone left with a singular wall and a familiar face from the 2nd story window.\n"
                      "you stop catching a breath then continue cautiously down the path")
            else:
                print("You run out the front and down the path from which you came,\n"
                        "from the woods you turn to see the front doors totally gone left with a singular wall and a familiar face from the 2nd story window.\n"
                        "You turn to your friend and smile he returns the smile with a look of relief and you both continue down the path together not ready to let each other go.")

    def start_timer_thread(self):
        """Run the countdown in a separate thread."""
        self.timer_thread = threading.Thread(target=self.start_chase)
        self.timer_thread.daemon = True
        self.timer_thread.start()


def game_decisions(timer, stage=1):
    """Simulate player choices during the chase with evolving options."""
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


if __name__ == "__main__":
    initial_time = 15
    timer = ChaseGame(initial_time)
    timer.start_timer_thread()
    game_decisions(timer)
