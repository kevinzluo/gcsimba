from entities import StatContainer

class Buff:
    def __init__(self, bonus_stats: StatContainer, snappable: bool, placement_time: int = 0):
        self.bonus_stats = bonus_stats
        self.snappable = snappable
        self.placement_time = placement_time
        self.character = None

    def get_stat(self, stat):
        return getattr(self.bonus_stats, stat)
    
    def set_equipped_character(self, char):
        self.character = char

class RecklessCinnabar(Buff):
    def __init__(self):
        super().__init__(StatContainer(), True, 0)
        # self.character = character
    
    def get_stat(self, stat):
        if stat == "flat_atk":
            atk_mult = 0.8
            if self.character.curr_hp / self.character.get_hp() < 0.5:
                atk_mult += 1
            return self.character.get_hp() * atk_mult / 100
        else:
            return 0
        
class ProtectorsVirtue(Buff):
    def __init__(self):
        super().__init__(StatContainer(), True, 0)

    def get_stat(self, stat):
        if stat == "flat_atk":
            atk_mult = 1.2
            return self.character.get_hp() * atk_mult / 100
        else:
            return 0

class SanguineRouge(Buff):
    def __init__(self):
        super().__init__(StatContainer(), True, 0)

    def get_stat(self, stat):
        if stat == "pyro_bonus":
            if self.character.curr_hp < 0.5 * self.character.get_hp():
                return 33
        return 0

class HydroResonance(Buff):
    def __init__(self):
        super().__init__(
            bonus_stats = StatContainer(
                hp_pct=25,
            ),
            snappable = True,
        )

class ParamitaPapilio(Buff):
    def __init__(self, placement_time):
        super().__init__(StatContainer(), True, placement_time=placement_time)
        self.duration = 9 * 60
    
    def get_stat(self, stat):
        if stat == "flat_atk":
            return min(
                6.26 / 100 * self.character.get_hp() ,
                4 * self.character.get_total_base_atk()
            )
        return 0
