# 刘佳会 - 个人简历网站

> 🌐 https://G-LJH.github.io

## 网站结构

```
├── index.html          ← 首页（个人简介 + 核心亮点）
├── projects.md         ← 项目总览页
├── blog.md             ← 博客列表页
├── about.md            ← 关于我
├── _data/
│   └── projects.yml    ← 📝 在这里管理项目（增删改）
├── projects/           ← 项目详情页
│   ├── agent-framework.md
│   ├── rag-system.md
│   └── cv-project.md
├── _posts/             ← 博客文章
├── _config.yml         ← 网站配置
└── style.scss          ← 样式
```

## 如何修改内容

### 添加/编辑项目

编辑 `_data/projects.yml`，每个项目的格式：

```yaml
- title: 项目名称
  date: 2025
  description: 简短描述
  technologies:
    - Python
    - LangChain
  featured: true       # 是否在首页展示
  order: 1             # 排序（数字越小越靠前）
  url: /projects/my-project/
  github: https://github.com/...
  demo: https://...
  article: https://...
```

然后在 `projects/` 目录下创建对应的详情页。

### 写博客文章

在 `_posts/` 目录下创建文件，命名格式：`YYYY-MM-DD-标题.md`

```markdown
---
layout: post
title: 文章标题
---

正文内容...
```

### 更新个人信息

- `_config.yml` → 姓名、描述、头像、链接
- `about.md` → 详细介绍

## 部署到 GitHub

```bash
git add .
git commit -m "update site"
git push origin main
```

推送后 GitHub Pages 会自动构建，几分钟后可访问。
