---
doc_id: KWC-DDR-001
title: Kitewright Core TRL 2 review decisions
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
  change: TRL 2 review decisions D1 to D15, decided under Amish's 2026-10-03 pre-approval
---

# 0001: TRL 2 review decisions

- **Date:** 2026-10-03
- **Status:** accepted. Decided by Amish under his pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." and, for this second batch, "Proceed with the remaining 15 scaffolds".

## Context

The scaffold (KWC-PRB-001 v0.1, KWC-PRC-001 v0.1) left five open questions and several choices that the TRL 2 concept and TRL 3 calculations need settled: the flight stack, the controller class, the bus voltage, the payload class, how the mount works, how the core meets a frame, and where optional parts go. The TRL 2 review (`docs/REVIEW.md`, TRL 2 section) listed each with options and a recommendation. Under Amish's pre-approval every recommendation below is decided. Partners and regions are recorded as the first candidate to approach, not as agreed. Choices that touch safety take the conservative option and say what evidence would relax it. Requirements that the design does not meet are not decided here; they are put to Amish in `docs/REVIEW.md`.

## Options considered and decision

*Table 1. Decisions.*

| # | Item | Options considered | Decision | Why |
| --- | --- | --- | --- | --- |
| D1 | Flight stack | PX4; ArduPilot; both equal | PX4 for the whole family; ArduPilot kept as a documented alternative | R10 names PX4; PX4 runs multirotor and standard VTOL from one release |
| D2 | Flight controller class | FMUv6X class (triple IMU, heater, Ethernet); FMUv6C class; non-standard boards | FMUv6X class on the standard baseboard | IMU heater for cold boots, Ethernet for DS-014, 16 outputs for both frames, rated -40 to +85 °C |
| D3 | Power bus | Fixed 12S; fixed 6S; 18 to 60 V window | 18 to 60 V at the pack inputs (6S Li-ion to 16S LiFePO4); two inputs, two outputs, AS150 anti-spark connectors | One board for a light Range and a heavy Lift; ColdCell may use Li-ion, LiFePO4 or sodium-ion |
| D4 | Payload class | One class; light and heavy classes | One class for version 1: 5 kg and 100 W | Covers Lift's sea-level payload and every planned payload; one shoe and one test |
| D5 | Mount mechanism | Plain rail with rear entry and front stops; side-loading rail; quick-release plate on four pins | Plain rail under the plate, shoe enters from the rear to two front stops, DS-014 on a hand-plugged pigtail | Keeps the patent design-around (no bayonet); a pigtail avoids a blind-mating connector that DS-014 parts are not rated for |
| D6 | Payload retention (safety) | One locking pin; two independent pins; pin plus lanyard | Two independent spring locking pins, each with a red band that shows when it is withdrawn | Conservative choice: a released payload is a falling object. Evidence that would relax it to one pin: a vibration test at flight levels and a pull test showing a single pin cannot back out, on the built mount at TRL 4 |
| D7 | Core to frame | Core on top of the deck; core under the deck with the lid through an opening; frame-specific mounts | Core hangs under the frame deck on four M4 bolts on a 220 x 130 mm pattern with 8 mm spacers; the deck has a 200 x 112 mm opening for the lid | Payload loads go straight into the frame's hard points; the rail is free under the frame; one pattern for both frames |
| D8 | Companion computer | Inside the core lid; in its own box on the frame; none | Optional, in its own box on the frame, linked by Ethernet | Keeps 5 W of heat and 60 g out of the core; only some payloads need it |
| D9 | Pack data | DroneCAN; SMBus; analog only | ColdCell reports temperature and charge over DroneCAN | Released PX4 reads DroneCAN batteries without source changes (R10) |
| D10 | Radios | 900 MHz class telemetry and long-range control link; 2.4 GHz only; one combined video link | 900 MHz class telemetry (up to 1 W) and a long-range control link, band and power set per country; for India the 865 to 867 MHz licence-exempt band is the first candidate, to confirm | Range in steep terrain; open MAVLink radios |
| D11 | Altitude parameter sets | One set; three bands; continuous scheduling | Three bands: sea level, 3,000 m and 5,000 m (KWC-CAL-001, Table 6) | Simple to publish and check; matches AltiRig's test points |
| D12 | DS-014 licence | Wait for confirmation; proceed and confirm; own interface | Proceed with the DS-014 connector and pinout and confirm the licence before buying; if it restricts reuse, keep the same connector with Kitewright's own open pinout | Keeps the open standard the family was built around without blocking TRL 3 |
| D13 | Co-design partner | Rescue organisation; research group; both | First candidate to approach: a university glaciology group in Jammu and Kashmir; second: a state disaster response force unit in the same region (not agreed) | Lake survey is the first mission with a clear payload (LakeWatch) |
| D14 | Remote ID and logging | Fit now; fit when required; never | Log every flight on the controller; a remote ID module goes on the CAN bus when a country's rules require it | Certification is out of scope at TRL 3; the slot is kept |
| D15 | Hover-time model | Publish the 47 % figure; publish a model | Publish the model of KWC-CAL-001 section F (47 % with cold packs, 70 % with ColdCell) | R7 needs a model that can be checked against AltiRig and flight logs |

## Consequences

- KWC-PRC-001, KWC-REQ-001 (definitions), KWC-CAL-001 and the model use these decisions.
- D3, D4, D7 and D9 are shared interfaces with Kitewright Lift, Kitewright Range and ColdCell; they are listed under Cross-repo actions in `docs/REVIEW.md`. The sibling repos are not edited from here.
- D6 adds about 55 g and USD 32 against one pin; R9 is affected (see `docs/REVIEW.md`).
