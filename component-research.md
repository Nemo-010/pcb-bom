# Component research — small MCU + WiFi + IMU, and the driver stage

Job description: **one small module that already has MCU + WiFi + IMU**, so the
custom board is only the motor-driver stage. Robu pages checked **2026-10-15**.

## The short version

**No XIAO-sized board has WiFi *and* an IMU.** The XIAO is 21 × 17.8 mm and you
only get one of the two:

| Board | Size | MCU | Radio | IMU | Price | Stock |
|---|---|---|---|---|---|---|
| Seeed XIAO ESP32S3 | **21 × 17.8 mm** | ESP32-S3 | WiFi + BLE 5 | — | ₹1139 | OOS |
| Seeed XIAO ESP32-C5 | 21 × 17.8 mm | ESP32-C5 | WiFi 6 dual-band | — | ₹979 | In stock |
| Seeed XIAO nRF52840 Sense | 21 × 17.8 mm | nRF52840 | BLE only | LSM6DS3TR-C | — | OOS |
| **Arduino Nicla Sense ME** | **22.9 × 22.9 mm, 2 g** | nRF52832 | BLE only | **BHI260AP 9-axis** + BME688 | ₹5409 | **In stock** |
| **Arduino Nicla Vision** | **22.9 × 22.9 mm** | STM32H747 | **NINA-W102 WiFi + BLE** | **LSM6DSOX** + camera | ₹9089 | listed |
| Waveshare ESP32-S3 + RGB matrix | small | ESP32-S3 | WiFi + BLE | **QMI8658C** | ₹1189 | OOS |
| M5Stack M5StickS3 (K150) | ~48 × 24 mm | ESP32-S3 | WiFi + BLE | 6-axis (unnamed) | ₹3779 | In stock |
| M5Stack CoreS3 | 54 × 54 mm | ESP32-S3 | WiFi | BMI270 + BMM150 | ₹7759 | OOS |
| Arduino Nano 33 IoT | 45 × 18 mm | SAMD21 | WiFi | LSM6DS3 | ₹2709 | In stock (too big) |

## Pick, smallest first

1. **Seeed XIAO ESP32S3 + a bare 2.5 × 3 mm IMU on your carrier.** This is the
   actual smallest answer. The XIAO is 21 × 17.8 mm; drop an LGA-14 IMU
   (`LSM6DSO32` / `BMI270` / `ICM-42688-P`) next to it and the whole compute
   block is still XIAO-sized and ~3 g. You keep designing only the motor
   driver; the IMU is a 14-pad footprint, not a subsystem. XIAO ESP32S3 is OOS
   right now, but OOS is acceptable per you — and the XIAO ESP32-C5 (WiFi 6) is
   in stock as a drop-in-ish fallback.
2. **Arduino Nicla Sense ME — 22.9 × 22.9 mm, 2 g, in stock (₹5409).** The
   smallest *integrally* packaged board with a real IMU: **BHI260AP** (9-axis,
   on-chip sensor fusion — actually better for a flight loop than an LSM6DS3)
   plus a BME688. Catch: **BLE only, no WiFi**.
3. **Arduino Nicla Vision — 22.9 × 22.9 mm (₹9089).** The smallest board with
   **WiFi + IMU together** (NINA-W102 + LSM6DSOX). Costly and it carries a
   camera you don't need.
4. **Waveshare ESP32-S3 + QMI8658C (₹1189, OOS).** ESP32-S3 + WiFi + IMU on one
   small board, cheap. Worth watching for restock.
5. **M5Stack M5StickS3 (₹3779, in stock).** ESP32-S3 + WiFi + IMU, but ~48 ×
   24 mm with a display and a cell — the *anti*-small option.

So: if "small" beats "integrated", option 1. If "integrated" beats "small",
option 3 (WiFi) or option 2 (BLE, and lighter/cheaper).

## Driver stage — best in stock

| Role | Part | Why | Robu SKU | Price | Stock |
|---|---|---|---|---|---|
| MOSFET | **SI2300** | 20 V / 6 A, **27 mΩ @ 4.5 V** — best logic-level for a 3.3 V gate | R248300 | ₹3.08 | In stock |
| MOSFET (alt) | AO3400 | 30 V / 5.8 A, 30 mΩ @ 10 V | R248310 | ₹3.08 | In stock |
| MOSFET (cheap) | SI2302 | 20 V / 2.8 A, 55 mΩ @ 4.5 V | R248316 | ₹1.49 | In stock |
| Flyback | **SS34** (JSCJ) | 40 V / 3 A SMA, headroom for 720/8520 | R221237 | ₹2.18 | In stock |
| Flyback (alt) | SS24FL KEXIN | 40 V / 2 A SOD-123FL | R194451 | ₹3.46 | In stock |

The BOM's own `DMN2058U` (35 mΩ @ 10 V, ₹10) is fine but worse value than
SI2300 for a 1S, 3.3 V-gate design.

## Discrete IMU reality check

`ICM-42688-P`, `BMI270` and `LSM6DSO32` — the IMUs worth having — are **all out
of stock on Robu**. The only in-stock discrete IMU is the **MPU6050 module**
(₹444). That is the whole reason to take an integrated board or to place a bare
IMU on your own carrier while it is in stock.

## Suggested split (smallest build)

- Compute: **XIAO ESP32S3 (21 × 17.8 mm)** + **LSM6DSO32 / BMI270 / ICM-42688-P**
  (2.5 × 3 mm) on the carrier — or **Nicla Sense ME (2 g)** if you want it
  factory-packaged and BLE is enough.
- Motor stage: 4× SI2300 + 4× SS34 + 10 Ω gate resistors + 10 k pull-downs.
- Motors: 7 × 20 mm (720) coreless + 65 mm props.
- Power: 1S LiPo 600–1000 mAh, charged off-board.
