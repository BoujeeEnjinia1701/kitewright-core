"""Kitewright Core concept media (TRL 3, constructable design of KWC-DDR-002), from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Takes the components from cad/src/model.py and renders the media set with .kit/concept.py:
media/hero.png, cutaway.png, exploded.png, flow.png, concept-blueprint.png/.pdf, model.glb and
viewer.html. Every coloured part carries the BOM line number used in bom/bom.csv; the grey forearm
and hand is scale context with no BOM number. Figures on the sheet and in the flow diagram come from
docs/04-calcs/sizing.py (KWC-CAL-001). CONCEPT, NOT FOR FABRICATION.

Coordinates in mm: X forward along the payload rail, Y left, Z up, plate top at Z = 0.
"""
import functools
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build123d  # noqa: E402
from build123d import Pos, Rot  # noqa: E402
import concept  # noqa: E402
from concept import Part, render_all  # noqa: E402
from context_parts import forearm_hand  # noqa: E402
from model import BOM, build_components, derived  # noqa: E402

# The kit's glTF export defaults to a 0.001 mm deflection, which makes a huge file; use a coarse one.
build123d.export_gltf = functools.partial(build123d.export_gltf, linear_deflection=1.0, angular_deflection=0.35)

D = derived()
C = build_components()

STYLE = {  # BOM line: (colour, exploded offset in mm)
    1: ("#A8A29E", (0, 0, 0)),
    2: ("#6B7280", (0, 0, 60)),
    3: ("#57534E", (0, 0, -45)),
    4: ("#78716C", (0, 0, -80)),
    5: ("#F5F5F4", (0, 0, -62)),
    6: ("#44403C", (60, 0, -45)),
    7: ("#0E7490", (0, 0, -125)),
    8: ("#C2410C", (0, 0, -175)),
    9: ("#94A3B8", (-60, 0, -230)),
    10: ("#E5E7EB", (0, 0, 260)),
    11: ("#1F2937", (0, 0, 200)),
    12: ("#65A30D", (0, 0, 150)),
    13: ("#111827", (0, 0, 125)),
    14: ("#9CA3AF", (0, 0, 100)),
    15: ("#0F766E", (0, 0, 180)),
    16: ("#1D4ED8", (0, 0, 360)),
    17: ("#374151", (0, 0, 330)),
    18: ("#16A34A", (0, 0, 60)),
    19: ("#7C3AED", (0, -170, 30)),
    21: ("#DC2626", (-150, 0, 60)),
    22: ("#2563EB", (0, 170, 30)),
    23: ("#D97706", (-40, -150, 90)),
    24: ("#4B5563", (0, 0, 320)),
    25: ("#EAB308", (80, 0, -60)),
    26: ("#BE123C", (0, 0, 300)),
    27: ("#111827", (-50, 0, 260)),
}
NAMES = {1: "Core plate", 2: "Corner spacers (4)", 3: "Rail spacer bars (2)", 4: "Rail lips (2)", 5: "Wear tape",
         6: "Front stops (2)", 7: "Pin blocks (2)", 8: "Locking pins (2)", 9: "Payload shoe", 10: "Lid",
         11: "Lid gasket", 12: "Damping plate", 13: "Vibration dampers (4)", 14: "Standoffs (8)",
         15: "Flight controller", 16: "GNSS receiver and compass", 17: "GNSS mast", 18: "Power distribution board",
         19: "Power modules", 21: "Strain-relief bar", 22: "Telemetry radio", 23: "Control link receiver",
         24: "Antennas", 25: "DS-014 pigtail and plug", 26: "Safety switch", 27: "Grommets (2)"}


def parts():
    groups = {}
    for key, shape in C.items():
        n = BOM[key][0]
        groups.setdefault(n, []).append(shape)
    out = []
    for n in sorted(groups):
        shape = groups[n][0]
        for s in groups[n][1:]:
            shape = shape + s
        col, off = STYLE[n]
        out.append(Part(NAMES[n], shape, col, n, off))
    return out


def hand(dist=250.0):
    """A flat left forearm and hand on the bench the core sits on, off to the right of the core in the
    default view (elevation 24 deg, azimuth -58 deg), fingers toward it; never between camera and core."""
    import math
    a = math.radians(-58)
    right = (-math.sin(a), math.cos(a))          # screen-right direction on the ground
    ang = math.degrees(math.atan2(-right[1], -right[0]))
    h = Rot(0, 0, ang) * forearm_hand(side="left", pose="flat", include_forearm=False)
    z0 = h.bounding_box().min.Z
    return Part("Adult hand (scale)", Pos(dist * right[0], dist * right[1], D["knob_bot"] - z0) * h, "#9CA3AF")


if __name__ == "__main__":
    P = parts()
    render_all(
        P, project="Kitewright Core", title="Shared avionics, power and payload core", dwg_no="KWC-DWG-010",
        key_figures=["Core plate 240 x 150 mm; bolts to the frame on a 220 x 130 mm M4 pattern",
                     "Lid 168 x 92 x 62 mm, rises through a 200 x 112 mm opening in the frame deck",
                     "Plain rail and two locking pins; payload shoe 184 x 128 x 5 mm",
                     "Rated payload 5 kg; vertical design load 147 N, lips 13 x, screws 69 x",
                     "DS-014 40-pin pigtail; 100 W to the payload, 8 A switch",
                     "Bus 18 to 60 V; core about 1.00 kg; USD 3,944 with ground station",
                     "Hover time at 5,000 m, -20 C: 47 % cold packs, 70 % ColdCell (est.)"],
        scale_figure=False, context=[hand()],
        cut_exclude=("Antennas", "GNSS mast", "GNSS receiver and compass"),
        flow={"title": "power flow in Lift hover at sea level, W (KWC-CAL-001 estimates)", "unit": "W",
              "stages": [("Two ColdCell packs", 4414.0), ("Core power board", 4410.0), ("Frame ESCs and motors", 4300.0)],
              "losses": [(0, "Bus conduction", 4.0), (1, "Payload via DS-014 (max)", 100.0), (1, "Avionics", 10.0)]},
    )
    print("media written")
