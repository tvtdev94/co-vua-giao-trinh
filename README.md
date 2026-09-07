# Giáo trình cờ vua 30 buổi cho bé 5 tuổi

Dạy bé 5 tuổi chơi cờ vua từ số 0, **mỗi buổi ≤15 phút**. Phụ huynh làm huấn
luyện viên — không cần biết chơi cờ trước, có sẵn lời thoại từng câu.

**Đọc trên web:** https://tvtdev94.github.io/co-vua-giao-trinh/

## Mở cái gì trước

| Bạn muốn | Mở file |
|---|---|
| Xem tổng quan, mục tiêu, rủi ro | [`plan.md`](plans/260907-0938-co-vua-30-buoi/plan.md) |
| Đọc từng buổi, mỗi buổi một file | [`buoi/README.md`](plans/260907-0938-co-vua-30-buoi/buoi/README.md) |
| Việc phải làm **trước buổi 1** | [`phase-01`](plans/260907-0938-co-vua-30-buoi/phase-01-ban-co-xe-tuong.md) → *Cổng chuẩn bị* |
| In ra giấy để chạy buổi 1–6 | [`print-buoi-1-6.html`](plans/260907-0938-co-vua-30-buoi/print-buoi-1-6.html) |

## Ba luật xuyên suốt

- **Trần 15 phút.** Hết 15 phút mà bé vẫn muốn chơi → **vẫn dừng**. Dừng lúc
  đang vui là lý do bé đòi chơi lần sau.
- **Quy tắc 3 tín hiệu.** Bé rời mắt, đi bừa, hay chơi quân như đồ chơi — 2 tín
  hiệu là dừng ngay, không tiếc buổi.
- **Không dùng chữ "sai".** Chỉ sửa nước vừa đi, im lặng khi bé đang nghĩ.

## Tiến độ nội dung

- **Buổi 1–6:** viết đầy đủ — lời thoại, sơ đồ bày bàn, câu sửa lỗi, điều kiện
  dừng sớm. Sơ đồ bàn cờ đã qua kiểm tự động.
- **Buổi 7–30:** đã chốt chủ đề, trò chơi và tiêu chí "xong"; phần lời thoại và
  sơ đồ soạn sau. **Cố ý** — soạn trước 30 kịch bản là soạn theo tưởng tượng,
  vì chưa biết bé ngồi được bao nhiêu phút thật.

## Dựng lại file sinh tự động

Bốn script, chạy trong `plans/260907-0938-co-vua-30-buoi/`. Mỗi script **tự kiểm
trước khi ghi** — sai một toạ độ là báo lỗi, không im lặng xuất bản hỏng.

```sh
python make-days.py         # sinh 30 file buoi/buoi-NN-*.md
python make-site.py         # sinh buoi/README.md + docs/ cho GitHub Pages
python make-print-pages.py  # sinh print-buoi-1-6.html
python rebuild-html.py      # nhung lai phase-*.md vao plan.html
```

Nguồn gốc để sửa là các file `.md`. Sửa `.md` rồi chạy lại script — đừng sửa
ngược vào file sinh ra.
