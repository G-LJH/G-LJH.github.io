from html.parser import HTMLParser
from pathlib import Path
import struct
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
DETAIL = ROOT / "projects" / "agent-for-you" / "index.html"
PROJECTS = ROOT / "projects" / "index.html"
STYLES = ROOT / "css" / "site.css"
FEATURE_IMAGES = {
    "agent-for-you-chat.png": (2500, 1200),
    "agent-for-you-workspaces.png": (2500, 1200),
    "agent-for-you-meeting-workspace.png": (1400, 1000),
    "agent-for-you-automations.png": (2500, 1200),
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
    def test_homepage_introduces_the_personal_agent_in_one_compact_block(self):
        html = HOME.read_text(encoding="utf-8")
        for phrase in [
            "面向个人日常工作的本地桌面 Agent",
            "在后续任务中复用个人上下文",
            "产品定位：",
            "本地优先、长期记忆与能力可扩展",
            "功能集成：",
            "项目工作台、长期记忆、AI 会议、自动化、MCP、Computer Use 与任务录制",
            "可运行落地：",
            "React、Node.js 与 Electron",
            "完成主要能力集成和桌面可运行版本",
        ]:
            self.assertIn(phrase, html)
        self.assertEqual(html.count('class="project-block agent-overview-project"'), 1)
        self.assertIn('class="result-list agent-overview-resume"', html)
        self.assertNotIn('class="agent-overview-tags"', html)

    def test_detail_page_leads_with_the_personal_agent_positioning(self):
        self.assertTrue(DETAIL.is_file())
        text = " ".join(parse(DETAIL).text)
        for phrase in [
            "一个会在工作中持续了解你的个人 Agent",
            "本地优先、可持续扩展的桌面个人 Agent",
            "长期参与用户的日常工作",
            "同一份用户记忆和项目上下文",
            "本地优先",
            "长期记忆",
            "能力可扩展",
            "桌面可运行版本",
        ]:
            self.assertIn(phrase, text)

    def test_detail_page_builds_from_memory_to_capabilities_and_productization(self):
        text = " ".join(parse(DETAIL).text)
        for phrase in [
            "真正的个人化，不是换一个人设",
            "对话产生记忆，记忆进入下一次工作",
            "同一个 Agent，围绕项目持续工作",
            "在同一个底座上不断获得新的工作能力",
            "MCP",
            "Computer Use",
            "任务录制器",
            "可复用的 Skill",
            "把高权限、长生命周期 Agent 做成可控制的桌面产品",
            "React",
            "Node.js Studio Server",
            "独立的 Pi Agent 进程",
            "Electron",
        ]:
            self.assertIn(phrase, text)

    def test_page_keeps_four_existing_work_capabilities(self):
        text = " ".join(parse(DETAIL).text)
        for phrase in ["项目工作台", "长期记忆", "AI 会议", "定时任务"]:
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
        self.assertIn("一个会在工作中持续了解你的个人 Agent", text)
        self.assertIn("本地优先、长期记忆、能力可扩展", text)

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
