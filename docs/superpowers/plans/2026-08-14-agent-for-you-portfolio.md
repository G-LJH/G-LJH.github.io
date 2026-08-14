# agent-for-you Portfolio Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 agent-for-you 详情页改造成简洁、可信、能体现 AI 产品经理产品判断的作品案例，并用清晰的小尺寸截图介绍核心功能。

**Architecture:** 保留现有静态 HTML 架构，在详情页中新增 agent-for-you 专属案例区块，并复用既有按钮、卡片和响应式基础样式。新增独立验收测试读取真实 HTML 与 PNG 文件，校验叙事、链接、图片分辨率和本地资源完整性。

**Tech Stack:** HTML5、CSS3、Python `unittest`、静态 PNG 资源

## Global Constraints

- 主命题必须体现“工作不发生在聊天框，而发生在项目和时间里”。
- 必须如实说明通过 Vibe Coding 落地，底层 Agent 基于 pi 集成。
- 必须介绍项目工作台、工作区与长期记忆、AI 会议、定时任务。
- 桌面端功能截图使用两列小卡片，移动端单列且无横向溢出。
- 不改动 agent-for-you 产品源码，只修改个人作品站。

---

### Task 1: 页面叙事与资源验收测试

**Files:**
- Create: `tests/test_agent_for_you_portfolio.py`

**Interfaces:**
- Consumes: `projects/agent-for-you/index.html`、`projects/index.html` 和 `assets/images/agent-for-you-*.png`
- Produces: `AgentForYouPortfolioTest`，作为页面内容与资源的回归验收入口

- [ ] **Step 1: 写入失败的页面验收测试**

```python
class AgentForYouPortfolioTest(unittest.TestCase):
    def test_page_tells_ai_pm_story(self):
        text = " ".join(parse(DETAIL).text)
        for phrase in ["AI 产品经理", "工作不发生在聊天框", "Vibe Coding", "基于 pi"]:
            self.assertIn(phrase, text)

    def test_page_introduces_four_core_capabilities(self):
        text = " ".join(parse(DETAIL).text)
        for phrase in ["项目工作台", "工作区与长期记忆", "AI 会议", "定时任务"]:
            self.assertIn(phrase, text)
```

- [ ] **Step 2: 运行测试并确认因新叙事缺失而失败**

Run: `python3 -m unittest tests/test_agent_for_you_portfolio.py -v`

Expected: FAIL，缺少“AI 产品经理”或“工作不发生在聊天框”等新文案。

- [ ] **Step 3: 保留失败证据并进入页面实现**

测试输出应明确指向缺失的页面文本，而不是 Python 语法或路径错误。

### Task 2: 高清资源与详情页实现

**Files:**
- Modify: `projects/agent-for-you/index.html`
- Create: `assets/images/agent-for-you-project-files.png`
- Modify: `assets/images/agent-for-you-workspaces.png`
- Create: `assets/images/agent-for-you-meeting-workspace.png`
- Modify: `assets/images/agent-for-you-automations.png`

**Interfaces:**
- Consumes: `/Users/ljh/Documents/agent-for-you/docs/readme-screenshots/*.png` 和 `docs/prototypes/meeting-recording-workspace-v1.png`
- Produces: 四张作品页功能截图，以及包含 `agent-feature-grid`、`agent-decision-grid`、`agent-contribution` 的详情页结构

- [ ] **Step 1: 复制四张高清原始截图到作品站资源目录**

```bash
cp /Users/ljh/Documents/agent-for-you/docs/readme-screenshots/07-project-files.png assets/images/agent-for-you-project-files.png
cp /Users/ljh/Documents/agent-for-you/docs/readme-screenshots/04-workspaces.png assets/images/agent-for-you-workspaces.png
cp /Users/ljh/Documents/agent-for-you/docs/prototypes/meeting-recording-workspace-v1.png assets/images/agent-for-you-meeting-workspace.png
cp /Users/ljh/Documents/agent-for-you/docs/readme-screenshots/02-automations.png assets/images/agent-for-you-automations.png
```

- [ ] **Step 2: 重写详情页首屏、问题、功能、决策和贡献内容**

页面必须包含以下标题与职责说明：

```html
<h1>把一次性 AI 对话，变成持续工作的个人 Agent</h1>
<h2>工作不发生在聊天框，而发生在项目和时间里</h2>
<h2>核心功能</h2>
<h2>三个关键产品决策</h2>
<h2>我如何把想法做成可运行 Demo</h2>
```

四张图片外层链接必须使用 `target="_blank" rel="noopener"`，图片必须提供具体 `alt` 文本。

- [ ] **Step 3: 运行页面测试并确认叙事与资源测试通过**

Run: `python3 -m unittest tests/test_agent_for_you_portfolio.py -v`

Expected: 页面叙事、核心功能、图片尺寸和本地链接相关测试全部 PASS。

### Task 3: 响应式样式与列表摘要

**Files:**
- Modify: `css/site.css`
- Modify: `projects/index.html`
- Test: `tests/test_agent_for_you_portfolio.py`

**Interfaces:**
- Consumes: 详情页中的 `agent-story`、`agent-feature-grid`、`agent-feature-card`、`agent-decision-grid` 类名
- Produces: 桌面端两列功能展示、移动端单列展示，以及与详情页一致的作品列表摘要

- [ ] **Step 1: 在测试中加入结构与作品摘要断言并确认失败**

```python
self.assertIn('class="agent-feature-grid"', html)
self.assertEqual(html.count('class="agent-feature-card"'), 4)
self.assertIn("持续工作的本地个人 Agent", list_text)
```

Run: `python3 -m unittest tests/test_agent_for_you_portfolio.py -v`

Expected: FAIL，原因是新类名样式或列表摘要尚未实现。

- [ ] **Step 2: 添加 agent-for-you 专属布局样式并更新作品列表摘要**

```css
.agent-feature-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

@media (max-width: 640px) {
  .agent-feature-grid,
  .agent-decision-grid {
    grid-template-columns: 1fr;
  }
}
```

- [ ] **Step 3: 运行完整静态站测试**

Run: `python3 -m unittest discover -s tests -v`

Expected: 所有测试 PASS，无 broken local link。

### Task 4: 浏览器视觉验收

**Files:**
- Verify: `projects/agent-for-you/index.html`
- Verify: `css/site.css`

**Interfaces:**
- Consumes: 本地静态站页面
- Produces: 桌面端与手机端视觉验收证据

- [ ] **Step 1: 启动本地静态服务器**

Run: `python3 -m http.server 4173`

Expected: 服务在 `http://127.0.0.1:4173/` 可访问。

- [ ] **Step 2: 检查桌面端页面**

打开 `http://127.0.0.1:4173/projects/agent-for-you/`，确认首屏主次清晰、四张截图为两列小卡片、文字无需依赖图片也能理解。

- [ ] **Step 3: 检查手机端页面**

使用约 390px 宽视口确认卡片为单列、按钮可点击、页面无横向滚动。

- [ ] **Step 4: 最终复跑测试**

Run: `python3 -m unittest discover -s tests -v`

Expected: 所有测试 PASS。

