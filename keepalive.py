import subprocess
import time

# 监控闲鱼
app_package = "com.taobao.idlefish"
app_activity = "com.taobao.idlefish/.maincontainer.activity.MainActivity"  # 主界面 Activity
adb_path = "adb"  # adb路径


# 检查应用是否在前台
def is_app_in_foreground(package_name):
    result = subprocess.run(
        ['adb', 'shell', 'dumpsys', 'activity', 'activities'],
        capture_output=True, text=True
    )
    return package_name in result.stdout and 'mResumedActivity' in result.stdout


# 启动应用
def start_app(package_name, activity):
    command = [adb_path, "shell", "am", "start", "-n", activity]
    print(f"启动应用：{command}")
    subprocess.run(command)


# 确保应用在前台
def bring_app_to_foreground(package_name):
    if not is_app_in_foreground(package_name):
        print(f"{package_name} 不在前台，正在将其带到前台...")
        start_app(package_name, app_activity)
    else:
        print(f"{package_name} 已经在前台，无需重新启动。")


# 循环监控应用状态
while True:
    bring_app_to_foreground(app_package)
    time.sleep(10)
