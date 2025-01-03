import json
import yaml
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


# 加载外部 JSON 文件中的 capabilities 配置
def load_capabilities_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            capabilities = json.load(file)
        print(f"成功加载配置：{capabilities}")
        return capabilities
    except Exception as e:
        print(f"加载配置失败，原因：{e}")
        return None

# 加载 YAML 文件并返回内容
def load_yaml_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        print(f"成功加载 YAML 文件：{file_path}")
        return data
    except Exception as e:
        print(f"加载 YAML 文件失败，原因：{e}")
        return None

# 加载 capabilities 和 YAML 数据
capabilities = load_capabilities_from_file("capabilities.json")
yaml_data = load_yaml_from_file("data.yaml")

if not capabilities or not yaml_data:
    exit("无法加载配置或数据，程序退出。")

# 创建 UiAutomator2Options 对象并加载 capabilities
options = UiAutomator2Options().load_capabilities(capabilities)

# 启动 Appium 会话
driver = webdriver.Remote("http://127.0.0.1:4723", options=options)


def launch_activity(package_name, activity_name):

   # 启动指定的 Activity
    try:
        command = f"adb shell am start -n {package_name}/{activity_name}"
        print(f"启动应用命令：{command}")
        import os
        os.system(command)
        driver.implicitly_wait(5)  # 等待启动完成
        print(f"成功启动 {package_name}/{activity_name}")
    except Exception as e:
        print(f"启动 Activity 失败，原因：{e}")


def click_element(selector, timeout=10):
    """使用 UiSelector 定位元素并点击"""
    try:
        # 等待元素可见且可点击
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, selector))
        )
        element.click()
        print(f"成功点击元素：{selector}")
    except Exception as e:
        print(f"点击元素失败，原因：{e}")
        # 在调试时打印出更多信息
        if "no such element" in str(e).lower():
            print("无法找到元素，请检查选择器是否正确。")
        elif "element click intercepted" in str(e).lower():
            print("元素点击被拦截，可能被遮挡。")
        else:
            print("其他错误，请检查日志输出。")


def get_content_desc_from_page(timeout=10):
    """获取页面中所有元素的 content-desc 属性"""
    try:
        elements = driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("")')  # 查找所有有 description 的元素
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
    """根据 content-desc 和 YAML 中的 text 匹配，返回对应的 link"""
    for entry in yaml_data:
        text = entry.get('text')
        link = entry.get('link')

        if not text or not link:
            continue  # 如果没有 text 或 link 跳过

        for content_desc in content_desc_list:
            if text in content_desc:  # 如果 content-desc 包含 text
                print(f"匹配成功：content-desc='{content_desc}' 对应 text='{text}'")
                return link  # 返回匹配的 link
    return None  # 如果没有找到匹配的链接，则返回 None


def set_clipboard_text(text):
    """将文本设置到剪贴板"""
    driver.set_clipboard(text.encode('utf-8'))
    print(f"成功将文本 '{text}' 设置到剪贴板。")


def paste(link):
    try:
        # 获取当前焦点所在的元素，假设是输入框
        element = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("想跟TA说点什么...")')

        # 聚焦到该元素
        element.click()

        # 创建 ActionChains 实例
        actions = ActionChains(driver)

        # 模拟 CTRL+V 操作
        actions.send_keys(link).perform()

        print("成功模拟 Ctrl+V 粘贴操作")

    except Exception as e:
        print(f"操作失败，原因：{e}")


def go_back_to_main_activity(target_activity=".maincontainer.activity.MainActivity", max_attempts=5):

   # 返回到指定的目标 Activity，如果不在目标界面，则按返回键返回
    attempts = 0
    while attempts < max_attempts:
        current_activity = driver.current_activity
        print(f"当前 Activity: {current_activity}")
        if current_activity == target_activity:
            print(f"已经返回到目标界面：{target_activity}")
            return
        driver.back()  # 按返回键
        driver.implicitly_wait(1)  # 等待一秒，避免返回过快
        attempts += 1
    print(f"未能返回到目标界面，当前 Activity: {driver.current_activity}")

# 确保在主界面
if driver.current_activity != ".maincontainer.activity.MainActivity":
    print("当前不在目标主界面，启动主界面...")
    launch_activity("com.taobao.idlefish", ".maincontainer.activity.MainActivity")
else:
    print("已经在目标主界面，无需重新启动。")

# 点击“我的”按钮
click_element('new UiSelector().resourceId("com.taobao.idlefish:id/tab_icon").instance(3)')

# 点击“我卖出的”按钮
click_element('new UiSelector().descriptionContains("我卖出的")')

# 点击“待发货”按钮
click_element('new UiSelector().descriptionContains("待发货")')

# 2. 获取页面中所有 content-desc
content_desc_list = get_content_desc_from_page()

# 3. 根据 content-desc 和 YAML 文件中的 text 匹配，得到合适的 link
link_to_paste = find_link_from_yaml(content_desc_list, yaml_data)


set_clipboard_text(link_to_paste)


click_element('new UiSelector().descriptionContains("等待卖家发货")')


click_element('new UiSelector().className("android.widget.ImageView").instance(10)')


if link_to_paste:
    click_element('new UiSelector().description("想跟TA说点什么...")')
    paste(link_to_paste)
    click_element('new UiSelector().description("发送")')
    print("发送成功")
else:
    print("未找到有效的链接，无法粘贴")


click_element('new UiSelector().description("去发货")')


go_back_to_main_activity()

# 关闭会话
driver.quit()