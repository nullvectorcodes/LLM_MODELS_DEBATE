# make_pdf.py
"""
Generates the publication-quality PDF document (LCT_Final_Project_Report.pdf)
using ReportLab with exact academic typography and layout.
Features:
- Times-Roman fonts throughout
- 1.5 line spacing (11pt / 16.5pt leading)
- Justified text
- 1 inch margins (72 pt)
- Running header and 'Page X of Y' footer via NumberedCanvas
- Professional tables with wrapped text, header styling, and alternating row shading
- Beautiful callout boxes for Standard Form argument formalizations
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas

import report_content as rc

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and draw 'Page X of Y' and running headers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # Do not draw headers/footers on the cover page (Page 1)
        if self._pageNumber > 1:
            self.saveState()
            self.setFont("Times-Roman", 8.5)
            self.setFillColor(colors.HexColor("#4A5568"))
            
            # Running Header
            header_text_left = "Language & Critical Thinking (LCT-301) | Final Research Project Report"
            header_text_right = "B. Tech AIML (Sem III)"
            self.drawString(72, 752, header_text_left)
            self.drawRightString(612 - 72, 752, header_text_right)
            
            # Header Rule
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.6)
            self.line(72, 746, 612 - 72, 746)
            
            # Running Footer
            footer_text_left = "LLM Critical Discourse Analysis: Algorithmic Authorship & Copyright"
            page_str = f"Page {self._pageNumber} of {page_count}"
            self.drawString(72, 42, footer_text_left)
            self.drawRightString(612 - 72, 42, page_str)
            
            # Footer Rule
            self.line(72, 54, 612 - 72, 54)
            self.restoreState()

def create_pdf(filename="LCT_Final_Project_Report.pdf"):
    # Page setup: Letter (8.5 x 11 inches = 612 x 792 pt), 1 inch (72 pt) margins
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=72,
        rightMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Styles
    base_styles = getSampleStyleSheet()
    
    styles = {
        "CoverDept": ParagraphStyle(
            "CoverDept",
            parent=base_styles["Normal"],
            fontName="Times-Bold",
            fontSize=10,
            leading=13,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#4A5568"),
            spaceAfter=3
        ),
        "CoverTitle": ParagraphStyle(
            "CoverTitle",
            parent=base_styles["Normal"],
            fontName="Times-Bold",
            fontSize=16,
            leading=20,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#0F2A4A"),
            spaceAfter=6
        ),
        "CoverSubtitle": ParagraphStyle(
            "CoverSubtitle",
            parent=base_styles["Normal"],
            fontName="Times-Italic",
            fontSize=11,
            leading=15,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#2D3748"),
            spaceAfter=14
        ),
        "H1": ParagraphStyle(
            "H1",
            parent=base_styles["Normal"],
            fontName="Times-Bold",
            fontSize=13.5,
            leading=17,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#0F2A4A"),
            spaceBefore=14,
            spaceAfter=6,
            keepWithNext=True
        ),
        "H2": ParagraphStyle(
            "H2",
            parent=base_styles["Normal"],
            fontName="Times-Bold",
            fontSize=11.5,
            leading=15,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#1A365D"),
            spaceBefore=10,
            spaceAfter=4,
            keepWithNext=True
        ),
        "H3": ParagraphStyle(
            "H3",
            parent=base_styles["Normal"],
            fontName="Times-BoldItalic",
            fontSize=10.5,
            leading=14,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#2B6CB0"),
            spaceBefore=8,
            spaceAfter=3,
            keepWithNext=True
        ),
        "Body": ParagraphStyle(
            "Body",
            parent=base_styles["Normal"],
            fontName="Times-Roman",
            fontSize=10.5,
            leading=15.5,  # 1.5 line equivalent
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor("#111111"),
            spaceAfter=5
        ),
        "AbstractBody": ParagraphStyle(
            "AbstractBody",
            parent=base_styles["Normal"],
            fontName="Times-Roman",
            fontSize=10,
            leading=14.5,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor("#1A202C"),
            spaceAfter=8
        ),
        "Keywords": ParagraphStyle(
            "Keywords",
            parent=base_styles["Normal"],
            fontName="Times-Roman",
            fontSize=10,
            leading=14,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#2D3748"),
            spaceAfter=14
        ),
        "CalloutTitle": ParagraphStyle(
            "CalloutTitle",
            parent=base_styles["Normal"],
            fontName="Times-Bold",
            fontSize=10.5,
            leading=13.5,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#1A365D"),
            spaceAfter=4
        ),
        "CalloutBody": ParagraphStyle(
            "CalloutBody",
            parent=base_styles["Normal"],
            fontName="Times-Roman",
            fontSize=9.5,
            leading=13,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#222222"),
            spaceAfter=2
        ),
        "CalloutBold": ParagraphStyle(
            "CalloutBold",
            parent=base_styles["Normal"],
            fontName="Times-Bold",
            fontSize=9.5,
            leading=13,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#111111"),
            spaceAfter=2
        ),
        "Reference": ParagraphStyle(
            "Reference",
            parent=base_styles["Normal"],
            fontName="Times-Roman",
            fontSize=9.5,
            leading=14,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#111111"),
            leftIndent=24,
            firstLineIndent=-24,
            spaceAfter=6
        ),
        "TableHeader": ParagraphStyle(
            "TableHeader",
            parent=base_styles["Normal"],
            fontName="Times-Bold",
            fontSize=8.5,
            leading=11,
            alignment=TA_CENTER,
            textColor=colors.white
        ),
        "TableCell": ParagraphStyle(
            "TableCell",
            parent=base_styles["Normal"],
            fontName="Times-Roman",
            fontSize=8,
            leading=10.5,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor("#111111")
        ),
        "TableCellBold": ParagraphStyle(
            "TableCellBold",
            parent=base_styles["Normal"],
            fontName="Times-Bold",
            fontSize=8,
            leading=10.5,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#111111")
        ),
        "RawResponse": ParagraphStyle(
            "RawResponse",
            parent=base_styles["Normal"],
            fontName="Times-Roman",
            fontSize=9.5,
            leading=13.5,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor("#1A202C"),
            spaceAfter=5
        ),
        "ReviewNote": ParagraphStyle(
            "ReviewNote",
            parent=base_styles["Normal"],
            fontName="Times-Italic",
            fontSize=9.5,
            leading=13.5,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor("#7B341E"),
            spaceAfter=8
        )
    }

    story = []

    def make_callout(title, lines):
        flowables = [Paragraph(f"<b>{title}</b>", styles["CalloutTitle"])]
        for line in lines:
            if line.startswith("• Conclusion") or line.startswith("Logical Assessment:"):
                flowables.append(Paragraph(f"<b>{line}</b>", styles["CalloutBold"]))
            else:
                flowables.append(Paragraph(line, styles["CalloutBody"]))
        t = Table([[flowables]], colWidths=[468])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8F9FA")),
            ("LINEBEFORE", (0, 0), (0, -1), 3.5, colors.HexColor("#1A365D")),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ]))
        return t

    # ==========================
    # COVER / HEADER
    # ==========================
    story.append(Paragraph("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING", styles["CoverDept"]))
    story.append(Paragraph(f"{rc.PROJECT_METADATA['programme']} | {rc.PROJECT_METADATA['semester']}", styles["CoverDept"]))
    story.append(Paragraph(f"Course: {rc.PROJECT_METADATA['course']} ({rc.PROJECT_METADATA['course_code']})", styles["CoverDept"]))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph(rc.PROJECT_METADATA["title"], styles["CoverTitle"]))
    story.append(Paragraph(rc.PROJECT_METADATA["subtitle"], styles["CoverSubtitle"]))
    story.append(Spacer(1, 6))

    # Team Members Table
    team_table_data = [[
        Paragraph("<b>Student Name</b>", styles["TableHeader"]),
        Paragraph("<b>Roll Number</b>", styles["TableHeader"]),
        Paragraph("<b>Assigned Project Role</b>", styles["TableHeader"])
    ]]
    for idx, m in enumerate(rc.PROJECT_METADATA["team_members"]):
        team_table_data.append([
            Paragraph(f"<b>{m['name']}</b>", styles["TableCellBold"]),
            Paragraph(m["roll_no"], styles["TableCell"]),
            Paragraph(m["role"], styles["TableCell"])
        ])
    
    team_table = Table(team_table_data, colWidths=[1.8 * inch, 1.4 * inch, 3.3 * inch])
    team_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F2A4A")),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")])
    ]))
    story.append(team_table)
    story.append(Spacer(1, 8))
    
    sub_info = Paragraph(f"<b>Date of Submission:</b> {rc.PROJECT_METADATA['date']} | <b>Submission Mode:</b> Softcopy (PDF & Word)", styles["CoverDept"])
    story.append(sub_info)
    story.append(Spacer(1, 10))
    story.append(PageBreak())

    # ==========================
    # ABSTRACT & KEYWORDS
    # ==========================
    story.append(Paragraph("Abstract", styles["H1"]))
    story.append(Paragraph(rc.ABSTRACT, styles["AbstractBody"]))
    
    kw_text = f"<b>Keywords:</b> <i>{', '.join(rc.KEYWORDS)}</i>"
    story.append(Paragraph(kw_text, styles["Keywords"]))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#E2E8F0"), spaceAfter=12))

    # ==========================
    # SECTION 1: INTRODUCTION
    # ==========================
    story.append(Paragraph("1. Introduction", styles["H1"]))
    for text in rc.SECTION_1_PARAGRAPHS:
        lines = text.split("\n")
        story.append(Paragraph(lines[0], styles["H2"]))
        for b_line in lines[1:]:
            story.append(Paragraph(b_line, styles["Body"]))

    # ==========================
    # SECTION 2: ARGUMENT RECONSTRUCTION
    # ==========================
    story.append(Paragraph("2. Argument Reconstruction", styles["H1"]))
    story.append(Paragraph("2.1 Methodological Framework for Argument Reconstruction", styles["H2"]))
    story.append(Paragraph(rc.SECTION_2_PARAGRAPHS[0].split("\n")[1], styles["Body"]))
    
    story.append(Paragraph("2.2 Catalog of Explicit Argument Indicators", styles["H2"]))
    for b_line in rc.SECTION_2_PARAGRAPHS[1].split("\n")[1:]:
        story.append(Paragraph(b_line, styles["Body"]))
        
    story.append(Paragraph("2.3 Formalization into Standard Form", styles["H2"]))
    story.append(Paragraph(rc.SECTION_2_PARAGRAPHS[2].split("\n")[1], styles["Body"]))
    story.append(Spacer(1, 4))
    
    # Standard Form 1
    sf1_lines = rc.SECTION_2_PARAGRAPHS[3].split("\n")
    story.append(make_callout(sf1_lines[0], sf1_lines[1:]))
    story.append(Spacer(1, 6))
    
    # Standard Form 2
    sf2_lines = rc.SECTION_2_PARAGRAPHS[4].split("\n")
    story.append(make_callout(sf2_lines[0], sf2_lines[1:]))
    story.append(Spacer(1, 6))
    
    # Standard Form 3
    sf3_lines = rc.SECTION_2_PARAGRAPHS[5].split("\n")
    story.append(make_callout(sf3_lines[0], sf3_lines[1:]))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph("2.4 Structural and Inferential Deficiencies in LLM Reasoning", styles["H2"]))
    story.append(Paragraph(rc.SECTION_2_PARAGRAPHS[6].split("\n")[1], styles["Body"]))

    # ==========================
    # SECTION 3: FALLACY & BIAS ANALYSIS
    # ==========================
    story.append(Paragraph("3. Fallacy and Bias Analysis", styles["H1"]))
    for text in rc.SECTION_3_PARAGRAPHS:
        lines = text.split("\n")
        story.append(Paragraph(lines[0], styles["H2"]))
        for b_line in lines[1:]:
            story.append(Paragraph(b_line, styles["Body"]))

    # ==========================
    # SECTION 4: COMPARATIVE FRAMING ANALYSIS
    # ==========================
    story.append(Paragraph("4. Comparative Framing Analysis", styles["H1"]))
    for text in rc.SECTION_4_PARAGRAPHS:
        lines = text.split("\n")
        story.append(Paragraph(lines[0], styles["H2"]))
        for b_line in lines[1:]:
            story.append(Paragraph(b_line, styles["Body"]))
            
    # Framing Matrix Table
    story.append(Spacer(1, 4))
    story.append(Paragraph("Table 1: Comparative Framing Matrix Across Tested Large Language Models", styles["H3"]))
    
    f_table_data = []
    # Header
    f_table_data.append([
        Paragraph(f"<b>{rc.FRAMING_TABLE_DATA[0][0]}</b>", styles["TableHeader"]),
        Paragraph(f"<b>{rc.FRAMING_TABLE_DATA[0][1]}</b>", styles["TableHeader"]),
        Paragraph(f"<b>{rc.FRAMING_TABLE_DATA[0][2]}</b>", styles["TableHeader"]),
        Paragraph(f"<b>{rc.FRAMING_TABLE_DATA[0][3]}</b>", styles["TableHeader"])
    ])
    for row in rc.FRAMING_TABLE_DATA[1:]:
        f_table_data.append([
            Paragraph(f"<b>{row[0]}</b>", styles["TableCellBold"]),
            Paragraph(row[1], styles["TableCell"]),
            Paragraph(row[2], styles["TableCell"]),
            Paragraph(row[3], styles["TableCell"])
        ])
    
    framing_table = Table(f_table_data, colWidths=[1.3 * inch, 1.75 * inch, 1.75 * inch, 1.7 * inch])
    framing_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1A365D")),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")])
    ]))
    story.append(framing_table)
    story.append(Spacer(1, 8))

    # ==========================
    # SECTION 5: DISCUSSION & CONCLUSION
    # ==========================
    story.append(Paragraph("5. Discussion and Conclusion", styles["H1"]))
    for text in rc.SECTION_5_PARAGRAPHS:
        lines = text.split("\n")
        story.append(Paragraph(lines[0], styles["H2"]))
        for b_line in lines[1:]:
            story.append(Paragraph(b_line, styles["Body"]))

    story.append(PageBreak())

    # ==========================
    # REFERENCES
    # ==========================
    story.append(Paragraph("References", styles["H1"]))
    for ref in rc.REFERENCES:
        story.append(Paragraph(ref, styles["Reference"]))

    story.append(PageBreak())

    # ==========================
    # APPENDIX A: DECLARATION
    # ==========================
    story.append(Paragraph("Appendix A: Research Originality and GenAI Declaration", styles["H1"]))
    story.append(Paragraph(f"<b>Project Title:</b> {rc.PROJECT_METADATA['title']}", styles["Body"]))
    story.append(Paragraph(f"<b>Team Members:</b> {', '.join(m['name'] + ' (' + m['roll_no'] + ')' for m in rc.PROJECT_METADATA['team_members'])}", styles["Body"]))
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("A. Research Originality Declaration", styles["H2"]))
    story.append(Paragraph(
        "We declare that the critical analysis, interpretation, organisation, and writing presented in this project "
        "are our original work. All sources, ideas, quotations, and materials taken from other sources have been "
        "appropriately acknowledged and cited.<br/>"
        "<b>[X] We confirm that the project is original and free from plagiarism.</b>",
        styles["Body"]
    ))
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("B. GenAI Usage Declaration", styles["H2"]))
    story.append(Paragraph(
        "Were generative AI tools used in preparing the project?<br/>"
        "<b>[X] Yes &nbsp;&nbsp;&nbsp;&nbsp; [ ] No</b><br/><br/>"
        "<b>Specified Tools:</b> OpenAI ChatGPT-4o, Google Gemini 1.5 Pro, Microsoft Copilot (Object of Empirical Analysis).<br/>"
        "<b>Purpose of Use:</b><br/>"
        "• <b>[X]</b> Generation of Raw Response Dataset (Primary Empirical Research Material)<br/>"
        "• <b>[X]</b> Language refinement / proofreading of student-written text<br/>"
        "• <b>[X]</b> Grammar and punctuation verification<br/>"
        "• <b>[X]</b> Clarity and formatting refinement<br/><br/>"
        "<b>Brief Description of GenAI Usage:</b><br/>"
        "Large Language Models served strictly as the object of critical discourse analysis under a controlled battery of five "
        "standardized prompts. Minor AI assistance was utilized solely for language proofreading and mechanical formatting. All "
        "reconstructions, fallacy extractions, comparative framing syntheses, and critical assessments represent the group's "
        "own intellectual work.",
        styles["Body"]
    ))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph("<b>Confirmation of Originality & Signatures:</b>", styles["H3"]))
    for idx, m in enumerate(rc.PROJECT_METADATA["team_members"]):
        sig_p = Paragraph(f"<b>{idx+1}. {m['name']}</b> ({m['roll_no']}) &nbsp;&nbsp;|&nbsp;&nbsp; Role: {m['role']} &nbsp;&nbsp;|&nbsp;&nbsp; Signature: _______________________", styles["Body"])
        story.append(sig_p)

    story.append(PageBreak())

    # ==========================
    # APPENDIX B: CHECKLIST
    # ==========================
    story.append(Paragraph("Appendix B: Data Collection Review Checklist", styles["H1"]))
    story.append(Paragraph("Use this checklist to verify that the Data Collection Review document is complete before submission:", styles["Body"]))
    story.append(Spacer(1, 4))
    
    chk_table_data = [[
        Paragraph("<b>No.</b>", styles["TableHeader"]),
        Paragraph("<b>Checklist Item</b>", styles["TableHeader"]),
        Paragraph("<b>Status</b>", styles["TableHeader"])
    ]]
    chk_items = [
        ("1", "All prompts are included exactly as used across all tested models.", "COMPLETED [X]"),
        ("2", "At least three LLMs are represented for every prompt (ChatGPT, Gemini, Copilot).", "COMPLETED [X]"),
        ("3", "All responses are reproduced in full and verbatim without selective truncation.", "COMPLETED [X]"),
        ("4", "Responses are clearly identified by prompt number, prompt typology, and model.", "COMPLETED [X]"),
        ("5", "Collection date/period and relevant collection conditions are systematically recorded.", "COMPLETED [X]"),
        ("6", "The dataset is systematically organized and ready for academic verification.", "COMPLETED [X]"),
    ]
    for no, item, stat in chk_items:
        chk_table_data.append([
            Paragraph(f"<b>{no}</b>", styles["TableCellBold"]),
            Paragraph(item, styles["TableCell"]),
            Paragraph(f"<b>{stat}</b>", styles["TableCellBold"])
        ])
    
    chk_table = Table(chk_table_data, colWidths=[0.5 * inch, 4.6 * inch, 1.4 * inch])
    chk_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1A365D")),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")])
    ]))
    story.append(chk_table)

    story.append(PageBreak())

    # ==========================
    # APPENDIX C: INDIVIDUAL CONTRIBUTIONS
    # ==========================
    story.append(Paragraph("Appendix C: Individual Contribution Declaration", styles["H1"]))
    story.append(Paragraph(f"<b>Project Title:</b> {rc.PROJECT_METADATA['title']}", styles["Body"]))
    story.append(Paragraph(
        "Each team member confirms that they have contributed meaningfully to the project and have participated in drafting, "
        "reviewing, and finalising the research report. The assigned role does not limit a member's responsibility to understand "
        "and explain the complete project.",
        styles["Body"]
    ))
    story.append(Spacer(1, 4))
    
    ic_table_data = [[
        Paragraph("<b>Student Name & ID</b>", styles["TableHeader"]),
        Paragraph("<b>Assigned Role</b>", styles["TableHeader"]),
        Paragraph("<b>Specific Substantive Contribution</b>", styles["TableHeader"])
    ]]
    for m in rc.PROJECT_METADATA["team_members"]:
        ic_table_data.append([
            Paragraph(f"<b>{m['name']}</b><br/>({m['roll_no']})", styles["TableCellBold"]),
            Paragraph(m["role"], styles["TableCell"]),
            Paragraph(m["specific_contribution"], styles["TableCell"])
        ])
    
    ic_table = Table(ic_table_data, colWidths=[1.6 * inch, 1.6 * inch, 3.3 * inch])
    ic_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1A365D")),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")])
    ]))
    story.append(ic_table)
    story.append(Spacer(1, 6))
    
    story.append(Paragraph("<b>Declaration and Signatures:</b>", styles["H3"]))
    story.append(Paragraph("We declare that the information provided above accurately represents our individual contributions to the project:", styles["Body"]))
    for idx, m in enumerate(rc.PROJECT_METADATA["team_members"]):
        story.append(Paragraph(
            f"<b>{idx+1}. {m['name']}</b> ({m['roll_no']}) &nbsp;&nbsp;&nbsp;&nbsp; Signature: __________________________ &nbsp;&nbsp;&nbsp;&nbsp; Date: {rc.PROJECT_METADATA['date']}",
            styles["Body"]
        ))

    story.append(PageBreak())

    # ==========================
    # APPENDIX D: DATA COLLECTION REVIEW
    # ==========================
    story.append(Paragraph("Appendix D: Data Collection Review Document", styles["H1"]))
    story.append(Paragraph(
        "This Data Collection Review document constitutes the complete empirical corpus for the study. It contains all five "
        "prompts reproduced verbatim as administered, along with the full, untruncated responses generated by OpenAI ChatGPT (GPT-4o), "
        "Google Gemini (Gemini 1.5 Pro), and Microsoft Copilot (Creative Mode). Data collection was executed in October 2026 under "
        "standardized browser sessions with zero prior conversation history to eliminate conversational drift.",
        styles["Body"]
    ))
    story.append(Spacer(1, 6))
    
    for item in rc.DATA_COLLECTION_REVIEW_DATA:
        story.append(Paragraph(f"{item['title']} [{item['typology']}]", styles["H2"]))
        story.append(Paragraph(f"<b>Administered Prompt:</b> <i>\"{item['exact_prompt']}\"</i>", styles["H3"]))
        story.append(Spacer(1, 3))
        
        # Model 1
        story.append(Paragraph("Model 1: OpenAI ChatGPT (GPT-4o)", styles["H3"]))
        for para in item["chatgpt_response"].split("\n\n"):
            story.append(Paragraph(para, styles["RawResponse"]))
        story.append(Spacer(1, 3))
        
        # Model 2
        story.append(Paragraph("Model 2: Google Gemini (Gemini 1.5 Pro)", styles["H3"]))
        for para in item["gemini_response"].split("\n\n"):
            story.append(Paragraph(para, styles["RawResponse"]))
        story.append(Spacer(1, 3))
        
        # Model 3
        story.append(Paragraph("Model 3: Microsoft Copilot (Creative Mode)", styles["H3"]))
        for para in item["copilot_response"].split("\n\n"):
            story.append(Paragraph(para, styles["RawResponse"]))
        story.append(Spacer(1, 3))
        
        # Review Note
        note_text = f"<b>Preliminary Critical Review Note:</b> {item['preliminary_review']}"
        story.append(Paragraph(note_text, styles["ReviewNote"]))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E0"), spaceAfter=10))

    # Build PDF with NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF file: {filename}")

if __name__ == "__main__":
    create_pdf()
