#!/usr/bin/env python3
"""Export project detail pages to A4 PDF via Chrome headless (print CSS).

Usage:
  python3 scripts/export_works_pdf.py              # all works + portfolio
  python3 scripts/export_works_pdf.py agent-for-you doctor-assistant
"""

from __future__ import annotations

import argparse
import http.server
import socketserver
import subprocess
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "assets" / "pdf" / "works"
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
COVER_PATH = ROOT / "projects" / "print-portfolio-cover.html"

# slug -> output filename stem
PROJECTS = [
    ("agent-for-you", "Agent-for-You"),
    ("doctor-assistant", "医生智能助手"),
    ("betteryeah-ai-cs", "BetterYeah-AI智能客服"),
    ("fastgpt-agent-tester", "LLM自动化测评"),
    ("wecom-archive", "企业微信会话存档"),
    ("xbotos-monitor", "xbotos机器人监控"),
    ("niuke-ai-coach", "牛客AI面试教练"),
]


def start_server(directory: Path) -> tuple[socketserver.TCPServer, int]:
    root = str(directory)

    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=root, **kwargs)

        def log_message(self, format: str, *args) -> None:  # noqa: A003
            return

    httpd = socketserver.TCPServer(("127.0.0.1", 0), QuietHandler)
    httpd.allow_reuse_address = True
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd, port


def chrome_print(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        dest.unlink()
    cmd = [
        str(CHROME),
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--virtual-time-budget=10000",
        f"--print-to-pdf={dest}",
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 or not dest.exists() or dest.stat().st_size < 1000:
        raise RuntimeError(
            f"Chrome PDF failed for {url}\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )


def merge_pdfs(inputs: list[Path], dest: Path) -> bool:
    try:
        from pypdf import PdfWriter
    except ImportError:
        try:
            from PyPDF2 import PdfWriter  # type: ignore
        except ImportError:
            return False

    writer = PdfWriter()
    for path in inputs:
        writer.append(str(path))
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("wb") as fh:
        writer.write(fh)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "slugs",
        nargs="*",
        help="Optional project slugs; default = all",
    )
    parser.add_argument(
        "--no-portfolio",
        action="store_true",
        help="Skip merged portfolio PDF",
    )
    args = parser.parse_args()

    if not CHROME.exists():
        print(f"Chrome not found at {CHROME}", file=sys.stderr)
        return 1

    wanted = set(args.slugs) if args.slugs else {slug for slug, _ in PROJECTS}
    selected = [(slug, name) for slug, name in PROJECTS if slug in wanted]
    unknown = wanted - {slug for slug, _ in PROJECTS}
    if unknown:
        print(f"Unknown slugs: {', '.join(sorted(unknown))}", file=sys.stderr)
        return 1
    if not selected:
        print("No projects selected", file=sys.stderr)
        return 1

    httpd, port = start_server(ROOT)
    time.sleep(0.3)
    written: list[Path] = []

    try:
        for slug, stem in selected:
            url = f"http://127.0.0.1:{port}/projects/{slug}/"
            dest = OUT_DIR / f"{stem}.pdf"
            print(f"Exporting {slug} → {dest.relative_to(ROOT)}")
            chrome_print(url, dest)
            written.append(dest)
            print(f"  {dest.stat().st_size // 1024} KB")

        if not args.no_portfolio and len(written) >= 1:
            cover_pdf = OUT_DIR / "_cover.pdf"
            cover_url = f"http://127.0.0.1:{port}/projects/print-portfolio-cover.html"
            print(f"Exporting cover → {cover_pdf.relative_to(ROOT)}")
            chrome_print(cover_url, cover_pdf)

            portfolio = OUT_DIR / "作品集总册.pdf"
            merge_inputs = [cover_pdf, *written]
            if merge_pdfs(merge_inputs, portfolio):
                print(f"Merged portfolio → {portfolio.relative_to(ROOT)}")
                print(f"  {portfolio.stat().st_size // 1024} KB")
                cover_pdf.unlink(missing_ok=True)
            else:
                print(
                    "Skip portfolio merge (install: pip install pypdf)",
                    file=sys.stderr,
                )
    finally:
        httpd.shutdown()

    print(f"Done. Files in {OUT_DIR.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
