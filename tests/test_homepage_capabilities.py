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

    def test_homepage_copy_uses_capability_led_agent_product_positioning(self):
        html = HOME.read_text(encoding="utf-8")
        for phrase in [
            "把真实业务问题，转化为可执行、可验证、可复用的 Agent 产品方案。",
            "能力与方法",
            "不是工具清单，而是我解决问题的四种方式。",
            "需求与场景拆解",
            "Agent 产品设计",
            "评测与效果优化",
            "交付与标准化复制",
            "需求分析 · 用户调研 · 流程建模 · 产品方案",
            "Agent 工作流 · 知识库 · Prompt / SOP · Tool Use",
            "评测集构建 · Bad Case 归因 · Prompt 调优 · 上线复盘",
            "B 端交付 · 验收推进 · Skill 沉淀 · 1-N 复制",
            "我擅长把模糊需求拆解为可落地的 Agent 产品方案",
            "AI Native 学习与实践能力",
        ]:
            self.assertIn(phrase, html)
        for superseded_phrase in [
            "在业务场景、AI 能力边界与产品方案之间做连接",
            "我擅长在业务场景、AI 能力边界、产品方案与研发实现之间做连接",
        ]:
            self.assertNotIn(superseded_phrase, html)
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


if __name__ == "__main__":
    unittest.main()
