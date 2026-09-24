import os
import sys
import math
import subprocess
import base64
import datetime
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1920, 1080
FPS = 30

# Colors
BG_DARK = (15, 23, 42)        # #0f172a
PANEL_BG = (30, 41, 59)       # #1e293b
CARD_BG = (51, 65, 85)        # #334155
ACCENT_BLUE = (14, 165, 233)  # #0ea5e9
ACCENT_ORANGE = (249, 115, 22)# #f97316
TEXT_WHITE = (248, 250, 252) # #f8fafc
TEXT_MUTED = (148, 163, 184) # #94a3b8
GREEN_SUCCESS = (34, 197, 94) # #22c55e
RED_ALERT = (239, 68, 68)     # #ef4444
GOLD_AMBER = (245, 158, 11)   # #f59e0b

# Try loading truetype font, fallback to default
try:
    font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 42)
    font_subtitle = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    font_heading = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
    font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
    font_code = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 20)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
except Exception:
    font_title = font_subtitle = font_heading = font_body = font_code = font_small = ImageFont.load_default()

def draw_header(draw, title_suffix=""):
    # Header bar
    draw.rectangle([(0, 0), (WIDTH, 90)], fill=(10, 15, 30))
    draw.text((40, 25), "Databricks Cluster Intelligence & Governance Agent", fill=ACCENT_ORANGE, font=font_heading)
    draw.text((820, 30), f"| {title_suffix}" if title_suffix else "", fill=TEXT_MUTED, font=font_body)
    
    # Status badges right
    draw.rectangle([(WIDTH - 380, 20), (WIDTH - 40, 70)], fill=(20, 35, 60), outline=ACCENT_BLUE, width=2)
    draw.text((WIDTH - 365, 33), "Vertex AI Agent Engine 🟢 LIVE", fill=TEXT_WHITE, font=font_small)

def draw_sidebar(draw, active_tab=1):
    # Left sidebar
    draw.rectangle([(0, 90), (320, HEIGHT)], fill=(15, 20, 35))
    draw.text((30, 120), "NAVIGATION", fill=TEXT_MUTED, font=font_small)
    
    tabs = [
        ("1. Governance Audit", 1),
        ("2. Sizing & Workloads", 2),
        ("3. System Telemetry", 3),
        ("4. Firestore DB History", 4),
        ("5. 3D Omni Video Preview", 5),
    ]
    
    for i, (label, idx) in enumerate(tabs):
        top = 160 + i * 55
        is_active = (idx == active_tab)
        bg_c = (30, 58, 95) if is_active else (20, 28, 45)
        text_c = TEXT_WHITE if is_active else TEXT_MUTED
        draw.rectangle([(20, top), (300, top + 45)], fill=bg_c, outline=ACCENT_BLUE if is_active else None, width=1)
        draw.text((40, top + 12), label, fill=text_c, font=font_body)

def make_scene_1(t, duration=4.0):
    # Intro Scene
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)
    
    # Pulsing glow ring
    glow_r = int(180 + 20 * math.sin(t * 3))
    draw.ellipse([(WIDTH//2 - glow_r, 220 - glow_r//2), (WIDTH//2 + glow_r, 220 + glow_r//2)], outline=(14, 165, 233, 100), width=4)
    
    draw.text((WIDTH//2 - 420, 200), "Databricks Cluster-Intel Agent", fill=TEXT_WHITE, font=font_title)
    draw.text((WIDTH//2 - 350, 270), "Autonomous FinOps, HIPAA Governance & Sizing Engine", fill=ACCENT_ORANGE, font=font_heading)
    draw.text((WIDTH//2 - 280, 320), "Powered by Google Gemini 2.0 & ADK Agent Engine", fill=TEXT_MUTED, font=font_subtitle)
    
    # Feature Grid
    features = [
        ("🛡️ HIPAA Compliance Guardrails", "Single-user compute, Unity Catalog & No Public IP enforcement"),
        ("💰 Autonomous FinOps", "System Tables telemetry & 8x worker right-sizing savings"),
        ("⚡ Photon Engine Prediction", "13.3 LTS Photon acceleration & execution speedup analysis"),
        ("🎥 Gemini Omni Video Gen", "3D motion previews via gemini-omni-flash-preview & GCS upload"),
    ]
    
    for i, (title, desc) in enumerate(features):
        x = 220 + (i % 2) * 760
        y = 420 + (i // 2) * 200
        draw.rectangle([(x, y), (x + 700, y + 160)], fill=PANEL_BG, outline=ACCENT_BLUE, width=2)
        draw.text((x + 30, y + 30), title, fill=GOLD_AMBER, font=font_heading)
        draw.text((x + 30, y + 85), desc, fill=TEXT_MUTED, font=font_body)
        
    draw.text((WIDTH//2 - 250, HEIGHT - 80), "▶ Interactive Demo Walkthrough Starting...", fill=GREEN_SUCCESS, font=font_heading)
    return img

def make_scene_2(t, duration=10.0):
    # Prompt 1: Primary Capability - Compliance & Sizing Audit
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "Prompt 1: Primary Capability (HIPAA Governance & Audit)")
    draw_sidebar(draw, active_tab=1)
    
    main_left, main_top = 350, 110
    
    # User prompt box
    draw.rectangle([(main_left, main_top), (WIDTH - 40, main_top + 80)], fill=PANEL_BG, outline=ACCENT_BLUE, width=2)
    draw.text((main_left + 20, main_top + 15), "👤 User Prompt:", fill=ACCENT_BLUE, font=font_small)
    user_text = "Audit my Databricks clusters for HIPAA policy compliance, cost anomalies, and predict Photon speedups."
    # Typing effect
    chars = int(len(user_text) * min(1.0, t / 2.0))
    draw.text((main_left + 20, main_top + 42), user_text[:chars], fill=TEXT_WHITE, font=font_heading)
    
    if t > 2.0:
        # Tool execution callouts
        draw.rectangle([(main_left, main_top + 100), (main_left + 450, main_top + 280)], fill=(20, 30, 50), outline=GOLD_AMBER, width=2)
        draw.text((main_left + 15, main_top + 115), "🛠️ Active Tool Invocations:", fill=GOLD_AMBER, font=font_heading)
        
        tools = [
            "✓ audit_cluster_policy_compliance()",
            "✓ predict_photon_acceleration()",
            "✓ query_databricks_system_tables()",
        ]
        for i, tool in enumerate(tools):
            if t > 2.5 + i * 0.5:
                draw.text((main_left + 25, main_top + 160 + i * 35), tool, fill=GREEN_SUCCESS, font=font_code)
                
    if t > 4.5:
        # Agent response card
        draw.rectangle([(main_left, main_top + 300), (WIDTH - 40, HEIGHT - 40)], fill=PANEL_BG, outline=RED_ALERT, width=3)
        draw.text((main_left + 30, main_top + 325), "🤖 Agent Response & Compliance Audit Report", fill=TEXT_WHITE, font=font_heading)
        
        lines = [
            "🚨 VIOLATION DETECTED: Cluster `dbx-claims-etl-01` violates HIPAA Security Policy.",
            "• Single User Access Mode: REQUIRED (Currently: Shared Mode ❌)",
            "• Photon Engine: DISABLED (Recommended: 13.3 LTS Photon ⚡)",
            "• Sizing Bottleneck: Oversized by 8x (16 workers active, 4 workers required)",
            "",
            "💡 EXECUTIVE SUMMARY:",
            "\"This job violates HIPAA policy because Single User Access Mode is required.",
            " This cluster is oversized by 8x. Photon should be enabled. Expected annual savings: 64%.\"",
            "",
            "📊 Confidence Score: 98% (High Confidence) | Action: Policy Remediation Ready"
        ]
        
        for i, line in enumerate(lines):
            c = RED_ALERT if "VIOLATION" in line else (GOLD_AMBER if "EXECUTIVE" in line or "Savings" in line else TEXT_WHITE)
            if "Confidence" in line: c = GREEN_SUCCESS
            draw.text((main_left + 30, main_top + 375 + i * 32), line, fill=c, font=font_body)

    return img

def make_scene_3(t, duration=12.0):
    # Prompt 2: Rich Multi-Tool Prompt - DB Lookup, Sizing & 3D Video Tool
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "Prompt 2: Rich Multi-Tool Execution & Omni Video Generation")
    draw_sidebar(draw, active_tab=5)
    
    main_left, main_top = 350, 110
    
    # User prompt box
    draw.rectangle([(main_left, main_top), (WIDTH - 40, main_top + 90)], fill=PANEL_BG, outline=ACCENT_BLUE, width=2)
    draw.text((main_left + 20, main_top + 12), "👤 User Prompt (Rich Multi-Tool Request):", fill=ACCENT_BLUE, font=font_small)
    user_text = "Query system tables for billing, apply optimal right-sizing to dbx-claims-etl-01 with audit history, and generate a 3D motion graphic video."
    chars = int(len(user_text) * min(1.0, t / 2.5))
    draw.text((main_left + 20, main_top + 40), user_text[:chars], fill=TEXT_WHITE, font=font_body)

    if t > 2.5:
        # Split screen: Left = DB Mutation & Audit, Right = Video Gen
        draw.rectangle([(main_left, main_top + 110), (main_left + 720, HEIGHT - 40)], fill=PANEL_BG, outline=ACCENT_BLUE, width=2)
        draw.text((main_left + 20, main_top + 130), "🔥 Firestore DB Lookup & Right-Sizing Audit", fill=ACCENT_ORANGE, font=font_heading)
        
        db_steps = [
            ("1. Database Query", "Fetched cluster `dbx-claims-etl-01` from Firestore"),
            ("2. Sizing Optimization", "Scaled Workers: 16 -> 4 workers"),
            ("3. Monthly Cost Impact", "$2,840.00/mo -> $710.00/mo (-75% savings)"),
            ("4. Audit Trail Written", "Logged Before/After state to `recommendation_history`"),
        ]
        
        for i, (st, desc) in enumerate(db_steps):
            if t > 3.0 + i * 0.8:
                draw.rectangle([(main_left + 20, main_top + 180 + i * 85), (main_left + 700, main_top + 250 + i * 85)], fill=CARD_BG)
                draw.text((main_left + 35, main_top + 190 + i * 85), st, fill=GOLD_AMBER, font=font_heading)
                draw.text((main_left + 35, main_top + 220 + i * 85), desc, fill=TEXT_WHITE, font=font_small)

    if t > 6.0:
        # Right box: Gemini Omni Video Tool execution & GCS upload
        right_x = main_left + 750
        draw.rectangle([(right_x, main_top + 110), (WIDTH - 40, HEIGHT - 40)], fill=PANEL_BG, outline=GOLD_AMBER, width=2)
        draw.text((right_x + 20, main_top + 130), "🎥 Tool: generate_domain_video_preview", fill=GOLD_AMBER, font=font_heading)
        draw.text((right_x + 20, main_top + 165), "Model: gemini-omni-flash-preview (global)", fill=TEXT_MUTED, font=font_small)
        
        draw.rectangle([(right_x + 20, main_top + 200), (WIDTH - 60, main_top + 380)], fill=(10, 15, 25))
        draw.text((right_x + 40, main_top + 220), "▶ Generating 3D Motion Graphic Video...", fill=GREEN_SUCCESS, font=font_heading)
        
        # Progress bar
        prog = min(1.0, (t - 6.0) / 4.0)
        draw.rectangle([(right_x + 40, main_top + 260), (WIDTH - 80, main_top + 290)], fill=(30, 40, 60))
        draw.rectangle([(right_x + 40, main_top + 260), (right_x + 40 + int(prog * (WIDTH - right_x - 120)), main_top + 290)], fill=ACCENT_BLUE)
        draw.text((right_x + 40, main_top + 300), f"Status: {int(prog * 100)}% Complete | Saving to tool_context", fill=TEXT_WHITE, font=font_small)
        
        if t > 10.0:
            draw.text((right_x + 20, main_top + 410), "🌐 Public Cloud Storage HTTPS URL:", fill=ACCENT_ORANGE, font=font_heading)
            gcs_url = "https://storage.googleapis.com/databricks-ops-optimizer.../video.mp4"
            draw.rectangle([(right_x + 20, main_top + 450), (WIDTH - 60, main_top + 510)], fill=(15, 30, 55), outline=GREEN_SUCCESS, width=2)
            draw.text((right_x + 35, main_top + 470), gcs_url, fill=GREEN_SUCCESS, font=font_code)

    return img

def make_outro_scene(t, duration=4.0):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)
    
    draw.text((WIDTH//2 - 380, 180), "Databricks Cluster-Intel Agent", fill=TEXT_WHITE, font=font_title)
    draw.text((WIDTH//2 - 250, 250), "✅ Deployment Verified & Production Ready", fill=GREEN_SUCCESS, font=font_heading)
    
    box_x = WIDTH//2 - 500
    draw.rectangle([(box_x, 320), (box_x + 1000, 750)], fill=PANEL_BG, outline=ACCENT_BLUE, width=3)
    
    details = [
        ("🪪 Agent Card URL:", "https://us-east1-aiplatform.googleapis.com/.../agent-card.json"),
        ("🌐 GitHub Repository:", "https://github.com/deepacts/buildwithgemini-databricks-cluster-intel-agent"),
        ("☁️ Cloud Storage Bucket:", "databricks-ops-optimizer-qwiklabs-gcp-02-7222a271d6bd"),
        ("⚡ Gemini Omni Model:", "gemini-omni-flash-preview (global region)"),
        ("📊 Firestore Database:", "qwiklabs-gcp-02-7222a271d6bd (databricks_clusters)"),
    ]
    
    for i, (label, val) in enumerate(details):
        draw.text((box_x + 40, 360 + i * 75), label, fill=GOLD_AMBER, font=font_heading)
        draw.text((box_x + 40, 398 + i * 75), val, fill=TEXT_WHITE, font=font_body)
        
    draw.text((WIDTH//2 - 300, 820), "Build with Gemini 2.0 Challenge Submission", fill=ACCENT_ORANGE, font=font_heading)
    return img

def generate_video():
    frames_dir = "/tmp/demo_frames"
    os.makedirs(frames_dir, exist_ok=True)
    
    scenes = [
        (make_scene_1, 4.0),
        (make_scene_2, 10.0),
        (make_scene_3, 12.0),
        (make_outro_scene, 4.0),
    ]
    
    frame_count = 0
    print("Generating video frames...")
    
    for scene_fn, duration in scenes:
        num_frames = int(duration * FPS)
        for f in range(num_frames):
            t = f / FPS
            img = scene_fn(t, duration)
            frame_path = os.path.join(frames_dir, f"frame_{frame_count:05d}.png")
            img.save(frame_path)
            frame_count += 1
            if frame_count % 60 == 0:
                print(f"Generated {frame_count} frames...")
                
    output_mp4 = "/config/.gemini/antigravity/brain/5dd2c1ba-dbbb-4107-92f6-61e2f371bdd2/agent_demo_video.mp4"
    print(f"Compiling {frame_count} frames into MP4 with ffmpeg...")
    
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", os.path.join(frames_dir, "frame_%05d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        output_mp4
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print("SUCCESS! Video created at:", output_mp4)
    else:
        print("FFmpeg error:", res.stderr)

if __name__ == "__main__":
    generate_video()
