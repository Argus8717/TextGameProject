import time
import threading #Allows the time to actively run while the main choices go 


def monster(self):
    if len(T.roomsEntered) >= 70:
        self.monster = ("Chimera")
        print("")
    else:
        self.monster = ("Silas")
        print("")
    return (self.monster)

class ChaseGame:
    def __init__(self, start_time): #defining the base for variables
        self.time_left = start_time
        self.is_caught = False
        self.timer_thread = None
        self.lock = threading.Lock()
        self.turns_taken = 0 #based number for turns

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
            time.sleep(1)
            self.time_left -= 1
            if self.time_left == 0:
                self.is_caught = True
                break

        if self.is_caught:
            print("You're thrown to the ground", monster, "hovers over you and raises their hand, everything goes black")
        else:
            if self.turns_taken ==10:
                print("You fling open the door at the end of the hallway and end up within a graveyard.\n"
                "Still filled with fear you quickly turn around and see the door gone with banging on the other side of the wall.\n"
                "Seeing a familiar face in the second floor window you give a small nod of thanks and go into the surrounding woods.\n")
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
    """Simulate player choices dur1)ing the chase with evolving options."""
    actions_stage_1 = {
        "1": {"action": "Sprint away!", "time_change": 10},
        "2": {"action": "Hide in a nearby alley.", "time_change": -5},
        "3": {"action": "Use a speed boost!", "time_change": 20},
        "4": {"action": "Look for a shortcut!", "time_change": 15}
    }

    actions_stage_2 = {
        "1": {"action": "Jump over a fence!", "time_change": -20},
        "2": {"action": "Hide in the shadows.", "time_change": -10},
        "3": {"action": "Attempt a risky maneuver!", "time_change": 30},
        "4": {"action": "Take the long way around.", "time_change": -25}
    }

    actions_stage_3 = {
        "1": {"action": "Try to blend in with the crowd.", "time_change": -5},
        "2": {"action": "Climb a building to escape.", "time_change": 10},
        "3": {"action": "Throw an object to mislead the pursuer.", "time_change": -15},
        "4": {"action": "Dash to a hidden spot.", "time_change": -30}
    }

    actions_stage_4 = {
        "1": {"action": "Try to blend in with the crowd.", "time_change": -5},
        "2": {"action": "Climb a building to escape.", "time_change": 10},
        "3": {"action": "Throw an object to mislead the pursuer.", "time_change": -15},
        "4": {"action": "Dash to a hidden spot.", "time_change": -30}
    }

    actions_stage_5 = {
        "1": {"action": "Try to blend in with the crowd.", "time_change": -5},
        "2": {"action": "Climb a building to escape.", "time_change": 10},
        "3": {"action": "Throw an object to mislead the pursuer.", "time_change": -15},
        "4": {"action": "Dash to a hidden spot.", "time_change": -30}
    }

    actions_stage_6 = {
        "1": {"action": "Try to blend in with the crowd.", "time_change": -5},
        "2": {"action": "Climb a building to escape.", "time_change": 10},
        "3": {"action": "Throw an object to mislead the pursuer.", "time_change": -15},
        "4": {"action": "Dash to a hidden spot.", "time_change": -30}
    }

    actions_stage_7 = {
        "1": {"action": "Try to blend in with the crowd.", "time_change": -5},
        "2": {"action": "Climb a building to escape.", "time_change": 10},
        "3": {"action": "Throw an object to mislead the pursuer.", "time_change": -15},
        "4": {"action": "Dash to a hidden spot.", "time_change": -30}
    }

    actions_stage_8 = {
        "1": {"action": "Try to blend in with the crowd.", "time_change": -5},
        "2": {"action": "Climb a building to escape.", "time_change": 10},
        "3": {"action": "Throw an object to mislead the pursuer.", "time_change": -15},
        "4": {"action": "Dash to a hidden spot.", "time_change": -30}
    }

    actions_stage_9 = {
        "1": {"action": "Try to blend in with the crowd.", "time_change": -5},
        "2": {"action": "Climb a building to escape.", "time_change": 10},
        "3": {"action": "Throw an object to mislead the pursuer.", "time_change": -15},
        "4": {"action": "Dash to a hidden spot.", "time_change": -30}
    }

    actions_stage_10 = {
        "1": {"action": "Try to blend in with the crowd.", "time_change": -5},
        "2": {"action": "Climb a building to escape.", "time_change": 10},
        "3": {"action": "Throw an object to mislead the pursuer.", "time_change": -15},
        "4": {"action": "Dash to a hidden spot.", "time_change": -30}
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
