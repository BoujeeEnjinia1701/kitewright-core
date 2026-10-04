"""Kitewright Core parametric model (build123d), constructable design (KWC-DDR-002).

Run from the repo root:
    python cad/src/model.py            export STEP and STL to cad/step and cad/stl
    python cad/src/model.py --check    run the constructability checks only

Coordinates in mm. X points forward along the payload rail (the payload slides in from the rear,
-X, toward the front stops), Y to the left, Z up. Z = 0 is the top face of the core plate; the
frame's lower deck sits on four 8 mm corner spacers, so its underside is at Z = 8. Everything in
the avionics stack sits on the plate under the printed lid; the plain rail, the front stops and the
locking pin hang under the plate. Every main dimension used by the drawings, the calculations,
the build plan pictures and the appearance model comes from PARAMS and derived() here.
CONCEPT, NOT FOR FABRICATION until the build plan's first checks are done.
"""
from __future__ import annotations

import sys
from pathlib import Path

from build123d import Box, Cylinder, Pos, Rot, Compound, export_step, export_stl

ROOT = Path(__file__).resolve().parents[2]

PARAMS = {
    # core plate, 2 mm carbon fibre plate (KWC-DDR-003, O1 option B; was 2 mm 5052-H32 aluminium)
    "plate": (240.0, 150.0, 2.0),            # length (X), width (Y), thickness
    "frame_holes": (110.0, 65.0, 4.5),        # +/-X, +/-Y, diameter: the 220 x 130 mm frame pattern, M4
    "corner_spacer": (16.0, 4.5, 8.0),        # OD, bore, height
    "deck_opening": (200.0, 112.0),           # opening the frame leaves in its lower deck
    # plain rail (two sides, mirror images)
    "rail_x": (-100.0, 100.0),
    "spacer_bar": (10.0, 6.0),                # width (Y), height (Z); outer edge on the plate edge
    "lip": (30.0, 3.0),                       # width (Y), thickness
    # pockets milled in the rail bars (KWC-DDR-003, O1 option B): spacer bar windows through the
    #   height, walls each side; lip pockets from the underside inboard of the spacer; web kept
    #   round every screw hole (from the hole centre)
    "spacer_window_wall": 1.5, "lip_pocket": (2.0, 46.5, 63.5), "pocket_web": 6.5,
    "tape": 0.7,                              # UHMW-PE wear tape on the lip top face
    "shoe": (184.0, 128.0, 5.0),              # payload shoe length, width, thickness (6061 plate)
    "shoe_rear_x": -96.0,                     # rear edge of the shoe when locked home
    "notch": (18.0, 28.0),                    # cable notch in the shoe's front edge: depth (X), width (Y)
    "slot": (70.0, 82.0, 24.0),               # cable slot in the plate: x from, x to, width
    "front_stop": (12.0, 19.0),               # length (X), width (Y)
    "pin_xy": (-84.0, -55.0),                 # locking pin axis
    "pin_d": 5.0, "pin_hole": 5.5,
    "pin_block": (28.0, 30.0, 15.0),          # X, Y, Z, under the right lip
    "plunger_thread": 10.0,                   # M10 x 1 indexing plunger body
    "knob_d": 18.0,
    "rail_screws_left": (-30.0, 30.0, 90.0),
    "rail_screws_right": (-30.0, 30.0, 90.0),
    "block_screws_x": (-93.0, -75.0),
    "stop_screw": (95.0, 55.0),
    "screw_y": 70.0,
    "shoe_holes": ((-70.0, 30.0), (-70.0, -30.0), (50.0, 30.0), (50.0, -30.0)),
    # lid (printed ASA)
    "lid": (168.0, 92.0, 62.0, 1.5),          # outer length, width, height, wall (1.5 mm, KWC-DDR-003; was 2 mm)
    "flange": (180.0, 108.0, 3.0),
    "gasket": 1.0,
    "flange_screws_x": (-60.0, 0.0, 60.0), "flange_screws_y": 50.0,
    "grommet": (20.0, 13.0, 18.0),            # hole diameter, +/-Y, Z of the two rear grommets
    "mast_xy": (-55.0, 0.0), "mast_boss": (22.0, 14.0), "mast_tube": (10.0, 150.0),
    "gnss": (50.0, 16.0),
    "ant_xy": ((65.0, 32.0), (65.0, -32.0)), "ant": (10.0, 110.0), "rc_ant_xy": (40.0, 0.0), "rc_ant": (8.0, 80.0),
    "sma": (9.0, 8.0),
    "switch_xy": (-15.0, 30.0),
    # avionics stack
    "fc": (102.0, 53.0, 17.0), "fc_c": (-25.0, 0.0),
    "fc_plate": (110.0, 70.0, 2.0),
    "fc_standoffs": ((-75.0, 30.0), (-75.0, -30.0), (25.0, 30.0), (25.0, -30.0)), "fc_standoff_h": 25.0,
    "damper": (10.0, 10.0),
    "pdb": (80.0, 50.0, 1.6), "pdb_x": (-70.0, 10.0), "pdb_standoff_h": 8.0,
    "pdb_block": (60.0, 34.0, 12.0),
    "pdb_standoffs": ((-66.0, 21.0), (-66.0, -21.0), (6.0, 21.0), (6.0, -21.0)),
    "radio": (29.0, 81.0, 14.0, 43.0, 13.0),         # x0, x1, y0, y1, height
    "pmods": (30.0, 80.0, -43.0, -17.0, 12.0),
    "rc_rx": (-2.0, 20.0, -43.0, -30.0, 6.0),
    # frame harness leads (owned by Lift and Range since KWC-DDR-003; drawn here as context only)
    "leads_y": (-17.0, -9.0, 9.0, 17.0), "lead_d": 8.0, "lead_z": 18.0, "lead_out": 70.0,
    # strain-relief bar for the frame harness leads, outside the lid flange at the rear: G10 strip
    #   (X, Y, Z) on two 11 mm posts; x centre; post y
    "strain_bar": (6.0, 64.0, 3.0), "strain_x": -95.0, "strain_post_y": 28.0, "strain_post": (5.5, 11.0),
    "pigtail_d": 7.0, "plug": (40.0, 14.0, 16.0), "plug_x": 79.0,
    # context only (the frame repos own these)
    "deck": (300.0, 200.0, 3.0),
}

# Mass densities, g/cm3
RHO = {"al": 2.70, "asa": 1.07, "g10": 1.85, "steel": 7.9, "uhmw": 0.94, "cfrp": 1.55}


def strain_post_points(P=PARAMS):
    return [(P["strain_x"], s * P["strain_post_y"]) for s in (1, -1)]


def _rail_pockets_x(P=PARAMS):
    """X ranges between the screw holes of one rail, keeping the web round each hole."""
    xs = sorted(set(list(P["rail_screws_left"]) + list(P["block_screws_x"])))
    x0, x1 = P["rail_x"]
    w = P["pocket_web"]
    edges = [x0 - w + 4.0] + xs + [x1 + w - 4.0]
    out = []
    for a, b in zip(edges, edges[1:]):
        lo, hi = a + w, b - w
        if hi - lo >= 8.0:
            out.append((lo, hi))
    return out


def derived(P=PARAMS):
    L, W, t = P["plate"]
    sw, sh = P["spacer_bar"]
    lw, lt = P["lip"]
    D = {}
    D["plate_bot"] = -t
    D["spacer_z"] = (-t - sh, -t)
    D["lip_z"] = (-t - sh - lt, -t - sh)
    D["tape_z"] = (D["lip_z"][1], D["lip_z"][1] + P["tape"])
    D["shoe_z"] = (D["tape_z"][1], D["tape_z"][1] + P["shoe"][2])
    D["shoe_gap"] = D["plate_bot"] - D["shoe_z"][1]
    D["spacer_y"] = (W / 2 - sw, W / 2)
    D["lip_y"] = (W / 2 - lw, W / 2)
    D["shoe_x"] = (P["shoe_rear_x"], P["shoe_rear_x"] + P["shoe"][0])
    D["side_gap"] = D["spacer_y"][0] - P["shoe"][1] / 2
    D["overlap"] = P["shoe"][1] / 2 - D["lip_y"][0]
    D["neck_halfwidth"] = D["lip_y"][0]
    D["block_z"] = (D["lip_z"][0] - P["pin_block"][2], D["lip_z"][0])
    D["lid_z"] = (P["gasket"], P["gasket"] + P["lid"][2])
    D["deck_z"] = P["corner_spacer"][2]
    D["mast_top"] = D["lid_z"][1] + P["mast_boss"][1] - 12.0 + P["mast_tube"][1]
    D["gnss_top"] = D["mast_top"] + P["gnss"][1]
    D["knob_bot"] = D["block_z"][0] - 6.0 - 4.0 - 14.0
    D["overall_h"] = D["gnss_top"] - D["knob_bot"]
    D["fc_plate_z"] = P["fc_standoff_h"] + P["damper"][1]
    D["fc_z"] = (D["fc_plate_z"] + P["fc_plate"][2], D["fc_plate_z"] + P["fc_plate"][2] + P["fc"][2])
    D["lid_inner_top"] = D["lid_z"][1] - P["lid"][3]
    D["fc_headroom"] = D["lid_inner_top"] - D["fc_z"][1]
    D["pin_tip"] = D["shoe_z"][1] - 0.5
    D["pin_engage"] = D["pin_tip"] - D["shoe_z"][0]
    return D


def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def cyl(x, y, z0, z1, d):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(d / 2, z1 - z0)


def xcyl(y, z, x0, x1, d):
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(d / 2, x1 - x0)


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def _holes(shape, pts, z0, z1, d):
    for x, y in pts:
        shape = shape - cyl(x, y, z0 - 1, z1 + 1, d)
    return shape


def rail_screw_points(P=PARAMS):
    y = P["screw_y"]
    pts = [(x, y) for x in P["rail_screws_left"]] + [(x, -y) for x in P["rail_screws_right"]]
    pts += [(x, s * y) for x in P["block_screws_x"] for s in (1, -1)]
    sx, sy = P["stop_screw"]
    pts += [(sx, sy), (sx, -sy)]
    return pts


def flange_screw_points(P=PARAMS):
    return [(x, s * P["flange_screws_y"]) for x in P["flange_screws_x"] for s in (1, -1)]


def frame_points(P=PARAMS):
    fx, fy, _ = P["frame_holes"]
    return [(sx * fx, sy * fy) for sx in (1, -1) for sy in (1, -1)]


# ------------------------------------------------------------------ components
def build_components(P=PARAMS):
    """Every component of the constructable core, as build123d solids keyed by a short name."""
    D = derived(P)
    L, W, t = P["plate"]
    C = {}
    x0, x1 = P["rail_x"]

    # 1 core plate
    plate = box(-L / 2, L / 2, -W / 2, W / 2, -t, 0)
    fd = P["frame_holes"][2]
    plate = _holes(plate, frame_points(P), -t, 0, fd)
    plate = _holes(plate, rail_screw_points(P), -t, 0, 4.5)
    plate = _holes(plate, flange_screw_points(P) + list(P["fc_standoffs"]) + list(P["pdb_standoffs"]) + strain_post_points(P), -t, 0, 4.22)
    sx0, sx1, sw_ = P["slot"]
    plate = plate - box(sx0, sx1, -sw_ / 2, sw_ / 2, -t - 1, 1)
    C["plate"] = plate

    # 2 corner spacers (bought), between plate and frame deck
    od, bore, h = P["corner_spacer"]
    C["corner_spacers"] = _fuse([cyl(x, y, 0, h, od) - cyl(x, y, -1, h + 1, bore) for x, y in frame_points(P)])

    # 3 spacer bars and 4 lips (left +Y, right -Y)
    sy0, sy1 = D["spacer_y"]
    ly0, ly1 = D["lip_y"]
    sz0, sz1 = D["spacer_z"]
    lz0, lz1 = D["lip_z"]
    ys = P["screw_y"]
    for side, s in (("left", 1), ("right", -1)):
        bar = box(x0, x1, min(s * sy0, s * sy1), max(s * sy0, s * sy1), sz0, sz1)
        lip = box(x0, x1, min(s * ly0, s * ly1), max(s * ly0, s * ly1), lz0, lz1)
        pts = [p for p in rail_screw_points(P) if p[1] * s > 0]
        bar = _holes(bar, [p for p in pts if abs(p[1]) == ys], sz0, sz1, 4.5)
        lip = _holes(lip, pts, lz0, lz1, 4.5)
        ww = P["spacer_window_wall"]
        pd_, py0_, py1_ = P["lip_pocket"]
        for wx0, wx1 in _rail_pockets_x(P):
            bar = bar - box(wx0, wx1, min(s * (sy0 + ww), s * (sy1 - ww)), max(s * (sy0 + ww), s * (sy1 - ww)), sz0 - 1, sz1 + 1)
            if wx1 < P["pin_xy"][0] - 8 or wx0 > P["pin_xy"][0] + 8:
                lip = lip - box(wx0, wx1, min(s * py0_, s * py1_), max(s * py0_, s * py1_), lz0 - 1, lz0 + pd_)
        lip = lip - cyl(P["pin_xy"][0], s * abs(P["pin_xy"][1]), lz0 - 1, lz1 + 1, P["pin_hole"])
        C[f"spacer_{side}"] = bar
        C[f"lip_{side}"] = lip
        tape = box(x0, P["shoe_rear_x"] + P["shoe"][0], min(s * ly0, s * (P["shoe"][1] / 2 + 0.5)),
                   max(s * ly0, s * (P["shoe"][1] / 2 + 0.5)), D["tape_z"][0], D["tape_z"][1])
        tape = tape - cyl(P["pin_xy"][0], s * abs(P["pin_xy"][1]), lz0, lz1 + 5, P["pin_hole"])
        C[f"tape_{side}"] = tape

    # 5 front stops, between plate and lip, clamped by the stop screws
    fl, fw = P["front_stop"]
    sx, ssy = P["stop_screw"]
    stops = []
    for s in (1, -1):
        st = box(x1 - fl, x1, min(s * ly0, s * sy0), max(s * ly0, s * sy0), lz1, sz1)
        st = st - cyl(sx, s * ssy, lz1 - 1, sz1 + 1, 4.5)
        stops.append(st)
    C["front_stops"] = _fuse(stops)

    # 6 pin blocks under both lips, each with the M10 x 1 threaded bore for its plunger
    #   (two independent locking pins, KWC-DDR-002: either pin alone holds the payload)
    bx, by, bz = P["pin_block"]
    px, py0 = P["pin_xy"]
    bz0, bz1 = D["block_z"]
    blocks, bodies, nuts = [], [], []
    for s in (1, -1):
        py = s * abs(py0)
        yb0, yb1 = sorted((s * W / 2, s * (W / 2 - by)))
        blk = box(px - bx / 2, px + bx / 2, yb0, yb1, bz0, bz1)
        blk = blk - cyl(px, py, bz0 - 1, bz1 + 1, P["plunger_thread"])
        blk = _holes(blk, [(x, s * ys) for x in P["block_screws_x"]], bz0, bz1, 4.5)
        blocks.append(blk)
        # indexing plunger (bought): threaded body in the block, jam nut, knob, pin engaged in the shoe
        body = cyl(px, py, bz0, bz1, P["plunger_thread"])
        shaft = cyl(px, py, bz0 - 10, bz0 - 6, 6.0)
        knob = cyl(px, py, bz0 - 24, bz0 - 10, P["knob_d"])
        pin = cyl(px, py, bz1, D["pin_tip"], P["pin_d"])
        bodies.append(_fuse([body, shaft, knob, pin]))
        nuts.append(cyl(px, py, bz0 - 6, bz0, 17.0) - cyl(px, py, bz0 - 7, bz0 + 1, P["plunger_thread"]))
    C["pin_block"] = _fuse(blocks)
    C["plunger"] = _fuse(bodies)
    C["jam_nut"] = _fuse(nuts)

    # 8 payload shoe (one per payload; the core kit carries one)
    sL, sW, sT = P["shoe"]
    shx0, shx1 = D["shoe_x"]
    shoe = box(shx0, shx1, -sW / 2, sW / 2, D["shoe_z"][0], D["shoe_z"][1])
    nd, nw = P["notch"]
    shoe = shoe - box(shx1 - nd, shx1 + 1, -nw / 2, nw / 2, D["shoe_z"][0] - 1, D["shoe_z"][1] + 1)
    for s_ in (1, -1):
        shoe = shoe - cyl(px, s_ * abs(py0), D["shoe_z"][0] - 1, D["shoe_z"][1] + 1, P["pin_hole"])
    shoe = _holes(shoe, P["shoe_holes"], D["shoe_z"][0], D["shoe_z"][1], 4.5)
    C["shoe"] = shoe

    # 9 lid (printed) with flange, mast boss, and gasket under the flange
    lL, lW, lH, wall = P["lid"]
    fL, fW, fT = P["flange"]
    g = P["gasket"]
    lz0 = g
    outer = box(-lL / 2, lL / 2, -lW / 2, lW / 2, lz0, lz0 + lH)
    inner = box(-lL / 2 + wall, lL / 2 - wall, -lW / 2 + wall, lW / 2 - wall, lz0 - 1, lz0 + lH - wall)
    flange = box(-fL / 2, fL / 2, -fW / 2, fW / 2, lz0, lz0 + fT) - box(-lL / 2 + wall, lL / 2 - wall, -lW / 2 + wall, lW / 2 - wall, lz0 - 1, lz0 + fT + 1)
    mx, my = P["mast_xy"]
    bd, bh = P["mast_boss"]
    boss = cyl(mx, my, lz0 + lH, lz0 + lH + bh, bd)
    lid = outer - inner + flange + boss
    lid = lid - cyl(mx, my, lz0 + lH + bh - 12, lz0 + lH + bh + 1, P["mast_tube"][0] + 0.2)
    lid = _holes(lid, flange_screw_points(P), lz0, lz0 + fT, 3.4)
    for (ax, ay) in list(P["ant_xy"]) + [P["rc_ant_xy"]]:
        lid = lid - cyl(ax, ay, lz0 + lH - wall - 1, lz0 + lH + 1, 6.5)
    lid = lid - cyl(*P["switch_xy"], lz0 + lH - wall - 1, lz0 + lH + 1, 12.2)
    gd, gy, gz = P["grommet"]
    for s in (1, -1):
        lid = lid - xcyl(s * gy, gz, -lL / 2 - 1, -lL / 2 + wall + 1, gd)
    lid = lid - box(-lL / 2 - 1, -lL / 2 + wall + 1, -6, 6, 42.5, 49.5)        # USB-C service opening
    lid = lid - cyl(mx + 14, 0, lz0 + lH - wall - 1, lz0 + lH + 1, 6.0)          # GNSS cable hole
    C["lid"] = lid
    C["gasket"] = (box(-fL / 2, fL / 2, -fW / 2, fW / 2, 0, g)
                   - box(-lL / 2 + wall, lL / 2 - wall, -lW / 2 + wall, lW / 2 - wall, -1, g + 1))
    C["gasket"] = _holes(C["gasket"], flange_screw_points(P), 0, g, 6.0)

    # 10 rear grommets and the power leads with their AS150 plugs
    gro = []
    for s in (1, -1):
        r = xcyl(s * gy, gz, -lL / 2 - 3, -lL / 2 + wall + 3, gd + 6) - xcyl(s * gy, gz, -lL / 2 - 4, -lL / 2 + wall + 4, gd - 4)
        r = r - box(-lL / 2 + 0.0, -lL / 2 + wall, -lW, lW, 0, 80)               # groove that takes the wall
        gro.append(r)
    C["grommets"] = _fuse(gro)
    # the leads belong to each frame's harness (KWC-DDR-003); only the strain-relief bar is core
    bl, bw, bt = P["strain_bar"]
    pd, ph = P["strain_post"]
    sxp = P["strain_x"]
    bar = box(sxp - bl / 2, sxp + bl / 2, -bw / 2, bw / 2, ph, ph + bt)
    bar = _holes(bar, strain_post_points(P), ph, ph + bt, 3.4)
    C["strain_bar"] = bar
    C["strain_posts"] = _fuse([cyl(x, y, 0, ph, pd) for x, y in strain_post_points(P)])

    # 11 FC standoffs, dampers, damping plate, flight controller
    C["fc_standoffs"] = _fuse([cyl(x, y, 0, P["fc_standoff_h"], 5.5) for x, y in P["fc_standoffs"]])
    dd, dh = P["damper"]
    C["dampers"] = _fuse([cyl(x, y, P["fc_standoff_h"], P["fc_standoff_h"] + dh, dd) for x, y in P["fc_standoffs"]])
    fpl, fpw, fpt = P["fc_plate"]
    cx, cy = P["fc_c"]
    fz = D["fc_plate_z"]
    fcp = box(cx - fpl / 2, cx + fpl / 2, cy - fpw / 2, cy + fpw / 2, fz, fz + fpt)
    C["fc_plate"] = _holes(fcp, P["fc_standoffs"], fz, fz + fpt, 3.4)
    fl_, fw_, fh_ = P["fc"]
    C["fc"] = box(cx - fl_ / 2, cx + fl_ / 2, cy - fw_ / 2, cy + fw_ / 2, D["fc_z"][0], D["fc_z"][1])

    # 12 power distribution board on short standoffs
    ph = P["pdb_standoff_h"]
    pl, pw, pt = P["pdb"]
    px0, px1 = P["pdb_x"]
    C["pdb_standoffs"] = _fuse([cyl(x, y, 0, ph, 5.5) for x, y in P["pdb_standoffs"]])
    pbl, pbw, pbh = P["pdb_block"]
    pcx = (px0 + px1) / 2
    pdb = box(px0, px1, -pw / 2, pw / 2, ph, ph + pt)
    pdb = pdb + box(pcx - pbl / 2 + 4, pcx + pbl / 2 + 4, -pbw / 2, pbw / 2, ph + pt, ph + pt + pbh)
    C["pdb"] = pdb

    # 13 radios and power modules (foam-taped to the plate)
    rx0, rx1, ry0, ry1, rh = P["radio"]
    C["radio"] = box(rx0, rx1, ry0, ry1, 0, rh)
    mx0, mx1, my0, my1, mh = P["pmods"]
    C["pmods"] = box(mx0, mx1, my0, my1, 0, mh)
    cx0, cx1, cy0, cy1, ch = P["rc_rx"]
    C["rc_rx"] = box(cx0, cx1, cy0, cy1, 0, ch)

    # 14 antennas, SMA bulkheads, safety switch, GNSS mast and receiver (on the lid)
    top = D["lid_z"][1]
    sd, sh_ = P["sma"]
    ants = []
    for (ax, ay) in P["ant_xy"]:
        ants.append(cyl(ax, ay, top, top + sh_, sd))
        ants.append(cyl(ax, ay, top + sh_, top + sh_ + P["ant"][1], P["ant"][0]))
    rx, ry = P["rc_ant_xy"]
    ants.append(cyl(rx, ry, top, top + sh_, sd))
    ants.append(cyl(rx, ry, top + sh_, top + sh_ + P["rc_ant"][1], P["rc_ant"][0]))
    C["antennas"] = _fuse(ants)
    C["switch"] = cyl(*P["switch_xy"], top, top + 8, 16.0) + cyl(*P["switch_xy"], top - 6, top, 12.0)
    tube_d, tube_l = P["mast_tube"]
    t0 = top + P["mast_boss"][1] - 12.0
    C["mast"] = cyl(mx, my, t0, t0 + tube_l, tube_d)
    gd_, gh_ = P["gnss"]
    C["gnss"] = cyl(mx, my, D["mast_top"], D["gnss_top"], gd_)

    # 15 DS-014 pigtail: cable through the plate slot and the shoe notch, plug in front of the payload
    pxp = P["plug_x"]
    pz1 = D["lip_z"][0] - 3
    C["pigtail"] = cyl(pxp - 3, 0, pz1, 6, P["pigtail_d"]) + box(pxp - 30, pxp - 3 + 3.5, -3.5, 3.5, 2, 6) \
        + box(pxp - 34, pxp - 22, -8, 8, 0, 10)
    plx, ply, plz = P["plug"]
    C["plug"] = box(pxp - 3 - ply / 2, pxp - 3 + ply / 2, -plx / 2, plx / 2, pz1 - plz, pz1)
    return C


def harness_context(P=PARAMS):
    """The frame's four power leads (Lift or Range harness, not part of this repo since KWC-DDR-003):
    soldered to the power board pads, out through the rear grommets and over the strain-relief bar.
    For checks and pictures only."""
    D = derived(P)
    lL = P["lid"][0]
    ld = P["lead_d"]
    ph, bt = P["strain_post"][1], P["strain_bar"][2]
    z_out = ph + bt + ld / 2                                  # lead axis where it lies on the bar
    x_in = P["pdb_x"][0] + 6
    x_g = -lL / 2 - 3                                         # leaves the grommet
    x_out = -lL / 2 - P["lead_out"]
    leads = []
    for y in P["leads_y"]:
        leads.append(xcyl(y, P["lead_z"], x_g, x_in, ld))
        leads.append(cyl(x_in - ld / 2, y, P["pdb_standoff_h"] + P["pdb"][2], P["lead_z"], ld))   # drop to the board pad
        # bend down from the grommet height onto the bar, then out to the rear
        leads.append(cyl(x_g - ld / 2, y, z_out - ld / 2, P["lead_z"] + ld / 2, ld))
        leads.append(xcyl(y, z_out, x_out, x_g, ld))
    return _fuse(leads)


# BOM line numbers and names for the colored parts (match bom/bom.csv)
BOM = {
    "plate": (1, "Core plate"),
    "corner_spacers": (2, "Corner spacers (4)"),
    "spacer_left": (3, "Rail spacer bar, left"), "spacer_right": (3, "Rail spacer bar, right"),
    "lip_left": (4, "Rail lip, left"), "lip_right": (4, "Rail lip, right"),
    "tape_left": (5, "Wear tape"), "tape_right": (5, "Wear tape"),
    "front_stops": (6, "Front stops (2)"),
    "pin_block": (7, "Pin blocks (2)"),
    "plunger": (8, "Locking pins (2, indexing plungers)"), "jam_nut": (8, "Locking pin jam nuts"),
    "shoe": (9, "Payload shoe"),
    "lid": (10, "Lid"), "gasket": (11, "Lid gasket"),
    "fc_plate": (12, "Damping plate"), "dampers": (13, "Vibration dampers (4)"), "fc_standoffs": (14, "Standoffs"),
    "pdb_standoffs": (14, "Standoffs"),
    "fc": (15, "Flight controller"), "gnss": (16, "GNSS receiver and compass"), "mast": (17, "GNSS mast"),
    "pdb": (18, "Power distribution board"), "pmods": (19, "Power modules"),
    "radio": (22, "Telemetry radio"), "rc_rx": (23, "Control link receiver"), "antennas": (24, "Antennas"),
    "pigtail": (25, "DS-014 pigtail"), "plug": (25, "DS-014 plug"),
    "switch": (26, "Safety switch"), "grommets": (27, "Grommets (2)"),
    "strain_bar": (21, "Strain-relief bar"), "strain_posts": (21, "Strain-relief bar posts"),
}

# material of each component, for mass (bought electronics use catalogue masses in the calculations)
MATERIAL = {"plate": "cfrp", "strain_bar": "g10", "strain_posts": "al", "corner_spacers": "al", "spacer_left": "al", "spacer_right": "al", "lip_left": "al",
            "lip_right": "al", "tape_left": "uhmw", "tape_right": "uhmw", "front_stops": "al", "pin_block": "al",
            "shoe": "al", "lid": "asa", "fc_plate": "g10", "jam_nut": "steel"}


def deck_context(P=PARAMS):
    """The frame's lower deck (Lift or Range; not part of this repo), for pictures only."""
    L, W, t = P["deck"]
    ox, oy = P["deck_opening"]
    z = P["corner_spacer"][2]
    d = box(-L / 2, L / 2, -W / 2, W / 2, z, z + t) - box(-ox / 2, ox / 2, -oy / 2, oy / 2, z - 1, z + t + 1)
    return _holes(d, frame_points(P), z, z + t, P["frame_holes"][2])


def assembly(P=PARAMS, with_shoe=True, with_deck=False):
    C = build_components(P)
    shapes = [s for k, s in C.items() if with_shoe or k != "shoe"]
    if with_deck:
        shapes.append(deck_context(P))
    return Compound(shapes)


# ------------------------------------------------------------------ constructability checks
TOUCH = [  # pairs that must touch (a face rests on a face or a part sits in a bore)
    ("corner_spacers", "plate"), ("spacer_left", "plate"), ("spacer_right", "plate"),
    ("lip_left", "spacer_left"), ("lip_right", "spacer_right"), ("tape_left", "lip_left"), ("tape_right", "lip_right"),
    ("front_stops", "plate"), ("front_stops", "lip_left"), ("front_stops", "lip_right"),
    ("pin_block", "lip_right"), ("pin_block", "lip_left"), ("plunger", "pin_block"), ("jam_nut", "pin_block"),
    ("shoe", "tape_left"), ("shoe", "tape_right"), ("shoe", "front_stops"),
    ("gasket", "plate"), ("lid", "gasket"), ("fc_standoffs", "plate"), ("dampers", "fc_standoffs"),
    ("fc_plate", "dampers"), ("fc", "fc_plate"), ("pdb_standoffs", "plate"), ("pdb", "pdb_standoffs"),
    ("radio", "plate"), ("pmods", "plate"), ("rc_rx", "plate"), ("antennas", "lid"), ("mast", "lid"),
    ("gnss", "mast"), ("switch", "lid"), ("grommets", "lid"), ("pigtail", "plug"),
    ("strain_posts", "plate"), ("strain_bar", "strain_posts"),
]
HARNESS_TOUCH = ["grommets", "pdb", "strain_bar"]   # the frame harness leads must reach these
GAPS = [  # pairs that must stay apart by at least this much (mm)
    ("shoe", "plate", 0.25), ("shoe", "spacer_left", 0.9), ("shoe", "spacer_right", 0.9),
    ("fc", "lid", 5.0), ("pdb", "fc_plate", 5.0), ("radio", "lid", 0.9), ("pmods", "lid", 0.9),
    ("rc_rx", "fc_standoffs", 1.0), ("pigtail", "shoe", 1.5), ("plug", "lip_left", 10.0), ("plug", "lip_right", 10.0),
    ("pdb", "fc_standoffs", 1.0), ("strain_posts", "gasket", 1.0), ("strain_bar", "lid", 1.0),
]
WEB = 0.6   # mm: a sliver thinner than this would not survive cutting or printing


def check(P=PARAMS, verbose=True):
    """Pairwise interference and contact checks on the components. Returns (passed, failed)."""
    C = build_components(P)
    D = derived(P)
    keys = list(C)
    ok, bad = 0, []
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            try:
                v = (C[a] & C[b]).volume
            except Exception:
                v = 0.0
            if v > 1e-3:
                bad.append(f"overlap {a} / {b}: {v:.3f} mm3")
            else:
                ok += 1
    for a, b in TOUCH:
        d = C[a].distance_to(C[b])
        if d > 0.05:
            bad.append(f"no contact {a} / {b}: gap {d:.2f} mm")
        else:
            ok += 1
    for a, b, g in GAPS:
        if b is None:
            continue
        d = C[a].distance_to(C[b])
        if d < g:
            bad.append(f"too close {a} / {b}: {d:.2f} mm < {g} mm")
        else:
            ok += 1
    # frame harness context: reaches the board pads, the grommets and the bar; clear of the avionics
    har = harness_context(P)
    for k in HARNESS_TOUCH:
        if har.distance_to(C[k]) > 0.05:
            bad.append(f"frame harness leads do not reach {k}")
        else:
            ok += 1
    for k in keys:
        if k in ("grommets", "pdb", "strain_bar", "lid"):
            continue
        try:
            v = (har & C[k]).volume
        except Exception:
            v = 0.0
        if v > 1e-3:
            bad.append(f"overlap frame harness leads / {k}: {v:.3f} mm3")
        else:
            ok += 1
    # deck context: nothing of the core may touch the deck except the corner spacers
    deck = deck_context(P)
    for k in keys:
        if k == "corner_spacers":
            if C[k].distance_to(deck) > 0.05:
                bad.append("corner spacers do not reach the deck")
            else:
                ok += 1
            continue
        try:
            v = (C[k] & deck).volume
        except Exception:
            v = 0.0
        if v > 1e-3:
            bad.append(f"overlap {k} / frame deck")
        else:
            ok += 1
    # payload keep-out: below the lips nothing of the core may enter the payload neck zone (|Y| < lip inner edge - 1)
    nz = D["neck_halfwidth"] - 1
    zone = box(-200, 200, -nz, nz, -200, D["lip_z"][0] - 0.1)
    for k in ("pin_block", "plunger", "jam_nut"):
        if (C[k] & zone).volume > 1e-3:
            bad.append(f"{k} enters the payload neck zone")
        else:
            ok += 1
    if verbose:
        print(f"constructability checks: {ok} passed, {len(bad)} failed")
        for b in bad:
            print("  FAIL", b)
    return ok, bad


def volumes(P=PARAMS):
    C = build_components(P)
    return {k: s.volume / 1000.0 for k, s in C.items()}   # cm3


def main():
    if "--check" in sys.argv:
        ok, bad = check()
        sys.exit(1 if bad else 0)
    ok, bad = check()
    C = build_components()
    (ROOT / "cad/step").mkdir(parents=True, exist_ok=True)
    (ROOT / "cad/stl").mkdir(parents=True, exist_ok=True)
    asm = Compound(list(C.values()))
    export_step(asm, str(ROOT / "cad/step/kitewright-core-assembly.step"))
    for k in ("plate", "lid", "shoe", "pin_block", "fc_plate"):
        export_stl(C[k], str(ROOT / f"cad/stl/kitewright-core-{k.replace('_', '-')}.stl"), tolerance=0.05, angular_tolerance=0.2)
    print("exported cad/step/kitewright-core-assembly.step and STL for the plate, lid, shoe, pin block and damping plate")


if __name__ == "__main__":
    main()
