#!/usr/bin/env python3
"""Emit bom-robu-weight-budget.csv.

Same component data as bom-robu.csv, plus:
  * a weight per component and a weight source,
  * an nRF52840 Seeed XIAO module row,
  * a 27x27 mm 1.6 mm FR4 carrier PCB row,
  * a placeholder row + an assumed-values row, after a gap,
  * a second input set (battery, motor, prop, budget).
"""
import csv, os

OUT = os.path.dirname(os.path.abspath(__file__))
R = "https://robu-prod-media.s3.ap-south-1.amazonaws.com/uploads"

H = ["Section","Reference","Category","Qty","Value","Footprint",
     "Unit_Weight_g","Total_Weight_g","Weight_Source",
     "Robu_SKU","Unit_Price_INR","Availability","Datasheet","Notes"]

rows = [
 # ---------------- component table (same data as bom-robu.csv, + weights) ----------------
 ["COMPONENT","BZ1","Buzzer",1,"Buzzer","Buzzer_5020 (5x2mm SMD)",0.15,0.15,
  "typical 5x2mm SMD magnetic buzzer","R179638","41.00","In Stock",f"{R}/2024/11/buzzer-datasheet.pdf",""],
 ["COMPONENT","C1,C2,C3,C4","Capacitor",4,"10n","0603 MLCC",0.004,0.016,
  "typical 0603 MLCC (BaTiO3 body + terminations)","594976","0.72","In Stock","","Generic 10nF 0603 pack; no brand datasheet"],
 ["COMPONENT","D1,D2,D3,D4","Diode",4,"SS24L","SOD-123F",0.012,0.048,
  "computed from SOD-123FL body x mold density","R194451","3.46","In Stock",f"{R}/2024/12/C489144.pdf",
  "Bought part is SS24FL (exact SS24L is Out of Stock)"],
 ["COMPONENT","D5","Diode",1,"1N4148W","SOD-123",0.010,0.010,
  "Diodes Inc datasheet (Weight: 0.01 g)","R242981","2.56","In Stock",f"{R}/2025/08/C83528.pdf",""],
 ["COMPONENT","J1","Connector",1,"Conn_01x04_Socket","PinHeader 1x04 P2.54mm Vertical (DNP)",0.60,0.60,
  "typical 1x4 2.54mm pin header","R197649","3.31","In Stock",f"{R}/2025/04/DS1021.pdf","DNP - not populated"],
 ["COMPONENT","J2,J3,J4,J5,J6,J7,J8,J9,J10,J11","SolderPad",10,"Conn_01x01_Socket",
  "SolderWirePad 1x01 SMD 1x2mm",0.00,0.00,"bare PCB copper, no component","","","n/a","",
  "Board copper for soldering wires; nothing to buy"],
 ["COMPONENT","Q1,Q2,Q3,Q4,Q5","MOSFET",5,"DMN2058U","SOT-23",0.009,0.045,
  "Diodes Inc datasheet (Weight: 0.009 g)","R246407","10.00","In Stock",f"{R}/2025/08/C5245280.pdf",""],
 ["COMPONENT","R1,R4,R6,R8,R10","Resistor",5,"10k","0603",0.002,0.010,
  "Vishay CRCW0603 datasheet (MASS = 2 mg)","R232165","0.83","In Stock",
  f"{R}/2025/07/2506161050_YAGEO-RC0402FR-07220RP_C7038454.pdf",""],
 ["COMPONENT","R2,R3,R5,R7","Resistor",4,"10","0603",0.002,0.008,
  "Vishay CRCW0603 datasheet (MASS = 2 mg)","R178890","0.08","In Stock",f"{R}/2024/11/C163851.pdf",""],
]

gap = [[""]*len(H) for _ in range(6)]

tail = [
 ["MODULE","U7","nRF52840 (Seeed XIAO)",1,"Seeed Studio XIAO BLE nRF52840","21 x 17.8 mm",8.0,8.0,
  "Robu shipping weight 0.008 kg (with packaging)","1201741","1244.00","Out of Stock","",
  "Board is ~3 g; Robu lists 8 g shipping weight. Nothing as light as the bare nRF52840 SoC."],
 ["PCB","PCB1","Carrier PCB",1,"27x27mm 1.6mm FR4","2-layer, 14 XIAO pin holes + 8x M2 mount holes",
  2.16,2.16,"computed: 2.7 x 2.7 x 0.16 cm3 x 1.85 g/cm3","","","n/a","",
  "14 pin holes (XIAO has 14 castellated pads, no mounting holes of its own) + 8 extra = 22 holes. Adjust if you meant 8 total."],
 ["PLACEHOLDER","<REF>","<cat>",1,"<value>","<footprint>","","","<source>","","","","",
  "Fill col C (category) and col G (weight); the budget formula picks up rows by category in col C."],
 ["ASSUMED","U99","Custom part (assumed)",1,"ASSUMED-VALUE","ASSUMED-FOOTPRINT",1.50,1.50,"assumed",
  "","","","","Example row with assumed values, replace before use."],
 ["INPUT","BAT1","Battery",1,"1000mAh 1S LiPo","LiPo pouch",28.0,28.0,"typical 1S 1000mAh 25C","","","n/a","",
  "3.7V nominal / 4.2V full / ~28 g / ~3.7 Wh; usable ~800 mAh at 80% DoD"],
 ["INPUT","MOT1","Motor",4,"7x20 coreless (720)","coreless brushed",2.5,10.0,"vendor typical","","","n/a","",
  "3.7V, ~48000 rpm, ~1.5-2 A max, ~28 g thrust each with 65mm prop"],
 ["INPUT","PROP1","Propeller",4,"65mm 2-blade","micro drone prop",0.5,2.0,"typical","","","n/a","",""],
 ["INPUT","BUDGET","Budget",1,"Total build budget (INR)","", "","","","","5000","n/a","",
  "Put your total here; see README for the remaining-budget formula."],
]

with open(f"{OUT}/bom-robu-weight-budget.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(H)
    for r in rows: w.writerow(r)
    for r in gap: w.writerow(r)
    for r in tail: w.writerow(r)

comp = [r for r in rows if r[0]=="COMPONENT"]
print("component rows:", len(comp), "| total component weight: %.3f g" %
      sum(r[7] for r in comp))
print("all rows:", len(rows)+len(gap)+len(tail))
