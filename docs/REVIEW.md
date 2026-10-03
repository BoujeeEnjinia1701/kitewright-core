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
