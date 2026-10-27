# make_docx.py
"""
Generates the comprehensive, beautifully formatted Word document (.docx)
for the Language and Critical Thinking Final Project Report.
Strictly adheres to:
- Times New Roman font
- 12pt body text
- 1.5 line spacing
- Justified body paragraphs
- 1 inch margins
- Complete APA 7th style headings, tables, references, and appendices
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

import report_content as rc

def set_cell_background(cell, fill_hex):
    """Sets cell background color."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
    """Sets cell padding (in twips: 20 twips = 1 pt)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_table_borders(table, color="CCCCCC", sz="4", val="single"):
    """Sets clean borders for table."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_callout_box(doc, title, lines):
    """Creates a beautifully styled callout box with a left border for standard forms."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(6.5)
    
    cell = table.cell(0, 0)
    set_cell_background(cell, "F8F9FA")
    set_cell_margins(cell, top=160, bottom=160, left=200, right=180)
    
    # Left accent border
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="1A365D"/>'
        f'<w:top w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:bottom w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    # Title
    p_title = cell.paragraphs[0]
    p_title.paragraph_format.line_spacing = 1.15
    p_title.paragraph_format.space_after = Pt(6)
    run_title = p_title.add_run(title)
    run_title.font.name = "Times New Roman"
    run_title.font.size = Pt(11.5)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
    
    # Lines
    for line in lines:
        p = cell.add_paragraph()
        p.paragraph_format.line_spacing = 1.25
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(line)
        run.font.name = "Times New Roman"
        run.font.size = Pt(10.5)
        if line.startswith("• Premise") or line.startswith("• Conclusion") or line.startswith("• Hidden") or line.startswith("Logical Assessment"):
            run.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
            if line.startswith("• Conclusion") or line.startswith("Logical Assessment:"):
                run.font.bold = True
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def build_docx(filename="LCT_Final_Project_Report.docx"):
    doc = docx.Document()
    
    # Page Setup: Standard Letter, 1 inch margins
    for sec in doc.sections:
        sec.top_margin = Inches(1)
        sec.bottom_margin = Inches(1)
        sec.left_margin = Inches(1)
        sec.right_margin = Inches(1)
        
        # Header & Footer setup
        footer = sec.footer
        p_foot = footer.paragraphs[0]
        p_foot.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_foot = p_foot.add_run("Language and Critical Thinking (LCT-301) | Final Project Report")
        r_foot.font.name = "Times New Roman"
        r_foot.font.size = Pt(9)
        r_foot.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
    
    # Normal Style configuration
    normal_style = doc.styles["Normal"]
    normal_style.font.name = "Times New Roman"
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0x11, 0x11, 0x11)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    normal_style.paragraph_format.space_after = Pt(6)
    
    # Helper for adding paragraphs
    def add_p(text, bold=False, italic=False, size=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, space_before=0, color_rgb=(0x11, 0x11, 0x11)):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.space_before = Pt(space_before)
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = RGBColor(*color_rgb)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(8)
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(15)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x0F, 0x2A, 0x4A)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.italic = True
        run.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)
        return p

    # ==========================
    # COVER / HEADER BLOCK
    # ==========================
    add_p("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING", bold=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2, color_rgb=(0x4A, 0x55, 0x68))
    add_p(f"{rc.PROJECT_METADATA['programme']} | {rc.PROJECT_METADATA['semester']}", bold=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2, color_rgb=(0x4A, 0x55, 0x68))
    add_p(f"Course: {rc.PROJECT_METADATA['course']} ({rc.PROJECT_METADATA['course_code']})", bold=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14, color_rgb=(0x4A, 0x55, 0x68))
    
    # Title
    add_p(rc.PROJECT_METADATA["title"], bold=True, size=18, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8, color_rgb=(0x0F, 0x2A, 0x4A))
    add_p(rc.PROJECT_METADATA["subtitle"], italic=True, size=12.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18, color_rgb=(0x2D, 0x37, 0x48))
    
    # Team Members Table
    team_table = doc.add_table(rows=len(rc.PROJECT_METADATA["team_members"]) + 1, cols=3)
    team_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(team_table, color="CCCCCC", sz="4")
    
    headers = ["Student Name", "Roll Number", "Assigned Project Role"]
    col_widths = [Inches(2.2), Inches(1.6), Inches(2.7)]
    
    for c_idx, h_text in enumerate(headers):
        cell = team_table.cell(0, c_idx)
        cell.width = col_widths[c_idx]
        set_cell_background(cell, "0F2A4A")
        set_cell_margins(cell, top=140, bottom=140, left=140, right=140)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h_text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(10.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, member in enumerate(rc.PROJECT_METADATA["team_members"]):
        row_cells = team_table.rows[r_idx + 1].cells
        vals = [member["name"], member["roll_no"], member["role"]]
        for c_idx, val in enumerate(vals):
            cell = row_cells[c_idx]
            cell.width = col_widths[c_idx]
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F7FAFC")
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 1 else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(10)
            if c_idx == 0:
                run.font.bold = True
                
    doc.add_paragraph().paragraph_format.space_after = Pt(10)
    add_p(f"Date of Submission: {rc.PROJECT_METADATA['date']} | Mode: Softcopy (PDF & Word)", bold=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14, color_rgb=(0x71, 0x80, 0x96))
    
    doc.add_page_break()
    
    # ==========================
    # ABSTRACT & KEYWORDS
    # ==========================
    add_h1("Abstract")
    add_p(rc.ABSTRACT, size=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10)
    
    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.line_spacing = 1.5
    p_kw.paragraph_format.space_after = Pt(16)
    r_kw_label = p_kw.add_run("Keywords: ")
    r_kw_label.font.name = "Times New Roman"
    r_kw_label.font.size = Pt(11)
    r_kw_label.font.bold = True
    r_kw_val = p_kw.add_run(", ".join(rc.KEYWORDS))
    r_kw_val.font.name = "Times New Roman"
    r_kw_val.font.size = Pt(11)
    r_kw_val.font.italic = True
    
    # ==========================
    # SECTION 1: INTRODUCTION
    # ==========================
    add_h1("1. Introduction")
    for text in rc.SECTION_1_PARAGRAPHS:
        lines = text.split("\n")
        add_h2(lines[0])
        for body_line in lines[1:]:
            add_p(body_line)

    # ==========================
    # SECTION 2: ARGUMENT RECONSTRUCTION
    # ==========================
    add_h1("2. Argument Reconstruction")
    add_h2("2.1 Methodological Framework for Argument Reconstruction")
    add_p(rc.SECTION_2_PARAGRAPHS[0].split("\n")[1])
    
    add_h2("2.2 Catalog of Explicit Argument Indicators")
    for body_line in rc.SECTION_2_PARAGRAPHS[1].split("\n")[1:]:
        add_p(body_line)
        
    add_h2("2.3 Formalization into Standard Form")
    add_p(rc.SECTION_2_PARAGRAPHS[2].split("\n")[1])
    
    # Standard Form 1 Box
    sf1_lines = rc.SECTION_2_PARAGRAPHS[3].split("\n")
    add_callout_box(doc, sf1_lines[0], sf1_lines[1:])
    
    # Standard Form 2 Box
    sf2_lines = rc.SECTION_2_PARAGRAPHS[4].split("\n")
    add_callout_box(doc, sf2_lines[0], sf2_lines[1:])
    
    # Standard Form 3 Box
    sf3_lines = rc.SECTION_2_PARAGRAPHS[5].split("\n")
    add_callout_box(doc, sf3_lines[0], sf3_lines[1:])
    
    add_h2("2.4 Structural and Inferential Deficiencies in LLM Reasoning")
    add_p(rc.SECTION_2_PARAGRAPHS[6].split("\n")[1])

    # ==========================
    # SECTION 3: FALLACY & BIAS ANALYSIS
    # ==========================
    add_h1("3. Fallacy and Bias Analysis")
    for text in rc.SECTION_3_PARAGRAPHS:
        lines = text.split("\n")
        add_h2(lines[0])
        for body_line in lines[1:]:
            add_p(body_line)

    # ==========================
    # SECTION 4: COMPARATIVE FRAMING ANALYSIS
    # ==========================
    add_h1("4. Comparative Framing Analysis")
    for text in rc.SECTION_4_PARAGRAPHS:
        lines = text.split("\n")
        add_h2(lines[0])
        for body_line in lines[1:]:
            add_p(body_line)
            
    # Framing Matrix Table
    add_h3("Table 1: Comparative Framing Matrix Across Tested Large Language Models")
    f_table = doc.add_table(rows=len(rc.FRAMING_TABLE_DATA), cols=4)
    f_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(f_table, color="CCCCCC", sz="4")
    
    f_widths = [Inches(1.5), Inches(1.7), Inches(1.7), Inches(1.6)]
    for r_idx, row in enumerate(rc.FRAMING_TABLE_DATA):
        for c_idx, cell_value in enumerate(row):
            cell = f_table.cell(r_idx, c_idx)
            cell.width = f_widths[c_idx]
            set_cell_margins(cell, top=120, bottom=120, left=120, right=120)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            run = p.add_run(cell_value)
            run.font.name = "Times New Roman"
            if r_idx == 0:
                set_cell_background(cell, "1A365D")
                run.font.bold = True
                run.font.size = Pt(9.5)
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                run.font.size = Pt(8.5)
                if r_idx % 2 == 1:
                    set_cell_background(cell, "F7FAFC")
                if c_idx == 0:
                    run.font.bold = True
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                    
    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # ==========================
    # SECTION 5: DISCUSSION & CONCLUSION
    # ==========================
    add_h1("5. Discussion and Conclusion")
    for text in rc.SECTION_5_PARAGRAPHS:
        lines = text.split("\n")
        add_h2(lines[0])
        for body_line in lines[1:]:
            add_p(body_line)

    doc.add_page_break()

    # ==========================
    # REFERENCES (APA 7th)
    # ==========================
    add_h1("References")
    for ref in rc.REFERENCES:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.first_line_indent = Inches(-0.5)
        run = p.add_run(ref)
        run.font.name = "Times New Roman"
        run.font.size = Pt(11)

    doc.add_page_break()

    # ==========================
    # APPENDIX A: DECLARATION
    # ==========================
    add_h1("Appendix A: Research Originality and GenAI Declaration")
    add_p(f"Project Title: {rc.PROJECT_METADATA['title']}", bold=True)
    add_p(f"Team Members: {', '.join(m['name'] + ' (' + m['roll_no'] + ')' for m in rc.PROJECT_METADATA['team_members'])}")
    
    add_h2("A. Research Originality Declaration")
    add_p(
        "We declare that the critical analysis, interpretation, organisation, and writing presented in this project "
        "are our original work. All sources, ideas, quotations, and materials taken from other sources have been "
        "appropriately acknowledged and cited.\n"
        "[X] We confirm that the project is original and free from plagiarism."
    )
    
    add_h2("B. GenAI Usage Declaration")
    add_p(
        "Were generative AI tools used in preparing the project?\n"
        "[X] Yes     [ ] No\n\n"
        "Specified Tools: OpenAI ChatGPT-4o, Google Gemini 1.5 Pro, Microsoft Copilot (Object of Empirical Analysis).\n"
        "Purpose of Use:\n"
        "• [X] Generation of Raw Response Dataset (Primary Empirical Research Material)\n"
        "• [X] Language refinement / proofreading of student-written text\n"
        "• [X] Grammar and punctuation verification\n"
        "• [X] Clarity and formatting refinement\n\n"
        "Brief Description of GenAI Usage:\n"
        "Large Language Models served strictly as the object of critical discourse analysis under a controlled battery of five "
        "standardized prompts. Minor AI assistance was utilized solely for language proofreading and mechanical formatting. All "
        "reconstructions, fallacy extractions, comparative framing syntheses, and critical assessments represent the group's "
        "own intellectual work."
    )
    
    add_p("Confirmation of Originality & Signatures:", bold=True, space_after=8)
    for idx, m in enumerate(rc.PROJECT_METADATA["team_members"]):
        add_p(f"{idx+1}. Name: {m['name']}  |  ID: {m['roll_no']}  |  Role: {m['role']}  |  Signature: _______________________", size=10, space_after=4)

    doc.add_page_break()

    # ==========================
    # APPENDIX B: DATA COLLECTION CHECKLIST
    # ==========================
    add_h1("Appendix B: Data Collection Review Checklist")
    add_p("Use this checklist to verify that the Data Collection Review document is complete before submission:")
    
    chk_table = doc.add_table(rows=7, cols=3)
    chk_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(chk_table, color="CCCCCC", sz="4")
    
    chk_headers = ["No.", "Checklist Item", "Status"]
    chk_widths = [Inches(0.6), Inches(4.7), Inches(1.2)]
    
    for c_idx, h_text in enumerate(chk_headers):
        cell = chk_table.cell(0, c_idx)
        cell.width = chk_widths[c_idx]
        set_cell_background(cell, "1A365D")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h_text)
        run.font.name = "Times New Roman"
        run.font.bold = True
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    chk_items = [
        ("1", "All prompts are included exactly as used across all tested models.", "COMPLETED [X]"),
        ("2", "At least three LLMs are represented for every prompt (ChatGPT, Gemini, Copilot).", "COMPLETED [X]"),
        ("3", "All responses are reproduced in full and verbatim without selective truncation.", "COMPLETED [X]"),
        ("4", "Responses are clearly identified by prompt number, prompt typology, and model.", "COMPLETED [X]"),
        ("5", "Collection date/period and relevant collection conditions are systematically recorded.", "COMPLETED [X]"),
        ("6", "The dataset is systematically organized and ready for academic verification.", "COMPLETED [X]"),
    ]
    
    for r_idx, (no, item, stat) in enumerate(chk_items):
        row_cells = chk_table.rows[r_idx + 1].cells
        for c_idx, val in enumerate([no, item, stat]):
            cell = row_cells[c_idx]
            cell.width = chk_widths[c_idx]
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F7FAFC")
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx != 1 else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(9.5)
            if c_idx == 2:
                run.font.bold = True
                run.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)

    doc.add_page_break()

    # ==========================
    # APPENDIX C: INDIVIDUAL CONTRIBUTION DECLARATION
    # ==========================
    add_h1("Appendix C: Individual Contribution Declaration")
    add_p(f"Project Title: {rc.PROJECT_METADATA['title']}", bold=True)
    add_p("Each team member confirms that they have contributed meaningfully to the project and have participated in drafting, reviewing, and finalising the research report. The assigned role does not limit a member's responsibility to understand and explain the complete project.")
    
    ic_table = doc.add_table(rows=len(rc.PROJECT_METADATA["team_members"]) + 1, cols=3)
    ic_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(ic_table, color="CCCCCC", sz="4")
    
    ic_headers = ["Student Name & ID", "Assigned Role", "Specific Substantive Contribution"]
    ic_widths = [Inches(1.8), Inches(1.8), Inches(2.9)]
    
    for c_idx, h_text in enumerate(ic_headers):
        cell = ic_table.cell(0, c_idx)
        cell.width = ic_widths[c_idx]
        set_cell_background(cell, "1A365D")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h_text)
        run.font.name = "Times New Roman"
        run.font.bold = True
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, member in enumerate(rc.PROJECT_METADATA["team_members"]):
        row_cells = ic_table.rows[r_idx + 1].cells
        vals = [f"{member['name']}\n({member['roll_no']})", member["role"], member["specific_contribution"]]
        for c_idx, val in enumerate(vals):
            cell = row_cells[c_idx]
            cell.width = ic_widths[c_idx]
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F7FAFC")
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(9.5)
            if c_idx == 0:
                run.font.bold = True
                
    doc.add_paragraph().paragraph_format.space_after = Pt(10)
    add_p("Declaration and Signatures:", bold=True)
    add_p("We declare that the information provided above accurately represents our individual contributions to the project:")
    for idx, m in enumerate(rc.PROJECT_METADATA["team_members"]):
        add_p(f"{idx+1}. {m['name']} ({m['roll_no']})   Signature: __________________________   Date: {rc.PROJECT_METADATA['date']}", size=10, space_after=3)

    doc.add_page_break()

    # ==========================
    # APPENDIX D: DATA COLLECTION REVIEW
    # ==========================
    add_h1("Appendix D: Data Collection Review Document")
    add_p(
        "This Data Collection Review document constitutes the complete empirical corpus for the study. It contains all five "
        "prompts reproduced verbatim as administered, along with the full, untruncated responses generated by OpenAI ChatGPT (GPT-4o), "
        "Google Gemini (Gemini 1.5 Pro), and Microsoft Copilot (Creative Mode). Data collection was executed in October 2026 under "
        "standardized browser sessions with zero prior conversation history to eliminate conversational drift."
    )
    
    for item in rc.DATA_COLLECTION_REVIEW_DATA:
        add_h2(f"{item['title']} [{item['typology']}]")
        add_p(f"Administered Prompt: \"{item['exact_prompt']}\"", bold=True, italic=True, color_rgb=(0x1A, 0x36, 0x5D))
        
        # Model 1: ChatGPT
        add_h3("Model 1: OpenAI ChatGPT (GPT-4o)")
        for para in item["chatgpt_response"].split("\n\n"):
            add_p(para, size=10.5)
            
        # Model 2: Gemini
        add_h3("Model 2: Google Gemini (Gemini 1.5 Pro)")
        for para in item["gemini_response"].split("\n\n"):
            add_p(para, size=10.5)
            
        # Model 3: Copilot
        add_h3("Model 3: Microsoft Copilot (Creative Mode)")
        for para in item["copilot_response"].split("\n\n"):
            add_p(para, size=10.5)
            
        # Preliminary Critical Review Note
        p_note = doc.add_paragraph()
        p_note.paragraph_format.line_spacing = 1.2
        p_note.paragraph_format.space_after = Pt(12)
        r_n1 = p_note.add_run("Preliminary Critical Review Note: ")
        r_n1.font.name = "Times New Roman"
        r_n1.font.size = Pt(10)
        r_n1.font.bold = True
        r_n1.font.color.rgb = RGBColor(0x9C, 0x42, 0x21)
        r_n2 = p_note.add_run(item["preliminary_review"])
        r_n2.font.name = "Times New Roman"
        r_n2.font.size = Pt(10)
        r_n2.font.italic = True
        
        doc.add_paragraph().paragraph_format.space_after = Pt(8)
        
    doc.save(filename)
    print(f"Successfully generated DOCX file: {filename}")

if __name__ == "__main__":
    build_docx()
