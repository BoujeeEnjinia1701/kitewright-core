"""Kitewright Core prototype build plan pictures (KWC-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/KWC-DWG-101 to 108        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
Uses .kit/build_views.py. Screws and nuts are drawn here for the joint pictures only.
BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from build123d import Cone, Pos  # noqa: E402
from model import PARAMS as P, build_components, derived, deck_context, harness_context, box, cyl, rail_screw_points, flange_screw_points, frame_points  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-03"
D = derived(P)
C = build_components(P)

COL = {"plate": "#3F3F46", "bar": "#65A30D", "spacer": "#57534E", "stop": "#44403C", "lip": "#78716C", "tape": "#E7E5E4",
       "block": "#0E7490", "plunger": "#C2410C", "nut": "#374151", "pdb": "#16A34A", "standoff": "#9CA3AF",
       "damper": "#111827", "fcplate": "#65A30D", "fc": "#0F766E", "radio": "#2563EB", "pmods": "#7C3AED",
       "rx": "#D97706", "pigtail": "#EAB308", "gasket": "#1F2937", "lid": "#E5E7EB", "grommet": "#111827",
       "switch": "#BE123C", "ant": "#4B5563", "mast": "#374151", "gnss": "#1D4ED8", "leads": "#DC2626",
       "as150": "#F59E0B", "corner": "#6B7280", "shoe": "#94A3B8", "deck": "#D6D3D1", "screw": "#1F2937"}


def fuse(*keys):
    s = C[keys[0]]
    for k in keys[1:]:
        s = s + C[k]
    return s


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def made():
    return {
        "plate": part("Core plate", C["plate"], COL["plate"]),
        "spacers": part("Rail spacer bars (2)", fuse("spacer_left", "spacer_right"), COL["spacer"]),
        "stops": part("Front stops (2)", C["front_stops"], COL["stop"]),
        "lips": part("Rail lips (2) with wear tape", fuse("lip_left", "lip_right", "tape_left", "tape_right"), COL["lip"]),
        "blocks": part("Pin blocks (2)", C["pin_block"], COL["block"]),
        "plungers": part("Locking pins (2) and jam nuts", fuse("plunger", "jam_nut"), COL["plunger"]),
        "pdb": part("Power board on 8 mm standoffs", fuse("pdb", "pdb_standoffs"), COL["pdb"]),
        "fcmount": part("25 mm standoffs and dampers (4)", fuse("fc_standoffs", "dampers"), COL["damper"]),
        "fcplate": part("Damping plate", C["fc_plate"], COL["fcplate"]),
        "fc": part("Flight controller", C["fc"], COL["fc"]),
        "modules": part("Radio, power modules, receiver", fuse("radio", "pmods", "rc_rx"), COL["radio"]),
        "pigtail": part("DS-014 pigtail and plug", fuse("pigtail", "plug"), COL["pigtail"]),
        "gasket": part("Lid gasket", C["gasket"], COL["gasket"]),
        "lid": part("Lid with grommets and safety switch", fuse("lid", "grommets", "switch"), COL["lid"]),
        "top": part("Antennas, GNSS mast and receiver", fuse("antennas", "mast", "gnss"), COL["gnss"]),
        "bar": part("Strain-relief bar on two posts", fuse("strain_bar", "strain_posts"), COL["bar"]),
        "corner": part("Corner spacers (4)", C["corner_spacers"], COL["corner"]),
        "shoe": part("Payload shoe", C["shoe"], COL["shoe"]),
    }


ORDER = ["plate", "spacers", "stops", "lips", "blocks", "plungers", "pdb", "fcmount", "fcplate", "fc",
         "modules", "pigtail", "gasket", "lid", "top", "bar", "corner", "shoe"]


# ----------------------------------------------------------------- fasteners drawn for the joint pictures
def m4_csk(x, y, z_bot, length):
    """M4 countersunk screw from below: head flush with the lip's underside at z_bot."""
    head = Pos(x, y, z_bot + 1.1) * Cone(4.0, 2.0, 2.2)
    return head + cyl(x, y, z_bot, z_bot + length, 4.0)


def m4_nut(x, y, z):
    return cyl(x, y, z, z + 5.0, 7.6) - cyl(x, y, z - 1, z + 6, 4.0)


def rail_fixings(points):
    sh = None
    for x, y in points:
        s = m4_csk(x, y, D["lip_z"][0], 16.0) + m4_nut(x, y, 0.0)
        sh = s if sh is None else sh + s
    return sh


def insert(x, y):
    """Bonded flush M3 insert: body through the 4.2 mm hole, flush underneath, 0.8 mm flange on top."""
    return (cyl(x, y, -P["plate"][2], 0.0, 4.2) + cyl(x, y, 0.0, 0.8, 7.0)) - cyl(x, y, -3, 2, 3.0)


def m3_flange_fixing(x, y):
    z0 = D["lid_z"][0]
    head = cyl(x, y, z0 + P["flange"][2], z0 + P["flange"][2] + 3.0, 5.5)
    shank = cyl(x, y, 0.8, z0 + P["flange"][2], 3.0)
    return head + shank, insert(x, y)


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    off = {"plate": (0, 0, 0), "spacers": (0, 0, -60), "stops": (90, 0, -60), "lips": (0, 0, -110),
           "blocks": (-170, 0, -150), "plungers": (-170, 0, -230), "pdb": (0, 0, 60), "bar": (-170, 0, 60),
           "fcmount": (0, 0, 120), "fcplate": (0, 0, 170), "fc": (0, 0, 210), "modules": (60, 0, 90),
           "pigtail": (150, 0, -40), "gasket": (0, 0, 310), "lid": (0, 0, 380), "top": (0, 0, 500),
           "corner": (120, 120, 300), "shoe": (-120, 0, -300)}
    parts = []
    for k in ORDER:
        p = M[k]
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "Kitewright Core prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Seen from the front right and above",
                       elev=20, azim=-55, size=(11, 9), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets():
    M = made()
    base = dict(project="Kitewright Core", date=DATE)
    out = []
    L, W, t = P["plate"]
    fx, fy, fd = P["frame_holes"]
    out.append(bv.component_sheet(
        Part("Core plate", C["plate"], COL["plate"]), [M["lips"], M["lid"], M["spacers"]],
        dwg_no="KWC-DWG-101", title="Kitewright Core plate: making sketch", material="Carbon fibre plate 2 mm, quasi-isotropic",
        notes=[f"Cut {L:.0f} x {W:.0f} mm from 2 mm carbon plate (waterjet or CNC service);",
               "  origin at the centre;",
               "  X is positive toward the front, Y to the left; top face is the datum.",
               f"Frame holes 4.5 mm at {fx:.0f} mm each side of centre, {fy:.0f} mm each side (4).",
               "Rail holes 4.5 mm on lines 70 mm each side: at -93, -75, -30, 30, 90",
               "  mm along X on both lines; stop holes 4.5 mm at 95 mm, 55 mm each side.",
               "Insert holes 4.22 mm (16): lid flange at -60, 0, 60 mm, 50 each",
               "  side; 25 mm standoffs at -75 and 25 mm, 30 each side; 8 mm",
               "  standoffs at -66 and 6 mm, 21 each side; bar posts -95 mm, 28 each side.",
               "Cable slot 12 x 24 mm from 70 to 82 mm along X, on the centre line.",
               "Seal every cut edge with thin epoxy; wear a mask (carbon dust).",
               "Bond M3 flush inserts with structural epoxy, flange on top, body",
               "  flush underneath (the shoe slides 0.3 mm below the plate).",
               "Check: run a straight edge across the underside; nothing proud."],
        inset_view=(-30, -58), **base))
    sb = C["spacer_left"]
    out.append(bv.component_sheet(
        Part("Rail spacer bar", sb, COL["spacer"]), [M["plate"], M["lips"]],
        dwg_no="KWC-DWG-102", title="Kitewright Core rail spacer bar (make 2): making sketch",
        material="Aluminium flat bar 10 x 6 mm, 6061-T6",
        view_shape=Pos(0, -70, -D["spacer_z"][0]) * sb, inset_view=(-30, -58),
        notes=["Make two, the same. Saw 10 x 6 mm bar to 200 mm; square the ends.",
               "Lay it 6 mm side down. Mark a centre line 5 mm from each edge.",
               "Holes 4.5 mm on the centre line at 7, 25, 70, 130 and 190 mm",
               "  from the rear end (X = -93, -75, -30, 30 and 90 mm).",
               "Mill three windows 6 mm wide through the 6 mm height, leaving",
               "  1.5 mm walls: 31.5 to 63.5, 76.5 to 123.5, 136.5 to 183.5 mm",
               "  from the rear end (6.5 mm of web from each hole centre).",
               "Deburr; break every edge lightly. The outer 6 mm face lines up",
               "  with the long edge of the core plate.",
               "Check: lay it under the plate and look through all five holes."],
        **base))
    st = C["front_stops"] & box(80, 110, 30, 80, -20, 5)
    out.append(bv.component_sheet(
        Part("Front stop", st, COL["stop"]), [M["plate"], M["lips"], M["spacers"]],
        dwg_no="KWC-DWG-103", title="Kitewright Core front stop (make 2): making sketch",
        material="Aluminium flat bar 20 x 6 mm, 6061-T6",
        view_shape=Pos(-94, -55, -D["spacer_z"][0]) * st, inset_view=(-30, -58),
        notes=["Make two, the same. Saw 20 x 6 mm bar into 12 mm pieces.",
               "File the cut ends square: the rear face is where the payload",
               "  shoe stops, so it must be flat and square to the 6 mm face.",
               "Drill one 4.5 mm hole 7 mm from the rear face, 5 mm from the",
               "  front end and 10 mm from each side.",
               "Fit: between the plate and the lip, against the spacer bar, at",
               "  the front end of the rail. Its rear face is 12 mm in from the",
               "  rail's front end.",
               "Check: both stops line up across the plate within 0.2 mm."],
        **base))
    lp = C["lip_left"]
    out.append(bv.component_sheet(
        Part("Rail lip", lp, COL["lip"]), [M["plate"], M["spacers"], M["shoe"]],
        dwg_no="KWC-DWG-104", title="Kitewright Core rail lip (make 2, mirror pair): making sketch",
        material="Aluminium flat bar 30 x 3 mm, 6061-T6; UHMW-PE tape 0.7 mm",
        view_shape=Pos(0, -60, -D["lip_z"][0]) * lp, inset_view=(-30, -58),
        notes=["Make a left and a right. Saw 30 x 3 mm bar to 200 mm.",
               "Screw holes 4.5 mm on a line 5 mm from the OUTER edge, at 7, 25,",
               "  70, 130 and 190 mm from the rear end; stop hole 4.5 mm at 195",
               "  mm, 20 mm from the outer edge.",
               "Pin hole 5.5 mm at 16 mm from the rear end, 20 mm from the outer",
               "  edge. Countersink the screw holes 90 deg from the UNDERSIDE so",
               "  the M4 heads sit flush; the left and right lips are mirror images.",
               "Underside pockets 2 mm deep, 1.5 to 18.5 mm from the INNER edge,",
               "  at the same X as the spacer windows (1 mm skin left).",
               "Stick 0.7 mm UHMW tape on the top face from the inner edge to 1 mm",
               "  short of the spacer, rear end to the stop; cut out the pin hole.",
               "Check: a 5 mm shoe offcut slides between lip and plate with",
               "  a 0.2 to 0.4 mm feeler gap once assembled."],
        **base))
    blk = C["pin_block"] & box(-120, -60, -80, -40, -40, 0)
    out.append(bv.component_sheet(
        Part("Pin block", blk, COL["block"]), [M["lips"], M["plungers"], M["plate"]],
        dwg_no="KWC-DWG-105", title="Kitewright Core pin block (make 2): making sketch",
        material="Aluminium bar 30 x 15 mm, 6061-T6",
        view_shape=Pos(84, 60, -D["block_z"][0]) * blk, inset_view=(-30, -58),
        notes=["Make two, the same. Saw 30 x 15 mm bar to 28 mm long.",
               "Plunger hole: centre 14 mm from each end, 20 mm from the OUTER",
               "  face; drill 9.0 mm through, square to the 28 x 30 face, and tap",
               "  M10 x 1 (fine thread) all the way.",
               "Two screw holes 4.5 mm, 5 mm from the outer face, at 5 mm and",
               "  23 mm from the rear end.",
               "Fit: under the lip at the rear of the rail, outer face flush with",
               "  the plate edge; two M4 x 35 cap screws through block, lip,",
               "  spacer and plate, nylon-insert nuts on top.",
               "Check: the plunger screws in by hand; its pin comes up through",
               "  the lip hole without touching the sides."],
        **base))
    out.append(bv.component_sheet(
        Part("Payload shoe", C["shoe"], COL["shoe"]), [M["lips"], M["plate"], M["stops"]],
        dwg_no="KWC-DWG-106", title="Kitewright Core payload shoe: making sketch",
        material="Aluminium plate 5 mm, 6061-T6",
        view_shape=Pos(0, 0, -D["shoe_z"][0]) * C["shoe"], inset_view=(-30, -58),
        notes=["One per payload. Blank 184 x 128 mm from 5 mm plate; ends and",
               "  long edges square and straight (they run in the rail).",
               "Cable notch in the front edge: 18 mm deep, 28 mm wide, centred.",
               "Pin holes 5.5 mm: 12 mm from the rear edge, 9 mm in from each",
               "  long edge (55 mm each side of the centre line).",
               "Payload holes: four 4.5 mm, countersunk on the TOP face for M4,",
               "  at 26 and 146 mm from the rear edge, 30 mm each side of centre.",
               "Chamfer the rear corners 2 mm so the shoe finds the rail.",
               "Check: slides the full rail length without binding; both pins",
               "  drop into their holes at the front stops."],
        **base))
    out.append(bv.component_sheet(
        Part("Lid", C["lid"], COL["lid"]), [M["plate"], M["gasket"], M["top"]],
        dwg_no="KWC-DWG-107", title="Kitewright Core lid: making sketch",
        material="3D printed ASA, light grey, 0.2 mm layers, 4 walls, 25 % infill",
        notes=["Print open side down on the flange; no supports except the two",
               "  rear grommet holes and the service opening (bridges).",
               "Outside 168 x 92 x 62 mm, 1.5 mm walls and top; flange 180 x 108 x",
               "  3 mm with six 3.4 mm holes, 50 mm each side, at -60, 0, 60 mm.",
               "Top: mast boss 22 mm across, 14 mm tall, 10.2 mm socket 12 mm",
               "  deep, at 55 mm behind centre; heat-set M3 insert in its side",
               "  for the thumbscrew; 6 mm GNSS cable hole beside it.",
               "Top: three 6.5 mm SMA holes and a 12.2 mm safety switch hole.",
               "Rear wall: two 20 mm grommet holes, 13 mm each side, 17 mm up;",
               "  12 x 7 mm service opening for the USB-C lead.",
               "Check: lid sits flat on the plate on its gasket with no rock."],
        **base))
    out.append(bv.component_sheet(
        Part("Damping plate", C["fc_plate"], COL["fcplate"]), [M["fcmount"], M["fc"], M["plate"]],
        dwg_no="KWC-DWG-108", title="Kitewright Core damping plate: making sketch",
        material="G10 / FR4 glass-epoxy sheet 2 mm",
        view_shape=Pos(25, 0, -D["fc_plate_z"]) * C["fc_plate"],
        notes=["Cut 110 x 70 mm from 2 mm G10 with a fine-tooth saw; wear a mask",
               "  (glass dust) and file the edges smooth.",
               "Damper holes 3.4 mm at 5 mm in from each end, 5 mm in from each",
               "  long edge (100 x 60 mm pattern).",
               "Flight controller holes: mark from the controller's own mounting",
               "  pattern, centred on the plate, and drill 3.2 mm.",
               "The controller is fixed with M3 nylon screws and its arrow points",
               "  forward (+X, toward the cable slot).",
               "Check: the plate hangs level on the four dampers and nothing",
               "  touches it except the dampers."],
        **base))
    return out


# ----------------------------------------------------------------- joints
def window(keys_cols, region):
    out = []
    for name, shape, col in keys_cols:
        s = shape & region
        out.append(part(name, s, col))
    return out


def joints():
    out = []
    # 1 rail cross-section through a screw at X = 30 (left rail)
    reg = box(-20, 30, 30, 80, -16, 8)
    fix = rail_fixings([(30.0, 70.0), (-30.0, 70.0)])
    out.append(bv.joint(window([("Core plate", C["plate"], COL["plate"]), ("Spacer bar", C["spacer_left"], COL["spacer"]),
                                ("Lip", C["lip_left"], COL["lip"]), ("Wear tape", C["tape_left"], COL["tape"]),
                                ("Payload shoe (edge)", C["shoe"], COL["shoe"]),
                                ("M4 countersunk screw and nylon-insert nut", fix, COL["screw"])], reg),
                        OUT / "joint-01.png", "Joint 1: the plain rail, cut across at a screw",
                        subtitle="Shoe edge runs between plate and taped lip: 0.3 mm gap above, 1 mm at the side",
                        elev=12, azim=-35))
    # 2 locking pin, cut through its axis (right rail, rear)
    px, py = P["pin_xy"]
    reg = box(-125, px, -80, -28, -55, 6)
    fix = cyl(-93, -70, D["block_z"][0] - 4, 0, 4.0) + cyl(-93, -70, D["block_z"][0] - 4, D["block_z"][0], 7.0) + m4_nut(-93, -70, 0.0)
    out.append(bv.joint(window([("Core plate", C["plate"], COL["plate"]), ("Spacer bar", C["spacer_right"], COL["spacer"]),
                                ("Lip", C["lip_right"], COL["lip"]), ("Payload shoe", C["shoe"], COL["shoe"]),
                                ("Pin block", C["pin_block"], COL["block"]), ("Locking pin (indexing plunger)", C["plunger"], COL["plunger"]),
                                ("Jam nut", C["jam_nut"], COL["nut"]), ("M4 x 35 cap screw and nut", fix, COL["screw"])], reg),
                        OUT / "joint-02.png", "Joint 2: a locking pin, cut through its axis",
                        subtitle="Pin passes up through the lip into the shoe; pull the knob down and twist to hold it out",
                        elev=10, azim=-30))
    # 3 front stop, sandwiched between plate and lip, cut through its screw
    reg = box(70, 95, 30, 80, -16, 8)
    sx, sy = P["stop_screw"]
    fix = rail_fixings([(sx, sy)])
    out.append(bv.joint(window([("Core plate", C["plate"], COL["plate"]), ("Spacer bar", C["spacer_left"], COL["spacer"]),
                                ("Front stop", C["front_stops"], COL["stop"]), ("Lip", C["lip_left"], COL["lip"]),
                                ("Payload shoe (front edge)", C["shoe"], COL["shoe"]), ("M4 screw and nut", fix, COL["screw"])], reg),
                        OUT / "joint-03.png", "Joint 3: a front stop, cut through its screw",
                        subtitle="The shoe's front edge stops against it; both pins then line up with their holes",
                        elev=14, azim=-40))
    # 4 DS-014 pigtail through the plate slot and the shoe notch, cut on the centre line
    reg = box(40, 100, 0, 40, -40, 14)
    out.append(bv.joint(window([("Core plate", C["plate"], COL["plate"]), ("Payload shoe (notch)", C["shoe"], COL["shoe"]),
                                ("DS-014 pigtail and clamp", C["pigtail"], COL["pigtail"]), ("DS-014 plug", C["plug"], COL["pigtail"])], reg),
                        OUT / "joint-04.png", "Joint 4: the DS-014 pigtail, cut on the centre line",
                        subtitle="Cable drops through the 12 x 24 mm slot and the shoe's notch; plug hangs in front of the payload",
                        elev=14, azim=-60))
    # 5 flight controller damping, cut through a damper
    reg = box(-95, -55, 30, 50, -4, 60)
    fix = cyl(-75, 30, D["fc_plate_z"], D["fc_plate_z"] + P["fc_plate"][2] + 3, 3.0) + cyl(-75, 30, D["fc_plate_z"] + P["fc_plate"][2], D["fc_plate_z"] + P["fc_plate"][2] + 3, 5.5)
    clinch = insert(-75, 30)
    out.append(bv.joint(window([("Core plate", C["plate"], COL["plate"]), ("M3 bonded flush insert", clinch, COL["screw"]),
                                ("25 mm standoff", C["fc_standoffs"], COL["standoff"]), ("Silicone damper", C["dampers"], COL["damper"]),
                                ("Damping plate", C["fc_plate"], COL["fcplate"]), ("Flight controller", C["fc"], COL["fc"]),
                                ("M3 screw in the damper", fix, COL["screw"])], reg),
                        OUT / "joint-05.png", "Joint 5: flight controller damping, cut through a damper",
                        subtitle="Standoff screws into the bonded flush insert; the plate floats on four silicone dampers",
                        elev=12, azim=-62))
    # 6 lid flange to plate
    scr, cl = m3_flange_fixing(-60.0, 50.0)
    reg = box(-80, -60, 30, 62, -4, 18)
    out.append(bv.joint(window([("Core plate", C["plate"], COL["plate"]), ("M3 bonded insert (flush below)", cl, COL["screw"]),
                                ("Gasket", C["gasket"], COL["gasket"]), ("Lid flange and wall", C["lid"], COL["lid"]),
                                ("M3 cap screw", scr, COL["screw"])], reg),
                        OUT / "joint-06.png", "Joint 6: lid flange to plate, cut through a screw",
                        subtitle="Six M3 screws into bonded inserts; the 1 mm foam gasket seals the flange", elev=14, azim=-35))
    # 7 core to frame deck (the deck belongs to the frame repos)
    fx, fy, _ = P["frame_holes"]
    reg = box(92, fx, 45, 75, -14, 18)
    bolt = cyl(fx, fy, -P["plate"][2] - 5, D["deck_z"] + P["deck"][2] + 3, 4.0) + cyl(fx, fy, D["deck_z"] + P["deck"][2], D["deck_z"] + P["deck"][2] + 3, 7.0) \
        + m4_nut(fx, fy, -P["plate"][2] - 5)
    out.append(bv.joint(window([("Core plate", C["plate"], COL["plate"]), ("Corner spacer 16 x 8 mm", C["corner_spacers"], COL["corner"]),
                                ("Frame deck (Lift or Range)", deck_context(P), COL["deck"]), ("M4 bolt, nut below the plate", bolt, COL["screw"]),
                                ("Rail lip", C["lip_left"], COL["lip"])], reg),
                        OUT / "joint-07.png", "Joint 7: core to frame deck at a corner, cut through the bolt",
                        subtitle="The core hangs under the deck on four M4 bolts; the lid rises through the deck opening",
                        elev=14, azim=-35))
    return out


# ----------------------------------------------------------------- steps
def steps():
    M = made()
    done = []
    out = []

    def go(n, new, title, sub, explode, **kw):
        for p, e in zip(new, explode):
            p.explode = e
        kw.setdefault("label_done", n <= 2)   # later steps: only the new parts are labelled; fitted parts are grey
        out.append(bv.step(list(done), new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))
        done.extend(part(p.name, p.shape, p.color) for p in new)

    below = dict(elev=-28, azim=-50)
    done.append(M["plate"])
    go(1, [M["spacers"], M["stops"], M["lips"]], "rails onto the core plate (from below)",
       "Spacer bars, front stops, then taped lips; ten M4 countersunk screws up through all three, nuts on top",
       [(0, 0, -50), (0, 0, -50), (0, 0, -100)], **below)
    go(2, [M["blocks"], M["plungers"]], "pin blocks and locking pins",
       "Blocks under the lips at the rear, M4 x 35 screws; screw each plunger in until its pin is 0.5 mm short of the plate",
       [(0, 0, -60), (0, 0, -140)], **below)
    go(3, [M["pdb"]], "power board",
       "8 mm standoffs into the bonded inserts; the four power pads stay bare for the frame harness leads",
       [(0, 0, 60)], elev=30, azim=-50)
    go(4, [M["fcmount"], M["fcplate"], M["fc"]], "flight controller on its dampers",
       "25 mm standoffs, dampers, damping plate; controller on M3 nylon screws, arrow forward",
       [(0, 0, 60), (0, 0, 100), (0, 0, 140)], elev=30, azim=-50)
    go(5, [M["modules"]], "radio, power modules and receiver",
       "Foam-taped to the plate in front of the controller; plug the harness", [(0, 0, 70)], elev=30, azim=-50)
    go(6, [M["pigtail"]], "DS-014 pigtail",
       "Cable down through the slot, clamped to the plate; plug left hanging below", [(0, 0, 80)], elev=30, azim=-50)
    go(7, [M["gasket"], M["lid"]], "gasket and lid",
       "Lower the lid onto the gasket, six M3 screws", [(0, 0, 80), (0, 0, 160)], elev=30, azim=-50)
    go(8, [M["top"]], "antennas, GNSS mast and receiver",
       "SMA bulkheads through the lid top; mast into its socket, thumbscrew", [(0, 0, 120)], elev=24, azim=-50)
    harness = part("Frame harness leads (Lift or Range, not in this repo)", harness_context(P), COL["leads"])
    go(9, [M["bar"]], "strain-relief bar; frame harness leads",
       "Two posts and a G10 bar behind the lid; the frame's own four leads are soldered to the pads and tied to it",
       [(-80, 0, 40)], context=[harness], elev=24, azim=-50)
    go(10, [M["shoe"]], "payload shoe in from the rear (payload swap)",
       "Pull and twist both pins out, slide to the front stops, twist back: both pins snap in, no red showing",
       [(-260, 0, 0)], elev=-22, azim=-40)
    deck = part("Frame deck (Lift or Range, not in this repo)", deck_context(P), COL["deck"])
    go(11, [M["corner"]], "into the frame",
       "Corner spacers on the plate, lid up through the deck opening; four M4 bolts down through deck, spacers and plate",
       [(160, -120, 0)], context=[deck], elev=26, azim=-50)
    return out


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "joints", "steps"]
    for w in what:
        r = {"overview": overview, "sheets": sheets, "joints": joints, "steps": steps}[w]()
        print(w, "done")
