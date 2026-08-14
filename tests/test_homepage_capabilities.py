from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
STYLES = ROOT / "css" / "home-capabilities.css"


class HomepageCapabilitiesTest(unittest.TestCase):
    def test_capabilities_nav_and_section_precede_experience(self):
        html = HOME.read_text(encoding="utf-8")
        self.assertIn('<a href="#capabilities">能力</a>', html)
        self.assertIn('id="capabilities"', html)
        self.assertLess(html.index('id="capabilities"'), html.index('id="experience"'))

    def test_capabilities_copy_contains_four_methods_and_self_evaluation(self):
        html = HOME.read_text(encoding="utf-8")
        for phrase in [
            "能力与方法",
            "不是工具清单，而是我解决问题的四种方式。",
            "场景与产品",
            "Agent 构建",
            "评测与优化",
            "交付与复用",
            "约 600 条评测集通过率 85% → 92%",
            "1 个月交付 19 个 Agent · 37 个意图骨架",
            "我擅长在业务场景、AI 能力边界、产品方案与研发实现之间做连接",
            "把模糊想法变成真正可用的结果",
        ]:
            self.assertIn(phrase, html)
        self.assertEqual(html.count('class="tile capability-card"'), 4)

    def test_capabilities_styles_include_desktop_and_mobile_grids(self):
        html = HOME.read_text(encoding="utf-8")
        self.assertIn(
            '<link rel="stylesheet" href="css/home-capabilities.css" />', html
        )
        css = STYLES.read_text(encoding="utf-8")
        self.assertIn(".capabilities-grid {", css)
        self.assertIn("scroll-margin-top: 4.5rem;", css)
        self.assertIn(
            "grid-template-columns: repeat(2, minmax(0, 1fr));", css
        )
        mobile = css[css.index("@media (max-width: 640px)") :]
        self.assertIn(".capabilities-grid {", mobile)
        self.assertIn("grid-template-columns: 1fr;", mobile)


if __name__ == "__main__":
    unittest.main()
