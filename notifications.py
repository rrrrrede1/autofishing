import subprocess


def get_notifications():
    # 执行 ADB 命令获取通知
    command = ["adb", "shell", "dumpsys", "notification", "--noredact"]
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='ignore')

    # 检查 adb 命令是否成功执行
    if result.returncode != 0:
        print(f"运行adb命令时出错：{result.stderr}")
        return None

    return result.stdout


def filter_notifications(app_package):
    # 获取所有通知
    notifications = get_notifications()

    if not notifications:  # 检查是否成功获取到通知
        print("未找到通知")
        return []

    # 过滤出通知
    app_notifications = []
    lines = notifications.splitlines()

    for line in lines:
        if app_package in line:  # 根据包名过滤通知
            app_notifications.append(line)

    return app_notifications


# 过滤通知
app_package = "com.taobao.idlefish"  # 监听闲鱼
notifications = filter_notifications(app_package)

if notifications:
    for notification in notifications:
        print(notification)
else:
    print("没有收到通知")
