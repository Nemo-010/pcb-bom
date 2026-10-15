#!/usr/bin/env python3
"""Write bom-robu-weight-budget.xlsx from the CSV, with live formulas.

No openpyxl available in the sandbox, so this emits the OOXML zip by hand:
[Content_Types].xml, _rels, xl/workbook.xml, xl/styles.xml and one sheet XML
per worksheet. Formula cells get a cached value so plain viewers show a number
and Excel/Sheets recalc on open.
"""
import csv, os, zipfile
from xml.sax.saxutils import escape

OUT = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(OUT, "bom-robu-weight-budget.csv")
XLSX = os.path.join(OUT, "bom-robu-weight-budget.xlsx")

def col(n):
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s

def cell_xml(ref, val, style=None):
    s = f' s="{style}"' if style else ""
    if isinstance(val, str) and val.startswith("="):
        f = escape(val[1:])
        cached = CACHE.get(ref, "")
        v = f"<v>{cached}</v>" if cached != "" else ""
        return f'<c r="{ref}"{s}><f>{f}</f>{v}</c>'
    if isinstance(val, (int, float)) and not isinstance(val, bool):
        return f'<c r="{ref}"{s}><v>{val}</v></c>'
    if val is None or val == "":
        return f'<c r="{ref}"{s}/>'
    return f'<c r="{ref}"{s} t="inlineStr"><is><t xml:space="preserve">{escape(str(val))}</t></is></c>'

def sheet_xml(rows):
    out = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
           '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>']
    for ri, row in enumerate(rows, 1):
        cells = "".join(cell_xml(f"{col(ci)}{ri}", v, 1 if ri == 1 else None)
                        for ci, v in enumerate(row, 1))
        out.append(f'<row r="{ri}">{cells}</row>')
    out.append("</sheetData></worksheet>")
    return "".join(out)

# cached values for the formulas (Excel/Sheets recalc on open)
CACHE = {
    "H21": 15,        # 600 mAh * 0.025 g/mAh
    "H25": 37.447,    # AUW
    "H31": 2.9908,    # T/W
    "H32": 11.2341,   # hover W
    "H33": 9.4854,    # hover min
    "H34": 6.3236,    # mixed min
}
BUDGET_CACHE = {"B2": 1761, "B3": 1761, "B4": 39.547}

# ---- BOM sheet straight from the CSV, H21 added as a battery-weight formula
bom = []
with open(CSV, newline="") as f:
    for r in csv.reader(f):
        bom.append(list(r))
def find(ref):
    return int("".join(c for c in ref if c.isdigit())), ord(ref[0]) - 64
r21, c21 = find("H21")
bom[r21 - 1][c21 - 1] = "=E21*E22"

rates = [["Category", "INR per gram"],
         ["Buzzer", 50], ["Capacitor", 120], ["Diode", 80], ["Connector", 40],
         ["SolderPad", 0], ["MOSFET", 200], ["Resistor", 30],
         ["nRF52840 (Seeed XIAO)", 60], ["Carrier PCB", 40], ["Battery", 25],
         ["Motor", 150], ["Propeller", 300], ["Custom part (assumed)", 100],
         ["<cat>", 1]]

budget = [["Total budget (INR)", "=BOM!E35"],
          ["Remaining budget (Google Sheets)",
           "=BOM!E35-SUMPRODUCT(BOM!G2:G100,ARRAYFORMULA(IFERROR(VLOOKUP(BOM!C2:C100,Rates!$A$2:$B$100,2,FALSE),0)))"],
          ["Remaining budget (Excel)",
           "=BOM!E35-SUMPRODUCT(SUMIF(Rates!$A$2:$A$100,BOM!$C$2:$C$100,Rates!$B$2:$B$100),BOM!$G$2:$G$100)"],
          ["Total weight (g)", "=SUM(BOM!H2:H100)"]]
# fold the budget cached values in
for i, (a, b) in enumerate(budget, 1):
    if isinstance(b, str) and b.startswith("="):
        CACHE.setdefault(f"B{i}", BUDGET_CACHE.get(f"B{i}", ""))

CT = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' \
 '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">' \
 '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>' \
 '<Default Extension="xml" ContentType="application/xml"/>' \
 '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>' \
 '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' \
 '<Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' \
 '<Override PartName="/xl/worksheets/sheet3.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' \
 '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>' \
 '</Types>'

RELS = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' \
 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' \
 '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>' \
 '</Relationships>'

WB = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' \
 '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" ' \
 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>' \
 '<sheet name="BOM" sheetId="1" r:id="rId1"/>' \
 '<sheet name="Rates" sheetId="2" r:id="rId2"/>' \
 '<sheet name="Budget" sheetId="3" r:id="rId3"/>' \
 '</sheets></workbook>'

WBRELS = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' \
 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' \
 '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>' \
 '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>' \
 '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet3.xml"/>' \
 '<Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>' \
 '</Relationships>'

STYLES = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' \
 '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">' \
 '<fonts count="2"><font><sz val="11"/><name val="Calibri"/></font>' \
 '<font><b/><sz val="11"/><name val="Calibri"/></font></fonts>' \
 '<fills count="2"><fill><patternFill patternType="none"/></fill>' \
 '<fill><patternFill patternType="gray125"/></fill></fills>' \
 '<borders count="1"><border/></borders>' \
 '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>' \
 '<cellXfs count="2"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>' \
 '<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/></cellXfs>' \
 '</styleSheet>'

with zipfile.ZipFile(XLSX, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", CT)
    z.writestr("_rels/.rels", RELS)
    z.writestr("xl/workbook.xml", WB)
    z.writestr("xl/_rels/workbook.xml.rels", WBRELS)
    z.writestr("xl/styles.xml", STYLES)
    z.writestr("xl/worksheets/sheet1.xml", sheet_xml(bom))
    z.writestr("xl/worksheets/sheet2.xml", sheet_xml(rates))
    z.writestr("xl/worksheets/sheet3.xml", sheet_xml(budget))

print("wrote", XLSX, os.path.getsize(XLSX), "bytes")
