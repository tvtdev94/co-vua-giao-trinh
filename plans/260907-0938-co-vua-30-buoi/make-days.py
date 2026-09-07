#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sinh 30 file `buoi/buoi-NN-*.md` — moi buoi mot file.

Buoi 1-6: lay NGUYEN VAN tu phase-01-ban-co-xe-tuong.md (noi dung da qua
red-team + da doi chieu so do voi make-print-pages.py). Khong go tay lai.

Buoi 7-30: lay KHUNG DA CHOT (muc 5.2 cua ban tu van) tu phase-02..06 —
chu de, tro choi, tieu chi "xong". Phan chi tiet (loi thoai, so do bay ban)
danh dau ro la CHUA SOAN, dung muc 2.17.

    python make-days.py

Script tu kiem sau khi ghi: du 30 file, buoi 1-6 khop byte voi phase-01,
va moi link dieu huong tro toi file co that.
"""

import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "phase-01-ban-co-xe-tuong.md")
OUTDIR = os.path.join(HERE, "buoi")

SLUG = {
    1: "ban-co-huong-ban-mau-o", 2: "xe-di-ngang-doc", 3: "xe-an-quan",
    4: "o-bi-kiem-soat", 5: "tuong-di-cheo", 6: "xe-tuong-cung-ban",
    7: "hau-la-xe-cong-tuong", 8: "hau-manh-co-nao", 9: "vua-di-1-o",
    10: "chieu-la-gi", 11: "ba-cach-thoat-chieu", 12: "ma-di-chu-l",
    13: "ma-nhay-qua-dau", 14: "ma-di-duong-dai", 15: "ma-doi-dau-quan-khac",
    16: "cua-1-bingo-quan", 17: "tot-di-thang", 18: "tot-an-cheo",
    19: "tot-nuoc-dau-2-o", 20: "phong-cap", 21: "cua-2-bingo-co-tot",
    22: "chieu-het-vs-chieu-thuong", 23: "mate-2-xe", 24: "mate-hau-vua",
    25: "hoa-va-stalemate", 26: "nhap-thanh", 27: "van-nho-8-quan",
    28: "van-nho-12-quan", 29: "van-day-du-tap", 30: "van-moc",
}

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

# Khung da chot (muc 5.2) cho buoi 7-30: tieu de, chu de, tro, tieu chi xong.
FRAME = {
    7: ("Hậu = Xe + Tượng", "**Hậu** = Xe + Tượng (không luật mới)",
        'Trò "Hậu ăn 3 xu trong 3 nước", 3 bài', "Giải được 3/3"),
    8: ("Hậu mạnh cỡ nào", "Hậu mạnh cỡ nào",
        'Trò "Hậu vs 4 quân": bé cầm Hậu, người lớn 4 Xe/Tốt bất động; Hậu ăn hết',
        "Bé thắng ít nhất 1 lần"),
    9: ("Vua đi 1 ô mọi hướng", "**Vua** đi 1 ô mọi hướng",
        'Trò "Vua đi bộ": Vua từ a1 tới h8, người lớn đặt 3 chướng ngại',
        "Bé không nhảy ô, tới đích"),
    10: ("Chiếu là gì", "**Chiếu** là gì",
         'Trò "Chiếu hay không chiếu?": người lớn dựng 8 thế, bé trả lời có/không',
         "7/8 đúng"),
    11: ("Ba cách thoát chiếu", "3 cách thoát chiếu",
         'Trò "Cứu Vua": 6 thế, bé tìm cách chạy / chắn / ăn', "5/6 đúng"),
    12: ("Mã đi hình chữ L", "**Mã** đi hình chữ L",
         'Trò "Mã ăn cà rốt": 1 Mã + 3 xu đặt gần', "8/10 nước đúng"),
    13: ("Mã nhảy qua đầu quân khác", "Mã **nhảy qua đầu** quân khác",
         'Trò "Mã vượt rào": vây Mã bằng 6 Tốt, bé vẫn nhảy ra',
         'Bé tự nói "Mã không bị chắn"'),
    14: ("Mã đi đường dài", "Mã đi đường dài",
         'Trò "Đua Mã": 2 Mã từ 2 góc, ai tới ô đích trước',
         "Bé tới đích, ≤1 nước sai"),
    15: ("Mã đối đầu quân khác", "Mã đối đầu quân khác",
         'Trò "Mã bắt Xe": Mã của bé vs Xe của người lớn, ai ăn được trước',
         "Chơi trọn 1 ván"),
    16: ("CỬA 1 — ôn 5 quân", "**CỬA 1** — ôn 5 quân (Xe, Tượng, Hậu, Vua, Mã)",
         'Trò "Bingo quân": người lớn chỉ 1 quân, bé đi 1 nước hợp lệ, '
         "12 lượt trộn ngẫu nhiên",
         "**≥11/12 đúng.** Không đạt → không đi tiếp"),
    17: ("Tốt đi thẳng, không ăn thẳng", "**Tốt** đi 1 ô thẳng, **không ăn thẳng**",
         'Trò "Tốt xếp hàng": 4 Tốt mỗi bên đối đầu → tắc hoàn toàn; '
         "để bé tự phát hiện", 'Bé tự nói "Tốt không ăn phía trước"'),
    18: ("Tốt ăn chéo", "Tốt **ăn chéo**",
         'Trò "Chiến tranh Tốt" 4 vs 4: ai đưa 1 Tốt tới cuối bàn trước thì thắng',
         "Chơi hết ván, ra kết quả"),
    19: ("Nước đầu đi 2 ô", "Nước đầu đi 2 ô",
         'Trò "Chiến tranh Tốt" 8 vs 8 đầy đủ',
         "Bé chơi hết ván, không cần nhắc luật đi"),
    20: ("Phong cấp Tốt → Hậu", "**Phong cấp** Tốt → Hậu",
         "Chiến tranh Tốt 8v8, tới đích đổi thành Hậu và **chơi tiếp** "
         "tới khi ăn sạch", 'Bé tự đổi đúng quân, hiểu "Tốt lên Hậu"'),
    21: ("CỬA 2 — ôn cả 6 quân", "**CỬA 2** — ôn cả 6 quân (thêm Tốt)",
         'Trò "Bingo quân" 12 lượt, có Tốt',
         "**≥11/12 đúng.** Không đạt → xem nhánh 5.2b"),
    22: ("Chiếu hết vs chiếu thường", "**Chiếu hết** vs chiếu thường",
         'Trò "Hết hay chưa hết?": 8 thế, bé phân loại', "6/8 đúng"),
    23: ("Chiếu hết bằng 2 Xe", "Chiếu hết bằng **2 Xe** (kiểu cầu thang)",
         "Bé cầm 2 Xe + Vua vs Vua trần của người lớn",
         "Mate được với ≤2 gợi ý"),
    24: ("Chiếu hết bằng Hậu + Vua", "Chiếu hết bằng **Hậu + Vua** (kiểu thu hộp)",
         "Bé cầm Hậu + Vua vs Vua trần", "Mate được với ≤2 gợi ý"),
    25: ("Hòa — vua bí mà không bị chiếu",
         "**Hòa**: Vua bí mà không bị chiếu; không đủ lực",
         '4 thế, bé phân biệt "hết" / "hòa"', "3/4 đúng"),
    26: ("Nhập thành", '**Nhập thành** như một "phép đặc biệt"',
         "Làm động tác 5 lần liên tiếp (2 bên, 2 cánh) + 3 thế "
         '"được / không được"',
         "5/5 động tác đúng; nói được ≥2 trong 4 điều kiện"),
    27: ("Ván nhỏ 8 quân mỗi bên", "Ván nhỏ 8 quân/bên",
         "Vua + Hậu + 2 Xe + 4 Tốt, chơi từ đầu tới chiếu hết. Cho đi lại tự do",
         "Ván có kết quả (chiếu hết hoặc hòa)"),
    28: ("Ván nhỏ 12 quân mỗi bên", "Ván nhỏ 12 quân/bên",
         "Thêm 2 Tượng + 2 Mã. Cho đi lại tự do", "Ván có kết quả"),
    29: ("Ván đầy đủ 32 quân — chế độ tập",
         "**Ván đầy đủ 32 quân**, chế độ tập",
         "Người lớn chơi yếu có chủ đích, **đi lại không giới hạn**, "
         "nhắc luật thoải mái", "Ván có kết quả, bé không rời bàn giữa ván"),
    30: ("VÁN MỐC", "**VÁN MỐC** — nghiệm thu cả chương trình",
         "32 quân, **không đi lại**, chạm quân là phải đi. Người lớn chỉ nhắc "
         "khi bé đi phi luật — **đếm số lần nhắc**. Bấm giờ thời gian bé tự "
         "nguyện ngồi",
         "Ván có kết quả, **≤3 lần nhắc luật**, và sau ván bé "
         "**tự đòi chơi tiếp**"),
}


def phase_of(n):
    for p, (a, b, _) in PHASE.items():
        if a <= n <= b:
            return p
    raise ValueError(n)


def fname(n):
    return "buoi-%02d-%s.md" % (n, SLUG[n])


def nav(n):
    prev = "[← Buổi %d](./%s)" % (n - 1, fname(n - 1)) if n > 1 else "—"
    nxt = "[Buổi %d →](./%s)" % (n + 1, fname(n + 1)) if n < 30 else "—"
    return "%s · [Mục lục](./README.md) · %s" % (prev, nxt)


def extract_sessions():
    """Cat 6 buoi ra khoi PHAN 2 cua phase-01, giu nguyen van."""
    md = io.open(SRC, encoding="utf-8").read()
    part2 = md[md.index("## PHẦN 2 — Sáu buổi"):
               md.index("## PHẦN 3 — Nghiệm thu Phase 1")]
    secs = list(re.finditer(r"^### (BUỔI (\d+) — .+)$", part2, re.M))
    if len(secs) != 6:
        sys.exit("Doi 6 buoi trong PHAN 2, tim thay %d" % len(secs))
    out = {}
    for i, m in enumerate(secs):
        stop = secs[i + 1].start() if i + 1 < len(secs) else len(part2)
        body = part2[m.end():stop].strip()
        body = re.sub(r"\n+---\s*$", "", body).strip()
        out[int(m.group(2))] = (m.group(1).split("—", 1)[1].strip(), body)
    return out


def frame_body(n, ph):
    t, chude, tro, xong = FRAME[n]
    return (
        "> **Buổi này mới có KHUNG ĐÃ CHỐT — chưa soạn chi tiết.**\n"
        "> Cố ý theo mục 2.17: lời thoại và sơ đồ bày bàn chỉ soạn sau khi chạy "
        "xong phase trước và đo được số phút chú ý thật của bé.\n"
        "> Chủ đề, trò chơi và tiêu chí \"xong\" bên dưới **đã chốt, không đổi**.\n\n"
        "## Khung đã chốt\n\n"
        "| Mục | Nội dung |\n|---|---|\n"
        "| **Chủ đề** | %s |\n"
        "| **Trò / hoạt động** | %s |\n"
        "| **\"Xong\" trông như thế nào** | %s |\n\n"
        "## Còn phải soạn trước khi chạy buổi này\n\n"
        "- [ ] Sơ đồ bày bàn cụ thể — toạ độ từng quân, kiểm trước khi gọi bé\n"
        "- [ ] Lời thoại gợi ý — mở đầu, vào trò, câu chốt\n"
        "- [ ] Bảng sửa lỗi 1-nước — \"bé làm gì / ĐỪNG nói / HÃY nói\"\n"
        "- [ ] Điều kiện dừng sớm riêng của buổi\n\n"
        "Ràng buộc kế thừa và Risk Assessment của cả phase: xem "
        "[`%s.md`](../%s.md).\n" % (chude, tro, xong, PFILE[ph], PFILE[ph])
    )


def build():
    if not os.path.isdir(OUTDIR):
        os.makedirs(OUTDIR)
    ex = extract_sessions()
    written = []
    for n in range(1, 31):
        ph = phase_of(n)
        pname = PHASE[ph][2]
        if n <= 6:
            title, body = ex[n]
            detail = "day-du"
        else:
            title = FRAME[n][0]
            body = frame_body(n, ph)
            detail = "khung-da-chot"

        doc = (
            "---\n"
            "buoi: %d\n"
            'title: "Buổi %d — %s"\n'
            "phase: %d\n"
            "chi_tiet: %s\n"
            "status: pending\n"
            "---\n\n"
            "# Buổi %d — %s\n\n"
            "*Phase %d — %s · buổi %d/30*\n\n"
            "%s\n\n---\n\n"
            "%s\n\n---\n\n"
            "## Ghi sau buổi — 3 con số (15 giây, không bỏ)\n\n"
            "| Số phút thực | Lý do dừng | Bé đòi chơi thêm? |\n|---|---|---|\n"
            "| ___ | hết nội dung / 1 tín hiệu / 2 tín hiệu / hết 15 phút | C / K |\n\n"
            "%s\n"
        ) % (n, n, title, ph, detail, n, title, ph, pname, n,
             nav(n), body.strip(), nav(n))

        path = os.path.join(OUTDIR, fname(n))
        io.open(path, "w", encoding="utf-8", newline="\n").write(doc)
        written.append((n, fname(n), len(doc)))
    return written, ex


def verify(written, ex):
    """Doc lai tu dia. Sai la dung, khong im lang xuat ra ban hong."""
    errs = []
    if len(written) != 30:
        errs.append("chi tao %d file, can 30" % len(written))

    names = {f for _, f, _ in written}
    for n, f, _ in written:
        body = io.open(os.path.join(OUTDIR, f), encoding="utf-8").read()
        # Buoi 1-6 phai chua nguyen van noi dung goc.
        if n <= 6 and ex[n][1] not in body:
            errs.append("buoi %d: noi dung KHONG khop phase-01" % n)
        # Moi link dieu huong phai tro toi file co that.
        for link in re.findall(r"\]\(\./(buoi-\d\d-[a-z0-9-]+\.md)\)", body):
            if link not in names:
                errs.append("buoi %d: link hong -> %s" % (n, link))
        if "README.md" not in body:
            errs.append("buoi %d: thieu link muc luc" % n)
    if errs:
        sys.exit("SINH FILE SAI:\n  " + "\n  ".join(errs))


def main():
    written, ex = build()
    verify(written, ex)
    total = sum(s for _, _, s in written)
    full = sum(1 for n, _, _ in written if n <= 6)
    print("Da tao 30 file trong buoi/ (%s KB)" % format(total // 1024, ","))
    print("  %d buoi chi tiet day du (1-6), nguyen van tu phase-01" % full)
    print("  %d buoi moi co khung da chot (7-30)" % (30 - full))
    print("Tat ca link dieu huong da qua tu kiem.")


if __name__ == "__main__":
    main()
