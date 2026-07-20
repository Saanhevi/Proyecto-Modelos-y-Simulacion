# -*- coding: utf-8 -*-
"""
html_to_pdf.py
--------------
Exporta ../index.html a ../presentacion.pdf (una pagina por diapositiva).

Uso:
    python html_to_pdf.py

Dependencias:
    pip install playwright pymupdf pillow
    playwright install chromium
"""
from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

try:
    import fitz
    from PIL import Image
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Instala: pip install playwright pymupdf pillow && playwright install chromium")
    sys.exit(1)

PKG = Path(__file__).resolve().parent.parent
HTML = PKG / "index.html"
PDF_OUT = PKG / "presentacion.pdf"

VIEWPORT_W = 1920
VIEWPORT_H = 1080
SCALE = 1.5
JPEG_QUALITY = 92

PREPARE_PAGE_JS = """
() => {
  ['counter', 'progress', 'fs', 'lightbox'].forEach((id) => {
    const el = document.getElementById(id);
    if (el) el.style.display = 'none';
  });
  document.querySelectorAll('.slide').forEach((s) => { s.style.transition = 'none'; });
}
"""

GOTO_SLIDE_JS = """
(i) => {
  const slides = [...document.querySelectorAll('.slide')];
  slides.forEach((s, j) => {
    s.classList.toggle('active', j === i);
    s.style.transition = 'none';
    s.style.transform = 'none';
    s.style.filter = 'none';
    s.style.opacity = j === i ? '1' : '0';
    s.style.visibility = j === i ? 'visible' : 'hidden';
    s.style.zIndex = j === i ? '2' : '0';
  });
}
"""


def main() -> None:
    if not HTML.exists():
        raise SystemExit(f"No HTML: {HTML}")

    uri = HTML.resolve().as_uri()
    tmp = Path(tempfile.mkdtemp(prefix="e5_slides_"))
    shots: list[Path] = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context(
                viewport={"width": VIEWPORT_W, "height": VIEWPORT_H},
                device_scale_factor=SCALE,
            )
            page = context.new_page()
            page.goto(uri, wait_until="networkidle", timeout=90000)
            page.wait_for_timeout(800)
            page.evaluate(PREPARE_PAGE_JS)
            n = page.locator(".slide").count()
            print(f"Diapositivas: {n}")
            for i in range(n):
                page.evaluate(GOTO_SLIDE_JS, i)
                page.wait_for_timeout(200)
                page.wait_for_function(
                    """(i) => {
                      const slide = document.querySelectorAll('.slide')[i];
                      if (!slide) return false;
                      const imgs = slide.querySelectorAll('img');
                      if (!imgs.length) return true;
                      return [...imgs].every((img) => img.complete && img.naturalWidth > 0);
                    }""",
                    arg=i,
                    timeout=20000,
                )
                shot = tmp / f"slide_{i + 1:02d}.jpg"
                page.locator("#stage").screenshot(
                    path=str(shot), type="jpeg", quality=JPEG_QUALITY
                )
                shots.append(shot)
                print(f"  OK slide {i + 1}")
            browser.close()

        doc = fitz.open()
        for shot in shots:
            with Image.open(shot) as im:
                w, h = im.size
            pg = doc.new_page(width=w, height=h)
            pg.insert_image(pg.rect, filename=str(shot))
        doc.save(str(PDF_OUT), deflate=True)
        pages = doc.page_count
        doc.close()
        print(f"PDF: {PDF_OUT} ({pages} paginas, {PDF_OUT.stat().st_size // 1024} KB)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
