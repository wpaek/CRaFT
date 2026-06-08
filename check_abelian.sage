import sys
import os
import signal


# timeout in Docker: -e ORDER_TIMEOUT=...
ORDER_TIMEOUT = int(os.environ.get("ORDER_TIMEOUT", "10"))

# Group finiteness GAP can take too long
def on_alarm(signum, frame):
    raise TimeoutError
signal.signal(signal.SIGALRM, on_alarm)

gens = sys.argv[1].split(",")
F = FreeGroup(gens)
name_to_gen = {g: F.gen(j) for j, g in enumerate(gens)}

# Swap ^ to **.
relations = [eval(r.replace("^", "**"), {}, name_to_gen)
             for r in sys.argv[2].split(",")]
G = F / relations

signal.alarm(ORDER_TIMEOUT)
try:
    order = G.order()
except BaseException:
    order = "timeout"
finally:
    signal.alarm(0)

ai = G.abelian_invariants()
if 0 in ai:
    ab_order = Infinity
elif len(ai) == 0:
    ab_order = 1
else:
    ab_order = prod(ai)

if order == "timeout":
    abelian = "?"
else:
    abelian = "yes" if order == ab_order else "no"

print(order, ab_order, abelian)
