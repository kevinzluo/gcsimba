from entities import StatContainer, Character, Weapon
from buffs import SanguineRouge, RecklessCinnabar
from attack import AttackObject, DoNormalAttack, HuTaoSkill


class HuTao(Character):

    def __init__(self, level, artifact_stats: StatContainer, buffs):
        super().__init__(
            90, # hard coding level for now
            106.43,
            15552,
            StatContainer(cd = 38.4),
            artifact_stats,
            buffs + [SanguineRouge()]
        )

        self.pp_active = False
        self.skill_cooldown = 18 * 60


    def normal(self):
        # assume talent level 10
        mvs = [
            [83.65],
            [86.09],
            [108.92],
            [117.11],
            [59.36, 62.8],
            [153.36],
            [242.57],
        ]

        # major simplification: just going to be the time
        frames = [
            [12],
            [9],
            [17],
            [22],
            [16, 26],
            [23]
        ]

        if self.game_engine.current_time - self.last_na_time > 60 or self.na_count == len(mvs) - 1: # reset normal chain if waited too long
            self.na_count = 0
        

        # insert an attack object

        # needs to depend on if pp is active

        print(f"Performing HT normal attack {self.na_count + 1}")
        print(self.buffs)
        na_event = DoNormalAttack(
            pre_metaevents=[],
            post_metaevents=[],
            time=self.game_engine.current_time,
            game_state=self.game_engine,
            attack_object=AttackObject(
                self, 
                [m * self.get_atk() / 100 for m in mvs[self.na_count]],
                frames[self.na_count],
                "na_damage",
                "pyro" if self.pp_active else "phys",
                "na_damage"
            )
        )

        # print(na_event.is_user_action)


        self.game_engine.take_next_player_input(
            na_event
        )

        self.na_count += 1
        self.last_na_time = self.game_engine.current_time

        # snapshots at the time of cast I think
        # probably not a big issue

        # do a normal attack
        # self.game_engine.add
        pass

    def charge(self):
        assert False # broke for now
        self.na_count = 0 # reset this

    def skill(self):
        assert self.game_engine.current_time - self.last_skill_time > self.skill_cooldown

        # hu tao e skill
        # what to do about a buff that gives you pyro infusion????


        self.pp_active = True

        # buff = ParamitaPapilio(self.game_engine.current_time)

        # self.add_buff(
        #     buff
        # )

        e_skill_event = HuTaoSkill(
            time=self.game_engine.current_time,
            game_state=self.game_engine,
            hutao_obj=self,
        )

        self.game_engine.take_next_player_input(
            e_skill_event
        )

class StaffOfHoma(Weapon):
    def __init__(self):
        super().__init__(
            base_atk = 608,
            bonus_stats = StatContainer(
                cd = 66.15,
                hp_pct=20,
            )
        )
    
    def equip_to_character(self, char: Character):
        super().equip_to_character(char)

        char.add_buff(
            RecklessCinnabar()
        )
