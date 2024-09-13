# 4groundsCLI
A terminal emulator integrated with AI

Do chưa thể đóng gói ứng dụng, vui lòng sử dụng cách sau đây để khởi chạy:
Đầu tiên phải đảm bảo bạn đã có [Rust](https://www.rust-lang.org/tools/install) và Tauri (cargo install tauri-cli) trên máy tính cá nhân.
1. Clone repo về máy và cd vào thư mục src-tauri/src
2. Nếu chưa có node.js, tải node.js và nhập câu lệnh sau vào terminal của bạn "npm install http-server -g"
3. ngay tại đường dẫn ../src-tauri/src, nhập lệnh "http-server -c-1 -o index.html" để khởi chạy server front-end.
4. Mở một tab terminal khác, cd vào ../src-tauri và nhập lệnh "cargo tauri build" và "cargo tauri dev" để khởi chạy.
