# Feed MD Deck Guide (schema v1)

Thư mục này là toàn bộ feed để đưa lên repo GitHub công khai. Nội dung do script sinh, không sửa tay trừ khi chạy lại bước băm ở dưới.

| File | Vai trò |
|---|---|
| `manifest.json` | Điểm vào. Có `dataVersion` (số nguyên >= 1), `generatedAt`, `sources[]`, `files.*.{url,sha256,size}` |
| `decks.json` | 100 deck có nội dung và decklist; không có stub (`contentStatus:"in-review"`) |
| `guides.json` | 100 guide tiếng Việt; guide mới có line mở engine minh họa (`reviewStatus:"ai_draft"`) |
| `SOURCES-100-DECKS.md` | 65 deck mới, link Master Duel Meta, ngày/thành tích mẫu và các điều chỉnh banlist |
| `banlist.json` | TUỲ CHỌN. Chỉ cần cho list sắp hiệu lực / ghi đè giờ hiệu lực. Nếu không muốn dùng: xoá file và xoá khoá `files.banlist` trong manifest (rồi chạy lệnh băm) |
| `.gitattributes` | `* -text`: bắt Git giữ nguyên byte (không đổi CRLF) để `sha256` không lệch |

## Đưa lên GitHub
1. Tạo repo công khai, copy TẤT CẢ file trong thư mục này (kể cả `.gitattributes`) vào thư mục gốc repo.
2. Base URL của app = thư mục chứa `manifest.json`, ví dụ `https://raw.githubusercontent.com/<user>/<repo>/<branch>/`. Đặt ở config của app (không hard-code). URL trong manifest là đường dẫn tương đối nên không cần sửa khi đổi repo.
3. GitHub raw cache tối đa ~5 phút; `sha256` + `size` trong manifest bắt lỗi trộn file cũ/mới.

## Sau khi sửa tay một file JSON
```
dart run tool/build_feed/feed_hash.dart feed-dist            # kiểm tra manifest có khớp file không
dart run tool/build_feed/feed_hash.dart feed-dist --write    # ghi lại sha256/size vào manifest
```
Đồng thời tăng `dataVersion` (số nguyên) trong manifest VÀ trong từng file dữ liệu (phải bằng nhau).

## Dựng lại từ đầu
Xem `tool/build_feed/README.md` và chạy lint:
```
dart run tool/feed_lint.dart feed-dist --cards tool/build_feed/.cache/cardinfo_master_duel.json --allow-missing tool/build_feed/allow_missing_cards.txt
```

## Banlist ngày 06/10/2026 — dataVersion 5

Cả 100 deck dùng `MD-2026-10-06`. Đã đối chiếu 7 thay đổi trong ảnh người dùng với [Master Duel Meta](https://www.masterduelmeta.com/forbidden-limited-list), sửa decklist/guide bị ảnh hưởng và tính lại hash/size trong manifest. Xem chi tiết trong [BANLIST-2026-10-06.md](BANLIST-2026-10-06.md).

Kiểm tra bản hiện tại (cần cache `research/cardinfo.json`; nếu thiếu, chạy `rtk python research/fetch_cards.py`):

```powershell
rtk python research/validate_feed.py
```

Validator kiểm tra cả 100 deck/guide: ID/tên/vùng bài, số lá, giới hạn cộng dồn theo banlist được khai báo, liên kết combo, version và hash/size. `research/update_banlist_2026_10_06.py` lưu bước chuyển từ bản 4 sang bản 5; chạy lại sau khi áp dụng sẽ không tăng version lần nữa.

## Lịch sử: bản mở rộng 100 deck — dataVersion 4

Giữ nguyên nội dung 35 deck/guide ban đầu, thêm 65 deck có mẫu và kết quả trên Master Duel Meta. Mẫu được chọn có thành tích giải hoặc Master rank/Rating Duels/Win Streak/WCS DLv. Max trong tháng 06–10/2026. Các lựa chọn rogue được ghi rõ, không coi toàn bộ 100 deck là tier hiện tại. Xem bảng nguồn trong `SOURCES-100-DECKS.md`.

Decklist mới được kiểm tra theo cả hai snapshot banlist MD-2026-09-03 và MD-2026-10-06 của feed; thay đổi slot được ghi trong guide và tài liệu nguồn. Combo có điều kiện/cost cụ thể, không mặc định là end board tối đa. Guide vẫn là bản biên soạn chờ duyệt.

Các lệnh dưới đây dành cho bản mở rộng lịch sử, không cần bộ tool Dart của dự án app. Không dùng builder này để dựng lại bản 5: script sẽ từ chối ghi đè một bản mới hơn.

```powershell
rtk python research/fetch_cards.py
rtk python research/build_feed.py
rtk python research/validate_feed.py
```

`research/selected.json` lưu decklist/thành tích nguồn; `editorial.py` và `refinements.py` chứa nội dung biên soạn. Builder lịch sử giữ 35 mục đầu, thay thế 65 mục bổ sung, đặt `dataVersion = 4` và tính lại manifest. Các bản cập nhật banlist tiếp theo cần bước chuyển riêng để giữ những chỉnh sửa của bản hiện tại.
