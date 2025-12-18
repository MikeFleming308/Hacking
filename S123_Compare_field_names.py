# Compares Survey123 .xlsx names with existing Word feature service templates
# to streamline template creation.

# Import modules
import re


# Variables
# Input .xlsx and .docx
xlsx = r''
docx = r''

#!/usr/bin/env python3
"""
compare_survey123_fields.py

Compare Survey123 XLSForm 'name' column (survey sheet, column B) against field tokens
found in a feature service template DOCX where tokens appear like ${...}.

Extraction rules for DOCX tokens (as requested):
- Find every ${...} occurrence.
- The field name is the first whole word after the opening "${".
- A valid field name (per your spec) is composed of lowercase letters and underscores only: [a-z_]+
- If the first token inside the braces is prefixed with "If " (case/diacritic variants) or "#" (e.g. "${If rock_size}" or "${#rock_size}"),
  the "If"/"#" prefix is discarded and the field name is still extracted.
- The script normalizes any Unicode diacritics when checking for the "If" prefix so variants like "Ïf" are handled.

XLSX rules:
- Only the "survey" sheet is used (case-insensitive match).
- Only column B (the second column) is read, starting at row 2 (skipping header).
- Values are read as-is (but options are provided to compare case-insensitively or normalize spaces to underscores).

Usage:
    pip install openpyxl python-docx
    python compare_survey123_fields.py path/to/form.xlsx path/to/template.docx [--ignore-case] [--normalize] [--output report.json]

Options:
    --ignore-case    Compare case-insensitively (lowercases both sides before comparing).
    --normalize      Replace spaces with underscores before comparing.
    --output FILE    Save JSON report to FILE (suffix .json).

Author: tailored for MikeFleming308 (2025-12-18)
"""
from pathlib import Path
import argparse
import re
import json
import sys
import unicodedata

try:
    from openpyxl import load_workbook
except Exception:
    print("Missing required module 'openpyxl'. Install with: pip install openpyxl", file=sys.stderr)
    raise

try:
    from docx import Document
except Exception:
    print("Missing required module 'python-docx'. Install with: pip install python-docx", file=sys.stderr)
    raise


def read_survey_names_from_xlsx(xlsx_path: Path):
    """
    Read column B (index 2) from the sheet named 'survey' (case-insensitive).
    Start at row 2 (skip header). Preserve order and dedupe while preserving first occurrence.
    Returns list[str]
    """
    wb = load_workbook(filename=str(xlsx_path), read_only=True, data_only=True)
    survey_sheet = None
    for name in wb.sheetnames:
        if name.lower() == "survey":
            survey_sheet = wb[name]
            break
    if survey_sheet is None:
        raise ValueError(f"No sheet named 'survey' found in {xlsx_path}. Available sheets: {wb.sheetnames}")

    names = []
    seen = set()
    # Column B = min_col=2,max_col=2. Start at row 2 to skip header.
    for row in survey_sheet.iter_rows(min_row=2, min_col=2, max_col=2, values_only=True):
        val = row[0]
        if val is None:
            continue
        s = str(val).strip()
        if s == "":
            continue
        if s not in seen:
            seen.add(s)
            names.append(s)
    return names


def _strip_combining_marks(s: str) -> str:
    """
    Normalize to NFD and remove combining marks so diacritics are collapsed for matching.
    """
    n = unicodedata.normalize("NFD", s)
    return "".join(ch for ch in n if not unicodedata.combining(ch))


def _extract_field_from_token_content(content: str):
    """
    Given the text between ${ and }, extract the field name according to rules:
    - Skip optional leading whitespace.
    - If content starts with '#' -> discard it and leading whitespace.
    - If content starts with 'if' (case-insensitive) or variants with diacritics (e.g., 'Ïf'), discard the 'if' and following whitespace.
      To detect 'if' robustly, we normalize and remove combining marks then check for leading 'if'.
    - The field name is the first whole word after those optional prefixes, and must match [a-z_]+ (lowercase letters and underscores only).
    Returns the field name as matched (lowercase), or None if no valid field name found.
    """
    if content is None:
        return None
    # Work on a copy for prefix detection that has diacritics removed
    content_original = content
    content_norm = _strip_combining_marks(content_original)
    content_norm_stripped = content_norm.lstrip()
    # Remove leading '#' if present
    if content_norm_stripped.startswith("#"):
        # remove first '#' from the original content's left-stripped version
        # compute how many chars were stripped on the left to map back: easier to re-strip original and then drop leading '#'
        orig_stripped = content_original.lstrip()
        orig_after_hash = orig_stripped[1:].lstrip() if orig_stripped.startswith("#") else orig_stripped
        # now attempt to find first lowercase-word
        search_source = orig_after_hash
    else:
        # check for leading 'if' (case-insensitive) on normalized string
        low = content_norm_stripped.lower()
        if low.startswith("if") and (len(low) == 2 or (len(low) > 2 and not low[2].isalpha())):
            # remove the 'if' token from the original (use whitespace-aware approach)
            orig_stripped = content_original.lstrip()
            # remove first token if it's 'if' variant (match up to first whitespace)
            m = re.match(r'(?i)if\b', _strip_combining_marks(orig_stripped))
            if m:
                # remove the matched characters from orig_stripped by length of m.group(0)
                cut_len = len(m.group(0))
                # There might be diacritics in the original but the number of base chars should match for 'if' variants.
                orig_after_if = orig_stripped[cut_len:].lstrip()
                search_source = orig_after_if
            else:
                # fallback to original stripped
                search_source = content_original.lstrip()
        else:
            search_source = content_original.lstrip()

    # Now find the first whole word consisting only of lowercase letters and underscores
    # We'll search on a normalized version for matching, but return the matched substring lowercased
    # Create a lowercased, combining-removed search string for matching
    search_norm = _strip_combining_marks(search_source).lower()

    # Find first occurrence of [a-z_]+ as a whole word
    m2 = re.search(r'\b([a-z_]+)\b', search_norm)
    if not m2:
        return None
    candidate = m2.group(1)
    # Verify candidate uses only lowercase letters and underscores (already ensured by regex)
    return candidate


def extract_field_tokens_from_docx(docx_path: Path):
    """
    Scan paragraphs and table cells for ${...} occurrences.
    For each occurrence, extract the field name using _extract_field_from_token_content.
    Return list of unique field names preserving first-seen order.
    """
    doc = Document(str(docx_path))
    # Find all ${...} occurrences even across text runs by joining cell/paragraph text.
    token_pattern = re.compile(r'\$\{\s*([^}]*)\s*\}')

    found = []
    seen = set()

    # Helper to scan a given text block
    def scan_text_block(text: str):
        for m in token_pattern.finditer(text):
            inner = m.group(1)
            fld = _extract_field_from_token_content(inner)
            if fld and fld not in seen:
                seen.add(fld)
                found.append(fld)

    # scan paragraphs
    for p in doc.paragraphs:
        if p.text:
            scan_text_block(p.text)

    # scan table cells
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                if cell.text:
                    scan_text_block(cell.text)

    return found


def normalize_list(items, ignore_case=False, normalize_spaces=False):
    out = []
    seen = set()
    for it in items:
        s = it
        if s is None:
            continue
        s = s.strip()
        if normalize_spaces:
            s = s.replace(" ", "_")
        if ignore_case:
            s = s.lower()
        if s and s not in seen:
            seen.add(s)
            out.append(s)
    return out


def compare_lists(xlsx_list, docx_list):
    set_x = set(xlsx_list)
    set_d = set(docx_list)
    in_both = [s for s in xlsx_list if s in set_d]
    only_x = sorted(list(set_x - set_d))
    only_d = sorted(list(set_d - set_x))
    return {
        "xlsx_total": len(xlsx_list),
        "docx_total": len(docx_list),
        "in_both": in_both,
        "only_in_xlsx": only_x,
        "only_in_docx": only_d,
    }


def save_report(path: Path, report: dict, raw_xlsx, raw_docx):
    out = {
        "summary": {
            "xlsx_total": report["xlsx_total"],
            "docx_total": report["docx_total"],
        },
        "in_both": report["in_both"],
        "only_in_xlsx": report["only_in_xlsx"],
        "only_in_docx": report["only_in_docx"],
        "xlsx_fields_raw": raw_xlsx,
        "docx_fields_raw": raw_docx,
    }
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Compare Survey123 XLSForm 'name' column (survey sheet, column B) with ${...} tokens in a DOCX template.")
    parser.add_argument("xlsx", help="Path to Survey123 form .xlsx (must contain a sheet named 'survey').")
    parser.add_argument("docx", help="Path to feature service template .docx (tokens like ${field_name}).")
    parser.add_argument("--ignore-case", action="store_true", help="Compare case-insensitively.")
    parser.add_argument("--normalize", action="store_true", help="Replace spaces with underscores before comparing.")
    parser.add_argument("--output", help="Optional output JSON file path to save report (.json).")
    args = parser.parse_args()

    xlsx_path = Path(args.xlsx)
    docx_path = Path(args.docx)
    if not xlsx_path.exists():
        print(f"Error: XLSX not found: {xlsx_path}", file=sys.stderr)
        return 2
    if not docx_path.exists():
        print(f"Error: DOCX not found: {docx_path}", file=sys.stderr)
        return 2

    try:
        xlsx_raw = read_survey_names_from_xlsx(xlsx_path)
    except Exception as e:
        print(f"Error reading xlsx: {e}", file=sys.stderr)
        return 3

    try:
        docx_raw = extract_field_tokens_from_docx(docx_path)
    except Exception as e:
        print(f"Error reading docx: {e}", file=sys.stderr)
        return 4

    xlsx_list = normalize_list(xlsx_raw, ignore_case=args.ignore_case, normalize_spaces=args.normalize)
    docx_list = normalize_list(docx_raw, ignore_case=args.ignore_case, normalize_spaces=args.normalize)

    report = compare_lists(xlsx_list, docx_list)

    # Print results
    print("Comparison summary")
    print("------------------")
    print(f"Fields extracted from XLSX (survey sheet, column B): {report['xlsx_total']}")
    print(f"Fields extracted from DOCX (${{...}} tokens): {report['docx_total']}")
    print()
    print(f"In both ({len(report['in_both'])}):")
    for v in report["in_both"]:
        print(f"  - {v}")
    print()
    print(f"Only in XLSX ({len(report['only_in_xlsx'])}):")
    for v in report["only_in_xlsx"]:
        print(f"  - {v}")
    print()
    print(f"Only in DOCX ({len(report['only_in_docx'])}):")
    for v in report["only_in_docx"]:
        print(f"  - {v}")

    if args.output:
        out_path = Path(args.output)
        try:
            save_report(out_path, report, xlsx_raw, docx_raw)
            print()
            print(f"Report written to {out_path.resolve()}")
        except Exception as e:
            print(f"Error writing report: {e}", file=sys.stderr)
            return 5

    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)