import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor as PPTXColor

from google.cloud import storage

GCS_BUCKET_NAME = "databricks-ops-optimizer-qwiklabs-gcp-02-7222a271d6bd"
PROJECT_ID = "qwiklabs-gcp-02-7222a271d6bd"

# --- 1. BUILD WORD DOCUMENT (.docx) ---
def build_docx():
    doc = Document()
    
    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run("Databricks Cluster Intelligence &\nAutonomous Governance Agent")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(26)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(249, 115, 22) # Databricks Orange

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_sub.add_run("Project Highlights, GCP Architecture & FinOps Governance Briefing\nPowered by Google Gemini 2.0 & ADK Agent Engine")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(13)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # 1. Executive Summary
    h1 = doc.add_heading("1. Executive Summary & Value Proposition", level=1)
    h1.runs[0].font.color.rgb = RGBColor(15, 23, 42)

    p_exec = doc.add_paragraph(
        "The Databricks Cluster Intelligence & Autonomous Governance Agent (Databricks Cluster-Intel Agent) is an enterprise-grade AI assistant "
        "built using Google Gemini 2.0 and the Agent Development Kit (ADK). It solves the pressing challenges of cloud compute cost overruns, "
        "unmonitored shadow clusters, and HIPAA/PHI compliance violations in Databricks data platforms.\n\n"
        "By autonomously inspecting cluster configurations, querying System Tables telemetry, predicting 13.3 LTS Photon acceleration speedups, "
        "and right-sizing oversized worker nodes, the agent reduces Databricks compute spend by up to 75% while enforcing strict governance guardrails."
    )
    p_exec.style.font.name = "Arial"

    # 2. Key Capabilities & Highlights
    h2 = doc.add_heading("2. Core Capabilities & Feature Highlights", level=1)
    h2.runs[0].font.color.rgb = RGBColor(15, 23, 42)

    features = [
        ("🛡️ HIPAA Security Policy Governance", "Enforces Single-User compute, Unity Catalog binding, approved LTS Photon runtimes, and No Public IP policies across PHI/HIPAA workloads."),
        ("💰 Autonomous FinOps & Sizing Engine", "Detects idle, un-terminated clusters and derives optimal horizontal and vertical worker scale limits (achieving 8x worker right-sizing savings)."),
        ("⚡ Photon Engine Speedup Prediction", "Analyzes Spark workloads to predict execution acceleration (e.g. 3.4x speedup, 71% latency reduction) and net DBU savings."),
        ("🎥 3D Gemini Omni Motion Video Generation", "Uses Google's gemini-omni-flash-preview model in the global region to generate 3D motion previews of cluster auto-scaling and uploads directly to Cloud Storage."),
        ("📜 Firestore Before vs. After Audit Trail", "Records every sizing mutation and recommendation update with a complete timestamped audit log stored in Google Cloud Firestore."),
        ("🧠 Vertex AI Memory Bank Integration", "Leverages PreloadMemoryTool to remember user profiles, budget preferences, and cost center constraints across sessions.")
    ]

    for title, desc in features:
        p = doc.add_paragraph()
        r_t = p.add_run(f"• {title}: ")
        r_t.bold = True
        r_t.font.color.rgb = RGBColor(14, 165, 233)
        r_d = p.add_run(desc)

    # 3. GCP Architecture & Wiring Table
    h3 = doc.add_heading("3. Google Cloud Architecture & Services Matrix", level=1)
    h3.runs[0].font.color.rgb = RGBColor(15, 23, 42)

    table = doc.add_table(rows=1, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table.rows[0].cells
    hdr_titles = ["GCP Service / Integration", "Resource ID / Configuration", "Implementation & Usage in Code"]
    for i, title in enumerate(hdr_titles):
        hdr_cells[i].text = title
        hdr_cells[i].paragraphs[0].runs[0].font.bold = True
        hdr_cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        shading = parse_xml(r'<w:shd {} w:fill="0F172A"/>'.format(nsdecls('w')))
        hdr_cells[i]._tc.get_or_add_tcPr().append(shading)

    gcp_data = [
        ("Vertex AI Memory Bank", "PreloadMemoryTool & callback", "Cross-session memory of user profile & cost constraints"),
        ("Google Cloud Firestore", "qwiklabs-gcp-02-7222a271d6bd", "databricks_clusters collection & recommendation_history audit logs"),
        ("Google Cloud Storage", "databricks-ops-optimizer...", "Direct streaming upload of generated MP4 video bytes"),
        ("Vertex AI Omni Model", "gemini-omni-flash-preview (global)", "3D motion video generation & tool_context.save_artifact"),
        ("Agent Engine Sandbox", "REasoningEngine resource", "Isolated execution of Python cost modeling scripts"),
    ]

    for service, res_id, usage in gcp_data:
        row_cells = table.add_row().cells
        row_cells[0].text = service
        row_cells[0].paragraphs[0].runs[0].font.bold = True
        row_cells[1].text = res_id
        row_cells[2].text = usage

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # 4. Business Impact Metrics
    h4 = doc.add_heading("4. Quantifiable FinOps & Governance Impact", level=1)
    h4.runs[0].font.color.rgb = RGBColor(15, 23, 42)

    metrics = [
        ("Monthly DBU Spend Reduction", "Up to 75% cost savings per cluster ($2,840/mo -> $710/mo via worker right-sizing)."),
        ("Query Latency Acceleration", "71% reduction in execution time (45 mins -> 13 mins) via Photon engine upgrade."),
        ("Compliance Audit Coverage", "100% policy violation detection across HIPAA/PHI cluster configurations."),
        ("Auditability & Governance", "Complete Before/After state historical audit trail stored persistently in Firestore.")
    ]

    for label, val in metrics:
        p = doc.add_paragraph()
        r1 = p.add_run(f"• {label}: ")
        r1.bold = True
        p.add_run(val)

    docx_path = "/tmp/databricks_cluster_intel_highlights.docx"
    doc.save(docx_path)
    print("Saved Word Document at:", docx_path)
    return docx_path


# --- 2. BUILD POWERPOINT PRESENTATION (.pptx) ---
def build_pptx():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]

    BG_DARK = PPTXColor(15, 23, 42)
    PANEL_BG = PPTXColor(30, 41, 59)
    ACCENT_ORANGE = PPTXColor(249, 115, 22)
    ACCENT_BLUE = PPTXColor(14, 165, 233)
    TEXT_WHITE = PPTXColor(248, 250, 252)
    TEXT_MUTED = PPTXColor(148, 163, 184)
    GOLD_AMBER = PPTXColor(245, 158, 11)
    GREEN_SUCCESS = PPTXColor(34, 197, 94)

    def set_slide_background(slide):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = BG_DARK

    def add_header(slide, title_text, category_text="DATABRICKS CLUSTER INTELLIGENCE"):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.8))
        tf = tb.text_frame
        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(12)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_ORANGE
        
        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE

    # SLIDE 1: Title Slide
    slide1 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide1)
    
    tb1 = slide1.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.3), Inches(3.5))
    tf1 = tb1.text_frame
    p1 = tf1.paragraphs[0]
    p1.text = "Databricks Cluster Intelligence &\nAutonomous Governance Agent"
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    
    p2 = tf1.add_paragraph()
    p2.text = "Autonomous FinOps, HIPAA Security Policy Governance & 3D Gemini Omni Video Generation"
    p2.font.size = Pt(20)
    p2.font.color.rgb = ACCENT_ORANGE
    
    p3 = tf1.add_paragraph()
    p3.text = "\nPowered by Google Gemini 2.0 & ADK Agent Engine on Vertex AI"
    p3.font.size = Pt(16)
    p3.font.italic = True
    p3.font.color.rgb = TEXT_MUTED

    # SLIDE 2: Core Capabilities
    slide2 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide2)
    add_header(slide2, "Core Capabilities & Key Highlights")

    cards_data = [
        ("🛡️ HIPAA Compliance Audit", "Enforces Single-User mode, Unity Catalog, approved runtimes & No Public IP for PHI workloads."),
        ("💰 FinOps Right-Sizing Engine", "Detects idle clusters and scales worker nodes from 16 -> 4 (75% monthly DBU cost reduction)."),
        ("⚡ Photon Engine Prediction", "Forecasts 3.4x query execution speedup and 71% latency reduction with 13.3 LTS Photon."),
        ("🎥 Gemini Omni Video Gen", "Generates 3D motion graphic previews via gemini-omni-flash-preview and streams bytes to GCS.")
    ]

    for i, (ctitle, cdesc) in enumerate(cards_data):
        x = Inches(0.8 + (i % 2) * 5.9)
        y = Inches(1.6 + (i // 2) * 2.7)
        shape = slide2.shapes.add_shape(pptx.enum.shapes.MSO_SHAPE.RECTANGLE, x, y, Inches(5.6), Inches(2.3))
        shape.fill.solid()
        shape.fill.fore_color.rgb = PANEL_BG
        shape.line.color.rgb = ACCENT_BLUE
        shape.line.width = Pt(1.5)
        
        tf = shape.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = ctitle
        p_t.font.size = Pt(18)
        p_t.font.bold = True
        p_t.font.color.rgb = GOLD_AMBER
        
        p_d = tf.add_paragraph()
        p_d.text = f"\n{cdesc}"
        p_d.font.size = Pt(14)
        p_d.font.color.rgb = TEXT_WHITE

    # SLIDE 3: Architecture
    slide3 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide3)
    add_header(slide3, "Google Cloud Platform Infrastructure & Architecture")

    gcp_cards = [
        ("Vertex AI Memory Bank", "PreloadMemoryTool", "Cross-session memory of user profiles & cost limits."),
        ("Google Cloud Firestore", "qwiklabs-gcp-02-7222a271d6bd", "databricks_clusters & recommendation_history audit logs."),
        ("Google Cloud Storage", "databricks-ops-optimizer...", "Public HTTPS video streaming storage without local files."),
        ("Vertex AI Omni Model", "gemini-omni-flash-preview", "Global region 3D motion video generation."),
        ("Agent Engine Sandbox", "ReasoningEngine Resource", "Secure isolated python code execution environment.")
    ]

    for i, (stitle, sres, sdesc) in enumerate(gcp_cards):
        y = Inches(1.5 + i * 1.1)
        shape = slide3.shapes.add_shape(pptx.enum.shapes.MSO_SHAPE.RECTANGLE, Inches(0.8), y, Inches(11.7), Inches(0.95))
        shape.fill.solid()
        shape.fill.fore_color.rgb = PANEL_BG
        shape.line.color.rgb = ACCENT_BLUE
        
        tf = shape.text_frame
        p = tf.paragraphs[0]
        p.text = f"{stitle}  |  ({sres})\n{sdesc}"
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

    # SLIDE 4: Business Impact
    slide4 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide4)
    add_header(slide4, "Quantifiable Business & Governance Impact")

    impact_data = [
        ("75%", "Monthly Cost Savings", "$2,840/mo -> $710/mo per cluster via 8x worker right-sizing."),
        ("3.4x", "Query Performance Speedup", "71% reduction in Spark job latency using 13.3 LTS Photon."),
        ("100%", "Compliance Enforcement", "Instant detection & remediation of HIPAA/PHI security policy risks."),
        ("Audit", "Complete Historical Trail", "Persistent Before vs After state audit logs stored in Firestore.")
    ]

    for i, (val, label, desc) in enumerate(impact_data):
        x = Inches(0.8 + i * 2.95)
        shape = slide4.shapes.add_shape(pptx.enum.shapes.MSO_SHAPE.RECTANGLE, x, Inches(2.0), Inches(2.7), Inches(4.5))
        shape.fill.solid()
        shape.fill.fore_color.rgb = PANEL_BG
        shape.line.color.rgb = GREEN_SUCCESS
        shape.line.width = Pt(2)
        
        tf = shape.text_frame
        tf.word_wrap = True
        p_val = tf.paragraphs[0]
        p_val.text = val
        p_val.font.size = Pt(44)
        p_val.font.bold = True
        p_val.font.color.rgb = GREEN_SUCCESS
        p_val.alignment = PP_ALIGN.CENTER
        
        p_lbl = tf.add_paragraph()
        p_lbl.text = f"\n{label}"
        p_lbl.font.size = Pt(16)
        p_lbl.font.bold = True
        p_lbl.font.color.rgb = TEXT_WHITE
        p_lbl.alignment = PP_ALIGN.CENTER
        
        p_desc = tf.add_paragraph()
        p_desc.text = f"\n{desc}"
        p_desc.font.size = Pt(13)
        p_desc.font.color.rgb = TEXT_MUTED
        p_desc.alignment = PP_ALIGN.CENTER

    pptx_path = "/tmp/databricks_cluster_intel_presentation.pptx"
    prs.save(pptx_path)
    print("Saved PowerPoint Presentation at:", pptx_path)
    return pptx_path

# --- 3. UPLOAD TO GCS ---
def upload_to_gcs(file_path, object_name, content_type):
    client = storage.Client(project=PROJECT_ID)
    bucket = client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(file_path, content_type=content_type)
    url = f"https://storage.googleapis.com/{GCS_BUCKET_NAME}/{object_name}"
    print(f"Uploaded {object_name} to GCS: {url}")
    return url

if __name__ == "__main__":
    docx_file = build_docx()
    pptx_file = build_pptx()
    
    docx_url = upload_to_gcs(docx_file, "databricks_cluster_intel_highlights.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    pptx_url = upload_to_gcs(pptx_file, "databricks_cluster_intel_presentation.pptx", "application/vnd.openxmlformats-officedocument.presentationml.presentation")
    
    print("\nALL DOCUMENTS GENERATED & UPLOADED SUCCESSFULLY!")
