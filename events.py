from damage import calc_damage

class Event:
    def __init__(self, pre_metaevents, post_metaevents, time, game_state):
        self.pre_metaevents = pre_metaevents
        self.post_metaevents = post_metaevents
        self.time = time
        self.game_state = game_state

    def modify_state(self):
        # can potentially push new events to the queue
        pass

class DamageEvent(Event):
    def __init__(self, pre_metaevents, post_metaevents, time, game_state, damage_object):
        super().__init__(pre_metaevents, post_metaevents, time, game_state)

        self.damage_object = damage_object
    
    def modify_state(self):
        # do some damage calculation here
        damage_dealt = self.damage_object.target.take_incoming_damage(
            self.damage_object
        )

        if damage_dealt > 0:
            self.post_metaevents.append(
                "damage_dealt"
            )

def AddBuffEvent(Event):
    def __init__(self, pre_metaevents, post_metaevents, time, game_state, buff_object):
        super().__init__(pre_metaevents, post_metaevents, time, game_state)

        self.damage_object = damage_object
