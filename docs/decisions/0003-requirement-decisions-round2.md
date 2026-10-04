---
doc_id: KWC-DDR-003
title: Kitewright Core requirement decisions, round 2
project: Kitewright Core
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Decision O1 (R9 core mass) decided by Amish as recommended, option B, and carried into the model, calculations, BOM, drawings and build plan
---

# 0003: Requirement decisions, round 2

- **Date:** 2026-10-03
- **Status:** Decided. Decided by Amish Chadha on 2026-10-03: "i approve all of the 47 recommendations provided by you. Execute them." Each decision below is the recommended option, exactly as worded, including its conditions.

## Context

The TRL 3 calculations (KWC-CAL-001 v0.1) left one requirement not met on paper: R9, core mass. It was posed to Amish in `docs/REVIEW.md` and in the design decisions register (KWC-DEC-001) as open decision O1, with options and a recommendation. Amish approved every recommendation on 2026-10-03. This record states what was chosen, what it changed and the condition it carries. The decision also changes Kitewright Lift and Kitewright Range, which now own the power leads; the matching record in Kitewright Lift is KWL-DDR-003.

## Options considered

*Table 1. Decision O1 (global decision 17), as posed.*

| Option | What changes | Effect on R9 | Cost | Mass |
| --- | --- | --- | --- | --- |
| A | Lighter structure: 2 mm carbon fibre plate, 1.5 mm lid walls, pocketed rail bars | About 1.12 kg, still not met | About USD 60 more | 157 g less |
| B | A, plus the pack and frame leads and AS150 plugs moved to each frame's harness | About 0.99 kg, met | About USD 60 more on the core; USD 60 of leads move to the frames | 281 g less |
| C | Keep the design as drawn | 1.27 kg, not met | None | None |

## Decision

*Table 2. Decision, effect and condition.*

| # | Requirement | Option chosen | Effect | Condition |
| --- | --- | --- | --- | --- |
| O1 (17) | R9, core mass | **B**: lighter structure (2 mm carbon fibre plate, 1.5 mm lid walls, pocketed rail bars) and the pack and frame leads with their AS150 plugs moved to each frame's harness; the core keeps the power board's solder pads and a strain-relief bar | Core 0.996 kg against the 1.0 kg of R9: met on paper with a 4 g margin (was 1.27 kg). 278 g less: plate 81 g, lid 24 g, rail bars 52 g, leads 121 g net of the 3 g bar, inserts 1 g. Every strength factor stays above 5 (lowest 6.8, the side beam at a pocket). Core cost USD 59.80 more; USD 56 of leads and plugs leave the core; total USD 3,944.40 (was USD 3,940.60) | The decision's own conditions: R9 met with a small margin, every strength factor above 5, and Kitewright Lift and Kitewright Range own their power leads. Both hold on paper. The 4 g margin is inside the accuracy of the catalogue masses, so the built core is weighed at TRL 4 |

## Consequences

- `cad/src/model.py`: the plate is carbon fibre (same 240 x 150 x 2 mm); the spacer bars have three windows each with 1.5 mm walls and the lips three 2 mm pockets underneath, all with at least 4.25 mm of solid bar round every hole; the lid walls and top are 1.5 mm; the leads and AS150 plugs are no longer core parts; a G10 strain-relief bar on two 11 mm posts sits behind the lid; the frame's leads are drawn as context to check that they reach the pads, the grommets and the bar. 646 constructability checks pass.
- Clinch nuts cannot be pressed into carbon plate, so the 14 clinch nuts become 16 bonded flush inserts (two more for the bar posts). They sit flush underneath, where the shoe runs 0.3 mm below the plate. This is a direct consequence of the carbon plate; it is listed as a new item to confirm (KWC-DEC-001, To confirm, T10).
- `docs/04-calcs/sizing.py` and KWC-CAL-001 v0.2: sections A and H recalculated; R9 now met on paper; the lowest strength factor is 6.8.
- `bom/bom.csv`: line 1 carbon plate (USD 62), lines 3 and 4 pocketed (USD 7 and USD 8 each), line 10 lid (USD 5), line 20 bonded inserts (16 at USD 0.65, estimate), line 21 strain-relief bar (USD 4) in place of the leads and plugs.
- KWC-DWG-001 to Rev P2; making sketches KWC-DWG-101, 102, 104 and 107, the overview, joints 5 and 6 and steps 3, 7 and 9 redrawn; build plan KWC-BLD-001 v0.2.
- Kitewright Lift and Kitewright Range: each frame's harness gains two pack input leads and two frame output leads of 8 AWG with AS150 plugs, soldered to the core's pads and tied to its strain-relief bar (Lift: KWL-DDR-003). The interface the frames see is otherwise unchanged.
- New question raised while applying the decision (KWC-DEC-001, O2, proposed, awaiting Amish): the 14S lithium-ion pack Kitewright Lift adopted charges to 58.8 V, 1.2 V under the 60 V rating of the power board and power modules.

> **Safety:** The core still switches up to 60 V and 200 A. With the leads in the frame harness, the polarity and the opposite-gender keying of the pack inputs and frame outputs are checked when the harness is soldered in (build plan step 9, hold point), before any pack is connected. Carbon dust from drilling or cutting the plate is a breathing hazard and carbon conducts: drill wet or under extraction and seal the cut edges so no fibres can bridge the power board.
