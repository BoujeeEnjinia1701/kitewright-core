"""Kitewright Core general arrangement sheet KWC-DWG-001, Rev P2 (TRL 3, constructable design of KWC-DDR-002 with KWC-DDR-003).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/KWC-DWG-001.svg, .pdf and .png from cad/src/model.py with .kit/drawing.py.
The orthographic views leave out the removable GNSS mast, receiver and antennas so the core fits
the sheet at 1:2.5; the isometric view shows everything. Dimensions in the notes come from PARAMS
and derived(). The concept blueprint in media/ is KWC-DWG-010; making sketches are KWC-DWG-101 on.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Compound  # noqa: E402
from drawing import Sheet  # noqa: E402
from model import PARAMS as P, build_components, derived  # noqa: E402

DATE = "2026-10-03"


def safe_project_views(part, workdir, line_weight=0.35):
    """As drawing.project_views, edge by edge, so a degenerate edge from the hidden-line projection is
    skipped instead of stopping the export."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center()
    d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out, skipped = {}, 0
    for name, (origin, up) in setups.items():
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", visible), ("Hidden", hidden if name != "iso" else [])):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    skipped += 1
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    print(f"projected views; skipped {skipped} degenerate edges")
    return out


def main():
    D = derived(P)
    C = build_components(P)
    removable = ("mast", "gnss", "antennas")
    work = ROOT / "cad" / "drawings" / "_views"
    views = safe_project_views(Compound([s for k, s in C.items() if k not in removable]), work)
    iso = safe_project_views(Compound(list(C.values())), work / "iso")["iso"]
    s = Sheet(project="Kitewright Core", title="Kitewright Core shared avionics and payload core: general arrangement",
              dwg_no="KWC-DWG-001", rev="P2", author="Amish Chadha", date=DATE, scale=0.4, theme="technical",
              material="Carbon fibre plate, 6061 aluminium rails, printed ASA lid, bought avionics per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "First issue, constructable design (KWC-DDR-002)", DATE, "AC"),
                         ("P2", "Carbon plate, 1.5 mm lid, pocketed rails, leads to frame harness (KWC-DDR-003)", DATE, "AC")])
    s.add_ortho(views)
    s.add_svg(iso, 276, 30, 140, 92, label="Isometric view", sublabel="Not to scale; with GNSS mast and antennas")
    L, W, t = P["plate"]
    fx, fy, fd = P["frame_holes"]
    lL, lW, lH, wall = P["lid"]
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Core plate {L:.0f} x {W:.0f} x {t:.0f}, carbon fibre; top face is the datum, Z = 0",
        f"Frame bolts 4 x M4 on {2 * fx:.0f} x {2 * fy:.0f}; spacers {P['corner_spacer'][0]:.0f} OD x {P['corner_spacer'][2]:.0f}",
        f"Frame deck opening {P['deck_opening'][0]:.0f} x {P['deck_opening'][1]:.0f} (frame repos)",
        f"Lid {lL:.0f} x {lW:.0f} x {lH:.0f}, flange {P['flange'][0]:.0f} x {P['flange'][1]:.0f}, 6 x M3 into bonded inserts",
        f"Rails {P['rail_x'][1] - P['rail_x'][0]:.0f} long: spacer {P['spacer_bar'][0]:.0f} x {P['spacer_bar'][1]:.0f}, lip {P['lip'][0]:.0f} x {P['lip'][1]:.0f}",
        f"Shoe {P['shoe'][0]:.0f} x {P['shoe'][1]:.0f} x {P['shoe'][2]:.0f}; gap to plate {D['shoe_gap']:.1f}; slides in from the rear",
        f"Lip overlap {D['overlap']:.0f} each side; payload neck within {2 * D['neck_halfwidth'] - 2:.0f} wide",
        f"Two locking pins, 5 mm, at X {P['pin_xy'][0]:.0f}, Y +/-{abs(P['pin_xy'][1]):.0f}",
        f"DS-014 pigtail through slot {P['slot'][1] - P['slot'][0]:.0f} x {P['slot'][2]:.0f} at X {P['slot'][0]:.0f} to {P['slot'][1]:.0f}",
        f"GNSS top {D['gnss_top']:.0f} above the plate; knob bottom {-D['knob_bot']:.0f} below",
        "Rated 5 kg, 100 W; bus 18 to 60 V; power leads in the frame harness",
        "Third-angle; X forward along the rail; front view from -Y",
    ], x=276, y=140, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "KWC-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
