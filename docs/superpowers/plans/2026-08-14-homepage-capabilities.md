# Homepage Capabilities Section Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a responsive “能力与方法” section to the homepage that presents four evidence-backed capabilities and a concise self-evaluation before the internship history.

**Architecture:** Keep the site fully static. Add semantic HTML and a page anchor in `index.html`, load an isolated homepage capability stylesheet after the existing shared stylesheet, and protect the content order and responsive layout with a focused standard-library unittest file. The isolated stylesheet inherits the existing CSS variables while avoiding the unrelated uncommitted changes currently present in `css/site.css`.

**Tech Stack:** HTML5, CSS Grid, Python `unittest`

## Global Constraints

- Preserve all unrelated, pre-existing uncommitted changes, especially the current BetterYeah case-study edits in `css/site.css` and `tests/test_betteryeah_portfolio.py`; do not edit or stage either file for this feature.
- Reuse the existing `block-section`, `section-label`, `tile`, color variables, radius variables, border, and shadow styles.
- Do not add JavaScript, icon libraries, animation frameworks, external dependencies, or a separate “自我评价” navigation item.
- Keep the homepage order exactly: Hero → 能力与方法 → 实习经历 → 作品 → 联系.
- Desktop uses a two-column capability grid; viewports at or below 640px use one column without changing source order.
- Do not modify project detail pages, resume PDFs, or existing project copy.

## File Map

- Create `tests/test_homepage_capabilities.py`: focused structural and responsive-contract tests for the homepage module.
- Create `css/home-capabilities.css`: capability-card, evidence, self-evaluation, and mobile-grid styles that inherit variables from `site.css`.
- Modify `index.html`: load the isolated stylesheet, then add the “能力” navigation link and semantic capability/self-evaluation markup.

---

### Task 1: Homepage content and semantic structure

**Files:**
- Create: `tests/test_homepage_capabilities.py`
- Modify: `index.html` immediately after the closing tag of `.hero-tile`

**Interfaces:**
- Consumes: existing homepage anchors `#experience` and `#contact`, and shared classes `block-section`, `section-label`, and `tile`.
- Produces: the stable anchor `#capabilities` and CSS hooks `.capabilities-grid`, `.capability-card`, `.capability-evidence`, and `.capabilities-statement` for Task 2.

- [ ] **Step 1: Write failing homepage structure tests**

Create `tests/test_homepage_capabilities.py` with:

```python
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
        self.assertIn('<link rel="stylesheet" href="css/home-capabilities.css" />', html)
        css = STYLES.read_text(encoding="utf-8")
        self.assertIn(".capabilities-grid {", css)
        self.assertIn("grid-template-columns: repeat(2, minmax(0, 1fr));", css)
        mobile = css[css.index("@media (max-width: 640px)") :]
        self.assertIn(".capabilities-grid {", mobile)
        self.assertIn("grid-template-columns: 1fr;", mobile)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the focused test and verify it fails**

Run:

```bash
python3 -m unittest tests/test_homepage_capabilities.py -v
```

Expected: two failures for the missing HTML content and one error because `css/home-capabilities.css` does not exist yet.

- [ ] **Step 3: Add the navigation anchor**

In the `.nav` element in `index.html`, insert the new link before “经历”:

```html
<nav class="nav">
  <a href="#capabilities">能力</a>
  <a href="#experience">经历</a>
  <a href="projects/">作品</a>
  <a href="#contact">联系</a>
</nav>
```

- [ ] **Step 4: Add the semantic capability module**

In `index.html`, insert the following markup between the closing `</section>` of `.hero-tile` and `<section id="experience" ...>`:

```html
<section id="capabilities" class="block-section" aria-labelledby="capabilities-title">
  <div class="section-label">
    <h2 id="capabilities-title">能力与方法</h2>
    <p>不是工具清单，而是我解决问题的四种方式。</p>
  </div>

  <div class="capabilities-grid">
    <article class="tile capability-card">
      <h3>场景与产品</h3>
      <p>澄清客户需求，拆解业务场景与流程，识别 AI 能力边界，把模糊问题转成可实现、可验收的产品方案。</p>
      <p class="capability-evidence">需求调研 · 流程建模 · 方案设计 · 验收推进</p>
    </article>

    <article class="tile capability-card">
      <h3>Agent 构建</h3>
      <p>设计 Agent 工作流、知识体系、SOP 与 Prompt，并补齐工具调用、多轮对话、异常兜底和转人工策略。</p>
      <p class="capability-evidence">FastGPT · RAG · Knowledge · Tool Use</p>
    </article>

    <article class="tile capability-card">
      <h3>评测与优化</h3>
      <p>通过 Testcase、评测集和 Bad Case 归因定位问题，持续优化 Prompt、知识与配置。</p>
      <p class="capability-evidence">约 600 条评测集通过率 85% → 92%</p>
    </article>

    <article class="tile capability-card">
      <h3>交付与复用</h3>
      <p>推动方案完成上线、培训、复盘与规模化复制，并将一次性经验沉淀为模板、SOP 和 Skill。</p>
      <p class="capability-evidence">1 个月交付 19 个 Agent · 37 个意图骨架</p>
    </article>
  </div>

  <article class="tile capabilities-statement" aria-labelledby="self-review-title">
    <h3 id="self-review-title">自我评价</h3>
    <p>我擅长在业务场景、AI 能力边界、产品方案与研发实现之间做连接，推动 Agent 从需求走到上线，再沉淀成可复用的方法。比起只做需求翻译，我更愿意自己下场搭建、评测和造工具，把模糊想法变成真正可用的结果。</p>
  </article>
</section>
```

- [ ] **Step 5: Run the focused test and confirm only the CSS contract still fails**

Run:

```bash
python3 -m unittest tests/test_homepage_capabilities.py -v
```

Expected: the navigation/order and copy tests pass; the desktop/mobile CSS test errors because the isolated stylesheet does not exist yet.

- [ ] **Step 6: Commit the semantic content**

```bash
git add index.html tests/test_homepage_capabilities.py
git commit -m "feat: add homepage capabilities content"
```

Expected: the commit contains only `index.html` and `tests/test_homepage_capabilities.py`.

---

### Task 2: Isolated capability styling and responsive verification

**Files:**
- Create: `css/home-capabilities.css`
- Modify: `index.html` in `<head>`, immediately after the existing `css/site.css` link
- Test: `tests/test_homepage_capabilities.py`

**Interfaces:**
- Consumes: Task 1 hooks `.capabilities-grid`, `.capability-card`, `.capability-evidence`, and `.capabilities-statement`.
- Produces: a two-column desktop grid, one-column mobile grid, and a visually distinct self-evaluation card; no JavaScript or exported API. The stylesheet relies on variables already defined by `css/site.css`.

- [ ] **Step 1: Load the isolated homepage stylesheet**

In `index.html`, add the second stylesheet link immediately after the existing `css/site.css` link:

```html
<link rel="stylesheet" href="css/site.css" />
<link rel="stylesheet" href="css/home-capabilities.css" />
```

- [ ] **Step 2: Create the complete component stylesheet**

Create `css/home-capabilities.css` with:

```css
/* ——— Capabilities ——— */
.capabilities-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.85rem;
}

.capability-card {
  display: flex;
  flex-direction: column;
  padding: 1.15rem 1.2rem 1.2rem;
}

.capability-card h3,
.capabilities-statement h3 {
  margin: 0;
  font-size: 1.02rem;
  font-weight: 700;
}

.capability-card > p:not(.capability-evidence) {
  margin: 0.55rem 0 0;
  color: var(--ink-soft);
  font-size: 0.9rem;
  line-height: 1.65;
}

.capability-evidence {
  margin: auto 0 0;
  padding-top: 0.8rem;
  color: var(--accent-deep);
  font-size: 0.78rem;
  font-weight: 600;
  line-height: 1.5;
}

.capabilities-statement {
  margin-top: 0.85rem;
  padding: 1.25rem 1.3rem 1.35rem;
  background: #171b27;
  color: #fff;
}

.capabilities-statement h3 {
  color: #9fbdff;
  font-size: 0.82rem;
  letter-spacing: 0.05em;
}

.capabilities-statement p {
  margin: 0.55rem 0 0;
  max-width: 62rem;
  color: rgba(255, 255, 255, 0.82);
  font-size: 0.96rem;
  line-height: 1.75;
}

@media (max-width: 640px) {
  .capabilities-grid {
    grid-template-columns: 1fr;
  }

  .capability-card,
  .capabilities-statement {
    padding-right: 1.05rem;
    padding-left: 1.05rem;
  }
}
```

- [ ] **Step 3: Run focused and full automated tests**

Run:

```bash
python3 -m unittest tests/test_homepage_capabilities.py -v
python3 -m unittest discover -s tests -v
```

Expected: all homepage capability tests pass, followed by the complete test suite passing with no failures or errors.

- [ ] **Step 4: Preview desktop and mobile layouts**

Run:

```bash
python3 -m http.server 8765
```

Open `http://127.0.0.1:8765/` and verify at approximately 1280px and 390px viewport widths:

- “能力” scrolls to the new section.
- Desktop shows two equal card columns; mobile shows one column.
- No text is clipped or overlaps.
- The self-evaluation card spans the section width and remains readable.
- Existing resume menus, internship cards, works, and contact layout still behave normally.

- [ ] **Step 5: Inspect the final diff for scope and accidental overwrites**

Run:

```bash
git diff -- index.html css/home-capabilities.css tests/test_homepage_capabilities.py
git status --short
```

Expected: the feature diff contains only the new homepage module, its isolated stylesheet, and its dedicated tests. Existing unrelated working-tree changes remain present and unchanged; `css/site.css` and `tests/test_betteryeah_portfolio.py` still show only their pre-existing edits.

- [ ] **Step 6: Commit the responsive styling**

```bash
git add index.html css/home-capabilities.css
git commit -m "style: add responsive capability cards"
```

Expected: the commit contains only the new stylesheet and the stylesheet-link change in `index.html`; no unrelated file is staged.
