---
layout: default
title: 项目经历
permalink: /projects/
---

<div class="page-header">
  <h1>🛠️ 我的项目</h1>
  <p class="page-desc">以下是我参与过的项目，涵盖 AI Agent、RAG、计算机视觉等方向。<br>点击卡片查看详情。</p>
</div>

<div class="projects-grid projects-full">
  {% for project in site.data.projects %}
  <a href="{{ site.baseurl }}{{ project.url }}" class="project-card">
    <div class="card-header">
      <h3>{{ project.title }}</h3>
      <span class="card-date">{{ project.date }}</span>
    </div>
    <p class="card-desc">{{ project.description }}</p>
    <div class="card-tags">
      {% for tech in project.technologies %}
      <span class="tag tag-tech">{{ tech }}</span>
      {% endfor %}
    </div>
    <div class="card-links">
      {% if project.github %}
      <span class="card-link">📂 GitHub</span>
      {% endif %}
      {% if project.demo %}
      <span class="card-link">🔗 Demo</span>
      {% endif %}
      {% if project.article %}
      <span class="card-link">📝 文章</span>
      {% endif %}
    </div>
  </a>
  {% endfor %}
</div>

<div class="projects-tip">
  <p>💡 提示：项目信息存储在 <code>_data/projects.yml</code> 中，修改后会自动更新。</p>
</div>
