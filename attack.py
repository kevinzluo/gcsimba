from buffs import ParamitaPapilio
from events import Event, DamageEvent, RemoveBuffEvent
from damage import DamageObject
from metaevents import NAStartME, NAEndME
import metaevents

class AttackObject(Event):
    def __init__(self, owner, multiplied_stats, frame_counts, icd_tag, elemental_type, damage_type):
        self.owner = owner # owner is an entity (e.g. could be xiangling OR pyronado); I guess there should be both an entityowner attribute and a characterorigin attribute for transformatives, but that's too complicated for now
        self.multiplied_stats = multiplied_stats
        self.frame_counts = frame_counts
        assert len(multiplied_stats) == len(frame_counts)

        self.damage_type = damage_type # like normal attack, etc
        self.icd_tag = icd_tag
        self.elemental_type = elemental_type

class DoNormalAttack(Event):
    def __init__(self, pre_metaevents, post_metaevents, time, game_state, attack_object):
        super().__init__(pre_metaevents, post_metaevents, time, game_state, is_user_action=True)
        self.attack_object = attack_object

    def modify_state(self):
        # should queue 3 new events
        self.game_state.add_event(
            NormalAttackStart(game_state = self.game_state, time = self.time, attack_object=self.attack_object)
        )

        for mult, frame in zip(self.attack_object.multiplied_stats, self.attack_object.frame_counts):

            constructed_damage_object = DamageObject(
                self.attack_object.owner,
                damage_target = self.game_state.enemy,
                damage_source_type="NormalAttack",
                damage_source_subtype=self.attack_object.elemental_type,
                multiplied_stat=mult,
                icd_tag=self.attack_object.icd_tag
            )

            self.game_state.add_event(
                DamageEvent(
                    pre_metaevents=[],
                    post_metaevents=[],
                    time = self.time + frame,
                    game_state=self.game_state,
                    damage_object= constructed_damage_object
                )
            )
        
        print("enqueuing normal attack end")
        print(max(self.attack_object.frame_counts) + 5)
        # heuristic
        self.game_state.add_event(
            NormalAttackEnd(
                pre_metaevents=[],
                post_metaevents=[],
                time = self.time + max(self.attack_object.frame_counts) + 5,
                game_state=self.game_state,
                attack_object=self.attack_object
            )
        )
    
    def __str__(self):
        return f"Normal Attack, owner {self.attack_object.owner}"


class NormalAttackStart(Event):
    def __init__(self, game_state, attack_object, time, pre_metaevents = None, post_metaevents = None, ):
        if pre_metaevents is None:
            pre_metaevents = []


        if post_metaevents is None:
            post_metaevents = [NAStartME(attack_object.owner)]
        else:
            post_metaevents = post_metaevents + [NAStartME(attack_object.owner)]

        super().__init__(pre_metaevents, post_metaevents, time, game_state, is_user_action=False)

        self.attack_object = attack_object
    
    def modify_state(self):
        self.game_state.in_action = True
        self.game_state.is_dash_cancelable = False

class NormalAttackEnd(Event):
    def __init__(self, game_state, attack_object, time, pre_metaevents = None, post_metaevents = None):
        if pre_metaevents is None:
            pre_metaevents = []

        if post_metaevents is None:
            post_metaevents = [NAEndME(attack_object.owner)]
        else:
            post_metaevents = post_metaevents + [NAEndME(attack_object.owner)]

        super().__init__(pre_metaevents, post_metaevents, time, game_state, is_user_action=False)

    def modify_state(self):
        self.game_state.in_action = False
        self.game_state.is_dash_cancelable = True

class HuTaoSkill(Event):
    def __init__(self, time, game_state, hutao_obj, pre_metaevents = None, post_metaevents = None,):
        if pre_metaevents is None:
            pre_metaevents = []

        if post_metaevents is None:
            post_metaevents = []

        self.hutao_obj = hutao_obj

        super().__init__(pre_metaevents, post_metaevents, time, game_state, is_user_action = True, is_dash = False, is_delay = False)
    
    def modify_state(self):
        # create an eskill start, eskill finish, buff expire events

        self.game_state.add_event(
            HuTaoSkillStart(
                time=self.game_state.current_time,
                game_state=self.game_state,
                hutao_obj=self.hutao_obj,
            )
        )
        # buff removal is created by this event bc needs access to the same buff object

        self.game_state.add_event(
            HuTaoSkillEnd(
                time = self.game_state.current_time + 5,
                game_state=self.game_state,
                hutao_obj=self.hutao_obj,
            )
        )

        pass

class HuTaoSkillStart(Event):
    def __init__(self, time, game_state, hutao_obj, pre_metaevents = None, post_metaevents = None,):
        if pre_metaevents is None:
            pre_metaevents = []

        if post_metaevents is None:
            post_metaevents = []

        # post_metaevents += [metaevents.SkillME(hutao_obj)] moved to event end

        self.hutao_obj = hutao_obj

        super().__init__(pre_metaevents, post_metaevents, time, game_state, is_user_action = True, is_dash = False, is_delay = False)

    def modify_state(self):
        assert self.time == self.game_state.current_time
        self.hutao_obj.pp_active = True

        self.game_state.in_action = True
        self.game_state.is_dash_cancelable = False

        self.hutao_obj.last_skill_time = self.game_state.current_time

        # give hutao the pp buff

        buff_obj = ParamitaPapilio(placement_time=self.game_state.current_time)

        self.hutao_obj.add_buff(
            buff_obj
        )


        self.game_state.add_event(
            RemoveBuffEvent(
                time=self.game_state.current_time + 60 * 9,
                game_state=self.game_state,
                buff_object=buff_obj
            )
        )

        # give hutao pp state
        # give hutao
        # disable ability to act
        # start the skill cooldown
        # pass

class HuTaoSkillEnd(Event):
    def __init__(self, time, game_state, hutao_obj, pre_metaevents = None, post_metaevents = None,):
        if pre_metaevents is None:
            pre_metaevents = []

        if post_metaevents is None:
            post_metaevents = []

        post_metaevents += [metaevents.SkillME(hutao_obj)]

        self.hutao_obj = hutao_obj

        super().__init__(pre_metaevents, post_metaevents, time, game_state, is_user_action = True, is_dash = False, is_delay = False)

    def modify_state(self):
        # re-enable ability to act

        self.game_state.in_action = False
        self.game_state.is_dash_cancelable = True



    


# class NormalAttackContact(Event):
#     def __init__(self, game_state, attack_object, damage_object, pre_metaevents = [], post_metaevents = [], time = [], is_user_action=False):
#         post_metaevents += [NAEndME(attack_object.owner)]
#         super().__init__(pre_metaevents, post_metaevents, time, game_state, is_user_action) 
    
#     def modify_state(self):
#         return


    
