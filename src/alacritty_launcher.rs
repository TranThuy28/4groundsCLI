use std::process::Command;

pub fn launch_alacritty() {
    Command::new("alacritty")
        .arg("--title")
        .arg("My Custom CLI")
        .spawn()
        .expect("Failed to launch Alacritty");
}
