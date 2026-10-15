#!/usr/bin/env python3
"""Emit bom-robu-weight-budget.csv with a *dynamic* battery-weight calculation.

Layout (1-based rows, columns A..N):
  row 1        headers
  rows 2-10    9 component lines (as bom-robu.csv) + weights
  row 11       Seeed XIAO nRF52840 module
  row 12       carrier PCB
  rows 13-18   blank gap
  row 19       PLACEHOLDER
  row 20       ASSUMED example
  row 21       battery capacity input (mAh)
  row 22       battery weight element (g/mAh)
  row 23       motor input
  row 24       propeller input
  row 25       CALC total flying weight (AUW)
  rows 26-30   motor / electrical parameters
  rows 31-34   CALC thrust-weight, hover power, flight time
  row 35       budget input

Cells that start with "=" are live Google Sheets formulas on import.
"""
import csv, os

OUT = os.path.dirname(os.path.abspath(__file__))
R = "https://robu-prod-media.s3.ap-south-1.amazonaws.com/uploads"

H = ["Section","Reference","Category","Qty","Value","Footprint",
     "Unit_Weight_g","Total_Weight_g","Weight_Source",
     "Robu_SKU","Unit_Price_INR","Availability","Datasheet","Notes"]

rows = [
 # rows 2-10: components
 ["COMPONENT","BZ1","Buzzer",1,"Buzzer","Buzzer_5020 (5x2mm SMD)",0.15,0.15,
  "typical 5x2mm SMD magnetic buzzer","R179638","41.00","In Stock",
  f"{R}/2024/11/buzzer-datasheet.pdf",""],
 ["COMPONENT","C1,C2,C3,C4","Capacitor",4,"10n","0603 MLCC",0.004,0.016,
  "typical 0603 MLCC","594976","0.72","In Stock","",
  "Generic 10nF 0603 pack; no brand datasheet"],
 ["COMPONENT","D1,D2,D3,D4","Diode",4,"SS24L","SOD-123F",0.012,0.048,
  "computed from SOD-123FL body x mold density","R194451","3.46","In Stock",
  f"{R}/2024/12/C489144.pdf","Bought part is SS24FL"],
 ["COMPONENT","D5","Diode",1,"1N4148W","SOD-123",0.010,0.010,
  "Diodes Inc datasheet (0.01 g)","R242981","2.56","In Stock",f"{R}/2025/08/C83528.pdf",""],
 ["COMPONENT","J1","Connector",1,"Conn_01x04_Socket","PinHeader 1x04 P2.54mm (DNP)",0.60,0.60,
  "typical 1x4 2.54mm pin header","R197649","3.31","In Stock",f"{R}/2025/04/DS1021.pdf",
  "DNP - not populated, excluded from AUW"],
 ["COMPONENT","J2,J3,J4,J5,J6,J7,J8,J9,J10,J11","SolderPad",10,"Conn_01x01_Socket",
  "SolderWirePad 1x01 SMD 1x2mm",0.00,0.00,"bare PCB copper, no component","","","n/a","",""],
 ["COMPONENT","Q1,Q2,Q3,Q4,Q5","MOSFET",5,"DMN2058U","SOT-23",0.009,0.045,
  "Diodes Inc datasheet (0.009 g)","R246407","10.00","In Stock",f"{R}/2025/08/C5245280.pdf",""],
 ["COMPONENT","R1,R4,R6,R8,R10","Resistor",5,"10k","0603",0.002,0.010,
  "Vishay CRCW0603 MASS = 2 mg","R232165","0.83","In Stock",
  f"{R}/2025/07/2506161050_YAGEO-RC0402FR-07220RP_C7038454.pdf",""],
 ["COMPONENT","R2,R3,R5,R7","Resistor",4,"10","0603",0.002,0.008,
  "Vishay CRCW0603 MASS = 2 mg","R178890","0.08","In Stock",f"{R}/2024/11/C163851.pdf",""],
 # rows 11-12: modules
 ["MODULE","U7","nRF52840 (Seeed XIAO)",1,"Seeed Studio XIAO BLE nRF52840","21 x 17.8 mm",8.0,8.0,
  "Robu shipping weight 0.008 kg (board ~3 g)","1201741","1244.00","Out of Stock","",""], 
 ["PCB","PCB1","Carrier PCB",1,"27x27mm 1.6mm FR4","2-layer, 14 XIAO pin holes + 8x M2",2.16,2.16,
  "computed: 2.7*2.7*0.16 cm3 x 1.85 g/cm3","","","n/a","",
  "14 XIAO pin holes + 8 extra = 22 holes"],
 # rows 13-18: blank gap
 *[[""]*len(H) for _ in range(6)],
 # row 19: placeholder
 ["PLACEHOLDER","<REF>","<cat>",1,"<value>","<footprint>","","<weight_g>","<source>","","","","",
  "Fill col C (category) and col G (weight); formulas pick rows up by C and G"],
 # row 20: assumed example
 ["ASSUMED","U99","Custom part (assumed)",1,"ASSUMED-VALUE","ASSUMED-FOOTPRINT",1.50,1.50,"assumed",
  "","","","","Example with assumed values; not counted in AUW until you move it up"],
 # row 21: battery capacity input
 ["INPUT","BAT1","Battery capacity",1,600,"mAh 1S LiPo","","","input: capacity in mAh","","","n/a","",
  "Change E21 to any capacity; battery weight and AUW recompute"],
 # row 22: battery weight element
 ["PARAM","BAT_ELEM","Battery weight element",1,0.025,"g/mAh",0.025,0.025,
  "~150 Wh/kg at 3.7V -> 0.025 g/mAh","","","n/a","","Battery weight = E21 * E22"],
 # row 23: motor
 ["INPUT","MOT1","Motor",4,"7x20 coreless (720)","coreless brushed",2.5,10.0,"vendor typical",
  "","","n/a","","Per-motor weight 2.5 g"],
 # row 24: propeller
 ["INPUT","PROP1","Propeller",4,"65mm 2-blade","micro drone prop",0.5,2.0,"typical","","","n/a","",""],
 # row 25: AUW (formula)
 ["CALC","AUW","Total flying weight",1,"AUW (g)","","","=H2+H3+H4+H6+H7+H8+H9+H10+H11+H12+H23+H24+(E21*E22)",
  "computed: components (no DNP) + module + PCB + motors + props + battery","","","n/a","",
  "Excludes J1 (DNP) and the ASSUMED row; add a frame/wire row if needed"],
 # rows 26-30: params
 ["PARAM","MOT_TMAX","Motor max thrust",1,28,"g","","","vendor typical","","","n/a","","720 + 65mm prop"],
 ["PARAM","MOT_IMAX","Motor max current",1,1.7,"A","","","vendor typical","","","n/a","",""],
 ["PARAM","P_HOVER","Hover specific power",1,0.30,"W/g","","","micro-quad typical 0.25-0.35 W/g","","","n/a","",""],
 ["PARAM","V_NOM","Battery nominal voltage",1,3.7,"V","","","1S LiPo","","","n/a","",""],
 ["PARAM","DOD","Usable depth of discharge",1,0.8,"","","","leave 20% in the pack","","","n/a","",""],
 # rows 31-34: calculations
 ["CALC","TW","Thrust / weight","","x","","","=4*E26/H25","=4 motors x max thrust / AUW","","","n/a","",""],
 ["CALC","HOVER_P","Hover power",1,"W","","","=H25*E28","=AUW x specific power","","","n/a","",""],
 ["CALC","FLY_HOVER","Flight time (hover)",1,"min","","","=E21/1000*E29*E30/H32*60","=mAh/1000 x V x DoD / hover power x 60","","","n/a","",""],
 ["CALC","FLY_MIXED","Flight time (mixed)",1,"min","","","=H33/1.5","hover / 1.5 for normal flying","","","n/a","",""],
 # row 35: budget
 ["INPUT","BUDGET","Budget",1,5000,"INR","","","input","","","n/a","","Cell E35 = total budget (kept out of the price column so it is not counted as a cost)"],
]

with open(f"{OUT}/bom-robu-weight-budget.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(H)
    for r in rows:
        w.writerow(r)

# sanity: replicate the sheet maths outside Sheets
comp = sum(float(r[7]) for r in rows[:9])
auw = comp - 0.60  # drop DNP J1
auw += 8.0 + 2.16 + 4*2.5 + 4*0.5 + 600*0.025
hover_p = auw*0.30
fly_hover = (600/1000*3.7*0.8)/hover_p*60
print("component weight: %.3f g (with J1) / %.3f g (without DNP)" % (comp, comp-0.60))
print("AUW (600 mAh): %.2f g | T/W: %.2f | hover power: %.2f W" % (auw, 4*28/auw, hover_p))
print("flight time: hover %.1f min | mixed %.1f min" % (fly_hover, fly_hover/1.5))
for cap in (600, 1000):
    a = comp-0.60 + 8.0 + 2.16 + 4*2.5 + 4*0.5 + cap*0.025
    h = (cap/1000*3.7*0.8)/(a*0.30)*60
    print("  %4d mAh -> AUW %.1f g, hover %.1f min, mixed %.1f min" % (cap, a, h, h/1.5))
