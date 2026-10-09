"""Create deterministic PDF exports of the engineering case-sheet SVGs."""
from __future__ import annotations

import hashlib
import io
from pathlib import Path

import cairosvg
from pypdf import PdfReader, PdfWriter

CASE_NAMES = ("00-overview", "01-air", "02-waterjet", "03-maybell")

def normalized_pdf(pages, title, fingerprint):
    writer = PdfWriter()
    for raw in pages:
        reader = PdfReader(io.BytesIO(raw), strict=True)
        writer.append(reader)
    writer.add_metadata({
        "/Title": title,
        "/Author": "Tucker Vana",
        "/Producer": "career-portfolio / CairoSVG and pypdf",
        "/PortfolioSourceSHA256": fingerprint,
    })
    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()

def build_pdf_exports(root: Path, generated_sources):
    exports = {}
    pages = []
    combined = hashlib.sha256()
    for name in CASE_NAMES:
        relative = f"artifacts/career-sheets/{name}.svg"
        retained = root / relative
        source = generated_sources[retained].read_bytes()
        fingerprint = hashlib.sha256(source).hexdigest()
        combined.update(relative.encode("utf-8") + b"\0" + source + b"\0")
        raw = cairosvg.svg2pdf(bytestring=source)
        title = "Tucker Vana / " + name.replace("-", " ")
        exports[f"artifacts/career-sheets/{name}.pdf"] = normalized_pdf([raw], title, fingerprint)
        pages.append(raw)
    exports["artifacts/career-sheets/engineering-portfolio.pdf"] = normalized_pdf(
        pages, "Tucker Vana / Engineering case packet", combined.hexdigest()
    )
    return exports
