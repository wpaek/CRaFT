import Mathlib

-- Z/2Z stuff
theorem z2_abelian_add (x y : ZMod 2) : x + y = y + x := by
  exact add_comm x y

-- Z/3Z stuff
theorem z3_abelian_add (x y : ZMod 3) : x + y = y + x := by
  exact add_comm x y
