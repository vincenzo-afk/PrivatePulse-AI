from __future__ import annotations

import math
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FRAMES = ROOT / ".video-frames"
OUTPUT = ROOT / "docs" / "privatepulse-demo.mp4"
WIDTH, HEIGHT, FPS = 1280, 720, 24

FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def font(path: str, size: int):
    return ImageFont.truetype(path, size)


def mix(a: tuple[int, int, int], b: tuple[int, int, int], t: float):
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def draw_text(draw: ImageDraw.ImageDraw, xy, text, fnt, fill, anchor=None):
    draw.text(xy, text, font=fnt, fill=fill, anchor=anchor)


def background(frame: int):
    t = frame / (FPS * 20)
    yy, xx = np.mgrid[0:HEIGHT, 0:WIDTH]
    radial = np.clip(1.0 - np.hypot(xx - WIDTH * 0.58, yy - HEIGHT * 0.1) / 850.0, 0.0, 1.0) * 0.65
    base = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)
    base[:, :, 0] = 5 + (10 - 5) * radial
    base[:, :, 1] = 13 + (34 - 13) * radial
    base[:, :, 2] = 12 + (29 - 12) * radial
    pulse = (np.sin(t * math.tau + xx / 240.0) + 1.0) * 1.5
    base[:, :, 0] += pulse
    base[:, :, 1] += pulse * 2
    base[:, :, 2] += pulse * 1.6
    image = Image.fromarray(np.uint8(np.clip(base, 0, 255)), "RGB").convert("RGBA")
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for x in range(-HEIGHT, WIDTH, 64):
        od.line((x, 0, x + HEIGHT, HEIGHT), fill=(0, 212, 170, 12), width=1)
    for y in range(0, HEIGHT, 64):
        od.line((0, y, WIDTH, y), fill=(0, 212, 170, 10), width=1)
    return Image.alpha_composite(image, overlay)


def rounded_card(draw: ImageDraw.ImageDraw, box, fill=(13, 33, 30, 235), outline=(29, 76, 67, 255), radius=18, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def reveal(frame: int, start: int, duration: int):
    return max(0.0, min(1.0, (frame - start) / max(1, duration)))


def scene_intro(image, local):
    d = ImageDraw.Draw(image)
    p = reveal(local, 0, 18)
    d.rounded_rectangle((82, 94, 470, 132), radius=19, fill=(0, 212, 170, 28), outline=(0, 212, 170, 90), width=1)
    d.ellipse((104, 107, 116, 119), fill=(0, 212, 170, 255))
    draw_text(d, (132, 113), "PRIVACY-FIRST DOCUMENT INTELLIGENCE", font(FONT_BOLD, 13), (104, 230, 208, 255), anchor="lm")
    y = 210 + int((1 - p) * 22)
    draw_text(d, (82, y), "Your documents.", font(FONT_BOLD, 65), (239, 255, 251, 255))
    draw_text(d, (82, y + 72), "Your AI assistant.", font(FONT_BOLD, 65), (0, 212, 170, 255))
    draw_text(d, (86, y + 184), "Ask natural-language questions about sensitive files\nwith grounded answers and visible sources.", font(FONT_REGULAR, 23), (154, 189, 181, 255))
    rounded_card(d, (820, 166, 1140, 472), fill=(10, 31, 27, 220))
    d.ellipse((910, 235, 1050, 375), outline=(0, 212, 170, 180), width=3)
    d.ellipse((942, 267, 1018, 343), outline=(104, 230, 208, 200), width=3)
    d.polygon([(980, 205), (1040, 230), (1054, 335), (980, 420), (906, 335), (920, 230)], outline=(0, 212, 170, 220), fill=(0, 212, 170, 20))
    draw_text(d, (980, 462), "CONTROLLED BY DESIGN", font(FONT_MONO, 13), (154, 189, 181, 255), anchor="ma")


def scene_ingest(image, local):
    d = ImageDraw.Draw(image)
    p = reveal(local, 0, 20)
    draw_text(d, (82, 92), "01 / INGEST SECURELY", font(FONT_BOLD, 15), (0, 212, 170, 255))
    draw_text(d, (82, 142), "Bring the document.\nKeep control of the data.", font(FONT_BOLD, 51), (239, 255, 251, 255))
    draw_text(d, (84, 276), "Session-scoped storage and local processing\nkeep the workflow easy to inspect.", font(FONT_REGULAR, 21), (154, 189, 181, 255))
    x = 670 + int((1 - p) * 30)
    rounded_card(d, (x, 116, 1158, 564))
    draw_text(d, (720, 152), "PRIVATE WORKSPACE", font(FONT_BOLD, 15), (239, 255, 251, 255))
    draw_text(d, (1056, 152), "SESSION ISOLATED", font(FONT_MONO, 12), (104, 230, 208, 255), anchor="ra")
    d.rounded_rectangle((720, 210, 1108, 398), radius=14, fill=(0, 212, 170, 10), outline=(63, 129, 117, 255), width=2)
    draw_text(d, (914, 294), "DROP FILES HERE", font(FONT_BOLD, 20), (104, 230, 208, 255), anchor="mm")
    draw_text(d, (914, 326), "PDF  ·  DOCX  ·  TXT", font(FONT_MONO, 13), (154, 189, 181, 255), anchor="mm")
    d.rounded_rectangle((720, 442, 1108, 498), radius=12, fill=(17, 52, 45, 255))
    draw_text(d, (742, 470), "employee-handbook.pdf", font(FONT_REGULAR, 15), (239, 255, 251, 255), anchor="lm")
    draw_text(d, (1084, 470), "INDEXED LOCALLY", font(FONT_MONO, 11), (0, 212, 170, 255), anchor="rm")


def scene_answer(image, local):
    d = ImageDraw.Draw(image)
    p = reveal(local, 0, 22)
    draw_text(d, (82, 92), "02 / ASK NATURALLY", font(FONT_BOLD, 15), (0, 212, 170, 255))
    draw_text(d, (82, 142), "Answers grounded\nin your sources.", font(FONT_BOLD, 51), (239, 255, 251, 255))
    x = 570 + int((1 - p) * 40)
    rounded_card(d, (x, 132, 1168, 552))
    d.rounded_rectangle((626, 184, 1112, 264), radius=14, fill=(0, 212, 170, 28), outline=(0, 212, 170, 75), width=1)
    draw_text(d, (650, 224), "What is the reimbursement limit for client travel?", font(FONT_REGULAR, 16), (239, 255, 251, 255), anchor="lm")
    d.rounded_rectangle((626, 302, 1112, 472), radius=14, fill=(14, 39, 35, 255), outline=(29, 76, 67, 255), width=1)
    draw_text(d, (650, 338), "The policy sets a maximum reimbursement of", font(FONT_REGULAR, 17), (216, 255, 246, 255))
    draw_text(d, (650, 370), "$2,500 per trip", font(FONT_BOLD, 24), (0, 212, 170, 255))
    draw_text(d, (650, 414), "with receipts required for expenses over $25.", font(FONT_REGULAR, 17), (216, 255, 246, 255))
    draw_text(d, (650, 446), "SOURCE  employee-handbook.pdf  ·  PAGE 18", font(FONT_MONO, 11), (104, 230, 208, 255))
    draw_text(d, (82, 570), "Retrieve  →  rank  →  generate  →  cite", font(FONT_MONO, 16), (154, 189, 181, 255))


def scene_vision(image, local):
    d = ImageDraw.Draw(image)
    p = reveal(local, 0, 20)
    draw_text(d, (82, 92), "03 / UNDERSTAND MORE", font(FONT_BOLD, 15), (0, 212, 170, 255))
    draw_text(d, (82, 142), "Text, scans, charts,\nand images in one flow.", font(FONT_BOLD, 49), (239, 255, 251, 255))
    draw_text(d, (84, 300), "Vision-enabled queries and OCR fallback\nmake complex documents easier to explore.", font(FONT_REGULAR, 21), (154, 189, 181, 255))
    cards = [(660, "PDF", "Multi-format ingestion"), (842, "OCR", "Scanned document fallback"), (1024, "5", "Images per request")]
    for i, (x, big, small) in enumerate(cards):
        offset = int((1 - p) * (25 - i * 6))
        rounded_card(d, (x, 424 + offset, x + 156, 584 + offset), fill=(13, 33, 30, 235))
        draw_text(d, (x + 78, 474 + offset), big, font(FONT_BOLD, 28), (0, 212, 170, 255), anchor="mm")
        draw_text(d, (x + 78, 532 + offset), small, font(FONT_REGULAR, 11), (154, 189, 181, 255), anchor="mm")


def scene_close(image, local):
    d = ImageDraw.Draw(image)
    p = reveal(local, 0, 18)
    draw_text(d, (WIDTH // 2, 180), "Private by design.", font(FONT_BOLD, 60), (239, 255, 251, 255), anchor="ma")
    draw_text(d, (WIDTH // 2, 254), "Useful by default.", font(FONT_BOLD, 60), (0, 212, 170, 255), anchor="ma")
    draw_text(d, (WIDTH // 2, 368), "PrivatePulse AI", font(FONT_MONO, 20), (104, 230, 208, 255), anchor="ma")
    d.rounded_rectangle((WIDTH // 2 - 150, 422, WIDTH // 2 + 150, 475), radius=25, fill=(0, 212, 170, int(220 * p)))
    draw_text(d, (WIDTH // 2, 449), "EXPLORE THE PROJECT", font(FONT_BOLD, 14), (4, 32, 26, 255), anchor="mm")


def main():
    if FRAMES.exists():
        shutil.rmtree(FRAMES)
    FRAMES.mkdir(parents=True)
    scenes = [(3.0, scene_intro), (4.0, scene_ingest), (4.0, scene_answer), (3.5, scene_vision), (3.5, scene_close)]
    frame = 0
    for duration, renderer in scenes:
        count = round(duration * FPS)
        for local in range(count):
            image = background(frame).filter(ImageFilter.GaussianBlur(radius=0.05))
            renderer(image, local)
            d = ImageDraw.Draw(image)
            d.rectangle((0, HEIGHT - 9, WIDTH, HEIGHT), fill=(4, 15, 13, 255))
            d.rectangle((0, HEIGHT - 9, int(WIDTH * ((frame + 1) / sum(dur * FPS for dur, _ in scenes))), HEIGHT), fill=(0, 212, 170, 255))
            image.convert("RGB").save(FRAMES / f"frame-{frame:05d}.png", optimize=True)
            frame += 1
    print(f"frames={frame}")
    print(f"frame_dir={FRAMES}")
    print(f"output={OUTPUT}")


if __name__ == "__main__":
    main()
