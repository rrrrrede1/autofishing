import subprocess
import re


def get_notifications():
    command = ["adb", "shell", "dumpsys", "notification", "--noredact"]
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='ignore')

    if result.returncode != 0:
        print(f"运行adb命令时出错：{result.stderr}")
        return None

    return result.stdout


def extract_notification_details(notification_data):
    notifications = []
    notification_pattern = r'android\.title=String \((.*?)\).*?android\.text=String \((.*?)\)'

    matches = re.findall(notification_pattern, notification_data, re.DOTALL)
    for match in matches:
        title, text = match
        notifications.append({'title': title, 'text': text})

    return notifications


# 获取并处理通知
notifications_data = get_notifications()

if notifications_data:
    notifications = extract_notification_details(notifications_data)
    if notifications:
        for notification in notifications:
            print(f"标题: {notification['title']}")
            print(f"内容: {notification['text']}")
            print("-" * 40)
    else:
        print("没有提取到通知内容")
else:
    print("未找到通知")
