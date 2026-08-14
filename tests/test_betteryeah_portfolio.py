from html.parser import HTMLParser
from pathlib import Path
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
DETAIL = ROOT / "projects" / "betteryeah-ai-cs" / "index.html"
DEMO = ROOT / "projects" / "betteryeah-ai-cs" / "demo" / "index.html"
SCREENSHOTS = [
    ROOT / "assets" / "images" / "betteryeah-ai-cs-hero.png",
    ROOT / "assets" / "images" / "betteryeah-ai-cs-work.png",
    ROOT / "assets" / "images" / "betteryeah-ai-cs-growth.png",
    ROOT / "assets" / "images" / "betteryeah-ai-cs-scale.png",
]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "a" and values.get("href"):
            self.links.append((values["href"], values))
        if tag == "img" and values.get("src"):
            self.images.append((values["src"], values))

    def handle_data(self, data):
        value = data.strip()
        if value:
            self.text.append(value)


def parse(path):
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def resolve_local(page, value):
    parts = urlsplit(value)
    if (
        parts.scheme
        or value.startswith("#")
        or value.startswith("mailto:")
        or value.startswith("tel:")
    ):
        return None
    path = unquote(parts.path)
    target = (page.parent / path).resolve()
    if path.endswith("/"):
        target /= "index.html"
    return target


class BetterYeahPortfolioTest(unittest.TestCase):
    def test_detail_page_contains_pm_story_and_demo_link(self):
        self.assertTrue(DETAIL.is_file())
        page = parse(DETAIL)
        text = " ".join(page.text)
        for phrase in ["AI 产品经理", "三个关键判断", "我做了什么", "待上线"]:
            self.assertIn(phrase, text)
        demo_links = [(href, attrs) for href, attrs in page.links if href == "demo/"]
        self.assertEqual(len(demo_links), 2)
        for _, attrs in demo_links:
            self.assertEqual(attrs.get("target"), "_blank")
            self.assertIn("noopener", attrs.get("rel", ""))

    def test_demo_and_four_screenshots_exist(self):
        self.assertTrue(DEMO.is_file())
        for screenshot in SCREENSHOTS:
            self.assertTrue(screenshot.is_file(), screenshot)
            self.assertGreater(screenshot.stat().st_size, 20_000)

    def test_detail_images_have_alt_text_and_resolve(self):
        self.assertTrue(DETAIL.is_file())
        page = parse(DETAIL)
        self.assertEqual(
            len([src for src, _ in page.images if "betteryeah-ai-cs-" in src]), 4
        )
        for src, attrs in page.images:
            self.assertTrue(attrs.get("alt", "").strip(), src)
            target = resolve_local(DETAIL, src)
            if target:
                self.assertTrue(target.is_file(), target)

    def test_public_pages_link_to_detail(self):
        for page_path in [ROOT / "index.html", ROOT / "projects" / "index.html"]:
            page = parse(page_path)
            targets = [resolve_local(page_path, href) for href, _ in page.links]
            self.assertIn(DETAIL.resolve(), targets)

    def test_changed_pages_have_no_broken_local_links(self):
        self.assertTrue(DETAIL.is_file())
        for page_path in [DETAIL, ROOT / "index.html", ROOT / "projects" / "index.html"]:
            page = parse(page_path)
            for value, _ in page.links + page.images:
                target = resolve_local(page_path, value)
                if target:
                    self.assertTrue(target.is_file(), f"{page_path}: {value}")


if __name__ == "__main__":
    unittest.main()
