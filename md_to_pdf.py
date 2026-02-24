#!/usr/bin/env python3
"""
Reusable Markdown-to-PDF converter using fpdf2.

Converts any Markdown file into a professionally formatted PDF with:
  - Cover page (title, subtitle, author, version, year)
  - Auto-generated Table of Contents from ## headers
  - Color-coded section headers (## -> blue, ### -> dark gray)
  - Gray-background code blocks with Courier font
  - Styled tables with blue headers and alternating row shading
  - Bullet points, bold text, and regular paragraphs
  - Page headers and footers with page numbers
  - Unicode sanitization for Latin-1 compatibility

Usage:
    python md_to_pdf.py --input FILE.md --output FILE.pdf \
        --title "Title" --subtitle "Subtitle" --author "Author"
"""

import argparse
import re
from datetime import datetime
from fpdf import FPDF

# ---------------------------------------------------------------------------
# Unicode -> Latin-1 safe replacements
# ---------------------------------------------------------------------------
UNICODE_REPLACEMENTS = {
    "\u2022": "-",
    "\u2191": "Up",
    "\u2193": "Down",
    "\u2190": "Left",
    "\u2192": "Right",
    "\u2014": "--",
    "\u2013": "-",
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u2026": "...",
    "\u00a0": " ",
    "\u200b": "",
    "\u2003": " ",
    "\u2002": " ",
    "\u2009": " ",
    "\u200a": " ",
    "\u2501": "-",
    "\u2502": "|",
    "\u250c": "+",
    "\u2510": "+",
    "\u2514": "+",
    "\u2518": "+",
    "\u251c": "+",
    "\u2524": "+",
    "\u252c": "+",
    "\u2534": "+",
    "\u253c": "+",
    "\u2500": "-",
}


def sanitize_text(text):
    """Replace known Unicode characters and drop any remaining non-Latin-1 chars."""
    for char, replacement in UNICODE_REPLACEMENTS.items():
        text = text.replace(char, replacement)
    result = []
    for ch in text:
        try:
            ch.encode("latin-1")
            result.append(ch)
        except UnicodeEncodeError:
            result.append("?")
    return "".join(result)


# ---------------------------------------------------------------------------
# Custom PDF class with header / footer
# ---------------------------------------------------------------------------
class MarkdownPDF(FPDF):
    """FPDF subclass that renders a header banner and page-number footer."""

    def __init__(self, header_title="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._header_title = header_title

    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(128, 128, 128)
            self.cell(
                0,
                10,
                sanitize_text(self._header_title),
                align="C",
            )
            self.ln(5)
            self.set_draw_color(200, 200, 200)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


# ---------------------------------------------------------------------------
# PDF-building helpers (operate on a given *pdf* instance)
# ---------------------------------------------------------------------------

def _add_cover_page(pdf, title, subtitle, author, version="1.0", year=None):
    """Render a centred cover page."""
    if year is None:
        year = str(datetime.now().year)

    pdf.add_page()
    pdf.ln(60)

    # Title lines – split on whitespace runs so long titles wrap naturally
    pdf.set_font("Helvetica", "B", 32)
    pdf.set_text_color(41, 128, 185)  # #2980B9

    title_words = sanitize_text(title).split()
    # Group into lines of ~3 words each for a nice cover look
    chunk_size = 3
    title_lines = []
    for i in range(0, len(title_words), chunk_size):
        title_lines.append(" ".join(title_words[i : i + chunk_size]))
    for line in title_lines:
        pdf.cell(0, 15, line, align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(10)
    # Decorative line
    pdf.set_draw_color(41, 128, 185)
    pdf.set_line_width(1)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(10)

    # Subtitle
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(
        0, 10, sanitize_text(subtitle), align="C", new_x="LMARGIN", new_y="NEXT"
    )

    pdf.ln(20)

    # Author / version
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(
        0,
        8,
        f"Author: {sanitize_text(author)}",
        align="C",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.cell(
        0,
        8,
        f"Version: {version}  |  {year}",
        align="C",
        new_x="LMARGIN",
        new_y="NEXT",
    )


def _add_toc(pdf, toc_items):
    """Render a Table of Contents page from a list of section titles."""
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(41, 128, 185)
    pdf.cell(0, 12, "Table of Contents", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(50, 50, 50)
    for idx, item in enumerate(toc_items, start=1):
        pdf.cell(10)
        pdf.cell(
            0,
            8,
            sanitize_text(f"{idx}. {item}"),
            new_x="LMARGIN",
            new_y="NEXT",
        )


def _section_title(pdf, title):
    """New page + large blue header with underline."""
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(41, 128, 185)
    pdf.cell(0, 12, sanitize_text(title), new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(41, 128, 185)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y() + 2, 200, pdf.get_y() + 2)
    pdf.ln(8)


def _subsection_title(pdf, title):
    """Dark-grey bold subsection heading."""
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(52, 73, 94)
    pdf.cell(0, 10, sanitize_text(title), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)


def _body_text(pdf, text):
    """Normal paragraph text."""
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 6, sanitize_text(text))
    pdf.ln(2)


def _code_block(pdf, lines):
    """Render a code block with grey background and Courier font."""
    pdf.set_fill_color(240, 240, 240)
    pdf.set_draw_color(200, 200, 200)
    pdf.set_font("Courier", "", 9)
    pdf.set_text_color(30, 30, 30)
    x = pdf.get_x()
    w = 190
    for line in lines:
        if pdf.get_y() > 265:
            pdf.add_page()
        pdf.set_x(x)
        pdf.cell(
            w,
            5.5,
            "  " + sanitize_text(line),
            fill=True,
            new_x="LMARGIN",
            new_y="NEXT",
        )
    pdf.ln(4)


def _table_col_widths(num_cols):
    """Return a list of column widths that sum to 190 mm."""
    if num_cols == 2:
        return [45, 145]
    elif num_cols == 3:
        return [35, 55, 100]
    elif num_cols == 4:
        return [30, 45, 50, 65]
    else:
        # 5+ columns: distribute evenly
        w = int(190 / num_cols)
        widths = [w] * num_cols
        # give any remaining space to the last column
        widths[-1] += 190 - sum(widths)
        return widths


def _table_row(pdf, cells, header=False):
    """Render one table row with optional header styling."""
    pdf.set_font("Helvetica", "B" if header else "", 9)
    if header:
        pdf.set_fill_color(41, 128, 185)
        pdf.set_text_color(255, 255, 255)
    else:
        pdf.set_fill_color(245, 245, 245)
        pdf.set_text_color(50, 50, 50)

    col_widths = _table_col_widths(len(cells))
    for i, cell in enumerate(cells):
        cw = col_widths[i] if i < len(col_widths) else 60
        pdf.cell(cw, 7, sanitize_text(cell.strip()), border=1, fill=True)
    pdf.ln()


def _clean_inline_md(text):
    """Strip inline Markdown formatting (backticks, bold, links)."""
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text


# ---------------------------------------------------------------------------
# Markdown parser  →  PDF builder
# ---------------------------------------------------------------------------

def _extract_toc(sections):
    """Return a list of section titles (from ## headers) for the ToC."""
    toc = []
    for sec in sections:
        lines = sec.strip().split("\n")
        title = lines[0].strip().lstrip("#").strip()
        if title.lower().startswith("table of contents"):
            continue
        toc.append(title)
    return toc


def _parse_and_render(pdf, md_content):
    """Walk through Markdown content and emit PDF elements."""
    sections = md_content.split("\n## ")

    # First pass: collect ToC items (skip the part before the first ##)
    toc_items = _extract_toc(sections[1:])
    _add_toc(pdf, toc_items)

    # Second pass: render each section
    for sec_idx, section in enumerate(sections):
        if sec_idx == 0:
            # Content before the first ## (often a top-level # heading / intro)
            continue

        lines = section.strip().split("\n")
        title = lines[0].strip().lstrip("#").strip()

        if title.lower().startswith("table of contents"):
            continue

        _section_title(pdf, title)

        in_code = False
        code_lines = []
        in_table = False

        for line in lines[1:]:
            stripped = line.strip()

            # --- code fences ---
            if stripped.startswith("```"):
                if in_code:
                    _code_block(pdf, code_lines)
                    code_lines = []
                    in_code = False
                else:
                    in_code = True
                continue

            if in_code:
                code_lines.append(line.rstrip())
                continue

            # --- tables ---
            if stripped.startswith("|") and not stripped.startswith("|---"):
                cells = [c.strip() for c in stripped.split("|") if c.strip()]
                if not in_table:
                    in_table = True
                    if pdf.get_y() > 250:
                        pdf.add_page()
                    _table_row(pdf, cells, header=True)
                elif (
                    stripped.replace("|", "").replace("-", "").replace(" ", "") == ""
                ):
                    continue
                else:
                    if pdf.get_y() > 270:
                        pdf.add_page()
                    _table_row(pdf, cells, header=False)
                continue
            elif in_table and not stripped.startswith("|"):
                in_table = False
                pdf.ln(3)

            # Skip separator lines
            if stripped.startswith("|---") or stripped == "---":
                continue

            # --- subsection headers ---
            if stripped.startswith("### "):
                _subsection_title(pdf, stripped[4:].strip())
                continue

            # --- bold-only paragraphs ---
            if stripped.startswith("**") and stripped.endswith("**"):
                pdf.set_font("Helvetica", "B", 10)
                pdf.set_text_color(50, 50, 50)
                text = stripped.strip("*").strip()
                pdf.multi_cell(0, 6, sanitize_text(text))
                pdf.ln(2)
                continue

            # --- bullet points ---
            if stripped.startswith("- "):
                pdf.set_font("Helvetica", "", 10)
                pdf.set_text_color(50, 50, 50)
                text = _clean_inline_md(stripped[2:])
                pdf.cell(5)
                pdf.cell(5, 6, "-")
                pdf.multi_cell(175, 6, sanitize_text(text))
                pdf.ln(1)
                continue

            # --- blockquotes (render as italic indented text) ---
            if stripped.startswith("> "):
                pdf.set_font("Helvetica", "I", 10)
                pdf.set_text_color(100, 100, 100)
                text = _clean_inline_md(stripped[2:].lstrip("*").rstrip("*").strip())
                pdf.cell(10)
                pdf.multi_cell(175, 6, sanitize_text(text))
                pdf.ln(2)
                continue

            # --- regular paragraph ---
            if stripped and not stripped.startswith("#"):
                text = _clean_inline_md(stripped)
                _body_text(pdf, text)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def convert_md_to_pdf(
    input_path,
    output_path,
    title="Document",
    subtitle="",
    author="Author",
    version="1.0",
    year=None,
):
    """Read *input_path* (Markdown) and write a styled PDF to *output_path*."""
    if year is None:
        year = str(datetime.now().year)

    with open(input_path, "r", encoding="utf-8") as fh:
        md_content = fh.read()

    pdf = MarkdownPDF(header_title=title)
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    _add_cover_page(pdf, title, subtitle, author, version=version, year=year)
    _parse_and_render(pdf, md_content)

    pdf.output(output_path)
    print(f"PDF generated successfully: {output_path}")


# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Convert a Markdown file to a professionally formatted PDF.",
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the input Markdown file.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path for the output PDF file.",
    )
    parser.add_argument(
        "--title",
        default="Document",
        help="Document title (displayed on cover page and header).",
    )
    parser.add_argument(
        "--subtitle",
        default="",
        help="Document subtitle (displayed on cover page).",
    )
    parser.add_argument(
        "--author",
        default="Author",
        help="Author name (displayed on cover page).",
    )
    parser.add_argument(
        "--version",
        default="1.0",
        help="Document version string (default: 1.0).",
    )
    parser.add_argument(
        "--year",
        default=None,
        help="Year shown on the cover page (default: current year).",
    )

    args = parser.parse_args()

    convert_md_to_pdf(
        input_path=args.input,
        output_path=args.output,
        title=args.title,
        subtitle=args.subtitle,
        author=args.author,
        version=args.version,
        year=args.year,
    )


if __name__ == "__main__":
    main()
