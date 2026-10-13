#!/usr/bin/env python3
"""Fetch the live v4 App Store media for the Toybird Labs landing pages.

Source: Apple iTunes lookup API, the public production listing for app 6782023263.
This runs only when the explicit v4 media-sync script is committed.
"""
from __future__ import annotations
from io import BytesIO
from pathlib import Path
import json
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from PIL import Image, ImageDraw, ImageFont

APP_ID = "6782023263"
OUT = Path("shared/ai-study-sheet-v4")
LOCALES = {"ja": "jp", "en": "us", "ko": "kr", "zh-cn": "cn"}
NAMES = ["01_automation", "02_auto_answers", "03_review_reminder",
         "04_personal_review", "05_new_home", "06_share_backup"]


def download(url: str) -> bytes:
    error = None
    for attempt in range(4):
        try:
            req = Request(url, headers={"User-Agent": "Mozilla/5.0 (Toybird Labs v4 assets)"})
            with urlopen(req, timeout=40) as response:
                return response.read()
        except Exception as exc:
            error = exc
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"Failed download: {url}: {error}")


def screenshot(url: str, path: Path) -> Image.Image:
    im = Image.open(BytesIO(download(url))).convert("RGB")
    if im.height <= im.width:
        raise RuntimeError(f"Unexpected screenshot aspect ratio: {im.size}, {url}")
    im.thumbnail((700, 1520), Image.Resampling.LANCZOS)
    im.save(path, "WEBP", quality=84, method=6)
    return im


def make_og(lang: str, icon: Image.Image, shot: Image.Image) -> None:
    og = Image.new("RGB", (1200, 630), (255, 248, 250))
    d = ImageDraw.Draw(og)
    for y in range(630):
        t = y / 630
        d.line((0, y, 1200, y), fill=(255, int(248 - 12 * t), int(250 - 18 * t)))
    d.rounded_rectangle((54, 92, 1137, 554), radius=42, fill=(255, 255, 255))
    face = icon.resize((224, 224), Image.Resampling.LANCZOS)
    og.paste(face, (114, 182))
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font = ImageFont.truetype(font_path, 47)
    small = ImageFont.truetype(font_path, 23)
    d.text((122, 431), "AI Study Sheet", font=font, fill=(28, 34, 53))
    d.text((125, 497), "Photos  •  PDFs  •  Recall", font=small, fill=(88, 99, 115))
    framed = shot.copy()
    framed.thumbnail((330, 716), Image.Resampling.LANCZOS)
    og.paste(framed, (770, 52))
    og.save(OUT / f"og-{lang}.jpg", quality=88, optimize=True)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for lang, country in LOCALES.items():
        lookup = "https://itunes.apple.com/lookup?" + urlencode({"id": APP_ID, "country": country, "entity": "software"})
        payload = json.loads(download(lookup).decode("utf-8"))
        if payload.get("resultCount") != 1:
            raise RuntimeError(f"Store lookup not found: {country}")
        app = payload["results"][0]
        if str(app.get("version", "")).removeprefix("v") != "4.0.0":
            raise RuntimeError(f"Store version isn't v4.0.0 for {country}: {app.get('version')}")
        shots = app.get("screenshotUrls") or []
        if len(shots) < len(NAMES):
            raise RuntimeError(f"Only {len(shots)} screenshots found for {country}; expected six")
        images = [screenshot(url, OUT / f"{lang}-{name}.webp") for name, url in zip(NAMES, shots)]
        artwork = app.get("artworkUrl512") or app.get("artworkUrl100")
        if not artwork:
            raise RuntimeError(f"Missing app icon artwork URL for {country}")
        icon = Image.open(BytesIO(download(artwork))).convert("RGB")
        if lang == "ja":
            icon.resize((512, 512), Image.Resampling.LANCZOS).save(OUT / "app-icon.png", optimize=True)
        make_og(lang, icon, images[0])
        print(f"{lang}: v4.0.0, six screenshots, OG media OK")
    print("All four locales synced from production App Store v4.0.0.")


if __name__ == "__main__":
    main()
