#!/usr/bin/env python3
"""Nhung lai noi dung 6 file phase-*.md vao plan.html.

plan.html giu mot ban sao day du cua cac file phase-*.md de doc offline
khong can server. Cac file .md la ban goc; chay script nay sau moi lan
sua .md de ban sao trong HTML khong bi lech.

    python rebuild-html.py

Script kiem tra lai sau khi ghi va bao loi neu ban nhung khong khop dia.
"""

import glob
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(HERE, "plan.html")
BLOCK = re.compile(
    r'(<script id="phase-src" type="application/json">)(.*?)(</script>)', re.S
)


def read_phases():
    """Doc tat ca phase-*.md, tra ve dict {ten file: noi dung}."""
    files = sorted(glob.glob(os.path.join(HERE, "phase-*.md")))
    if not files:
        sys.exit("Khong tim thay file phase-*.md nao trong " + HERE)
    return {os.path.basename(f): io.open(f, encoding="utf-8").read() for f in files}


def encode(phases):
    """JSON hoa, tranh dong </script> ket thuc som the script."""
    return json.dumps(phases, ensure_ascii=False).replace("</script>", "<\\/script>")


def decode(payload):
    return json.loads(payload.replace("<\\/script>", "</script>"))


def main():
    phases = read_phases()
    html = io.open(HTML, encoding="utf-8").read()

    if not BLOCK.search(html):
        sys.exit("Khong tim thay khoi <script id=\"phase-src\"> trong plan.html")

    payload = encode(phases)
    new = BLOCK.sub(lambda m: m.group(1) + payload + m.group(3), html, count=1)
    io.open(HTML, "w", encoding="utf-8", newline="").write(new)

    # Doc lai tu dia de xac nhan ban nhung khop, khong tin bien trong bo nho.
    check = decode(BLOCK.search(io.open(HTML, encoding="utf-8").read()).group(2))
    if check != phases:
        sys.exit("Ban nhung KHONG khop file .md tren dia - kiem tra lai")

    print("Da nhung {} file phase vao plan.html:".format(len(phases)))
    for name, body in sorted(phases.items()):
        print("  {:44s} {:>7,} ky tu".format(name, len(body)))


if __name__ == "__main__":
    main()
