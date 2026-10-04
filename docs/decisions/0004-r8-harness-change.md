---
doc_id: KWC-DDR-004
title: Kitewright Core R8 common core, bench harness change between frames
project: Kitewright Core
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-04'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-04'
  author: Amish Chadha
  change: Amish's round-3 decision 7A (option A of register item O2) recorded and carried out
---

# 0004: R8 common core: accept a bench harness change between frames

- **Date:** 2026-10-04
- **Status:** accepted. Decided by Amish Chadha (owner) on 2026-10-04: "For round 3, I agree with all your proposed recommendations"" (round 3, item 7A).

## Context

Since decision 33B (KWC-DDR-003) each frame's power leads are soldered to the core's board pads, so a core moved between Kitewright Lift and Kitewright Range needs its harness changed: lid off, four 8 AWG leads desoldered and the other frame's soldered on. R8 read "parameter changes only". The point was put to Amish as register item O2.

## Options considered

| Option | What changes | Effect | Cost and mass |
| --- | --- | --- | --- |
| A | Accept a bench harness change (about 30 min, lid off) and restate R8 | R8 met as restated; R9 stays met | None |
| B | Four M4 studs on the board's pads and ring lugs on the frame leads | R8 closer to its wording; R9 missed by about 2 g | About 12 g and USD 15 more |
| C | AS150 plugs back on short core pigtails | R8 met as written; R9 not met (about 1.06 kg) | About 70 g more |

## Decision

Option A, as recommended. R8 is restated in KWC-REQ-001 v0.4: "Same core flies Lift and Range with parameter changes and a change of the frame's power harness at the board." No change to the model, drawings, bill of materials or calculations; the build plan's step 11 already describes the soldered harness, and section 5 now says how a core moves between frames.

## Consequences

- R8 is met by design as restated; R9 stays at 0.99 kg (met on paper).
- The TRL 4 check of R8 is one bench swap by the builder, timed.
- The Kitewright interface table of 2026-10-04 (decision 10A) fixes the frames' side of the swap: the same 220 x 130 mm M4 fixing and AS150 harness plugs on both frames.

> **Safety:** Soldering 8 AWG leads takes a 100 W iron; disconnect every pack first, check polarity with a meter at the AS150 plugs before the first pack goes on, and redo safety stop 2 after every harness change.
