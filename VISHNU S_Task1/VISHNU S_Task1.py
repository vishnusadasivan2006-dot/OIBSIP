"""
EV ADAS Dashboard — Python side
Reads two telemetry lines every 100 ms from the STM32 (via PicSimLab's virtual COM port)
and draws 5 live panels with matplotlib.

Run with real/simulated hardware:
    python dashboard.py --port COM3      (Windows)
    python dashboard.py --port /dev/ttyUSB0   (Linux)

Run without hardware (fake data, useful to test the dashboard alone):
    python dashboard.py --demo
"""

import re
import time
import random
import argparse
import collections

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

try:
    import serial
except ImportError:
    serial = None


# ---------- Shared state dictionary (Python side of the "shared whiteboard") ----------
state = {
    "spd": 0.0, "soc": 100.0, "trq": 0.0, "tmp": 25.0, "rng": 3000.0,
    "acc": 0.0, "brk": 0.0,
    "f": 400, "l": 400, "r": 400, "ttc": 99.0,
    "col": 0, "bsd_l": 0, "bsd_r": 0, "alm": 0, "flt": 0,
    "mode": "NORMAL", "signal": "ON",
}

speed_history = collections.deque([0.0] * 60, maxlen=60)

LINE1_RE = re.compile(
    r"SPD:([\d.]+)\s+SOC:([\d.]+)\s+TRQ:(-?[\d.]+)\s+TMP:([\d.]+)\s+RNG:([\d.]+)\s+ACC:([\d.]+)\s+BRK:([\d.]+)"
)
LINE2_RE = re.compile(
    r"F:(\d+)\s+L:(\d+)\s+R:(\d+)\s+TTC:([\d.]+)s\s+COL:(\d+)\s+BSD:(\d)(\d)\s+ALM:(\d)\s+FLT:([0-9A-Fa-f]+)"
)


def parse_line(line: str):
    """Update `state` dict from one telemetry line. Returns True if it matched."""
    m1 = LINE1_RE.search(line)
    if m1:
        state["spd"] = float(m1.group(1))
        state["soc"] = float(m1.group(2))
        state["trq"] = float(m1.group(3))
        state["tmp"] = float(m1.group(4))
        state["rng"] = float(m1.group(5))
        state["acc"] = float(m1.group(6))
        state["brk"] = float(m1.group(7))
        speed_history.append(state["spd"])
        return True

    m2 = LINE2_RE.search(line)
    if m2:
        state["f"] = int(m2.group(1))
        state["l"] = int(m2.group(2))
        state["r"] = int(m2.group(3))
        state["ttc"] = float(m2.group(4))
        state["col"] = int(m2.group(5))
        state["bsd_l"] = int(m2.group(6))
        state["bsd_r"] = int(m2.group(7))
        state["alm"] = int(m2.group(8))
        state["flt"] = int(m2.group(9), 16)
        return True

    return False


# ---------- Demo data generator (no hardware needed) ----------
def demo_tick():
    state["spd"] = max(0, min(200, state["spd"] + random.uniform(-3, 4)))
    state["soc"] = max(0, state["soc"] - 0.01)
    state["trq"] = random.uniform(-40, 200)
    state["tmp"] = 25 + state["spd"] * 0.2 + random.uniform(-1, 1)
    state["rng"] = state["soc"] / 100.0 * 3000
    state["acc"] = random.uniform(0, 100)
    state["brk"] = random.uniform(0, 20)
    state["f"] = random.randint(15, 400)
    state["ttc"] = 99 if state["f"] > 100 else state["f"] / max(state["spd"] / 3.6, 1)
    state["col"] = 2 if state["f"] < 20 else 1 if state["f"] < 50 else 0
    state["alm"] = 3 if state["col"] == 2 else 2 if state["col"] == 1 else 0
    speed_history.append(state["spd"])


ALARM_NAMES = {0: "NONE", 1: "ADVISORY", 2: "WARNING", 3: "CRITICAL"}
ALARM_COLORS = {0: "#2ecc71", 1: "#f1c40f", 2: "#e67e22", 3: "#e74c3c"}


def speed_color(spd):
    if spd < 80:
        return "#2ecc71"
    if spd < 140:
        return "#f1c40f"
    return "#e74c3c"


def draw_speed(ax):
    ax.clear()
    ax.set_facecolor("#0d0d14")
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-0.2, 1.3)
    ax.axis("off")
    theta = np.linspace(np.pi, 0, 100)
    ax.plot(np.cos(theta), np.sin(theta), color="#444", lw=10)
    frac = min(state["spd"], 200) / 200.0
    theta2 = np.linspace(np.pi, np.pi - frac * np.pi, 50)
    ax.plot(np.cos(theta2), np.sin(theta2), color=speed_color(state["spd"]), lw=10)
    ang = np.pi - frac * np.pi
    ax.plot([0, 0.85 * np.cos(ang)], [0, 0.85 * np.sin(ang)], color="white", lw=3)
    ax.text(0, 0.15, f"{state['spd']:.0f}", ha="center", fontsize=26, color="white", weight="bold")
    ax.text(0, -0.05, "km/h", ha="center", fontsize=10, color="#aaaaaa")
    ax.set_title("Speedometer", color="white", fontsize=12, loc="left")


def draw_soc(ax):
    ax.clear()
    ax.set_facecolor("#0d0d14")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 1)
    ax.axis("off")
    color = "#2ecc71" if state["soc"] > 20 else "#e74c3c"
    ax.barh(0.5, state["soc"], height=0.5, color=color)
    ax.barh(0.5, 100, height=0.5, color="#333", zorder=0)
    ax.barh(0.5, state["soc"], height=0.5, color=color, zorder=1)
    ax.text(0, 0.5, f"{state['soc']:.1f}%   ~{state['rng']:.0f} km   Mode: {state['mode']}",
            va="center", fontsize=11, color="white")
    ax.set_title("Battery (SOC)", color="white", fontsize=12, loc="left")


def draw_speed_history(ax):
    ax.clear()
    ax.set_facecolor("#0d0d14")
    ax.plot(list(speed_history), color="cyan", lw=2)
    ax.set_ylim(0, 220)
    ax.tick_params(colors="#888888", labelsize=8)
    for spine in ax.spines.values():
        spine.set_color("#333333")
    ax.set_title("Speed History", color="white", fontsize=12, loc="left")


def draw_metrics(ax):
    ax.clear()
    ax.set_facecolor("#0d0d14")
    ax.axis("off")
    rows = [
        ("TORQUE", f"{state['trq']:.0f} Nm"),
        ("ACCEL", f"{state['acc']:.0f} %"),
        ("BRAKE", f"{state['brk']:.0f} %"),
        ("MOT TEMP", f"{state['tmp']:.1f} °C"),
        ("ALARM", ALARM_NAMES[state["alm"]]),
        ("FAULT", f"0x{state['flt']:02X}"),
        ("SIGNAL", state["signal"]),
    ]
    y = 0.95
    for label, val in rows:
        ax.text(0.02, y, label, fontsize=10, color="#999999", transform=ax.transAxes)
        ax.text(0.62, y, val, fontsize=10, color="white", weight="bold", transform=ax.transAxes)
        y -= 0.14
    ax.set_title("EV Metrics", color="white", fontsize=12, loc="left")


def draw_adas(ax):
    ax.clear()
    ax.set_facecolor("#0d0d14")
    ax.set_xlim(-2, 2)
    ax.set_ylim(0, 5)
    ax.axis("off")
    ax.add_patch(patches.Rectangle((-0.9, -0.1), 0.5, -0.1, transform=ax.transAxes, clip_on=False))  # no-op placeholder
    ax.add_patch(patches.Circle((0, 0.3), 0.25, color="#3498db"))  # ego car
    col_color = ALARM_COLORS[state["col"] * 1 if state["col"] < 3 else 3]
    front_y = 0.3 + max(0.3, min(4.5, state["f"] / 100.0))
    ax.add_patch(patches.Rectangle((-0.25, front_y), 0.5, 0.3, color=col_color))
    if state["bsd_l"]:
        ax.add_patch(patches.Rectangle((-1.6, 0.1), 0.4, 0.6, color="#e67e22", alpha=0.7))
    if state["bsd_r"]:
        ax.add_patch(patches.Rectangle((1.2, 0.1), 0.4, 0.6, color="#e67e22", alpha=0.7))
    ax.text(0, 4.7, f"TTC: {state['ttc']:.1f}s   F:{state['f']}cm", ha="center", color="white", fontsize=9)
    ax.set_title("ADAS Bird-Eye", color="white", fontsize=12, loc="left")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=None, help="Serial port, e.g. COM3 or /dev/ttyUSB0")
    parser.add_argument("--baud", type=int, default=115200)
    parser.add_argument("--demo", action="store_true", help="Run with generated fake data")
    args = parser.parse_args()

    ser = None
    if not args.demo:
        if serial is None:
            raise SystemExit("pyserial not installed. Run: pip install pyserial")
        if not args.port:
            raise SystemExit("Provide --port COMx (or use --demo for no hardware).")
        ser = serial.Serial(args.port, args.baud, timeout=0.2)

    plt.style.use("dark_background")
    fig, axes = plt.subplots(2, 3, figsize=(13, 7))
    fig.suptitle("EV ADAS Dashboard", color="white", fontsize=16)
    fig.patch.set_facecolor("#0d0d14")
    ax_speed, ax_soc, ax_adas = axes[0]
    ax_hist, ax_metrics, ax_blank = axes[1]
    ax_blank.axis("off")

    plt.ion()
    plt.show()

    try:
        while True:
            if args.demo:
                demo_tick()
                time.sleep(0.1)
            else:
                raw = ser.readline().decode(errors="ignore").strip()
                if raw:
                    parse_line(raw)
                else:
                    continue

            draw_speed(ax_speed)
            draw_soc(ax_soc)
            draw_speed_history(ax_hist)
            draw_metrics(ax_metrics)
            draw_adas(ax_adas)
            plt.pause(0.01)
    except KeyboardInterrupt:
        pass
    finally:
        if ser:
            ser.close()


if __name__ == "__main__":
    main()
