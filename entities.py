# is this really useful?

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

    def set_game_state(self, game_engine):
        self.game_engine = game_engine


class Character(Entity):
    # has stats n stuff
    # must have a weapon

    def __init__(self, base_atk: float, base_hp: float, base_bonus_stats: StatContainer):
        self.base_atk = base_atk
        self.base_hp = base_hp
        self.base_bonus_stats = base_bonus_stats

        self.buffs = []

        self.game_engine = None
        self.weapon = None
        pass

    def equip_weapon(self, weap):
        self.weapon = weap

    def get_atk(self):
        return self.get_total_base_atk() * self.get_total_stat("atk_pct") + self.get_total_flat_atk("flat_atk")
    
    def get_total_base_atk(self):
        return self.base_atk + self.weapon.base_atk
    
    def get_total_stat(self, stat: str):
        acc = getattr(self.base_bonus_stats, stat) + getattr(self.weapon.base_bonus_stats, stat)
        for buff in self.buffs:
            acc += getattr(buff.bonus_stats, stat)


class Buff:
    def __init__(self, bonus_stats: StatContainer, snappable: bool):
        self.bonus_stats = bonus_stats
        self.snappable = snappable


class Weapon:
    # has stats

    def __init__(self, base_atk, bonus_stats: StatContainer, buffs):
        self.base_atk = base_atk
        self.base_bonus_stats = bonus_stats
        self.buffs = buffs

        self.equipped_character = None

    def equip_to_character(self, char: Character):
        self.equipped_character = char
        char.buffs.extend(self.buffs)
    
class Enemy:

    def __init__(self):
        pass

    def take_incoming_damage(self, damage_object):
        assert self == damage_object.damage_target
        pass