# Review note: Kitewright Core

## Session 2026-10-03: round 2 requirement decisions applied

Amish, 2026-10-03: "i approve all of the 47 recommendations provided by you. Execute them." For this repo that is decision O1 (global decision 17, R9 core mass), decided as recommended: option B. Recorded in `docs/decisions/0003-requirement-decisions-round2.md` (KWC-DDR-003). Work stayed inside the TRL 3 cap: no test articles, test plans, firmware, PCB layouts, build-log entries or purchasing lists.

### What was done

- `cad/src/model.py`: core plate changed to 2 mm carbon fibre; three windows milled through each rail spacer bar (1.5 mm walls) and three 2 mm pockets under each lip, with at least 4.25 mm of bar round every hole; lid walls and top 1.5 mm; the four power leads and AS150 plugs removed from the core; a G10 strain-relief bar on two 11 mm posts added behind the lid; clinch nut holes now take 16 bonded flush inserts (14 plus 2 for the bar posts); the frame's harness leads drawn as context (`harness_context`) and checked to reach the board pads, grommets and bar. 646 constructability checks pass (was 614).
- `docs/04-calcs/sizing.py`, `results.csv` and `01-sizing.md` (KWC-CAL-001 v0.2): sections A, C and H recalculated; new lines [A8] (frame bolt bearing in carbon) and [C3] (bus top voltage).
- `bom/bom.csv`: lines 1, 3, 4, 10, 20 and 21 changed (carbon plate, pocketed bars, lid, bonded inserts, strain-relief bar in place of the leads).
- Regenerated: `cad/step/kitewright-core-assembly.step` and the five STL files; `cad/drawings/KWC-DWG-001` Rev P2; making sketches KWC-DWG-101 to 108, overview, joints and steps in `docs/05-build-plan/`; concept media (`media/hero.png`, `cutaway.png`, `exploded.png`, `flow.png`, `concept-blueprint.png` and `.pdf`, `model.glb` at 1.0 mm linear and 0.35 rad angular deflection).
- `docs/05-build-plan.md` (KWC-BLD-001 v0.2), `docs/03-requirements.md` (KWC-REQ-001 v0.3), `docs/02-concept.md` (KWC-PRC-001 v0.3), `docs/06-design-decisions.md` (KWC-DEC-001 v0.2), `README.md`, `cad/src/product_model.py` (carbon plate colour, bar in place of leads), `cad/src/concept_media.py` and `cad/src/sheets.py`, `project.yaml` (trl_evidence).

### Requirement status

| ID | Before | After |
| --- | --- | --- |
| R3 | Met on paper, lowest factor 10.8 | Met on paper, lowest factor 6.8 (side beam at a pocket; lip 13, screws 69, pin 36) |
| R9 | Not met, 1.27 kg | **Met on paper, 0.996 kg** (4 g margin; weigh at TRL 4) |
| All others | Met on paper or by design | Unchanged |

### Cost

Value-engineering target: USD 5,000. Estimated cost of the constructable design: USD 3,944.40 (USD 1,055.60 under the target); before: USD 3,940.60. The core gained USD 59.80 (carbon plate USD 44 more, rail pockets USD 12, bonded inserts USD 4.80, lid USD 1 less) and lost USD 56 net of leads and plugs, which now cost USD 60 in each frame's harness (Kitewright Lift BOM).

### Cross-repo changes

- **Kitewright Lift** (edited in the same round, KWL-DDR-003): its harness gains the two pack input and two frame output leads, 8 AWG with AS150 plugs (USD 60, 124 g), soldered to the core's pads and tied to the strain-relief bar; its Core allowance is now 1.0 kg without leads.
- **Kitewright Range** (not edited in this round): it must also supply its own four leads; its BOM and harness need the same lines when it is next worked on.
- **ColdCell** (edited in the same round, CCL-DDR-003): the new lithium-ion 14S3P variant for Lift reports over DroneCAN and connects through the frame's AS150 pack leads like the reference pack.

### New questions (Proposed, awaiting Amish)

**O2. Bus headroom for the 14S lithium-ion pack.**
- State: Kitewright Lift adopted a 14S lithium-ion ColdCell variant (its decision 2). A full pack reads 58.8 V (a full 16S LiFePO4 pack 58.4 V). The power board and both power modules are rated 60 V, leaving 1.2 V for the short rise in bus voltage when eight motor controllers brake.
- Option A: specify the power board and power modules for a 75 V class rating; estimate about USD 40 more; mass unchanged at catalogue class.
- Option B: keep 60 V parts and charge the Lift packs only to 4.10 V a cell (57.4 V); about 3 % less energy, about 0.6 min less hover for Lift.
- Option C: keep 60 V parts and full charge, relying on the controllers' braking limits.
- **Recommendation: A.** It restores about 16 V of margin with no loss of hover time for a small cost.

**To confirm when parts are bought (T10, added to KWC-DEC-001):** the bonded flush insert type, its bond strength in 2 mm carbon plate and the epoxy's rating from -20 to +45 °C.

### Safety notes

- The core still switches up to 60 V and 200 A. The pack and frame leads now arrive with each frame's harness; polarity and the opposite-gender keying of inputs and outputs are checked at a new hold point when the harness is soldered in (build plan step 9), before any pack is connected.
- Lithium-ion fire energy: Kitewright Lift now flies two 14S3P lithium-ion ColdCell packs (about 680 Wh each), which carry more stored energy and a more violent failure than LiFePO4. The core's role is unchanged (it does not charge packs and passes ColdCell's temperature data to the autopilot), but the lithium fire plan in safety stop 2 applies with more force; see ColdCell CCL-DDR-003 for the pack's own protections.
- Carbon dust from cutting or drilling the plate is a breathing hazard and is conductive: work wet or under extraction and seal every cut edge so no fibre can bridge the power board.
- The bus top voltage (O2) is a margin question for transients, not a hazard at steady state; until O2 is decided, first power stays on the current-limited bench supply as the build plan says.

### Re-render

The hero geometry is the same size and layout, but the plate changes from bare aluminium to black carbon and the four red leads with yellow plugs no longer hang out of the rear of the lid. Both are visible in `media/render-hero.png`, so the photoreal hero, exploded and detail renders and the cards should be re-rendered on Amish's Mac.

### Checks

- `python cad/src/model.py --check`: 646 passed, 0 failed.
- `python .kit/render.py --check`: see the end of this session's report; the only failure left is the missing `media/render-hero.png` storefront image of this working copy.

### Recommended next step

Amish decides O2. The design is then ready for TRL 4 (build and the bench checks of section 5 of the build plan) once the DS-014 licence and pinout are confirmed; that is a recommendation, not started.

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
