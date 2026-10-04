"""Kitewright Core sizing calculations, KWC-CAL-001 (TRL 3, constructable design of KWC-DDR-002).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md (tags in brackets, for example [A3]) and
writes docs/04-calcs/results.csv. Geometry and part volumes come from cad/src/model.py, so the
parts here are the parts in the STEP file, the drawings and the build plan. Costs come from
bom/bom.csv and the value-engineering target from project.yaml. First-principles paper estimates;
nothing here is measured.
"""
import csv
import math
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad/src"))
from model import PARAMS as P, RHO, MATERIAL, derived, volumes  # noqa: E402

D = derived(P)
rows = []
G = 9.81


def out(tag, text):
    print(f"[{tag}] {text}")


def res(rid, value, target, status):
    rows.append((rid, value, target, status))


# =============================================================== assumptions
M_RATED = 5.0            # kg, rated payload on the mount (Lift's sea-level payload, KWC-DDR-001 D4)
K_STATIC = 3.0           # R3 static factor
K_DROP, A_DROP = 1.5, 2.0  # R3: 1.5 x rated mass under a 2 g drop
A_FORE = 3.0             # g, fore-aft design case (hard landing or crash pitch), times K_DROP
A_SIDE = 1.0             # g, side case, payload centre of mass 80 mm below the shoe
H_CG = 80.0              # mm
SY_6061, SY_5052 = 276.0, 193.0   # MPa yield, 6061-T6 and 5052-H32
S_CFRP = 250.0           # MPa, design allowable of a quasi-isotropic 2 mm carbon plate in bending (conservative; typical flexural strength 500 to 600 MPa)
TAU_PIN = 400.0          # MPa, hardened steel plunger pin, shear (conservative)
F_M4 = 8.78 * 450.0 * 0.8
# Payload power
P_PAY = 100.0            # W, R4
V_BUS_MIN = {"6S Li-ion at end of discharge (3.0 V/cell)": 18.0, "12S Li-ion at end of discharge": 36.0,
             "14S Li-ion at end of discharge (3.0 V/cell), ColdCell variant for Lift": 42.0,
             "16S LiFePO4 at end of discharge (2.8 V/cell)": 44.8}
V_BUS_TOP = {"14S Li-ion full (4.2 V/cell), ColdCell variant for Lift": 58.8, "16S LiFePO4 full (3.65 V/cell)": 58.4}
V_BOARD_MAX = 60.0       # V, rating of the power board and power modules (BOM lines 18, 19)
R_PIGTAIL = 0.30 * 0.0333 * 2 / 2   # ohm: 0.3 m, 20 AWG out and back, two pins in parallel each way
EFUSE_LIMIT = 8.0        # A
# Heat
H_STILL, H_FORCED = 10.0, 25.0     # W/m2K, still air (convection plus radiation) and in hover
T_AMB_HOT, T_AMB_COLD = 45.0, -20.0
T_BODY = 10.0            # K, allowance for sun on the frame's body shell around the lid
T_PART_MAX = 85.0        # degC, rated maximum of the flight controller, radio and GNSS class parts
T_PART_MIN = -40.0
HOTSPOT = 10.0           # K, allowance between lid air and the hottest part
# W dissipated inside the lid: ground idle and hover (Lift at 100 A bus current)
DISS_IDLE = {"Flight controller (with IMU heater)": 2.5, "Telemetry radio (standby and bursts)": 1.0,
             "Control link receiver": 0.3, "5.3 V supplies at 90 % (about 10 W out)": 1.1}
I_HOVER = 100.0          # A, Lift hover estimate (about 4.4 kW at 44 V)
R_PATH = 0.4e-3          # ohm, PDB bus bar, current sensor and solder joints inside the lid
DISS_HOVER = dict(DISS_IDLE)
DISS_HOVER["Telemetry radio (standby and bursts)"] = 2.0
DISS_HOVER["Payload switch at 5.6 A, 15 mOhm"] = 5.6 ** 2 * 0.015
DISS_HOVER["Bus conduction at 100 A, 0.4 mOhm"] = I_HOVER ** 2 * R_PATH
# Atmosphere and hover
RHO0 = 1.225
CAP_COLD_BARE = 0.60     # usable capacity of an unheated Li-ion pack at -20 degC, fraction of 25 degC
CAP_WARM = 0.95          # ColdCell pack kept warm
HEATER_SHARE = 0.05      # fraction of pack energy spent on its heater in flight
# Bought-part masses, g (catalogue class values, to confirm when bought)
M_BOUGHT = {"Flight controller (FMUv6X class, with baseboard)": 100.0, "GNSS receiver and compass": 35.0,
            "GNSS mast tube and thumbscrew": 10.0, "Locking pins (2 plungers)": 50.0,
            "Vibration dampers (4)": 8.0, "Standoffs (8)": 12.0, "Bonded flush inserts M3 (16)": 6.4,
            "Power distribution board with current sensor": 70.0, "Power modules (monitor, backup supply, payload switch)": 35.0,
            "Telemetry radio (air side)": 25.0,
            "Control link receiver": 6.0, "Antennas and SMA bulkheads (3)": 60.0, "DS-014 pigtail and plug": 35.0,
            "Safety switch and buzzer": 15.0, "Grommets (2)": 6.0, "Signal harness": 50.0, "Fasteners": 30.0,
            "Lid gasket": 4.0}
M_COMPANION = 60.0       # optional companion computer, carried outside the core lid
M_LEADS_MOVED = 124.0    # g: four 8 AWG leads and AS150 halves, now in each frame's harness (KWC-DDR-003)
R9_LIMIT = 1.0           # kg, as written in KWC-REQ-001 R9


def isa(h):
    T = 288.15 - 0.0065 * h
    p = 101325.0 * (T / 288.15) ** 5.2559
    return T, p, p / (287.05 * T)


print("Kitewright Core sizing, KWC-CAL-001")

# =============================================================== A. mount strength (R3)
F_static = K_STATIC * M_RATED * G
F_drop = K_DROP * M_RATED * A_DROP * G
F_v = max(F_static, F_drop)
out("A1", f"Rated payload {M_RATED:.0f} kg; static case {F_static:.0f} N; drop case {F_drop:.0f} N; vertical design load {F_v:.0f} N")
lw, lt = P["lip"]
ov = D["overlap"]
L_bear = P["shoe"][0]
arm = (P["plate"][1] / 2 - P["spacer_bar"][0]) - (D["lip_y"][0] + ov / 2)   # spacer inner edge to the middle of the overlap
M_lip = F_v / 2 * arm
Z_lip = L_bear * lt ** 2 / 6
s_lip_root = M_lip / Z_lip
# the lip pockets (KWC-DDR-003) stop 1.5 mm short of the spacer, so the root keeps the full 3 mm; at the
# pocket edge the lever is shorter but, conservatively, the whole shoe length is taken at the pocket skin
pk_d, pk_y0, pk_y1 = P["lip_pocket"]
arm_pk = pk_y1 - (D["lip_y"][0] + ov / 2)
skin = lt - pk_d
s_lip_pk = F_v / 2 * arm_pk / (L_bear * skin ** 2 / 6)
s_lip = max(s_lip_root, s_lip_pk)
out("A2", f"Shoe overlaps each lip by {ov:.1f} mm over {L_bear:.0f} mm; lever {arm:.1f} mm; lip bending at the root {s_lip_root:.1f} MPa; "
          f"at the pocket edge (lever {arm_pk:.1f} mm, {skin:.1f} mm skin over the whole length, conservative) {s_lip_pk:.1f} MPa vs 276 MPa (factor {SY_6061 / s_lip:.0f})")
n_scr = 5 + 5   # screws per side: 3 rail, 2 block (the stop screws carry no vertical shoe load)
F_scr = F_v / n_scr * (1 + arm / (P["spacer_bar"][0] / 2))   # prying factor about the spacer edge
out("A3", f"Rail screws M4: {n_scr} in all; worst tension with prying {F_scr:.0f} N vs {F_M4:,.0f} N allowable (factor {F_M4 / F_scr:.0f})")
span = P["frame_holes"][0] * 2
w = F_v / 2 / (P["rail_x"][1] - P["rail_x"][0])     # N/mm along each rail
M_beam = w * span ** 2 / 8
Zs = (lambda b, h: b * h ** 2 / 6)
ww = P["spacer_window_wall"]
Z_side = (Zs(30.0, P["plate"][2]) + Zs(2 * ww, P["spacer_bar"][1])
          + Zs(lw - (pk_y1 - pk_y0), lt) + Zs(pk_y1 - pk_y0, skin))     # at a pocket: spacer walls only, lip skin
s_beam = M_beam / Z_side
S_SIDE = min(S_CFRP, SY_6061)
out("A4", f"Plate edge strip (carbon), spacer walls and pocketed lip as one side beam between frame bolts {span:.0f} mm apart, taken at a pocket: "
          f"{s_beam:.0f} MPa vs {S_SIDE:.0f} MPa, the lower of the carbon plate allowable and 6061 yield (factor {S_SIDE / s_beam:.1f}); the three parts are taken as separate (not bonded), which is conservative")
F_fore = K_DROP * M_RATED * A_FORE * G
A_pin = math.pi * P["pin_d"] ** 2 / 4
tau = F_fore / A_pin
bear = F_fore / (P["pin_d"] * P["shoe"][2])
out("A5", f"Fore-aft {A_FORE:.0f} g x {K_DROP} x {M_RATED:.0f} kg = {F_fore:.0f} N on ONE pin: shear {tau:.1f} MPa vs {TAU_PIN:.0f} MPa; bearing in the 5 mm shoe {bear:.1f} MPa vs 276 MPa")
A_stop = P["front_stop"][1] * P["shoe"][2] * 2
out("A6", f"Forward load into the two front stops: bearing {F_fore / A_stop:.1f} MPa on {A_stop:.0f} mm2")
M_roll = A_SIDE * K_DROP * M_RATED * G * H_CG / 1000
F_roll = M_roll / ((P["shoe"][1] / 2 - ov / 2) * 2 / 1000)
out("A7", f"Side case: roll moment {M_roll:.1f} N m reacted across the lips: {F_roll:.0f} N per side")
bear_cf = F_v / 4 / (P["frame_holes"][2] * P["plate"][2])
out("A8", f"Frame bolt bearing in the 2 mm carbon plate: {bear_cf:.1f} MPa per hole at the vertical design load (carbon bearing strength typically over 300 MPa)")
r3_ok = SY_6061 / s_lip > 5 and F_M4 / F_scr > 5 and S_SIDE / s_beam > 5 and TAU_PIN / tau > 5
res("R3", f"Vertical {F_v:.0f} N: lips {SY_6061 / s_lip:.0f}x, screws {F_M4 / F_scr:.0f}x, side beam {S_SIDE / s_beam:.1f}x; fore-aft {F_fore:.0f} N on one pin {TAU_PIN / tau:.0f}x",
    "3 x and 1.5 x at 2 g, rated 5 kg", "Met on paper" if r3_ok else "Not met")

# =============================================================== B. payload swap (R2)
STEPS = [("Unplug the DS-014 plug", 6), ("Pull and twist both locking pins to their rest", 5), ("Slide the payload out to the rear", 4),
         ("Slide the next payload in to the front stops", 5), ("Twist both pins back; they snap into the shoe", 3),
         ("Plug the DS-014 plug and close its latch", 8), ("Check both pins show no red band; tug the payload", 4)]
t_bare = sum(t for _, t in STEPS)
GLOVE = 1.5
out("B1", f"Swap sequence {t_bare} s bare-handed; x {GLOVE} with gloves = {t_bare * GLOVE:.0f} s; no tools")
res("R2", f"About {t_bare * GLOVE:.0f} s with gloves, no tools; pin state shown by a red band", "60 s, no tools, pin visible",
    "Met on paper (estimate)" if t_bare * GLOVE <= 60 else "At risk")

# =============================================================== C. payload power (R4)
for k, v in V_BUS_MIN.items():
    i = P_PAY / v
    out("C1", f"{k}: {v:.1f} V; 100 W needs {i:.2f} A; pigtail drop {i * R_PIGTAIL * 1000:.0f} mV")
i_max = P_PAY / min(V_BUS_MIN.values())
out("C2", f"Payload switch current limit {EFUSE_LIMIT:.0f} A covers the worst case {i_max:.2f} A with {EFUSE_LIMIT / i_max:.2f} x margin")
for k, v in V_BUS_TOP.items():
    out("C3", f"{k}: {v:.1f} V, {V_BOARD_MAX - v:.1f} V under the {V_BOARD_MAX:.0f} V rating of the power board and modules")
res("R4", f"100 W needs at most {i_max:.1f} A (6S at 18 V); switch limit {EFUSE_LIMIT:.0f} A; DS-014 pin rating to confirm",
    "100 W continuous at bus voltage", "Met on paper (pin rating to confirm)")

# =============================================================== D. heat (R5)
lL, lW, lH, wall = P["lid"]
A_lid = (lL * lW + 2 * (lL + lW) * lH) / 1e6
q_idle = sum(DISS_IDLE.values())
q_hover = sum(DISS_HOVER.values())
dT_idle = q_idle / (H_STILL * A_lid)
dT_hover = q_hover / (H_FORCED * A_lid)
out("D1", f"Lid surface {A_lid:.4f} m2; inside dissipation {q_idle:.1f} W on the ground, {q_hover:.1f} W in Lift hover at {I_HOVER:.0f} A")
for k, v in DISS_HOVER.items():
    out("D1", f"   {k}: {v:.2f} W")
t_hot_idle = T_AMB_HOT + T_BODY + dT_idle
t_hot_hover = T_AMB_HOT + T_BODY + dT_hover
t_hot = max(t_hot_idle, t_hot_hover) + HOTSPOT
out("D2", f"Hot: lid air {t_hot_idle:.1f} degC on the ground (rise {dT_idle:.1f} K), {t_hot_hover:.1f} degC in hover (rise {dT_hover:.1f} K); hottest part about {t_hot:.0f} degC vs {T_PART_MAX:.0f} degC rating")
t_cold = T_AMB_COLD + dT_idle
out("D3", f"Cold: parts cold-soaked to {T_AMB_COLD:.0f} degC at boot (rated {T_PART_MIN:.0f} degC); lid air settles near {t_cold:.0f} degC once running")
res("R5", f"Hottest part about {t_hot:.0f} degC at 45 degC ambient; cold boot at -20 degC within the -40 degC rating", "-20 to +45 degC",
    "Met on paper" if t_hot <= T_PART_MAX else "At risk")

# =============================================================== E. altitude (R6)
for h in (0, 3000, 5000, 6000):
    T, p, r = isa(h)
    out("E1", f"ISA {h:>5,} m: {T - 273.15:6.1f} degC, {p / 1000:5.1f} kPa, density {r:.3f} kg/m3 ({r / RHO0 * 100:.0f} % of sea level)")
T5, p5, r5 = isa(5000)
rho_cold = p5 / (287.05 * (273.15 - 20))
out("E2", f"At 5,000 m and -20 degC: density {rho_cold:.3f} kg/m3; barometer range needed down to {p5 / 1000:.0f} kPa (typical flight-controller barometers read 30 to 110 kPa)")
res("R6", "Sensors in range at 54 kPa; failsafe set per altitude band (Table 6); control margin is a frame property", "Stable control and failsafes at 5,000 m density",
    "Met on paper (core); flight check needs a frame")

# =============================================================== F. hover-time model (R7)
ratio_air = math.sqrt(r5 / RHO0)
bare = ratio_air * CAP_COLD_BARE
warm = ratio_air * CAP_WARM * (1 - HEATER_SHARE)
out("F1", f"Same aircraft and mass: hover power scales with 1/sqrt(density), so time scales by {ratio_air:.3f} at 5,000 m")
out("F2", f"Unheated packs at -20 degC ({CAP_COLD_BARE:.0%} capacity): {bare:.1%} of sea-level hover time (the scaffold's 47 % estimate)")
out("F3", f"ColdCell packs kept warm ({CAP_WARM:.0%} capacity, {HEATER_SHARE:.0%} heater share): {warm:.1%} of sea-level hover time")
res("R7", f"Model published: {bare:.0%} (cold packs) and {warm:.0%} (ColdCell) of sea-level hover time at 5,000 m and -20 degC", "Within 15 % of measured",
    "Model ready; accuracy shown only at TRL 4")

# =============================================================== G. common core (R8, R10)
IO = {"Lift, eight motors": 8 + 3, "Lift, six motors": 6 + 3, "Range, four lift motors, pusher and five servos": 4 + 1 + 5}
for k, v in IO.items():
    out("G1", f"{k}: {v} outputs needed of 16 on an FMUv6X class controller")
res("R8", "One core, one interface (Table 7); Lift needs 11 of 16 outputs and Range 10 of 16; parameter sets only", "Same core in Lift and Range",
    "Met by design")
res("R10", "Released PX4 (v1.15 or later), parameters and stock modules only; ColdCell reports over DroneCAN", "Released PX4, no source change",
    "Met by design")
res("R1", "DS-014 40-pin connector on a 0.3 m pigtail; signals from the flight controller and bus; licence and pinout to confirm", "DS-014 signals and power present",
    "Met on paper (licence and pinout to confirm)")

# =============================================================== H. mass (R9)
V = volumes()
made = {}
for k, mat in MATERIAL.items():
    made[k] = V[k] * RHO[mat]
shoe_g = made.pop("shoe")
m_made = sum(made.values())
m_bought = sum(M_BOUGHT.values())
m_core = (m_made + m_bought) / 1000
out("H1", "Made parts from model volumes, g: " + ", ".join(f"{k} {v:.0f}" for k, v in made.items()))
out("H2", f"Made parts {m_made:.0f} g; bought parts {m_bought:.0f} g; core {m_core:.3f} kg without the shoe ({shoe_g:.0f} g, counted with each payload) and without the optional companion computer ({M_COMPANION:.0f} g, outside the lid)")
over = m_core - R9_LIMIT
out("H3", f"R9: {m_core:.3f} kg against the R9 figure; {over * 1000:+.0f} g ({over / R9_LIMIT:+.1%})")
# what decision O1 option B changed (KWC-DDR-003), against the design of KWC-DDR-002
was = {"plate": V["plate"] * RHO["al"], "lid (2 mm walls)": 114.0, "rail spacer bars and lips, unpocketed": 158.0,
       "power leads and four AS150 halves": M_LEADS_MOVED, "clinch nuts (14)": 7.0}
now = {"plate": made["plate"], "lid (2 mm walls)": made["lid"],
       "rail spacer bars and lips, unpocketed": made["lip_left"] + made["lip_right"] + made["spacer_left"] + made["spacer_right"],
       "power leads and four AS150 halves": made["strain_bar"] + made["strain_posts"],
       "clinch nuts (14)": M_BOUGHT["Bonded flush inserts M3 (16)"]}
for k in was:
    out("H4", f"O1 option B: {k}: {was[k]:.0f} g before, {now[k]:.0f} g now ({now[k] - was[k]:+.0f} g)")
saved = sum(was.values()) - sum(now.values())
out("H5", f"O1 option B saves {saved:.0f} g against the 1.274 kg design of KWC-DDR-002; the leads ({M_LEADS_MOVED:.0f} g) are now carried in each frame's harness")
out("H6", f"R9 margin {-over * 1000:.0f} g, inside the accuracy of the bought-part catalogue masses: weigh the built core at TRL 4")
res("R9", f"{m_core:.3f} kg estimated (carbon plate, 1.5 mm lid walls, pocketed rail bars; power leads in the frame harness)", "See KWC-REQ-001 R9",
    "Not met" if over > 0 else f"Met on paper ({-over * 1000:.0f} g margin)")

# =============================================================== I. cost (R11)
bom = list(csv.DictReader((ROOT / "bom/bom.csv").open()))
total = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in bom)
air = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in bom if r.get("group", "") == "air")
ground = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in bom if r.get("group", "") == "ground")
spares = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in bom if r.get("group", "") == "spares")
target = float(yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"])
diff = total - target
out("I1", f"BOM: airborne core USD {air:,.2f}; ground station USD {ground:,.2f}; spares USD {spares:,.2f}; total USD {total:,.2f}")
out("I2", f"Value-engineering target: USD {target:,.0f}. Estimated cost of the constructable design: USD {total:,.2f} (USD {abs(diff):,.2f} {'over' if diff > 0 else 'under'} the target)")
res("R11", f"USD {total:,.2f} including ground station and spares", f"Value-engineering target USD {target:,.0f}",
    f"Under the target by USD {abs(diff):,.2f}" if diff <= 0 else f"Over the target by USD {diff:,.2f}")

# =============================================================== results
order = [f"R{i}" for i in range(1, 12)]
rows.sort(key=lambda r: order.index(r[0]))
with (ROOT / "docs/04-calcs/results.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["requirement", "result", "target", "status"])
    w.writerows(rows)
print()
for r in rows:
    print(f"[L] {r[0]}: {r[3]}: {r[1]}")
