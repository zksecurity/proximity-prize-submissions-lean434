# Proximity Prize submissions on Lean 4.34

Five leading [Proximity Prize](https://github.com/proximity-prize/proximity-prize) submissions,
ported from Lean 4.32.2 to Lean 4.34.0 and re-verified at the scores they held: four steps of the
reduction-lower lineage and the leading reduction-upper proof.

The 4.34 upgrade moved the toolchain, Mathlib, ArkLib and CompPoly together, which invalidated
every existing proof. These ports keep the proofs as their authors wrote them. The edits are
confined to what the new libraries renamed or restated underneath them, plus a few raised
elaboration budgets.

| track | submission | claim | score | origin |
|---|---|---|---|---|
| `proximity-prize-reduction-lower` | [`6401`](submissions/reduction-lower/6401) | `ProtocolClaim 6401 307163 1048576` | 64.01 bits | `proximity-prize@b3fac81a` |
| `proximity-prize-reduction-lower` | [`6812`](submissions/reduction-lower/6812) | `ProtocolClaim 6812 331243519 1073741824` | 68.12 bits | `proximity-prize@0275bb59` |
| `proximity-prize-reduction-lower` | [`6813`](submissions/reduction-lower/6813) | `ProtocolClaim 6813 331284479 1073741824` | 68.13 bits | `proximity-prize@a4a66a15` |
| `proximity-prize-reduction-lower` | [`6815`](submissions/reduction-lower/6815) | `ProtocolClaim 6815 331366399 1073741824` | 68.15 bits | `proximity-prize@ed2b68c4` |
| `proximity-prize-reduction-upper` | [`11613`](submissions/reduction-upper/11613) | `ProtocolClaimUpper 11613 122369` | 116.13 bits | |

Each directory is a submission source tree as the verifier receives it, flat, with the claim
files the challenge requires (`score.txt` with `radius.txt` on the lower track, `unsafe-index.txt`
on the upper). They are not a buildable project on their own: they import the challenge's
`ProximityPrize.Benchmark.*` modules and each other as `ProximityPrize.SubmissionLower.*`
(`SubmissionUpper.*` for upper).

## How they were ported

**6815 and 11613** were ported by hand against the 4.34 Mathlib and ArkLib: renamed lemmas, a
handful of restated APIs (`AddMonoidAlgebra` became a structure, so `MvPolynomial.coeff m p`
became `p.coeff m`; `Finsupp.mapDomain_apply` became `mapDomain_apply_of_injective`), proofs that
`simp` or `omega` no longer closed rewritten with `interval_cases` and `decide`, and raised
elaboration budgets on five declarations.

**6401** carried 124 vendored Mathlib backports (`LocalMathlib_*`) among its 228 files. 118 of
them were fully upstream in 4.34 and only collided with it, so each became
`import Mathlib.<Path>`; that took 112 build errors to 6, and the rest were the same API drift as
above.

**6812 and 6813** are 6815's ancestors in the same lineage, but share almost no file with it:
6815 merged their modules into new ones. They were ported by carrying 6815's own port across:

1. A three-way merge (`git merge-file`) of 6815's port into the four files the trees share by
   name, `LowerFoundation.lean` among them. No conflicts.
2. [`tools/declport.py`](tools/declport.py), which aligns 6815's 4.32 and 4.34 trees one
   top-level declaration at a time and replays every changed declaration wherever its old text
   appears verbatim. 153 rules.
3. Four edits by hand, each one 6815's port had already made somewhere else: a `simpa` replaced
   by `exact`; a `convert … using k` fallback chain where a `simpa` met an instance mismatch; and
   in `MovingFiberScalar6811` the frozen-interpolant lemma restated in `RCN279`'s form, with a
   bridging lemma `homogenizedTranslation_rcn319` proved by `rfl` at abstract points. Comparing
   the two identical-but-separate translations inside the numeral-heavy proof exhausted Lean
   4.34's recursion limit, and `convert` there ran out of memory.

## Verifying

Every port was checked against the Proximity Prize 4.34 challenge with these pins:

| | revision |
|---|---|
| Lean | `leanprover/lean4:v4.34.0` |
| ArkLib | [`Verified-zkEVM/ArkLib@34a834c6`](https://github.com/Verified-zkEVM/ArkLib/commit/34a834c61c859cc04205f5f43fd237cda8fb0da4) |
| CompPoly | [`zksecurity/CompPoly@411708c`](https://github.com/zksecurity/CompPoly/commit/411708c17175) |
| Comparator | [`leanprover/comparator@d03acab1`](https://github.com/leanprover/comparator/commit/d03acab154d2) |

To check one, place its directory at `ProximityPrize/SubmissionLower` (or `SubmissionUpper`) in
the challenge project, build it, and run Comparator against the challenge's target theorem. Each
builds cleanly, its `ProximityPrize.Benchmark.candidate` depends on exactly `propext`,
`Classical.choice` and `Quot.sound`, and a full cold kernel replay accepts it. The 6815 replay
takes 2h25m of CPU against the challenge's four-hour limit.

CompPoly is pinned at `zksecurity/CompPoly@411708c` because its KoalaBear Rabin certificates are
replay-safe; at the upstream revision the same replay does not terminate (see
[Verified-zkEVM/CompPoly#396](https://github.com/Verified-zkEVM/CompPoly/pull/396)).

## License

Apache License 2.0; see [`LICENSE`](LICENSE). The submissions are their authors' work and come
from [proximity-prize/proximity-prize](https://github.com/proximity-prize/proximity-prize), which
publishes them under the same license; the ports and `tools/` are released under it too.
