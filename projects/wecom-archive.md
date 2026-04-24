---
layout: page
title: 企业微信会话存档系统
permalink: /projects/wecom-archive/
---

# 💰 企业微信低成本会话存档系统 (WeCom Archive)

<img src="https://img.shields.io/badge/Python-3.8+-blue" alt="Python 3.8+">
<img src="https://img.shields.io/badge/Framework-Flask-lightgrey" alt="Flask">
<img src="https://img.shields.io/badge/Database-MySQL-blue" alt="MySQL">
<img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License">

> **一句话定义**：通过xbotox的回调机制，实现企业微信消息的自动化异步存储，将企业合规成本从官方的 **9万/人/年** 降至趋近于 **0**。

---

## 📌 项目背景与痛点

在企业运营中，监控与存档会话内容是合规与质检的核心环节。然而：

- **官方成本极高**：官方接口服务费昂贵，中小型企业难以负担。
- **开发门槛高**：直接对接企业微信底层 SDK 逻辑复杂，且涉及复杂的解密流程。
- **数据孤岛**：难以将聊天数据灵活地集成到公司内部的 CRM 或 AI 知识库中。

**本项目通过集成 xbotox 平台，打通了从"消息捕获"到"结构化存储"的全链路，实现了一套高可用、零门槛的替代方案。**

---

## 🚀 工程亮点（为什么这个项目值得关注）

- **极简部署**：采用 **uv** 现代包管理工具，实现秒级环境搭建。
- **高可靠性**：内置详尽的日志监控系统（Logging），通过 `/health` 接口实现服务自检。
- **前沿思维**：项目预留了 RAG（检索增强生成）接口，存档的数据可直接作为企业私域大模型的训练语料。

---

## �️ 成功部署到 1Panel 运行

本项目已成功部署到 1Panel 容器管理面板上运行，以下是部署详情：

<img src="/images/wecom-chat-1panel.png" alt="1panel部署" width="60%">

*1panel部署*

### 部署环境

| 项目 | 配置 |
|------|------|
| 服务器 | 2核4G |
| 操作系统 | Ubuntu 22.04 LTS |
| 容器平台 | 1Panel |
| 反向代理 | OpenResty (1Panel 内置) |
| 数据库 | MySQL 8.0 (Docker) |

---

## ��🔗 资源与文档

- **GitHub 源码**：[https://github.com/G-LJH/wecom-archive](https://github.com/G-LJH/wecom-archive)
- **详细设计文档**：查看仓库中的 README.md
- **致谢**：[xbotox 平台技术支持](https://xbotox.com)

---