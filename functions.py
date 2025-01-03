import json
import yaml
import re
import subprocess
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def load_capabilities_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            capabilities = json.load(file)
        print(f"成功加载配置：{capabilities}")
        return capabilities
    except Exception as e:
        print(f"加载配置失败，原因：{e}")
        return None


def load_yaml_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        print(f"成功加载 YAML 文件：{file_path}")
        return data
    except Exception as e:
        print(f"加载 YAML 文件失败，原因：{e}")
        return None


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


def launch_activity(package_name, activity_name):
    try:
        command = f"adb shell am start -n {package_name}/{activity_name}"
        print(f"启动应用命令：{command}")
        import os
        os.system(command)
    except Exception as e:
        print(f"启动 Activity 失败，原因：{e}")


def click_element(driver, selector, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, selector))
        )
        element.click()
        print(f"成功点击元素：{selector}")
    except Exception as e:
        print(f"点击元素失败，原因：{e}")


def get_content_desc_from_page(driver, timeout=10):
    try:
        elements = driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("")')
        content_desc_list = []
        for element in elements:
            content_desc = element.get_attribute("content-desc")
            if content_desc:
                content_desc_list.append(content_desc)
        return content_desc_list
    except Exception as e:
        print(f"获取 content-desc 失败，原因：{e}")
        return []


def find_link_from_yaml(content_desc_list, yaml_data):
    for entry in yaml_data:
        text = entry.get('text')
        link = entry.get('link')

        if not text or not link:
            continue

        for content_desc in content_desc_list:
            if text in content_desc:
                print(f"匹配成功：content-desc='{content_desc}' 对应 text='{text}'")
                return link
    return None


def set_clipboard_text(driver, text):
    driver.set_clipboard(text.encode('utf-8'))
    print(f"成功将文本 '{text}' 设置到剪贴板。")


def paste(driver, link):
    try:
        element = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("想跟TA说点什么...")')
        element.click()

        actions = ActionChains(driver)
        actions.send_keys(link).perform()

        print("成功模拟 Ctrl+V 粘贴操作")

    except Exception as e:
        print(f"操作失败，原因：{e}")


def go_back_to_main_activity(driver, target_activity=".maincontainer.activity.MainActivity", max_attempts=5):
    attempts = 0
    while attempts < max_attempts:
        current_activity = driver.current_activity
        print(f"当前 Activity: {current_activity}")
        if current_activity == target_activity:
            print(f"已经返回到目标界面：{target_activity}")
            return
        driver.back()
        attempts += 1
    print(f"未能返回到目标界面，当前 Activity: {driver.current_activity}")
