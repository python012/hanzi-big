#!/usr/bin/env python3
"""把 index.html 里的三个外部 JS 内联，生成可单独拷走的 hanzi-big.html。

同时把页脚里的版本占位符替换成实际版本号，来源优先级从高到低：

1. 命令行参数：`python3 build.py v1.0.1`
2. 环境变量 BUILD_VERSION（发布工作流会传入 tag 名）
3. 当前提交正好打了 tag 时用该 tag
4. 都不是则写「开发版」（本地开发构建）
"""
import os
import subprocess
import sys
from html import escape

HTML = "index.html"
SOURCES = ["hanzi-data.js", "hanzi-writer.min.js", "pinyin-pro.min.js"]
OUT = "hanzi-big.html"
PLACEHOLDER = '<span id="build-version">开发版</span>'


def detect_version():
    if len(sys.argv) > 1 and sys.argv[1].strip():
        return sys.argv[1].strip()

    env = os.environ.get("BUILD_VERSION", "").strip()
    if env:
        return env

    try:
        r = subprocess.run(["git", "describe", "--tags", "--exact-match"],
                           capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except OSError:
        pass

    return "开发版"


version = detect_version()

html = open(HTML, encoding="utf-8").read()

for name in SOURCES:
    content = open(name, encoding="utf-8").read()
    content = content.replace("//# sourceMappingURL=hanzi-writer.min.js.map", "")
    tag = '<script src="%s"></script>' % name
    if tag not in html:
        raise SystemExit("找不到 %s" % tag)
    html = html.replace(tag, "<script>" + content + "</script>")

if PLACEHOLDER not in html:
    raise SystemExit("找不到版本占位符：%s" % PLACEHOLDER)
html = html.replace(
    PLACEHOLDER,
    '<span id="build-version">%s</span>' % escape(version),
)

open(OUT, "w", encoding="utf-8").write(html)
print("%s 已生成：%.1f MB（版本 %s）" % (OUT, len(html.encode("utf-8")) / 1048576, version))
