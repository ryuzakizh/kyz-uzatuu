"""
Kyz Uzatuu Guest Information Brochure
Style: cream background, Kyrgyz ornamental corners (sage green + terracotta),
       serif/script fonts, centered layout — matching Maksym.png invite.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image
import io

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE    = os.path.dirname(os.path.abspath(__file__))
UZOR    = os.path.join(BASE, "uzor.PNG")
OUTPUT  = os.path.join(BASE, "Kyz_Uzatuu_Guest_Brochure.pdf")

# ── Colours (matching invitation) ─────────────────────────────────────────────
CREAM       = HexColor("#F5F0E8")
TERRACOTTA  = HexColor("#B84C2E")
SAGE        = HexColor("#7A9E7E")
DARK_TEXT   = HexColor("#2C2416")
DIVIDER     = HexColor("#C8B89A")

# ── Page setup ────────────────────────────────────────────────────────────────
W, H = A4          # 595.27 x 841.89 pt
MARGIN = 2.2 * cm

# ── Helpers ───────────────────────────────────────────────────────────────────

def rotated_image(path, degrees):
    """Return a PIL image rotated by degrees (expand=True keeps full size)."""
    img = Image.open(path).convert("RGBA")
    return img.rotate(degrees, expand=True)


def pil_to_reader(pil_img):
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    buf.seek(0)
    return ImageReader(buf)


def draw_corners(c, page_w, page_h, size=90):
    """Draw the uzor ornament rotated into all four corners."""
    s = size        # points
    pad = 6         # small inset from edge

    # top-left  → original orientation
    tl = rotated_image(UZOR, 0)
    c.drawImage(pil_to_reader(tl),  pad, page_h - s - pad,  s, s, mask="auto")

    # top-right  → flip horizontally (rotate 90 then vertical flip is easier via -90)
    tr = rotated_image(UZOR, 90)
    c.drawImage(pil_to_reader(tr),  page_w - s - pad, page_h - s - pad, s, s, mask="auto")

    # bottom-right → 180°
    br = rotated_image(UZOR, 180)
    c.drawImage(pil_to_reader(br),  page_w - s - pad, pad, s, s, mask="auto")

    # bottom-left → 270°
    bl = rotated_image(UZOR, 270)
    c.drawImage(pil_to_reader(bl),  pad, pad, s, s, mask="auto")


def draw_background(c, page_w, page_h):
    c.setFillColor(CREAM)
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)


def divider(c, y, page_w, margin):
    c.setStrokeColor(DIVIDER)
    c.setLineWidth(0.8)
    c.line(margin + 10, y, page_w - margin - 10, y)


def section_title(c, text, y, page_w):
    """Terracotta bold section heading."""
    c.setFont("Times-Bold", 14)
    c.setFillColor(TERRACOTTA)
    c.drawCentredString(page_w / 2, y, text)


def body_text_block(c, lines, y_start, page_w, margin, leading=16, font="Times-Roman", size=11):
    """Draw a list of strings centred, return y after last line."""
    c.setFont(font, size)
    c.setFillColor(DARK_TEXT)
    y = y_start
    for line in lines:
        c.drawCentredString(page_w / 2, y, line)
        y -= leading
    return y


def left_aligned_block(c, lines, y_start, x, leading=15, font="Times-Roman", size=10.5):
    """Draw left-aligned lines, return y after last line."""
    c.setFont(font, size)
    c.setFillColor(DARK_TEXT)
    y = y_start
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


# ── PAGE 1 – Cover / Arrival ──────────────────────────────────────────────────

def page1(c):
    draw_background(c, W, H)
    draw_corners(c, W, H, size=95)

    y = H - 3.5 * cm

    # ── Greeting ──────────────────────────────────────────────────────────────
    c.setFont("Times-Italic", 13)
    c.setFillColor(DARK_TEXT)
    c.drawCentredString(W / 2, y, "Dear Guests,")
    y -= 22

    c.setFont("Times-Roman", 11)
    c.setFillColor(DARK_TEXT)
    greeting = [
        "We are overjoyed to have you celebrate with us.",
        "This guide will help you arrive comfortably",
        "and make the most of your time in Osh.",
    ]
    for line in greeting:
        c.drawCentredString(W / 2, y, line)
        y -= 16
    y -= 10

    divider(c, y, W, MARGIN)
    y -= 22

    # ── Event banner ──────────────────────────────────────────────────────────
    c.setFont("Times-Bold", 28)
    c.setFillColor(TERRACOTTA)
    c.drawCentredString(W / 2, y, "ELNURA'S")
    y -= 32

    c.setFont("Times-BoldItalic", 26)
    c.setFillColor(TERRACOTTA)
    c.drawCentredString(W / 2, y, "Kyz Uzatuu")
    y -= 28

    c.setFont("Times-Bold", 13)
    c.setFillColor(DARK_TEXT)
    c.drawCentredString(W / 2, y, "Kasiet Grand Palace  ·  Osh, Kyrgyzstan")
    y -= 18

    c.setFont("Times-BoldItalic", 13)
    c.setFillColor(TERRACOTTA)
    c.drawCentredString(W / 2, y, "Saturday, June 6th  ·  4:00 PM")
    y -= 28

    divider(c, y, W, MARGIN)
    y -= 26

    # ── How to Arrive ─────────────────────────────────────────────────────────
    section_title(c, "HOW TO ARRIVE IN OSH", y, W)
    y -= 24

    # ✈ By Air
    c.setFont("Times-Bold", 11.5)
    c.setFillColor(SAGE)
    c.drawCentredString(W / 2, y, "✈  By Air")
    y -= 17

    air_lines = [
        "Osh International Airport (OSS) has direct flights",
        "from Bishkek (approx. 1 hr) and connections from",
        "Almaty, Istanbul, Moscow, and Dubai.",
        "",
        "Airlines: Air Manas · Turkish Airlines",
        "· FlyArystan (seasonal)",
        "",
        "From the airport, the city centre is ~15 min by taxi.",
        "Recommended apps: Yandex Go · inDrive",
    ]
    y = body_text_block(c, air_lines, y, W, MARGIN, leading=15)
    y -= 10

    # 🚌 By Road
    c.setFont("Times-Bold", 11.5)
    c.setFillColor(SAGE)
    c.drawCentredString(W / 2, y, "🚌  By Road from Bishkek")
    y -= 17

    road_lines = [
        "Shared taxis ('marshrutka') depart from the",
        "West Bus Station in Bishkek — approx. 8–10 hrs.",
        "Private car hire is also widely available.",
        "",
        "Note: the Bishkek–Osh highway crosses the",
        "Taldyk Pass (~3,615 m). Dress in layers!",
    ]
    y = body_text_block(c, road_lines, y, W, MARGIN, leading=15)
    y -= 14

    divider(c, y, W, MARGIN)
    y -= 22

    # ── Local Transport ───────────────────────────────────────────────────────
    section_title(c, "GETTING AROUND OSH", y, W)
    y -= 20

    local_lines = [
        "Taxis are inexpensive — always agree on a price first,",
        "or use Yandex Go / inDrive apps for fixed fares.",
        "The venue (Kasiet Grand Palace) is centrally located",
        "and well known to local drivers.",
    ]
    body_text_block(c, local_lines, y, W, MARGIN, leading=15)

    c.showPage()


# ── PAGE 2 – Accommodation & Itinerary ───────────────────────────────────────

def page2(c):
    draw_background(c, W, H)
    draw_corners(c, W, H, size=95)

    y = H - 3.5 * cm

    # ── Accommodation ─────────────────────────────────────────────────────────
    section_title(c, "WHERE TO STAY", y, W)
    y -= 22

    c.setFont("Times-Italic", 10.5)
    c.setFillColor(DARK_TEXT)
    c.drawCentredString(W / 2, y, "We have pre-arranged rates at the following hotels.")
    y -= 14
    c.drawCentredString(W / 2, y, "Please mention 'Elnura & Adilbek Wedding' when booking.")
    y -= 24

    hotels = [
        {
            "name": "[ HOTEL NAME 1 ]",
            "address": "[ Address, Osh ]",
            "phone": "[ +996 XXX XXX XXX ]",
            "distance": "[ X min from venue ]",
            "rate": "[ ~$XX / night ]",
        },
        {
            "name": "[ HOTEL NAME 2 ]",
            "address": "[ Address, Osh ]",
            "phone": "[ +996 XXX XXX XXX ]",
            "distance": "[ X min from venue ]",
            "rate": "[ ~$XX / night ]",
        },
        {
            "name": "[ HOTEL NAME 3 ]",
            "address": "[ Address, Osh ]",
            "phone": "[ +996 XXX XXX XXX ]",
            "distance": "[ X min from venue ]",
            "rate": "[ ~$XX / night ]",
        },
    ]

    for hotel in hotels:
        # Hotel box
        box_x = MARGIN + 5
        box_w = W - 2 * MARGIN - 10
        box_h = 68
        c.setFillColor(HexColor("#EDE8DC"))
        c.setStrokeColor(DIVIDER)
        c.setLineWidth(0.7)
        c.roundRect(box_x, y - box_h + 10, box_w, box_h, 5, fill=1, stroke=1)

        c.setFont("Times-Bold", 12)
        c.setFillColor(TERRACOTTA)
        c.drawCentredString(W / 2, y - 2, hotel["name"])

        c.setFont("Times-Roman", 10)
        c.setFillColor(DARK_TEXT)
        row1 = f"Address: {hotel['address']}    Phone: {hotel['phone']}"
        row2 = f"Distance to venue: {hotel['distance']}    Rate: {hotel['rate']}"
        c.drawCentredString(W / 2, y - 17, row1)
        c.drawCentredString(W / 2, y - 31, row2)

        y -= box_h + 8

    y -= 6
    divider(c, y, W, MARGIN)
    y -= 26

    # ── Itinerary ─────────────────────────────────────────────────────────────
    section_title(c, "WEDDING DAY ITINERARY  —  Saturday, June 6th", y, W)
    y -= 22

    itinerary = [
        ("12:00 PM", "Guests begin arriving at the family home"),
        ("1:00 PM",  "Traditional blessing & farewell ceremony (Kyz Uzatuu) begins"),
        ("2:30 PM",  "Light refreshments served at the family home"),
        ("3:30 PM",  "Guests depart for Kasiet Grand Palace"),
        ("4:00 PM",  "Doors open at the venue — welcome reception"),
        ("4:30 PM",  "Bride's grand entrance & formal ceremony"),
        ("5:15 PM",  "Toasts & blessing from family elders"),
        ("6:00 PM",  "Festive dinner begins"),
        ("7:00 PM",  "Live music, traditional songs & dances"),
        ("9:00 PM",  "Cake cutting & dessert"),
        ("10:00 PM", "Evening dancing & celebration"),
        ("12:00 AM", "Farewell & safe travels home"),
    ]

    col_time = MARGIN + 15
    col_event = MARGIN + 100

    for time, event in itinerary:
        c.setFont("Times-Bold", 10.5)
        c.setFillColor(TERRACOTTA)
        c.drawString(col_time, y, time)
        c.setFont("Times-Roman", 10.5)
        c.setFillColor(DARK_TEXT)
        c.drawString(col_event, y, event)
        y -= 17

    y -= 10
    divider(c, y, W, MARGIN)
    y -= 20

    # ── Footer ────────────────────────────────────────────────────────────────
    c.setFont("Times-Italic", 10)
    c.setFillColor(SAGE)
    footer = [
        "For any questions, please contact us:",
        "[ Your Name / WhatsApp: +996 XXX XXX XXX ]",
        "",
        "We look forward to celebrating with you!",
        "— Elnura & Adilbek —",
    ]
    for line in footer:
        c.drawCentredString(W / 2, y, line)
        y -= 15

    c.showPage()


# ── Build PDF ─────────────────────────────────────────────────────────────────

def build():
    c = canvas.Canvas(OUTPUT, pagesize=A4)
    c.setTitle("Kyz Uzatuu — Guest Information Brochure")
    c.setAuthor("Elnura & Adilbek")

    page1(c)
    page2(c)

    c.save()
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    build()
