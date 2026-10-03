---
doc_id: KWC-REQ-001
title: Kitewright Core requirements
project: Kitewright Core
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-10-03'
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
---

# Kitewright Core requirements

The requirements below are unchanged in their targets from version 0.1. Each now carries its TRL 3 status from the sizing calculations, KWC-CAL-001, on the constructable design of KWC-DDR-002. Ten are met on paper or by design; one, R9 core mass, is not met and is set out for Amish's decision in `docs/REVIEW.md`.

> **Safety:** The core carries lithium pack power of up to 60 V and 200 A, and holds payloads that would fall if released in flight. Requirements R3 and R5 and the build plan's safety stops cover these; none of the figures here is a safety approval.

Table 1. Requirements

| ID | Requirement | Target | Verification (TRL 3 or later) | TRL 3 status (KWC-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Payload electrical interface | DS-014 40-pin connector with all required signals and battery power present and documented | Continuity and protocol test with a reference payload on the bench | Met on paper; licence and pinout to confirm from the standard |
| R2 | Payload swap | Swap in 60 s or less without tools, with locking pin engaged and visible (target) | Timed field trials with gloved users | Met on paper: about 52 s with gloves (estimate) |
| R3 | Mount strength | Holds 3 times the rated payload mass statically and 1.5 times under a 2 g drop (target) | CalRig proof-load and drop test | Met on paper: factor 10 or more on every part at 147 N |
| R4 | Payload power | At least 100 W continuous to the payload at bus voltage (target) | Load bank test at -20 and +45 °C | Met on paper: at most 5.6 A; DS-014 pin rating to confirm |
| R5 | Operating temperature | Avionics boot and fly from -20 to +45 °C (target) | Climatic chamber soak and bench run | Met on paper: hottest part about 75 °C, cold boot within rating |
| R6 | Altitude envelope | Stable control and failsafes at air density equivalent to 5,000 m (target) | AltiRig tests, then field flights at a high site | Met on paper for the core; flight check needs a frame |
| R7 | Performance model | Published hover time model predicts measured hover time within 15% at each altitude band (target) | Compare model to AltiRig and flight logs | Model published; accuracy shown only at TRL 4 |
| R8 | Common core | Same core flies Lift and Range with parameter changes only | Build both frames and fly from one core set | Met by design |
| R9 | Core mass | Avionics, radios and mount 1.0 kg or less, excluding batteries (target) | Weigh the assembled core | Not met: 1.27 kg estimated (Decisions for Amish) |
| R10 | Upstream firmware | Runs a released PX4 version with no source changes, parameters and modules only | Build check against the PX4 release tag | Met by design |
| R11 | Prototype cost | USD 5,000 or less including ground station and spares | Bill of materials and receipts | USD 3,940.60, under the value-engineering target by USD 1,059.40 |

## Definitions fixed at TRL 3

- **Rated payload:** 5 kg on the mount, one payload class for version 1, so R3's load cases are 147 N vertical (KWC-DDR-001, D4).
- **Bus voltage:** 18 to 60 V at the core's pack inputs, from 6S Li-ion to 16S LiFePO4 (KWC-DDR-001, D3).
- **Core mass (R9):** the airborne core as built, excluding batteries, the payload shoe (each payload carries its own) and the optional companion computer (carried outside the core, KWC-DDR-001, D8).
- **Prototype cost (R11):** treated as a value-engineering target, not a limit (STANDARDS section 18).

## Requirements at risk

- R9 is not met on paper; options and a recommendation are in `docs/REVIEW.md`, TRL 3 section, Decisions for Amish.
- R2 has a small margin (about 52 s); a gloved timed trial at TRL 4 decides it.
- R1 and R4 depend on the DS-014 licence, pinout and pin rating, to be confirmed from the published standard (register, To confirm).

## Assumptions

- The 47% hover time at 5,000 m and -20 °C is a first estimate, not a measurement; KWC-CAL-001 traces it to unheated packs and gives 70 % with ColdCell packs.
- Pixhawk-standard flight controllers and DS-014 connectors can be bought in small quantities.
- PX4 supports the needed multirotor and quadplane modes without source changes.
- ColdCell can keep packs above their minimum discharge temperature for a full flight.
