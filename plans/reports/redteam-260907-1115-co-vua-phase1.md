# Red-team: giáo trình 30 buổi cờ vua — Phase 1

Ngày: 2026-09-07 · Vai: hostile verifier (HLV cờ + thực hành phát triển trẻ)
Nguồn khoá: `plans/reports/advise-260907-0854-co-vua-30-ngay.md`
Bị soi: `plans/260907-0938-co-vua-30-buoi/plan.md` + 6 file `phase-*.md`
Thiết kế LOCKED — không đề xuất redesign. Không sửa file nào.

Ground truth dùng để kiểm: ô sáng ⇔ (file_index + rank) lẻ với a=1..h=8. a1 TỐI, h1 SÁNG.
Mọi sơ đồ đã kiểm bằng cách dựng lại độc lập (script Python: màu ô, đường đi, block, thứ tự ăn, BFS số nước tối thiểu). Không tin nhãn tự ghi trong plan.

---

## Tổng kết

| Mức | Số |
|---|---|
| BLOCKER | **3** |
| MAJOR | 5 |
| MINOR | 6 |

3 BLOCKER đều ở PRIORITY A (sơ đồ bàn cờ), đều ở phase-01, đều làm hỏng đúng buổi mà chúng nằm trong: buổi 3 và buổi 5 sai số nước tối thiểu, buổi 6 ván kết thúc ở nước 1.

---

# PRIORITY A — Kiểm từng sơ đồ bằng tay

## A1. BUỔI 1 — lưới ô màu (phase-01 dòng 155–167) — **ĐÚNG**

Kiểm cả 64 ô, đối chiếu từng ô với công thức. **0 sai lệch.**
- Hàng 8 `□■□■□■□■` → a8 sáng ✓ (a=1, rank=8, 1+8=9 lẻ = sáng)
- Hàng 1 `■□■□■□■□` → a1 TỐI ✓, h1 SÁNG ✓
- Alternation dọc/ngang đúng toàn bộ, 8 cột × 8 hàng, không thiếu/thừa.
- Mũi tên `↑ ô trắng phải ở đây` đặt dưới cột h, hàng 1 → chỉ đúng h1 = SÁNG. Khớp lời "ô trắng ở góc phải dưới".

Không có finding.

## A2. BUỔI 2 — Xe d4 + 5 xu (phase-01 dòng 234–249) — **ĐÚNG về hình học, SAI con số ẩn**

Kiểm từng xu so với d-file / rank-4:
| Xu | Cùng cột d? | Cùng hàng 4? | Kết |
|---|---|---|---|
| d7 | ✓ | – | hợp lệ |
| a4 | – | ✓ | hợp lệ |
| h4 | – | ✓ | hợp lệ |
| d1 | ✓ | – | hợp lệ |
| **g4** | – | ✓ | **hợp lệ** |

g4 (nghi vấn trong yêu cầu review) hợp lệ: cùng hàng 4 với d4. Cả 5 xu đều thoả "cùng hàng hoặc cùng cột".

Lưới ASCII: hàng 4 in `o . . X . . o o` = a4, d4(X), g4, h4 ✓. Hàng 7 `. . . o` = d7 ✓. Hàng 1 `. . . o` = d1 ✓. Khớp prose hoàn toàn.

Thế thay thế lượt 2 (Xe e2; xu e6, a2, h2, e8, c2): e6 ✓ cột e · a2 ✓ hàng 2 · h2 ✓ hàng 2 · e8 ✓ cột e · c2 ✓ hàng 2. **Đúng cả 5.**

→ Xem **M1** (số nước tối thiểu thực tế) ở phần MAJOR.

## A3. BUỔI 3 — Xe a1 + 5 Tốt bia (phase-01 dòng 312–326) — **ĐÚNG**

Đường đi plan tuyên bố: `a1→a5 · a5→d5 · d5→d1 · d1→h1 · h1→h5`.

Mô phỏng có xoá quân đã ăn theo thứ tự:

| # | Nước | Hợp lệ Xe? | Quân chắn tại thời điểm đi | Ăn |
|---|---|---|---|---|
| 1 | a1→a5 | ✓ dọc cột a | a2,a3,a4 trống | a5 ✓ |
| 2 | a5→d5 | ✓ ngang hàng 5 | b5,c5 trống | d5 ✓ |
| 3 | d5→d1 | ✓ dọc cột d | d4,d3,d2 trống | d1 ✓ |
| 4 | d1→h1 | ✓ ngang hàng 1 | e1,f1,g1 trống | h1 ✓ |
| 5 | h1→h5 | ✓ dọc cột h | h2,h3,h4 trống | h5 ✓ |

**5 nước, không nước nào bị chắn, ăn đủ 5/5.** Tuyên bố của plan đúng.

BFS xác nhận **5 là số nước tối thiểu thật** (không có lời giải 4 nước). Thêm: có **4** đường 5-nước khác nhau, không chỉ 1 — thiết kế khoan dung, tốt cho bé:
- `a1→a5→d5→d1→h1→h5` (bản in trong plan)
- `a1→a5→d5→h5→h1→d1`
- `a1→d1→d5→a5→h5→h1`
- `a1→d1→h1→h5→d5→a5`

Lưới ASCII khớp prose: hàng 5 `p . . p . . . p` = a5,d5,h5 ✓; hàng 1 `X . . p . . . p` = a1(X),d1,h1 ✓.

→ Nhưng tiêu chí "xong" ≤6 nước có vấn đề: xem **B1** (BLOCKER).

## A4. BUỔI 5 — Tượng c1 + 5 xu (phase-01 dòng 461–475) — **BLOCKER**

**Màu ô — plan ĐÚNG.** c1 = TỐI (c=3, rank=1, 3+1=4 chẵn). Cả 5 xu TỐI:

| Ô | file+rank | Màu |
|---|---|---|
| c1 (Tượng) | 3+1=4 chẵn | TỐI ✓ |
| a3 | 1+3=4 | TỐI ✓ |
| e3 | 5+3=8 | TỐI ✓ |
| g5 | 7+5=12 | TỐI ✓ |
| d4 | 4+4=8 | TỐI ✓ |
| f2 | 6+2=8 | TỐI ✓ |

**Nhưng REACHABILITY hỏng.** Cùng màu là điều kiện cần, không đủ — và ở đây nó không đủ thật:

| Xu | Trên đường chéo trực tiếp từ c1? |
|---|---|
| a3 | ✓ (c1-b2-a3) |
| e3 | ✓ (c1-d2-e3) |
| g5 | ✓ nhưng **e3 chắn** đường c1-d2-e3-f4-g5 |
| **d4** | **✗ KHÔNG cùng đường chéo với c1** (cần 2 nước) |
| **f2** | **✗ KHÔNG cùng đường chéo với c1** (cần 2 nước) |

Vét cạn toàn bộ 120 thứ tự: **0 thứ tự nào ăn hết 5 xu trong 5 nước.** BFS cho số nước tối thiểu thật = **6**, không phải 5.

Hệ quả tại bàn: bé đi hết các xu "1 nước tới" rồi mắc kẹt trước d4/f2, phải đi một nước **không ăn gì** — đúng cái mà buổi 5 chưa dạy (bé mới học "đi chéo là tới xu"). Chính xác là kịch bản mà cảnh báo `⚠` ở dòng 475 và hàng "Bé nản vì không tới được xu" (dòng 521) đang cố phòng — nhưng cảnh báo chỉ bảo kiểm **màu ô**, mà màu ô thì đúng. **Cảnh báo được viết ra sẽ pass, còn thế cờ vẫn hỏng.** Phụ huynh làm đúng hướng dẫn vẫn dính lỗi.

Ghi nhận giảm nhẹ: quét toàn bộ cây trạng thái → **0 dead-end** (không có thứ tự nào làm xu còn lại thành bất khả thi). Nên đây là "khó hơn công bố + phá cảnh báo tự kiểm", không phải "không giải được".

**FIX (toạ độ cụ thể).** Giữ Tượng `c1`, giữ `a3`, `e3`, `g5`; thay `d4`→`c5`, `f2`→`b2`:

```
Tượng trắng c1 (ô ĐEN). 5 xu, tất cả ô ĐEN: a3, b2, c5, e3, g5

   a  b  c  d  e  f  g  h
8  .  .  .  .  .  .  .  .
7  .  .  .  .  .  .  .  .
6  .  .  .  .  .  .  .  .
5  .  .  o  .  .  .  o  .
4  .  .  .  .  .  .  .  .
3  o  .  .  .  o  .  .  .
2  .  o  .  .  .  .  .  .
1  .  .  T  .  .  .  .  .
```

Đã kiểm: cả 5 xu ô TỐI; tồn tại đúng **1** đường 5 nước, mỗi nước ăn 1 xu, không nước nào bị chắn:
`c1 → b2 → a3 → c5 → e3 → g5`

Cảnh báo: bộ này chỉ có **1** thứ tự đúng → kém khoan dung hơn buổi 3 (4 đường). Vét cạn toàn bộ 5-xu-cùng-màu-tối từ c1: **không tồn tại** bộ nào vừa trải rộng (≥3 đường chéo khác nhau) vừa có ≥3 thứ tự đúng. Phải chọn 1 trong 2:
- **(a)** giữ bộ trên, và **sửa tiêu chí buổi 5** thành "ăn hết trong ≤7 nước" (cho bé đi nước trống); hoặc
- **(b)** dùng bộ khoan dung nhất — 6 thứ tự đúng, nhưng cả 5 xu nằm trên **một đường chéo**: `c5, d4, e3, f2, g1`. Bé chỉ trượt một mạch xuống chéo → quá dễ, và không dạy được "chéo có 2 hướng".

Khuyến nghị **(a)**. Buổi 5 không có tiêu chí đếm nước ("xong" = bé tự nói được màu ô), nên nới số nước không đụng nghiệm thu.

## A5. BUỔI 6 — Xe+Tượng hai bên (phase-01 dòng 543–557) — **BLOCKER**

**Màu Tượng — plan ĐÚNG.** c2 = 3+2 = 5 lẻ = **SÁNG**. f7 = 6+7 = 13 lẻ = **SÁNG**. Hai Tượng **cùng màu** ✓ → gặp nhau được, kết luận của plan đúng.

⚠ Nhưng **nhãn sai**: dòng 555 ghi *"Tượng của bé ở `c2` (**ô đen**), Tượng người lớn ở `f7` (**ô đen**)"*. Cả hai đều là ô **TRẮNG/SÁNG**. Kết luận (cùng màu) đúng, tiền đề (đen) sai. Phụ huynh cầm thẻ A5 làm bước "⚠ kiểm tra trước khi gọi bé" theo kiểu buổi 5 sẽ thấy màu không khớp và tự "sửa" thành thế sai.

**Lỗi thật — ván kết thúc ở nước 1.** Thế bày: bé Tượng `c2` + Xe `f2`; người lớn Xe `c7` + Tượng `f7`.

| Bên | Quân | Ăn được gì ngay nước 1 |
|---|---|---|
| **Bé** | Xe f2 | **f2×f7 ăn Tượng người lớn** — cột f, f3–f6 trống |
| Người lớn | Xe c7 | **c7×c2 ăn Tượng của bé** — cột c, c3–c6 trống |

Bé đi trước (dòng 557) → **bé ăn ngay Tượng đối phương ở nước 1**. Cân đối vỡ ngay lập tức: bé 2 quân vs người lớn 1 quân, luật thắng là "ăn sạch quân đối phương".

Đây là **đúng cái bẫy mà chính plan đã tự cảnh báo và tự tin là đã tránh** — dòng 381 (buổi 4): *"nếu 2 Xe khởi đầu cùng hàng hoặc cùng cột, người đi trước ăn luôn — ván kết thúc ở nước 1, bé không học gì"*. Cảnh báo được nêu ở buổi 4, được tuân thủ ở buổi 4, rồi **vi phạm ở buổi 6** — nơi nó còn quan trọng hơn vì buổi 6 là **cửa nghiệm thu Phase 1** ("chơi trọn 1 ván"). Ván 1 nước thì tiêu chí "chơi trọn 1 ván, không phải nhắc cách đi quân" không đo được gì.

Xấu thêm: nếu người lớn (đúng chỉ tiêu thua 2/3) không ăn lại, bé học được rằng "cứ chộp là thắng" — ngược mục tiêu buổi 4 vừa dạy hôm kia.

**FIX (toạ độ cụ thể).** Giữ Tượng bé `c2`, đổi Xe bé `f2`→`e2`; giữ Tượng người lớn `f7`, đổi Xe người lớn `c7`→`b7`:

```
Bé: Tượng c2 + Xe e2   ·   Người lớn: Tượng f7 + Xe b7

   a  b  c  d  e  f  g  h
8  .  .  .  .  .  .  .  .
7  .  X  .  .  .  T  .  .   ← Xe + Tượng người lớn
6  .  .  .  .  .  .  .  .
5  .  .  .  .  .  .  .  .
4  .  .  .  .  .  .  .  .
3  .  .  .  .  .  .  .  .
2  .  .  T  .  X  .  .  .   ← Tượng + Xe của bé
1  .  .  .  .  .  .  .  .
```

Đã kiểm bằng vét cạn 4 quân × mọi mục tiêu:
- c2 và f7 **cùng màu** (cả hai SÁNG) → hai Tượng vẫn gặp được nhau ✓
- **Không quân nào của bên nào ăn được quân nào ở nước 1** (không cùng hàng/cột/chéo thông thoáng) ✓

Kèm theo: **sửa dòng 555** từ "(ô đen)" → "(ô trắng)" cho cả c2 và f7. Nếu muốn giữ nguyên chữ "ô đen" thì phải dời cả cặp Tượng sang ô tối (vd bé `b2`, người lớn `g7`) — nhưng đổi Xe rẻ hơn.

## A6. BUỔI 4 — Xe b2 vs Xe g7 (phase-01 dòng 386–400) — **ĐÚNG**

- b2: cột b, hàng 2. g7: cột g, hàng 7. **Khác cột (b≠g), khác hàng (2≠7)** ✓ → không ai ăn được ở nước 1. Tuyên bố của plan đúng.
- Thế thay thế ván 2: c3 / f6 → khác cột (c≠f), khác hàng (3≠6) ✓ **đúng**.
- Lưới ASCII: hàng 7 `. . . . . . X .` = g7 ✓ · hàng 2 `. X . . . . . .` = b2 ✓. Khớp prose.
- Chú thích màu: không tuyên bố màu ô → không có gì sai được. (FYI b2, g7, c3, f6 đều TỐI — vô hại ở buổi này.)

Không có finding.

---

# BLOCKER

### B1 — Buổi 3: tiêu chí "≤6 nước" mâu thuẫn giữa nguồn khoá và câu chốt (phase-01: 302, 326, 347, 610)

Ba con số đá nhau trong cùng một buổi:
- Dòng 302 "Xong": **≤6 nước** (khớp nguồn mục 5.2 dòng 131 ✓)
- Dòng 312: *"bố trí để ăn hết đúng **5–6 nước**"*
- Dòng 326: đường tối ưu **5 nước** ← đã verify là tối ưu thật
- Dòng 347 câu chốt: *"Con dọn sạch bàn trong **6 nước**"*

Câu chốt in cứng "6 nước" là câu phụ huynh **đọc ra miệng**, trong khi thế cờ giải được trong 5 và bé có 4 đường 5-nước để tìm ra. Bé đi 5 nước, phụ huynh vẫn đọc "6 nước" → khen sai sự thật, và vi phạm chính luật của plan là **khen phải cụ thể và đúng** (dòng 215–218: "❌ chung chung"). Khen sai còn tệ hơn khen chung chung: bé 5 tuổi biết đếm tới 6.

**FIX:** câu chốt dòng 347 → *"Con dọn sạch bàn hết bàn trong **___ nước**. Xe của con làm việc nhanh ghê."* — điền số thật. Và dòng 312 sửa "5–6 nước" → "**5 nước nếu đi tối ưu, 6 vẫn đạt**" cho khớp tiêu chí ≤6.

### B2 — Buổi 5: thế Tượng không giải được trong 5 nước; cảnh báo tự kiểm bị vô hiệu (phase-01: 461–475)

Chi tiết + toạ độ sửa: **A4** ở trên. Tóm: `d4` và `f2` không nằm trên đường chéo nào của `c1`; min = 6 nước, không phải 5. Cảnh báo dòng 475 chỉ kiểm màu ô → **pass trong khi thế vẫn hỏng**. Phụ huynh làm đúng 100% hướng dẫn vẫn gặp bé nản.
**FIX:** đổi 2 xu → `a3, b2, c5, e3, g5` (đã verify: toàn ô tối, đường 5 nước tồn tại: `c1→b2→a3→c5→e3→g5`), + nới trần nước lên ≤7 (buổi 5 không đếm nước trong tiêu chí "xong").

### B3 — Buổi 6: bé ăn Tượng đối phương ngay nước 1; nhãn màu ô sai (phase-01: 543–557)

Chi tiết + toạ độ sửa: **A5** ở trên. Tóm: Xe bé `f2` ăn thẳng Tượng người lớn `f7` (cột f thông); Xe người lớn `c7` ăn thẳng Tượng bé `c2`. Bé đi trước → ván xong ở nước 1. Vi phạm đúng cảnh báo mà plan tự viết ở dòng 381. Buổi 6 là **cửa nghiệm thu Phase 1** → nghiệm thu không đo được.
**FIX:** Xe bé `f2`→`e2`, Xe người lớn `c7`→`b7` (đã verify: 0 nước-1-capture, hai Tượng vẫn cùng màu). Sửa dòng 555: c2/f7 là ô **TRẮNG**, không phải "ô đen".

---

# MAJOR

### M1 — Buổi 2: "10/10 nước đi đúng" không đo được với thế 5 xu (fidelity + executability)

Tiêu chí "xong" = **10/10 nước** (dòng 224, khớp nguồn ✓). Nhưng thế bày cho 5 xu, và số nước tối thiểu thật = **6** (BFS, cả lượt 1 lẫn lượt thay thế e2). Một lượt sinh ra ~6–8 nước, không phải 10. Để có 10 nước quan sát được, phụ huynh **bắt buộc phải chơi ≥2 lượt** — plan có nói "2–3 lượt" ở khung chung (dòng 120) nhưng **buổi 2 không nói rõ 10 nước là cộng dồn qua các lượt**.

Rủi ro thật: phụ huynh chơi 1 lượt, thấy 6/6 đúng, tick "xong" — nghiệm thu Phase 1 dòng 610 (`10/10 nước Xe`) đánh dấu đạt trên 6 quan sát. Ngưỡng bị làm loãng lặng lẽ.

**FIX:** dòng 224 → *"10/10 nước đi đúng, **cộng dồn qua 2–3 lượt** (mỗi lượt ~6 nước)"*.

### M2 — Câu chốt buổi 2 dạy tối ưu hoá, xung đột luật "không giảng" (phase-01: 269)

> "6 nước! Lượt sau mình thử ít hơn được không?"

Số nước tối thiểu thật là **6**. Câu này mời bé làm việc **bất khả thi** — và bé sẽ thử, thất bại, ở đúng buổi thứ hai của cả chương trình. Cùng câu đó ở buổi 3 (dòng 343) thì **hợp lệ** vì bé thường đi 8 nước còn tối ưu là 5, có chỗ để cải thiện thật.

**FIX:** buổi 2 đổi thành câu không hứa cải thiện: *"6 nước! Lượt sau mình chơi thế khác nhé."* Giữ nguyên câu "thử ít hơn" ở buổi 3.

### M3 — plan.md trỏ tới `plan.html` không tồn tại, và gọi nó là "Artifact chính" (plan.md: 15–16)

```
> **Artifact chính:** [`plan.html`](./plan.html) — ... có sơ đồ, mockup thẻ A5 và modal chi tiết từng buổi.
> File `plan.md` này là bản chỉ mục ngắn.
```

Kiểm: **không có file `.html` nào trong repo.** Thư mục plan chỉ có `plan.md` + 6 `phase-*.md` + `.claude/`.

Hai hệ quả: (1) link chết; (2) plan.md tự hạ cấp mình thành "chỉ mục ngắn" và đẩy quyền authority sang một file không tồn tại. Phụ huynh đọc dòng 15 sẽ đi tìm bản HTML "dễ đọc" và không thấy gì.

**FIX:** hoặc bỏ block 15–16, hoặc tạo `plan.html`. Nếu tạo: nó **sẽ chứa lại các sơ đồ** → phải mang theo cả 3 fix BLOCKER, nếu không sẽ có 2 nguồn sơ đồ mâu thuẫn (một sai). Khuyến nghị: **bỏ dòng 15–16**, giữ plan.md là nguồn duy nhất. Rẻ hơn và loại được rủi ro sơ đồ phân đôi.

### M4 — Metric "≤1 đợt nghỉ 3 ngày" bị bỏ khỏi Success Criteria của plan.md (nguồn mục 8 dòng 356)

Nguồn khoá liệt kê 4 metric cho Mục tiêu 2. plan.md dòng 82–83 chỉ mang sang 3:

| Nguồn mục 8 | plan.md Success Criteria |
|---|---|
| ≥4 lần bé tự đòi chơi trong 7 ngày cuối | ✓ dòng 82 |
| Sau ván mốc bé đòi chơi tiếp = Có | ✓ dòng 82 |
| ≤20% buổi dừng sớm (≤6/30) | ✓ dòng 83 |
| **Số đợt "nghỉ 3 ngày" phải kích hoạt: ≤1** | **THIẾU** |

Không phải metric vụn: nó là **tín hiệu cảnh báo sớm** cho leo thang 5.3 bậc 3 (2 đợt nghỉ 3 ngày → nghỉ 2 tuần → có thể dừng chương trình). Bỏ nó ra khỏi checklist nghiệm thu = mất cái đếm quyết định "dừng hay tiếp". Càng nặng vì **R2 đã chấp nhận không có HLV dự bị** — chính chỗ cần đo đứt mạch nhất.

phase-01 dòng 634 có nhắc *cơ chế* (≥3 buổi dừng sớm → nghỉ 3 ngày) nhưng không có *metric đếm số đợt*. Cơ chế ≠ chỉ số nghiệm thu.

**FIX:** thêm vào plan.md Success Criteria: `- [ ] Số đợt "nghỉ 3 ngày" phải kích hoạt: ≤1`.

### M5 — Luật "người lớn cố tình đi sai" bị hạ tần suất trong phase-01 (nguồn 5.4 dòng 225; plan.md 71 vs phase-01 285/537)

| Nơi | Phát biểu |
|---|---|
| Nguồn 5.4 | *"Người lớn cũng cố tình đi sai 1 nước **mỗi 2–3 buổi**"* |
| plan.md dòng 71 | *"cố tình đi sai 1 nước **mỗi 2–3 buổi**"* ✓ khớp |
| phase-01 dòng 285 | *"làm **1 lần trong Phase 1**, gợi ý buổi 4 hoặc 6"* |
| phase-01 dòng 537 | *"buổi nên dùng ... **nếu chưa dùng ở buổi 4**"* |

Phase 1 = 6 buổi. "Mỗi 2–3 buổi" → **2–3 lần** trong Phase 1. phase-01 quy định **1 lần**, và dòng 537 nói rõ nếu đã dùng ở buổi 4 thì buổi 6 thôi. Cắt 50–67% tần suất.

Đây là cơ chế được nguồn mô tả là *"cách rẻ nhất để chuyển bé từ người-bị-dạy sang người-biết-luật"* — tức nó phục vụ trực tiếp Mục tiêu 2 (bé còn muốn chơi). Cùng một luật, hai file nói hai số → phụ huynh đọc phase-01 (file thi hành) sẽ chạy con số thấp.

**FIX:** phase-01 dòng 285 → *"làm **2–3 lần** trong Phase 1 (mỗi 2–3 buổi) — gợi ý buổi 2 hoặc 3, rồi buổi 4, rồi buổi 6"*. Dòng 537 bỏ mệnh đề "nếu chưa dùng ở buổi 4".

---

# MINOR

### m1 — Buổi 3 rò rỉ luật Tốt qua cửa hậu (phase-01: 334, 353)

Kịch bản chống rò rỉ rất chặt: dòng 308 cấm giải thích, dòng 356 có câu trả lời sẵn, Risk Assessment dòng 644 có mục riêng. **Nhưng** dòng 334 viết:

> "Hôm nay Xe của con gặp mấy bạn **đứng chắn đường**."

và dòng 353: *"Trên đường đi có ai đứng không nhỉ?"*

"Đứng chắn đường" là thuộc tính của **Tốt** trong ngữ cảnh này (Tốt chặn cột). Nhẹ, và không dạy Tốt **đi** thế nào — nên MINOR, không MAJOR. Nhưng nó gieo "Tốt = vật cản", mà buổi 17 phải xây "Tốt = quân đi được". Rẻ để tránh.
**FIX:** "gặp mấy bạn **đang đứng trên bàn**" / "Trên đường đi có ai **đang đứng** không nhỉ?" — bỏ chữ "chắn".

### m2 — phase-01 vẫn ra lệnh "bàn cờ đặt cố định" như checklist cứng, mâu thuẫn R1 đã chấp nhận (phase-01: 94, 647; plan.md: 46, 100, 114–116)

plan.md ghi rõ R1: phụ huynh **bày ra khi học rồi cất** — quyết định đã chốt, kèm phương án bù (để cạnh bàn học, ≤60 giây, kẹp giấy ghi thế buổi sau vào thẻ A5).

Nhưng:
- phase-01 dòng 94 (checklist vật lý): `[ ] Bàn cờ đặt **cố định** ... — **không bao giờ cất vào hộp**`
- phase-01 dòng 647 (Risk Assessment): *"**Bàn cờ bị cất vào hộp** | Bàn không còn trên bàn thấp | ... **Đặt lại ngay**"*
- plan.md dòng 46 (Cổng chuẩn bị): `[ ] Bàn cờ đặt **cố định** ..., bày sẵn thế buổi 1`

phase-01 là file phụ huynh thực sự cầm khi chạy buổi. Dòng 94 là **ô tick không bao giờ tick được** — theo đúng quyết định đã chốt. Dòng 647 biến hành vi-đã-được-chấp-nhận thành **rủi ro cần phản ứng "đặt lại ngay"**. Checklist có ô vĩnh viễn đỏ làm hỏng chính cơ chế checklist (phụ huynh học cách bỏ qua ô không tick được), và dòng 647 mâu thuẫn trực tiếp quyết định người dùng.

Cùng lỗi này ở **HLV dự bị**: phase-01 dòng 100 `[ ] HLV dự bị đã đọc thẻ A5: ______` và plan.md dòng 48, trong khi plan.md dòng 102/118 chốt **không có HLV dự bị**. Ô thứ hai không tick được.

Và **bạn cùng tuổi**: phase-04 dòng 48–50 đặt mốc `[ ] Bé đã chơi với 1 bạn 5 tuổi ... hạn chót buổi 20` + plan.md dòng 49, trong khi R3 (plan.md 122) chốt **không có**. Ô thứ ba không tick được.

**FIX:** ở cả 3 chỗ, thay ô tick "làm điều đã bị từ chối" bằng ô tick "làm phương án bù đã ghi trong R1/R2/R3":
- dòng 94 → `[ ] Bàn cờ + hộp quân để **ngay cạnh bàn học** (không cất tủ/kệ cao) — bày xong ≤60 giây` + `[ ] Kẹp giấy ghi thế buổi sau vào thẻ A5`
- dòng 647 → tín hiệu đổi thành *"≥2 buổi bị bỏ vì ngại bày"* → phản ứng *"chuyển sang để cố định"* (đúng nguyên văn R1 dòng 116)
- dòng 100 → `[ ] Đã đọc lại R2 (không có HLV dự bị): dùng "ngày duy trì" 3 phút cho ngày bận, ghi bảng cả ngày nghỉ`
- phase-04 dòng 50 → mốc bù của R3 (người lớn thứ hai chơi 1 ván cho bé xem / anh chị em họ cuối tuần / bé "dạy lại" ông bà) + ngưỡng kiểm buổi 20 (`chỉ số tự đòi chơi <2 lần/tuần → xem lại, không cố đẩy`)
- plan.md dòng 46/48/49 sửa tương ứng cho khớp Rủi ro đã chấp nhận ngay bên dưới trong cùng file

### m3 — plan.md Cổng chuẩn bị mâu thuẫn nội bộ trong cùng một file (plan.md: 46/48/49 vs 100/102/122)

Tách riêng khỏi m2 vì đây là mâu thuẫn **trong một file**: dòng 41–49 là checklist "hoàn tất TRƯỚC buổi 1" yêu cầu bàn cố định + HLV dự bị + hẹn bạn 5 tuổi; dòng 95–124 ngay sau đó ghi cả ba là **không có, đã chấp nhận**. Người đọc tuần tự gặp yêu cầu trước, phủ định sau. Nếu Cổng chuẩn bị là "điều kiện vào Phase 1" (dòng 39) thì theo văn bản hiện tại **Phase 1 không bao giờ mở được**.
**FIX:** như m2, đồng bộ dòng 46/48/49 với R1/R2/R3.

### m4 — Buổi 4: bé đi trước cả 3 ván, mâu thuẫn chỉ tiêu thắng 60–70% (phase-01: 400, 382)

Dòng 400: *"Bé đi trước **cả 3 ván**."* Dòng 382: chỉ tiêu bé thắng **2/3**. Trong trò Xe-đấu-Xe trên bàn trống, quyền đi trước là lợi thế đáng kể. Cộng thêm dòng 432 (bé buồn → *"cho bé đi trước và người lớn thua ván tiếp theo"*) và dòng 440 (thua 2 ván → *"ván 3 người lớn **chắc chắn thua**"*), tổng hợp lại nghiêng mạnh về bé thắng gần 100% — đúng cái luật 0.6/dòng 649 cấm ("Bé thắng 100% vì người lớn nhường quá").

Không phải lỗi tính toán, là xung đột chỉ tiêu. Ở buổi 4 tác hại nhỏ (khái niệm mới, cần thắng để bám). MINOR.
**FIX:** dòng 400 → *"Bé đi trước ván 1 và 3; ván 2 người lớn đi trước"* — giữ 2/3 mà không cần nhường lộ liễu.

### m5 — Metric "≥90% nước hợp luật" thiếu điều kiện mẫu tối thiểu ở một chỗ (plan.md: 78 vs 85; nguồn dòng 345)

Nguồn: *"≥ 90% (đếm trên **tối thiểu 20 nước** của bé)"*. plan.md dòng 78 có `(đếm ≥20 nước)` ✓. phase-06 dòng 46–47 có ✓. Khớp. **Không phải finding** — ghi lại để xác nhận đã kiểm.

Cái thực sự lệch: plan.md dòng 85 gộp *"30 buổi trong ≤45 ngày; ≤8 'ngày duy trì' 3 phút; bảng ghi đủ 3 số ≥27/30 buổi"* nhưng **bỏ** metric nguồn dòng 364: *"Không có chuỗi ≥3 ngày không có buổi nào (kể cả buổi tối thiểu 3 phút), ngoài các đợt nghỉ chủ đích."* Goal #4 ở dòng 33 có nhắc "không chuỗi ≥3 ngày trống" nhưng Success Criteria (mục nghiệm thu thật) thì không.
**FIX:** thêm dòng vào Success Criteria: `- [ ] Không có chuỗi ≥3 ngày không có buổi nào, ngoài đợt nghỉ chủ đích`.

### m6 — "Tượng đen thì đen mãi mãi" áp cho Tượng ô sáng ở buổi 6 (phase-01: 456, 494, 555)

Buổi 5 dạy mẹo bằng một Tượng **ô tối** (c1) và câu chốt in đậm *"**Tượng đen thì đen mãi mãi**"*. Buổi 6 hôm sau đưa cho bé một Tượng **ô sáng** (c2 — đã verify SÁNG, xem A5), và dòng 555 lại dán nhãn nó là "ô đen".

Nếu sửa nhãn theo B3, xuất hiện khe hở sư phạm thật: bé thuộc câu "đen thì đen mãi mãi" rồi được giao Tượng trắng. Nguồn 5.2 dòng 133 phát biểu mẹo trung tính hơn ("Tượng đen thì đen mãi mãi" là ví dụ, tiêu chí là *"bé tự nói được màu ô của Tượng mình"*).
**FIX:** buổi 5 dòng 494 thêm nửa câu tổng quát hoá: *"Ơ, lạ nhỉ! Tượng đen thì đen mãi mãi. **Mà Tượng trắng thì trắng mãi mãi.** Bạn ấy không đổi màu ô bao giờ luôn."* Rồi buổi 6 dùng được cho cả hai màu.

---

# PRIORITY B — Đối chiếu fidelity với nguồn khoá

Kiểm từng dòng mục 5.2 / 5.3 / 5.4 / 5.5 / 8 so với plan.

### 30 buổi (5.2) — **khớp 30/30**
Cả 6 bảng "Khung đã chốt" trong phase-02..06 sao đúng nguyên văn nguồn: chủ đề, trò, tiêu chí "xong". Đã đối chiếu từng ô:
- Phase 2 (7–11): 3/3 · 1 lần · 3 chướng ngại · 7/8 · 5/6 ✓
- Phase 3 (12–16): 8/10 · "Mã không bị chắn" · ≤1 nước sai · trọn 1 ván · ≥11/12 ✓
- Phase 4 (17–21): "Tốt không ăn phía trước" · ra kết quả · không cần nhắc · tự đổi đúng quân · ≥11/12 ✓
- Phase 5 (22–26): 6/8 · ≤2 gợi ý · ≤2 gợi ý · 3/4 · 5/5 + ≥2 trong 4 điều kiện ✓
- Phase 6 (27–30): ván có kết quả ×3 · ≤3 lần nhắc + tự đòi chơi tiếp ✓
- Phase 1 (1–6): 2 lần liên tiếp · 10/10 · ≤6 nước · 2/3 ván · tự nói màu ô · trọn 1 ván ✓ (nhưng xem B1, M1 — tiêu chí đúng, thế cờ/câu thoại không đỡ nổi tiêu chí)

### Ngưỡng cửa 16 và 21 — **khớp**
≥11/12 ở cả hai, ở cả plan.md dòng 62/81 và phase-03 dòng 28/34 và phase-04 dòng 29/34. Luật "không cho qua cửa" giữ nguyên (phase-03 dòng 55–56). Phase 4 chỉ mở khi CỬA 1 đạt, Phase 5 chỉ mở khi CỬA 2 đạt ✓. CỬA 1 = 5 quân **chưa có Tốt** ✓ (phase-03 dòng 32), CỬA 2 = cả 6 quân ✓.

### Nhánh 5.2b — **khớp**
phase-03 dòng 34–37 sao đủ: xác định quân sai nhiều nhất → chèn 2–3 buổi chỉ quân đó → 1 trò cũ + 1 biến thể dễ → đánh lại → **trượt lần 2 dừng ở đây, kết quả hợp lệ** ✓.
phase-04 dòng 34–36 sao đủ: chỉ sai Tốt → 2 buổi Chiến tranh Tốt thuần chơi; lan sang quân khác → nghỉ 3 ngày ✓.

### Bảng 3 tín hiệu (5.3) — **khớp, đủ 5 hàng**
S1 (>5s, 2 lần liên tiếp) · S2 (đi bừa 2 nước liền) · S3 (không muốn / chơi quân như đồ chơi) ✓ (plan.md 70, thẻ A5 phase-01 66–68).
Bảng quyết định: 0 tín hiệu → tiếp · 1 tín hiệu → trò tay 60–90s + quay lại **đúng 1 lần** + tối đa **+3 phút** · 2 tín hiệu → **dừng ngay** + nước thắng dễ + khen cụ thể · hết 15 phút mà bé vẫn muốn → **vẫn dừng** ✓.
**Ghi nhận:** hàng thứ 4 của nguồn (*"3 tín hiệu, bé phản kháng hoặc khóc → dừng ngay, **bỏ luôn nội dung buổi đó**, lần sau lặp lại ở phiên bản dễ hơn, **không tính là buổi đã hoàn thành**"*) **không xuất hiện** trong plan.md dòng 70, thẻ A5 (phase-01 65–78), hay bảng "điều kiện dừng sớm" của bất kỳ buổi nào.
→ Đây là hàng có hệ quả **kế toán tiến độ** (không tính buổi = ảnh hưởng "30 buổi trong ≤45 ngày"). Thẻ A5 rút gọn 5 dòng theo nguồn thì bỏ được, nhưng plan.md dòng 70 tự nhận là *"Nguyên văn từ bản tư vấn, không sửa"* — mà thiếu 1/5 hàng. **MINOR-nghiêng-MAJOR**; xếp MINOR vì cơ chế "khóc → dừng" trong thực tế không cần nhắc, phần mất thật là quy tắc không-tính-buổi.
**FIX:** thêm vào plan.md dòng 70: *"3 tín hiệu / bé khóc → dừng, **bỏ nội dung buổi đó, không tính là buổi đã hoàn thành**, lần sau lặp bản dễ hơn."*

### Leo thang 5.3 — **khớp**
2 lần dừng sớm cùng chủ đề → chẻ buổi ✓ (phase-02 dòng 55, phase-03 dòng 54 áp dụng đúng tinh thần).
3 buổi liên tiếp dừng sớm → nghỉ trọn 3 ngày ✓ (phase-01 dòng 634 — **nhưng** ghi *"≥3 buổi trong Phase 1"*, nguồn ghi *"3 buổi **liên tiếp**"*. phase-01 chặt hơn nguồn (3 buổi bất kỳ trong 6 ≠ 3 liên tiếp). Chặt hơn = an toàn hơn, không phải làm loãng → không tính là finding, nhưng nên đồng bộ chữ "liên tiếp").
2 đợt nghỉ 3 ngày → nghỉ 2 tuần, cất thế nhưng để bàn bé thấy, không mời, điều kiện quay lại bé tự đòi / mời đúng 1 lần / từ chối → dừng 3 tháng ✓ (phase-01 dòng 657, nguyên văn).

### Giao thức sửa lỗi (5.4) — **4/5 khớp, 1 lệch (M5)**
| Luật nguồn | plan |
|---|---|
| Không dùng chữ "sai", dùng câu hỏi | ✓ plan.md 71, phase-01 108, mọi bảng sửa lỗi |
| Chỉ sửa nước VỪA đi | ✓ phase-01 202 |
| Không nói gì khi bé đang nghĩ | ✓ phase-01 203, 282 ("luật cứng") |
| Sai cùng 1 luật 3 lần → không sửa lần 4, ghi lại, trò riêng buổi sau | ✓ phase-01 204, 283, 357, 513, 590 |
| Người lớn cố tình đi sai **mỗi 2–3 buổi** | **✗ M5** — phase-01 hạ còn 1 lần/Phase 1 |

### Trần màn hình (5.5) — **khớp, đủ số**
≤10 phút/lần · ≤2 lần/tuần · tổng ≤60 phút/30 buổi ✓ (plan.md 72, phase-04 45).
Mở khoá **sau buổi 17**, không sớm hơn ✓. Phase 1–3 = **0 phút** ✓ (plan.md 72, phase-01 109, phase-02 48).
Cấm Puzzle Duel ✓ · cấm online người lạ ✓ · cấm mọi thứ tính điểm ✓ · ChessKid Puzzles Mode = **Unrated** kèm đường dẫn Settings → Play → Puzzles Mode ✓ · máy phụ huynh, ngồi cạnh cùng xem ✓ · iOS Screen Time / Family Link ✓ · **không mở app vào ngày buổi bàn cờ bị cắt sớm vì bé nản** ✓ (phase-04 46) · cap không áp cho người lớn ✓ (plan.md 72, phase-01 24).
Thiếu duy nhất: *"chỉ dùng vào ngày **đã có buổi bàn cờ**, và **sau khi** đã chơi xong trên bàn"* — phase-04 dòng 45 có ("chỉ dùng vào ngày đã chơi xong trên bàn") ✓. Đủ.

### Mục 8 — Success metrics — **2 thiếu (M4, m5)**
| Nguồn mục 8 | plan.md Success Criteria |
|---|---|
| Ván mốc ra kết quả | ✓ 78 |
| ≤3 lần nhắc luật | ✓ 78 |
| ≥90% nước hợp luật, ≥20 nước | ✓ 78 |
| Tự bày 32 quân ≤3 phút, 2 lần liên tiếp | ✓ 79 |
| Nhận diện chiếu hết ≥6/8 (đo buổi 22 **và đo lại buổi 30**) | ⚠ **không có trong plan.md** Success Criteria; có ở phase-06 dòng 52 ✓ → chấp nhận được, ghi nhận |
| Mate 2 Xe **hoặc** Hậu+Vua, ≤2 gợi ý | ✓ 80 |
| Nhập thành 5/5 | ✓ 80 |
| CỬA 1 & 2 ≥11/12 | ✓ 81 |
| ≥4 lần bé tự đòi chơi 7 ngày cuối | ✓ 82 |
| Sau ván mốc bé đòi chơi tiếp = Có | ✓ 82 |
| ≤20% buổi dừng sớm (≤6/30) | ✓ 83 |
| **≤1 đợt "nghỉ 3 ngày"** | **✗ M4 — THIẾU** |
| Trung vị buổi 26–30 ≥12 phút, tăng ≥50% | ✓ 84 |
| Số buổi bé rời bàn giữa ván Phase 6 ≤1 | ⚠ không có trong plan.md; có ở phase-06 dòng 73 ✓ |
| 30 buổi trong ≤45 ngày | ✓ 85 |
| **Không chuỗi ≥3 ngày không buổi nào** | **✗ m5 — THIẾU** ở Success Criteria (chỉ có ở Goals dòng 33) |
| Ngày duy trì ≤8 | ✓ 85 |
| Bảng ghi đủ 3 số ≥27/30 | ✓ 85 |
| App ≤60 phút · ≤8 lần · 0 Puzzle Duel/online/tính điểm | ✓ 86 |
| App dùng **thay** buổi bàn cờ / vào ngày bị cắt sớm: **0** | ⚠ không có trong plan.md metrics; luật có ở phase-04 dòng 46 ✓ |

**Không có metric nào bị làm yếu hay bịa thêm.** 2 metric bị bỏ khỏi checklist nghiệm thu (M4, m5), 3 metric nằm ở phase file thay vì plan.md (chấp nhận được — plan.md tự nói phase-01 giữ nghiệm thu riêng, dòng 88).

### Van an toàn 29–30, "treo ván bằng ảnh" — **khớp nguyên văn**
phase-06 dòng 29–36: đừng ép xong · đừng huỷ · người lớn chụp, bé không cầm máy · không tính cap màn hình của bé · hôm sau dựng lại chơi tiếp · người lớn xin thua vẫn là kết quả hợp lệ ✓. plan.md dòng ~78 ghi *"(Được phép treo ván bằng ảnh...)"* — thực ra nằm ở nguồn dòng 343; plan.md dòng 78 **không** có mệnh đề này. Nhỏ, phase-06 đã phủ.

### Non-goals — **khớp**
plan.md dòng 35 liệt kê: ký hiệu bàn cờ · nguyên tắc khai cuộc · mẫu chiến thuật · en passant · Elo ✓ (nguồn dòng 12 + mục 3). phase-01 dòng 83 nhắc lại *"Không bao giờ nói toạ độ với bé"* ✓. phase-04 dòng 19 giữ hoãn en passant ✓. phase-06 dòng 63 đẩy en passant sang sau ngày 30 ✓.

### Takeback — **khớp**
Không giới hạn tới hết buổi 29; chạm-quân chỉ ở buổi 30 ✓ (phase-01 106, phase-02 49, phase-06 38–40).

### 4 nhịp học lại của người lớn — **khớp**
Nhịp 1 (Tối A + B) ✓ phase-01 22–40 · Nhịp 2 (Mã a1→h8 ×5, trước buổi 12) ✓ phase-03 41 · Nhịp 3 (mate 2 Xe + Hậu/Vua <2 phút + "thua cho đúng", trước buổi 22) ✓ phase-05 31–33 · Nhịp 4 (4 điều kiện nhập thành, trước buổi 26) ✓ phase-05 35–36. Nội dung 4 điều kiện nhập thành sao đúng nguyên văn ✓.

---

# PRIORITY C — Executability tại bàn

### C1 — Mục tiêu từng buổi so với bé 5 tuổi, zero prior

| Buổi | Mục tiêu | Khả thi? |
|---|---|---|
| 1 | Tự quay bàn đúng, 2 lần liên tiếp | ✓ Dễ. Chỉ cần nhớ 1 quy tắc thị giác |
| 2 | 10/10 nước Xe đúng | ✓ nhưng cần 2–3 lượt để đủ mẫu (**M1**) |
| 3 | Ăn hết trong ≤6 nước | ✓ **nếu** bé đi hợp lý; tối ưu = 5, có 4 đường. Ngưỡng ≤6 hợp lý |
| 4 | 2/3 ván không tự đi vào ô bị ăn | ⚠ Xem C4 |
| 5 | Tự nói màu ô của Tượng | ✓ mục tiêu dễ — **nhưng thế cờ hỏng (B2)** làm bé nản trước khi tới đó |
| 6 | Chơi trọn 1 ván không nhắc | ✗ **không đo được với thế hiện tại (B3)** — ván xong ở nước 1 |

Không có buổi nào **mục tiêu** quá tầm. Chỗ hỏng là **thế cờ và câu thoại không đỡ nổi mục tiêu** ở buổi 3/5/6.

### C2 — Lời thoại tiếng Việt có nói được với bé 5 tuổi không?

Đã đọc từng câu thoại của 6 buổi. Nhìn chung **đạt**: câu ngắn, xưng "bố/mẹ – con", gọi quân là "bạn Xe / bạn Tượng", dùng câu hỏi thay câu khẳng định, có chỉ dẫn cử chỉ ("vừa nói vừa trượt ngón tay") — đúng với việc bé 5 tuổi học bằng vận động hơn bằng lời.

Ba chỗ hơi dài/trừu tượng so với tuổi:
- Buổi 2 dòng 257: *"Bạn ấy đi thẳng băng thôi: ngang, hoặc dọc. Xa bao nhiêu cũng được. Nhưng không biết đi chéo."* — 4 mệnh đề trong 1 lượt nói. Có chỉ tay kèm nên qua được, nhưng là câu dài nhất Phase 1. Gợi ý chẻ: nói 2 mệnh đề đầu, cho bé đẩy 1 nước, rồi mới nói "không biết đi chéo".
- Buổi 4 dòng 411: *"Xe kia cũng đi thẳng băng như Xe con. Nên đừng đứng vào đường của bạn ấy."* — "đường của bạn ấy" là ẩn dụ không gian trừu tượng. Plan có bù bằng trượt ngón tay dọc hàng 7 và cột g ✓, và giới hạn "gieo hạt, chỉ 1 lần" ✓. Chấp nhận được.
- Buổi 4 dòng 429/571: *"Xe kia đi thẳng, có tới chỗ đó được không nhỉ?"* — câu hỏi phản-thực (counterfactual) về nước đi của **quân đối phương**. Đây là nội dung nhận thức nặng nhất Phase 1. Xem C4.

Xưng hô, độ dài, từ vựng: không có từ nào ngoài tầm bé 5 tuổi. "Kiểm soát", "hợp lệ", "tối ưu" chỉ xuất hiện trong phần **cho người lớn**, không lọt vào lời thoại ✓ — kiểm bằng grep, xác nhận.

### C3 — Có rò rỉ non-goal không?

| Non-goal | Kiểm | Kết |
|---|---|---|
| Ký hiệu (e4, Nf3) | Toạ độ chỉ xuất hiện trong sơ đồ + phần người lớn; dòng 83 cấm tường minh nói toạ độ với bé | ✓ sạch |
| Nguyên tắc khai cuộc | Không có "chiếm trung tâm" / "phát triển quân" ở bất kỳ đâu | ✓ sạch |
| Mẫu chiến thuật (fork/pin) | Dòng 588 cấm tường minh: *"Không giảng chiến thuật — đó là non-goal"* | ✓ sạch |
| en passant | Chỉ ở phần người lớn (dòng 40, thẻ A5 dòng 62 "✗ HOÃN") + sau ngày 30 | ✓ sạch |
| **Cách Tốt đi, trước buổi 17** | Buổi 3 dùng Tốt làm bia. Dòng 308 cảnh báo người lớn; dòng 356 có câu trả lời sẵn; Risk dòng 644 có mục riêng | ⚠ **m1** — "đứng chắn đường" (334, 353) là rò rỉ nhẹ |

Kịch bản buổi 3 chống rò rỉ **tốt hơn mức trung bình** — 3 lớp phòng thủ độc lập. Chỉ mắc ở chữ "chắn".

### C4 — Buổi 4 ("ô bị quân khác kiểm soát") — mitigation có đủ không?

Đây là nội dung trừu tượng nhất Phase 1, đặt ở buổi thứ 4 của chương trình. Kiểm các lớp giảm nhẹ mà plan đã đặt:

1. Hạ kỳ vọng tường minh (dòng 375): *"Không kỳ vọng bé hiểu — kỳ vọng bé **né được**."* ✓ Đúng cách — chuyển mục tiêu từ nhận thức sang hành vi.
2. Ngưỡng chỉ 2/3 ván ✓ (cho phép sai 1/3).
3. Gieo khái niệm **đúng 1 lần**, kèm cử chỉ trượt ngón tay (dòng 411–412) ✓.
4. Chỉ nói **sau khi tay bé rời quân** + takeback không giới hạn (dòng 414–416) ✓ — bé được thử lại, không bị phạt.
5. Sau 3 lần sai → **đổi sang công cụ vật lý**: đặt 4 xu lên ô nguy hiểm cho bé *nhìn thấy* (dòng 431) ✓ — chuyển từ lời sang thị giác, đúng kênh học của tuổi này. Đây là mitigation mạnh nhất.
6. Người lớn thua **bằng đúng lỗi bé hay mắc** (dòng 418–420) ✓ — bình thường hoá lỗi.
7. Không lặp buổi nếu bé không hiểu; khái niệm quay lại ở buổi 10–11 với ngữ cảnh mạnh hơn (dòng 442, 643) ✓ — có đường thoát, không tạo nút thắt.

**Kết luận: mitigation ĐỦ.** 7 lớp, trong đó lớp 5 và 7 là loại tốt (đổi kênh cảm giác; có đường thoát không phạt). Không có finding về pedagogy ở đây.

Cái duy nhất cần sửa ở buổi 4 là **m4** (bé đi trước cả 3 ván xung đột chỉ tiêu 60–70%) — vấn đề chỉ tiêu, không phải độ khó.

### C5 — Trần 15 phút vs khối lượng buổi

Buổi 1 có **2 trò** (quay bàn ×2–3 lượt + 8 xu đoán màu). Với khung `[6-9 phút] 2–3 lượt của cùng một trò`, 8 xu thêm ~2 phút. Điều kiện dừng sớm dòng 213 đã ghi *"dừng trước phút thứ 11"* ✓ và dòng 210 cho phép bỏ dở 8 xu ✓. Vừa khít, có van. Chấp nhận được.

---

# PRIORITY D — Nhất quán nội bộ

Ngoài m2/m3/M5 đã nêu:

### D1 — "≥3 buổi" vs "3 buổi liên tiếp" (phase-01 634 vs nguồn 214)
phase-01 chặt hơn nguồn. Chặt hơn ⇒ không làm loãng ⇒ không phải defect. Nên đồng bộ chữ cho khỏi lệch khi viết Phase 2.

### D2 — Ngưỡng dừng sớm khác nhau giữa các phase (phase-02 54 "≥2 buổi trong 10–11" vs phase-03 53 "≥2 buổi **liên tiếp** trong 12–15")
Hai ngưỡng khác nhau cho cùng loại tín hiệu, không có lý do ghi kèm. Không sai so với nguồn (nguồn không quy định ngưỡng theo phase), nhưng khi viết chi tiết Phase 2/3 sẽ dễ tự mâu thuẫn. Ghi nhận, không phải finding.

### D3 — plan.md dòng 22 tuyên bố "không thiết kế lại gì" — **đúng**
Kiểm: không tìm thấy chỗ nào plan tự thêm nội dung dạy học ngoài nguồn. Lớp bổ sung đúng là "lớp thi hành" như tuyên bố (lời thoại, sơ đồ, câu sửa lỗi, điều kiện dừng sớm). **Không có scope creep.**

### D4 — Placeholder Phase 2–6 — **không tính là finding** (mục 2.17), và làm đúng
Mỗi placeholder đều: trích nguyên văn khung 5.2 · liệt kê điều kiện viết chi tiết · nêu ràng buộc kế thừa · có Risk Assessment. Đủ để không phải đọc lại nguồn khi tới lượt viết.

### D5 — Numbering: nguồn dùng "mục 2.17", plan.md dòng 24/64 cũng "mục 2.17"
Kiểm nguồn: mục 2 mục C có **17 mục đánh số liên tục 1–17**, mục 17 là *"Chỉ viết chi tiết Phase 1 trước..."*. Tham chiếu **đúng**. (Nguồn không đánh số "2.17" tường minh nhưng suy ra không mơ hồ.)

### D6 — Điều kiện thực tế bảng plan.md dòng 97–103 thiếu hàng 5
Bảng đánh số 1, 2, 3, 4, **6** — thiếu 5. Dòng 107 giải thích: câu 5 nằm ở "Còn treo". Cố ý, đọc được. Không phải finding.

---

# Recommended Actions — theo thứ tự

1. **B3** — sửa thế buổi 6: Xe bé `f2`→`e2`, Xe người lớn `c7`→`b7`; sửa nhãn dòng 555 "ô đen"→"ô trắng". *(cửa nghiệm thu Phase 1 đang không đo được gì)*
2. **B2** — sửa thế buổi 5: xu `d4`,`f2` → `c5`,`b2`; nới tiêu chí nước lên ≤7; cập nhật sơ đồ ASCII dòng 463–473.
3. **B1** — buổi 3: câu chốt dòng 347 bỏ số cứng "6 nước" → điền số thật; dòng 312 ghi rõ "5 nếu tối ưu, ≤6 vẫn đạt".
4. **M5** — phase-01 dòng 285/537: khôi phục tần suất "cố tình đi sai" về 2–3 lần trong Phase 1.
5. **M4 + m5** — plan.md Success Criteria: thêm `≤1 đợt nghỉ 3 ngày` và `không chuỗi ≥3 ngày không buổi nào`.
6. **M3** — bỏ block plan.md dòng 15–16 (`plan.html` không tồn tại), hoặc tạo file kèm sơ đồ **đã sửa**.
7. **M1 + M2** — buổi 2: ghi rõ 10 nước là cộng dồn 2–3 lượt; đổi câu chốt "thử ít hơn" (bất khả thi ở buổi 2, giữ ở buổi 3).
8. **m2 + m3** — đồng bộ checklist với R1/R2/R3: thay 3 ô tick không-tick-được (bàn cố định, HLV dự bị, bạn 5 tuổi) bằng ô tick phương án bù; sửa Risk dòng 647.
9. **m6** — tổng quát hoá mẹo Tượng ở buổi 5 để dùng được cho Tượng trắng ở buổi 6.
10. **m1** — buổi 3: bỏ chữ "chắn đường" (dòng 334, 353).
11. **m4** — buổi 4 dòng 400: ván 2 người lớn đi trước.
12. **PRIORITY B ghi nhận** — thêm hàng "3 tín hiệu / bé khóc → không tính là buổi đã hoàn thành" vào plan.md dòng 70.

---

# Bảng trạng thái Plan TODO

| Hạng mục | Trạng thái quan sát được |
|---|---|
| Phase 1 viết chi tiết | Hoàn tất về cấu trúc (5 phần/buổi đúng yêu cầu) — **3 BLOCKER thế cờ chặn chạy thật** |
| Phase 2–6 placeholder | Hoàn tất đúng mục 2.17 ✓ |
| Cổng chuẩn bị | **Mâu thuẫn R1/R2/R3** — 3 ô không tick được (m2/m3) |
| Success Criteria | 2 metric thiếu so với mục 8 (M4, m5) |
| plan.html | **Không tồn tại**, đang được gọi là "artifact chính" (M3) |

Không đề xuất đổi trạng thái phase — để lead/planner quyết.

---

# Câu hỏi còn treo

1. `plan.html` — dự định tạo hay tàn dư của lần soạn trước? Nếu tạo, nó sẽ chứa lại sơ đồ ⇒ phải mang cả 3 fix BLOCKER, nếu không sẽ có 2 nguồn sơ đồ mâu thuẫn.
2. Buổi 5 sau khi sửa chỉ còn **1** thứ tự đúng duy nhất. Chấp nhận (kèm nới trần lên ≤7 nước), hay đổi mục tiêu buổi 5 thành "ăn được **3 trong 5** xu" để có dư địa sai? Không tồn tại bộ 5 xu cùng màu vừa trải rộng vừa có ≥3 lời giải — đây là ràng buộc hình học của quân Tượng, không phải thiếu sót thiết kế.
3. phase-01 dòng 634 dùng "≥3 buổi trong Phase 1" còn nguồn dùng "3 buổi **liên tiếp**" — cố ý siết chặt cho Phase 1, hay lỗi sao chép? Ảnh hưởng cách viết Phase 2.
4. Mốc "bạn 5 tuổi hạn chót buổi 20" (phase-04) giữ làm mục tiêu-nên-có dù R3 chốt là không có, hay thay hẳn bằng phương án bù của R3?
