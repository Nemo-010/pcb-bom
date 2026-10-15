# Redone board — Robu-only BOM

Sourcing sheet for the BOM pasted in the thread, restricted to
[Robu.in](https://robu.in) only. Price and availability were read from each
Robu product page (the live "Availability:" field) on **2026-10-08**.

- Output: [`bom-robu.csv`](bom-robu.csv) — 9 BOM lines, one chosen Robu part per line
- No-exact-match list: [`not-found-exact.csv`](not-found-exact.csv)

## Availability at a glance

| Match | Lines |
|---|---|
| Exact match, in stock | 7 |
| Nearest part only — **not exact** | 1 (`D1–D4` SS24L) |
| No component to buy | 1 (`J2–J11` bare solder pads) |

In-stock subtotal (unit price × qty): **₹114.75**. This excludes `J1`, which is
marked **DNP** in the BOM, and the `J2–J11` solder pads (no part).

## Parts with no exact match on Robu

Searched by exact MPN / value+package and checked the product page, not just
the search result.

| Ref | BOM part | Status |
|---|---|---|
| `D1–D4` | `SS24L`, footprint `D_SOD-123F` | **Exact MPN not orderable.** The only `SS24L` on Robu is HXY (R241435) and it is **Out of Stock**; Vishay `SS24L` is not stocked at all. The in-stock substitute is `SS24FL` KEXIN (R194451, ₹3.46) — same SOD-123F/FL, 40 V, 2 A Schottky. [datasheet](https://robu-prod-media.s3.ap-south-1.amazonaws.com/uploads/2024/12/C489144.pdf) — original ref was the [Vishay SS32 sheet](https://www.vishay.com/docs/88751/ss32.pdf). |
| `J2–J11` | `Conn_01x01_Socket`, footprint `SolderWirePad_1x01_SMD_1x2mm` | **No component to buy.** Ten bare 1×2 mm exposed SMD solder pads on the PCB for soldering wires to — board copper, not a purchased part, so there is nothing to source on Robu. |

## Datasheet links

Every line carries a `Datasheet` link except the two with nothing to document:

- `C1–C4` is a generic "10nF 0603" pack with no brand datasheet; every branded
  10nF 0603 on Robu (`R183944`, `R183959`, `R183991`) is currently **Out of
  Stock**, so the generic pack is the only in-stock exact option.
- `J2–J11` is bare PCB copper.
- Everything else links the datasheet attached to the exact Robu product page.
  Note the source BOM's Vishay `1N4148W` link is dead (404); the Diodes Inc
  part datasheet is used instead.

## Notes on availability

- `D5` **1N4148W**: Diodes Inc `1N4148W-7-F` (R242981, ₹2.56) in stock. Cheaper generic `1N4148W` (R662953, ₹0.91) and Slkor (R193213) also in stock.
- `Q1–Q5` **DMN2058U**: the `DMN2058U-7` reel (R231156) went Out of Stock; the `DMN2058U-13` variant (R246407, ₹10) is in stock, same part in SOT-23.
- `J1` **2.54 mm 1×4 header** is in stock (CONNFLY DS1021, R197649, ₹3.31) but is DNP, so it is not in the subtotal.
- `R2,R3,R5,R7` **10 Ω 0603**: the Yageo options (`R137893`, `R143616`) are Out of Stock; the Walsin `WR06X10R0FTL` (R178890, ₹0.08) is in stock.
- `R1,R4,R6,R8,R10` **10k 0603**: Yageo `RC0603JR-0710KP` (R232165, ₹0.83) in stock.

## Lead time

Robu does not publish a lead time. Each product page offers only a
"Check estimated delivery" widget that needs a delivery pincode; there is no
ships-in / restock / ETA field, including on out-of-stock items. So the
`Lead_Time` column is `Not published` throughout, and Out of Stock parts have
no announced restock date. If lead time matters, Robu's support/B2B channel
(`sales@robu.in`) is the only place to ask.

## Method

1. Parsed the pasted KiCad BOM (9 lines).
2. Searched robu.in per part (exact MPN, then value + package) via the
   rendered site.
3. Opened each chosen product page and recorded the live `Availability:`
   field, price, SKU, MPN and attached datasheet. Search-result badges were
   **not** trusted — several disagreed with the product page (in both
   directions).
4. Marked a line `exact` only when the MPN (or value + package) matched.

Regenerate with `gen_bom.py` (edit the table, re-run) — the checked numbers
are baked into that file as of the date above.

---

# Weights, modules and budget

`bom-robu-weight-budget.csv` is the same 9-line component list as
`bom-robu.csv`, with a **weight per component**, plus an nRF52840 module, a
27 × 27 mm carrier PCB, a placeholder row, an assumed-values row, and a second
input set (battery, motor, propeller, budget). Component rows are as checked
2026-10-08; the module / motor additions were checked 2026-10-14.

## Weight column

| Ref | Part | Unit weight | Source |
|---|---|---|---|
| BZ1 | CL5020A 5×2 mm buzzer | 0.15 g | typical for a 5×2 mm SMD magnetic buzzer |
| C1–C4 | 0603 MLCC | 0.004 g | typical 0603 MLCC (BaTiO3 body + terminations) |
| D1–D4 | SS24FL SOD-123FL | 0.012 g | computed from body dimensions × mold density |
| D5 | 1N4148W SOD-123 | 0.010 g | Diodes Inc datasheet, "Weight: 0.01 grams (Approximate)" |
| J1 | 1×4 2.54 mm header | 0.60 g | typical through-hole header |
| J2–J11 | solder pads | 0.00 g | bare PCB copper |
| Q1–Q5 | DMN2058U SOT-23 | 0.009 g | Diodes Inc datasheet, "Weight: 0.009 grams (Approximate)" |
| R (all) | 0603 resistor | 0.002 g | Vishay CRCW0603 datasheet, MASS = 2 mg |
| U7 | XIAO nRF52840 | 8.00 g | Robu shipping weight 0.008 kg (board itself ≈ 3 g) |
| PCB1 | 27 × 27 × 1.6 mm FR4 | 2.16 g | 2.7 × 2.7 × 0.16 cm³ × 1.85 g/cm³ |

All 9 passive/board components together weigh **0.887 g**; the build weight is
dominated by the module and the battery.

## New rows

- **U7 — Seeed Studio XIAO nRF52840** (Robu SKU 1201741). Robu lists **Shipping
  Weight 0.008 kg**; it is **Out of Stock** as of 2026-10-14. Board size
  21 × 17.8 mm. The XIAO is a castellated solder-down module: the KiCad/DXF
  files show **no mounting holes of its own**, only the 14 castellated pads.
- **PCB1 — carrier PCB**, 27 × 27 mm, 1.6 mm FR4, 2-layer. Holes: **14 pin
  holes for the XIAO + 8 extra = 22 total** (the "same as the nRF needs plus
  8 more" rule). If you meant 8 mounting holes total, change the row.
- **PLACEHOLDER** row — put a category in column C and a weight in column G and
  the budget formula below picks it up.
- **ASSUMED** row — one worked example using assumed values.

## Second input set

| Key | Value | Notes |
|---|---|---|
| Battery | 1000 mAh 1S LiPo | 3.7 V nominal, 4.2 V full, ≈28 g, ≈3.7 Wh |
| Motor | 7×20 mm coreless (720) ×4 | ≈2.5 g each, ≈2 A max, ≈28 g thrust each on a 65 mm prop |
| Propeller | 65 mm 2-blade ×4 | ≈0.5 g each |
| Budget | ₹5000 | placeholder total |

## Google Sheets remaining-budget formula

Lay the CSV out with **column C = category** and **column G = unit weight**.
Add a `Rates` sheet mapping a category to a cost per gram in ₹:

```
Rates!A1:B      A = category, B = INR per gram
Buzzer          50
Capacitor       120
Diode           80
...
```

Then, with the total budget in `B1`, the remaining budget is:

```
=B1 - SUMPRODUCT(G2:G100, ARRAYFORMULA(IFERROR(VLOOKUP(C2:C100, Rates!$A$2:$B$100, 2, FALSE), 0)))
```

If instead each category has a flat cost (not per gram):

```
=B1 - SUMPRODUCT((C2:C100<>"") * IFERROR(VLOOKUP(C2:C100, Rates!$A$2:$B$100, 2, FALSE), 0))
```

And if you keep a per-row cost column (say column L = `=H2*rate`), it is simply:

```
=B1 - SUM(L2:L100)
```

## Motor selection (for the brushed-motor device)

The board drives 4 brushed channels (Q1–Q4 + SS24L flyback) plus a 5th channel
(Q5 + D5). With a 1000 mAh 1S LiPo, the practical coreless-motor options are:

| Motor | Size | Weight | Thrust each (55–65 mm prop) | Max current | Verdict |
|---|---|---|---|---|---|
| 615 | 6×15 mm | ≈1.2 g | 13–18 g | ≈1.0–1.3 A | smallest; needs a ≤400 mAh pack |
| 716 | 7×16 mm | ≈1.9 g | 18–22 g | ≈1.4 A | light option |
| **720** | **7×20 mm** | **≈2.5 g** | **25–32 g** | **≈1.6–2 A** | **best balance, fits the 2 A SS24L** |
| 816 | 8×16 mm | ≈2.8 g | 28–34 g | ≈2 A | close to 8520 thrust, in stock |
| 8520 | 8.5×20 mm | ≈3.6 g | 35–45 g | ≈2.5–3 A | max lift; exceeds the 2 A flyback at full throttle |

Live Indian stock checked 2026-10-14: Robu and Robocraze coreless motors are
**Out of Stock**; **[QuartzComponents](https://quartzcomponents.com)** has the
[720 + 55 mm prop](https://quartzcomponents.com/products/720-magnetic-micro-coreless-drone-motor-with-55mm-propeller)
(₹46), [716 + 55 mm prop](https://quartzcomponents.com/products/716-magnetic-micro-coreless-motor-with-55mm-propeller)
(₹50), [816](https://quartzcomponents.com/products/816-magnetic-micro-coreless-drone-motor-cw)
(₹48) and [612](https://quartzcomponents.com/products/612-magnetic-micro-coreless-drone-motor)
(₹30) in stock. Robu's coreless category and Robocraze's coreless listings were
Out of Stock at the same check.

## Dynamic battery weight, AUW and flight time

The battery weight is **computed**, not hard-coded, from its capacity and a
weight element (grams per mAh):

```
Battery_Weight_g = capacity_mAh * weight_element_g_per_mAh
```

- `E21` = capacity in mAh (default **600**)
- `E22` = weight element in g/mAh (default **0.025**, i.e. ≈150 Wh/kg at 3.7 V)
- `H21` = `=E21*E22`

Everything downstream is live, so changing `E21` re-does the whole sheet:

| Cell | Meaning | Formula |
|---|---|---|
| `H25` | total flying weight (AUW), J1/DNP excluded | `=H2+H3+H4+H6+H7+H8+H9+H10+H11+H12+H23+H24+(E21*E22)` |
| `H31` | thrust / weight | `=4*E26/H25` |
| `H32` | hover power (W) | `=H25*E28` |
| `H33` | hover time (min) | `=E21/1000*E29*E30/H32*60` |
| `H34` | mixed-flight time (min) | `=H33/1.5` |

Parameters: `E26` motor max thrust = 28 g, `E27` motor max current = 1.7 A,
`E28` hover specific power = 0.30 W/g, `E29` cell voltage = 3.7 V,
`E30` usable depth of discharge = 0.8.

### 600 mAh + 7×20 (720) result

| Capacity | AUW | T/W | Hover time | Mixed flying |
|---|---|---|---|---|
| **600 mAh** | ≈37.4 g | 3.0 | **≈9.5 min** | **≈6.3 min** |
| 1000 mAh | ≈47.4 g | 2.4 | ≈12.5 min | ≈8.3 min |

Notes: this is with 65 mm props and a hover specific power of 0.30 W/g. Add a
frame/wire/connector row (use the PLACEHOLDER row) and AUW rises and time
falls. A 600 mAh 25C pack supplies 15 A, and the four 720s pull ≈6.8 A at full
throttle, so the pack is fine; the SS24L 2 A flyback is the thing to watch at
full stick.

## Getting this into a Google Sheet

This repo can't create a Google Sheet for you (no Google credentials are
available here). Two ways to get one, both fully in your account:

**A. Build it with Apps Script (recommended, gives live formulas).**

1. Open <https://script.google.com> → **New project**.
2. Paste [`build-google-sheet.gs`](build-google-sheet.gs).
3. Set `SHARE_WITH` to your Google address (or leave `""` for private).
4. Run `buildBomSheet` and approve the prompt. The log prints the sheet URL.

It pulls this repo's CSV, writes the BOM with the formula cells live, adds a
`Rates` sheet (category → ₹/g) and a `Budget` sheet with the remaining-budget
and total-weight formulas.

**B. Import the CSV by hand.**

1. Open <https://sheets.new> → **File → Import → Upload**.
2. Pick `bom-robu-weight-budget.csv`; import as a new sheet.
3. Add a `Rates` sheet (`Category`, `INR per gram`) and put in `Budget!B2`:
   `=BOM!E35 - SUMPRODUCT(BOM!G2:G100, ARRAYFORMULA(IFERROR(VLOOKUP(BOM!C2:C100, Rates!$A$2:$B$100, 2, FALSE), 0)))`

**C. Open the XLSX instead.**

[`bom-robu-weight-budget.xlsx`](bom-robu-weight-budget.xlsx) is the same
workbook: a `BOM` sheet (formulas live, cached values so it shows numbers
immediately), a `Rates` sheet, and a `Budget` sheet with the remaining-budget
formula in both the Google Sheets (`ARRAYFORMULA`) and Excel (`SUMPRODUCT` +
`SUMIF`) forms. Upload it to Drive, or open it in Excel directly. It is
generated by `gen_xlsx.py` (hand-rolled OOXML, since the sandbox has no
openpyxl).
