import subprocess
import time

# 监控闲鱼
app_package = "com.taobao.idlefish"
adb_path = "adb"  # adb路径


# 是否在后台运行
def is_app_running(package_name):
    # 获取当前正在运行的进程列表
    command = [adb_path, "shell", "ps"]
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='ignore')

    # 检查应用包名是否出现在进程列表中
    return package_name in result.stdout


# 启动应用
def start_app(package_name):
    command = [adb_path, "shell", "am", "start", "-n", f"{package_name}/.maincontainer.activity.MainActivity"]
    subprocess.run(command)


# 循环监控应用状态
while True:
    if not is_app_running(app_package):
        print(f"{app_package} 没有在运行。正在重新启动...")
        start_app(app_package)
    else:
        print(f"{app_package} 正在运行。")

    # 每 10 秒检查一次
    time.sleep(10)
