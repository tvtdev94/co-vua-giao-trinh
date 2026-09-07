#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sinh muc luc `buoi/README.md` va trang web tinh trong `site/` cho GitHub Pages.

Doc 30 file `buoi/buoi-NN-*.md` lam nguon. Moi buoi thanh mot trang HTML doc
duoc tren dien thoai, cong them trang chu liet ke ca 30 buoi.

    python make-site.py

Script tu kiem truoc khi ghi: du 30 buoi, khong buoi nao trung so, moi link
tro toi file co that.
"""

import glob
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BUOI = os.path.join(HERE, "buoi")
SITE = os.path.join(HERE, "site")

PHASE = {
    1: (1, 6, "Bàn cờ + Xe + Tượng"), 2: (7, 11, "Hậu, Vua, Chiếu"),
    3: (12, 16, "Mã → CỬA 1"), 4: (17, 21, "Tốt → CỬA 2"),
    5: (22, 26, "Chiếu hết, hòa, nhập thành"), 6: (27, 30, "Ván đầy đủ → VÁN MỐC"),
}

PFILE = {
    1: "phase-01-ban-co-xe-tuong", 2: "phase-02-hau-vua-chieu",
    3: "phase-03-ma-cua-1", 4: "phase-04-tot-cua-2",
    5: "phase-05-chieu-het-hoa-nhap-thanh", 6: "phase-06-van-day-du-van-moc",
}


def load():
    """Doc 30 file buoi, tra ve list dict da sap xep theo so buoi."""
    days = []
    for path in sorted(glob.glob(os.path.join(BUOI, "buoi-*.md"))):
        raw = io.open(path, encoding="utf-8").read()
        fm = re.match(r"---\n(.*?)\n---\n", raw, re.S)
        if not fm:
            sys.exit("Thieu frontmatter: " + path)
        meta = dict(
            re.findall(r"^([a-z_]+):\s*(.+)$", fm.group(1), re.M)
        )
        days.append({
            "n": int(meta["buoi"]),
            "title": meta["title"].strip('"'),
            "phase": int(meta["phase"]),
            "full": meta["chi_tiet"] == "day-du",
            "file": os.path.basename(path),
            "body": raw[fm.end():],
        })
    days.sort(key=lambda d: d["n"])
    nums = [d["n"] for d in days]
    if nums != list(range(1, 31)):
        sys.exit("Can dung 30 buoi lien tuc 1..30, dang co: %s" % nums)
    return days


# ------------------------------------------------------------------ muc luc
def readme(days):
    out = [
        "# Giáo trình 30 buổi — mỗi buổi một file\n",
        "Bé 5 tuổi, bắt đầu từ số 0. Phụ huynh làm HLV, **không cần biết chơi cờ trước**.\n",
        "> **Đọc buổi nào thì mở đúng file buổi đó.** Mỗi buổi ≤15 phút, "
        "có sẵn lời thoại — không phải tự nghĩ lúc đang dạy.\n",
        "| Buổi | Nội dung | Chi tiết |",
        "|---|---|---|",
    ]
    cur = None
    for d in days:
        if d["phase"] != cur:
            cur = d["phase"]
            a, b, name = PHASE[cur]
            out.append(
                "| | **PHASE %d — %s** *(buổi %d–%d)* | |" % (cur, name, a, b)
            )
        mark = "đầy đủ" if d["full"] else "khung"
        out.append("| %d | [%s](./%s) | %s |"
                   % (d["n"], d["title"].split("—", 1)[1].strip(),
                      d["file"], mark))
    out += [
        "",
        "## Đọc gì trước khi bắt đầu",
        "",
        "1. [`../plan.md`](../plan.md) — tổng quan, mục tiêu, rủi ro đã chấp nhận",
        "2. [`../phase-01-ban-co-xe-tuong.md`](../phase-01-ban-co-xe-tuong.md) "
        "— **Cổng chuẩn bị**: việc phải làm TRƯỚC buổi 1 (thẻ A5, bảng 30 ô, "
        "người lớn học lại 2 tối)",
        "3. [`../print-buoi-1-6.html`](../print-buoi-1-6.html) — bản in, "
        "1 buổi/trang, chạy được không cần màn hình",
        "",
        "## Ba luật xuyên suốt mọi buổi",
        "",
        "- **Trần 15 phút.** Hết 15 phút mà bé vẫn muốn chơi → **vẫn dừng**.",
        "- **Quy tắc 3 tín hiệu.** 2 tín hiệu chán → dừng ngay, không tiếc.",
        "- **Không dùng chữ \"sai\".** Chỉ sửa nước vừa đi, im lặng khi bé đang nghĩ.",
        "",
        "## Vì sao buổi 7–30 mới có khung",
        "",
        "Cố ý. Chủ đề, trò chơi và tiêu chí \"xong\" của cả 30 buổi **đã chốt**. "
        "Phần lời thoại và sơ đồ bày bàn chỉ soạn sau khi chạy xong 6 buổi đầu — "
        "vì lúc đó mới biết bé ngồi được bao nhiêu phút thật. Soạn trước 30 kịch "
        "bản là soạn theo tưởng tượng, và sẽ phải viết lại.",
        "",
    ]
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------- web
CSS = """
:root { --ink:#1a1a1a; --mut:#666; --line:#e2e2e2; --accent:#b8232c; --bg:#fdfdfc; }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--ink);
  font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  -webkit-text-size-adjust:100%; }
.wrap { max-width:44rem; margin:0 auto; padding:1.5rem 1.1rem 4rem; }
h1 { font:600 1.6rem/1.25 Georgia,serif; margin:.2rem 0 .6rem; }
h2 { font:600 1.15rem/1.3 Georgia,serif; margin:2rem 0 .6rem;
  padding-top:1rem; border-top:1px solid var(--line); }
h3,h4 { font-size:.82rem; letter-spacing:.09em; text-transform:uppercase;
  color:var(--accent); margin:1.6rem 0 .5rem; font-weight:700; }
p,li { margin:.5rem 0; }
a { color:#0b5ea8; }
code { background:#f1f1ef; padding:.1em .35em; border-radius:3px; font-size:.9em; }
pre { background:#f7f7f5; border:1px solid var(--line); border-radius:6px;
  padding:.85rem; overflow-x:auto; font:13px/1.5 ui-monospace,Consolas,monospace; }
pre code { background:none; padding:0; font-size:inherit; }
blockquote { margin:.8rem 0; padding:.6rem .9rem; border-left:3px solid var(--accent);
  background:#fbf6f6; border-radius:0 5px 5px 0; }
blockquote p:first-child { margin-top:0; } blockquote p:last-child { margin-bottom:0; }
table { border-collapse:collapse; width:100%; margin:.9rem 0; font-size:.92rem;
  display:block; overflow-x:auto; }
th,td { border:1px solid var(--line); padding:.45rem .6rem; text-align:left;
  vertical-align:top; }
th { background:#f4f4f2; font-weight:600; }
.meta { color:var(--mut); font-size:.88rem; margin:0 0 1.2rem; }
.nav { display:flex; gap:.5rem; flex-wrap:wrap; margin:1.4rem 0; }
.nav a, .nav span { flex:1; min-width:8rem; text-align:center; padding:.65rem .5rem;
  border:1px solid var(--line); border-radius:7px; background:#fff;
  text-decoration:none; font-size:.9rem; }
.nav span { color:#bbb; }
.grid { display:grid; gap:.55rem; margin:.8rem 0 0; }
.card { display:flex; gap:.8rem; align-items:baseline; padding:.7rem .9rem;
  border:1px solid var(--line); border-radius:8px; background:#fff;
  text-decoration:none; color:inherit; }
.card:hover { border-color:var(--accent); }
.card b { color:var(--accent); font:600 .82rem/1 ui-monospace,monospace;
  min-width:3.4rem; }
.card span { flex:1; }
.tag { font-size:.7rem; letter-spacing:.06em; text-transform:uppercase;
  color:var(--mut); border:1px solid var(--line); border-radius:99px;
  padding:.15rem .5rem; white-space:nowrap; }
.tag.on { color:#137333; border-color:#b7dfc0; background:#f1f9f3; }
.ph { margin:1.7rem 0 .5rem; font:600 .78rem/1 ui-monospace,monospace;
  letter-spacing:.1em; text-transform:uppercase; color:var(--mut); }
.lead { font-size:1.02rem; color:#333; }
.note { background:#fffbe9; border:1px solid #f0e2b0; border-radius:7px;
  padding:.8rem 1rem; font-size:.93rem; margin:1.2rem 0; }
details { margin:2rem 0 0; border-top:1px solid var(--line); padding-top:1rem; }
details summary { cursor:pointer; font-size:.9rem; color:var(--mut);
  padding:.5rem 0; list-style-position:outside; }
details summary:hover { color:var(--accent); }
details[open] summary { margin-bottom:.5rem; font-weight:600; }
@media (max-width:34rem){ .wrap{padding:1.1rem .85rem 3rem;} h1{font-size:1.35rem;} }
"""


def md2html(md):
    """Markdown -> HTML, du dung cho tap tai lieu nay (bang, code, trich dan)."""
    md = md.replace("\r\n", "\n")
    out, i = [], 0
    lines = md.split("\n")
    while i < len(lines):
        ln = lines[i]

        if ln.startswith("```"):                                  # code block
            buf, i = [], i + 1
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i]); i += 1
            i += 1
            out.append("<pre><code>%s</code></pre>" % esc("\n".join(buf)))
            continue

        # HTML tho cho phan gap/mo — de nguyen, khong escape.
        if re.match(r"^</?(?:details|summary)\b", ln.strip()):
            out.append(ln.strip()); i += 1
            continue

        if ln.startswith("|") and i + 1 < len(lines) and re.match(
                r"^\|[\s:|-]+\|$", lines[i + 1].strip()):         # table
            head = cells(ln); i += 2
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(cells(lines[i])); i += 1
            out.append(
                "<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>" % (
                    "".join("<th>%s</th>" % inline(c) for c in head),
                    "".join("<tr>%s</tr>" % "".join(
                        "<td>%s</td>" % inline(c) for c in r) for r in rows)))
            continue

        if ln.startswith(">"):                                    # blockquote
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i].lstrip(">").strip()); i += 1
            para = "</p><p>".join(
                x for x in "\n".join(buf).split("\n\n") if x.strip())
            out.append("<blockquote><p>%s</p></blockquote>"
                       % inline(para).replace("\n", "<br>"))
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", ln)                    # heading
        if m:
            lv = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (lv, inline(m.group(2)), lv)); i += 1
            continue

        if re.match(r"^\s*[-*]\s+", ln) or re.match(r"^\s*\d+\.\s+", ln):
            ordered = bool(re.match(r"^\s*\d+\.\s+", ln))
            items = []
            while i < len(lines) and (
                    re.match(r"^\s*[-*]\s+", lines[i])
                    or re.match(r"^\s*\d+\.\s+", lines[i])):
                items.append(re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "", lines[i]))
                i += 1
            tag = "ol" if ordered else "ul"
            out.append("<%s>%s</%s>" % (
                tag, "".join("<li>%s</li>" % inline(x) for x in items), tag))
            continue

        if ln.strip() in ("---", "***"):
            out.append("<hr>"); i += 1; continue

        if not ln.strip():
            i += 1; continue

        buf = []                                                   # paragraph
        while i < len(lines) and lines[i].strip() and not re.match(
                r"^(#{1,6}\s|\||>|```|\s*[-*]\s|\s*\d+\.\s|---$)", lines[i]):
            buf.append(lines[i]); i += 1
        out.append("<p>%s</p>" % inline(" ".join(buf)))
    return "\n".join(out)


def cells(row):
    return [c.strip() for c in row.strip().strip("|").split("|")]


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def inline(s):
    s = esc(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"~~([^~]+)~~", r"<del>\1</del>", s)
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
                  lambda m: '<a href="%s">%s</a>'
                            % (weblink(m.group(2)), m.group(1)), s)


def weblink(href):
    """Doi link .md trong repo thanh .html phang trong docs/.

    Trang web de tat ca file cung mot thu muc, nen bo tien to ./ va ../.
    Muc luc buoi/README.md tro thanh trang chu index.html.
    """
    if "://" in href or href.startswith("#"):
        return href
    href = re.sub(r"^(?:\.\./|\./)+", "", href)
    if href == "README.md":
        return "index.html"
    return re.sub(r"\.md$", ".html", href)


def page(title, body, desc=""):
    return """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<style>%s</style>
</head>
<body><div class="wrap">
%s
</div></body>
</html>
""" % (esc(title), esc(desc), CSS, body)


def index_html(days):
    rows = []
    cur = None
    for d in days:
        if d["phase"] != cur:
            cur = d["phase"]
            a, b, name = PHASE[cur]
            rows.append('<div class="ph">Phase %d — %s · buổi %d–%d</div>'
                        % (cur, esc(name), a, b))
            rows.append('<div class="grid">')
            rows.append("</div>") if False else None
        tag = ('<span class="tag on">đầy đủ</span>' if d["full"]
               else '<span class="tag">khung</span>')
        rows.append(
            '<a class="card" href="%s"><b>BUỔI %d</b>'
            '<span>%s</span>%s</a>'
            % (d["file"].replace(".md", ".html"), d["n"],
               esc(d["title"].split("—", 1)[1].strip()), tag))
    body = """
<h1>Giáo trình cờ vua 30 buổi</h1>
<p class="lead">Cho bé 5 tuổi bắt đầu từ số 0. Phụ huynh làm huấn luyện viên —
<strong>không cần biết chơi cờ trước</strong>.</p>
<div class="note"><strong>Mỗi buổi ≤15 phút.</strong> Hết 15 phút mà bé vẫn muốn chơi
→ vẫn dừng. Bé chán → dừng ngay, hôm sau chơi tiếp. Vui quan trọng hơn lịch.</div>
<h2>30 buổi</h2>
%s
<h2>Đọc trước khi bắt đầu</h2>
<ul>
<li><a href="plan.html">Tổng quan giáo trình</a> — mục tiêu, cách vận hành, rủi ro</li>
<li><a href="print-buoi-1-6.html">Bản in buổi 1–6</a> — 1 buổi/trang, in ra chạy được
không cần màn hình</li>
</ul>
<h2>Vì sao buổi 7–30 mới có khung</h2>
<p>Cố ý. Chủ đề, trò chơi và tiêu chí &quot;xong&quot; của cả 30 buổi
<strong>đã chốt</strong>. Phần lời thoại và sơ đồ bày bàn chỉ soạn sau khi chạy xong
6 buổi đầu — vì lúc đó mới biết bé ngồi được bao nhiêu phút thật. Soạn sẵn 30 kịch bản
là soạn theo tưởng tượng, và sẽ phải viết lại.</p>
""" % "\n".join(rows)
    return page("Giáo trình cờ vua 30 buổi cho bé 5 tuổi", body,
                "Giáo trình cờ vua 30 buổi cho bé 5 tuổi, phụ huynh tự dạy.")


def build():
    days = load()

    io.open(os.path.join(BUOI, "README.md"), "w",
            encoding="utf-8", newline="\n").write(readme(days))

    if not os.path.isdir(SITE):
        os.makedirs(SITE)

    io.open(os.path.join(SITE, "index.html"), "w",
            encoding="utf-8", newline="\n").write(index_html(days))
    # Pages: khong chay Jekyll, tranh nuot file va thu muc bat dau bang _
    io.open(os.path.join(SITE, ".nojekyll"), "w").write("")

    for d in days:
        body = md2html(d["body"])
        html = page("Buổi %d — %s" % (d["n"], d["title"].split("—", 1)[1].strip()),
                    body, "Buổi %d/30 — giáo trình cờ vua cho bé 5 tuổi." % d["n"])
        io.open(os.path.join(SITE, d["file"].replace(".md", ".html")), "w",
                encoding="utf-8", newline="\n").write(html)

    # 6 trang phase + trang tong quan — cac trang buoi tro toi chung.
    for name in list(PFILE.values()) + ["plan"]:
        src = os.path.join(HERE, name + ".md")
        if not os.path.exists(src):
            continue
        raw = io.open(src, encoding="utf-8").read()
        raw = re.sub(r"^---\n.*?\n---\n", "", raw, count=1, flags=re.S)
        nav = ('<div class="nav"><a href="index.html">← Về mục lục 30 buổi</a>'
               "</div>")
        title = re.search(r"^#\s+(.+)$", raw, re.M)
        io.open(os.path.join(SITE, name + ".html"), "w",
                encoding="utf-8", newline="\n").write(
            page(title.group(1) if title else name,
                 nav + md2html(raw) + nav,
                 "Giáo trình cờ vua 30 buổi cho bé 5 tuổi."))

    # Ban in san co — sao chep sang docs/ de link tren web chay duoc.
    # `plan.html` goc KHONG sao chep: trang plan.html trong docs/ da duoc sinh
    # tu plan.md o tren, trung ten se de len nhau.
    copied = []
    for name in ("print-buoi-1-6.html",):
        src = os.path.join(HERE, name)
        if os.path.exists(src):
            io.open(os.path.join(SITE, name), "w", encoding="utf-8",
                    newline="").write(io.open(src, encoding="utf-8").read())
            copied.append(name)
    return days, copied


def verify(days, copied):
    """Doc lai tu dia. Moi link phai tro toi file co that trong docs/."""
    errs = []
    have = set(os.listdir(SITE))
    for d in days:
        f = d["file"].replace(".md", ".html")
        if f not in have:
            errs.append("thieu trang %s" % f); continue
        html = io.open(os.path.join(SITE, f), encoding="utf-8").read()
        for href in re.findall(r'href="([^"#:]+)"', html):
            if href not in have:
                errs.append("%s: link hong -> %s" % (f, href))
    idx = io.open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
    for href in re.findall(r'href="([^"#:]+)"', idx):
        if href not in have:
            errs.append("index.html: link hong -> %s" % href)
    if len(re.findall(r'class="card"', idx)) != 30:
        errs.append("trang chu khong liet ke du 30 buoi")
    if errs:
        sys.exit("SINH WEB SAI:\n  " + "\n  ".join(errs))


def main():
    days, copied = build()
    verify(days, copied)
    print("Da sinh buoi/README.md (muc luc 30 buoi)")
    print("Da sinh site/ cho GitHub Pages:")
    print("  index.html            trang chu, 30 the buoi")
    print("  buoi-01..30.html      %d trang buoi" % len(days))
    for c in copied:
        print("  %-22s(sao chep)" % c)
    print("Tat ca link da qua tu kiem.")


if __name__ == "__main__":
    main()
