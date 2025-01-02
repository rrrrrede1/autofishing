import json
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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

# 加载 capabilities
capabilities = load_capabilities_from_file("capabilities.json")
if not capabilities:
    exit("无法加载配置，程序退出。")

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


def click_element(xpath, timeout=10):

   # 等待并点击指定的元素
    try:
        # 等待元素可见
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        element.click()
        print(f"成功点击元素：{xpath}")
    except Exception as e:
        print(f"点击元素失败，原因：{e}")


def go_back_to_main_activity(target_activity=".maincontainer.activity.MainActivity", max_attempts=5):

   # 返回到指定的目标 Activity，如果不在目标界面，则按返回键返回
    attempts = 0
    while attempts < max_attempts:
        current_activity = driver.current_activity
        print(f"当前 Activity: {current_activity}")
        if current_activity == target_activity:
            print(f"已经返回到目标界面：{target_activity}")
            return
        driver.press_keycode(4)  # 按返回键
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
click_element('//android.widget.TextView[@resource-id="com.taobao.idlefish:id/tab_title" and @text="我的"]')

# 点击“我卖出的”按钮
click_element('//android.widget.ImageView[contains(@content-desc, "我卖出的")]')

# 点击“待发货”按钮
click_element('//android.view.View[contains(@content-desc, "待发货")]')


go_back_to_main_activity()

# 关闭会话
driver.quit()
