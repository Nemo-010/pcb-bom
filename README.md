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
