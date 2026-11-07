#!/usr/bin/env python3
"""把 index.html 里的三个外部 JS 内联，生成可单独拷走的 hanzi-big.html。"""

HTML = "index.html"
SOURCES = ["hanzi-data.js", "hanzi-writer.min.js", "pinyin-pro.min.js"]
OUT = "hanzi-big.html"

html = open(HTML, encoding="utf-8").read()

for name in SOURCES:
    content = open(name, encoding="utf-8").read()
    content = content.replace("//# sourceMappingURL=hanzi-writer.min.js.map", "")
    tag = '<script src="%s"></script>' % name
    if tag not in html:
        raise SystemExit("找不到 %s" % tag)
    html = html.replace(tag, "<script>" + content + "</script>")

open(OUT, "w", encoding="utf-8").write(html)
print("%s 已生成：%.1f MB" % (OUT, len(html.encode("utf-8")) / 1048576))
