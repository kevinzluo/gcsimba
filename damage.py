class DamageObject:
    def __init__(self, damage_owner, damage_source_type, damage_source_subtype, damage_target, damage_multiplier = None):
        self.damage_owner = damage_owner
        self.damage_source_type = damage_source_type
        self.damage_source_subtype = damage_source_subtype
        self.damage_multipler = damage_multiplier
        self.damage_target = damage_target

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
    #     return 100

