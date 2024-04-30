# how i see this working

from engine import GameEngine
from entities import TestDummy, StatContainer
from buffs import HydroResonance
from hutao import HuTao, StaffOfHoma

ge = GameEngine()

ht_artifact_stats = StatContainer(
    cr = 41.6 + 31.1,
    cd = 67.6,
    atk_pct=9.3,
    hp_pct=26.8 + 46.6,
    em=107,
    flat_atk=33 + 311,
    flat_hp=269 + 4780,
    pyro_bonus=15 + 46.6,
)
ht = HuTao(level = 90, artifact_stats=ht_artifact_stats, buffs = [HydroResonance()])
print(ht.buffs)

homa = StaffOfHoma()

ht.equip_weapon(homa)

print(ht.get_hp())
print(ht.get_atk())
print(ht.get_total_stat("pyro_bonus"))

ge.load_party([ht])

test_dummy = TestDummy()

ge.load_enemy(test_dummy)

ht.skill()
ht.normal()
ht.normal()
ht.normal()
ht.normal()
ht.normal()
ht.normal()
ht.normal()
ht.normal()
ht.normal()
ht.normal()
ht.normal()
ht.normal()
ht.normal()
ht.normal()
ht.normal()
ht.normal()
ht.normal()
ht.normal()
ht.normal()
ht.normal()
ht.normal()
ht.normal()
ht.normal()
ht.normal()
ht.normal()

ge.flush()

print(test_dummy.damage_taken)
# ht.normal()
# ht.normal()
# ht.normal()
# ht.normal()
# ht.normal()



# by end of today, hopefully can queue up like 5 attacks or an n2c, with their damage output
# print(ht.buffs[1].get_stat("flat_atk"))

# xq_artifact_stats = StatContainer(
#     cr = 44.7,
#     cd = 46.6,
#     atk_pct = 29.2,
#     em = 21,
#     er = 29.2,
#     flat_atk=27,
# )

# xq = XingQiu(level = 90, artifact_stats=xq_artifact_stats, buffs = [])



# print(xq.get_atk())
# print()

# td = TestDummy()

# ge.load_party([xq, ht])
# ge.load_enemy(td)



# xq.skill()
# ge.swap_to(ht)
# ht.skill()
# ht.normal(n = 1)

# ge.clear()

# diags = ge.get_diagostics()
# print(diags)

# xq.skill() # ooh particle collection delay needs to be a thing for prefunnel
# xq.ult()
# ge.swap_to(ht)
# ht.skill()
# ht.normal(n = 2)
# ht.charge()
# ht.dash()
# ht.normal(n = 2)
# ht.charge()
# ht.dash()
# # blah blah
# ht.ult()

# prints out a result