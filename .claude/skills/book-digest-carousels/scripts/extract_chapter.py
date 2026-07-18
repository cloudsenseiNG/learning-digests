#!/usr/bin/env python3
"""Extract clean text from a page range of a PDF.

Usage:
    python extract_chapter.py --pdf book.pdf --pages 12-34

Prints the extracted text to stdout. Use this once a chapter's page range is known
(cache the range in TRACKER.md so future runs skip the lookup). For scanned/image
PDFs this yields little text — OCR those pages instead.

    pip install pypdf
"""
import argparse
import sys

try:
    from pypdf import PdfReader
except ImportError:
    sys.exit("pypdf not installed. Run: pip install pypdf")


def parse_pages(spec, total):
    if "-" in spec:
        start, end = spec.split("-", 1)
        start, end = int(start), int(end)
    else:
        start = end = int(spec)
    start = max(1, start)
    end = min(total, end)
    return start, end


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--pages", required=True, help="e.g. 12-34 (1-indexed, inclusive)")
    args = ap.parse_args()

    reader = PdfReader(args.pdf)
    total = len(reader.pages)
    start, end = parse_pages(args.pages, total)

    chunks = []
    for i in range(start - 1, end):
        chunks.append(reader.pages[i].extract_text() or "")
    print("\n\n".join(chunks).strip())


if __name__ == "__main__":
    main()
