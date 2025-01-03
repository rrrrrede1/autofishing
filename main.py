from functions import (
    get_notifications,
    extract_notification_details,
    load_capabilities_from_file,
    load_yaml_from_file,
    click_element,
    get_content_desc_from_page,
    find_link_from_yaml,
    set_clipboard_text,
    paste,
    go_back_to_main_activity,
)
from appium import webdriver
from appium.options.android import UiAutomator2Options


# 检测通知
notifications_data = get_notifications()
if not notifications_data:
    exit("未能获取通知内容，程序退出。")

notifications = extract_notification_details(notifications_data)
if not notifications:
    exit("没有找到有效通知，程序退出。")

# 检查是否有标题为“等待你发货”的通知
target_notification = next((n for n in notifications if n['title'] == "等待你发货"), None)
if not target_notification:
    exit("未找到标题为“等待你发货”的通知，程序退出。")

# 加载配置文件
capabilities = load_capabilities_from_file("capabilities.json")
yaml_data = load_yaml_from_file("data.yaml")

if not capabilities or not yaml_data:
    exit("无法加载配置或 YAML 数据，程序退出。")

options = UiAutomator2Options().load_capabilities(capabilities)

# 启动 Appium 会话
driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

# 点击操作逻辑
click_element(driver, 'new UiSelector().resourceId("com.taobao.idlefish:id/tab_icon").instance(3)')
click_element(driver, 'new UiSelector().descriptionContains("我卖出的")')
click_element(driver, 'new UiSelector().descriptionContains("待发货")')

content_desc_list = get_content_desc_from_page(driver)
link_to_paste = find_link_from_yaml(content_desc_list, yaml_data)

if link_to_paste:
    set_clipboard_text(driver, link_to_paste)
    click_element(driver, 'new UiSelector().description("想跟TA说点什么...")')
    paste(driver, link_to_paste)
    click_element(driver, 'new UiSelector().description("发送")')
    print("发送成功")
else:
    print("未找到有效的链接，无法粘贴")

click_element(driver, 'new UiSelector().description("去发货")')
go_back_to_main_activity(driver)

driver.quit()
