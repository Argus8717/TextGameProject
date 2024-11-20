#Open in new window
import os
import sys
def open_new_terminal():
    if os.name == 'nt': # Windows
        # Check if the script is running, so we don't open another terminal recursively
        if 'GameV1.2.py' not in sys.argv:
            os.system('start cmd /k python GameV1.2.py')
    elif os.name == 'posix':  # Linux, macOS
        if 'GameV1.2.py' not in sys.argv:
            os.system('xterm -e python GameV1.2.py &')
open_new_terminal()
#Game Boot Function
class Greeter:
    def __init__(self):
        self.name = ""
    def ask_name(self):
        self.name = input("What is your name?")
    def greet(self):
        print(f"Dearest, {self.name}, It has been awhile since we last spoke, hasn't it? 10 years, I reckon. 10 years too long. Not a day has gone by that I haven't wanted to speak to you, share an idea, a revelation, a new discovery, but nothing felt big enough… Nothing seems to warrant contacting you again, especially considering the terms of our last conversation. But this time I find myself having encountered something extraordinary. A development in my genetic research that could change our very world. And we are far too wise to hang on to old grudges when science is involved. So I invite you, old friend, to visit me at my mansion so we may discuss this new discovery. For I feel your input would be most valuable. I have attached the address to the back of this letter, along with some money to get you here. And if you can’t make it, keep it. But I do wish to see you again. Sincerely, Dr. Elias's Finch")
greeter = Greeter()
#Starting the Game
greeter.ask_name()
greeter.greet()
#Entrance Hall
currentRoom = "Entrance Hall"
