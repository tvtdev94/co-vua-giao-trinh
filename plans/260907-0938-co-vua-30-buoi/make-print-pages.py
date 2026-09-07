#!/usr/bin/env python3
"""Sinh file in `print-buoi-1-6.html` — bo giay de chay Phase 1 khong can man hinh.

Gom: the A5 "trong tai" (2 mat, co duong cat) · 6 the bay ban cat roi de
kep vao the A5 (R1) · 6 trang kich ban 1 buoi/trang · bang theo doi 30 o.

So do ban co duoc SINH TU CONG THUC mau o, khong go tay, va script TU KIEM
truoc khi ghi file: mau o, tinh toi duoc cua Tuong, va khong ai an duoc o
nuoc 1 trong cac the doi khang. Sai mot toa do la script bao loi, khong im
lang xuat ra ban in hong.

    python make-print-pages.py
"""

import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "print-buoi-1-6.html")
FILES = "abcdefgh"


# ---------------------------------------------------------------- hinh hoc
def light(sq):
    """O sang <=> (so cot + so hang) le. a1 toi, h1 sang."""
    return ((FILES.index(sq[0]) + 1) + int(sq[1])) % 2 == 1


def same_line(a, b):
    """Cung hang hoac cung cot — duong di cua Xe."""
    return a[0] == b[0] or a[1] == b[1]


def same_diag(a, b):
    """Cung duong cheo — duong di cua Tuong."""
    return a != b and abs(FILES.index(a[0]) - FILES.index(b[0])) == abs(
        int(a[1]) - int(b[1])
    )


# ---------------------------------------------------------------- du lieu
# Moi the: {o: ky hieu}. X/T = quan cua be (do), x/t = quan nguoi lon (den),
# o = xu, p = Tot lam bia.
BOARDS = {
    1: {},
    2: {"d4": "X", "d7": "o", "a4": "o", "h4": "o", "d1": "o", "g4": "o"},
    3: {"a1": "X", "a5": "p", "d1": "p", "d5": "p", "h5": "p", "h1": "p"},
    4: {"b2": "X", "g7": "x"},
    5: {"c1": "T", "b2": "o", "a3": "o", "c5": "o", "e3": "o", "g5": "o"},
    6: {"b2": "X", "e2": "T", "d7": "t", "g7": "x"},
}

SETUP_NOTE = {
    1: "Ban TRONG. Dat lech huong co chu dich (o den goc phai duoi) de be co viec sua. 8 xu trong tui vai kin.",
    2: "1 Xe + 5 xu. Ca 5 xu cung hang hoac cung cot voi Xe.",
    3: "1 Xe + 5 Tot lam bia. Tot dung im, KHONG giai thich Tot di the nao.",
    4: "2 Xe doi khang. Khac hang, khac cot — khong ai an duoc ngay.",
    5: "1 Tuong + 5 xu, TAT CA o den. Kiem 2 buoc: mau o VA tinh toi duoc.",
    6: "Moi ben 1 Xe + 1 Tuong. Hai Tuong cung o trang nen gap duoc nhau.",
}

SESSIONS = [
    {
        "n": 1,
        "title": "Bàn cờ, hướng bàn, màu ô",
        "done": "Bé tự quay bàn đúng hướng, <b>2 lần liên tiếp</b>",
        "prep": [
            "Đặt bàn đúng hướng 2 lần, tự soát: <b>ô trắng ở góc phải dưới</b>.",
            "Thuộc một câu duy nhất: <b>“Ô trắng ở tay phải mình.”</b>",
            "Buổi này <b>không có quân cờ nào</b> trên bàn. Bé hỏi tên quân → “mai mình làm quen bạn ấy”.",
        ],
        "lines": [
            "“Con nhìn cái bàn này xem. Có gì lạ không?” <i>(để bé nói bất cứ gì, không sửa)</i>",
            "“Bàn này có quy tắc buồn cười: <b>ô trắng phải ở tay phải mình</b>. Giờ ô góc phải màu gì?”",
            "“Vậy mình sửa kiểu gì nhỉ?” <i>(để bé tự quay. Quay sai chiều → im lặng, để bé thử tiếp)</i>",
            "“Đúng rồi! Giờ con quay lung tung đi, rồi tự sửa lại cho bố/mẹ xem.”",
            "<b>Trò 2:</b> “Con lấy 1 xu, đặt đại lên bàn, rồi nói nó đứng trên ô màu gì.”",
            "<b>Chốt:</b> “Con nhớ ô trắng ở tay nào rồi đấy. Mai mình cho một bạn lên bàn chơi.”",
        ],
        "fix": [
            ("Quay bàn sai chiều", "<i>(im lặng 5 giây)</i> → “Ô góc tay phải con giờ màu gì?”"),
            ("Nói sai màu ô", "“Con đặt ngón tay lên ô đó xem?”"),
            ("Đếm ô lung tung", "Không sửa. Buổi này không dạy đếm ô."),
        ],
        "stop": [
            ("Quay đúng 2 lần rồi dựng xu thành tháp", "<b>S3</b> — trò đã xong việc. Chốt buổi ngay, đừng ép hết 8 xu"),
            ("Nhìn ra cửa sổ &gt;5 giây, 2 lần", "<b>S1</b> → trò tay 60–90s (đoán quân trong túi kín) → quay lại đúng 1 lần → tối đa +3 phút"),
            ("Nói “chán quá”", "<b>S3</b> — nếu là tín hiệu thứ 2 → dừng ngay, kết bằng 1 lượt bé chắc chắn làm được + khen cụ thể"),
            ("Đúng 2 lần, mới 4 phút, vẫn hào hứng", "Chơi tiếp trò xu, nhưng <b>dừng trước phút 11</b>"),
        ],
    },
    {
        "n": 2,
        "title": "Xe đi ngang và dọc",
        "done": "<b>10/10 nước</b> đi đúng đường thẳng — <b>cộng dồn qua 2–3 lượt</b> (mỗi lượt ~6 nước)",
        "prep": [
            "Đặt 1 Xe giữa bàn trống, tự đi 5 nước: 2 ngang, 2 dọc, 1 dài hết bàn.",
            "Thuộc câu: <b>“Xe đi thẳng băng — ngang hoặc dọc, đi bao xa cũng được, nhưng không đi chéo.”</b>",
            "<b>Chưa dạy ăn quân.</b> Xu chỉ để nhặt lên, tránh dùng chữ “ăn” nếu được.",
        ],
        "lines": [
            "<b>Ôn:</b> “Ô trắng ở tay nào ấy nhỉ?” <i>(bé chỉ → đi tiếp ngay, không giảng)</i>",
            "“Đây là bạn <b>Xe</b>. Bạn ấy đi thẳng băng thôi: ngang, hoặc dọc.” <i>(vừa nói vừa trượt ngón tay)</i>",
            "“Xa bao nhiêu cũng được.” <i>(cho bé đẩy 1 nước)</i> “<b>Nhưng không biết đi chéo.</b>”",
            "“Trên bàn có 5 cái xu. Con lấy Xe đi thu hết về. Xem hết bao nhiêu nước nhé.”",
            "<b>Kết lượt:</b> “6 nước! Lượt sau mình <b>chơi thế khác</b> nhé.”",
            "<b>Chốt:</b> “Bạn Xe của con đi thẳng băng luôn, không đi chéo lần nào.”",
        ],
        "fix": [
            ("Đẩy Xe đi chéo", "<i>(chờ tay rời quân)</i> → <b>“Xe đi kiểu gì ấy nhỉ?”</b>"),
            ("Nhấc Xe, đặt xa, nhảy qua ô", "“Con thử <b>trượt</b> Xe trên mặt bàn cho bố/mẹ xem đường nó đi”"),
            ("Đi 1 nước ăn 2 xu", "“Xe mình đứng được mấy chỗ một lúc?”"),
            ("Đi đúng nhưng chậm, ngập ngừng", "<b>Không nói gì. Đợi.</b> Im lặng khi bé đang nghĩ là luật cứng"),
            ("Đi chéo lần thứ 3", "<b>Ngừng sửa.</b> Ghi bảng. Buổi sau: Xe trên hàng 1, xu cùng hàng đó"),
        ],
        "stop": [
            ("Xong lượt 1, bé nói “nữa nữa”", "Chơi lượt 2. Sau lượt 2 <b>dừng nếu đã 9–10 phút</b>, kể cả bé còn muốn"),
            ("Đi bừa 2 nước liền", "<b>S2</b> → trò tay 60–90s → quay lại đúng 1 lần"),
            ("Xếp xu thành chồng thay vì ăn", "<b>S3</b> → dừng, chốt bằng 1 nước Xe dễ"),
            ("Sai &gt;3 nước trong lượt 1", "Đơn giản hoá ngay: còn <b>3 xu</b>, cả 3 <b>cùng một cột</b> với Xe"),
        ],
        "warn": "ĐỪNG nói “lượt sau thử ít nước hơn” ở buổi này — thế này ít nhất phải 6 nước. Câu đó để dành buổi 3.",
    },
    {
        "n": 3,
        "title": "Xe ăn quân (thay chỗ)",
        "done": "Ăn hết trong <b>≤6 nước</b> (5 nếu tối ưu — có 4 đường 5 nước)",
        "prep": [
            "Tự làm động tác ăn 3 lần: <b>nhấc quân bị ăn ra trước, rồi đặt Xe vào ô đó</b>.",
            "Thuộc câu: <b>“Xe đi tới ô có quân đối phương thì mình nhấc bạn kia ra, Xe đứng vào chỗ ấy.”</b>",
            "<b>CẢNH BÁO:</b> Tốt hôm nay chỉ làm bia. <b>Không giải thích Tốt đi thế nào.</b> Bé hỏi → “mấy bạn này hôm nay đứng im thôi, mai mốt mình mới làm quen”.",
        ],
        "lines": [
            "<b>Ôn:</b> “Bạn Xe đi kiểu gì ấy nhỉ?” <i>(bé trả lời hoặc chỉ tay — đủ rồi)</i>",
            "“Hôm nay Xe của con gặp mấy bạn <b>đang đứng trên bàn</b>. Xe đi tới chỗ bạn ấy thì bạn ấy phải ra khỏi bàn, còn Xe đứng vào đúng chỗ đó.”",
            "<i>(làm mẫu 1 lần thật chậm: nhấc Tốt ra → đặt Xe vào)</i> “Con làm thử nước đầu tiên xem.”",
            "“Còn mấy bạn nữa?” <i>(cho bé đếm, đừng đếm hộ)</i>",
            "<b>Bé đi vòng vèo — KHÔNG sửa:</b> “8 nước! Lượt sau mình thử ít hơn xem có được không.”",
            "<b>Chốt:</b> “Con dọn sạch bàn trong ___ nước.” <i>(điền số THẬT, đừng đọc số in sẵn)</i>",
        ],
        "fix": [
            ("Nhảy Xe <b>qua đầu</b> một Tốt", "<i>(chờ tay rời quân)</i> → <b>“Trên đường đi có ai đang đứng không nhỉ?”</b>"),
            ("Để 2 quân trên cùng 1 ô", "“Một ô đứng được mấy bạn?”"),
            ("Nhấc Tốt ra nhưng quên đặt Xe vào", "“Giờ Xe đứng ở đâu?”"),
            ("Hỏi “bạn Tốt đi thế nào?”", "<b>“Hôm nay bạn ấy đứng im thôi. Mai mốt mình làm quen.”</b> <i>(tuyệt đối không giải thích)</i>"),
        ],
        "stop": [
            ("Lượt 1 ăn hết ≤6 nước", "<b>Mục tiêu đã đạt.</b> Chơi thêm tối đa 1 lượt rồi dừng, kể cả còn thời gian"),
            ("Mất &gt;10 nước ở lượt 1, bắt đầu thở dài", "Bỏ bớt còn <b>3 Tốt</b> ngay ở lượt 2, đừng chờ tín hiệu thứ 2"),
            ("Cầm Tốt bị ăn lên chơi", "<b>S3</b> → trò tay 60–90s: đoán quân trong túi kín"),
            ("Đòi tự bày lại thế để chơi nữa", "<b>Cho làm</b> — hoạt động bé tự chọn kéo dài chú ý tốt nhất. Vẫn dừng trước phút 12"),
        ],
    },
    {
        "n": 4,
        "title": "Ô bị quân khác kiểm soát",
        "done": "<b>2/3 ván</b> bé không tự đi vào ô bị ăn",
        "prep": [
            "Dựng thế Xe vs Xe, tự hỏi trước mỗi nước: <i>“ô mình định đến có nằm trên hàng/cột của Xe kia không?”</i>",
            "Thuộc câu: <b>“Đừng đứng vào đường của bạn kia.”</b>",
            "<b>Đây là buổi khái niệm đầu tiên.</b> Không kỳ vọng bé hiểu — kỳ vọng bé <b>né được</b>.",
            "Chỉ tiêu: <b>bé thắng 2/3</b>. Người lớn thua bằng cách <i>đi vào đường của bé</i>, y hệt lỗi bé hay mắc.",
        ],
        "lines": [
            "<b>Ôn:</b> “Xe ăn bạn khác kiểu gì ấy nhỉ?” <i>(bé làm mẫu 1 nước là đủ)</i>",
            "“Hôm nay hai bạn Xe đấu nhau. Ai ăn được Xe kia trước thì thắng.”",
            "<b>Gieo hạt, CHỈ 1 LẦN:</b> “Có một mẹo: Xe kia cũng đi thẳng băng như Xe con. Nên <b>đừng đứng vào đường của bạn ấy</b>.” <i>(trượt ngón tay dọc hàng và cột của Xe kia)</i>",
            "<b>Bé định đi vào ô bị ăn — CHỈ NÓI SAU KHI TAY RỜI QUÂN:</b> “Xe kia đi thẳng từ chỗ nó, có tới được chỗ Xe con vừa đứng không nhỉ?”",
            "<b>Khi người lớn thua:</b> “Ối, bố/mẹ đứng nhầm vào đường của con rồi!”",
            "<b>Chốt:</b> “Con nhìn thấy đường của Xe kia trước khi đi. Khó đấy, mà con làm được.”",
        ],
        "fix": [
            ("Đặt Xe vào hàng/cột của Xe đối phương", "<b>“Xe kia đi thẳng, có tới chỗ đó được không nhỉ?”</b> → cho đi lại"),
            ("Né quá mức, lùi vào góc, không tấn công", "<b>Không sửa.</b> Né là kỹ năng buổi này"),
            ("Đi vào ô bị ăn lần thứ 3", "<b>Ngừng sửa.</b> Đổi cách: bỏ 4 xu lên các ô nguy hiểm cho bé <i>nhìn thấy</i>"),
            ("Thua và buồn", "“Ván này bố/mẹ may thôi. Ván nữa nhé?” → cho bé đi trước, người lớn thua ván sau"),
        ],
        "stop": [
            ("Thắng ván 1 nhanh, đòi chơi tiếp", "Chơi ván 2. <b>Buổi dễ chạm trần nhất</b> — dừng ở phút 11–12"),
            ("Thua 2 ván liên tiếp, mặt xị", "<b>Nguy cơ S3.</b> Ván 3 người lớn <b>chắc chắn thua</b>, kết buổi ngay sau đó"),
            ("Đi bừa, không nhìn Xe đối phương, 2 nước liền", "<b>S2</b> → trò tay 60–90s → quay lại đúng 1 lần"),
            ("Không hiểu “đường của Xe kia” sau cả 3 ván", "<b>Không sao.</b> Ghi bảng. Khái niệm quay lại ở buổi 10–11. Không lặp thêm buổi"),
        ],
        "warn": "Bé đi trước ván 1 và 3; VÁN 2 NGƯỜI LỚN ĐI TRƯỚC. Đi trước là lợi thế thật — cho bé đi trước cả 3 ván sẽ đẩy tỉ lệ thắng lên gần 100%, phá chỉ tiêu 60–70%.",
    },
    {
        "n": 5,
        "title": "Tượng đi chéo + mẹo tự kiểm",
        "done": "Bé <b>tự nói được</b> màu ô của Tượng mình, không cần hỏi",
        "prep": [
            "Đặt 1 Tượng, đi 5 nước chéo, tự soát: <b>màu ô không bao giờ đổi</b>.",
            "Thuộc câu: <b>“Tượng đi chéo. Và bạn ấy ở ô màu gì thì ở màu đó mãi mãi.”</b>",
            "<b>Kiểm 2 bước trước khi gọi bé:</b> (1) tất cả xu cùng màu ô với Tượng; (2) từng xu có nằm trên đường chéo <b>đi tới được</b> không. Cùng màu là CHƯA ĐỦ.",
        ],
        "lines": [
            "<b>Ôn:</b> “Hôm qua hai bạn Xe đấu nhau, ai thắng ấy nhỉ?” <i>(chuyện trò, không kiểm tra)</i>",
            "“Đây là bạn <b>Tượng</b>. Bạn ấy không đi thẳng như Xe đâu — bạn ấy đi <b>chéo</b>.” <i>(trượt ngón tay theo đường chéo)</i>",
            "<b>Gieo mẹo — quan trọng nhất buổi:</b> “Con nhìn xem bạn Tượng đang đứng ô màu gì?” → “Giờ đi thêm một nước… Ô màu gì?” → “Nữa đi… Màu gì?”",
            "“Ơ, lạ nhỉ! <b>Tượng đen thì đen mãi mãi.</b> <b>Mà Tượng trắng thì cũng trắng mãi mãi</b> — bạn Tượng nào cũng giữ nguyên màu ô của mình.”",
            "“Trên bàn có 5 cái xu, cái nào cũng đứng ô đen — vừa đúng màu của Tượng con. Con đi thu hết nhé.”",
            "<b>Chốt:</b> “Con tự biết Tượng của con ở ô đen mà bố/mẹ không phải nhắc.”",
        ],
        "fix": [
            ("Đi Tượng thẳng (lẫn với Xe)", "<i>(chờ tay rời quân)</i> → <b>“Tượng đi kiểu gì ấy nhỉ?”</b>"),
            ("Đi chéo nhưng lệch sang ô khác màu", "<b>“Tượng mình màu ô gì? Còn ô con vừa đặt?”</b> → bé tự thấy"),
            ("Hỏi “sao Tượng không đi thẳng được?”", "<b>“Ừ, mỗi bạn có kiểu đi riêng.”</b> Không giải thích thêm"),
            ("Lẫn Xe/Tượng 3 lần", "<b>Ngừng sửa.</b> Ghi bảng. Buổi 6 sẽ tự phân giải"),
        ],
        "stop": [
            ("Tự nói “đen mãi mãi” không cần hỏi", "<b>Mục tiêu đã đạt.</b> Chơi nốt lượt rồi dừng"),
            ("Lẫn Tượng với Xe liên tục ở lượt 1", "Đơn giản hoá: <b>1 Tượng + 2 xu</b>, cả 2 nằm đúng trên đường chéo hiện tại"),
            ("Nản vì “không tới được” xu", "Kiểm lại ngay. Nếu đặt sai → <b>lỗi người lớn</b>: “À, bố/mẹ đặt nhầm rồi, xin lỗi con”"),
            ("Xin đổi sang chơi Xe", "Cho chơi Xe 1 lượt rồi kết buổi. Buổi này coi như chưa xong, lặp nội dung Tượng buổi sau"),
        ],
        "warn": "BUỔI NÀY KHÔNG ĐẾM NƯỚC. Đường 5 nước là DUY NHẤT — bé đi 6–7 nước vẫn đạt. Đừng lấy số 5 làm mục tiêu rồi sửa bé lệch khỏi đường đó.",
    },
    {
        "n": 6,
        "title": "Xe + Tượng cùng bàn — ván thật đầu tiên",
        "done": "Chơi trọn <b>1 ván</b>, <b>không phải nhắc cách đi quân</b> — cửa nghiệm thu Phase 1",
        "prep": [
            "Đi 3 nước Xe + 3 nước Tượng liên tiếp, không ngập ngừng.",
            "<b>Người lớn phải thua 2/3 lần</b>, và thua <i>tự nhiên</i> — đi vào đường quân của bé. <b>Không cho không quân 2 nước liền.</b>",
            "Buổi này <b>nên dùng</b> “người lớn cố tình đi sai 1 nước” — kể cả đã dùng ở buổi 4.",
            "<b>Kiểm trước khi gọi bé:</b> hai Tượng cùng màu ô; trượt ngón tay dọc hàng/cột mỗi Xe — không chạm quân nào của bên kia.",
        ],
        "lines": [
            "<b>Ôn — cho bé làm mẫu, đừng hỏi lý thuyết:</b> “Con đi cho bố/mẹ xem một nước Xe… rồi một nước Tượng.”",
            "“Hôm nay mình chơi thật nhé. Mỗi bên có một bạn Xe và một bạn Tượng. <b>Ai ăn hết quân của bên kia thì thắng.</b> Con đi trước.”",
            "<b>Trong ván — im lặng là mặc định:</b> “Đến lượt con.” · “Quân nào của con đang đứng gần bạn kia nhỉ?”",
            "<b>Cố tình đi sai 1 lần:</b> <i>(đẩy Tượng đi thẳng như Xe)</i> → chờ 3 giây → bé bắt được: <b>“Ối! Con bắt được bố/mẹ rồi.”</b>",
            "<b>Bé hỏi vì sao Tượng này ô trắng:</b> “Ừ, bạn Tượng này ở ô trắng, nên bạn ấy trắng mãi mãi.”",
            "<b>Chốt:</b> “Con chơi hết cả ván mà bố/mẹ không phải nhắc quân nào đi kiểu gì luôn.”",
        ],
        "fix": [
            ("Đi Tượng thẳng / Xe chéo", "<i>(chờ tay rời quân)</i> → <b>“Bạn ấy đi kiểu gì ấy nhỉ?”</b> → cho đi lại"),
            ("Cầm nhầm quân", "Không sửa. Cho đặt lại, không bình luận"),
            ("Để mất cả 2 quân nhanh", "Không sửa. <b>Ván sau người lớn thua.</b> Không giảng chiến thuật — non-goal"),
            ("Sai cách đi lần thứ 3", "<b>Ngừng sửa.</b> Ghi bảng → nghĩa là <b>Phase 1 chưa xong</b>"),
        ],
        "stop": [
            ("Ván 1 xong trong 6–7 phút, muốn chơi nữa", "Chơi ván 2. Dừng ở phút 11–12 dù chưa xong — <b>“mai mình chơi tiếp ván này”</b>, để nguyên thế"),
            ("Ván kéo dài, rượt nhau không ăn được gì", "Người lớn <b>chủ động đưa 1 quân vào đường bé ăn</b>. Ván không kết thúc là kịch bản tệ nhất"),
            ("2 tín hiệu giữa ván", "Dừng ngay, <b>để nguyên bàn cờ</b>. “Ván này mình để đây, mai chơi tiếp.” Không dọn"),
            ("Thắng và đòi chơi ván 3", "<b>Từ chối vui vẻ:</b> “Mai nhé.” → đây chính là lúc <b>sản xuất</b> chỉ số “bé tự đòi chơi”"),
        ],
    },
]


# ---------------------------------------------------------------- tu kiem
def verify():
    """Kiem lai moi the truoc khi in. Sai la dung, khong xuat ban in hong."""
    errs = []

    # Buoi 2: moi xu phai cung hang hoac cung cot voi Xe
    for sq, v in BOARDS[2].items():
        if v == "o" and not same_line(sq, "d4"):
            errs.append("buoi 2: xu %s khong cung hang/cot voi Xe d4" % sq)

    # Buoi 3: duong 5 nuoc, moi nuoc an 1 Tot, khong bi chan
    path3 = ["a1", "a5", "d5", "d1", "h1", "h5"]
    left = {s for s, v in BOARDS[3].items() if v == "p"}
    for a, b in zip(path3, path3[1:]):
        if not same_line(a, b):
            errs.append("buoi 3: %s->%s khong phai nuoc Xe" % (a, b))
        if b not in left:
            errs.append("buoi 3: %s khong co Tot de an" % b)
        left.discard(b)
    if left:
        errs.append("buoi 3: con Tot chua an: %s" % sorted(left))

    # Buoi 4: hai Xe khac hang VA khac cot
    if same_line("b2", "g7"):
        errs.append("buoi 4: hai Xe an duoc nhau ngay nuoc 1")

    # Buoi 5: cung mau ô + duong 5 nuoc lien tiep hop le
    path5 = ["c1", "b2", "a3", "c5", "e3", "g5"]
    if any(light(s) != light("c1") for s in path5):
        errs.append("buoi 5: co o khong cung mau voi Tuong c1")
    for a, b in zip(path5, path5[1:]):
        if not same_diag(a, b):
            errs.append("buoi 5: %s->%s khong phai nuoc Tuong" % (a, b))
    if set(path5[1:]) != {s for s, v in BOARDS[5].items() if v == "o"}:
        errs.append("buoi 5: duong di khong khop bo xu tren ban")

    # Buoi 6: hai Tuong cung mau, va KHONG ai an duoc o nuoc 1
    mine = {s: v for s, v in BOARDS[6].items() if v.isupper()}
    yours = {s: v for s, v in BOARDS[6].items() if v.islower()}
    bishops = [s for s, v in BOARDS[6].items() if v in "Tt"]
    if light(bishops[0]) != light(bishops[1]):
        errs.append("buoi 6: hai Tuong khac mau o, khong bao gio gap nhau")
    for group_a, group_b in ((mine, yours), (yours, mine)):
        for sq, pc in group_a.items():
            hit = same_line if pc in "Xx" else same_diag
            for tgt in group_b:
                if hit(sq, tgt):
                    errs.append("buoi 6: %s an duoc %s ngay nuoc 1" % (sq, tgt))

    if errs:
        sys.exit("THE CO SAI — khong xuat ban in:\n  " + "\n  ".join(errs))


# ---------------------------------------------------------------- ve ban co
GLYPH = {"X": "X", "T": "T", "x": "X", "t": "T"}


def draw(pieces, coords=False):
    """Sinh HTML mot ban co. coords=True thi in chu cai/so quanh ban."""
    out = ['<div class="cb">']
    for r in range(8, 0, -1):
        out.append('<i>%s</i>' % (r if coords else ""))
        for f in FILES:
            sq = f + str(r)
            v = pieces.get(sq)
            cls = "l" if light(sq) else "d"
            txt = ""
            if v == "o":
                cls += " coin"
            elif v == "p":
                cls += " tgt"
            elif v:
                cls += " pc " + ("me" if v.isupper() else "op")
                txt = GLYPH[v]
            out.append('<b class="%s">%s</b>' % (cls, txt))
    out.append("<i></i>")
    out.extend('<i>%s</i>' % (c if coords else "") for c in FILES)
    out.append("</div>")
    return "".join(out)


# ---------------------------------------------------------------- dung trang
def li(items):
    return "".join("<li>%s</li>" % x for x in items)


def rows(pairs):
    return "".join("<tr><td>%s</td><td>%s</td></tr>" % p for p in pairs)


def session_page(s):
    warn = ""
    if s.get("warn"):
        warn = '<p class="warn">⚠ %s</p>' % s["warn"]
    return """
<article class="page">
  <header class="ph">
    <span class="pn">BUỔI %(n)d</span>
    <h2>%(title)s</h2>
    <p class="done"><b>“Xong” trông như thế nào:</b> %(done)s</p>
  </header>
  <div class="cols">
    <div class="left">
      <h3>Bày bàn</h3>
      %(board)s
      <p class="setup">%(setup)s</p>
      <h3>Ôn cho người lớn — trước khi gọi bé</h3>
      <ul class="prep">%(prep)s</ul>
      %(warn)s
    </div>
    <div class="right">
      <h3>Lời thoại gợi ý</h3>
      <ol class="lines">%(lines)s</ol>
    </div>
  </div>
  <div class="cols bot">
    <div>
      <h3>Sửa lỗi — giao thức 1-nước</h3>
      <table><tbody>%(fix)s</tbody></table>
    </div>
    <div>
      <h3>Điều kiện dừng sớm</h3>
      <table><tbody>%(stop)s</tbody></table>
    </div>
  </div>
  <footer class="pf">
    <span>Số phút thực: <b>____</b></span>
    <span>Lý do dừng: hết nội dung / 1 tín hiệu / 2 tín hiệu / hết 15 phút</span>
    <span>Bé đòi chơi thêm? <b>C / K</b></span>
  </footer>
</article>""" % {
        "n": s["n"],
        "title": s["title"],
        "done": s["done"],
        "board": draw(BOARDS[s["n"]], coords=True),
        "setup": SETUP_NOTE[s["n"]],
        "prep": li(s["prep"]),
        "lines": li(s["lines"]),
        "fix": rows(s["fix"]),
        "stop": rows(s["stop"]),
        "warn": warn,
    }


def setup_cards():
    """6 the bay ban nho, cat roi, kep vao the A5 (R1)."""
    cards = []
    for n in range(1, 7):
        cards.append(
            '<div class="scard"><span class="sn">BUỔI %d</span>%s<p>%s</p></div>'
            % (n, draw(BOARDS[n], coords=True), SETUP_NOTE[n])
        )
    return "".join(cards)


def tracker():
    cells = "".join(
        '<div class="tc"><span>%d</span></div>' % i for i in range(1, 31)
    )
    return '<div class="track">%s</div>' % cells


CSS = """
@page { size: A4; margin: 12mm 10mm; }
* { box-sizing: border-box; }
body {
  margin: 0; background: #fff; color: #000;
  font-family: "Segoe UI", Roboto, Arial, sans-serif; font-size: 9.6pt; line-height: 1.42;
}
h2, h3 { font-family: Georgia, "Times New Roman", serif; margin: 0; }
.page { page-break-after: always; break-after: page; }
.page:last-child { page-break-after: auto; }

.ph { border-bottom: 2px solid #000; padding-bottom: 5pt; margin-bottom: 8pt; }
.pn { font-family: Consolas, monospace; font-size: 8pt; letter-spacing: .14em; color: #b8232c; }
.ph h2 { font-size: 17pt; line-height: 1.1; margin: 2pt 0 4pt; }
.done { margin: 0; font-size: 9pt; }

.cols { display: flex; gap: 9mm; align-items: flex-start; }
.cols > div { flex: 1; min-width: 0; }
.cols .left { flex: 0 0 62mm; }
.bot { margin-top: 7pt; border-top: 1px solid #bbb; padding-top: 6pt; }
h3 {
  font-family: Consolas, monospace; font-size: 7.6pt; letter-spacing: .12em;
  text-transform: uppercase; color: #b8232c; margin: 7pt 0 4pt;
}
.cols .left h3:first-of-type, .cols .right h3:first-of-type { margin-top: 0; }

/* ban co */
.cb {
  display: grid; grid-template-columns: 4mm repeat(8, 1fr);
  grid-template-rows: repeat(8, 1fr) 4mm; width: 56mm;
}
.cb i {
  font-style: normal; font-family: Consolas, monospace; font-size: 5.4pt; color: #777;
  display: flex; align-items: center; justify-content: center;
}
.cb b {
  aspect-ratio: 1/1; display: flex; align-items: center; justify-content: center;
  font-weight: 400; position: relative; border: .2pt solid #999;
}
.cb b.l { background: #fff; }
.cb b.d { background: #c4c4c4; }
.cb b.pc { font-family: Georgia, serif; font-weight: 700; font-size: 8.4pt; }
.cb b.me { color: #b8232c; }
.cb b.coin::after {
  content: ""; position: absolute; width: 42%; aspect-ratio: 1;
  border-radius: 50%; background: #b8232c;
}
.cb b.tgt::after {
  content: ""; position: absolute; width: 42%; aspect-ratio: 1;
  border-radius: 50%; border: .7pt solid #000;
}
.setup { font-size: 8.2pt; color: #444; margin: 4pt 0 0; }

ul, ol { margin: 0; padding-left: 13pt; }
li { margin-bottom: 3.4pt; }
.prep li { font-size: 8.8pt; }
.lines li { margin-bottom: 5pt; }
.warn {
  border-left: 2pt solid #b8232c; padding: 3pt 0 3pt 6pt; margin: 6pt 0 0;
  font-size: 8.4pt; font-weight: 600;
}
table { width: 100%; border-collapse: collapse; font-size: 8.4pt; }
td { border-bottom: .4pt solid #ccc; padding: 2.6pt 3pt; vertical-align: top; }
td:first-child { width: 38%; color: #444; }

.pf {
  margin-top: 8pt; border-top: 2px solid #000; padding-top: 4pt;
  display: flex; justify-content: space-between; gap: 5mm;
  font-family: Consolas, monospace; font-size: 7.4pt;
}

/* the A5 */
.a5page { display: flex; flex-direction: column; gap: 6mm; }
.a5 { border: .6pt dashed #888; padding: 6mm; }
.a5 h4 {
  font-family: Consolas, monospace; font-size: 7.4pt; letter-spacing: .13em;
  text-transform: uppercase; color: #b8232c; margin: 0 0 4pt;
}
.a5 dl { display: grid; grid-template-columns: 15mm 1fr; gap: 2pt 4mm; margin: 0; font-size: 9pt; }
.a5 dt { font-family: Georgia, serif; font-weight: 700; }
.a5 dd { margin: 0; }
.a5 .sub { margin-top: 5pt; padding-top: 4pt; border-top: .4pt solid #ccc; }
.cut { text-align: center; font-family: Consolas, monospace; font-size: 6.6pt; color: #999; }
.golden {
  text-align: center; font-family: Georgia, serif; font-style: italic; font-size: 10pt;
  border-top: 1pt solid #000; border-bottom: 1pt solid #000; padding: 4pt 0; margin-top: 5pt;
}
.sigbox { display: flex; gap: 4mm; margin-top: 4pt; }
.sigbox div { flex: 1; border: .4pt solid #999; padding: 3pt 4pt; font-size: 8pt; }
.sigbox b { color: #b8232c; }

/* the bay ban cat roi */
.scards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 5mm; }
.scard { border: .6pt dashed #888; padding: 4mm; text-align: center; }
.scard .sn {
  display: block; font-family: Consolas, monospace; font-size: 7.4pt;
  letter-spacing: .12em; color: #b8232c; margin-bottom: 3pt;
}
.scard .cb { width: 42mm; margin: 0 auto; }
.scard p { font-size: 7.4pt; color: #444; margin: 3pt 0 0; text-align: left; }

/* bang theo doi */
.track { display: grid; grid-template-columns: repeat(6, 1fr); gap: 3mm; margin-top: 5mm; }
.tc {
  border: .8pt solid #000; aspect-ratio: 1; display: flex;
  align-items: flex-start; justify-content: flex-start;
}
.tc span { font-family: Consolas, monospace; font-size: 7pt; color: #999; padding: 1.5mm; }
.intro { font-size: 9pt; color: #444; max-width: 150mm; }
@media screen {
  body { background: #eee; padding: 8mm; }
  .page { background: #fff; padding: 12mm; margin: 0 auto 8mm; max-width: 210mm; box-shadow: 0 1px 4px rgba(0,0,0,.2); }
}
"""

A5_PAGE = """
<article class="page a5page">
  <header class="ph">
    <span class="pn">IN RỒI CẮT · ĐỂ CẠNH BÀN CỜ VĨNH VIỄN</span>
    <h2>Thẻ A5 “trọng tài”</h2>
    <p class="done">Giáo trình tự chứa. <b>Không đọc lại file dài mỗi buổi.</b></p>
  </header>

  <div class="a5">
    <h4>Mặt trước — cách đi quân</h4>
    <dl>
      <dt>XE</dt><dd>↑↓←→ thẳng, không chéo</dd>
      <dt>TƯỢNG</dt><dd>⤢⤡ chéo, <b>giữ nguyên màu ô mãi mãi</b></dd>
      <dt>HẬU</dt><dd>Xe + Tượng gộp lại</dd>
      <dt>VUA</dt><dd>1 ô, mọi hướng</dd>
      <dt>MÃ</dt><dd>chữ L, <b>NHẢY QUA</b> đầu quân</dd>
      <dt>TỐT</dt><dd>đi thẳng 1 ô · <b>ĂN CHÉO</b> (khác cách đi!) · nước đầu 2 ô · tới cuối bàn → lên Hậu</dd>
    </dl>
    <div class="sub">
      <b>Bày bàn:</b> Ô TRẮNG GÓC PHẢI · HẬU ĐỨNG Ô CÙNG MÀU<br>
      <b style="color:#b8232c">✗ HOÃN en passant — không dạy trong 30 buổi</b>
    </div>
  </div>

  <p class="cut">✂ — — — — — — — — — — — — — — — — — — — — — — — — — — — — — —</p>

  <div class="a5">
    <h4>Mặt sau — luật + quy tắc dừng</h4>
    <dl>
      <dt>THOÁT CHIẾU</dt><dd>1. Vua chạy · 2. Chắn bằng quân khác · 3. Ăn quân đang chiếu</dd>
      <dt>NHẬP THÀNH</dt><dd>Vua + Xe đó <b>chưa từng đi</b> · không có quân ở giữa · Vua <b>không đang</b> bị chiếu · Vua không <b>đi qua</b> và không <b>đến</b> ô bị kiểm soát</dd>
      <dt>HẾT / HÒA</dt><dd>Vua bí mà <b>KHÔNG</b> bị chiếu = <b>HÒA</b>, không phải thắng</dd>
    </dl>
    <div class="sub">
      <b style="color:#b8232c">QUY TẮC 3 TÍN HIỆU</b>
      <div class="sigbox">
        <div><b>S1</b> rời mắt &gt;5 giây, 2 lần liền</div>
        <div><b>S2</b> đi bừa 2 nước liền</div>
        <div><b>S3</b> nói “không muốn” / chơi quân như đồ chơi</div>
      </div>
      <table style="margin-top:4pt">
        <tbody>
          <tr><td><b>1 tín hiệu</b></td><td>Trò tay 60–90 giây → quay lại <b>đúng 1 lần</b> → tối đa <b>+3 phút</b> rồi dừng</td></tr>
          <tr><td><b>2 tín hiệu</b></td><td><b>DỪNG NGAY.</b> Cho bé 1 nước thắng dễ + 1 câu khen cụ thể. Không giảng thêm</td></tr>
          <tr><td><b>3 tín hiệu / khóc</b></td><td>Dừng, <b>bỏ nội dung buổi đó</b>, KHÔNG tính là buổi đã hoàn thành</td></tr>
          <tr><td><b>Hết 15 phút</b></td><td>Bé vẫn muốn → <b>VẪN DỪNG.</b> “Mai chơi tiếp nhé”</td></tr>
        </tbody>
      </table>
      <p class="golden">Dừng lúc bé còn muốn chơi,<br>không dừng lúc bé đã hết muốn.</p>
    </div>
  </div>
</article>"""


def build():
    verify()

    parts = [A5_PAGE]

    parts.append("""
<article class="page">
  <header class="ph">
    <span class="pn">CẮT RỜI · KẸP VÀO THẺ A5 TRƯỚC MỖI BUỔI</span>
    <h2>Sáu thế bày bàn</h2>
    <p class="done">Bàn cờ được cất đi sau mỗi buổi (R1), nên <b>bày sẵn thế từ tối trước là không làm được</b>. Thay bằng: kẹp tấm thế của buổi kế tiếp vào thẻ A5. Mục tiêu <b>bày xong ≤60 giây</b>.</p>
  </header>
  <div class="scards">%s</div>
  <p class="warn">Toạ độ chỉ để người lớn đọc sơ đồ. <b>Không bao giờ nói toạ độ với bé</b> — ký hiệu bàn cờ là non-goal.</p>
</article>""" % setup_cards())

    parts.extend(session_page(s) for s in SESSIONS)

    parts.append("""
<article class="page">
  <header class="ph">
    <span class="pn">DÁN TỦ LẠNH · BÉ TỰ TÔ</span>
    <h2>Bảng theo dõi 30 buổi</h2>
    <p class="done">Bé tô một ô sau mỗi buổi. Biến bé thành <b>người đồng sở hữu tiến độ</b> thay vì đối tượng bị dạy.</p>
  </header>
  <p class="intro">Ghi <b>3 con số</b> sau mỗi buổi (15 giây, không bỏ): số phút thực · lý do dừng · bé có đòi chơi thêm không.
  Đây là dữ liệu để viết Phase 2 — không có nó thì Phase 2 phải viết theo tưởng tượng.</p>
  %s
  <p class="warn" style="margin-top:6mm">Ngày bận: <b>buổi tối thiểu 3 phút</b>, 1 trò cũ, không nội dung mới — vẫn tô ô, ghi là “ngày duy trì” (≤8 ngày). Nghỉ 2 ngày liền → ngày thứ 3 <b>bắt buộc</b> làm buổi tối thiểu.</p>
</article>""" % tracker())

    html = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<title>Cờ vua buổi 1–6 — bộ in</title>
<style>%s</style>
</head>
<body>
%s
</body>
</html>
""" % (CSS, "\n".join(parts))

    io.open(OUT, "w", encoding="utf-8", newline="").write(html)
    print("Da tao %s (%.1f KB)" % (os.path.basename(OUT), len(html.encode()) / 1024))
    print("  1 trang the A5 (2 mat, co duong cat)")
    print("  1 trang 6 the bay ban cat roi")
    print("  6 trang kich ban, moi buoi 1 trang")
    print("  1 trang bang theo doi 30 o")
    print("Tat ca %d the co da qua tu kiem." % len(BOARDS))


if __name__ == "__main__":
    build()
