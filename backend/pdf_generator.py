from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)
from xml.sax.saxutils import escape

PAPER = colors.HexColor("#F7F6F2")
INK = colors.HexColor("#181818")
MUTED = colors.HexColor("#77726A")
ACCENT = colors.HexColor("#C65D3A")
BORDER = colors.HexColor("#E1DDD5")
WHITE = colors.white


def get_styles():
    return {
        "cover_label": ParagraphStyle(
            "CoverLabel",
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=12,
            textColor=ACCENT,
            tracking=2,
            spaceAfter=14,
        ),
        "title": ParagraphStyle(
            "Title",
            fontName="Helvetica-Bold",
            fontSize=34,
            leading=38,
            textColor=INK,
            spaceAfter=18,
        ),
        "intro": ParagraphStyle(
            "Intro",
            fontName="Helvetica",
            fontSize=13,
            leading=21,
            textColor=MUTED,
            spaceAfter=20,
        ),
        "section_number": ParagraphStyle(
            "SectionNumber",
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=ACCENT,
        ),
        "section_title": ParagraphStyle(
            "SectionTitle",
            fontName="Helvetica-Bold",
            fontSize=19,
            leading=24,
            textColor=INK,
            spaceAfter=10,
        ),
        "body": ParagraphStyle(
            "Body",
            fontName="Helvetica",
            fontSize=11,
            leading=18,
            textColor=MUTED,
        ),
        "checklist": ParagraphStyle(
            "Checklist",
            fontName="Helvetica",
            fontSize=11,
            leading=17,
            textColor=INK,
        ),
        "small": ParagraphStyle(
            "Small",
            fontName="Helvetica",
            fontSize=8,
            leading=11,
            textColor=MUTED,
        ),
    }


GENERATED_DIR = Path(__file__).parent / "generated"
GENERATED_DIR.mkdir(exist_ok=True)

def create_pdf(product, filename):
    styles = get_styles()
    file_path = GENERATED_DIR / filename

    doc = SimpleDocTemplate(
        str(file_path),
        pagesize=A4,
        rightMargin=22 * mm,
        leftMargin=22 * mm,
        topMargin=24 * mm,
        bottomMargin=22 * mm,
        title=product.title,
        author="Niched",
    )

    story = []

    # ─────────────────────────────────────
    # COVER / INTRO
    # ─────────────────────────────────────

    story.append(Spacer(1, 18 * mm))

    story.append(
        Paragraph(
            "NICHED  ·  GENERATED DIGITAL PRODUCT",
            styles["cover_label"],
        )
    )

    story.append(
        Paragraph(
            escape(product.title),
            styles["title"],
        )
    )

    story.append(
        Paragraph(
            escape(product.introduction),
            styles["intro"],
        )
    )

    # Accent divider
    divider = Table(
        [[""]],
        colWidths=[18 * mm],
        rowHeights=[1.2 * mm],
    )

    divider.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), ACCENT),
                ("BOX", (0, 0), (-1, -1), 0, ACCENT),
            ]
        )
    )

    story.append(divider)
    story.append(Spacer(1, 16 * mm))

    # ─────────────────────────────────────
    # SECTIONS
    # ─────────────────────────────────────

    for index, section in enumerate(product.sections, start=1):

        story.append(
            Paragraph(
                f"{index:02d}",
                styles["section_number"],
            )
        )

        story.append(Spacer(1, 3 * mm))

        story.append(
            Paragraph(
                escape(section.title),
                styles["section_title"],
            )
        )

        story.append(
            Paragraph(
                escape(section.content),
                styles["body"],
            )
        )

        story.append(Spacer(1, 12 * mm))

    # ─────────────────────────────────────
    # CHECKLIST
    # ─────────────────────────────────────

    checklist_header = Table(
        [
            [
                Paragraph(
                    "CHECKLIST",
                    styles["cover_label"],
                )
            ]
        ],
        colWidths=[doc.width],
    )

    checklist_header.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), WHITE),
                ("BOX", (0, 0), (-1, -1), 0.7, BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(Spacer(1, 4 * mm))

    story.append(checklist_header)

    checklist_rows = []

    for index, item in enumerate(product.checklist, start=1):
        checklist_rows.append(
            [
                Paragraph(
                    "✓",
                    ParagraphStyle(
                        "Check",
                        parent=styles["checklist"],
                        textColor=ACCENT,
                        fontName="Helvetica-Bold",
                    ),
                ),
                Paragraph(
                    escape(item),
                    styles["checklist"],
                ),
            ]
        )

    if checklist_rows:
        checklist_table = Table(
            checklist_rows,
            colWidths=[10 * mm, doc.width - 10 * mm],
        )

        checklist_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), WHITE),
                    ("BOX", (0, 0), (-1, -1), 0.7, BORDER),
                    ("INNERGRID", (0, 0), (-1, -1), 0.4, BORDER),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 9),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
                ]
            )
        )

        story.append(checklist_table)

    # ─────────────────────────────────────
    # CONCLUSION
    # ─────────────────────────────────────

    story.append(Spacer(1, 16 * mm))

    story.append(
        Paragraph(
            "CONCLUSION",
            styles["cover_label"],
        )
    )

    story.append(
        Paragraph(
            escape(product.conclusion),
            styles["body"],
        )
    )

    # ─────────────────────────────────────
    # FOOTER
    # ─────────────────────────────────────

    def add_footer(canvas, doc):
        canvas.saveState()

        canvas.setStrokeColor(BORDER)
        canvas.setLineWidth(0.5)

        canvas.line(
            doc.leftMargin,
            14 * mm,
            A4[0] - doc.rightMargin,
            14 * mm,
        )

        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(MUTED)

        canvas.drawString(
            doc.leftMargin,
            9 * mm,
            "NICHED",
        )

        canvas.drawRightString(
            A4[0] - doc.rightMargin,
            9 * mm,
            f"{doc.page}",
        )

        canvas.restoreState()

    doc.build(
        story,
        onFirstPage=add_footer,
        onLaterPages=add_footer,
    )
