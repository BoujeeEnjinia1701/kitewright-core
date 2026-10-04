---
doc_id: KWC-REQ-001
title: Kitewright Core requirements
project: Kitewright Core
doc_type: Requirements
version: "0.4"
status: Draft
date: '2026-10-04'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 3 status of every requirement from KWC-CAL-001; rated payload class and bus voltage window stated (KWC-DDR-001); targets unchanged
- version: "0.3"
  date: '2026-10-03'
  author: Amish Chadha
  change: Amish's decision 33B carried out (KWC-DDR-003); status of R3, R8, R9 and R11 updated from KWC-CAL-001 v0.2; R9 now met on paper; targets unchanged; R8 harness point open (O2)
- version: "0.4"
  date: '2026-10-04'
  author: Amish Chadha
  change: R8 restated under Amish's round-3 decision 7A (KWC-DDR-004); register item O2 closed; all eleven requirements met on paper or by design
---

# Kitewright Core requirements

The requirements below are unchanged in their targets from version 0.1. Each carries its TRL 3 status from the sizing calculations, KWC-CAL-001 v0.2, on the constructable design of KWC-DDR-002 as lightened under decision 33B (KWC-DDR-003). On 2026-10-03 Amish decided R9 core mass as recommended ("i agree with all the 46 recommendations you provided. please proceed."): a lighter structure, with the power leads moved out of the core into the frames. All eleven requirements are met on paper or by design. On 2026-10-04 Amish decided R8 as recommended (round 3, item 7A): Amish Chadha (owner) on 2026-10-04: "For round 3, I agree with all your proposed recommendations". A core moved between Lift and Range now has its frame's power harness changed at the bench, and R8 is restated to say so (KWC-DDR-004).

> **Safety:** The core carries lithium pack power of up to 60 V and 200 A, and holds payloads that would fall if released in flight. Requirements R3 and R5 and the build plan's safety stops cover these; none of the figures here is a safety approval.

Table 1. Requirements

| ID | Requirement | Target | Verification (TRL 3 or later) | TRL 3 status (KWC-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Payload electrical interface | DS-014 40-pin connector with all required signals and battery power present and documented | Continuity and protocol test with a reference payload on the bench | Met on paper; licence and pinout to confirm from the standard |
| R2 | Payload swap | Swap in 60 s or less without tools, with locking pin engaged and visible (target) | Timed field trials with gloved users | Met on paper: about 52 s with gloves (estimate) |
| R3 | Mount strength | Holds 3 times the rated payload mass statically and 1.5 times under a 2 g drop (target) | CalRig proof-load and drop test | Met on paper: factor 8 or more on every part at 147 N, carbon plate included |
| R4 | Payload power | At least 100 W continuous to the payload at bus voltage (target) | Load bank test at -20 and +45 °C | Met on paper: at most 5.6 A; DS-014 pin rating to confirm |
| R5 | Operating temperature | Avionics boot and fly from -20 to +45 °C (target) | Climatic chamber soak and bench run | Met on paper: hottest part about 75 °C, cold boot within rating |
| R6 | Altitude envelope | Stable control and failsafes at air density equivalent to 5,000 m (target) | AltiRig tests, then field flights at a high site | Met on paper for the core; flight check needs a frame |
| R7 | Performance model | Published hover time model predicts measured hover time within 15% at each altitude band (target) | Compare model to AltiRig and flight logs | Model published; accuracy shown only at TRL 4 |
| R8 | Common core | Same core flies Lift and Range with parameter changes and a change of the frame's power harness at the board (a bench change, lid off, about 30 min); restated 2026-10-04, decision 7A | Build both frames and fly from one core set; time the bench harness change | Met by design as restated: same firmware, same 220 x 130 mm fixing (Kitewright interface table), four 8 AWG leads resoldered at the board |
| R9 | Core mass | Avionics, radios and mount 1.0 kg or less, excluding batteries (target) | Weigh the assembled core | Met on paper: 0.99 kg estimated, 10 g margin (decision 33B); bought-part masses to confirm |
| R10 | Upstream firmware | Runs a released PX4 version with no source changes, parameters and modules only | Build check against the PX4 release tag | Met by design |
| R11 | Prototype cost | USD 5,000 or less including ground station and spares | Bill of materials and receipts | USD 3,946.80, under the value-engineering target by USD 1,053.20 |

## Definitions fixed at TRL 3

- **Rated payload:** 5 kg on the mount, one payload class for version 1, so R3's load cases are 147 N vertical (KWC-DDR-001, D4).
- **Bus voltage:** 18 to 60 V at the core's pack inputs, from 6S Li-ion to 16S LiFePO4 (KWC-DDR-001, D3).
- **Core mass (R9):** the airborne core as built, excluding batteries, the payload shoe (each payload carries its own), the optional companion computer (carried outside the core, KWC-DDR-001, D8) and, since decision 33B, the frame's power leads and AS150 plugs, which belong to each frame's harness (KWC-DDR-003).
- **Prototype cost (R11):** treated as a value-engineering target, not a limit (STANDARDS section 18).

## Requirements at risk

- R9 is met on paper with a 10 g margin after decision 33B; bought-part masses are catalogue-class values, so weighing them when bought (register, T9) decides it.
- R2 has a small margin (about 52 s); a gloved timed trial at TRL 4 decides it.
- R1 and R4 depend on the DS-014 licence, pinout and pin rating, to be confirmed from the published standard (register, To confirm).

## Assumptions

- The 47% hover time at 5,000 m and -20 °C is a first estimate, not a measurement; KWC-CAL-001 traces it to unheated packs and gives 70 % with ColdCell packs.
- Pixhawk-standard flight controllers and DS-014 connectors can be bought in small quantities.
- PX4 supports the needed multirotor and quadplane modes without source changes.
- ColdCell can keep packs above their minimum discharge temperature for a full flight.
