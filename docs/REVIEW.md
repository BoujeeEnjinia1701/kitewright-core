# Review note: Kitewright Core

## Session 2026-09-30: scaffolded

### What was done

- Repository created from kit 1.6.0 at TRL 1, target TRL 2.
- `docs/01-problem.md` (KWC-PRB-001 v0.1): problem with cited evidence, users, environment, constraints, prior work, open questions.
- `docs/02-concept.md` (KWC-PRC-001 v0.1): how it works, components, patent design-arounds, shared blocks, safety.
- `docs/03-requirements.md` (KWC-REQ-001 v0.1): 11 proposed requirements.
- `README.md` with concept rationale, burning platform, where it could be used, and what sparked the idea.

### Next

- Run `/populate` to bring the repo to a strong TRL 2 with concept media.

## Session 2026-10-03: TRL 2 (populate), under Amish's pre-approval

Kit 1.7.0 installed. Amish's go for the batch (2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." and "Proceed with the remaining 15 scaffolds") counts as the TRL 2 approval, and every recommendation below is decided under it.

### What was done

- `docs/01-problem.md` (KWC-PRB-001 v0.2): open questions answered, co-design candidate named, budget worded as a value-engineering target, safety section.
- `docs/03-requirements.md` (KWC-REQ-001 v0.2): targets unchanged; rated payload, bus window and the R9 boundary defined; TRL 3 status per requirement.
- `docs/02-concept.md` (KWC-PRC-001 v0.2): how it works, components, key figures, design choices, safety section.
- Massing and media from `cad/src/concept_media.py`: `media/hero.png` (adult hand for scale), `cutaway.png`, `exploded.png` with BOM callouts, `flow.png` (power flow, estimates), `concept-blueprint.png/.pdf` (KWC-DWG-010), `model.glb` (coarse deflection, about 3 MB) and `viewer.html`.
- `bom/bom.csv`: 35 priced lines with suppliers.

### TRL 2 review items and how they were decided

Each item below was offered with options and a recommendation, and is recorded as decided in KWC-DDR-001 (D1 to D15): PX4 primary (D1); FMUv6X class controller (D2); 18 to 60 V bus (D3); one 5 kg, 100 W payload class (D4); plain rail with rear entry, front stops and pigtail (D5); two independent locking pins (D6, safety: conservative); core under the frame deck (D7); companion computer outside the core (D8); DroneCAN pack data (D9); radios per country (D10); three altitude bands (D11); DS-014 licence confirmed before purchase (D12); first co-design candidate to approach, not agreed (D13); logging and remote ID (D14); published hover-time model (D15).

### Safety concerns

- Lithium packs at up to 60 V and 200 A: bench supply first, anti-spark keyed connectors, fire plan.
- Falling payload: two pins, red bands, tug test before every flight.
- Propellers: the frames' safety stops apply; the core's safety switch gates arming.

## Session 2026-10-03: TRL 3 (advance and build plan), under Amish's pre-approval

### What was done

- `docs/04-calcs/01-sizing.md` and `sizing.py` (KWC-CAL-001 v0.1), `results.csv`.
- `cad/src/model.py`: parametric build123d model of the constructable core with 614 constructability checks, all passing; `cad/step/kitewright-core-assembly.step` and STL for the plate, lid, shoe, pin block and damping plate.
- `cad/src/sheets.py`: general arrangement KWC-DWG-001 Rev P1.
- `cad/src/build_plan_media.py`: overview, eight making sketches (KWC-DWG-101 to 108), seven joint close-ups and eleven step pictures.
- `docs/05-build-plan.md` (KWC-BLD-001 v0.1), `docs/06-design-decisions.md` (KWC-DEC-001 v0.1), `docs/decisions/0002-design-for-construction.md` (KWC-DDR-002).
- `cad/src/product_model.py` and render scenes exported to `/home/claude/renders/kitewright-core` (hero, exploded, detail, and the jobs file). Photoreal renders, captions and cards are made on Amish's Mac; the README already leads with `media/render-hero.png`.
- `project.yaml`: trl 3, trl_target 3, design_state constructable, trl_evidence listed. `budget_usd` unchanged.

### Results (KWC-CAL-001)

| ID | Status | Result |
| --- | --- | --- |
| R1 | Met on paper (licence and pinout to confirm) | DS-014 40-pin pigtail with bus and controller signals |
| R2 | Met on paper (estimate) | About 52 s with gloves, no tools |
| R3 | Met on paper | Factor 10.8 or more at 147 N; 221 N fore-aft on one pin alone |
| R4 | Met on paper (pin rating to confirm) | At most 5.6 A for 100 W |
| R5 | Met on paper | Hottest part about 75 °C at 45 °C ambient |
| R6 | Met on paper for the core | Sensors in range at 54 kPa; failsafes per band |
| R7 | Model ready; accuracy only at TRL 4 | 47 % (cold packs) and 70 % (ColdCell) of sea-level hover time at 5,000 m and -20 °C |
| R8 | Met by design | Lift 11, Range 10 of 16 outputs |
| R9 | Not met | 1.27 kg estimated |
| R10 | Met by design | Released PX4, parameters only |
| R11 | Under the value-engineering target | Value-engineering target: USD 5,000. Estimated cost of the constructable design: USD 3,940.60 (USD 1,059.40 under the target) |

### Requirements not met

- R9, core mass (below). R2 has a small margin and needs the gloved trial at TRL 4.

### Decisions for Amish

**R9, core mass.** State: the constructable core is estimated at 1.27 kg against R9, 274 g over. Cause: the plate, rails, pin blocks and lid are sized for making from aluminium sheet and bar (strength factors of 10 to 99), and the four 8 AWG power leads with their AS150 plugs (124 g) sit inside the core.

| Option | What changes | Effect on R9 | Cost | Mass |
| --- | --- | --- | --- | --- |
| A | Lighter structure: 2 mm carbon fibre plate, 1.5 mm lid walls, pockets milled in the rail bars | Still not met (about 1.12 kg) | About USD 60 more | -157 g |
| B | A, plus the pack and frame leads and AS150 plugs moved to each frame's harness; the core keeps solder pads and a strain-relief bar | Met (about 0.99 kg) | About USD 60 more on the core; USD 60 of leads move to the frames | -281 g |
| C | Keep the design as drawn | Not met (1.27 kg) | None | None |

**Recommendation: B.** It meets R9 with a small margin, keeps every strength factor above 5, and the lead lengths were frame-specific anyway; it needs Kitewright Lift and Kitewright Range to own their power leads. Listed in KWC-DEC-001 as O1, "Proposed, awaiting Amish".

### Decisions made under the pre-approval

- KWC-DDR-001, D1 to D15 (TRL 2 review), and KWC-DDR-002, C1 to C10 (design for construction), all dated 2026-10-03 and indexed in KWC-DEC-001.

### Build plan findings (design changes made for construction, KWC-DDR-002)

- C1 plain rail of spacer bars and taped lips; C2 two plungers in pin blocks; C3 front stops clamped by the rail screws; C4 DS-014 pigtail through a plate slot and a shoe notch; C5 flush clinch nuts under the plate; C6 core hung under the frame deck on spacers, lid through a deck opening; C7 damped controller plate above the power board; C8 printed lid with gasketed flange; C9 leads out through grommets, plugs soldered last; C10 removable GNSS mast.
- The shoe's 0.3 mm running gap depends on stock thicknesses and the tape; the first check is a feeler-gauge check along the rail.

### Appearance model

- `cad/src/product_model.py` uses the model's components unchanged; there are no appearance deviations from `model.py`. The hero places an adult hand beside the core on the bench, to the right of it in view, never in front.

### Safety concerns

- Lithium power path (60 V, 200 A peak): build plan safety stops 1 and 2; inputs and outputs keyed by opposite-gender plugs.
- Payload retention: two independent pins (D6, conservative). A vibration and pull test on the built mount could justify one pin later.
- The proof-load check (15 kg) is done with the core on a fixed stand and nobody beneath.
- Radio band and power must be legal at each site; flights only under the site partner's permissions.

### Cross-repo actions (sibling repos not edited)

- **Kitewright Lift and Kitewright Range:** provide a lower deck with four M4 hard points on a 220 x 130 mm pattern, a 200 x 112 mm opening for the lid, and at least 70 mm clear above the deck for the lid and 240 mm for the GNSS mast (or a frame position for the GNSS on a longer cable); carry the core's mass of about 1.27 kg (0.99 kg if O1 goes with B); accept AS150 frame outputs on an 18 to 60 V bus; keep the payload's neck zone (88 mm wide, 30 mm below the lips) and the area behind the rail clear for rear entry of the shoe. If O1 goes with B, each frame supplies its own pack and output leads.
- **Kitewright Range:** fuselage pod interior at least 150 mm wide at the core position; 10 of the controller's 16 outputs are used.
- **ColdCell:** report temperature and charge over DroneCAN; AS150 pack connector; pack voltage within 18 to 60 V; block charging when cold (the core does not).
- **AvalancheScout, LakeWatch and other payloads:** carry a 184 x 128 x 5 mm shoe to KWC-DWG-106, stay within 5 kg and 100 W, and put the DS-014 socket where the plug reaches in front of the shoe's notch.
- **AltiRig:** supply the hover-thrust factors used in the altitude parameter sets (KWC-CAL-001, Table 6).

### Recommended next step

Amish decides O1 (R9). The design is ready for TRL 4 (build and bench checks of section 5 of the build plan) once the DS-014 licence and pinout are confirmed; that is a recommendation, not started.

## 2026-10-03: photoreal renders

Rendered with Blender Cycles on Amish's Mac from `cad/src/product_model.py`; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` made with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes and `render.py --check` has no FAIL.

## 2026-10-03: Amish's requirement decisions carried out

Amish Chadha (owner) on 2026-10-03: "i agree with all the 46 recommendations you provided. please proceed." His round 2 decision for this repo is item 33B: lighter structure and the power leads moved out of the core into the frames. It is recorded in KWC-DDR-003 (`docs/decisions/0003-r9-core-mass.md`) and in the register (`docs/06-design-decisions.md`, O1 moved to Decisions made).

### Changes made

- **Model** (`cad/src/model.py`; 720 constructability checks, all passing, up from 614). New checks cover the strain-relief bar, the frame harness drawn as context (it reaches the pads, the grommets and the bar, and overlaps nothing), a flush underside wherever the shoe runs, the metal left by the pockets and the land under each countersink. STEP and STL regenerated.
  - Core plate: 2 mm carbon fibre, CNC-cut, in place of 2 mm 5052 aluminium. The 14 clinch nuts cannot go into carbon, so 16 M3 holes are countersunk from below; countersunk screws set with thread-locker carry the standoffs (now female-female) and act as the lid's six studs (nylon-insert nuts on the flange).
  - Rail spacer bars: three 3.6 mm windows between the screws. Rail lips: three 1.8 mm pockets underneath. Both are clear-anodised, as are the front stops, corner spacers and standoffs, because they touch the carbon.
  - Pin blocks from 30 x 12 mm bar (was 15 mm; M4 x 30 screws); corner spacers 12 mm OD (was 16 mm); lid walls and top 1.5 mm (was 2 mm).
  - Power leads and AS150 plugs removed from the core. The frame's own harness comes in through the existing grommets and is soldered to the board's pads. A new strain-relief bar (G10, 60 x 8 x 2 mm, on two 12 mm standoffs behind the lid) takes any pull on the leads.
- **BOM** (`bom/bom.csv`): lines 1, 2, 3, 4, 6, 7, 10, 14, 20, 21 and 27 changed, each with a price basis. Line 20 is now the countersunk fixings and line 21 the strain-relief bar (the USD 60 of leads and plugs move to the frames).
- **Calculations** (KWC-CAL-001 v0.2): sections A, H, I and the results updated; new checks A2 (the lip at its pocket floor), A4 (the carbon side beam with the windowed bar) and A8 (carbon bearing).
- **Requirements** (KWC-REQ-001 v0.3): R3, R8, R9 and R11 status updated, and the R9 definition now excludes the frame's harness. No targets changed; 33B does not restate a requirement.
- **Build plan** (KWC-BLD-001 v0.2): sections 1, 2, 3.1, 3.2, 3.3, 3.4, 3.5 and 3.7, a new section 3.9 (strain-relief bar, Figure 10; later figures renumbered), Table 2, steps 1 to 4, 7, 9 and 11, the first checks, safety stop 2, and tools.

### New result per requirement

| ID | Before | Now | Target |
| --- | --- | --- | --- |
| R9 | 1.27 kg, not met | 0.99 kg, met on paper (10 g margin; bought-part masses to confirm, T9) | 1.0 kg or less |
| R3 | Factors 10.8 or more | Factors 8.3 or more: lips 19 x at the pocket floor, carbon side beam 8.3 x, carbon bearing 14 x, screws 69 x, one pin 36 x | 3 x static, 1.5 x at 2 g |
| R11 | USD 3,940.60 | Value-engineering target: USD 5,000. Estimated cost of the constructable design: USD 3,946.80 (USD 1,053.20 under the target) | USD 5,000 |
| R8 | Met by design | Met by design for firmware and fixing; a core moved between frames now needs a harness change (O2, below) | Parameter changes only |

All other requirements are unchanged. Mass breakdown: carbon plate -81 g, rail windows and pockets -44 g, pin blocks and corner spacers -20 g, lid -24 g, leads and plugs -124 g, strain-relief bar and fixings +9 g; 284 g lighter in all. Cost: about USD 58 more for the structure, USD 8 for the strain-relief bar, USD 0.80 less in fixings and USD 60 of leads out: USD 6.20 more in all.

### Pictures changed

General arrangement KWC-DWG-001 to Rev P2. Making sketches KWC-DWG-101, 102, 104, 105 and 107 to Rev P2, and KWC-DWG-109 (strain-relief bar) new. The other sketches were redrawn unchanged. Also redrawn: the overview, joints 1, 2, 5, 6 and 7, all eleven step pictures (step 3 is now the power board alone, step 9 the strain-relief bar, and step 11 adds the frame's harness), and the concept media (hero, cutaway, exploded, blueprint, flow, model.glb). The appearance model (`cad/src/product_model.py`) shows the carbon plate and the strain-relief bar; render scenes were exported again. The photoreal renders, captions and cards in `media/` still show the aluminium plate with leads and need a re-run on Amish's Mac.

### New decision for Amish

**O2, R8 common core and the frame harness.** State: since 33B the frame's power leads are soldered to the core's board pads. A core moved between Lift and Range therefore needs its harness changed: lid off, four 8 AWG leads desoldered and the other frame's soldered on. R8 reads "parameter changes only".

| Option | What changes | Effect | Cost and mass |
| --- | --- | --- | --- |
| A | Accept a bench harness change (about 30 min, lid off) and restate R8 as "same core flies Lift and Range with parameter changes and a change of the frame's power harness at the board" | R8 met as restated; R9 stays met | None |
| B | Four M4 studs on the board's pads, with ring lugs on the frame leads: a nut-driver swap, no soldering | R8 closer to its wording; R9 missed by about 2 g | About 12 g and USD 15 more |
| C | AS150 plugs back on short core pigtails | R8 met as written; R9 not met (about 1.06 kg) | About 70 g more |

**Recommendation: A.** The R8 check at TRL 4 is a single bench swap by the builder, soldering 8 AWG is already in the build plan, and R9 stays met. Listed as O2 in KWC-DEC-001, "Proposed, awaiting Amish".

### Safety

- Carbon dust when cutting or filing the plate: wet or under extraction, with a mask.
- Galvanic corrosion between aluminium and carbon: every aluminium part that touches the plate is anodised, and the plate's edges are sealed.
- The frame's harness is soldered inside the lid. Safety stop 2 now checks the harness's keyed, labelled AS150 plugs and their polarity before any pack is connected.
- The countersinks leave 0.4 mm of carbon under each M3 head (T7). If the heads pull through, the fallback is bonded flush inserts.

### Cross-repo actions (not edited here)

- **Kitewright Lift and Kitewright Range** (Core decision 33B): each frame supplies its own power harness: two pack leads and two output leads in 8 AWG, with AS150 plugs (inputs and outputs of opposite gender), labelled, and long enough to pass through the core's two rear grommets (20 mm holes, 13 mm each side of the centre line, 18 mm above the plate) to the board's pads, about 20 mm inside the lid's rear wall. Mass about 124 g and cost about USD 60 per frame. Core mass for frame sizing is now about 0.99 kg.
- **Kitewright Lift and Kitewright Range:** the core's corner spacers are now 12 mm OD (were 16 mm); the 220 x 130 mm M4 pattern and the 200 x 112 mm deck opening are unchanged. Keep 1 mm or more clear of the strain-relief bar, which sits 91 to 99 mm behind the core's centre, up to 14 mm above the plate.

## 2026-10-04: Amish's round-3 decisions carried out

Amish Chadha (owner) on 2026-10-04: "For round 3, I agree with all your proposed recommendations". For Kitewright Core that is item 7A (register item O2, R8) and its share of the Kitewright family reconciliation (8A, 9A and 10A), which also touched Kitewright Lift, Kitewright Range, ColdCell, AvalancheScout and LakeWatch. Recorded in `docs/decisions/0004-r8-harness-change.md` (KWC-DDR-004) and the register (`docs/06-design-decisions.md` v0.3). Nothing was committed or pushed.

### Changes made

- **7A, R8 restated** (`docs/03-requirements.md` v0.4): "Same core flies Lift and Range with parameter changes and a change of the frame's power harness at the board." The bench harness change (lid off, four 8 AWG leads resoldered, about 30 min) is accepted. New result: **R8 met by design as restated.** No hardware, cost or mass change; R9 stays 0.99 kg (met on paper) and R11 USD 3,946.80 (USD 1,053.20 under the USD 5,000 target).
- **Build plan** (`docs/05-build-plan.md`): step 11 now says how a core moves to the other frame.
- **10A, interface reconciliation:** the Core's drawings (KWC-DWG-001 Rev P2, KWC-DWG-106) are the reference for the one mounting envelope that Lift and Range now both carry; both frames model the Core from these figures (`cad/src/core_envelope.py` in each). No change to the Core itself, so the model, drawings and render scenes are unchanged.

### Kitewright interface table

The same table stands in the review notes of Kitewright Core, Kitewright Lift, Kitewright Range, ColdCell, AvalancheScout and LakeWatch (Amish's decision 10A, 2026-10-04). The Core's drawings are the reference for the mounting envelope.

| Interface | Family figure | Source |
| --- | --- | --- |
| Power connector | AS150 on every pack lead and on each frame's power harness (two pack inputs, two frame outputs, opposite genders); no XT60 or XT90 on the bus | Decision 10A; KWC-DDR-001, D3 |
| Core mounting envelope and hole pattern | Core plate 240 x 150 x 2 mm hung under the frame's lower deck on four 12 mm OD x 8 mm corner spacers; four M4 holes on a 220 x 130 mm pattern; a 200 x 112 mm opening in the deck for the lid; lid 168 x 92 mm, its top 55 mm above the deck's underside (GNSS mast boss 69 mm); where a frame has no 240 mm clear above the lid, the antennas and GNSS receiver go to frame positions on extension cables; rail, pin blocks and pin knobs to 47 mm below the plate top; payload shoe 184 x 128 x 5 mm, payload neck 88 mm wide from the shoe to 30 mm below the rail lips | KWC-DWG-001 Rev P2, KWC-DWG-106 |
| Bus voltage | 18 to 60 V at the Core's pack inputs. Lift: 14S lithium-ion, 42.0 to 58.8 V (50.4 V nominal). Range: 6S lithium-ion, 18.0 to 25.2 V (21.6 V nominal) | KWC-DDR-001, D3 |
| Pack size and mass | Lift: two ColdCell 14S3P lithium-ion packs, 410 x 94 x 94 mm, 4.46 kg and 680 Wh each (CCL-DWG-002). Range: two 6S3P lithium-ion packs of 5.0 Ah cells, 138 x 75 x 82 mm, 1.40 kg and 324 Wh each (Range's figure; ColdCell has not yet drawn this pack) | Decision 8A; CCL-CAL-001 K; KWR-CAL-001 |
| Core mass | 0.99 kg: avionics, radios, GNSS, rail and locking pins; packs, payload shoe and the frame's harness excluded | Core R9; KWC-DDR-003 |

What the frames gave the Core when they took this envelope (nothing in the Core changes): Lift hangs the Core under its bottom hub plate with 63 mm from the deck's underside to its top hub plate, which is drilled over the lid's mast boss, SMA bulkheads and switch; Range hangs it under its fuselage floor at the centre of gravity, the fuselage widened to 150 mm inside. Both take the Core's GNSS receiver and antennas to frame positions on extension cables, as the table allows. The Core asked for 70 mm clear above the deck; its own drawing needs 55 mm for the lid and 69 mm at the mast boss.

### Pictures changed

None: no geometry changed in this repo.

### Open decisions

None. Nothing in carrying out 7A or the reconciliation needs Amish here.

### Safety

- A harness change means soldering 8 AWG leads inside the lid: every pack disconnected, a 100 W iron, and safety stop 2 (polarity at the AS150 plugs with a meter) repeated before the first pack goes on.

### Cross-repo actions

- None outstanding from this repo: Lift, Range, ColdCell, AvalancheScout and LakeWatch were brought to the table in the same reconciliation.

### Recommended next step

Unchanged: the design is ready for TRL 4 (build and the bench checks of section 5 of the build plan) once the DS-014 licence and pinout are confirmed; a recommendation, not started.

## 2026-10-04: photoreal renders redone after the round-2 and round-3 decisions

Views: hero, exploded, detail; cards regenerated; image_qc passes and `render.py --check` has no FAIL.
