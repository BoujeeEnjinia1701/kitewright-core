---
doc_id: KWC-DEC-001
title: Kitewright Core design decisions register
project: Kitewright Core
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-04'
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
    change: O1 decided by Amish as option B (round 2 item 33B, KWC-DDR-003) and moved to Decisions made; new item O2 (R8 harness change) proposed; T7 reworded for the carbon plate; cost updated
  - version: "0.3"
    date: '2026-10-04'
    author: Amish Chadha
    change: O2 decided by Amish as option A (round 3 item 7A, KWC-DDR-004) and moved to Decisions made; R8 restated
---

# Kitewright Core design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

> **Safety:** Decisions D3, D6 and D7 set the lithium power path, the payload retention and the load path into the frame. Any change to them reopens the build plan's safety stops.

## Open decisions

None. Amish decided O2 (R8, the frame harness change) on 2026-10-04 as option A; see Decisions made and KWC-DDR-004. Nothing in carrying it out needs Amish.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| T1 | DS-014 licence terms | Whether the connector and pinout may be reused in an open design (D12) | KWC-PRB-001 |
| T2 | DS-014 connector part numbers, pinout and current per battery pin | R1 and R4: 100 W at 6S needs 5.6 A across the battery pins | KWC-CAL-001 section C |
| T3 | Flight controller size and mounting pattern | Damping plate holes and lid headroom (5 mm or more) | KWC-DWG-108 |
| T4 | Indexing plunger stroke (at least 9 mm) and pin length | The pin must clear the shoe when withdrawn and enter it 4.5 mm when released | KWC-DWG-105 |
| T5 | Damper hardness for the controller's mass | Vibration isolation | Build plan 3.9 |
| T6 | Power board, power module and radio footprints | Layout inside the lid; clearances checked in the model | `cad/src/model.py` |
| T7 | M3 countersunk heads in the 2 mm carbon plate: flush seating and no pull-through (0.4 mm land under each head); bonded flush inserts as the fallback | Flush underside where the shoe slides 0.3 mm below (KWC-DDR-003) | KWC-DWG-101 |
| T8 | Telemetry band and power allowed at the first site (India: 865 to 867 MHz candidate) | Radio choice (D10) | KWC-DDR-001 |
| T9 | Bought-part masses | R9 is met by only 10 g on catalogue class values | KWC-CAL-001 section H |
| T10 | Carbon plate laminate and price from the cutting service (3K twill, quasi-isotropic, 2 mm) | 250 MPa bending and 200 MPa bearing allowables; USD 58 estimate | KWC-CAL-001 section A; `bom/bom.csv` line 1 |

## Value engineering

Value-engineering target: USD 5,000 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 3,946.80 (USD 1,053.20 under the target). Main cost drivers: the rugged ground station tablet (USD 900), the spares kit (USD 560), the telemetry radio pair (USD 400), the flight controller (USD 390), the field charger (USD 350) and the control handset (USD 250); the made parts cost about USD 150 in all, the carbon plate (USD 58) the largest of them. Savings worth trying: a tablet the team already owns if it is rated to -20 °C, a control link with built-in MAVLink telemetry in place of the separate radio pair (about USD 400), and a smaller spares kit once the first core has flown.

## Decisions made

D1 to D15 and C1 to C10 were decided by Amish under his pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." and "Proceed with the remaining 15 scaffolds".

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
| 2026-10-03 | O1 (round 2 item 33B): R9 core mass, option B. Lighter structure (carbon plate with countersunk M3 fixings in place of clinch nuts, pocketed rail bars, 12 mm pin blocks, 12 mm corner spacers, 1.5 mm lid walls) and the power leads and AS150 plugs moved to each frame's harness, with a strain-relief bar on the core: 0.99 kg (R9 met on paper), USD 6.20 more in all. Amish: "i agree with all the 46 recommendations you provided. please proceed." | Amish | KWC-DDR-003 |
| 2026-10-04 | O2 (round 3 item 7A): R8 common core, option A. Accept a bench change of the frame's power harness when a core moves between Lift and Range (lid off, four 8 AWG leads desoldered and the other frame's soldered on, about 30 min); R8 restated as "same core flies Lift and Range with parameter changes and a change of the frame's power harness at the board". No hardware change; R9 stays met. Amish: "For round 3, I agree with all your proposed recommendations" | Amish | KWC-DDR-004 |
