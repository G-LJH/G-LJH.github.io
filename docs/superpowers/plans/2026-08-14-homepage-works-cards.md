# Homepage Works Cards Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the homepage image thumbnails with an HR-friendly, text-first project-card grid whose first three projects are Agent_for_you, 医生智能助手, and AI 智能客服官网.

**Architecture:** Keep the site static and reuse the existing homepage section, native links, design tokens, and responsive stylesheet. Add one focused regression test file for content order, links, text-only markup, CTA language, and responsive/accessibility CSS; then replace only the homepage works markup and its existing `.works-*` style block.

**Tech Stack:** Static HTML5, CSS3, Python `unittest`

## Global Constraints

- Modify only the homepage works section, its related styles, and focused tests.
- Do not modify the standalone projects index or any case-study page.
- Use no project thumbnail images in the homepage works section.
- Preserve the existing light, restrained, professional site visual system.
- Order the first three cards exactly as `Agent_for_you`, `医生智能助手`, `AI 智能客服官网`.
- Use native `<a>` elements for every card, visible `:focus-visible` styling, a single-column mobile layout, and reduced-motion handling.
- Preserve unrelated dirty-worktree changes.

---

### Task 1: Add Homepage Works Regression Coverage

**Files:**
- Create: `tests/test_homepage_works.py`
- Read: `index.html`
- Read: `css/site.css`

**Interfaces:**
- Consumes: homepage section selected by `id="works"` and CSS classes prefixed with `.works-` or `.work-card`.
- Produces: regression checks that define the card order, six local targets, text-only presentation, CTA copy, responsive layout, focus treatment, and reduced-motion behavior.

- [ ] **Step 1: Write the failing tests**

```python
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
STYLES = ROOT / "css" / "site.css"


class HomepageWorksTest(unittest.TestCase):
    def setUp(self):
        self.html = HOME.read_text(encoding="utf-8")
        self.css = STYLES.read_text(encoding="utf-8")
        self.section = self.html[
            self.html.index('<section id="works"') : self.html.index(
                '<section id="contact"'
            )
        ]

    def test_core_projects_appear_first_in_required_order(self):
        names = ["Agent_for_you", "医生智能助手", "AI 智能客服官网"]
        positions = [self.section.index(name) for name in names]
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
        self.assertIn("grid-template-columns: repeat(2, minmax(0, 1fr));", self.css)
        self.assertIn(".work-card:focus-visible", self.css)
        mobile = self.css[self.css.index("@media (max-width: 640px)") :]
        self.assertIn(".works-grid", mobile)
        self.assertIn("grid-template-columns: 1fr;", mobile)
        self.assertIn("@media (prefers-reduced-motion: reduce)", self.css)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the focused test and verify it fails**

Run: `python3 -m unittest tests.test_homepage_works -v`

Expected: FAIL because the current homepage section has no `id="works"`, starts with the website project, uses thumbnail images, and lacks the new card classes.

- [ ] **Step 3: Commit the test definition**

```bash
git add tests/test_homepage_works.py
git commit -m "test: define homepage works card behavior"
```

### Task 2: Build the Text-First Homepage Works Cards

**Files:**
- Modify: `index.html` works section
- Modify: `css/site.css` existing Works block and responsive rules
- Test: `tests/test_homepage_works.py`

**Interfaces:**
- Consumes: existing `--surface`, `--ink`, `--muted`, `--accent`, `--line`, `--radius`, and `--shadow` CSS tokens and existing project detail URLs.
- Produces: `#works`, `.works-heading`, `.works-hint`, `.works-grid`, `.work-card`, `.work-card-featured`, `.work-card-top`, `.work-number`, `.work-tag`, `.work-summary`, `.work-proof`, and `.work-action` markup/styles.

- [ ] **Step 1: Replace the homepage works section markup**

Add `id="works"` to the section. Replace the thumbnail bento and separate “全部作品” tile with six native linked cards in this exact order and using these content contracts:

```html
<a class="tile work-card work-card-featured" href="projects/agent-for-you/">
  <div class="work-card-top"><span class="work-number">01</span><span class="work-tag">个人 Agent · Vibe Coding</span></div>
  <h3>Agent_for_you</h3>
  <p class="work-summary">让 AI 不止回答一次，而是围绕项目持续记忆、开会、整理文件并按时执行任务。</p>
  <p class="work-proof">从产品定义到本地原型，完整设计项目工作台、长期记忆、AI 会议与自动化任务。</p>
  <span class="work-action">查看详情 <span aria-hidden="true">↗</span></span>
</a>
```

Use the same structure for:

- `02` / `医疗 AI · 0–1 交付` / `医生智能助手` / “把专科知识、对话策略与安全兜底组合成可实际服务患者的医生 Agent。” / “搭建 8 位专科医生智能体，标准化模板让后续搭建周期缩短约 80%。”
- `03` / `产品官网 · AI 客服` / `AI 智能客服官网` / “从客户定位到价值表达，重新设计面向 KA 客群的 AI 智能客服产品官网。” / “完成竞品研究、信息架构、三层价值主张与可访问的完整官网 Demo。”
- `04` / `Agent 评测 · 自动化` / `LLM 自动化测评` / “用用户智能体与裁判智能体批量模拟对话，让 Agent 回归测试稳定可复现。” / “支持无代码配置与多维评分，把原本天级的人工回归压缩到分钟级。”
- `05` / `企业微信 · 工程方案` / `企业微信会话存档` / “用第三方回调完成低成本会话沉淀，为后续质检与 RAG 留下数据接口。” / “将官方方案约 9 万元/人/年的成本降至接近 0，并沉淀为公司服务能力。”
- `06` / `AI 求职 · 产品闭环` / `牛客 AI 面试教练` / “结合面经、简历与 JD，生成针对具体岗位的个性化面试准备报告。” / “覆盖 8 大准备模块，把零散招聘信息组织成可直接练习的行动方案。”

Place this instruction beneath the section title:

```html
<p class="works-hint"><span aria-hidden="true">↘</span> 点击卡片查看详情</p>
```

- [ ] **Step 2: Replace the existing works styles**

Implement a two-column `.works-grid`, a dark gradient `.work-card-featured`, consistent minimum card height, flex column layout, compact pill tags, muted proof text separated by a top border, and bottom-aligned `.work-action`. Add hover and `:focus-visible` states with no reliance on color alone. On hover/focus, move the card upward and translate the action arrow slightly.

At `@media (max-width: 640px)`, set `.works-grid { grid-template-columns: 1fr; }`, reduce card padding/minimum height, and keep all cards readable without horizontal overflow.

Add:

```css
@media (prefers-reduced-motion: reduce) {
  .work-card,
  .work-action span {
    transition: none;
  }

  .work-card:hover,
  .work-card:focus-visible,
  .work-card:hover .work-action span,
  .work-card:focus-visible .work-action span {
    transform: none;
  }
}
```

- [ ] **Step 3: Run the focused regression tests**

Run: `python3 -m unittest tests.test_homepage_works -v`

Expected: 4 tests PASS.

- [ ] **Step 4: Run the full regression suite**

Run: `python3 -m unittest discover -s tests -v`

Expected: all existing and new tests PASS.

- [ ] **Step 5: Check changed-file integrity**

Run: `git diff --check -- index.html css/site.css tests/test_homepage_works.py`

Expected: no output and exit code 0.

- [ ] **Step 6: Commit the implementation**

```bash
git add index.html css/site.css tests/test_homepage_works.py
git commit -m "feat: redesign homepage works cards"
```
