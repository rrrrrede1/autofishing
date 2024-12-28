import subprocess


def get_notifications():
    # 执行 ADB 命令获取通知
    command = ["adb", "shell", "dumpsys", "notification", "--noredact"]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout


def filter_notifications(app_package):
    # 获取所有通知
    notifications = get_notifications()

    # 过滤出特定应用的通知
    app_notifications = []
    lines = notifications.splitlines()

    for line in lines:
        if app_package in line:  # 根据包名过滤通知
            app_notifications.append(line)

    return app_notifications


# 示例：过滤特定应用的通知
app_package = "com.example.app"  # 用你要监听的应用包名替换
notifications = filter_notifications(app_package)

for notification in notifications:
    print(notification)
