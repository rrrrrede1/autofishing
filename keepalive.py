import subprocess
import time

# 监控闲鱼
app_package = "com.taobao.idlefish"
adb_path = "adb"  # adb路径

# 检查应用是否在后台运行
def is_app_running(package_name):
    result = subprocess.run(
        [adb_path, "shell", "pidof", package_name],
        capture_output=True, text=True
    )
    return result.returncode == 0 and result.stdout.strip()

# 启动应用到后台
def start_app_in_background(package_name):
    command = [adb_path, "shell", "monkey", "-p", package_name, "-c", "android.intent.category.LAUNCHER", "1"]
    print(f"启动应用到后台：{command}")
    subprocess.run(command)

# 确保应用运行
def ensure_app_in_background(package_name):
    if not is_app_running(package_name):
        print(f"{package_name} 未运行，启动应用到后台...")
        start_app_in_background(package_name)
    else:
        print(f"{package_name} 已在后台运行。")

# 主程序
while True:
    ensure_app_in_background(app_package)
    time.sleep(10)
