import subprocess
import time

# 监控闲鱼
app_package = "com.taobao.idlefish"
adb_path = "adb"  # adb路径
activity = ".maincontainer.activity.MainActivity"

# 检查应用是否在后台运行
def is_app_running(package_name):
    result = subprocess.run(
        [adb_path, "shell", "pidof", package_name],
        capture_output=True, text=True
    )
    return result.returncode == 0 and result.stdout.strip()

# 启动应用到后台
def start_app_in_background(package_name, activity_name):
    # 启动应用
    start_command = [adb_path, "shell", "am", "start", "-n", f"{package_name}/{activity_name}"]
    print(f"启动应用：{start_command}")
    subprocess.run(start_command)

    # 模拟按下 Home 键，将应用置于后台
    home_command = [adb_path, "shell", "input", "keyevent", "3"]  # 3 是 HOME 键的 keycode
    print(f"将应用置于后台：{home_command}")
    subprocess.run(home_command)


# 确保应用运行
def ensure_app_in_background(package_name, activity_name):
    if not is_app_running(package_name):
        print(f"{package_name} 未运行，启动应用到后台...")
        start_app_in_background(package_name, activity_name)
    else:
        print(f"{package_name} 已在后台运行。")

# 主程序
while True:
    ensure_app_in_background(app_package, activity)
    time.sleep(10)
