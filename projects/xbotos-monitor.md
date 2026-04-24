---
layout: page
title: xbotos 机器人监控系统
permalink: /projects/xbotos-monitor/
---

# 🤖 xbotos 机器人监控系统

> **基于 Streamlit 的机器人在线状态监控平台**，支持阿里云短信告警，提供实时状态监控、历史数据追踪和智能告警功能。

<div style="display: flex; gap: 10px; flex-wrap: wrap; margin: 20px 0;">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/Frontend-Streamlit-orange.svg" alt="Streamlit">
  <img src="https://img.shields.io/badge/Cloud-Aliyun_SMS-green.svg" alt="Aliyun SMS">
  <img src="https://img.shields.io/badge/Deploy-Docker-purple.svg" alt="Docker">
</div>

---

## 🏗️ 项目简介

xbotos 机器人监控系统是一个轻量级的在线状态监控平台，针对 xbotos 平台的机器人服务提供实时健康监测。当机器人出现连续异常时，自动通过阿里云短信发送告警通知，帮助运维人员第一时间发现问题。

---

## ✨ 核心功能

### 📡 实时监控

<img src="/assets/images/xbotos-overview.png" alt="总览面板" width="100%">

*实时总览面板 — 一目了然所有机器人状态*

- 定时检测机器人在线状态，自动刷新数据
- 可视化展示当前所有机器人的运行状态
- 支持一键启停监控服务

### 🔔 连续失败告警

- **防误报机制**：连续 N 次失败后才发送短信，避免单次抖动误报
- **告警冷却**：设置冷却时间，防止短信轰炸
- **阿里云短信**：通过阿里云 SMS 服务推送告警，稳定可靠

### 📊 历史追踪

- **机器人管理**：统一管理平台下的所有机器人配置

<img src="/assets/images/xbotos-robot-management.png" alt="机器人管理" width="100%">

*机器人管理面板 — 集中配置与维护*

- **检测历史**：完整记录每次检测的时间与结果

<img src="/assets/images/xbotos-history.png" alt="检测历史" width="100%">

*检测历史面板 — 完整的时间线追踪*

### 🐳 Docker 一键部署

支持 Docker / Docker Compose 部署，兼容 1Panel 容器管理平台，秒级上线。

---

## 🔧 技术栈

- **前端框架**：Streamlit
- **数据处理**：Pandas
- **HTTP 请求**：Requests
- **短信服务**：阿里云短信 SDK
- **部署**：Docker / Docker Compose
- **数据存储**：本地 JSON 持久化

---

## 🛠️ 我的工程实践

**系统架构设计**
- 关键动作：设计模块化架构（配置/数据/监控/告警四层分离）
- 交付成果：清晰的代码结构，易于维护和扩展

**告警策略优化**
- 关键动作：引入连续失败阈值 + 告警冷却机制
- 交付成果：有效降低误报率，避免短信骚扰

**容器化部署**
- 关键动作：编写 Dockerfile 和 docker-compose.yml
- 交付成果：支持一键部署到 1Panel / Docker 环境

---

## 📦 快速开始

### 本地运行

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Docker 部署

```bash
docker compose up -d
```

### 1Panel 部署

1. 上传项目到服务器
2. 在 1Panel 中创建 Docker Compose 项目
3. 配置环境变量（短信 AccessKey 等）
4. 启动容器，访问 `http://服务器IP:8501`

---

## 🔗 项目链接

- **GitHub 仓库**：[https://github.com/G-LJH/xbotos-monitor](https://github.com/G-LJH/xbotos-monitor)
- **详细文档**：查看仓库中的 README.md

---
