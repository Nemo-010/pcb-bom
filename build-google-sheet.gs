/**
 * Build the Robu BOM weight/budget Google Sheet.
 *
 * How to use (runs in YOUR Google account, so you own and can share it):
 *   1. Go to https://script.google.com  ->  New project
 *   2. Paste this file in, set SHARE_WITH to your Google address (or "")
 *   3. Run buildBomSheet (top toolbar). Approve the permissions prompt.
 *   4. The execution log prints the spreadsheet URL.
 *
 * It pulls bom-robu-weight-budget.csv from the repo, so re-running after a
 * repo update rebuilds the sheet with the latest numbers.
 */

var REPO_CSV = "https://raw.githubusercontent.com/Nemo-010/pcb-bom/master/bom-robu-weight-budget.csv";
var SHEET_NAME = "pcb-bom weights & budget";

// Set to your Google address to auto-share, e.g. "you@gmail.com". "" = private.
var SHARE_WITH = "";
var SHARE_EDIT = true;

function buildBomSheet() {
  var csv = UrlFetchApp.fetch(REPO_CSV, { muteHttpExceptions: true }).getContentText();
  var data = Utilities.parseCsv(csv);

  var ss = SpreadsheetApp.create(SHEET_NAME);
  var bom = ss.getSheets()[0].setName("BOM");
  bom.getRange(1, 1, data.length, data[0].length).setValues(data);

  // Make the formula cells evaluate (they arrive as text from a CSV import).
  ["H25", "H31", "H32", "H33", "H34"].forEach(function (a1) {
    var r = bom.getRange(a1);
    var v = r.getValue();
    if (typeof v === "string" && v.charAt(0) === "=") r.setFormula(v);
  });
  bom.getRange("H21").setFormula("=E21*E22");        // dynamic battery weight
  bom.getRange("H25").setNumberFormat("0.00");
  bom.getRange("H31:H34").setNumberFormat("0.00");

  // Budget sheet: parts are fixed packs, so line cost = Qty x Unit price (D x K).
  var bud = ss.insertSheet("Budget");
  bud.getRange("A1:B4").setValues([
    ["Total budget (INR)", "=BOM!E35"],
    ["BOM cost (INR)", "=SUMPRODUCT(BOM!D2:D100,BOM!K2:K100)"],
    ["Remaining budget (INR)", "=BOM!E35-SUMPRODUCT(BOM!D2:D100,BOM!K2:K100)"],
    ["Total weight (g)", "=SUM(BOM!H2:H100)"]
  ]);
  bud.setColumnWidth(1, 220);

  if (SHARE_WITH) {
    if (SHARE_EDIT) ss.addEditor(SHARE_WITH); else ss.addViewer(SHARE_WITH);
  }
  Logger.log("Created: " + ss.getUrl());
  return ss.getUrl();
}
