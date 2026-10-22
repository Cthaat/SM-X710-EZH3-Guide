"""Build public HTML from an explicit documentation allowlist (Python 3.10+).

Install tools/site-requirements.txt, then run python tools/build_site.py.
Use --check to detect stale generated pages without changing files.
"""
from __future__ import annotations

import argparse
import html
import json
import posixpath
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
from xml.sax.saxutils import escape

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
REPO = 'https://github.com/Cthaat/SM-X710-EZH3-Guide'
BASE = 'https://cthaat.github.io/SM-X710-EZH3-Guide/'
PAGES = {
    'README.md': ('index.html', '三星 Tab S9 刷机教程：SM-X710 One UI 8.5 EZH3 升级、Root 与救援', '国行三星 Galaxy Tab S9 SM-X710 实机升级记录：混合 BL、One UI 8.5 / Android 16、KernelSU-Next 3.4.2 Root、Odin 刷机文件下载与启动循环救援。仅验证一台已解锁设备。'),
    'README.en.md': ('en.html', 'Samsung Tab S9 SM-X710 Root, One UI 8.5 EZH3 Upgrade & Rescue', 'Single-device verified China SM-X710 / gts9wifi guide: Android 16 firmware upgrade, hybrid bootloader, KernelSU-Next 3.4.2 root and stock boot/init_boot bootloop rescue.'),
    'FILES.md': ('files.html', 'SM-X710 刷机包、Root 包与救援包下载和 SHA-256 校验', '三星 Tab S9 EZH3 Release 文件清单、AP 分片合并、混合 BL、HOME_CSC、Root 与救援包用途及哈希校验。'),
    'NOTICE.md': ('notice.html', '第三方文件与许可说明', 'Samsung 固件、Odin、Linux 与 KernelSU-Next 的来源、许可和分发边界。'),
    'docs/01-preparation.md': ('01-preparation.html', '三星 Tab S9 SM-X710 刷机前的适用条件与备份', '核对 CHN、gts9wifi、固件版本、解锁状态、回滚限制和私人备份边界。'),
    'docs/02-upgrade.md': ('02-upgrade.html', '三星 Tab S9 One UI 8.5 EZH3 混合 BL 升级步骤', 'SM-X710 使用 CYH4 ABL5 与 EZH3 其他 BL 成员的单机升级记录，包含 Odin 槽位与开机验收。'),
    'docs/03-root.md': ('03-root.html', 'SM-X710 Root 教程：KernelSU-Next 3.4.2 boot-only AP', '三星 Tab S9 EZH3 内建 KernelSU-Next Root 的 Odin AP 单槽步骤、管理器区别、ADB 核对与模块限制。'),
    'docs/04-rescue.md': ('04-rescue.html', '三星 Tab S9 Root 无限重启救援：恢复原版 boot 与 init_boot', 'SM-X710 EZH3 启动循环救援记录。要求 Download 模式仍可用，使用原版 boot + init_boot AP，不是所有故障的通用救砖方案。'),
    'docs/05-failures.md': ('05-failures.html', 'SM-X710 刷机与 Root 失败记录及验证边界', '记录 PIN 错误、LZ4 打包与 Root 启动循环经过，区分假设、失败试验与实机结果。'),
    'docs/06-backups.md': ('06-backups.html', 'SM-X710 私人分区备份与公开文件边界', '备份原则和恢复限制；本网站不公开个人 EFS、加密元数据或原始设备日志。'),
    'docs/07-source.md': ('07-source.html', 'SM-X710 KernelSU-Next 内核对应源码与构建记录', '自编译 EZH3 内核对应源码、工具链、配置及出处；尚未验证全新环境的字节级重现。'),
    'docs/08-publishing.md': ('08-publishing.html', '教程仓库、Release 附件与 GitHub Pages 发布方法', '公开教程的提交检查、大文件分片上传、附件校验与静态网页更新方法。'),
}
CSS = '''*{box-sizing:border-box}body{margin:0;color:#172b40;background:#f6f8fa;font:17px/1.8 system-ui,-apple-system,"Segoe UI",sans-serif}header,main,footer{max-width:1020px;margin:auto;padding:24px}header{border-bottom:1px solid #d0d7de}header a{display:inline-block;margin:0 18px 6px 0}a{color:#0969da;text-underline-offset:3px}main{background:white;margin:24px auto;border:1px solid #d0d7de;border-radius:8px;padding:36px}h1{font-size:2rem;line-height:1.35}h2{margin-top:2em}h1,h2,h3{scroll-margin-top:20px}pre{padding:18px;background:#f0f3f6;border-radius:6px;overflow:auto;line-height:1.5}code{font-size:.9em;overflow-wrap:anywhere}pre code{overflow-wrap:normal}table{display:block;overflow:auto;border-collapse:collapse;max-width:100%}th,td{border:1px solid #d0d7de;padding:8px 12px;text-align:left}th{background:#f6f8fa}blockquote{margin-left:0;border-left:4px solid #0969da;padding-left:18px;color:#475569}img{max-width:100%;height:auto}footer{font-size:.88rem;color:#475569}nav{font-size:.95rem}@media(max-width:700px){body{font-size:16px}main{margin:0;border:0;border-radius:0;padding:20px}header,footer{padding:18px}h1{font-size:1.65rem}}
'''


def rewrite_link(href: str, source: str) -> str:
    url = urlsplit(href)
    if url.scheme or url.netloc or not url.path or url.path.startswith('/'):
        return href
    resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source), url.path))
    if resolved in PAGES:
        return urlunsplit(('', '', PAGES[resolved][0], url.query, url.fragment))
    return urlunsplit(('https', 'github.com', '/Cthaat/SM-X710-EZH3-Guide/blob/main/' + resolved, url.query, url.fragment))


def render_markdown(source: str) -> str:
    md = MarkdownIt('commonmark', {'html': False}).enable('table').enable('strikethrough')
    tokens = md.parse((ROOT / source).read_text(encoding='utf-8'))
    ids: dict[str, int] = {}
    for i, token in enumerate(tokens):
        if token.type == 'heading_open':
            label = tokens[i + 1].content.lower()
            slug = re.sub(r'[^\w\s-]', '', label).strip().replace(' ', '-')
            count = ids.get(slug, 0)
            ids[slug] = count + 1
            token.attrSet('id', slug if not count else f'{slug}-{count}')
        for child in token.children or []:
            if child.type == 'link_open':
                child.attrSet('href', rewrite_link(child.attrGet('href') or '', source))
    return md.renderer.render(tokens, md.options, {})


def outputs() -> dict[str, str]:
    files = {'.nojekyll': '', 'site.css': CSS}
    for source, (name, title, description) in PAGES.items():
        lang = 'en' if source == 'README.en.md' else 'zh-CN'
        canonical = BASE if name == 'index.html' else BASE + name
        alternate = ''
        if source in ('README.md', 'README.en.md'):
            alternate = f'<link rel="alternate" hreflang="zh-CN" href="{BASE}"><link rel="alternate" hreflang="en" href="{BASE}en.html"><link rel="alternate" hreflang="x-default" href="{BASE}">'
        data = json.dumps({'@context': 'https://schema.org', '@type': 'TechArticle', 'headline': title, 'description': description, 'url': canonical, 'inLanguage': lang, 'author': {'@type': 'Person', 'name': 'Cthaat', 'url': 'https://github.com/Cthaat'}}, ensure_ascii=False).replace('<', '\\u003c')
        files[name] = f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(description, quote=True)}">
<meta name="robots" content="index,follow"><link rel="canonical" href="{canonical}">{alternate}
<meta property="og:type" content="article"><meta property="og:title" content="{html.escape(title, quote=True)}"><meta property="og:description" content="{html.escape(description, quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:site_name" content="SM-X710 EZH3 Guide"><meta name="twitter:card" content="summary">
<link rel="stylesheet" href="site.css"><script type="application/ld+json">{data}</script></head>
<body><header><nav aria-label="Main navigation"><a href="./">三星 Tab S9 刷机教程</a><a href="en.html">English</a><a href="files.html">下载与校验</a><a href="03-root.html">SM-X710 Root</a><a href="04-rescue.html">启动循环救援</a><a href="{REPO}">GitHub</a><a href="{REPO}/releases/latest">Release 附件</a></nav></header>
<main>{render_markdown(source)}</main>
<footer>单台已解锁 SM-X710 / CHN 的实机记录，不代表其他设备兼容。Hardware verified: 2026-10-16. <a href="{REPO}/blob/main/{source}">查看原文 / Source</a> · <a href="notice.html">文件许可</a> · <a href="sitemap.xml">Sitemap</a></footer></body></html>
'''
    urls = [BASE if v[0] == 'index.html' else BASE + v[0] for v in PAGES.values()]
    files['sitemap.xml'] = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{escape(url)}</loc></url>\n' for url in urls) + '</urlset>\n'
    return files


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    generated = outputs()
    stale = []
    for name, content in generated.items():
        path = ROOT / 'docs' / name
        if args.check:
            if not path.exists() or path.read_bytes() != content.encode('utf-8'):
                stale.append(name)
        else:
            path.write_bytes(content.encode('utf-8'))
    if stale:
        raise SystemExit('Stale generated files: ' + ', '.join(stale))
    print(f'{"Verified" if args.check else "Built"} {len(PAGES)} public pages and sitemap; explicit public-source allowlist only.')


if __name__ == '__main__':
    main()
