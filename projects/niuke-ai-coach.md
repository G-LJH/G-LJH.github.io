---
layout: page
title: 牛客AI面试教练
permalink: /projects/niuke-ai-coach/
---

# 🎯 牛客AI面试教练

> 用 AI 对抗 AI，用技术反哺成长。

---

## 📖 项目简介

基于阿里百炼大模型的 AI 面试教练系统，能够自动抓取牛客网面经数据、深度解析简历内容，并生成个性化的面试准备报告。

---

## 📸 效果图

![Web界面效果图](/images/niuke-ai-coach-web-ui.png)
![报告截图](/images/niuke-ai-coach-report.png)

---

## ✨ 核心亮点

**智能爬虫**
自动从牛客网抓取目标岗位面经，内置反爬机制与请求限速。

**简历解析**
支持 PDF 简历结构化提取，为后续分析提供数据基础。

**JD 识别**
支持文字输入与截图 OCR 识别，自动提取岗位要求与技术栈。

**报告生成**
基于岗位+简历+面经，通过大模型生成8大模块面试报告（整体评价、岗位分析、高频考点、项目深挖、行为面试等）。

**断点续传**
长流程任务自动保存进度，支持异常恢复。

**Web 界面**
Flask 构建，支持实时进度展示与 Markdown 报告导出。

---

## 🛠️ 技术栈

| 类别 | 技术 |
|------|------|
| 编程语言 | Python 3.8+ |
| AI 模型 | 阿里百炼 DashScope API |
| Web 框架 | Flask |
| 爬虫 | Requests + BeautifulSoup |
| 其他 | PDF 解析、OCR 识别、状态管理 |

---

## 📁 项目结构

```
niuke-ai-coach/
├── main.py                 # 命令行入口
├── app.py                  # Web 服务入口
├── src/                    # 核心业务代码
│   ├── workflow.py         # 主工作流编排
│   ├── state_manager.py    # 状态管理与断点续传
│   └── tools/              # 爬虫、LLM、简历解析、JD识别
├── templates/              # Web 模板
└── static/                 # 静态资源
```

---

## 💡 写在最后

做这个项目的初衷很简单——自己找工作时觉得准备工作太繁琐，想搞个工具帮自己省点事。开源出来，希望能帮到更多人。

> 💡 **用 AI 对抗 AI，用技术反哺成长**
