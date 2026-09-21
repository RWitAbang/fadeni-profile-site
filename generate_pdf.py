"""
Generates fadeni-executive-profile.pdf from content.json.

Mirrors the structure and section order of index.html/styles.css exactly,
so the PDF and the website stay in sync as the single source of truth
(content.json) changes. Re-run this script after any content.json edit.

Known limitation: this environment could not download the Georgia/Arial
webfonts used on the site, so the PDF uses reportlab's built-in
Times-Roman/Times-Bold and Helvetica as close substitutes. Swap in real
font files (see FONT NOTE below) for a pixel-perfect match before launch.
"""

import json
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image
)
from reportlab.lib.utils import ImageReader
import os

INK = HexColor("#1A1A1A")
BLACK = HexColor("#000000")
GREY_DARK = HexColor("#555555")
GREY_MID = HexColor("#888888")
GREY_LINE = HexColor("#E5E5E5")
CARD_BG = HexColor("#F9F9F9")

def esc(text):
    if text is None:
        return ""
    return (str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

with open("content.json") as f:
    data = json.load(f)

doc = SimpleDocTemplate(
    "fadeni-executive-profile.pdf",
    pagesize=LETTER,
    topMargin=0.85 * inch,
    bottomMargin=0.85 * inch,
    leftMargin=0.75 * inch,
    rightMargin=0.75 * inch,
    title=f"{data['name']} — Executive Profile",
)

styles = {
    "SectionNum": ParagraphStyle(
        "SectionNum", fontName="Helvetica-Bold", fontSize=8.5, leading=11,
        textColor=GREY_MID, spaceAfter=4, tracking=1,
    ),
    "H2": ParagraphStyle(
        "H2", fontName="Times-Roman", fontSize=20, leading=24,
        textColor=BLACK, spaceAfter=14, spaceBefore=0,
    ),
    "HeroTitle": ParagraphStyle(
        "HeroTitle", fontName="Times-Roman", fontSize=34, leading=38,
        textColor=BLACK, spaceAfter=12,
    ),
    "HeroSubtitle": ParagraphStyle(
        "HeroSubtitle", fontName="Helvetica", fontSize=12, leading=17,
        textColor=GREY_DARK, spaceAfter=6,
    ),
    "LeadP": ParagraphStyle(
        "LeadP", fontName="Times-Roman", fontSize=13, leading=19,
        textColor=INK, spaceAfter=10,
    ),
    "BodyP": ParagraphStyle(
        "BodyP", fontName="Helvetica", fontSize=9.5, leading=15,
        textColor=GREY_DARK, spaceAfter=8,
    ),
    "DriverTitle": ParagraphStyle(
        "DriverTitle", fontName="Times-Roman", fontSize=13, leading=16,
        textColor=BLACK, spaceAfter=6,
    ),
    "DriverDesc": ParagraphStyle(
        "DriverDesc", fontName="Helvetica", fontSize=8.5, leading=13,
        textColor=GREY_DARK,
    ),
    "FootTitle": ParagraphStyle(
        "FootTitle", fontName="Times-Roman", fontSize=13, leading=16,
        textColor=BLACK, spaceAfter=2,
    ),
    "FootRole": ParagraphStyle(
        "FootRole", fontName="Helvetica-Bold", fontSize=7.5, leading=11,
        textColor=GREY_MID, spaceAfter=4,
    ),
    "FootDesc": ParagraphStyle(
        "FootDesc", fontName="Helvetica", fontSize=9.5, leading=14,
        textColor=HexColor("#444444"),
    ),
    "EduRow": ParagraphStyle(
        "EduRow", fontName="Helvetica", fontSize=9, leading=13, textColor=HexColor("#333333"),
    ),
    "RecAward": ParagraphStyle(
        "RecAward", fontName="Helvetica", fontSize=10.5, leading=14, textColor=BLACK,
    ),
    "RecMeta": ParagraphStyle(
        "RecMeta", fontName="Helvetica", fontSize=8.5, leading=13, textColor=GREY_MID,
    ),
    "ContactP": ParagraphStyle(
        "ContactP", fontName="Times-Roman", fontSize=11.5, leading=17,
        textColor=HexColor("#222222"), spaceAfter=10,
    ),
    "FooterNote": ParagraphStyle(
        "FooterNote", fontName="Helvetica", fontSize=7.5, leading=11, textColor=GREY_MID,
    ),
}

story = []

# ---------- HERO ----------
story.append(Paragraph("EXECUTIVE PROFILE &amp; STATEMENT", styles["SectionNum"]))
story.append(Spacer(1, 4))
story.append(Paragraph(esc(data["name"]), styles["HeroTitle"]))
story.append(Paragraph(esc(data["heroSubtitle"]), styles["HeroSubtitle"]))
story.append(Spacer(1, 22))
story.append(HRFlowable(width="100%", thickness=0.75, color=GREY_LINE))
story.append(Spacer(1, 22))

# ---------- 01 EXECUTIVE PROFILE (with portrait, if supplied) ----------
story.append(Paragraph("01 — OVERVIEW", styles["SectionNum"]))
story.append(Paragraph("Executive Profile", styles["H2"]))
ep = data["executiveProfile"]

text_flowables = [Paragraph(esc(ep[0]), styles["LeadP"])]
for para in ep[1:]:
    text_flowables.append(Paragraph(esc(para), styles["BodyP"]))

photo_info = data.get("photo", {})
photo_path = photo_info.get("url")
if photo_path and os.path.exists(photo_path):
    photo_col_width = 1.7 * inch
    text_col_width = LETTER[0] - 1.5 * inch - photo_col_width - 14
    img_reader = ImageReader(photo_path)
    iw, ih = img_reader.getSize()
    display_h = photo_col_width * (ih / iw)
    photo_flowable = Image(photo_path, width=photo_col_width, height=display_h)
    profile_table = Table(
        [[photo_flowable, text_flowables]],
        colWidths=[photo_col_width, text_col_width],
    )
    profile_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, 0), 0),
        ("LEFTPADDING", (1, 0), (1, 0), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(profile_table)
else:
    for f in text_flowables:
        story.append(f)
    story.append(Spacer(1, 6))
    note = ("Portrait pending — see build notes; the printed profile will include a "
            "confirmed headshot alongside this section once supplied.")
    story.append(Paragraph(f"<i>{esc(note)}</i>", styles["FooterNote"]))

story.append(Spacer(1, 24))
story.append(HRFlowable(width="100%", thickness=0.75, color=GREY_LINE))
story.append(Spacer(1, 22))

# ---------- 02 STRATEGIC VALUE DRIVERS ----------
story.append(Paragraph("02 — CAPABILITY", styles["SectionNum"]))
story.append(Paragraph("Strategic Value Drivers", styles["H2"]))
drivers = data["strategicValueDrivers"]
driver_cells = []
row = []
for i, d in enumerate(drivers, 1):
    cell = [
        Paragraph(f"0{i}", ParagraphStyle("idx", fontName="Helvetica-Bold", fontSize=8, textColor=GREY_MID, spaceAfter=6)),
        Paragraph(esc(d["title"]), styles["DriverTitle"]),
        Paragraph(esc(d["desc"]), styles["DriverDesc"]),
    ]
    row.append(cell)
    if len(row) == 2:
        driver_cells.append(row)
        row = []
if row:
    row.append([Paragraph("", styles["DriverDesc"])])
    driver_cells.append(row)

col_width = (LETTER[0] - 1.5 * inch - 12) / 2
for pair in driver_cells:
    t = Table([pair], colWidths=[col_width, col_width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CARD_BG),
        ("BOX", (0, 0), (0, 0), 0.5, GREY_LINE),
        ("BOX", (1, 0), (1, 0), 0.5, GREY_LINE) if len(pair) > 1 else ("BOX", (0,0),(0,0),0,GREY_LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

story.append(Spacer(1, 14))
story.append(HRFlowable(width="100%", thickness=0.75, color=GREY_LINE))
story.append(Spacer(1, 22))

# ---------- 03 SECTOR FOOTPRINT ----------
story.append(Paragraph("03 — OPERATIONS &amp; LEADERSHIP", styles["SectionNum"]))
story.append(Paragraph("Sector Footprint", styles["H2"]))
for f in data["sectorFootprint"]:
    title = esc(f["title"])
    if not f["current"]:
        title += ' <font size="7" color="#999999">[FORMER]</font>'
    story.append(Paragraph(title, styles["FootTitle"]))
    story.append(Paragraph(f"{esc(f['org'])} &nbsp;·&nbsp; {esc(f['period'])}", styles["FootRole"]))
    story.append(Paragraph(f"<b>{esc(f['role'])}</b> — {esc(f['detail'])}", styles["FootDesc"]))
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GREY_LINE))
    story.append(Spacer(1, 12))

story.append(Spacer(1, 10))

# ---------- 04 EDUCATION & EXECUTIVE DEVELOPMENT ----------
story.append(Paragraph("04 — CREDENTIALS", styles["SectionNum"]))
story.append(Paragraph("Education &amp; Executive Development", styles["H2"]))
edu_rows = []
for e in data["education"]:
    edu_rows.append([
        Paragraph(f"<b>{esc(e['institution'])}</b>", styles["EduRow"]),
        Paragraph(esc(e["credential"]), styles["EduRow"]),
    ])
t = Table(edu_rows, colWidths=[3.1 * inch, 3.1 * inch])
t.setStyle(TableStyle([
    ("LINEBELOW", (0, 0), (-1, -1), 0.5, GREY_LINE),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
]))
story.append(t)
story.append(Spacer(1, 22))
story.append(HRFlowable(width="100%", thickness=0.75, color=GREY_LINE))
story.append(Spacer(1, 22))

# ---------- 05 RECOGNITION ----------
story.append(Paragraph("05 — HONORS", styles["SectionNum"]))
story.append(Paragraph("Recognition", styles["H2"]))
rec_rows = []
for r in data["recognition"]:
    meta = f"{esc(r['year'])}, {esc(r['issuer'])}" if r["issuer"] else esc(r["year"])
    rec_rows.append([
        Paragraph(esc(r["award"]), styles["RecAward"]),
        Paragraph(meta, styles["RecMeta"]),
    ])
t = Table(rec_rows, colWidths=[4.4 * inch, 1.8 * inch])
t.setStyle(TableStyle([
    ("LINEBELOW", (0, 0), (-1, -1), 0.5, GREY_LINE),
    ("TOPPADDING", (0, 0), (-1, -1), 10),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ("ALIGN", (1, 0), (1, -1), "RIGHT"),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
]))
story.append(t)
story.append(Spacer(1, 22))
story.append(HRFlowable(width="100%", thickness=0.75, color=GREY_LINE))
story.append(Spacer(1, 22))

# ---------- 06 CONTACT ----------
story.append(Paragraph("06 — GET IN TOUCH", styles["SectionNum"]))
story.append(Paragraph("Engagements &amp; Inquiries", styles["H2"]))
c = data["contact"]
main_site_display = c["mainSite"].replace("https://", "")
story.append(Paragraph(
    f"For strategic collaborations, direct advisory, or general corporate matters, "
    f"please direct all communication to <u>{esc(c['businessEmail'])}</u>.",
    styles["ContactP"],
))
story.append(Paragraph(
    f"To explore ongoing philanthropic initiatives, personal foundation work, and "
    f"broader venture investments, visit <u>{esc(main_site_display)}</u>.",
    styles["ContactP"],
))
story.append(Paragraph(
    "You can also connect professionally via <u>LinkedIn</u>.",
    styles["ContactP"],
))

doc.build(story)
print("Wrote fadeni-executive-profile.pdf")

# FONT NOTE:
# To match the site's Georgia/Arial typography exactly, register real font
# files with reportlab.pdfbase.pdfmetrics.registerFont / TTFont and swap the
# fontName values above (Times-Roman -> Georgia, Helvetica -> Arial) once
# licensed font files are available in this environment.
