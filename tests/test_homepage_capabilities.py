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

    def test_homepage_copy_uses_full_chain_ai_agent_builder_positioning(self):
        html = HOME.read_text(encoding="utf-8")
        for phrase in [
            "Hangzhou · AI Agent Builder",
            "产品理解 × 工程落地",
            "站在业务、产品与工程之间，把真实问题做成可运行、可评测、可交付的 AI Agent。",
            "能力与方法",
            "不是工具清单，而是我解决问题的四种方式。",
            "需求与产品定义",
            "Agent 工程实现",
            "评测与效果迭代",
            "部署交付与复制",
            "需求分析 · 用户调研 · 工作流还原 · 产品方案",
            "RAG / 知识库 · Tool Use · Context / Memory · API 接入",
            "Testcase · Bad Case · LLM-as-a-Judge · 回归验证",
            "Docker / 1Panel · 渠道集成 · SOP / Skill · 1-N 复制",
            "我既能理解业务、做产品取舍",
            "职业规划",
            "成为贯通业务、产品、工程与交付的全链路 AI Agent Builder，独立负责从需求判断到上线迭代的完整闭环，并对最终业务结果负责。",
        ]:
            self.assertIn(phrase, html)
        self.assertNotIn("Hangzhou · AI Agent FDE", html)
        self.assertEqual(html.count('class="tile capability-card"'), 4)

    def test_experience_copy_matches_updated_resume(self):
        html = HOME.read_text(encoding="utf-8")
        for phrase in [
            "将产品定位从单轮问答扩展为「围绕项目持续工作」的 Agent 应用",
            "长期工作区、项目材料沉淀、本地 Markdown 记忆与跨会话召回机制",
            "支撑 AI 客服 1-N 规模化复制",
            "知识缺失、业务规则不清、配置错误与平台能力问题",
            "将常见问答、挂号指引、购药引导等高频问题拆解为 Agent 可执行的意图、流程和异常分支",
            "使 Agent 接入真实医患沟通链路",
            "将「研报解析—信息提取—多维度分析—报告生成」拆解为可编排的智能投研工作流",
        ]:
            self.assertIn(phrase, html)

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
        for selector in [".hero-positioning {", ".career-plan {"]:
            self.assertIn(selector, css)


if __name__ == "__main__":
    unittest.main()
