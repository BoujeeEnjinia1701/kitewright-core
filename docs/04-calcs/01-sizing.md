---
doc_id: KWC-CAL-001
title: Kitewright Core sizing calculations
project: Kitewright Core
doc_type: Calculation
version: "0.2"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: "First issue for TRL 3 on the constructable design (KWC-DDR-002): mount strength, payload swap, payload power, heat, altitude, hover-time model, common core, mass and cost"
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: "Decision O1 option B applied (KWC-DDR-003): carbon fibre plate, 1.5 mm lid walls, pocketed rail bars, power leads moved to the frame harness; strength and mass recalculated; R9 now met on paper"
---

# Kitewright Core sizing calculations

On paper the constructable core meets all eleven of its requirements. The plain rail and two locking pins carry the 147 N vertical design load with factors of 6.8 or more on every part, a gloved payload swap takes about 52 s with no tools, 100 W reaches the payload at no more than 5.6 A, and the hottest avionics part stays near 75 °C at 45 °C ambient. The hover-time model explains the scaffold's 47 % figure: at 5,000 m and -20 °C an aircraft keeps 77.5 % of its sea-level hover time from air density alone, and unheated packs that give 60 % of their capacity bring it to 46.5 %; ColdCell packs kept warm raise it to 70.0 %. With decision O1 option B (KWC-DDR-003: a 2 mm carbon fibre plate, 1.5 mm lid walls, pockets in the rail bars and the power leads moved to each frame's harness) the core's estimated mass is 0.996 kg, which meets R9 with a 4 g margin; that margin is inside the accuracy of the catalogue masses, so the built core is weighed at TRL 4. The estimated cost of USD 3,944.40, with ground station and spares, is USD 1,055.60 under the USD 5,000 value-engineering target. Every number here is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [A3], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not show that the payload mount, the lithium packs, the power wiring or the aircraft is safe. The mount must be proof-loaded and the locking pins pull-tested, and the power board must be checked on a current-limited bench supply, before any pack is connected or any payload is flown. See KWC-PRC-001, Safety.

## Scope and method

The note checks every requirement in KWC-REQ-001 v0.2 against the design in KWC-PRC-001 v0.2 and the parametric model `cad/src/model.py`. The script imports the model's parameters and part volumes, so the plate, rails, shoe, pin blocks and lid used here are the ones in the STEP file, drawing KWC-DWG-001 and the build plan. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py`; it also writes `docs/04-calcs/results.csv`.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Rated payload | 5 kg on the mount, one payload class for version 1 (KWC-DDR-001, D4) | Kitewright Lift's sea-level payload |
| Load cases | Static 3 x 5 kg; drop 1.5 x 5 kg at 2 g (both 147 N, R3); fore-aft 1.5 x 5 kg at 3 g (221 N) on one pin alone; side 1.5 x 5 kg at 1 g with the payload's centre of mass 80 mm below the shoe | R3 and screening values |
| Materials | 6061-T6 yield 276 MPa; 2 mm quasi-isotropic carbon fibre plate 250 MPa design allowable in bending (conservative; typical flexural strength 500 to 600 MPa); hardened plunger pin 400 MPa in shear (conservative); M4 A2-70 screws at 0.8 x proof (3,161 N) | Handbook values; carbon allowable an estimate |
| Swap | Seven hand actions totalling 35 s bare-handed; gloves multiply by 1.5 | Estimate |
| Bus | 18 V (6S Li-ion at 3.0 V a cell) to 60 V; 100 W payload; pigtail 0.3 m of 20 AWG, two pins each way; payload switch limit 8 A | KWC-DDR-001, D3 |
| Heat | Lid surface 0.0477 m² (top and sides); 10 W/m²K in still air, 25 W/m²K in hover; 10 K allowance for sun on the frame body around the lid; 10 K from lid air to the hottest part; parts rated -40 to +85 °C | Handbook ranges; maker ratings of the part classes |
| Dissipation | Flight controller 2.5 W, telemetry 1 W idle and 2 W in flight, receiver 0.3 W, 5.3 V supplies 1.1 W, payload switch 0.47 W, bus conduction 4 W at 100 A through 0.4 mΩ | Estimates; 100 A is Kitewright Lift's hover estimate at 44 V |
| Atmosphere | International Standard Atmosphere | ISA |
| Hover model | Hover power proportional to 1/√(density) for the same mass and rotors; unheated Li-ion gives 60 % of capacity at -20 °C; ColdCell packs give 95 % and spend 5 % on their heater | Momentum theory; typical cell data |
| Mass | Made parts from model volumes (aluminium 2.70, carbon fibre plate 1.55, ASA 1.07, G10 1.85, UHMW-PE 0.94 g/cm³); bought parts from catalogue class values (Table 8) | Estimates, to confirm when bought |

## A. Mount strength (R3)

The vertical design load is 147 N in both R3 cases [A1]. The shoe overlaps each lip by 19 mm along 184 mm; the lip bends about the spacer bar's inner edge with a 10.5 mm lever, giving 2.8 MPa at the full 3 mm root. The lip pockets stop 1.5 mm short of the spacer, so the root keeps its full thickness; at the pocket edge the lever is 9.0 mm, and taking the whole shoe length at the 1 mm skin under the pockets (conservative, since a third of the length is unpocketed) gives 21.6 MPa, a factor of 13 on yield [A2]. The ten M4 screws that hold the lips see at most 46 N each with prying, a factor of 69 [A3]. Between the frame bolts, 220 mm apart, the plate's edge strip, the two 1.5 mm walls of the spacer bar and the pocketed lip, taken as three separate beams at a pocket, reach 37 MPa, a factor of 6.8 on the 250 MPa carbon plate allowable [A4]. The frame bolts bear on the carbon plate at 4.1 MPa per hole, far below its bearing strength [A8].

Fore and aft, the shoe is held by the front stops one way and by the locking pins both ways. The 221 N fore-aft case on ONE pin gives 11.2 MPa of shear in the 5 mm pin and 8.8 MPa of bearing in the shoe [A5]; forward load into the two front stops gives 1.2 MPa [A6]. A 1 g side load with the payload's centre of mass 80 mm down puts 54 N on each lip [A7]. Every factor stays above 5 after the lightening of decision O1, because the parts were sized for making and handling, not for strength. That margin is why two independent pins cost little: either pin alone holds the payload.

## B. Payload swap (R2)

*Table 2. Swap sequence [B1].*

| Action | Time, bare-handed (s) |
| --- | --- |
| Unplug the DS-014 plug | 6 |
| Pull and twist both locking pins to their rest | 5 |
| Slide the payload out to the rear | 4 |
| Slide the next payload in to the front stops | 5 |
| Twist both pins back; they snap into the shoe | 3 |
| Plug the DS-014 plug and close its latch | 8 |
| Check both pins show no red band; tug the payload | 4 |
| Total | 35 |

With gloves the swap takes about 52 s and needs no tools. The margin to R2's figure is small, so a timed gloved trial at TRL 4 is the real check.

## C. Payload power (R4)

*Table 3. Payload current at the end of discharge [C1].*

| Bus | Voltage (V) | Current for 100 W (A) | Pigtail drop (mV) |
| --- | --- | --- | --- |
| 6S Li-ion, 3.0 V a cell | 18.0 | 5.56 | 56 |
| 12S Li-ion | 36.0 | 2.78 | 28 |
| 14S Li-ion, 3.0 V a cell (ColdCell variant for Kitewright Lift) | 42.0 | 2.38 | 24 |
| 16S LiFePO4, 2.8 V a cell | 44.8 | 2.23 | 22 |

The 8 A payload switch covers the worst case with a 1.44 x margin [C2]. At the top of the window, a full 14S lithium-ion pack (the ColdCell variant Kitewright Lift adopted in its decision 2, KWL-DDR-003) reads 58.8 V and a full 16S LiFePO4 pack 58.4 V, only 1.2 V and 1.6 V under the 60 V rating of the power board and power modules [C3]. Braking of eight motors can lift the bus above the pack voltage for short moments, so this margin is raised as a new question for Amish (KWC-DEC-001, O2). The current each DS-014 battery pin may carry is to be confirmed from the published standard and the chosen connector; two pins each way at 3 A would cover the 6S case.

## D. Heat (R5)

The lid encloses 4.9 W on the ground and 10.4 W in Kitewright Lift's hover, where 4 W comes from the 100 A bus current [D1]. On a 45 °C day, with 10 K allowed for sun on the frame body, the lid air reaches 65.3 °C on the ground and 63.7 °C in hover, and the hottest part about 75 °C, 10 K inside the 85 °C rating [D2]. Cold-soaked to -20 °C, every part boots within its -40 °C rating, and once running the lid air settles near -10 °C [D3]. The optional companion computer sits outside the lid (KWC-DDR-001, D8), so its 5 W does not count here.

## E. Altitude (R6)

*Table 4. International Standard Atmosphere [E1].*

| Altitude (m) | Temperature (°C) | Pressure (kPa) | Density (kg/m³) | Share of sea-level density |
| --- | --- | --- | --- | --- |
| 0 | 15.0 | 101.3 | 1.225 | 100 % |
| 3,000 | -4.5 | 70.1 | 0.909 | 74 % |
| 5,000 | -17.5 | 54.0 | 0.736 | 60 % |
| 6,000 | -24.0 | 47.2 | 0.660 | 54 % |

At 5,000 m and -20 °C the density is 0.743 kg/m³, and the barometer must read down to 54 kPa; flight-controller barometers of this class read 30 to 110 kPa [E2]. The core's share of R6 is sensors in range and failsafes set for each band (Table 6). Whether a frame has the thrust to stay in control is a frame property, checked in Kitewright Lift and Kitewright Range with AltiRig data.

*Table 6. Altitude parameter sets: what each band changes (released PX4, parameters only).*

| Setting | Sea level band (0 to 1,500 m) | 3,000 m band (1,500 to 4,000 m) | 5,000 m band (4,000 to 6,000 m) |
| --- | --- | --- | --- |
| Hover thrust estimate | From the frame's sea-level hover test | Sea-level value x 1.16 | Sea-level value x 1.29 |
| Low-battery warning and return | 30 % and 20 % | 35 % and 25 % | 40 % and 30 % |
| Return altitude above launch | 30 m | 50 m | 80 m (terrain) |
| Link-loss action | Return after 5 s | Return after 5 s | Return after 3 s |
| Geofence | Set per site, 1,000 m radius by default | As sea level | As sea level, 120 m ceiling above launch |
| Pack temperature before arming | ColdCell reports at least 10 °C | As sea level | As sea level |

The hover-thrust factors are 1/√(density share) from Table 4; the battery thresholds are deliberately higher at altitude because a return through thin air takes more energy. All values are starting points to be tuned on AltiRig and in flight.

## F. Hover-time model (R7)

For the same aircraft and mass, hover power scales with 1/√(density), so hover time at 5,000 m is 0.775 of sea level from air alone [F1]. Unheated packs that give 60 % of their capacity at -20 °C bring that to 46.5 %, which is the scaffold's 47 % estimate [F2]. ColdCell packs kept warm, giving 95 % of their capacity and spending 5 % on their heater, bring it to 70.0 % [F3]. The model is:

hover time = usable pack energy x (1 - heater share) x efficiency / hover power, with hover power = (m g)^1.5 / (figure of merit x √(2 x density x rotor disc area)).

It leaves out the change in motor and propeller efficiency at the higher rotor speeds of thin air; AltiRig measures that. R7 asks that the model predict measured hover time within 15 %, which only TRL 4 flights can show.

## G. Common core (R8, R10, R1)

*Table 7. Outputs needed on the flight controller [G1].*

| Frame | Outputs needed | Available |
| --- | --- | --- |
| Lift, eight motors, plus three payload channels | 11 | 16 |
| Lift, six motors, plus three payload channels | 9 | 16 |
| Range, four lift motors, pusher and five servos | 10 | 16 |

One core, one frame pattern and one payload interface serve both frames with parameter changes only (R8). Released PX4 (v1.15 or later) runs multirotor and standard VTOL frames, DroneCAN battery reporting and MAVLink payload protocols without source changes (R10). The DS-014 pigtail carries the battery, Ethernet, CAN, UART and trigger lines named in the standard (R1); the exact pinout and licence terms are confirmed from the published standard before the connector is bought.

## H. Mass (R9)

*Table 8. Core mass [H1, H2].*

| Part | Mass (g) | Source |
| --- | --- | --- |
| Core plate, 2 mm carbon fibre | 109 | Model volume |
| Rail spacer bars and lips (pocketed) and wear tape | 111 | Model volume |
| Front stops, pin blocks, jam nuts, corner spacers | 96 | Model volume |
| Strain-relief bar and its two posts | 3 | Model volume |
| Lid, 1.5 mm walls | 90 | Model volume |
| Damping plate | 28 | Model volume |
| Flight controller | 100 | Catalogue class |
| Power board, power modules | 105 | Catalogue class |
| Radio, receiver, antennas and bulkheads | 91 | Catalogue class |
| GNSS receiver and mast | 45 | Catalogue class |
| Locking pins (2) | 50 | Catalogue class |
| DS-014 pigtail, harness, switch, grommets, gasket | 110 | Catalogue class |
| Dampers, standoffs, bonded inserts, fasteners | 56 | Catalogue class |
| Total (rows rounded) | 996 | |

The core weighs about 0.996 kg without the payload shoe (310 g, counted with each payload) and without the optional companion computer (60 g, outside the lid) [H2]. That is 4 g under the figure in R9 [H3], so R9 is met on paper; the margin is inside the accuracy of the catalogue masses, and the built core is weighed at TRL 4 [H6].

*Table 8a. What decision O1 option B changed (KWC-DDR-003) [H4, H5].*

| Item | Before (KWC-DDR-002) | Now | Change |
| --- | --- | --- | --- |
| Core plate | 190 g, 2 mm 5052 aluminium | 109 g, 2 mm carbon fibre | -81 g |
| Lid | 114 g, 2 mm walls | 90 g, 1.5 mm walls | -24 g |
| Rail spacer bars and lips | 158 g | 106 g, windows in the bars and pockets under the lips | -52 g |
| Power leads and four AS150 halves | 124 g in the core | In each frame's harness; the core keeps the board's solder pads and a 3 g strain-relief bar | -121 g |
| Clinch nuts (14) | 7 g | Bonded flush inserts (16), 6 g | -1 g |
| Core | 1,274 g | 996 g | -278 g |

Clinch nuts cannot be pressed into carbon plate, so the plate takes bonded flush inserts; they sit flush underneath, where the shoe runs 0.3 mm below the plate. The four leads (124 g, about USD 60) are now part of the Kitewright Lift and Kitewright Range harnesses, which count them in their own mass and cost.

## I. Cost (R11)

The bill of materials comes to USD 1,764.40 for the airborne core, USD 1,620.00 for the ground station and USD 560.00 for spares [I1]. Value-engineering target: USD 5,000. Estimated cost of the constructable design: USD 3,944.40 (USD 1,055.60 under the target) [I2]. Decision O1 added USD 59.80 to the core (carbon plate USD 44 more, rail pockets USD 12, bonded inserts USD 4.80, lid USD 1 less) and moved USD 56 of leads and plugs out to the frames (the USD 60 lead set, less USD 4 for the strain-relief bar), a net USD 3.80.

## L. Results against every requirement

*Table 9. Results (also in `docs/04-calcs/results.csv`).*

| ID | Result | Status |
| --- | --- | --- |
| R1 | DS-014 40-pin connector on a 0.3 m pigtail; signals from the flight controller and bus | Met on paper (licence and pinout to confirm) |
| R2 | About 52 s with gloves, no tools; pin state shown by a red band | Met on paper (estimate) |
| R3 | Vertical 147 N: lips 13 x, screws 69 x, side beam 6.8 x; fore-aft 221 N on one pin 36 x | Met on paper |
| R4 | 100 W needs at most 5.6 A (6S at 18 V); switch limit 8 A | Met on paper (pin rating to confirm) |
| R5 | Hottest part about 75 °C at 45 °C ambient; cold boot at -20 °C within the -40 °C rating | Met on paper |
| R6 | Sensors in range at 54 kPa; failsafes set per altitude band | Met on paper for the core; flight check needs a frame |
| R7 | Model published: 47 % (cold packs) and 70 % (ColdCell) of sea-level hover time at 5,000 m and -20 °C | Model ready; accuracy shown only at TRL 4 |
| R8 | One core and one interface; Lift needs 11 of 16 outputs, Range 10 | Met by design |
| R9 | 0.996 kg estimated (carbon plate, 1.5 mm lid walls, pocketed rail bars, power leads in the frame harness) | Met on paper, 4 g margin (weigh at TRL 4) |
| R10 | Released PX4, parameters and stock modules only; ColdCell reports over DroneCAN | Met by design |
| R11 | USD 3,944.40 including ground station and spares | Under the value-engineering target by USD 1,055.60 |

## Checks against earlier figures

- The scaffold's estimate of 47 % hover time at 5,000 m and -20 °C is reproduced (46.5 %) and traced to unheated packs; with ColdCell the model gives 70 %.
- R9 was written before the core had a constructable structure; the first constructable design (1.27 kg) did not meet it, and decision O1 option B (KWC-DDR-003) brings it to 0.996 kg (section H).
