"""Kitewright Core appearance model for product renders (STANDARDS section 12).

Every part and every main dimension comes from cad/src/model.py (build_components); nothing is
retyped here. This file only assigns names, colours, render materials, groups and exploded offsets,
and adds an adult hand from .kit/context_parts.py for scale. No appearance deviations from the model.
Export the render scenes with:  python .kit/export_views.py OUTDIR
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Pos, Rot  # noqa: E402
from context_parts import forearm_hand  # noqa: E402
from model import BOM, build_components, derived  # noqa: E402

TITLE = "Kitewright Core: shared avionics, power and payload core for open drones"

LOOK = {  # component: (name, colour, material, group)
    "plate": ("Core plate, carbon fibre", "#2A2A2C", "painted", "shell"),
    "corner_spacers": ("Corner spacers", "#9CA3AF", "metal", "shell"),
    "spacer_left": ("Rail spacer bar, left", "#A8A8A4", "metal", "shell"),
    "spacer_right": ("Rail spacer bar, right", "#A8A8A4", "metal", "shell"),
    "lip_left": ("Rail lip, left", "#B0B0AC", "metal", "shell"),
    "lip_right": ("Rail lip, right", "#B0B0AC", "metal", "shell"),
    "tape_left": ("Wear tape, left", "#F5F5F0", "painted", "shell"),
    "tape_right": ("Wear tape, right", "#F5F5F0", "painted", "shell"),
    "front_stops": ("Front stops", "#A8A8A4", "metal", "shell"),
    "pin_block": ("Pin blocks", "#0E7490", "painted", "shell"),
    "plunger": ("Locking pins (indexing plungers)", "#C2410C", "painted", "shell"),
    "jam_nut": ("Locking pin jam nuts", "#D1D5DB", "metal", "shell"),
    "shoe": ("Payload shoe", "#7D8A99", "metal", "shell"),
    "lid": ("Lid, printed ASA", "#D9DBDE", "painted", "shell"),
    "gasket": ("Lid gasket", "#1F2937", "rubber", "shell"),
    "grommets": ("Grommets", "#111827", "rubber", "shell"),
    "switch": ("Safety switch", "#BE123C", "painted", "shell"),
    "antennas": ("Antennas", "#1F2937", "rubber", "shell"),
    "mast": ("GNSS mast, carbon tube", "#2B2B2B", "painted", "shell"),
    "gnss": ("GNSS receiver and compass", "#1D4ED8", "painted", "shell"),
    "strain_bar": ("Strain-relief bar, G10", "#65A30D", "painted", "shell"),
    "strain_posts": ("Strain-relief bar posts", "#C0C0C0", "metal", "shell"),
    "pigtail": ("DS-014 pigtail", "#111827", "rubber", "shell"),
    "plug": ("DS-014 plug", "#EAB308", "painted", "shell"),
    "fc_standoffs": ("Standoffs, 25 mm", "#C0C0C0", "metal", "internal"),
    "pdb_standoffs": ("Standoffs, 8 mm", "#C0C0C0", "metal", "internal"),
    "dampers": ("Vibration dampers", "#111827", "rubber", "internal"),
    "fc_plate": ("Damping plate, G10", "#65A30D", "painted", "internal"),
    "fc": ("Flight controller", "#0F766E", "painted", "internal"),
    "pdb": ("Power distribution board", "#16A34A", "painted", "internal"),
    "pmods": ("Power modules", "#7C3AED", "painted", "internal"),
    "radio": ("Telemetry radio", "#2563EB", "painted", "internal"),
    "rc_rx": ("Control link receiver", "#D97706", "painted", "internal"),
}

EXPLODE = {  # by BOM line, mm (as the concept exploded view)
    1: (0, 0, 0), 2: (0, 0, 60), 3: (0, 0, -45), 4: (0, 0, -80), 5: (0, 0, -62), 6: (60, 0, -45), 7: (0, 0, -125),
    8: (0, 0, -175), 9: (-60, 0, -230), 10: (0, 0, 260), 11: (0, 0, 200), 12: (0, 0, 150), 13: (0, 0, 125),
    14: (0, 0, 100), 15: (0, 0, 180), 16: (0, 0, 360), 17: (0, 0, 330), 18: (0, 0, 60), 19: (0, -170, 30),
    21: (-150, 0, 60), 22: (0, 170, 30), 23: (-40, -150, 90), 24: (0, 0, 320), 25: (80, 0, -60), 26: (0, 0, 300),
    27: (-50, 0, 260),
}

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "context"], "explode": False, "el": 26, "az": -40,
     "note": "Product render from the front right and above (about 26 deg elevation): core with the payload shoe "
             "locked in its rail, lid, GNSS mast and antennas; an adult hand on the bench beside it for scale"},
    {"name": "exploded", "groups": ["shell", "internal"], "explode": True, "el": 22, "az": -50,
     "note": "Exploded view from the front right and above (about 22 deg elevation): GNSS, antennas and lid above, "
             "flight controller on its dampers, power board and radios on the plate, rail, pins and shoe below"},
    {"name": "detail", "groups": ["shell"], "explode": False, "el": 32, "az": -35,
     "note": "Detail from below the front right (about 28 deg below): the plain rail, front stops, the two locking "
             "pins with their knobs, the payload shoe and the DS-014 plug hanging through the shoe's notch"},
]


def _hand(az=-40.0, dist=260.0):
    D = derived()
    a = math.radians(az)
    right = (-math.sin(a), math.cos(a))
    ang = math.degrees(math.atan2(-right[1], -right[0]))
    h = Rot(0, 0, ang) * forearm_hand(side="left", pose="flat", include_forearm=False)
    z0 = h.bounding_box().min.Z
    return Pos(dist * right[0], dist * right[1], D["knob_bot"] - z0) * h


def product_parts():
    C = build_components()
    out = []
    for key, shape in C.items():
        name, color, material, group = LOOK[key]
        bom = BOM[key][0]
        out.append({"name": name, "shape": shape, "color": color, "material": material, "bom": bom,
                    "group": group, "explode": tuple(float(v) for v in EXPLODE.get(bom, (0, 0, 0)))})
    out.append({"name": "Adult hand (scale)", "shape": _hand(), "color": "#C8B8A8", "material": "painted",
                "bom": None, "group": "context", "explode": (0.0, 0.0, 0.0)})
    return out


if __name__ == "__main__":
    for p in product_parts():
        print(p["name"], p["group"], p["material"])
