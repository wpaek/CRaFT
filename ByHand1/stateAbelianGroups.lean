-- Z/2Z stuff
def rels_z2 : Set (FreeGroup (Fin 1)) :=
  {(FreeGroup.of (0 : Fin 1) ^ (2 : ℤ))}

theorem group_z2_abelian :
  ∀ x y : PresentedGroup rels_z2, x * y = y * x := by
  sorry

-- Z/3Z stuff
def rels_z3 : Set (FreeGroup (Fin 1)) :=
  {(FreeGroup.of (0 : Fin 1) ^ (3 : ℤ))}

theorem group_z3_abelian :
  ∀ x y : PresentedGroup rels_z3, x * y = y * x := by
  sorry

-- Klein 4 group stuff
def rels_klein4 : Set (FreeGroup (Fin 2)) :=
  {(FreeGroup.of (0 : Fin 2) ^ (2 : ℤ)),
   (FreeGroup.of (1 : Fin 2) ^ (2 : ℤ)),
   (FreeGroup.of (0 : Fin 2)) * (FreeGroup.of (1 : Fin 2)) * (FreeGroup.of (0 : Fin 2) ^ (-1 : ℤ)) * (FreeGroup.of (1 : Fin 2) ^ (-1 : ℤ))}

theorem group_klein4_abelian :
  ∀ x y : PresentedGroup rels_klein4, x * y = y * x := by
  sorry
