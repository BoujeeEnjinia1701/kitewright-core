---
doc_id: KWC-BLD-001
title: Kitewright Core prototype build plan
project: Kitewright Core
doc_type: Build plan
version: "0.2"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-03'
    author: Amish Chadha
    change: First build plan; design made constructable (KWC-DDR-002)
  - version: "0.2"
    date: '2026-10-03'
    author: Amish Chadha
    change: "Carbon fibre plate with bonded flush inserts, pocketed rail bars, 1.5 mm lid walls; power leads and AS150 plugs moved to the frame harness, strain-relief bar added (KWC-DDR-003)"
---

# Kitewright Core prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component of the core, pulled apart and numbered in build order.*

The prototype is one Kitewright Core: a 240 x 150 mm carbon fibre plate with the avionics on top under a printed lid, and the payload rail and two locking pins underneath, plus one payload shoe. Figure 1 shows its 18 components in the order you make or fit them. Nine are made in a small workshop: the core plate (cut by a carbon plate service from the sketch), the rail spacer bars, front stops, rail lips, pin blocks, payload shoe, lid, damping plate and strain-relief bar. Everything else is bought and fitted: the flight controller, GNSS receiver, power board and modules, radios, antennas, the DS-014 pigtail, the locking pins (indexing plungers), dampers, standoffs and bonded inserts. The four heavy power leads and their AS150 plugs are not part of the core: each frame brings them in its own harness and solders them to the power board's pads. The work is sawing, drilling, milling, tapping and filing aluminium bar, bonding inserts into carbon plate, one 3D print and cutting glass-epoxy sheet. The parts cost about USD 1,764 for the airborne core from the bill of materials; the ground station kit is bought complete.

> **Safety:** The finished core switches lithium pack power of up to 60 V and 200 A. Until section 6 says otherwise, power it only from a current-limited bench supply, never from a pack. Soldering the frame's 8 AWG leads to the board needs a 100 W iron or better and gets the wire hot enough to burn: hold it with pliers. Cut aluminium edges, carbon dust and glass-epoxy dust are hazards: deburr every edge, wear gloves and a dust mask, drill carbon and cut G10 wet or under extraction, and seal cut carbon edges. Printing ASA gives off fumes; print in a ventilated space.

## 2. What changed to make it buildable

The scaffold described the core in words; to build it, each part needed a shape, a material and a fixing. Each change below keeps what the core does and is recorded in decision record KWC-DDR-002. The last four rows are the lightening Amish chose for the core's mass (KWC-DDR-003).

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Payload rail | "A plain rail" | Spacer bar and taped lip on each side, bolted under the plate; 0.3 mm gap above the shoe (Figure 11) | Made from stock bar; the gap comes from stock thicknesses |
| Locking pin | "A locking pin" | Two spring plungers in blocks under the lips (Figure 13) | Either pin alone holds the payload |
| End of travel | None | Two front stops between plate and lip (Figure 14) | Lines the pins up with their holes |
| Payload connector | A connector on the mount | A pigtail through a slot in the plate and a notch in the shoe (Figure 20) | A sliding shoe cannot mate a 40-pin plug reliably |
| Fixings under the plate | Not shown | M3 inserts bonded into the plate, flush underneath (Figure 22) | The shoe slides just under the plate; clinch nuts cannot be pressed into carbon |
| Core to frame | "Bolts into any frame" | Hangs under the deck on four bolts and spacers (Figure 27) | Payload load goes straight into the frame |
| Flight controller | Not shown | On four dampers and a glass-epoxy plate above the power board (Figure 17) | Vibration isolation |
| Lid | "Cold-rated enclosure" | Printed lid with flange, gasket and six screws | Clears the stop nuts and the deck opening |
| Core plate | 2 mm aluminium sheet | 2 mm carbon fibre plate | 81 g lighter (R9) |
| Lid walls | 2 mm | 1.5 mm | 24 g lighter (R9) |
| Rail bars | Plain bar | Windows through the spacer bars and pockets under the lips, between the screw holes | 52 g lighter (R9); every strength factor stays above 5 |
| Power leads | Four 8 AWG leads with AS150 plugs in the core | In each frame's harness, soldered to the board's pads and tied to a strain-relief bar behind the lid (Figure 24) | 121 g off the core (R9); lead lengths differ for each frame anyway |

## 3. Making the components

Sizes are in millimetres. Positions are given from the centre of the core plate: "along" means toward the front (the end with the cable slot), "across" means to the left or right of the centre line.

### 3.1 Core plate

![Figure 2. Core plate making sketch](../cad/drawings/KWC-DWG-101.png)

*Figure 2. Making sketch KWC-DWG-101.*

**What it is and what it is made from.** The flat plate everything fixes to: 240 x 150 mm of 2 mm quasi-isotropic carbon fibre plate. Have a carbon plate service cut the outline, holes and slot from the sketch by waterjet or CNC; if you drill it yourself, drill wet with a sharp carbide drill on a backing board, and wear a dust mask.

**How to make it.**

1. Cut the blank 240 x 150 mm and mark a centre line each way.
2. Drill the four frame holes 4.5 mm, 110 mm along each way from the centre and 65 mm across each way.
3. Drill the rail holes 4.5 mm on two lines 70 mm each side of the centre line, at 93 mm and 75 mm behind the centre, 30 mm behind, 30 mm ahead and 90 mm ahead. Drill the two stop holes 4.5 mm at 95 mm ahead, 55 mm each side.
4. Drill the 16 insert holes 4.22 mm: six for the lid flange (60 mm behind, on the centre, 60 mm ahead; 50 mm each side), four for the tall standoffs (75 mm behind and 25 mm ahead; 30 mm each side), four for the short standoffs (66 mm behind and 6 mm ahead; 21 mm each side) and two for the strain-relief bar posts (95 mm behind, 28 mm each side).
5. Cut the cable slot, 12 mm long and 24 mm wide, from 70 to 82 mm ahead of the centre.
6. Seal every cut edge and hole with a thin coat of epoxy.
7. Bond an M3 flush insert into each 4.22 mm hole with structural epoxy, flange on the top face, body flush with the underside; wipe off any epoxy underneath and let it cure on a flat sheet with release film.

**How it fits the parts next to it.** The rails bolt to its underside (Figure 11), the lid, standoffs and strain-relief posts screw into its inserts from above (Figures 17 and 22), and it hangs from the frame on its four corner holes (Figure 27).

**Check before moving on.** Lay a straight edge across the underside in several directions: nothing stands proud, because the shoe slides 0.3 mm below.

### 3.2 Rail spacer bars (make 2)

![Figure 3. Rail spacer bar making sketch](../cad/drawings/KWC-DWG-102.png)

*Figure 3. Making sketch KWC-DWG-102.*

**What it is and what it is made from.** The bar that sets the gap between plate and lip: 10 x 6 mm 6061-T6 flat bar, 200 mm long, with three lightening windows.

**How to make it.**

1. Saw two pieces 200 mm long and square the ends.
2. Mark a centre line along the 10 mm face and drill five 4.5 mm holes on it at 7, 25, 70, 130 and 190 mm from the rear end.
3. Mill three windows 6 mm wide straight through the 6 mm height, centred on the 10 mm face so 1.5 mm walls remain each side: from 31.5 to 63.5 mm, 76.5 to 123.5 mm and 136.5 to 183.5 mm from the rear end. That leaves at least 4.25 mm of solid bar round every hole.
4. Deburr.

**How it fits the parts next to it.** Its 10 mm face lies against the underside of the plate with its outer edge on the plate's long edge; the lip lies under it (Figure 11). The screws pass through all three.

**Check before moving on.** Hold it under the plate and look through all five holes.

### 3.3 Front stops (make 2)

![Figure 4. Front stop making sketch](../cad/drawings/KWC-DWG-103.png)

*Figure 4. Making sketch KWC-DWG-103.*

**What it is and what it is made from.** A small block that stops the shoe at the front end of the rail: 20 x 6 mm 6061-T6 bar, 12 mm long.

**How to make it.**

1. Saw two pieces 12 mm long and file the cut ends flat and square: the rear face is where the shoe stops.
2. Drill one 4.5 mm hole, 7 mm from the rear face, 5 mm from the front end and 10 mm from each side.

**How it fits the parts next to it.** It sits between the plate and the lip, against the inner edge of the spacer bar, with its front end level with the rail's front end. The rail's stop screw clamps it (Figure 14).

**Check before moving on.** With both stops fitted loosely, their rear faces line up across the plate within 0.2 mm.

### 3.4 Rail lips with wear tape (make a left and a right)

![Figure 5. Rail lip making sketch](../cad/drawings/KWC-DWG-104.png)

*Figure 5. Making sketch KWC-DWG-104.*

**What it is and what it is made from.** The bar the shoe's edge rides on: 30 x 3 mm 6061-T6 flat bar, 200 mm long, with 0.7 mm UHMW-PE tape on top.

**How to make it.**

1. Saw two pieces 200 mm long.
2. Drill the five screw holes 4.5 mm on a line 5 mm from the outer edge, at 7, 25, 70, 130 and 190 mm from the rear end, and the stop hole 4.5 mm at 195 mm, 20 mm from the outer edge.
3. Drill the pin hole 5.5 mm, 16 mm from the rear end and 20 mm from the outer edge.
4. Countersink the screw and stop holes 90° from the underside, deep enough that an M4 countersunk head sits flush. The left and right lips are mirror images: lay them side by side, outer edges outward, before countersinking.
5. Mill three pockets 2 mm deep in the underside, from 1.5 to 18.5 mm in from the inner edge, at the same positions along the bar as the spacer bar windows (31.5 to 63.5, 76.5 to 123.5 and 136.5 to 183.5 mm from the rear end). The pockets stop 1.5 mm short of the spacer bar's line, so the lip keeps its full 3 mm where it bends.
6. Stick UHMW-PE tape on the top face from the inner edge to 1 mm short of the spacer bar's line, from the rear end to the front stop. Cut out the pin hole with a sharp knife.

**How it fits the parts next to it.** The tape faces up toward the plate. The shoe's edge overlaps the lip by 19 mm and rides on the tape, with 0.3 mm between the shoe and the plate (Figure 11).

**Check before moving on.** After step 1 of section 4, a 5 mm offcut of the shoe plate slides between lip and plate along the whole rail, with a 0.2 to 0.4 mm feeler gauge fitting above it.

### 3.5 Pin blocks (make 2)

![Figure 6. Pin block making sketch](../cad/drawings/KWC-DWG-105.png)

*Figure 6. Making sketch KWC-DWG-105.*

**What it is and what it is made from.** The threaded block that holds a locking pin under the lip: 30 x 15 mm 6061-T6 bar, 28 mm long.

**How to make it.**

1. Saw two pieces 28 mm long.
2. Mark the plunger hole 14 mm from each end and 20 mm from the outer face. Drill it 9.0 mm through, square to the 28 x 30 face, and tap M10 x 1 (fine thread) all the way.
3. Drill two 4.5 mm screw holes 5 mm from the outer face, at 5 and 23 mm from the rear end.

**How it fits the parts next to it.** The block sits under the lip at the rear of the rail with its outer face flush with the plate's edge; two M4 x 35 cap screws pass up through block, lip, spacer bar and plate into nylon-insert nuts. The plunger screws up into it from below; its pin passes up through the lip and into the shoe (Figure 13).

**Check before moving on.** The plunger screws in by hand, and its pin comes up through the lip hole without touching the sides.

### 3.6 Payload shoe

![Figure 7. Payload shoe making sketch](../cad/drawings/KWC-DWG-106.png)

*Figure 7. Making sketch KWC-DWG-106.*

**What it is and what it is made from.** The plate every payload carries on its top: 184 x 128 mm, cut from 5 mm 6061-T6 plate. The core kit carries one; each payload maker makes their own to this sketch.

**How to make it.**

1. Cut the blank 184 x 128 mm. The long edges and the front edge run in the rail and against the stops: make them straight and square.
2. Cut the cable notch in the middle of the front edge, 18 mm deep and 28 mm wide.
3. Drill the two pin holes 5.5 mm, 12 mm from the rear edge and 9 mm in from each long edge.
4. Drill four 4.5 mm payload holes at 26 and 146 mm from the rear edge, 30 mm each side of the centre line, and countersink them from the top so the screw heads sit flush.
5. Chamfer the rear corners 2 mm so the shoe finds the rail.

**How it fits the parts next to it.** It slides in from the rear between the plate and the lips until its front edge meets the front stops; both pins then rise into its holes (Figures 13 and 14). The payload bolts to its underside with four M4 countersunk screws from the top.

**Check before moving on.** In section 4, step 10: it slides the full rail without binding, and both pins drop into their holes at the stops.

### 3.7 Lid

![Figure 8. Lid making sketch](../cad/drawings/KWC-DWG-107.png)

*Figure 8. Making sketch KWC-DWG-107.*

**What it is and what it is made from.** The cover over the avionics, printed in light grey ASA: 168 x 92 x 62 mm outside with 1.5 mm walls and top and a 180 x 108 x 3 mm flange.

**How to make it.**

1. Print it open side down on the flange, 0.2 mm layers, three 0.5 mm walls (1.5 mm), 25 % infill, supports only under the rear grommet holes and the service opening.
2. Check the six 3.4 mm flange holes, the 10.2 mm mast socket (12 mm deep in the 22 mm boss, 55 mm behind the centre), the 6 mm GNSS cable hole beside it, the three 6.5 mm antenna holes and the 12.2 mm switch hole in the top, and the two 20 mm grommet holes (13 mm each side, 17 mm up) and the 12 x 7 mm service opening in the rear wall. Clear them with a drill of the same size.
3. Melt an M3 heat-set insert into the side of the mast boss for the thumbscrew.
4. Cut the 1 mm foam gasket to the flange outline, with six 6 mm holes at the screws.

**How it fits the parts next to it.** The lid stands on the gasket on the plate and six M3 cap screws pass through its flange into the bonded inserts (Figure 22). It rises through the frame deck's opening.

**Check before moving on.** The lid sits flat on its gasket with no rock, and the flight controller, once fitted, clears its top by at least 5 mm.

### 3.8 Damping plate

![Figure 9. Damping plate making sketch](../cad/drawings/KWC-DWG-108.png)

*Figure 9. Making sketch KWC-DWG-108.*

**What it is and what it is made from.** The plate the flight controller sits on: 110 x 70 mm of 2 mm G10 glass-epoxy sheet.

**How to make it.**

1. Cut 110 x 70 mm with a fine-tooth saw, wet or under extraction, and file the edges smooth.
2. Drill four 3.4 mm damper holes 5 mm in from each end and each long edge (a 100 x 60 mm pattern).
3. Mark the flight controller's own mounting pattern, centred, and drill 3.2 mm.

**How it fits the parts next to it.** It rests on the four silicone dampers, which sit on the tall standoffs; the controller is fixed to it with M3 nylon screws, its arrow pointing forward (Figure 17).

**Check before moving on.** It hangs level on the dampers and touches nothing else.

### 3.9 Strain-relief bar

**What it is and what it is made from.** A G10 strip 64 x 6 x 3 mm on two 11 mm M3 aluminium standoffs, behind the lid at the rear of the plate. The frame's four power leads are tied down to it with cable ties, so a pull on a lead never reaches the solder pads.

**How to make it.**

1. Cut the strip from the offcut of the damping plate sheet (wet or under extraction) and file the edges.
2. Drill two 3.4 mm holes on its centre line, 28 mm each side of the middle (56 mm apart).

**How it fits the parts next to it.** The two standoffs screw into the bonded inserts 95 mm behind the centre, 28 mm each side; the strip sits on them with two M3 screws, 14 mm above the plate, between the lid flange and the frame deck's opening edge (Figure 24).

**Check before moving on.** The strip is level and clears the lid flange by at least 2 mm.

### 3.10 Bought components

*Table 2. Bought components and what to do to them.*

| Component | What to buy (specification) | What to do to it |
| --- | --- | --- |
| Corner spacers (4) | Aluminium round spacers 16 mm OD x 8 mm, M4 clearance | Nothing |
| Locking pins (2) | Stainless indexing plungers, M10 x 1, 5 mm hardened pin, at least 9 mm stroke, pull knob with a rest (lock-out) position, with jam nuts | Paint a red band round each pin just below the lip when the pin is withdrawn, so a withdrawn pin shows red |
| Bonded inserts (16) | Aluminium flanged M3 inserts for a 4.2 mm hole in 2 mm composite plate | Bond into the plate (3.1) |
| Standoffs (8) | M3 male-female aluminium: four 25 mm, four 8 mm | Nothing |
| Dampers (4) | Silicone grommet dampers for M3, about 10 mm tall, rated -40 °C | Choose hardness for the controller's mass |
| Flight controller | Pixhawk FMUv6X class with standard baseboard | Load released PX4 and the Kitewright parameter set |
| GNSS receiver and mast | Multi-band GNSS with compass; 10 mm OD carbon tube, 150 mm; M3 thumbscrew | Fix the receiver to the tube's top with its own mount |
| Power distribution board | 18 to 60 V, 200 A peak, two inputs, two outputs, Hall current sensor, about 80 x 50 mm | Nothing |
| Power modules | Digital power monitor with 5.3 V supply, backup 5.3 V supply, payload switch (60 V, 8 A) | Nothing |
| Telemetry radio, receiver, antennas | 900 MHz class radio pair, long-range control link receiver, three antennas and SMA bulkhead pigtails | Set the band and power for the country of use |
| DS-014 pigtail | 40-pin connector pair per DS-014, 0.3 m pigtail, cable clamp | Wire to the controller and payload switch per the pin table |
| Safety switch, grommets, harness, gasket sheet, fasteners | As in `bom/bom.csv` | Nothing |

## 4. Putting it together

### Step 1: rails onto the core plate

![Figure 10. Step 1](05-build-plan/step-01.png)

Turn the plate upside down. Lay the two spacer bars along its long edges, the front stops at the front against their inner edges, then the taped lips, outer edges flush. Push ten M4 x 16 countersunk screws up through lip, spacer bar and plate (and the two stop screws through lip, stop and plate), and fit nylon-insert nuts on top. Use thread-locker; tighten to about 2 N·m. **Hold point:** do the shoe-offcut and feeler check of 3.4 now.

![Figure 11. Joint 1](05-build-plan/joint-01.png)

*Figure 11. The rail cut across at a screw: the shoe's edge runs on the taped lip, 0.3 mm under the plate.*

### Step 2: pin blocks and locking pins

![Figure 12. Step 2](05-build-plan/step-02.png)

Fit each pin block under its lip at the rear with two M4 x 35 cap screws up through block, lip, spacer bar and plate, nuts on top. Screw a plunger up into each block until, released, its pin tip is 0.5 mm short of the plate; lock it with the jam nut.

![Figure 13. Joint 2](05-build-plan/joint-02.png)

*Figure 13. A locking pin cut through its axis: the pin rises through the lip into the shoe.*

![Figure 14. Joint 3](05-build-plan/joint-03.png)

*Figure 14. A front stop, clamped between plate and lip by the stop screw.*

### Step 3: power board

![Figure 15. Step 3](05-build-plan/step-03.png)

Turn the plate the right way up. Screw the four 8 mm standoffs into their inserts and fix the power board on them with M3 screws. Leave its four power pads (two pack inputs, two frame outputs) bare and tinned: the frame's harness leads are soldered to them in step 9.

### Step 4: flight controller on its dampers

![Figure 16. Step 4](05-build-plan/step-04.png)

Screw the four 25 mm standoffs into their inserts, fit a damper on each, lay the damping plate on the dampers and fix it with M3 screws into the dampers. Fix the flight controller to the plate with M3 nylon screws, arrow forward.

![Figure 17. Joint 5](05-build-plan/joint-05.png)

*Figure 17. Flight controller damping, cut through a damper.*

### Step 5: radio, power modules and receiver

![Figure 18. Step 5](05-build-plan/step-05.png)

Stick the telemetry radio (left front), power modules (right front) and control link receiver (right, under the damping plate) to the plate with foam tape, at room temperature. Plug in the harness: power modules to the controller's two power inputs, radio to a telemetry port, receiver to the control input, power board current sensor to its input, payload switch enable to a spare output.

### Step 6: DS-014 pigtail

![Figure 19. Step 6](05-build-plan/step-06.png)

Pass the pigtail's plug down through the cable slot from above and clamp the cable to the plate just behind the slot. Wire its power pins to the payload switch and its data pins to the controller's Ethernet, CAN, serial and trigger ports, per the DS-014 pin table.

![Figure 20. Joint 4](05-build-plan/joint-04.png)

*Figure 20. The pigtail through the slot and the shoe's notch; the plug hangs in front of the payload.*

### Step 7: gasket and lid

![Figure 21. Step 7](05-build-plan/step-07.png)

Stick the gasket to the plate around the avionics. Fit the two grommets to the lid's rear wall. Lower the lid onto the gasket and fit six M3 x 8 cap screws through the flange into the bonded inserts, snug but not crushing the gasket.

![Figure 22. Joint 6](05-build-plan/joint-06.png)

*Figure 22. Lid flange to plate: screw, gasket and the bonded insert, flush underneath.*

### Step 8: antennas, GNSS mast and receiver

![Figure 23. Step 8](05-build-plan/step-08.png)

Fit the three SMA bulkheads through the lid top and screw on the antennas. Press the safety switch into its hole. Push the mast into its socket, lock it with the thumbscrew, and run the GNSS cable in through the hole beside the boss.

### Step 9: strain-relief bar; the frame's harness leads

![Figure 24. Step 9](05-build-plan/step-09.png)

Screw the two 11 mm standoffs into their inserts behind the lid and fix the strip on them. The core is now complete; it carries no power leads of its own. When it goes into a frame, take the lid off, pass that frame's four harness leads (two pack inputs, two frame outputs, made and plugged to the frame's own build plan, with input and output plugs of opposite gender) in through the rear grommets, two per grommet, and solder each to its marked pad on the power board. Refit the lid, then tie each lead to the strip with a cable tie. **Hold point:** check the polarity of every lead at its plug with a meter before step 11.

### Step 10: payload shoe in from the rear (payload swap)

![Figure 25. Step 10](05-build-plan/step-10.png)

Pull both plunger knobs down and twist them to their rest. Slide the shoe into the rail from the rear until it meets the front stops. Twist both knobs back: the pins snap up into the shoe. Push the DS-014 plug into the payload's socket. **Hold point:** no red band shows on either pin, and a firm tug does not move the shoe.

### Step 11: into the frame

![Figure 26. Step 11](05-build-plan/step-11.png)

Put a corner spacer on each frame hole of the plate, lift the core so the lid passes up through the frame deck's opening, and fit four M4 bolts down through deck, spacers and plate with nylon-insert nuts underneath. Plug the frame's speed controller wiring into the two frame output leads of its harness.

![Figure 27. Joint 7](05-build-plan/joint-07.png)

*Figure 27. Core to frame deck at a corner: the deck belongs to Kitewright Lift or Range.*

## 5. First checks

*Table 3. First checks; a TRL 4 test report records the results.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Rail fit | R2, R3 | Slide the shoe the full rail length; feeler gauge above it | No binding; 0.2 to 0.4 mm gap; both pins drop in at the stops |
| Pin retention | R3 | Pull each pin to its rest and back; tug the shoe with one pin withdrawn | Each pin alone stops the shoe; red band shows only when withdrawn |
| Proof load | R3 | Hang 15 kg from the shoe for 1 min on the bench (core on a fixed stand, nobody beneath) | No permanent set, no slip |
| Payload swap | R2 | Timed swap with winter gloves, three people, three times each | 60 s or less, no tools |
| First power | R4, R5 | Bench supply at 24 V, current limit 1 A, no packs | Controller boots; both 5.3 V rails in range; no part warm to the touch |
| Payload power | R4 | Payload switch on into a 100 W load at 18 V and 50 V | Load holds 100 W; switch and pigtail stay below 60 °C |
| Cold boot | R5 | Soak the core at -20 °C for 2 h, then power from the bench supply | Boots and logs normally |
| Interface | R1, R8 | DS-014 continuity and a MAVLink payload heartbeat with a reference payload | Every pin in the table connected; payload recognised |
| Firmware | R10 | Load the released PX4 build and the parameter set | No source changes; parameters load |
| Mass | R9 | Weigh the core without the shoe, packs and frame harness leads | 1.0 kg or less (estimate 0.996 kg, a 4 g margin) |

## 6. Safety stops

Work stops at each point below until what it says is true.

1. **Before first power.** Every solder joint inspected; no pack anywhere near the bench; the power board's inputs checked for shorts with a meter; the bench supply set to 24 V and 1 A.
2. **Before connecting a pack.** The bench checks of section 5 passed; the frame harness leads soldered and tied to the strain-relief bar, inputs and outputs keyed by opposite-gender AS150 plugs and labelled; polarity checked at the plug with a meter; the pack warm enough to discharge (ColdCell reports at least 10 °C); a lithium fire plan, sand bucket and extinguisher at hand; the core on a non-flammable surface; nobody alone.
3. **Before loading the mount.** Both pins show no red band and the shoe passes the tug test; the core is held on a fixed stand, not in a frame; nobody under the load.
4. **Before fitting propellers or arming any frame.** That frame's own build plan safety stops apply; the core's safety switch works; failsafes for the altitude band are loaded.
5. **Before any flight with a payload.** Pin check and tug test done by a second person; the flight follows local rules and the site partner's permissions.

## 7. Tools, skills and workspace

- Hacksaw or bandsaw, files, deburring tool, square and scriber; pillar drill with 3.2, 3.4, 4.2 (or 4.22), 4.5, 5.5 and 9.0 mm drills, carbide for the carbon plate; 90° countersink; M10 x 1 tap and wrench; a small mill or a drill press with an X-Y table and a 6 mm end mill for the rail windows and pockets.
- Structural epoxy, release film and a flat sheet for bonding the inserts.
- FDM printer that can print ASA (enclosure, heated bed); heat-set insert tip.
- Temperature-controlled soldering station of 100 W or more for 8 AWG; heat-shrink and heat gun; crimp tools for JST-GH.
- Multimeter, current-limited bench supply (at least 60 V, 5 A), feeler gauges, kitchen scale.
- Skills: careful marking and drilling to 0.2 mm, tapping, soldering heavy leads, and following the PX4 setup guide.
- A bench with good light and ventilation, and a non-flammable area with a lithium fire plan for any work with packs.

## 8. Where the numbers come from

- `cad/src/model.py`: every size and position, and the 646 constructability checks.
- `cad/drawings/KWC-DWG-001`: general arrangement; `KWC-DWG-101` to `108`: the making sketches.
- `docs/04-calcs/01-sizing.md` and `sizing.py` (KWC-CAL-001): loads, swap time, power, heat, altitude, mass and cost.
- `bom/bom.csv`: parts, specifications and prices.
- `docs/decisions/0001-trl2-review-decisions.md`, `0002-design-for-construction.md` and `0003-requirement-decisions-round2.md`.
