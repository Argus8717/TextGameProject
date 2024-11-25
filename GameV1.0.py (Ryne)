import time
#from subprocess import call
#call(["gnome-terminal", "-x", "sh", "-c", "espeak -ven+m1 -f sample.txt;bash"])
print("Welcome to !")
print("Your friend Elias has invited you to his house to hang out.")
print("What you  ")
print("Walking up the crumbling path of gravel, you approach your friend's mansion.")
print("The door, once grand, now creaks slightly, as if inviting you in.")
print("You push open the door, and it groans in protest, revealing the dim interior lit by a glass chandelier hanging from the ceiling.")
print("A large staircase stretches upward and two doors flank each side of the entry hall.")
print("HINT1: Use directions such as 'left' or 'right' to move into new rooms!")
print("Hint2: Use search to get more detailed descriptions of rooms, then use names of items you see such as 'axe' to try and interact with them!\n")
print("What do you do?\n")

#List of rooms
roomsList = {
    "Entrance Hall": {("Kitchen", "Game Room", "Hall", "Lower Library", "Dining Room")},
    "Kitchen": {},
    "Dining Room": {},
    "Upper Landing": {},

}

# Inventory
inventory = []
# Current room
currentRoom = "Entrance Hall"
# Room entrance tracker
roomsEntered = [currentRoom]

def check_room_event(room, moves_ago):
    global roomsEntered
    if len(roomsEntered) > moves_ago:
        room_at_moves_ago = roomsEntered[-(moves_ago+1)]
        if room_at_moves_ago == room:
            return True
        for i in range(len(roomsEntered) - moves_ago-1):
            if roomsEntered[i] == room:
                return True
    return False

def trigger_room_event(room, moves_ago, text1, text2):
    if check_room_event(room, moves_ago):
        print(text1)
    else:
        print(text2)

def add_to_inventory(item):
    global inventory
    inventory.append(item)
    print("You grabbed the {}!".format(item))

def check_inventory(item):
    global inventory
    if item in inventory:
        return True
    return False

def proceed(room):
    global roomsEntered, currentRoom
    currentRoom = room
    roomsEntered.append(room)

def get_current_room():
    global currentRoom
    return currentRoom

def get_rooms_entered():
    global roomsEntered
    return roomsEntered

def get_inventory():
    global inventory
    return inventory

while True:
    while currentRoom == "Entrance Hall":
        print(roomsEntered)
        entry_choice = input("> ")
        if "up".lower() in entry_choice:
            print("Walking up the stairs, you find another, larger floor.")
            print("There are two more doors; one to your left and one to your right.")
            if check_room_event("Upper Landing", 5):
                print("**  The hallway which used to end at a blank wall now has a door.  **")
            else:
                print("A hallway stretches fifty feet and dead ends.")
            print("A railing follows along the edge of the floorboards, overlooking the entry hall below.")
            print("Two statues sit in the corners of the landing.")
            print("What do you do?\n")
            proceed("Upper Landing")
        elif "left".lower() in entry_choice:
            print("You open the door to find a kitchen.")
            proceed("Kitchen")
        elif "right".lower() in entry_choice:
            print("Moving toward the door, you hear the sound of porcelain plates falling and breaking accompanied by a loud thud.")
            print("You open the door, revealing a dark room with a large wooden table and eight chairs.")
            print("There is a cabinet with fine china dishes inside against the far wall and another laying face down on the floor to you're right--the source of the thud.")
            print("There is a door on the left.")
            print("What do you do?\n")
            proceed("Dining Room")
        elif "search".lower() in entry_choice:
            print("")


        else:
            print("Invalid choice, try: 'go up the stairs' or 'open the left door' or 'open the right door'\n")


    while currentRoom == "Upper Landing":
        upper_choice = input("> ")
        if check_room_event("Upper Landing", 5):
            if "straight".lower() in upper_choice:
                print("As you open the door, blood rushes out like a river.")
                proceed("Secret Lab")
            else:
                continue

        elif "left".lower() in upper_choice:
            print("Entering the door on the left, you come upon a large dark room.")
            print("")
            proceed("Servant's Quarters")
        elif "right".lower() in upper_choice:
            print("")
            proceed("")
        elif "back".lower() in upper_choice:
            print("You go down the stairs and back into the entrance hall.\n")
            proceed("Entrance Hall")
        elif "search".lower() in upper_choice:
            print("")


        else:
            print("Invalid choice, try: 'open a left door' or 'go back down the stairs'\n")


    while currentRoom == "Kitchen":
        kitchen_choice = input("> ")
        if "straight".lower() in kitchen_choice:
            print("")
            proceed("Patio")
        elif "right".lower() in kitchen_choice:
            print("")
            proceed("Basement Landing")
        elif "back".lower() in kitchen_choice:
            print("You go back into the entrance hall.\n")
            proceed("Entrance Hall")


    while currentRoom == "Dining Room":
        dining_choice = input("> ")
        if "left".lower() in dining_choice:
            print("")
            proceed("")
        elif "back".lower() in dining_choice:
            print("You go back into the entrance hall.\n")
            proceed("Entrance Hall")
        elif "search".lower() in dining_choice:
            print("")

    while currentRoom == "Servant's Quarters":
        servants_choice = input("> ")
        if "right".lower() in servants_choice:
            print("")
            proceed("")
        elif "back".lower() in servants_choice:
            print("You go back into the upper landing.\n")
            proceed("Upper Landing")

    while currentRoom == "Master Bedroom":
        master_choice = input("> ")

