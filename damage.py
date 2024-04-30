from auras import AuraEngine
import random

# source type: transformative, nontransformative: normal, burst, skill, charge
# if nontransformative, damage subtype is pyro/hydro/electro/phys etc
class DamageObject:
    def __init__(self, damage_owner, damage_source_type, damage_source_subtype, damage_target, multiplied_stat, icd_tag):
        self.damage_owner = damage_owner
        self.damage_source_type = damage_source_type
        self.damage_source_subtype = damage_source_subtype
        self.multiplied_stat = multiplied_stat
        self.damage_target = damage_target
        self.icd_tag = icd_tag

    # def calc_damage(self):
    #     if self.damage_source_type == "transformative":
    #         return self.calc_transformative_damage()
    #     else:
    #         return self.calc_nontransformative_damage()

    # def calc_transformative_damage(self):
    #     assert self.damage_source_type == "transformative"
    #     assert False, "i didn't implement this lol"

    # def calc_nontransformative_damage(self):
    #     # return a number
    #     assert self.damage_source_type != "transformative"
    #     res = self.damage_target.res[self.damage_source_subtype]
    # what about li
    #     return 100


class DamageEngine:
    def __init__(self, owner_object):
        self.aura_engine = AuraEngine
        self.owner_object = owner_object

    def process_damage_object(self, damage_object: DamageObject):
        print("Processing damage object")
        # damage formula finally
        # reference: https://library.keqingmains.com/combat-mechanics/damage/damage-formula
        if damage_object.damage_source_type == "transformative":
            assert False

        res = self.owner_object.res[damage_object.damage_source_subtype]

        def calculate_enemy_res_mult(resistance):
            if resistance < 0:
                return 1 - resistance / 2
            elif 0 <= resistance < 0.75:
                return 1 - resistance
            else:
                return 1 / (4 * resistance + 1)
            
        res_mult = calculate_enemy_res_mult(res / 100)

        # this is somewhat more complicated but here it is simplified
        # damage_object.damage_source_type contains things like NA damage, Ca damage, burst damage, skill damage
        # damage_object.damage_source_subtype contains the elemental type
        # first part is not implemented yet

        dmg_bonus_mult = 1 + damage_object.damage_owner.get_total_stat(damage_object.damage_source_subtype + "_bonus") / 100 # + damage_object.damage_owner.get_total_stat

        # now measure if crit or not
        cr = damage_object.damage_owner.get_total_stat("cr") / 100
        did_crit = (random.uniform(0, 1) < (cr))

        crit_mult = 1
        if did_crit:
            crit_mult += damage_object.damage_owner.get_total_stat("cd") / 100

        # print(damage_object.multiplied_stat)

        damage_total = dmg_bonus_mult * res_mult * crit_mult * damage_object.multiplied_stat
        print(f"Dealt {damage_total}, crit = {did_crit}")

        return damage_total, did_crit



