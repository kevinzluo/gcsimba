# how i see this working

from engine import GameEngine
from entities import TestDummy, HuTao, XingQiu

ge = GameEngine()

ht = HuTao(arti stats here, weapon equipment, etc)
xq = XingQiu(same as above)
td = TestDummy(res or whatever)

ge.load_party([xq, ht])
ge.load_enemy(td)

xq.skill()
ge.swap_to(ht)
ht.skill()
ht.normal(n = 1)

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