def check_room_event(self, room, moves_ago):
        # If for instance you're checking if a number is in the index -2 or further moves_ago needs to be 2.
        # Check the portion of the list before the last `moves_ago` items.
        cutoff = len(self.roomsEntered) - moves_ago
        if cutoff < 0:
            cutoff = 0  # Ensure no negative slicing.
        return room_name in self.roomsEntered[:cutoff]
