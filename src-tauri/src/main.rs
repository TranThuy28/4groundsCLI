#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use std::process::{Command};
use std::thread;
use tokio::runtime::Runtime;
use warp::Filter;
use warp::http::Method;
use serde_json::Value;

use std::env;
use std::path::Path;
use std::sync::{Arc, RwLock};
use tauri::State;

#[derive(Clone)]
struct AppState {
    current_dir: Arc<RwLock<String>>,
}

impl AppState {
    // Tạo một hàm khởi tạo mới cho AppState
    fn new() -> Self {
        // Đặt thư mục khởi tạo ban đầu là C:/Users
        let initial_dir = "C:/Users/Minh Thuy".to_string();
        // Kiểm tra nếu thư mục tồn tại, sử dụng nó, nếu không thì dùng thư mục hiện tại của hệ thống
        let current_dir = if Path::new(&initial_dir).exists() {
            initial_dir
        } else {
            env::current_dir().unwrap().display().to_string()
        };
        AppState {
            current_dir: Arc::new(RwLock::new(current_dir)),
        }
    }

    // Hàm thay đổi thư mục làm việc
    fn change_directory(&self, path: &str) -> Result<(), String> {
        let new_dir = Path::new(path);
        if env::set_current_dir(&new_dir).is_err() {
            return Err(format!("Failed to change directory to {}", path));
        }
        let mut dir = self.current_dir.write().unwrap();
        *dir = new_dir.display().to_string();
        Ok(())
    }

    // Hàm lấy thư mục làm việc hiện tại
    fn get_current_directory(&self) -> String {
        let dir = self.current_dir.read().unwrap();
        dir.clone()
    }
}

#[tauri::command]
fn run_command(state: State<AppState>, input: String) -> Result<String, String> {
    let current_dir = state.get_current_directory(); // Lấy thư mục hiện tại từ AppState

    if input.starts_with("cd") {
        // Xử lý lệnh `cd`
        let path = input.split_whitespace().nth(1).unwrap_or("");
        // Kết hợp thư mục hiện tại và thư mục mới
        let new_path = Path::new(&current_dir).join(path);
        
        match state.change_directory(&new_path.display().to_string()) {
            Ok(_) => {
                let mut dir = state.current_dir.write().unwrap();
                *dir = new_path.display().to_string(); // Cập nhật lại thư mục mới
                Ok(format!("Changed directory to {}", *dir))
            }
            Err(e) => Err(format!("Failed to change directory: {}", e)),
        }
    } else {
        // Thực thi các lệnh khác ngoài `cd`
        let output = if cfg!(target_os = "windows") {
            Command::new("cmd")
                .args(&["/C", &input])
                .current_dir(&current_dir)  // Thực thi lệnh trong thư mục hiện tại
                .output()
                .expect("failed to execute command")
        } else {
            Command::new("sh")
                .arg("-c")
                .arg(&input)
                .current_dir(&current_dir)  // Thực thi lệnh trong thư mục hiện tại
                .output()
                .expect("failed to execute command")
        };

        let stdout = String::from_utf8_lossy(&output.stdout);
        let stderr = String::from_utf8_lossy(&output.stderr);

        if !stderr.is_empty() {
            Err(stderr.to_string())
        } else {
            Ok(stdout.to_string())
        }
    }
}

#[tauri::command]
fn change_directory(state: State<AppState>, new_dir: String) -> Result<String, String> {
    // Thay đổi thư mục làm việc thông qua AppState
    match state.change_directory(&new_dir) {
        Ok(_) => Ok(format!("Directory changed to {}", state.get_current_directory())),
        Err(e) => Err(e),
    }
}

fn main() {
    let app_state = AppState::new();  // Khởi tạo AppState với thư mục ban đầu là C:/Users nếu tồn tại

    // Chạy server warp trong thread riêng
    let state_clone = app_state.clone(); // Clone state để chia sẻ giữa các thread
    thread::spawn(move || {
        let rt = Runtime::new().unwrap();
        rt.block_on(async {
            let cors = warp::cors()
                .allow_any_origin()
                .allow_methods(&[Method::GET, Method::POST])
                .allow_headers(vec!["Content-Type"]);

            let run_command = warp::path("run_command")
                .and(warp::post())
                .and(warp::body::json())
                .and(warp::any().map(move || state_clone.clone())) // Truyền state vào warp
                .map(|input: Value, state: AppState| {
                    let command = input["input"].as_str().unwrap_or("");

                    let current_dir = state.get_current_directory(); // Lấy thư mục hiện tại từ state

                    let output = if cfg!(target_os = "windows") {
                        Command::new("cmd")
                            .args(&["/C", &command])
                            .current_dir(&current_dir)
                            .output()
                            .expect("failed to execute command")
                    } else {
                        Command::new("sh")
                            .arg("-c")
                            .arg(command)
                            .current_dir(&current_dir)
                            .output()
                            .expect("failed to execute command")
                    };

                    let stdout = String::from_utf8_lossy(&output.stdout).to_string();
                    let stderr = String::from_utf8_lossy(&output.stderr).to_string();

                    if !stderr.is_empty() {
                        warp::reply::json(&serde_json::json!({ "error": stderr }))
                    } else {
                        warp::reply::json(&serde_json::json!({ "output": stdout }))
                    }
                })
                .with(cors);

            warp::serve(run_command)
                .run(([127, 0, 0, 1], 3030))
                .await;
        });
    });

    // Khởi chạy ứng dụng Tauri
    tauri::Builder::default()
        .manage(app_state) // Quản lý state trong Tauri
        .invoke_handler(tauri::generate_handler![run_command, change_directory])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
