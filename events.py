from metaevents import DamageDealt, DidCrit, DamageReceived

# the workhorse class
class Event:
    def __init__(self, pre_metaevents, post_metaevents, time, game_state, is_user_action = False, is_dash = False, is_delay = False):
        self.pre_metaevents = pre_metaevents
        self.post_metaevents = post_metaevents
        self.time = time
        self.game_state = game_state
        self.is_user_action = is_user_action
        self.user_input_delay = 0 # in frames
        self.is_dash = is_dash
        self.is_delay = is_delay

    def modify_state(self):
        # can potentially push new events to the queue
        pass

    # def __str__(self):
    #     # print("aaaa", type(self))
    #     return str(type(self))

class DamageEvent(Event):
    def __init__(self, pre_metaevents, post_metaevents, time, game_state, damage_object):
        super().__init__(pre_metaevents, post_metaevents, time, game_state)

        self.damage_object = damage_object
    
    def modify_state(self):
        print("Damage event modifying state")
        # do some damage calculation here
        damage_dealt, did_crit = self.damage_object.damage_target.take_incoming_damage(
            self.damage_object
        )

        print(f"Damage dealt: {damage_dealt}, did_crit: {did_crit}")
        if damage_dealt > 0:
            print("Appending DamageDealt metaevent")
            self.post_metaevents.append(
                DamageDealt(self.damage_object.damage_owner)
            )
            self.post_metaevents.append(
                DamageReceived(self.damage_object.damage_target)
            )
        if did_crit and damage_dealt > 0:
            print("Appending DidCrit metaevent")
            self.post_metaevents.append(
                DidCrit(self.damage_object.damage_owner)
            )
        

class AddBuffEvent(Event):
    def __init__(self, pre_metaevents, post_metaevents, time, game_state, buff_object):
        super().__init__(pre_metaevents, post_metaevents, time, game_state)

        self.buff_object = buff_object
    
    def modify_state(self):
        pass

class RemoveBuffEvent(Event):
    def __init__(self, time, game_state, buff_object):
        super().__init__(pre_metaevents = [], post_metaevents = [], time = time, game_state = game_state)

        self.buff_object = buff_object
    
    def modify_state(self):
        self.buff_object.character.remove_buff(
            self.buff_object
        )
