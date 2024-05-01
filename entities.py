# is this really useful?
from damage import DamageEngine
import metaevents

class StatContainer:
    def __init__(self, flat_hp=0, hp_pct=0, flat_atk=0, atk_pct=0, cr=0, cd=0, er=0, 
                 dmg_bonus=0, pyro_bonus=0, hydro_bonus=0, ele_burst_bonus = 0, ele_skill_bonus = 0, 
                 melt_vape_bonus = 0, em = 0, ):
        self.flat_hp = flat_hp
        self.hp_pct = hp_pct
        self.flat_atk = flat_atk
        self.atk_pct = atk_pct
        self.cr = cr
        self.flat_hp = flat_hp
        self.hp_pct = hp_pct
        self.flat_atk = flat_atk
        self.atk_pct = atk_pct
        self.cr = cr
        self.cd = cd
        self.er = er
        self.dmg_bonus = dmg_bonus
        self.pyro_bonus = pyro_bonus
        self.phys_bonus = 0
        self.hydro_bonus = hydro_bonus
        self.ele_burst_bonus  = ele_burst_bonus 
        self.ele_skill_bonus  = ele_skill_bonus 
        self.melt_vape_bonus  = melt_vape_bonus 
        self.em  = em

class Entity:

    # should have an aura engine and an event engine
    def __init__(self, level = 90):
        # yeah
        self.level = level
        self.me_handler = metaevents.MetaEventHandler(owner_object=self, parent = None)

    def set_game_state(self, game_engine):
        self.game_engine = game_engine

class Character(Entity):
    # has stats n stuff
    # must have a weapon

    def __init__(self, level, base_atk: float, base_hp: float, base_bonus_stats: StatContainer, artifact_stats: StatContainer, buffs):
        super().__init__(level)
        # self.level = level
        self.base_atk = base_atk
        self.base_hp = base_hp
        self.base_bonus_stats = base_bonus_stats
        self.artifact_stats = artifact_stats

        # add in default character stats
        self.base_bonus_stats.cr += 5
        self.base_bonus_stats.cd += 50

        self.buffs = buffs

        for buff in buffs:
            buff.set_equipped_character(self)

        self.curr_hp = 1

        self.game_engine = None
        self.weapon = None

        self.na_count = 0
        self.last_na_time = -10000
        self.last_skill_time = -10000
        self.last_burst_time = -10000

        self.skill_cooldown = None
        self.burst_cooldown = None

        self.stamina = 240

    def equip_weapon(self, weap):
        self.weapon = weap
        weap.equip_to_character(self)

    def get_atk(self):
        return self.get_total_base_atk() * (1 + self.get_total_stat("atk_pct") / 100) + self.get_total_stat("flat_atk")

    def get_total_base_atk(self):
        return self.base_atk + self.weapon.base_atk

    def get_hp(self):
        # print(self.get_total_stat("hp_pct"))
        # print(self.base_hp)
        return self.base_hp * (1 + self.get_total_stat("hp_pct") / 100) + self.get_total_stat("flat_hp")
        
    def get_total_stat(self, stat: str):
        acc = getattr(self.base_bonus_stats, stat) + getattr(self.weapon.base_bonus_stats, stat) + getattr(self.artifact_stats, stat)
        # print("accumulator", acc)
        for buff in self.buffs:
            # print(buff)
            acc += buff.get_stat(stat) # getattr(buff.bonus_stats, stat)
        # print("accumulator", acc)
        return acc
    
    def add_buff(self, buff):
        self.buffs.append(buff)
        buff.set_equipped_character(self)
    
    def remove_buff(self, buff):
        self.buffs = [b for b in self.buffs if b != buff]


# class XingQiu(Character):
#     def __init__(self, level, artifact_stats, buffs):
#         super().__init__(
#             90, 
#             201.78,
#             757.6,
#             StatContainer(atk_pct = 24.0),
#             artifact_stats,
#             buffs
#         )
    


class Weapon:
    # has stats

    def __init__(self, base_atk, bonus_stats: StatContainer, buffs = []):
        self.base_atk = base_atk
        self.base_bonus_stats = bonus_stats
        self.buffs = buffs

        self.equipped_character = None

    def equip_to_character(self, char: Character):
        self.equipped_character = char
        # char.buffs.append(self.buffs)
    

# class PrimordialJadeCutter(Weapon):
#     def __init__(self):
#         super().__init__(
#             base_atk = 541.83,
#             bonus_stats = StatContainer(
#                 hp_pct = 20,
#                 cr = 44.1
#             )
#         )

#     def equip_to_character(self, char: Character):
#         char.add_buff(
#             ProtectorsVirtue()
#         )

# class MistSplitter(Weapon):
#     def __init__(self):
#         super().__init__(
#             base_atk = 674,
#             bonus_stats = StatContainer(
#                 hydro_bonus=12,
#             )
#         )

class Enemy(Entity):

    def __init__(self):
        super().__init__(level = 100)
        self.damage_taken = 0
        self.damage_engine = DamageEngine(self)
        self.res = {
            "phys": 10,
            "pyro": 10,
            "hydro": 10,
        }

    def take_incoming_damage(self, damage_object):
        assert self == damage_object.damage_target

        damage_taken = self.damage_engine.process_damage_object(
            damage_object
        )

        self.damage_taken += damage_taken[0]
        # not sure if there should be a new type for this

        return damage_taken

class TestDummy(Enemy):
    pass