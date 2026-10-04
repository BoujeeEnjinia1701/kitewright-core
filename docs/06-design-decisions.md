---
doc_id: KWC-DEC-001
title: Kitewright Core design decisions register
project: Kitewright Core
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-03'
    author: Amish Chadha
    change: Register opened at TRL 3; decisions D1 to D15 and C1 to C10 made under Amish's 2026-10-03 pre-approval; R9 core mass open for Amish
  - version: "0.2"
    date: '2026-10-03'
    author: Amish Chadha
    change: O1 decided by Amish (option B, KWC-DDR-003) and moved to Decisions made; new open decision O2 (bus headroom for the 14S lithium-ion pack); T10 added for the bonded inserts; value engineering updated
---

# Kitewright Core design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

> **Safety:** Decisions D3, D6 and D7 set the lithium power path, the payload retention and the load path into the frame. Any change to them reopens the build plan's safety stops.

## Open decisions

Proposed, awaiting Amish. O1 (R9 core mass) was decided on 2026-10-03 and is under Decisions made. O2 was raised while applying that round of decisions.

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| O2 | Bus headroom for the 14S lithium-ion ColdCell pack Kitewright Lift adopted (KWL-DDR-003). State: a full 14S pack reads 58.8 V (a full 16S LiFePO4 pack 58.4 V); the power board and power modules (lines 18, 19) are rated 60 V, so 1.2 V is left for the short voltage rise when eight motor controllers brake | A: specify the power board and both power modules for a 75 V class rating (14S to 16S class parts; estimate about USD 40 more, mass unchanged at catalogue class). B: keep 60 V parts and have the Lift packs charged only to 4.10 V a cell (57.4 V; about 3 % less energy, so Lift hover time drops by about 0.6 min). C: keep 60 V parts and full charge, and rely on the controllers' braking limits | **A**: it restores a margin of 16 V at no cost in hover time, and the price difference is small against the core. Proposed, awaiting Amish | BOM lines 18 and 19 (specification and price); bus window text in KWC-REQ-001 | KWC-CAL-001 section C [C3]; `docs/REVIEW.md`, Session 2026-10-03 round 2 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| T1 | DS-014 licence terms | Whether the connector and pinout may be reused in an open design (D12) | KWC-PRB-001 |
| T2 | DS-014 connector part numbers, pinout and current per battery pin | R1 and R4: 100 W at 6S needs 5.6 A across the battery pins | KWC-CAL-001 section C |
| T3 | Flight controller size and mounting pattern | Damping plate holes and lid headroom (5 mm or more) | KWC-DWG-108 |
| T4 | Indexing plunger stroke (at least 9 mm) and pin length | The pin must clear the shoe when withdrawn and enter it 4.5 mm when released | KWC-DWG-105 |
| T5 | Damper hardness for the controller's mass | Vibration isolation | Build plan 3.9 |
| T6 | Power board, power module and radio footprints | Layout inside the lid; clearances checked in the model | `cad/src/model.py` |
| T7 | Clinch nut fit in 2 mm 5052 sheet | Flush seating under the plate | KWC-DWG-101 |
| T8 | Telemetry band and power allowed at the first site (India: 865 to 867 MHz candidate) | Radio choice (D10) | KWC-DDR-001 |
| T9 | Bought-part masses | R9 estimate uses catalogue class values, and the R9 margin is only 4 g | KWC-CAL-001 section H |
| T10 | Bonded flush insert type, bond strength in 2 mm carbon plate and the epoxy's rating from -20 to +45 °C | The inserts hold the lid, the avionics standoffs and the strain-relief bar; they replace clinch nuts, which carbon cannot take | KWC-DDR-003 |

## Value engineering

Value-engineering target: USD 5,000 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 3,944.40 (USD 1,055.60 under the target). Decision O1 added USD 59.80 to the core (mostly the carbon plate, USD 44 more) and moved USD 56 of leads and plugs to the frames. Main cost drivers: the rugged ground station tablet (USD 900), the spares kit (USD 560), the telemetry radio pair (USD 400), the flight controller (USD 390), the field charger (USD 350) and the control handset (USD 250); the made parts cost under USD 70 in all. Savings worth trying: a tablet the team already owns if it is rated to -20 °C, a control link with built-in MAVLink telemetry in place of the separate radio pair (about USD 400), and a smaller spares kit once the first core has flown.

## Decisions made

All decided by Amish under his pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." and "Proceed with the remaining 15 scaffolds".

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-10-03 | D1: PX4 for the whole family; ArduPilot documented as the alternative | Amish (pre-approval) | KWC-DDR-001 |
| 2026-10-03 | D2: Pixhawk FMUv6X class flight controller | Amish (pre-approval) | KWC-DDR-001 |
| 2026-10-03 | D3: 18 to 60 V bus, two pack inputs, two frame outputs, AS150 connectors | Amish (pre-approval) | KWC-DDR-001 |
| 2026-10-03 | D4: one payload class for version 1, 5 kg and 100 W | Amish (pre-approval) | KWC-DDR-001 |
| 2026-10-03 | D5: plain rail, rear entry, front stops, hand-plugged DS-014 pigtail | Amish (pre-approval) | KWC-DDR-001 |
| 2026-10-03 | D6: two independent locking pins with red bands (conservative; a vibration and pull test on the built mount could relax it to one) | Amish (pre-approval) | KWC-DDR-001 |
| 2026-10-03 | D7: core hangs under the frame deck, 220 x 130 mm M4 pattern, 200 x 112 mm deck opening | Amish (pre-approval) | KWC-DDR-001 |
| 2026-10-03 | D8: optional companion computer in its own box on the frame | Amish (pre-approval) | KWC-DDR-001 |
| 2026-10-03 | D9: ColdCell reports over DroneCAN | Amish (pre-approval) | KWC-DDR-001 |
| 2026-10-03 | D10: 900 MHz class radios set per country; India 865 to 867 MHz as first candidate | Amish (pre-approval) | KWC-DDR-001 |
| 2026-10-03 | D11: three altitude parameter bands | Amish (pre-approval) | KWC-DDR-001 |
| 2026-10-03 | D12: proceed with DS-014 and confirm its licence; own open pinout as fallback | Amish (pre-approval) | KWC-DDR-001 |
| 2026-10-03 | D13: first co-design candidate to approach, a university glaciology group in Jammu and Kashmir (not agreed) | Amish (pre-approval) | KWC-DDR-001 |
| 2026-10-03 | D14: log every flight; remote ID module on CAN when required | Amish (pre-approval) | KWC-DDR-001 |
| 2026-10-03 | D15: publish the hover-time model | Amish (pre-approval) | KWC-DDR-001 |
| 2026-10-03 | C1 to C10: design for construction (rail, pins, stops, pigtail, clinch nuts, frame fixing, damping, lid, leads, mast) | Amish (pre-approval) | KWC-DDR-002 |
| 2026-10-03 | O1 (R9 core mass), option B: 2 mm carbon fibre plate, 1.5 mm lid walls, pocketed rail bars, and the pack and frame leads with AS150 plugs moved to each frame's harness; the core keeps solder pads and a strain-relief bar. Core 0.996 kg, R9 met on paper; every strength factor above 5 | Amish, 2026-10-03: "i approve all of the 47 recommendations provided by you. Execute them." | KWC-DDR-003 |

Change log: 2026-10-03, O1 moved from Open decisions to Decisions made (option B); O2 and T10 added.
