from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [ROOT / "backend" / "data" / "demo_documents", ROOT / "frontend" / "public" / "demo"]

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=9, leading=12, textColor=colors.HexColor("#374151")))
styles.add(ParagraphStyle(name="Section", parent=styles["Heading2"], fontSize=14, leading=18, spaceBefore=10, spaceAfter=6, textColor=colors.HexColor("#0f766e")))


def para(text: str, style: str = "BodyText") -> Paragraph:
    return Paragraph(text, styles[style])


def table(rows: list[list[str]]) -> Table:
    rendered = [[para(cell, "Small") for cell in row] for row in rows]
    result = Table(rendered, repeatRows=1, colWidths=[1.65 * inch] + [2.65 * inch] * (len(rows[0]) - 1))
    result.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#ccfbf1")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#115e59")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#99f6e4")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return result


def build_medical(path: Path) -> None:
    story = [para("PrivatePulse AI — Synthetic Medical Report", "Title"), para("Demonstration document only. This fictional record is safe for local product demos and testing.", "Small"), Spacer(1, 14), para("Patient demographics", "Section"), para("Patient: Alex Johnson<br/>Date of birth: 04/17/1988<br/>Record identifier: DEMO-MED-001<br/>SSN: 123-45-6789", "BodyText"), para("Diagnosis and medications", "Section"), para("Primary diagnosis: Type 2 Diabetes Mellitus. The care plan emphasizes nutrition, regular activity, and adherence to the medication schedule.", "BodyText"), table([["Medication", "Dosage", "Instructions"], ["Metformin", "500 mg", "Twice daily with meals"], ["Lisinopril", "10 mg", "Once daily in the morning"], ["Atorvastatin", "20 mg", "Once daily in the evening"]]), para("Laboratory results", "Section"), table([["Test", "Result", "Reference / note"], ["HbA1c", "7.2%", "Above target; recheck in 3 months"], ["Fasting blood glucose", "142 mg/dL", "Elevated"], ["Total cholesterol", "188 mg/dL", "Within target range"], ["LDL cholesterol", "96 mg/dL", "At treatment goal"]]), para("Doctor's notes and recommendations", "Section"), para("Continue current medications, monitor fasting glucose at home, schedule a nutrition consultation, and bring the glucose log to the next visit. Seek medical care promptly for persistent symptoms of high or low blood sugar.", "BodyText"), para("Follow-up", "Section"), para("Next follow-up appointment: October 14, 2026. This document contains fictional names, dates, and values.", "BodyText")]
    SimpleDocTemplate(str(path), pagesize=letter, rightMargin=0.7 * inch, leftMargin=0.7 * inch, topMargin=0.65 * inch, bottomMargin=0.65 * inch).build(story)


def build_financial(path: Path) -> None:
    story = [para("PrivatePulse AI — Synthetic Quarterly Financial Statement", "Title"), para("Demonstration document only. All figures and identifiers are fictional.", "Small"), Spacer(1, 14), para("Quarterly performance", "Section"), table([["Metric", "Q3 2026", "Q4 2026"], ["Revenue", "$480,000", "$560,000"], ["Cost of goods sold", "$192,000", "$218,000"], ["Operating expenses", "$210,000", "$226,000"], ["Net profit", "$78,000", "$116,000"]]), para("Balance sheet summary", "Section"), table([["Item", "Amount"], ["Cash and equivalents", "$312,450"], ["Accounts receivable", "$184,200"], ["Total assets", "$1,042,700"], ["Total liabilities", "$418,900"], ["Shareholders' equity", "$623,800"]]), para("Sensitive identifiers", "Section"), para("Operating account: acct 123456789012<br/>Routing number: 021000021<br/>Statement reference: DEMO-FIN-004", "BodyText"), para("Cash flow analysis", "Section"), para("Operating activities generated $148,000 in cash during Q4. Investing activities used $42,000 for equipment. Financing activities used $18,000 for distributions, resulting in a net increase of $88,000.", "BodyText"), para("Auditor notes", "Section"), para("The statement is presented for demonstration purposes only. The auditor found no material exceptions in the fictional records supplied for this sample.", "BodyText")]
    SimpleDocTemplate(str(path), pagesize=letter, rightMargin=0.7 * inch, leftMargin=0.7 * inch, topMargin=0.65 * inch, bottomMargin=0.65 * inch).build(story)


def build_contract(path: Path) -> None:
    story = [para("PrivatePulse AI — Synthetic Service Agreement", "Title"), para("Demonstration document only. This fictional agreement is not legal advice.", "Small"), Spacer(1, 14), para("Parties and service", "Section"), para("This Service Agreement is between Northstar Analytics LLC (the “Provider”) and Cedar Grove Retail Inc. (the “Client”). Provider will deliver monthly data quality reviews, dashboard maintenance, and written recommendations.", "BodyText"), para("Contacts", "Section"), para("Provider contact: legal@northstar.example<br/>Client contact: contracts@cedargrove.example<br/>Agreement reference: DEMO-CON-003", "BodyText"), para("Payment terms", "Section"), table([["Term", "Requirement"], ["Monthly fee", "$4,500 due on the first business day of each month"], ["Invoice timing", "Provider invoices five business days before the due date"], ["Late fee", "1.5% of the unpaid balance per month, where permitted"], ["Reimbursable costs", "Pre-approved expenses supported by receipts"]]), para("Term and termination", "Section"), para("The initial term is twelve months beginning January 1, 2026. Either party may terminate for convenience with thirty days' written notice. Either party may terminate for a material breach if the breach is not cured within fifteen days after written notice.", "BodyText"), para("Confidentiality", "Section"), para("Each party must protect the other party's confidential information using reasonable safeguards, disclose it only to people who need it for the agreement, and return or delete it when the relationship ends, subject to applicable recordkeeping requirements.", "BodyText"), para("Governing law", "Section"), para("This agreement is governed by the laws of the State of Delaware, without regard to conflict-of-law rules. This sample is fictional and should not be used as a contract.", "BodyText")]
    SimpleDocTemplate(str(path), pagesize=letter, rightMargin=0.7 * inch, leftMargin=0.7 * inch, topMargin=0.65 * inch, bottomMargin=0.65 * inch).build(story)


if __name__ == "__main__":
    for target in TARGETS:
        target.mkdir(parents=True, exist_ok=True)
    builders = {"medical-report-sample.pdf": build_medical, "financial-statement-sample.pdf": build_financial, "contract-sample.pdf": build_contract}
    for filename, builder in builders.items():
        for target in TARGETS:
            builder(target / filename)
            print(target / filename)
