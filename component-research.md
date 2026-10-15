# Component research — integrated MCU + WiFi + IMU

For the brushed-motor board: the goal is a **single module that already carries
MCU + WiFi + IMU**, so the custom board is only the motor-driver stage
(MOSFETs + flyback diodes + gate resistors). Robu.in stock checked
**2026-10-14** from the live product pages (search badges were ignored — they
disagreed with the pages repeatedly).

## Fully integrated WiFi + IMU modules on Robu

| Board | MCU | Radio | IMU | Robu SKU | Price | Stock |
|---|---|---|---|---|---|---|
| **Arduino Nano 33 IoT** | SAMD21 M0+ 48 MHz | NINA-W102 WiFi + BLE | **LSM6DS3** + ATECC608A | 957158 | ₹2709 | **In stock** |
| **M5Stack M5StickS3 (K150)** | ESP32-S3 240 MHz | 2.4 GHz WiFi + BLE | **6-axis IMU** (unnamed) | R261340 | ₹3779 | **In stock** |
| Wio Terminal | ATSAMD51 M4F 120 MHz | RTL8720DN WiFi + BLE | **LSM6DSL** | 758019 | ₹4099 | **In stock** |
| M5Stack Stopwatch Dev Kit | ESP32-S3 | WiFi | **BMI270** | R268137 | ₹7289 | **In stock** |
| M5Stack CoreS3 | ESP32-S3 | WiFi | BMI270 + BMM150 | 1850175 | ₹7759 | Out of stock |
| Arduino Nano RP2040 Connect | RP2040 | NINA-W102 WiFi + BLE | LSM6DSOX | 987958 | ₹1829 | Out of stock |
| Seeed XIAO ESP32S3 | ESP32-S3 | WiFi + BLE 5 | none | 1569230 | ₹1139 | Out of stock |
| Seeed XIAO nRF52840 Sense | nRF52840 | BLE only | LSM6DS3TR-C | — | — | Out of stock |
| Arduino Nano 33 BLE Sense Rev2 | nRF52840 | BLE only | BMI270 + BMM150 | 917384 | ₹4379 | In stock (no WiFi) |

### Pick

1. **Arduino Nano 33 IoT (₹2709, in stock)** — the sweet spot. WiFi + 6-axis
   IMU + secure element on one Nano-form board (~5 g), 2.54 mm/castellated
   pins, 11 PWM. You only add the MOSFET stage. SAMD21 is modest but plenty for
   a brushed-flight-control loop.
2. **M5Stack M5StickS3 (₹3779, in stock)** — if you specifically want
   **ESP32-S3** (WiFi + BLE 5, 240 MHz). It is a stick dev-kit with a display
   and 120 mAh cell, so ~29 g and not a bare module.
3. **Wio Terminal (₹4099, in stock)** — ATSAMD51 + WiFi + LSM6DSL, but 72×57 mm
   and 130 g shipping; too big for a micro quad, fine for a bench rig.
4. The exact XIAO combination you wanted — **XIAO ESP32S3 (WiFi) + a separate
   IMU** — is blocked right now: the XIAO ESP32S3 is out of stock, and so is the
   bare IMU (see below).

## Discrete parts (for the driver stage)

### N-channel MOSFET, SOT-23, logic level

| Part | Vds / Id | Rds(on) | Robu SKU | Price | Stock |
|---|---|---|---|---|---|
| **SI2300** | 20 V / 6 A | **27 mΩ @ 4.5 V** | R248300 | ₹3.08 | In stock |
| AO3400 | 30 V / 5.8 A | 30 mΩ @ 10 V | R248310 | ₹3.08 | In stock |
| SI2302 | 20 V / 2.8 A | 55 mΩ @ 4.5 V | R248316 | ₹1.49 | In stock |
| DMN2058U-13 (current) | 20 V / 4.6 A | 35 mΩ @ 10 V | R246407 | ₹10.00 | In stock |

**SI2300** is the best in-stock logic-level choice (lowest Rds at the 4.5 V
gate the 3.3 V MCU can actually give it). SI2302 if you want the cheapest.

### Schottky flyback diode

| Part | Rating | Package | Robu SKU | Price | Stock |
|---|---|---|---|---|---|
| **SS34** (JSCJ) | 40 V / 3 A | SMA | R221237 | ₹2.18 | In stock |
| SS34 (Slkor) | 40 V / 3 A | SMA | R193154 | ₹3.79 | In stock |
| SS24FL (KEXIN) | 40 V / 2 A | SOD-123FL | R194451 | ₹3.46 | In stock |
| SS24L (exact BOM part) | 40 V / 2 A | SOD-123FL | R241435 | ₹3.54 | Out of stock |

Go **SS34** if you run 720/8520 motors (3 A headroom); SS24FL if you keep 2 A.

### Discrete IMU (only if you don't use an integrated module)

| Part | Notes | Robu SKU | Price | Stock |
|---|---|---|---|---|
| MPU6050 module | 6-axis breakout, just wire I2C | R268095 | ₹444 | In stock |
| LSM6DSO32 | ±32 g, ST, best in-stock *bare* IMU | R263340 | ₹559 | Out of stock |
| ICM-42688-P | best-in-class, BOM original | R184326 | ₹2139 | Out of stock |
| BMI270 | best-in-class | R155006 | ₹599 | Out of stock |
| QMI8658A | cheap 6-axis | R184333 | ₹135 | Out of stock |

The bare IMUs you actually wanted (ICM-42688-P, BMI270, LSM6DSO32) are **all
out of stock on Robu**, and the only in-stock discrete option is the MPU6050
module. That is the strongest argument for taking one of the integrated boards
above and keeping the custom PCB to the motor driver.

## Suggested split

- **Compute/WiFi/IMU:** Arduino Nano 33 IoT (or M5StickS3 for ESP32-S3).
- **Motor stage:** 4× SI2300 + 4× SS34 + 10 Ω gate resistors + 10 k pull-downs,
  driving 7×20 mm (720) coreless motors with 65 mm props.
- **Power:** 1S LiPo (600–1000 mAh), charged off-board (the Nano 33 IoT has no
  charger; the M5StickS3 does).

Everything above was read from the live Robu product pages on 2026-10-14;
stock on Robu turns over fast, so re-check the SKU before ordering.
