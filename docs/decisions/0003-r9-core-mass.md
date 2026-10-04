---
doc_id: KWC-DDR-003
title: Kitewright Core R9 core mass, lighter structure and power leads in the frames
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
  change: Amish's decision 33B (option B of register item O1) recorded and carried out
---

# 0003: R9 core mass: lighter structure, power leads moved to the frames

- **Date:** 2026-10-03
- **Status:** accepted. Decided by Amish Chadha on 2026-10-03, round 2 item 33B: "i agree with all the 46 recommendations you provided. please proceed."

## Context

The constructable core of KWC-DDR-002 was estimated at 1.27 kg against R9's 1.0 kg (KWC-CAL-001 v0.1, section H). Its plate, rails, pin blocks and lid were sized for making from aluminium sheet and bar, with strength factors of 10 to 99, and the four 8 AWG power leads with their AS150 plugs (124 g) sat inside the core. The item was put to Amish as register item O1 with three options.

## Options considered

| Option | What changes | Effect on R9 | Cost |
| --- | --- | --- | --- |
| A | Lighter structure: carbon fibre plate, 1.5 mm lid walls, pocketed rail bars | Still not met (about 1.12 kg) | About USD 60 more |
| B | A, plus the pack and frame leads and AS150 plugs moved to each frame's harness; the core keeps solder pads and a strain-relief bar | Met (about 0.99 kg) | About USD 60 more on the core; USD 60 of leads move to the frames |
| C | Keep the design as drawn | Not met (1.27 kg) | None |

## Decision

Option B, as recommended. Carried out as follows (model `cad/src/model.py`, 720 constructability checks, all passing):

| # | Part | Was | Now | Mass saved |
| --- | --- | --- | --- | --- |
| L1 | Core plate | 2 mm 5052 aluminium with 14 pressed clinch nuts | 2 mm carbon fibre plate, CNC-cut; 16 M3 holes countersunk from below; M3 countersunk screws set from below with thread-locker carry the standoffs and act as the lid's studs (nylon-insert nuts on the flange). Clinch nuts cannot be pressed into carbon | 81 g |
| L2 | Rail spacer bars | Solid 10 x 6 mm bar | Three 3.6 mm windows between the screws, 1.2 mm flanges left; clear-anodised | 24 g |
| L3 | Rail lips | Solid 30 x 3 mm bar | Three pockets 1.8 mm deep under each lip between the screws, stopping 2 mm short of the spacer bar | 20 g |
| L4 | Pin blocks | 30 x 15 mm bar | 30 x 12 mm bar (12 mm of M10 x 1 thread); M4 x 30 screws | 12 g |
| L5 | Corner spacers | 16 mm OD | 12 mm OD, anodised | 8 g |
| L6 | Lid | 2 mm walls and top | 1.5 mm walls and top | 24 g |
| L7 | Power leads and AS150 plugs | Four 8 AWG leads and four AS150 halves in the core (BOM line 21, USD 60) | Supplied by each frame's harness (Kitewright Lift and Range); they enter through the existing grommets and solder to the board's pads | 124 g |
| L8 | Strain-relief bar (new, BOM line 21) | None | 60 x 8 x 2 mm G10 bar on two 12 mm standoffs behind the lid; the frame's leads are tied to it (KWC-DWG-109) | -9 g with the fixings |

L4 and L5 go a little beyond the three items named in option A. They were needed to reach option B's 0.99 kg in the model, and they are part of the same lighter structure.

## Results (KWC-CAL-001 v0.2)

- **R9:** 0.99 kg estimated, 10 g inside 1.0 kg. Met on paper; the margin is thin against catalogue-class bought-part masses (register, T9).
- **R3:** still met. Lips 19 x at the pocket floor, screws 69 x, carbon side beam 8.3 x on a 250 MPa allowable, carbon bearing 14 x at the pin block screws.
- **R11:** USD 3,946.80, USD 6.20 more than before (structure about USD 58, strain-relief bar USD 8, fixings USD 0.80 less, leads USD 60 moved out). Value-engineering target: USD 5,000. Estimated cost of the constructable design: USD 3,946.80 (USD 1,053.20 under the target).
- **R8:** firmware and fixing unchanged, but a core moved between Lift and Range now needs the frame's soldered harness changed. Put to Amish as register item O2.

## Consequences

- Kitewright Lift and Kitewright Range supply their own pack and output leads (8 AWG) with AS150 plugs, inputs and outputs of opposite gender, long enough to reach the board's pads through the core's rear grommets (cross-repo; not edited here).
- Galvanic corrosion: aluminium parts that touch the carbon plate (spacer bars, front stops, corner spacers, standoffs) are anodised; the plate's cut edges are sealed with epoxy.
- M4 nuts on the carbon plate sit on washers and are tightened to about 2 N·m so they do not crush the laminate.
- The countersinks leave 0.4 mm of plate under each M3 head. If the heads pull through or the laminate cracks at TRL 4, the fallback is bonded flush inserts (register, T7).
- Making sketches KWC-DWG-101, 102, 104, 105 and 107 go to Rev P2. KWC-DWG-109 is new. The general arrangement KWC-DWG-001 goes to Rev P2.
