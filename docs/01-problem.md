---
doc_id: KWC-PRB-001
title: Kitewright Core problem statement
project: Kitewright Core
doc_type: Problem statement
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
  change: Open questions answered by the decisions of KWC-DDR-001 (Amish's 2026-10-03 pre-approval); budget worded as a value-engineering target; co-design candidate named
---

# Kitewright Core problem statement

Every drone project for mountain rescue or survey ends up rebuilding the same things: autopilot setup, power, radio, a payload mount and cold-weather tuning. Commercial platforms solve this inside closed ecosystems that small teams cannot afford, inspect or adapt.

## The problem

Demand is real. Drones have helped rescue more than 1,000 people ([DJI, 2023](https://www.dji.com/media-center/announcements/dji-records-more-than-1000-people-rescued-by-drones-globally)), and heavy-lift drones now work above 5,000 m on Everest ([DJI, 2024](https://www.dji.com/media-center/announcements/dji-completes-world-first-drone-delivery-tests-on-mount-everest-en)). But mountain conditions stretch every part. The standard atmosphere at 5,000 m gives 60% of sea-level air density at -17.5 °C ([Engineering ToolBox](https://www.engineeringtoolbox.com/standard-atmosphere-d_604.html)), so rotors work harder while batteries deliver less. The Mavic Pro that found Rick Allen was flying far above its rated ceiling ([DroneDJ, 2018](https://dronedj.com/2018/07/16/mountaineer-rick-allen-was-feared-dead-on-broad-peak-but-a-dji-mavic-pro-drone-found-him-alive/)).

The closed route works but locks teams in. The Matrice 350 RTK is rated to 5,000 m with standard propellers and -20 °C ([Advexure](https://advexure.com/products/dji-matrice-350-rtk)), at USD 14,814 plus USD 899 per battery ([DroneFly](https://www.dronefly.com/products/dji-tb65-intelligent-flight-battery-m350)). The open route has strong parts: PX4 under BSD 3-Clause ([GitHub](https://github.com/PX4/PX4-Autopilot)), the Pixhawk standards including DS-014 ([Pixhawk Standards](https://github.com/pixhawk/Pixhawk-Standards)), and ArduPilot for fixed wing and VTOL ([ArduPilot](https://ardupilot.org/plane/docs/quadplane-overview.html)). What is missing is an integrated, documented core, with its power bus, mount, radios and altitude tuning specified once, that every frame and payload in a family can rely on.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Mountain rescue teams | A platform they can repair and adapt, with payloads that swap in the field | Search at 3,000 to 6,000 m, often in cold and wind |
| Glacier and hazard researchers | An inspectable platform whose logs, power and sensors are documented | Seasonal field campaigns at glacial lakes |
| Disaster response groups and NGOs | A lower-cost, multi-role drone that is not tied to one vendor | Floods, landslides and road cuts in mountain regions |
| Payload developers and students | A published mechanical, electrical and software interface to build against | University labs, makerspaces, small companies |

## Operating environment

- Operation from sea level to 5,000 m (design target), with growth to 6,000 m to be assessed.
- Ambient -20 to +45 °C (-4 to +113 °F) (target); snow, rain, dust and UV.
- Wind up to about 10 m/s in normal operation (target); gusts in mountain valleys.
- Remote sites without mains power; batteries charged from vehicles or generators.
- Radio links in steep terrain with frequent loss of line of sight.

## Constraints

- Value-engineering target of USD 5,000 for the core, including avionics, radios, a ground station setup and spares (a hypothetical control target, not a limit; STANDARDS section 18).
- Upstream PX4 (or ArduPilot) with parameters and documented modules; no private fork of the flight stack.
- Payload mount follows Pixhawk DS-014 electrically, with a plain rail and locking pin mechanically; no bayonet.
- Power bus runs from ColdCell packs with external film heaters and a BMS thermostat; any tether input is fixed voltage with onboard DC-DC conversion.
- Same core, unchanged, in the Lift and Range frames.
- Hardware under CERN-OHL-S-2.0; software under a licence compatible with PX4 (BSD 3-Clause) or ArduPilot (GPLv3).

## Out of scope

- Airframes (Kitewright Lift and Kitewright Range) and payloads (AvalancheScout, LakeWatch and others), which are sibling repos.
- Caged confined-space frames (deferred after the patent screen).
- Hybrid generator, fuel-cell or combustion power.
- Beyond-visual-line-of-sight approvals, satellite links and remote ID certification at this TRL.
- Aviation certification (FAA Part 107, EASA, India DGCA Drone Rules 2021) at this TRL; to be addressed if prototypes progress.
- Any weapon, targeting or military payload.

## Prior work

| Prior work | What it does | Gap for these users | Source |
| --- | --- | --- | --- |
| PX4 Autopilot | Open flight control software under BSD 3-Clause, governed by the Dronecode Foundation | Software only; no reference airframe, power bus or cold-weather integration | [link](https://github.com/PX4/PX4-Autopilot) |
| Pixhawk Payload Bus standard (DS-014) | Open standard with a 40-pin connector carrying Ethernet, USB 2.0, CAN FD, UART, trigger, PPS and battery power, plus MAVLink payload protocols | An interface standard, not a built mount or core; licence terms still to confirm | [link](https://dronecode.org/announcing-the-pixhawk-payload-bus-open-standard/) |
| DJI Matrice 350 RTK | Closed enterprise drone, 55 min flight, -20 to 50 °C, 5,000 m ceiling with standard propellers, USD 14,814 | Closed payload and battery ecosystem; cost beyond many mountain teams | [link](https://advexure.com/products/dji-matrice-350-rtk) |
| DJI TB65 self-heating battery | 263.2 Wh pack that heats itself below 5 °C, rated -20 to 50 °C, USD 899 | Works only in DJI aircraft; used in pairs | [link](https://www.dronefly.com/products/dji-tb65-intelligent-flight-battery-m350) |
| ArduPilot QuadPlane | Open flight control for fixed wing aircraft with VTOL motors | Firmware only; no shared hardware core across frames | [link](https://ardupilot.org/plane/docs/quadplane-overview.html) |

## Co-design

A mountain rescue organisation or high-altitude research group working in the Himalaya or Karakoram, such as a state disaster response force unit or a university glaciology team, that can define missions, test at altitude and review the payload interface. First candidate to approach (not agreed): a university glaciology group in Jammu and Kashmir that already surveys glacial lakes in the Kashmir Himalaya, with a state disaster response force unit in the same region as the second (KWC-DDR-001, D13).

> **Safety:** Field work with prototypes happens only with a partner that holds the local flying permissions and runs its own safety briefing; nothing here is an approval to fly.

## Open questions answered at TRL 3

*Table 1. The scaffold's open questions and the decisions that answer them (KWC-DDR-001, decided under Amish's 2026-10-03 pre-approval).*

| Question | Answer | Decision |
| --- | --- | --- |
| Under what licence is DS-014 published, and can its connector be used freely? | Proceed with the DS-014 connector and pinout; confirm the licence before the connector is bought; if it restricts reuse, keep the same 40-pin connector with Kitewright's own open pinout | D12 |
| PX4 or ArduPilot as the primary stack? | PX4 for the whole family; ArduPilot documented as the alternative | D1 |
| Which radio bands and power levels at target sites? | 900 MHz class radios set per country; for India the 865 to 867 MHz licence-exempt band is the first candidate, to confirm with the partner | D10 |
| What payload mass and power classes? | One class for version 1: 5 kg and 100 W | D4 |
| Remote ID and flight logging? | Every flight logged on the controller; a remote ID module goes on the CAN bus when a country's rules require it | D14 |

## Safety

> **Safety:** The problem involves lithium packs, spinning propellers and loads carried over people and terrain. Every Kitewright document that describes these keeps a safety section; the core's precis (KWC-PRC-001) and build plan (KWC-BLD-001) set out the hazards and the safety stops. Civilian use only; no weapons, targeting or military payloads.
