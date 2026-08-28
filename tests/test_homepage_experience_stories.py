from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
STYLES = ROOT / "css" / "site.css"


class HomepageExperienceStoriesTest(unittest.TestCase):
    def setUp(self):
        self.html = HOME.read_text(encoding="utf-8")
        self.css = STYLES.read_text(encoding="utf-8")

        beauty_start = self.html.index("某头部美妆集团")
        fashion_start = self.html.index("某时尚鞋服集团", beauty_start)
        company_end = self.html.index('</article>', fashion_start)
        self.beauty_story = self.html[beauty_start:fashion_start]
        self.fashion_story = self.html[fashion_start:company_end]

    def test_customer_projects_remain_two_independent_stories(self):
        self.assertIn("多店规模化交付", self.beauty_story)
        self.assertIn("Agent 效果优化", self.fashion_story)
        self.assertLess(
            self.html.index("某头部美妆集团"),
            self.html.index("某时尚鞋服集团"),
        )
        self.assertEqual(self.html.count('class="project-block story-project"'), 2)

    def test_beauty_story_focuses_on_scalable_delivery(self):
        for phrase in [
            "19 个 Agent，不能靠重复交付 19 次。",
            "不同店铺都要重新整理资料、编写 SOP",
            "37 个意图骨架",
            "证据提取—SOP 合成—人工审阅",
            "支撑 AI 客服 1-N 规模化复制",
            "近一个月完成 <strong>19</strong> 个智能体优化交付并全部上线",
            "我把逐店重复搭建，变成了一套可复制的规模化交付方法。",
        ]:
            self.assertIn(phrase, self.beauty_story)
        self.assertNotIn("85%", self.beauty_story)
        self.assertNotIn("Bad Case", self.beauty_story)

    def test_fashion_story_focuses_on_effect_diagnosis(self):
        for phrase in [
            "400 条 Bad Case，不能都靠修改 Prompt 解决。",
            "如果都靠修改 Prompt 解决",
            "Prompt、知识缺失、业务规则不清、配置错误与平台能力问题五类",
            "约 <strong>600</strong> 条评测集",
            "<strong>85%</strong> 提升至 <strong>92%</strong>",
            "我把凭感觉调优，变成了基于归因和评测的优化闭环。",
        ]:
            self.assertIn(phrase, self.fashion_story)
        self.assertNotIn("37 个意图骨架", self.fashion_story)
        self.assertNotIn("19</strong> 个智能体", self.fashion_story)

    def test_story_markup_and_styles_support_fast_scanning(self):
        for label in ["痛点", "解决", "成果"]:
            self.assertEqual(
                self.html.count(f'<span class="story-label">{label}</span>'), 2
            )
        for selector in [
            ".story-project {",
            ".story-hook {",
            ".story-detail {",
            ".story-label {",
            ".story-takeaway {",
        ]:
            self.assertIn(selector, self.css)

    def test_experience_is_static_resume_content_without_project_links(self):
        experience_start = self.html.index('<section id="experience"')
        works_start = self.html.index('<section id="works"', experience_start)
        experience = self.html[experience_start:works_start]

        self.assertNotIn("<a ", experience)
        self.assertNotIn("查看项目详情", experience)
        self.assertIn("聚焦职责、行动与成果", experience)


if __name__ == "__main__":
    unittest.main()
