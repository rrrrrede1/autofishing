import uiautomator2 as u2
import time
# 连接设备
d = u2.connect('VED7N18526003557')  # 设备序列号

d(text="我的").click()  # 根据文本查找元素并点击

# time.sleep(2)

# d(text="我卖出的").click()