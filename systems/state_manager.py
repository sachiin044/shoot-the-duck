from config import *

class StateManager:
    def __init__(self):
        self.state = MENU
        self.last_state = None

    def change_state(self, new_state):
        self.last_state = self.state
        self.state = new_state
        print(f"State changed to {new_state}")

    def is_state(self, state):
        return self.state == state
