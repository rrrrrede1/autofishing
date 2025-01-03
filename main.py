import time
from functions import (
    get_notif,
    extract_notif,
    load_caps,
    load_yaml,
    click,
    get_desc,
    find_link,
    set_clipboard,
    paste_text,
    back_to_main,
)
from appium import webdriver
from appium.options.android import UiAutomator2Options


# 加载配置和 YAML 数据
caps = load_caps("capabilities.json")
yaml_data = load_yaml("data.yaml")

if not caps or not yaml_data:
    exit("无法加载配置或 YAML 数据，程序退出。")

options = UiAutomator2Options().load_capabilities(caps)
driver = webdriver.Remote("http://127.0.0.1:4723", options=options)


# 循环检测通知
while True:
    notif_data = get_notif()
    if not notif_data:
        print("未能获取通知内容，继续检测...")
        time.sleep(5)
        continue

    notifs = extract_notif(notif_data)
    if not notifs:
        print("没有有效通知，继续检测...")
        time.sleep(5)
        continue

    target_notif = next((n for n in notifs if n['title'] == "等待你发货"), None)
    if not target_notif:
        print("未找到目标通知，继续检测...")
        time.sleep(5)
        continue

    print("检测到目标通知，执行操作...")

    # 点击操作逻辑
    click(driver, 'new UiSelector().resourceId("com.taobao.idlefish:id/tab_icon").instance(3)')
    click(driver, 'new UiSelector().descriptionContains("我卖出的")')
    click(driver, 'new UiSelector().descriptionContains("待发货")')

    desc_list = get_desc(driver)
    link = find_link(desc_list, yaml_data)

    if link:
        set_clipboard(driver, link)
        click(driver, 'new UiSelector().description("想跟TA说点什么...")')
        paste_text(driver, link)
        click(driver, 'new UiSelector().description("发送")')
        print("发送成功")
    else:
        print("未找到有效链接，跳过粘贴")

    click(driver, 'new UiSelector().description("去发货")')
    back_to_main(driver)

    print("操作完成，继续检测...")
    time.sleep(5)  # 等待一段时间后继续检测
