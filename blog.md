---
layout: default
title: 博客
permalink: /blog/
---

<div class="page-header">
  <h1>📝 博客</h1>
  <p class="page-desc">技术笔记、学习心得与项目记录。<br>更多文章请见我的 <a href="https://blog.csdn.net/qw1233w" target="_blank">CSDN 主页</a>。</p>
</div>

<div class="posts">
  {% for post in site.posts %}
  <article class="post">
    <h1><a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a></h1>
    <div class="entry">
      {{ post.excerpt }}
    </div>
    <a href="{{ site.baseurl }}{{ post.url }}" class="read-more">阅读更多 →</a>
  </article>
  {% endfor %}
</div>

{% if site.posts.size == 0 %}
<p style="text-align: center; color: #999; padding: 40px 0;">
  博客内容准备中... 可以先看看我的 <a href="https://blog.csdn.net/qw1233w" target="_blank">CSDN 文章</a> ✍️
</p>
{% endif %}
