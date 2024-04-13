
from queue import PriorityQueue
class GameEngine():
    def __init__(self):
        self.non_hitlag_queue = PriorityQueue()
        self.hitlag_queue = PriorityQueue()
        self.frames_in_hitlag = 0
        self.in_action = True
        self.is_dash_cancelable = True
        self.current_time = 0
        self.party = None
    
    def add_event(self, ):

        pass

    def process_next_event(self, ):
        pass

    def load_party(self, party_list):
        self.party = party_list
        for char in party_list:
            char.set_game_state(self)
        

class Event():
    def __init__(self, time):
        self.time = time