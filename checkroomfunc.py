def check_room_event(self, room, indices_from_right):
        # If for instance you're checking if a number is in the index -2 or further indices_from_right needs to be 2.
        # Check the portion of the list before the last `indices_from_right` items.
        cutoff = len(self.roomsEntered) - indices_from_right
        if cutoff < 0:
            cutoff = 0  # Ensure no negative slicing.
        return room_name in self.roomsEntered[:cutoff]
