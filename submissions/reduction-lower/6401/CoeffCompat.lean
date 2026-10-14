import ProximityPrize.Benchmark.TargetLower

/-!
# `MvPolynomial.coeff` compatibility

`MvPolynomial.coeff` took the monomial first. Mathlib has since made `coeff` the
`AddMonoidAlgebra` projection, so the coefficient is `p.coeff m` and the old
constant no longer exists. Several modules here use it partially applied -- under
`congrArg`, for instance -- so flipping the arguments at each call site is not a
textual rewrite. This keeps the original name and argument order.
-/

namespace MvPolynomial

abbrev coeffAt {sigma R : Type*} [CommSemiring R]
    (m : sigma →₀ ℕ) (p : MvPolynomial sigma R) : R :=
  p.coeff m

end MvPolynomial
