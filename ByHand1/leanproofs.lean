-- Z/2Z stuff
def rels_z2 : Set (FreeGroup (Fin 1)) :=
  {(FreeGroup.of (0 : Fin 1) ^ (2 : ℤ))}

theorem group_z2_abelian :
  ∀ x y : PresentedGroup rels_z2, x * y = y * x := by
  -- todo: fill this in later
  sorry

-- Z/3Z stuff
def rels_z3 : Set (FreeGroup (Fin 1)) :=
  {(FreeGroup.of (0 : Fin 1) ^ (3 : ℤ))}

theorem group_z3_abelian :
  ∀ x y : PresentedGroup rels_z3, x * y = y * x := by
  -- todo: fill this in later
  sorry
