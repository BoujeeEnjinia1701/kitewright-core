---
doc_id: KWC-DDR-002
title: Kitewright Core design for construction
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
  change: Changes that make the concept physically buildable, with the reason for each; decided under Amish's 2026-10-03 pre-approval
---

# 0002: Design for construction

- **Date:** 2026-10-03
- **Status:** accepted. Decided by Amish under his pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." and "Proceed with the remaining 15 scaffolds".

## Context

The scaffold described the core in words only: a stack that bolts into any frame, a payload mount of "a plain rail with a locking pin" and a DS-014 connector. It had no geometry, so nothing in it had been checked for how it is made or how it fixes to its neighbours. Writing the build plan (STANDARDS section 18) turned that description into parts that can be cut, drilled, printed or bought, and that fasten to each other. Amish's rule for this step (2026-09-30): "fix the design assumptions to match and be physically feasible". Every change keeps what the core does, its pitch and its patent design-arounds. The safety case is strengthened, not weakened: the second locking pin (KWC-DDR-001, D6) is part of it.

The model in `cad/src/model.py` runs 614 constructability checks (`python cad/src/model.py --check`): no two parts overlap, every part that must rest on another touches it, the shoe clears the plate by at least 0.25 mm and the spacer bars by 0.9 mm, the flight controller clears the lid by 5 mm, nothing but the corner spacers touches the frame deck, and nothing of the core enters the payload's neck zone below the lips. All pass.

## Decision

*Table 1. Changes from the concept to the constructable design.*

| # | Component | The concept had | The constructable design has | Why |
| --- | --- | --- | --- | --- |
| C1 | Payload rail | "A plain rail" with no shape | Two 200 mm rails, each a 10 x 6 mm spacer bar and a 30 x 3 mm lip bolted under the plate; 0.7 mm UHMW tape on the lips; shoe 5 mm thick, 0.3 mm gap above it, 1 mm at each side | Stock bar and sheet, drilled and screwed; the gap is set by stock thicknesses, not by machining |
| C2 | Locking pin | "A locking pin" | Two M10 x 1 indexing plungers in 28 x 30 x 15 mm blocks under the lips at the rear; 5 mm pins through 5.5 mm holes in lip, tape and shoe | A bought plunger needs a threaded block; under the lip it stays outside the payload's neck zone |
| C3 | End of travel | None | Two 12 mm front stops between plate and lip at the front of each rail, held by the rail's own screws | Aligns the pins with their holes without extra fixings |
| C4 | Payload connector | "A DS-014 connector" on the mount | A 0.3 m pigtail down through a 12 x 24 mm slot in the plate and an 18 x 28 mm notch in the shoe's front edge; plug pushed into the payload's socket by hand | A sliding shoe cannot mate a 40-pin connector reliably; the notch lets the shoe pass the cable |
| C5 | Fixings under the plate | Not shown | M3 self-clinching nuts pressed in from below, flush underneath, for the lid, standoffs and power board | The shoe slides 0.3 mm under the plate, so nothing may stand proud there |
| C6 | Core to frame | "Bolts into any frame" | Plate hangs under the deck on four M4 bolts on 220 x 130 mm with 16 x 8 mm spacers; lid rises through a 200 x 112 mm deck opening | Gives the rail a clear path under the frame and puts payload load into the frame's hard points |
| C7 | Flight controller mounting | Not shown | Four 25 mm standoffs, four silicone dampers, a 2 mm G10 damping plate; controller on nylon screws above the power board | Vibration isolation, and room for the power board beneath |
| C8 | Avionics cover | "Cold-rated avionics enclosure" | Printed ASA lid 168 x 92 x 62 mm with a 180 x 108 mm flange on a 1 mm foam gasket, six M3 screws on the long sides only | The flange clears the front stop nuts and the frame deck opening |
| C9 | Power leads | Not shown | Four 8 AWG leads out through two rubber grommets in the lid's rear wall; AS150 plugs soldered after the lid is on | A plug will not pass a grommet; soldering last avoids a split grommet |
| C10 | GNSS | "Mast-mounted" | Removable 10 mm carbon tube in a printed boss on the lid, GNSS 231 mm above the plate, thumbscrew | Clear of power wiring; comes off for transport |

## Consequences

- `cad/src/model.py`, the STEP and STL exports, drawing KWC-DWG-001 Rev P1, the making sketches KWC-DWG-101 to 108, the build plan pictures and the concept media are all generated from the changed model.
- `bom/bom.csv` gains the spacer bars, lips, tape, stops, pin blocks, second plunger, clinch nuts, damping parts, gasket and grommets.
- KWC-CAL-001 uses the changed geometry. The structure sized for making in sheet and bar weighs more than R9 allows; that is put to Amish in `docs/REVIEW.md`, not decided here.
- The frame interface of C6 is a shared assumption with Kitewright Lift and Kitewright Range (Cross-repo actions in `docs/REVIEW.md`).
