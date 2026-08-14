# BetterYeah AI 智能客服作品页实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在个人官网中新增精简的 AI 产品经理作品详情页，将完整 AI 客服官网 HTML Demo 复制到项目目录，并从 Demo 生成四张真实截图辅助说明。

**Architecture:** 保持现有纯静态 HTML/CSS/JS 架构。项目详情页复用全站导航和 `detail-prose` 内容壳，通过少量新 CSS 支持元信息、三列判断卡和一大两小截图布局；完整官网作为同源静态子目录独立打开。使用 Python 标准库验证页面结构和本地链接，不引入构建工具或运行时依赖。

**Tech Stack:** HTML5、CSS3、原生 JavaScript、Python 3 `unittest` / `html.parser`、Google Chrome headless、GitHub Pages。

## Global Constraints

- 这是个人作品详情页，不是一张新的产品营销官网。
- 沿用个人站已有导航、字体、背景、卡片和按钮样式。
- 页面使用四张从正式 Demo 生成的截图：首屏、会干活、会成长、铺得开各一张。
- 完整官网在 `/projects/betteryeah-ai-cs/demo/` 独立打开，不使用长 iframe。
- 不写未经核准的客户数字，不把评审状态写成正式上线。
- 保留当前工作区中与本项目无关的未提交改动。

---

### Task 1: 建立静态页面验证

**Files:**
- Create: `tests/test_betteryeah_portfolio.py`

**Interfaces:**
- Consumes: 仓库根目录下的静态 HTML 文件与本地资源。
- Produces: `python3 -m unittest tests/test_betteryeah_portfolio.py -v`，验证详情页结构、Demo、截图和入口。

- [ ] **Step 1: 写出失败的结构测试**

创建 `tests/test_betteryeah_portfolio.py`，使用 `HTMLParser` 收集链接、图片和文本，并断言：

```python
from html.parser import HTMLParser
from pathlib import Path
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
DETAIL = ROOT / "projects" / "betteryeah-ai-cs" / "index.html"
DEMO = ROOT / "projects" / "betteryeah-ai-cs" / "demo" / "index.html"
SCREENSHOTS = [
    ROOT / "assets" / "images" / "betteryeah-ai-cs-hero.png",
    ROOT / "assets" / "images" / "betteryeah-ai-cs-work.png",
    ROOT / "assets" / "images" / "betteryeah-ai-cs-growth.png",
    ROOT / "assets" / "images" / "betteryeah-ai-cs-scale.png",
]


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
    if parts.scheme or value.startswith("#") or value.startswith("mailto:") or value.startswith("tel:"):
        return None
    path = unquote(parts.path)
    target = (page.parent / path).resolve()
    if path.endswith("/"):
        target /= "index.html"
    return target


class BetterYeahPortfolioTest(unittest.TestCase):
    def test_detail_page_contains_pm_story_and_demo_link(self):
        self.assertTrue(DETAIL.is_file())
        page = parse(DETAIL)
        text = " ".join(page.text)
        for phrase in ["AI 产品经理", "三个关键判断", "我做了什么", "待上线"]:
            self.assertIn(phrase, text)
        demo_links = [(href, attrs) for href, attrs in page.links if href == "demo/"]
        self.assertEqual(len(demo_links), 2)
        for _, attrs in demo_links:
            self.assertEqual(attrs.get("target"), "_blank")
            self.assertIn("noopener", attrs.get("rel", ""))

    def test_demo_and_four_screenshots_exist(self):
        self.assertTrue(DEMO.is_file())
        for screenshot in SCREENSHOTS:
            self.assertTrue(screenshot.is_file(), screenshot)
            self.assertGreater(screenshot.stat().st_size, 20_000)

    def test_detail_images_have_alt_text_and_resolve(self):
        page = parse(DETAIL)
        self.assertEqual(len([src for src, _ in page.images if "betteryeah-ai-cs-" in src]), 4)
        for src, attrs in page.images:
            self.assertTrue(attrs.get("alt", "").strip(), src)
            target = resolve_local(DETAIL, src)
            if target:
                self.assertTrue(target.is_file(), target)

    def test_public_pages_link_to_detail(self):
        for page_path in [ROOT / "index.html", ROOT / "projects" / "index.html"]:
            page = parse(page_path)
            targets = [resolve_local(page_path, href) for href, _ in page.links]
            self.assertIn(DETAIL.resolve(), targets)

    def test_changed_pages_have_no_broken_local_links(self):
        for page_path in [DETAIL, ROOT / "index.html", ROOT / "projects" / "index.html"]:
            page = parse(page_path)
            for value, _ in page.links + page.images:
                target = resolve_local(page_path, value)
                if target:
                    self.assertTrue(target.is_file(), f"{page_path}: {value}")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 运行测试并确认失败**

Run: `python3 -m unittest tests/test_betteryeah_portfolio.py -v`

Expected: FAIL，至少包含 `projects/betteryeah-ai-cs/index.html` 和截图不存在的断言错误。

- [ ] **Step 3: 提交测试基线**

```bash
git add tests/test_betteryeah_portfolio.py
git commit -m "test: define BetterYeah portfolio requirements"
```

### Task 2: 复制完整官网并生成截图

**Files:**
- Create: `projects/betteryeah-ai-cs/demo/index.html`
- Create: `projects/betteryeah-ai-cs/demo/assets/**`
- Create: `assets/images/betteryeah-ai-cs-hero.png`
- Create: `assets/images/betteryeah-ai-cs-work.png`
- Create: `assets/images/betteryeah-ai-cs-growth.png`
- Create: `assets/images/betteryeah-ai-cs-scale.png`

**Interfaces:**
- Consumes: `/Users/ljh/Desktop/客服官网设计/tasks/task-20260804-html-demo/result/BetterYeah-AI-Customer-Service-Official/`。
- Produces: 可由 GitHub Pages 直接托管的 `demo/` 目录和详情页引用的四张 PNG。

- [ ] **Step 1: 复制完整 Demo 目录**

Run:

```bash
mkdir -p projects/betteryeah-ai-cs
cp -R "/Users/ljh/Desktop/客服官网设计/tasks/task-20260804-html-demo/result/BetterYeah-AI-Customer-Service-Official" projects/betteryeah-ai-cs/demo
```

Expected: `projects/betteryeah-ai-cs/demo/index.html` 与 `projects/betteryeah-ai-cs/demo/assets/` 存在，原始相对资源结构不变。

- [ ] **Step 2: 用复制后的 Demo 生成长截图**

Run:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --hide-scrollbars --allow-file-access-from-files \
  --window-size=1440,9000 \
  --screenshot=/tmp/betteryeah-ai-cs-full.png \
  "file://$PWD/projects/betteryeah-ai-cs/demo/index.html"
```

Expected: `/tmp/betteryeah-ai-cs-full.png` 为 1440×9000 PNG。

- [ ] **Step 3: 裁出首屏和会干活截图**

Run:

```bash
sips -c 760 1240 --cropOffset 0 100 /tmp/betteryeah-ai-cs-full.png --out assets/images/betteryeah-ai-cs-hero.png
sips -c 720 1240 --cropOffset 800 100 /tmp/betteryeah-ai-cs-full.png --out assets/images/betteryeah-ai-cs-work.png
```

Expected: 两张图宽 1240px，分别展示首屏和“会干活”区块。

- [ ] **Step 4: 复制最终官网中的成长与规模化成品图**

Run:

```bash
cp "projects/betteryeah-ai-cs/demo/assets/story/卖点二/01-客服优化助手.png" assets/images/betteryeah-ai-cs-growth.png
cp "projects/betteryeah-ai-cs/demo/assets/story/卖点三/01-多平台多店铺统一管理.png" assets/images/betteryeah-ai-cs-scale.png
```

Expected: 四张截图均为真实 Demo 内容，不包含占位图。

- [ ] **Step 5: 运行资源测试**

Run: `python3 -m unittest tests.test_betteryeah_portfolio.BetterYeahPortfolioTest.test_demo_and_four_screenshots_exist -v`

Expected: PASS。

- [ ] **Step 6: 提交 Demo 与截图**

```bash
git add projects/betteryeah-ai-cs/demo assets/images/betteryeah-ai-cs-*.png
git commit -m "feat: add BetterYeah customer service demo assets"
```

### Task 3: 创建作品详情页与专用样式

**Files:**
- Create: `projects/betteryeah-ai-cs/index.html`
- Modify: `css/site.css`

**Interfaces:**
- Consumes: Task 2 的四张截图与 `demo/`。
- Produces: `/projects/betteryeah-ai-cs/` 作品详情页，以及 `case-*` 前缀的响应式样式。

- [ ] **Step 1: 创建详情页**

页面复用现有 `site-header`、`page-hero`、`tile detail-prose` 和 `site-footer`。必须包含：

```html
<header class="page-hero case-hero">
  <p class="breadcrumb"><a href="../../">首页</a> / <a href="../">作品</a> / AI 智能客服官网</p>
  <h1>BetterYeah AI 智能客服官网</h1>
  <p>为一款新的 AI 客服产品从零建立对外表达：从产品研究和竞品分析，到价值定位、内容结构与官网 Demo。</p>
  <div class="case-meta" aria-label="项目信息">
    <span>AI 产品经理</span><span>独立完成</span><span>待上线</span>
  </div>
  <div class="detail-links">
    <a class="btn btn-primary" href="demo/" target="_blank" rel="noopener">查看官网作品</a>
    <a class="btn btn-ghost" href="../">全部作品</a>
  </div>
</header>
```

正文依次为“项目背景”“三个关键判断”“把判断变成页面”“我做了什么”。使用四张截图，给每张图写描述性 `alt` 和图注。在“把判断变成页面”后加入深色 `case-outcome`，再次链接 `demo/` 并注明“作品预览，非正式线上站点”。

- [ ] **Step 2: 添加详情页专用 CSS**

在 `css/site.css` 的详情页样式后添加：

```css
.case-meta { display:flex; flex-wrap:wrap; gap:.5rem; margin-top:1rem; }
.case-meta span { padding:.35rem .7rem; border:1px solid var(--line); border-radius:999px; background:rgba(255,255,255,.72); color:var(--ink-soft); font-size:.8rem; }
.case-brief { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.75rem; margin:1.25rem 0 0; }
.case-brief > div { padding:1rem; border-radius:var(--radius-sm); background:var(--bg); }
.case-brief strong { display:block; margin-bottom:.25rem; }
.case-brief span { color:var(--muted); font-size:.9rem; }
.case-thinking { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:.75rem; margin:1rem 0 0; }
.case-thinking article { padding:1rem; border:1px solid var(--line); border-radius:var(--radius-sm); }
.case-thinking .eyebrow { margin-bottom:.35rem; }
.case-thinking h3 { margin:0 0 .4rem; font-size:1rem; }
.case-thinking p { margin:0; color:var(--muted); font-size:.86rem; }
.case-gallery { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.85rem; margin-top:1rem; }
.case-gallery .detail-figure { margin:0; }
.case-gallery .detail-figure:first-child { grid-column:1 / -1; }
.case-outcome { margin-top:2rem; padding:1.25rem; border-radius:var(--radius-sm); background:#171b27; color:#fff; }
.case-outcome p { margin:0 0 .8rem; color:rgba(255,255,255,.76); }
.case-outcome .btn { background:#fff; color:#171b27; }
.case-role-list { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.45rem 1.25rem; }
.case-note { margin-top:1.5rem; padding-top:1rem; border-top:1px solid var(--line); color:var(--muted); font-size:.78rem; }
@media (max-width: 720px) {
  .case-brief,.case-thinking,.case-gallery,.case-role-list { grid-template-columns:1fr; }
  .case-gallery .detail-figure:first-child { grid-column:auto; }
}
```

- [ ] **Step 3: 运行详情页测试**

Run: `python3 -m unittest tests.test_betteryeah_portfolio.BetterYeahPortfolioTest.test_detail_page_contains_pm_story_and_demo_link tests.test_betteryeah_portfolio.BetterYeahPortfolioTest.test_detail_images_have_alt_text_and_resolve -v`

Expected: PASS。

- [ ] **Step 4: 提交详情页**

```bash
git add projects/betteryeah-ai-cs/index.html css/site.css
git commit -m "feat: add BetterYeah AI customer service case study"
```

### Task 4: 接入首页与作品列表

**Files:**
- Modify: `projects/index.html`
- Modify: `index.html`

**Interfaces:**
- Consumes: Task 3 的详情页路径 `projects/betteryeah-ai-cs/`。
- Produces: 首页作品卡和作品列表入口。

- [ ] **Step 1: 更新作品列表元信息与首条入口**

将 `projects/index.html` 的 description 改为包含 `BetterYeah AI 智能客服官网`。在 `work-list` 首部加入：

```html
<li>
  <a class="work-row" href="betteryeah-ai-cs/">
    <div>
      <h3>BetterYeah AI 智能客服官网</h3>
      <p>从产品研究与竞品分析，到 KA 客群定位、三层价值主张和完整官网 Demo。</p>
    </div>
    <span class="work-arrow" aria-hidden="true">→</span>
  </a>
</li>
```

保留当前未提交的 `agent-for-you` 入口，不覆盖或重排其内容。

- [ ] **Step 2: 在首页作品区加入项目卡**

在 `index.html` 的 `works-bento` 首部加入：

```html
<a class="tile work-tile" href="projects/betteryeah-ai-cs/">
  <div class="work-thumb">
    <img src="assets/images/betteryeah-ai-cs-hero.png" alt="BetterYeah AI 智能客服官网首屏" loading="lazy" />
  </div>
  <div class="work-copy">
    <h3>AI 智能客服官网</h3>
    <p>产品定位、三层价值主张与官网 Demo</p>
  </div>
</a>
```

- [ ] **Step 3: 运行入口与链接测试**

Run: `python3 -m unittest tests/test_betteryeah_portfolio.py -v`

Expected: 5 tests PASS。

- [ ] **Step 4: 提交入口改动**

```bash
git add index.html projects/index.html
git commit -m "feat: link BetterYeah case study from portfolio"
```

### Task 5: 浏览器验证与收尾

**Files:**
- Verify: `projects/betteryeah-ai-cs/index.html`
- Verify: `projects/betteryeah-ai-cs/demo/index.html`
- Verify: `index.html`
- Verify: `projects/index.html`

**Interfaces:**
- Consumes: Tasks 1–4 的全部交付物。
- Produces: 本地浏览器验证记录和干净的本项目 diff。

- [ ] **Step 1: 启动本地服务器**

Run: `python3 -m http.server 8765`

Expected: `Serving HTTP on 0.0.0.0 port 8765`。

- [ ] **Step 2: 用 Chrome 截取桌面与移动端详情页**

Run:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --window-size=1440,1100 --screenshot=/tmp/betteryeah-portfolio-desktop.png http://127.0.0.1:8765/projects/betteryeah-ai-cs/
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --window-size=390,844 --screenshot=/tmp/betteryeah-portfolio-mobile.png http://127.0.0.1:8765/projects/betteryeah-ai-cs/
```

Expected: 两张截图生成，页面无横向溢出，标题、截图和按钮可见。

- [ ] **Step 3: 验证完整 Demo 路径**

Run: `curl -I http://127.0.0.1:8765/projects/betteryeah-ai-cs/demo/`

Expected: `HTTP/1.0 200 OK`。

- [ ] **Step 4: 运行完整测试与差异检查**

Run:

```bash
python3 -m unittest tests/test_betteryeah_portfolio.py -v
git diff --check
git status --short
```

Expected: 5 tests PASS；无空白错误；状态只显示用户原有的无关改动和本计划明确生成的文件。
