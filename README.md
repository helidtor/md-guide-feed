# Feed MD Deck Guide (schema v1)

Thư mục này là toàn bộ feed để đưa lên repo GitHub công khai. Nội dung do script sinh, không sửa tay trừ khi chạy lại bước băm ở dưới.

| File | Vai trò |
|---|---|
| `manifest.json` | Điểm vào. Có `dataVersion` (số nguyên >= 1), `generatedAt`, `sources[]`, `files.*.{url,sha256,size}` |
| `decks.json` | 5 deck thật + các deck stub (chỉ `id`, `name`, `archetypes`, `contentStatus:"stub"`) |
| `guides.json` | Guide/combo của 5 deck thật (`reviewStatus:"ai_draft"`) |
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