import os
import sys
#import time

#Open in new window
class Terminal:
    def __init__(self, script_name="GameV1.5.py"):
        self.script_name = script_name
        self.currentRoom = "None"
        self.roomsEntered = [self.currentRoom]
        self.roomEntryCounts = {'Trophy Room':0}
        self.inventory = []
        self.interactions = ["Hedda Gabler Lever"]
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

T = Terminal()  # Create an instance of the Terminal class
T.open_new_terminal()  # Call the method to open a new terminal



#Tell the player the commands at the beginning of the game
class Commands:
    def __init__(self):
        self.commands = ""

    def tell_commands(self):
        self.commands = "To = Allows you to move to the room or direction stated.\nExamine = Look at an object stated.\nInteract = Pick up or touch an object\nUse = use an object you have interacted with to collect\nOn = Prompted after Use; asks what you want to use your object on.\n\n\n"
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
print("PRESS ENTER TO PROCEED")
input()
T.clear_screen()
G.ask_name()
T.clear_screen()
G.greet()
input()
T.clear_screen()

print("You stand before an entrance hall of cobble and wood.\nUnlike the rest of the house, the floors here are stone, with towering pillars of marble sprouting out.\nThe cobble walls crumble around you, spider webs seem to devour every dark corner of the room, and chunks of stone litter the ground.\nA single red carpet runs below your feet and up a grandiose spruce staircase, leading left and right.\nIts red fabric runs like fine wine flowing up to the landing.\n\n\nThe room is illuminated only by dim, flickering lanterns that hang from the ceiling. A wooden balcony overlooks the room you are in.\nYou clutch the note in your hand, then pocket it.\nThe room is eerily quiet, apart from the sound of your own short breathing and the creaking of the manor.\n\n\nTwo doors line the right wall, to the game room and lounge, and one sits on the left wall leading to a dining room.\n")
while True:

#Entrance Hall


    T.currentRoom = "Entrance Hall"
    while T.currentRoom == "Entrance Hall":
        T.user_input()
        if "to landing" in T.input or "to stairs" in T.input:
            T.clear_screen()
            C.tell_commands()
            print("Up the stairs there is a small hallway that branches into more rooms. \nFurther up is the balcony which overlooks the entrance hall. \n\n\nThere are doors to the master bedroom and a long hallway.\nThe balcony is mostly bare aside from \n")
            T.proceed("Upper Landing")
        elif "to game" in T.input or "to game room" in T.input:
            T.clear_screen()
            C.tell_commands()
            print("You enter the mansion's game room, immediately taking in the sharp aroma of alcohol and pool chalk. \nThe small square room has an open archway in the back that leads into a lounge. \n\n\nIn the front of the room lies a couch, a tv sitting on a stand across from it, buzzing static. \nA large red-felted pool table behind the couch displays a losing game of solids against stripes. \nA broken cue is discarded upon the table, snapped in half. \nA dartboard hangs from a wall behind the pool table, with some darts still scattered upon the floor and pinned into the wall.\n")
            T.proceed("Game Room")
        elif "to lounge" in T.input:
            T.clear_screen()
            C.tell_commands()
            print("You enter the lounge, the faint smell of firewood pricking your nose. \nScattered across the room, but all facing a central fireplace, are a few armchairs, a coffee table, and a large painting of what looks like Elias, but older. \n\n\nA door leads into the library and an archway opens up into the game room.\n")
            T.proceed("Lounge")
        elif "to dining" in T.input or "to dining room" in T.input:
            T.clear_screen()
            C.tell_commands()
            print("You enter the dining room. \nRich wooden floors and rugged stone walls line the room. \nA long, dark oak table stretches out in the center of the room, surrounded by carved wooden chairs. \nCandles hang along the wall and on the table, emanating an eerie glow. \n\n\nFood lines the table, the smell of meat and wine fills the air. \nAt the head of the table, sits a finished meal of steak and wine, and next to it, a half-eaten messy abomination of what you think used to be chicken, torn to shreds. \nA fresh apple sits alone among the mess, and a steak knife has fallen to the floor.\n")
            T.proceed("Dining Room")
        elif "examine pillar" in T.input:
            print("Large and crumbling ornate pillar supports the manor, carved with intricate patterns and words in another language.\n")
        elif "examine stone" in T.input:
            print("The large stones that litter the ground appear to have fallen from a large faded mural on the ceiling. \nYou can only make out the remains of a large star. \nSmaller stones sit akin to the large.\n")
        elif "examine door" in T.input:
            print("The mahogany door you came through towers over you. \nYou try to turn the large silver handle, but it doesn't budge. \nYou will need a key.\n")
        elif "examine carpet" in T.input:
            print("The carpet is old and worn, moreso in the areas that intersect the paths to the left and right doors. \nIt strikes you as odd, for Elias has always been a tidy man.\n")
        elif "interact stone" in T.input:
            if "Stone" not in T.inventory:
                print("You pick up a stone off the ground.\n")
            elif "Stone" in T.inventory:
                print("You already picked up the stone.\n")
        else:
            print("Invalid input, try something like 'to game room', 'examine stone', or 'interact door'.\n")

    while T.currentRoom == "Game Room":
        T.user_input()
        if "back" in T.input or "to entrance" in T.input:
            T.clear_screen()
            C.tell_commands()
            print("You go back into the entrance hall; the floors here are stone, with towering pillars of marble sprouting out.\nThe cobble walls crumble around you, spider webs seem to devour every dark corner of the room, and chunks of stone litter the ground.\nA single red carpet runs below your feet and up a grandiose spruce staircase, leading left and right.\nIts red fabric runs like fine wine flowing up to the landing.\n\n\nThe room is illuminated only by dim, flickering lanterns that hang from the ceiling. A wooden balcony overlooks the room you are in.\nThe room is eerily quiet, apart from the sound of your own short breathing and the creaking of the manor.\n\n\nTwo doors line the right wall, to the game room and lounge, and one sits on the left wall leading to a dining room.\n")
            T.proceed("Entrance Hall")
        elif "to lounge" in T.input or "to archway" in T.input:
            T.clear_screen()
            C.tell_commands()
            print("You enter the lounge, the faint smell of firewood pricking your nose. \nScattered across the room, but all facing a central fireplace, are a few armchairs, a coffee table, and a large painting of what looks like Elias, but older. \n\n\nA door leads into the library and an archway opens up into the game room behind you.\n")
            T.proceed("Lounge")
        elif "examine pool" in T.input or "examine table" in T.input:
            print("You see a game of pool, with stripes having an apparent winning position. You notice the 8 Ball is missing, and find it in one of the pockets. You look towards the broken cue. It seems like the solids player was having a bad day.")
        elif "interact cue" in T.input:
            if "Cue" not in T.inventory:
                print("You grab one of the broken halves of the pool cue.")
                T.add_to_inventory("Cue")
            elif "Cue" in T.inventory:
                print("You already picked up the cue.")
        elif "examine couch" in T.input:
            print("")
        elif "examine tv" in T.input:
            print("")
        elif "examine dart" in T.input or "examine board" in T.input:
            print("")
        elif "interact couch" in T.input:
            print("")
        elif "interact remote" in T.input:
            print("")
        elif "interact leaflet" in T.input or "interact rules" in T.input:
            print("")
        else:
            print("Invalid input, try something like 'to lounge', 'examine pool table', or 'interact cue'.\n")

    while T.currentRoom == "Lounge":
        T.user_input()
        if "back" in T.input or "to entrance" in T.input:
            T.clear_screen()
            C.tell_commands()
            print("You go back into the entrance hall, ")
            T.proceed("Entrance Hall")
        elif "to library" in T.input:
            T.clear_screen()
            C.tell_commands()
            print("")
            T.proceed("Lower Library")
        elif "to game room" in T.input or "to archway" in T.input:
            T.clear_screen()
            C.tell_commands()
            print("")
            T.proceed("Game Room")
        elif "examine fireplace" in T.input:
            if "Hedda Gabler Lever" in T.interactions:
                print("The fireplace is a classic gray brick, with a metal holder holding ashen wood, and a fire prod stuck inside. \n\n\nYou see behind the fireplace is an old lockbox with a combination lock. \nThere are colored tiles, Green, Black, Red, and White, with sliders to input numbers.\n")
                print("You may input any four numbers ranging from 1 to 99 in each slot with a space between each number. \nWhat would you like to input?\n")
                lockbox_input = input("> ")
                if "25 13 54 15" in lockbox_input:
                    print("You hear a click, and lift the lid of the box. Inside you find a small bronze key, and pocket it.\n")
                    T.add_to_inventory("Bronze Key")
                elif "25 13 54 15" not in lockbox_input:
                    print("The lockbox does not open.\n")
            elif "Hedda Gabler Lever" not in T.interactions:
                print("The fireplace is a classic gray brick, with a metal holder holding ashen wood, and a fire prod stuck inside. \nOddly, you see no vent to channel the smoke, and the fireplace seems more shallow than you would expect.\n")
        elif "examine painting" in T.input:
            print("As you walk closer, you notice the painting isn't actually of Elias, but rather of his Father, Silas. \nAlthough sitting regally in a fine armchair, he seems roughened up. Middle aged with a stubble covered face and crooked nose; he looks weary, this was probably painted close to his death.\n")
        elif "interact painting" in T.input:
            print("You lift up the painting, and a note falls to the ground. Picking it up to read, it simply says '6'.")
            T.add_to_inventory("Note: '6'")
        elif "interact prod" in T.input:
            print("As you pick up the fire prod, the weak metal turns to ash in your hands.\n")
        elif "examine armchair" in T.input:
            print("You scavenge through the armchairs, only finding some loose change and an old shopping list that reads:,\nBotany Book, Bucket, Painting, and Boar Head Mantle. \nYou pocket the list.\n")
        elif "examine table" in T.input:
            print("Scattered atop the coffee table are a variety of pages, appearing to be torn from various books. The table also seems to be burnt in areas, with holes pokes through some of the pages and through the table. The legible pages include: A ripped up children's book on learning to read, a page from Elias’s favorite book, “Hedda Gabler”, and an excerpt from the poem “On Being Human.” The except reads: Far richer they! I know the senses' witchery\nGuards us like air, from heavens too big to see;\nImminent death to man that barb'd sublimity\nAnd dazzling edge of beauty unsheathed would be.\nYet here, within this tiny, charmed interior,\nThis parlour of the brain, their Maker shares\nWith living men some secrets in a privacy\nForever ours, not theirs.\n")

    while T.currentRoom == "Dining Room":
        T.user_input()
        if "" in T.input:
            print("")

    while T.currentRoom == "":
        T.user_input()
        if "" in T.input:
            print("")

    while T.currentRoom == "Upper Landing":
        T.user_input()
        if "back" in T.input or "to entrance" in T.input:
            T.clear_screen()
            C.tell_commands()
            print("You go back down into the entrance hall; the floors here are stone, with towering pillars of marble sprouting out.\nThe cobble walls crumble around you, spider webs seem to devour every dark corner of the room, and chunks of stone litter the ground.\nA single red carpet runs below your feet and up a grandiose spruce staircase, leading left and right.\nIts red fabric runs like fine wine flowing up to the landing.\n\n\nThe room is illuminated only by dim, flickering lanterns that hang from the ceiling. A wooden balcony overlooks the room you are in.\nThe room is eerily quiet, apart from the sound of your own short breathing and the creaking of the manor.\n\n\nTwo doors line the right wall, to the game room and lounge, and one sits on the left wall leading to a dining room.\n")
            T.proceed("Entrance Hall")
        elif "to hallway" in T.input:

            T.clear_screen()
            C.tell_commands()
            print("You turn into the small hallway that parts from the stairs to find the trophy room. \nA few hunting trophies hang from high on the walls including: a lion, a deer, a wolf, and a boar.\nDoors leading to the servant's quarters and upper library are also found in the hallway.\n\n")
            if T.roomEntryCounts['Trophy Room'] == 0:
                print("A circular red carpet sits on the floor, and shelves full of gold and silver metal line the walls. You take note of a few awards: The Genetic Research Excellence Award for Elias Finch, The Genomic Innovation Award for Elias Finch, The Genetic Education and Outreach Award for Elias & Silas Finch, The Mendel Award for Silas Finch, and the Stem Cell Genetics Award for Silas Finch.\n")
            elif T.roomEntryCounts['Trophy Room'] == 1:
                print("A square red carpet lays down exhausted on the floor, shelves full of silver and gold metal line the walls. \nYou take note of a few awards: The Jean and Fabric Research Excellence Award for Elias Finch, The Genomal Innovation Award for Elias Finch, The Genetic Outreach Award for Silas Finch, The Mendel Award for Silas Finch, and the Mycology Award for Silas Finch. \nLittle mushrooms grow out of the Mycology award. \nYou feel a little lightheaded.\n")
            elif T.roomEntryCounts['Trophy Room'] == 2:
                print("A circular red mushroom cap grows out of the floor like a carpet, shelves full of gold, silver, and purple metal line the walls. \nYou take note of a few awards: The Deoxyribonucleic acid Award for Elias Hemlock, The Genome Intantiator Award for Elias Finch, The Genetic Mycology Award for Elias & Silas Finch, The Limb Splicer Award for Silas Finch, and the Medieval Torture Award for Silas Finch. \nMushrooms grow out of the trophies and the walls. \nYou feel lightheaded, a purple mist clouds your vision.\n")
            T.proceed("Trophy Room")
        elif "to master" in T.input or "to bedroom" in T.input:
            if "Bronze Key" in T.inventory:
                print("")
            elif "Bronze Key" not in T.inventory:
                print("")
        else:
            print("Invalid input, try 'to hallway' or 'to master'.")

        while T.currentRoom == "Trophy Room":
            T.user_input()
            if "to servant's" in T.input or "to quarters" in T.input:
                T.clear_screen()
                C.tell_commands()
                print("")
                T.proceed("Servant's Quarters")
            elif "back" in T.input or "to landing" in T.input:
                T.clear_screen()
                C.tell_commands()
                print("")
                T.proceed("Upper Landing")
            elif "to library" in T.input or "to upper" in T.input:
                T.clear_screen()
                C.tell_commands()
                print("")
                T.proceed("Upper Library")
