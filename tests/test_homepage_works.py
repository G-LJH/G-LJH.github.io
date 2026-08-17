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
        names = ["Agent for You", "医生智能助手", "BetterYeah AI 智能客服"]
        positions = [self.section.find(name) for name in names]
        self.assertNotIn(-1, positions)
        self.assertEqual(positions, sorted(positions))

    def test_section_has_four_projects_and_more_card(self):
        self.assertIn("点击卡片查看详情", self.section)
        self.assertEqual(self.section.count('class="tile work-card'), 4)
        for href in [
            "projects/agent-for-you/",
            "projects/doctor-assistant/",
            "projects/betteryeah-ai-cs/",
            "projects/fastgpt-agent-tester/",
        ]:
            self.assertIn(f'href="{href}"', self.section)
        self.assertNotIn('href="projects/wecom-archive/"', self.section)
        self.assertNotIn('href="projects/niuke-ai-coach/"', self.section)
        self.assertIn('class="tile works-more-card"', self.section)
        self.assertIn('href="projects/"', self.section)
        self.assertIn("查看更多作品", self.section)

    def test_homepage_works_section_is_text_only(self):
        self.assertNotIn("<img", self.section)
        self.assertNotIn("work-thumb", self.section)
        for number in ["01", "02", "03", "04"]:
            self.assertIn(f">{number}<", self.section)
        self.assertNotIn(">05<", self.section)
        self.assertNotIn(">06<", self.section)

    def test_agent_for_you_card_uses_the_same_light_style_as_other_cards(self):
        href_position = self.section.index('href="projects/agent-for-you/"')
        tag_start = self.section.rfind("<a", 0, href_position)
        tag_end = self.section.index(">", href_position)
        agent_card_tag = self.section[tag_start : tag_end + 1]
        self.assertIn('class="tile work-card"', agent_card_tag)
        self.assertNotIn("work-card-featured", agent_card_tag)

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

    def test_more_card_is_light_full_width_and_keyboard_accessible(self):
        self.assertIn(".works-more-card {", self.css)
        self.assertIn("grid-column: 1 / -1;", self.css)
        self.assertIn(".works-more-card:focus-visible", self.css)
        more_card_start = self.css.index(".works-more-card {")
        more_card_end = self.css.index("}", more_card_start)
        more_card_rule = self.css[more_card_start:more_card_end]
        self.assertNotIn("#101522", more_card_rule)
        self.assertNotIn("#19243b", more_card_rule)


if __name__ == "__main__":
    unittest.main()
