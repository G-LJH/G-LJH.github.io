from html.parser import HTMLParser
from pathlib import Path
import struct
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
DETAIL = ROOT / "projects" / "agent-for-you" / "index.html"
PROJECTS = ROOT / "projects" / "index.html"
STYLES = ROOT / "css" / "site.css"
FEATURE_IMAGES = {
    "agent-for-you-main-panel.png": (1200, 700),
    "agent-for-you-workspaces.png": (2500, 900),
    "agent-for-you-meeting-setup.png": (1200, 700),
    "agent-for-you-automations.png": (2500, 900),
}


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


def png_size(path):
    with path.open("rb") as image:
        signature = image.read(24)
    if signature[:8] != b"\x89PNG\r\n\x1a\n":
        raise AssertionError(f"Not a PNG file: {path}")
    return struct.unpack(">II", signature[16:24])


class AgentForYouPortfolioTest(unittest.TestCase):
    def test_page_tells_ai_pm_story(self):
        self.assertTrue(DETAIL.is_file())
        text = " ".join(parse(DETAIL).text)
        for phrase in [
            "AI 产品经理",
            "工作不发生在聊天框",
            "Vibe Coding",
            "基于 pi",
            "三个关键产品决策",
        ]:
            self.assertIn(phrase, text)

    def test_page_introduces_four_core_capabilities(self):
        text = " ".join(parse(DETAIL).text)
        for phrase in ["项目工作台", "工作区与长期记忆", "AI 会议", "定时任务"]:
            self.assertIn(phrase, text)

    def test_feature_grid_uses_four_compact_linked_screenshots(self):
        html = DETAIL.read_text(encoding="utf-8")
        page = parse(DETAIL)
        self.assertIn('class="agent-feature-grid"', html)
        self.assertEqual(html.count('class="agent-feature-card"'), 4)
        feature_links = {
            Path(urlsplit(href).path).name: attrs
            for href, attrs in page.links
            if Path(urlsplit(href).path).name in FEATURE_IMAGES
        }
        self.assertEqual(set(feature_links), set(FEATURE_IMAGES))
        for attrs in feature_links.values():
            self.assertEqual(attrs.get("target"), "_blank")
            self.assertIn("noopener", attrs.get("rel", ""))

    def test_feature_images_are_high_resolution_pngs_with_alt_text(self):
        page = parse(DETAIL)
        image_alts = {
            Path(urlsplit(src).path).name: attrs.get("alt", "").strip()
            for src, attrs in page.images
            if Path(urlsplit(src).path).name in FEATURE_IMAGES
        }
        self.assertEqual(set(image_alts), set(FEATURE_IMAGES))
        for name, (minimum_width, minimum_height) in FEATURE_IMAGES.items():
            target = ROOT / "assets" / "images" / name
            self.assertTrue(target.is_file(), target)
            width, height = png_size(target)
            self.assertGreaterEqual(width, minimum_width, name)
            self.assertGreaterEqual(height, minimum_height, name)
            self.assertTrue(image_alts[name], name)

    def test_projects_list_uses_new_positioning(self):
        text = " ".join(parse(PROJECTS).text)
        self.assertIn("持续工作的本地个人 Agent", text)
        self.assertIn("长期记忆、会议与定时任务", text)

    def test_styles_define_compact_desktop_and_mobile_layouts(self):
        css = STYLES.read_text(encoding="utf-8")
        self.assertIn(".agent-feature-grid", css)
        self.assertIn("grid-template-columns: repeat(2, minmax(0, 1fr));", css)
        self.assertIn(".agent-feature-card img", css)
        mobile = css[css.index("@media (max-width: 640px)") :]
        self.assertIn(".agent-feature-grid", mobile)
        self.assertIn("grid-template-columns: 1fr;", mobile)

    def test_changed_pages_have_no_broken_local_links(self):
        for page_path in [DETAIL, PROJECTS]:
            page = parse(page_path)
            for value, _ in page.links + page.images:
                target = resolve_local(page_path, value)
                if target:
                    self.assertTrue(target.is_file(), f"{page_path}: {value}")


if __name__ == "__main__":
    unittest.main()
