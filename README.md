# 刘佳慧 · 个人站点

纯静态站（HTML / CSS / JS），部署于 GitHub Pages：https://G-LJH.github.io

## 本地预览

```bash
python3 -m http.server 8765
```

打开 http://127.0.0.1:8765/

## 导出作品 PDF

依赖本机 Google Chrome；总册合并需要 `pip install pypdf`。

```bash
python3 scripts/export_works_pdf.py
```

输出到 `assets/pdf/works/`（7 份单册 + `作品集总册.pdf`）。

## 结构

| 路径 | 说明 |
|------|------|
| `index.html` | 首页 |
| `projects/` | 作品列表与详情 |
| `css/` `js/` | 样式与交互 |
| `assets/images/` | 截图、氛围图、微信码 |
| `assets/pdf/` | 简历 |
| `assets/pdf/works/` | 作品 PDF（单册 + 总册；由 `scripts/export_works_pdf.py` 生成） |
| `content/` | 文案与事实素材（非线上页面） |
| `discussion/` | 设计讨论记录 |

## 联系

- 邮箱：18045034451@189.cn
- GitHub：[G-LJH](https://github.com/G-LJH)
- CSDN：[qw1233w](https://blog.csdn.net/qw1233w)
