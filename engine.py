from queue import PriorityQueue
import metaevents 

# main game engine
class GameEngine():
    def __init__(self):
        self.non_hitlag_queue = PriorityQueue()
        self.input_list = []
        self.hitlag_queue = PriorityQueue() #unused
        self.frames_in_hitlag = 0
        self.in_action = False
        self.is_dash_cancelable = True
        self.current_time = 0
        self.previous_time = -1000
        self.party = None
        self.has_input_queued = False
        self.in_delay = False
        self.global_counter = 0
        self.global_me_handler = metaevents.MetaEventHandler(self, None)
    
    def add_event(self, e):
        # need to add a counter term for tie breaking 
        # adds an event to the non hitlag queue
        self.non_hitlag_queue.put((e.time,-1 * self.global_counter , e))
        self.global_counter += 1

    def process_next_event(self):
        # consume the next event in the queue
        print()
        print("Processing next event.")
        print(f"Key state - has_input_queued: {self.has_input_queued}; is_dash_cancelable: {self.is_dash_cancelable}, in_action: {self.in_action}")

        print()
        print("Queue state is now as follows:")
        print(self.str_queue_state())


        event_time, _ , event = self.non_hitlag_queue.get()
        print(event_time, event)
        self.current_time, self.previous_time = event_time, self.current_time

        # if self.current_time - self.previous_time > 0:
        #     # time has progressed
        #     if not self.has_input_queued:
        #         self.take_next_player_input()

        if event.is_user_action:
            self.has_input_queued = False

        # do something with event; THIS SHOULD DISABLE BEING ABLE TO ACT IF NECESSARY
        # propagate pre_metaevents

        print("Emitting pre_metaevents:")
        for pre_metaevent in event.pre_metaevents:
            print(pre_metaevent)
            pre_metaevent.trigger_owner.me_handler.process_metaevent(
                pre_metaevent
            )

        # execute state modification
        event.modify_state()

        # emit post metaevents
        print("Emitting post_metaevents")
        for post_metaevent in event.post_metaevents:
            print(post_metaevent)
            post_metaevent.trigger_owner.me_handler.process_metaevent(
                post_metaevent
            )

        # propagate post_metaevents

    def run_until_cancelable(self):
        print(f"Now running until cancelable, current time {self.current_time}")
        # need time to have progressed forward
        # see comments on run_until_actionable
        cancelable = (self.is_dash_cancelable or not self.in_action) and (self.current_time - self.previous_time > 0) and not self.has_input_queued
        print(f"cancelable: {cancelable}")
        
        while not cancelable:
            self.process_next_event()
            cancelable = (self.is_dash_cancelable or not self.in_action) and (self.current_time - self.previous_time > 0) and not self.has_input_queued
            print(f"Key state - has_input_queued: {self.has_input_queued}; is_dash_cancelable: {self.is_dash_cancelable}, in_action: {self.in_action}")

            print(f"State is now cancelable: {cancelable}")
    
    def run_until_actionable(self):
        print(f"Now running until actionable, current time {self.current_time}")
        # the reason for the time check is because sometimes the action itself doesn't disable user action, it is instead 
        # an event created by it; for example, for normal attack being queued, it creates a normal attack start event
        # which actually sets the in_action flag
        # as a result, if this is not processed immediately after the DoNormalAttack event, then we would exit too early
        # if we have an input queued, then we haven't run until the next input can be queued.
        actionable = ((not self.in_action) and (self.current_time - self.previous_time > 0)) and not self.has_input_queued
        print(f"actionable: {actionable}")
        while not actionable:
            self.process_next_event()
            actionable = (not self.in_action) and (self.current_time - self.previous_time > 0) and not self.has_input_queued
            print(f"Key state - has_input_queued: {self.has_input_queued}; is_dash_cancelable: {self.is_dash_cancelable}, in_action: {self.in_action}")
            
            print(f"State is now cancelable: {actionable}")

    
    def run_forward(self, delay):
        # to simulate delay, simply runforward for enough frames
        start_delay_time = self.current_time
        self.in_delay = True
        while self.current_time - start_delay_time < delay:
            self.process_next_event()
        self.in_delay = False

    def str_queue_state(self, num_events = None):
        # helper method for visualizing
        accum = ""
        if num_events is None:
            num_events = len(self.non_hitlag_queue.queue)
        
        for i, (t, _, e) in enumerate(self.non_hitlag_queue.queue):
            if i == num_events:
                break
            accum += f"t = {t}: {e}\n"
        return accum

    def take_next_player_input(self, e):
        # this is the driving method of the script. 
        # this consumes the next player action, and runs until a new action can be taken. 

        print("Taking next user action: ", e)

        # e = self.input_list[0]
        # self.input_list = self.inpu
        assert e.is_user_action

        # not implementing jump cancel
        if not e.is_dash:
            self.run_until_actionable()
        
        # insert the event at the start of the queue

        if not e.is_delay:
            # override time setting on event
            e.time = self.current_time
            print(e)
            self.add_event(e)
            self.has_input_queued = True
            print("Queue state after adding event")
            for (t, _, e) in self.non_hitlag_queue.queue:
                print(f"t = {t}\t{e}")
            # self.non_hitlag_queue
            self.run_until_cancelable()
        else:
            self.run_forward(e.delay)

    def load_party(self, party_list):
        self.party = party_list
        for char in party_list:
            char.set_game_state(self)
            char.me_handler.parent = self.global_me_handler

    def load_enemy(self, enemy):
        self.enemy = enemy
        self.enemy.me_handler.parent = self.global_me_handler

    def flush(self):
        # if finished acting, flush the remainder of the queue
        while not self.non_hitlag_queue.empty():
            print("Queue state is now as follows:")
            print(self.str_queue_state())

            self.process_next_event()

