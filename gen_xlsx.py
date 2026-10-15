#!/usr/bin/env python3
"""Write bom-robu-weight-budget.xlsx from the CSV, with live formulas.

No openpyxl available in the sandbox, so this emits the OOXML zip by hand.
Two sheets: BOM (from the CSV) and Budget. Costs are fixed pack costs, so a
line costs Qty x Unit price (columns D and K); remaining = budget - that sum.
Formula cells get a cached value so plain viewers show a number and
Excel/Sheets recalc on open.
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

CACHE = {}

def cell_xml(ref, val, style=None):
    s = f' s="{style}"' if style else ""
    if isinstance(val, str) and val.startswith("="):
        cached = CACHE.get(ref, "")
        v = f"<v>{cached}</v>" if cached != "" else ""
        return f'<c r="{ref}"{s}><f>{escape(val[1:])}</f>{v}</c>'
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

# ---- BOM sheet from the CSV, with the dynamic battery-weight formula ----
bom = [list(r) for r in csv.reader(open(CSV, newline=""))]
bom[20][7] = "=E21*E22"          # H21 battery weight = capacity * g/mAh element

# ---- Budget sheet: fixed pack costs ----
budget = [["Total budget (INR)", "=BOM!E35"],
          ["BOM cost (INR)", "=SUMPRODUCT(BOM!D2:D100,BOM!K2:K100)"],
          ["Remaining budget (INR)", "=BOM!E35-SUMPRODUCT(BOM!D2:D100,BOM!K2:K100)"],
          ["Total weight (g)", "=SUM(BOM!H2:H100)"]]

# cached values (Excel/Sheets recalc on open)
def num(row, col_idx):
    v = row[col_idx] if col_idx < len(row) else ""
    try: return float(v)
    except (TypeError, ValueError): return 0.0
bom_cost = sum(num(r, 3) * num(r, 10) for r in bom[1:])
CACHE.update({
    "H21": 15, "H25": 37.447, "H31": 2.9908, "H32": 11.2341, "H33": 9.4854, "H34": 6.3236,
    "B2": round(bom_cost, 2), "B3": round(5000 - bom_cost, 2), "B4": 39.547,
})

CT = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' \
 '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">' \
 '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>' \
 '<Default Extension="xml" ContentType="application/xml"/>' \
 '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>' \
 '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' \
 '<Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' \
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
 '<sheet name="Budget" sheetId="2" r:id="rId2"/>' \
 '</sheets></workbook>'

WBRELS = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' \
 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' \
 '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>' \
 '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>' \
 '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>' \
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
    z.writestr("xl/worksheets/sheet2.xml", sheet_xml(budget))

print("wrote", XLSX, os.path.getsize(XLSX), "bytes | BOM cost %.2f, remaining %.2f"
      % (bom_cost, 5000 - bom_cost))
