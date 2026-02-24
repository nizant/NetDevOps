import re
from fpdf import FPDF

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
}


def sanitize_text(text):
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


class UbuntuDocPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, "Ubuntu Basic Commands Documentation", align="C")
            self.ln(5)
            self.set_draw_color(200, 200, 200)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


def create_pdf():
    pdf = UbuntuDocPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # --- COVER PAGE ---
    pdf.add_page()
    pdf.ln(60)
    pdf.set_font("Helvetica", "B", 32)
    pdf.set_text_color(41, 128, 185)
    pdf.cell(0, 15, "Ubuntu", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 15, "Basic Commands", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 15, "Documentation", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_draw_color(41, 128, 185)
    pdf.set_line_width(1)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, "A Comprehensive Reference Guide", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, "Author: NetDevOps Team", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Version: 1.0  |  2025", align="C", new_x="LMARGIN", new_y="NEXT")

    # --- TABLE OF CONTENTS ---
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(41, 128, 185)
    pdf.cell(0, 12, "Table of Contents", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    toc_items = [
        "1. Introduction",
        "2. System Information Commands",
        "3. File & Directory Management",
        "4. File Viewing & Editing",
        "5. File Permissions & Ownership",
        "6. User Management",
        "7. Package Management (APT)",
        "8. Process Management",
        "9. Networking Commands",
        "10. Disk & Storage Management",
        "11. Search & Find Commands",
        "12. Compression & Archiving",
        "13. SSH & Remote Access",
        "14. System Services (systemctl)",
        "15. Useful Shortcuts & Tips",
        "16. Quick Reference Cheat Sheet",
    ]
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(50, 50, 50)
    for item in toc_items:
        pdf.cell(10)
        pdf.cell(0, 8, item, new_x="LMARGIN", new_y="NEXT")

    # --- HELPER FUNCTIONS ---
    def section_title(title):
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 20)
        pdf.set_text_color(41, 128, 185)
        pdf.cell(0, 12, sanitize_text(title), new_x="LMARGIN", new_y="NEXT")
        pdf.set_draw_color(41, 128, 185)
        pdf.set_line_width(0.5)
        pdf.line(10, pdf.get_y() + 2, 200, pdf.get_y() + 2)
        pdf.ln(8)

    def subsection_title(title):
        pdf.ln(4)
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_text_color(52, 73, 94)
        pdf.cell(0, 10, sanitize_text(title), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

    def body_text(text):
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(0, 6, sanitize_text(text))
        pdf.ln(2)

    def code_block(lines):
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
            pdf.cell(w, 5.5, "  " + sanitize_text(line), fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)

    def table_row(cells, header=False):
        pdf.set_font("Helvetica", "B" if header else "", 9)
        if header:
            pdf.set_fill_color(41, 128, 185)
            pdf.set_text_color(255, 255, 255)
        else:
            pdf.set_fill_color(245, 245, 245)
            pdf.set_text_color(50, 50, 50)
        col_widths = [35, 55, 100] if len(cells) == 3 else [45, 145]
        for i, cell in enumerate(cells):
            cw = col_widths[i] if i < len(col_widths) else 60
            pdf.cell(cw, 7, sanitize_text(cell.strip()), border=1, fill=True)
        pdf.ln()

    # --- PARSE MARKDOWN AND BUILD PDF ---
    with open("NetDevOps/Ubuntu_Basic_Commands_Documentation.md", "r", encoding="utf-8") as f:
        content = f.read()

    sections = content.split("\n## ")
    for sec_idx, section in enumerate(sections):
        if sec_idx == 0:
            continue

        lines = section.strip().split("\n")
        title = lines[0].strip().lstrip("#").strip()

        if title.startswith("Table of Contents"):
            continue



        section_title(title)

        in_code = False
        code_lines = []
        in_table = False

        for line in lines[1:]:
            stripped = line.strip()

            # Handle code blocks
            if stripped.startswith("```"):
                if in_code:
                    code_block(code_lines)
                    code_lines = []
                    in_code = False
                else:
                    in_code = True
                continue

            if in_code:
                code_lines.append(line.rstrip())
                continue

            # Handle tables
            if stripped.startswith("|") and not stripped.startswith("|---"):
                cells = [c.strip() for c in stripped.split("|") if c.strip()]
                if not in_table:
                    in_table = True
                    if pdf.get_y() > 250:
                        pdf.add_page()
                    table_row(cells, header=True)
                elif stripped.replace("|", "").replace("-", "").replace(" ", "") == "":
                    continue
                else:
                    if pdf.get_y() > 270:
                        pdf.add_page()
                    table_row(cells, header=False)
                continue
            elif in_table and not stripped.startswith("|"):
                in_table = False
                pdf.ln(3)

            # Skip separator lines
            if stripped.startswith("|---") or stripped == "---":
                continue

            # Handle subsection headers
            if stripped.startswith("### "):
                subsection_title(stripped[4:].strip())
                continue

            # Handle bold text paragraphs
            if stripped.startswith("**") and stripped.endswith("**"):
                pdf.set_font("Helvetica", "B", 10)
                pdf.set_text_color(50, 50, 50)
                text = stripped.strip("*").strip()
                pdf.multi_cell(0, 6, sanitize_text(text))
                pdf.ln(2)
                continue

            # Handle bullet points
            if stripped.startswith("- "):
                pdf.set_font("Helvetica", "", 10)
                pdf.set_text_color(50, 50, 50)
                text = stripped[2:]
                # Clean markdown formatting
                text = re.sub(r"`([^`]+)`", r"\1", text)
                text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
                text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
                pdf.cell(5)
                pdf.cell(5, 6, "-")
                pdf.multi_cell(175, 6, sanitize_text(text))
                pdf.ln(1)
                continue

            # Regular paragraph text
            if stripped and not stripped.startswith("#"):
                text = re.sub(r"`([^`]+)`", r"\1", stripped)
                text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
                text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
                body_text(text)

    # --- ADDITIONAL RESOURCES PAGE ---
    section_title("Additional Resources")
    resources = [
        ("Ubuntu Official Documentation", "https://help.ubuntu.com"),
        ("Ubuntu Community Wiki", "https://wiki.ubuntu.com"),
        ("Man Pages", "Type 'man command_name' in the terminal for detailed help"),
        ("Built-in Help", "Type 'command_name --help' for quick usage info"),
    ]
    for name, desc in resources:
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(41, 128, 185)
        pdf.cell(0, 8, name, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 6, desc, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)

    # Save
    output_path = "NetDevOps/Ubuntu_Basic_Commands_Documentation.pdf"
    pdf.output(output_path)
    print(f"PDF generated successfully: {output_path}")


if __name__ == "__main__":
    create_pdf()
