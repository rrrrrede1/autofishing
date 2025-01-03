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


def load_caps(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            caps = json.load(f)
        print(f"成功加载配置：{caps}")
        return caps
    except Exception as e:
        print(f"加载配置失败：{e}")
        return None


def load_yaml(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        print(f"成功加载 YAML：{path}")
        return data
    except Exception as e:
        print(f"加载 YAML 失败：{e}")
        return None


def get_notif():
    cmd = ["adb", "shell", "dumpsys", "notification", "--noredact"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')

    if res.returncode != 0:
        print(f"运行 adb 出错：{res.stderr}")
        return None

    return res.stdout


def extract_notif(data):
    notifs = []
    pattern = r'android\.title=String \((.*?)\).*?android\.text=String \((.*?)\)'

    matches = re.findall(pattern, data, re.DOTALL)
    for m in matches:
        title, text = m
        notifs.append({'title': title, 'text': text})

    return notifs


def start_activity(pkg, act):
    try:
        cmd = f"adb shell am start -n {pkg}/{act}"
        print(f"启动命令：{cmd}")
        import os
        os.system(cmd)
    except Exception as e:
        print(f"启动失败：{e}")


def click(driver, sel, timeout=10):
    try:
        el = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, sel))
        )
        el.click()
        print(f"点击成功：{sel}")
    except Exception as e:
        print(f"点击失败：{e}")


def get_desc(driver):
    try:
        els = driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("")')
        desc_list = []
        for el in els:
            desc = el.get_attribute("content-desc")
            if desc:
                desc_list.append(desc)
        return desc_list
    except Exception as e:
        print(f"获取 content-desc 失败：{e}")
        return []


def find_link(desc_list, yaml_data):
    for entry in yaml_data:
        text = entry.get('text')
        link = entry.get('link')

        if not text or not link:
            continue

        for desc in desc_list:
            if text in desc:
                print(f"匹配成功：content-desc='{desc}' 对应 text='{text}'")
                return link
    return None


def set_clipboard(driver, text):
    driver.set_clipboard(text.encode('utf-8'))
    print(f"剪贴板设置成功：{text}")


def paste_text(driver, text):
    try:
        el = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("想跟TA说点什么...")')
        el.click()

        actions = ActionChains(driver)
        actions.send_keys(text).perform()

        print("粘贴操作成功")
    except Exception as e:
        print(f"粘贴失败：{e}")


def back_to_main(driver, target=".maincontainer.activity.MainActivity", max_tries=5):
    tries = 0
    while tries < max_tries:
        curr = driver.current_activity
        print(f"当前 Activity: {curr}")
        if curr == target:
            print(f"已返回主界面：{target}")
            return
        driver.back()
        tries += 1
    print(f"未返回主界面，当前 Activity: {driver.current_activity}")
