# Homepage Works More Card Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将首页作品区收敛为四个重点项目，并增加横跨整行的浅色“查看更多作品”卡片。

**Architecture:** 保留现有静态 HTML 与作品网格，在 `index.html` 中用 CTA 替换第 5、6 张项目卡片，在 `css/site.css` 中增加独立浅色样式。通过 `HomepageWorksTest` 校验项目数量、链接、文案和响应式样式。

**Tech Stack:** HTML5、CSS3、Python `unittest`

## Global Constraints

- 只保留前四个重点项目卡片。
- CTA 链接必须为 `projects/`。
- CTA 必须使用浅色样式，桌面横跨两列，手机占满单列。
- 不删除任何项目详情页。

---

### Task 1: 更新首页作品结构

**Files:**
- Modify: `tests/test_homepage_works.py`
- Modify: `index.html`

**Interfaces:**
- Consumes: 首页 `#works` 区块
- Produces: 4 张 `work-card` 与 1 张 `works-more-card`

- [ ] **Step 1: 编写失败测试**

断言首页只有 4 张项目卡、不含第 5/6 项，并包含指向 `projects/` 的“查看更多作品”卡片。

- [ ] **Step 2: 运行测试确认失败**

Run: `python3 -m unittest tests/test_homepage_works.py -v`

Expected: FAIL，旧页面仍包含 6 张项目卡且没有 CTA。

- [ ] **Step 3: 用 CTA 替换第 5、6 张卡片**

在 `index.html` 中删除两张首页卡片，增加：

```html
<a class="tile works-more-card" href="projects/">
  <span>查看更多作品</span>
</a>
```

### Task 2: 添加浅色响应式样式

**Files:**
- Modify: `css/site.css`
- Test: `tests/test_homepage_works.py`

**Interfaces:**
- Consumes: `.works-more-card`
- Produces: 桌面双列跨栏、移动单列的 CTA 卡片

- [ ] **Step 1: 添加 CTA 样式断言并确认失败**

断言 CSS 包含 `.works-more-card`、`grid-column: 1 / -1;` 和聚焦样式。

- [ ] **Step 2: 实现浅色 CTA 样式**

```css
.works-more-card {
  grid-column: 1 / -1;
  background: linear-gradient(135deg, #eef4ff, #ffffff);
}
```

- [ ] **Step 3: 运行完整测试**

Run: `python3 -m unittest discover -s tests -v`

Expected: 所有测试 PASS。

