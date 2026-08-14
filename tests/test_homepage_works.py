from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
STYLES = ROOT / "css" / "site.css"


class HomepageWorksTest(unittest.TestCase):
    def setUp(self):
        self.html = HOME.read_text(encoding="utf-8")
        self.css = STYLES.read_text(encoding="utf-8")
        works_marker = self.html.index('aria-labelledby="works-title"')
        works_start = self.html.rfind("<section", 0, works_marker)
        works_end = self.html.index('<section id="contact"', works_start)
        self.section = self.html[works_start:works_end]

    def test_core_projects_appear_first_in_required_order(self):
        names = ["Agent_for_you", "医生智能助手", "AI 智能客服官网"]
        positions = [self.section.find(name) for name in names]
        self.assertNotIn(-1, positions)
        self.assertEqual(positions, sorted(positions))

    def test_section_has_six_linked_text_cards_and_clear_instruction(self):
        self.assertIn("点击卡片查看详情", self.section)
        self.assertEqual(self.section.count('class="tile work-card'), 6)
        for href in [
            "projects/agent-for-you/",
            "projects/doctor-assistant/",
            "projects/betteryeah-ai-cs/",
            "projects/fastgpt-agent-tester/",
            "projects/wecom-archive/",
            "projects/niuke-ai-coach/",
        ]:
            self.assertIn(f'href="{href}"', self.section)

    def test_homepage_works_section_is_text_only(self):
        self.assertNotIn("<img", self.section)
        self.assertNotIn("work-thumb", self.section)
        for number in ["01", "02", "03", "04", "05", "06"]:
            self.assertIn(f">{number}<", self.section)

    def test_styles_cover_grid_focus_mobile_and_reduced_motion(self):
        self.assertIn(".works-grid {", self.css)
        self.assertIn(
            "grid-template-columns: repeat(2, minmax(0, 1fr));", self.css
        )
        self.assertIn(".work-card:focus-visible", self.css)
        mobile = self.css[self.css.index("@media (max-width: 640px)") :]
        self.assertIn(".works-grid", mobile)
        self.assertIn("grid-template-columns: 1fr;", mobile)
        self.assertIn("@media (prefers-reduced-motion: reduce)", self.css)


if __name__ == "__main__":
    unittest.main()
