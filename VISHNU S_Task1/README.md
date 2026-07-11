# EV ADAS Dashboard — Task 1

**Intern:** VISHNU S  
**Task Number:** 1  
**Organization:** OASIS INFOBYTE (OIBSIP)  
**GitHub Repository:** [https://github.com/vishnusadasivan2006-dot/OIBSIP](https://github.com/vishnusadasivan2006-dot/OIBSIP)

---

## 📋 Project Overview

This project implements a **real-time EV (Electric Vehicle) ADAS (Advanced Driver Assistance System) Dashboard** built entirely in Python using `matplotlib`. The dashboard reads live telemetry data from an STM32 microcontroller (via a virtual COM port in PicSimLab) and visualizes it across 5 live panels simultaneously.

---

## 🚗 Features

| Panel | Description |
|---|---|
| **Speedometer** | Animated arc gauge showing speed (0–200 km/h) with color-coded zones |
| **Battery (SOC)** | Horizontal bar for State of Charge (%), estimated range (km), and drive mode |
| **Speed History** | Scrolling 60-sample line chart of speed over time |
| **EV Metrics** | Live readout: torque, acceleration, brake %, motor temperature, alarm, fault code |
| **ADAS Bird-Eye** | Top-down view showing ego vehicle, front obstacle distance, TTC, and blind-spot warnings |

---

## 🛠️ Tech Stack

- **Language:** Python 3.8+
- **Libraries:** `matplotlib`, `numpy`, `pyserial`
- **Hardware Target:** STM32 via PicSimLab virtual COM port
- **Protocol:** UART serial @ 115200 baud

---

## 📂 File Structure

```
VISHNU S_Task1/
├── VISHNU S_Task1.py      # Main dashboard script
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/vishnusadasivan2006-dot/OIBSIP.git
cd OIBSIP/"VISHNU S_Task1"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Dashboard

### Demo Mode (No Hardware Required)
Run with simulated fake telemetry data — perfect for testing the dashboard without any hardware:
```bash
python "VISHNU S_Task1.py" --demo
```

### Live Hardware Mode (STM32 / PicSimLab)
Connect your STM32 board and provide the COM port:
```bash
# Windows
python "VISHNU S_Task1.py" --port COM3

# Linux
python "VISHNU S_Task1.py" --port /dev/ttyUSB0
```

### Options
| Flag | Description | Default |
|---|---|---|
| `--port` | Serial port (e.g., `COM3`) | None |
| `--baud` | Baud rate | `115200` |
| `--demo` | Run with generated fake data | `False` |

---

## 📡 Serial Telemetry Protocol

The dashboard expects two alternating line formats from the STM32 firmware:

**Line 1 — Vehicle dynamics:**
```
SPD:72.5 SOC:84.3 TRQ:120 TMP:38.2 RNG:2520 ACC:65 BRK:5
```

**Line 2 — ADAS sensor data:**
```
F:180 L:250 R:300 TTC:8.9s COL:0 BSD:00 ALM:0 FLT:00
```

| Field | Meaning |
|---|---|
| `SPD` | Speed in km/h |
| `SOC` | Battery state of charge (%) |
| `TRQ` | Motor torque (Nm) |
| `TMP` | Motor temperature (°C) |
| `RNG` | Estimated range (km) |
| `ACC` | Accelerator pedal (%) |
| `BRK` | Brake pedal (%) |
| `F/L/R` | Front/Left/Right obstacle distance (cm) |
| `TTC` | Time to collision (s) |
| `COL` | Collision risk level (0=safe, 1=warn, 2=critical) |
| `BSD` | Blind-spot detection left/right (0 or 1) |
| `ALM` | Alarm level (0=NONE, 1=ADVISORY, 2=WARNING, 3=CRITICAL) |
| `FLT` | Fault code (hex) |

---

## 🎨 Dashboard Color Coding

The dashboard runs in a dark-themed window with color-coded indicators:

- 🟢 **Green** — Safe / Normal
- 🟡 **Yellow** — Advisory / Moderate speed
- 🟠 **Orange** — Warning
- 🔴 **Red** — Critical / High speed / Low battery

---

## 📝 How to Stop

Press `Ctrl+C` in the terminal to stop the dashboard. The serial port is gracefully closed automatically.

---

## 👤 Author

**VISHNU S**  
Intern — OASIS INFOBYTE (OIBSIP)  
GitHub: [vishnusadasivan2006-dot](https://github.com/vishnusadasivan2006-dot)
