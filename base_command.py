# 主要用于实现基础的操作命令
import pygetwindow as gw
import pyautogui as pag
import win32api
import win32con
import yaml
import time
import cv2
import numpy as np
from PIL import Image
 
config_path = "./config.yaml"
bottom_dir = "./bottom"
target_window_title = "HeavenBurnsRed"
window_height = 720
window_weight = 1280


def read_config(config_path):
    # 读取配置文件
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config

config = read_config(config_path)
bottom = config["bottom"]
keyboard = config["keyboard"]

def init_window(target_window_title):
    # 切换到目标窗口，并设置目标窗口的大小
    # target_window_title: 目标窗口的标题
    target_window = gw.getWindowsWithTitle(target_window_title)
    if target_window:
        target_window = target_window[0]
        target_window.activate()  # 切换到目标窗口
        target_window.restore() # 恢复目标窗口
        target_window.resizeTo(window_weight, window_height) # 设置目标窗口大小
        return target_window
    else:
        print(f"找不到 '{target_window_title}' 的窗口。")
        exit()


def screenshot(target_window, location):
    # 截取窗口目标区域的图像
    # target_window: 目标窗口
    # location: 目标区域的坐标 [x1, y1, x2, y2]
    # x1: 目标区域的左上角x坐标
    # y1: 目标区域的左上角y坐标
    # x2: 目标区域的右下角x坐标
    # y2: 目标区域的右下角y坐标
    return pag.screenshot(region=(target_window.left + location[0], target_window.top + location[1], location[2] - location[0], location[3] - location[1]))

def click_bottom(target_window, location):
    # 点击窗口目标区域
    # target_window: 目标窗口
    # location: 目标区域的坐标 [x1, y1, x2, y2]
    # x1: 目标区域的左上角x坐标
    # y1: 目标区域的左上角y坐标
    # x2: 目标区域的右下角x坐标
    # y2: 目标区域的右下角y坐标
    bottom_center_x = (location[0] + location[2]) / 2
    bottom_center_y = (location[1] + location[3]) / 2
    pag.click(target_window.left + bottom_center_x, target_window.top + bottom_center_y)

    time.sleep(1)

def key_down_up_n(key, times):
    # 按下并释放某个按键多次
    # key: 按键 [bvk, bScan]
    # times: 按下并释放的次数
    for i in range(times):
        win32api.keybd_event(key[0], key[1], 0, 0)
        win32api.keybd_event(key[0], key[1], win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.5)

def key_down_up_list(key_list):
    # 按下并释放某个按键列表
    # key_list: 按键列表 [按键]
    for key in key_list:
        bvk = keyboard[key][0]
        bScan = keyboard[key][1]
        win32api.keybd_event(bvk, bScan, 0, 0)
        win32api.keybd_event(bvk, bScan, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.5)


def compare_images(image1_path, image2_path, threshold):
    result = []
    # 加载并转换为灰度图像, 之后二值化处理
    img1 = cv2.imread(image1_path)
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.imread(image2_path)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # 灰度直方图算法
    # 计算单通道的直方图的相似值
    hist1 = cv2.calcHist([img1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([img2], [0], None, [256], [0.0, 255.0])
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + \
                (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    result.append(degree)
    # 有背景的图片需要二值化处理
    if(threshold != 0):
        img11 = cv2.threshold(img1, 127, 255, cv2.THRESH_BINARY)[1]
        img22 = cv2.threshold(img2, 127, 255, cv2.THRESH_BINARY)[1]
        hist1 = cv2.calcHist([img11], [0], None, [256], [0.0, 255.0])
        hist2 = cv2.calcHist([img22], [0], None, [256], [0.0, 255.0])
        # 计算直方图的重合度
        degree = 0
        for i in range(len(hist1)):
            if hist1[i] != hist2[i]:
                degree = degree + \
                    (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
            else:
                degree = degree + 1
        degree = degree / len(hist1)
        result.append(degree)

        print(result)
        if(result[0] > 0.7 and result[1] > 0.9):
            return True
        else:
            return False
        
    if(result[0] > 0.8):
        return True
    else:
        return False
    
def compare_images_by_pixel(image1_path, image2_path, pixel_list):
    img1 = np.array(Image.open(image1_path))  
    img2 = np.array(Image.open(image2_path))
    distance = []
    # 比较像素序列中的像素是否相同
    for pixel in pixel_list:
        v1 = img1[pixel[1], pixel[0]]
        v2 = img2[pixel[1], pixel[0]]
        v1 = [int(v1[0]), int(v1[1]), int(v1[2])]
        v2 = [int(v2[0]), int(v2[1]), int(v2[2])]
        # 计算两个三维向量之间的余弦相似度
        a = ((v1[0] - v2[0]) ** 2 + (int)(v1[1] - v2[1]) ** 2 + (int)(v1[2] - v2[2]) ** 2) ** 0.5 / 255   
        distance.append(a)
    print(distance)
    distance = sum(distance) / len(distance)
    print(distance)
    if(distance < 0.4):
        return True
    else:
        return False

    
    
def wait_until_bottom_appear(w, bottom_name, bottom_location, by_pixel=False):
    # 识别窗口bottom_location区域是否出现了bottom_name图片, 每隔0.5秒识别一次
    # 通过截图区域识别相似度来判断是否出现了bottom_name图片
    # w: 目标窗口
    # bottom_name: 底部按钮的名称
    # bottom_location: 底部按钮的位置

    while True:
        screenshot(w, bottom_location).save("bottom.png")
        if(by_pixel):
            if compare_images_by_pixel("./bottom.png", bottom_dir + "/" + bottom_name + ".png", config['compare'][bottom_name]):
                time.sleep(1)
                break
        else:
            if compare_images("./bottom.png", bottom_dir + "/" + bottom_name + ".png", 0):
                time.sleep(1)
                break
        time.sleep(0.5)

def act_cmd_list(w, cmd_list):
    # 执行指令列表
    # w: 目标窗口
    # cmd_list: 指令列表
    for cmd in cmd_list:
        if cmd[0] == 'B':
            location = bottom[cmd[2:]]
            click_bottom(w, location)
        if cmd[0] == 'K':
            key = keyboard[cmd[2:]]
            key_down_up_n(key, 1)
        if cmd[0] == 'W':
            location = bottom[cmd[2:]]
            wait_until_bottom_appear(w, cmd[2:], location)
        
def skillnum2keyboardlist(list, num):
    for i in range(0, num):
        list.append('S')
    list.append('enter')
    return list 

if __name__ == "__main__":
    # pass
    # w = init_window(target_window_title)

    # click_bottom(w, bottom["qianghua"])
    # click_bottom(w, bottom["shixiu"])
    # click_bottom(w, bottom["sheding"])
    # click_bottom(w, bottom["xuandui"])
    # key_down_up_n(keyboard["S"], 4)
    # key_down_up_n(keyboard["enter"], 1)
    # click_bottom(w, bottom["chuji"])

    # # sheding_location = bottom["sheding"]
    # # screenshot(w, sheding_location).save("sheding.png")
    # # xuandui_location = bottom["xuandui"]
    # # screenshot(w, xuandui_location).save("xuandui.png")
    # # click_bottom(w, bottom["xuandui"])
    # # key_down_up_n(keyboard["S"], 4)
    # # chuji_location = bottom["chuji"]
    # # screenshot(w, chuji_location).save("chuji.png")
    # # xindongkaishi_location = bottom["xindongkaishi"]
    # # screenshot(w, xindongkaishi_location).save("xindongkaishi.png")

    # time.sleep(5)
    # wait_until_bottom_appear(w, "xingdongkaishi", bottom["xingdongkaishi"])
    # # 5号位暗洛丽塔放2号位, 2号位释放2技能 key 5 2 2 s s enter
    # key_list = [keyboard[5], keyboard[2], keyboard[2], keyboard["S"], keyboard["S"], keyboard["enter"]]
    # key_down_up_list(key_list)
    # # 3号位孔明释放2技能给2号位，key3 s s enter 2
    # key_list = [keyboard[3], keyboard["S"], keyboard["S"], keyboard["enter"], keyboard[2]]
    # key_down_up_list(key_list)
    # key_down_up_n(keyboard["enter"], 1)

    # wait_until_bottom_appear(w, "xingdongkaishi", bottom["xingdongkaishi"])
    # # 1号位释放1技能， key 1 s enter
    # key_list = [keyboard[1], keyboard["S"], keyboard["enter"]]
    # key_down_up_list(key_list)
    # # 2号位释放3技能， key 2 s s s enter
    # key_list = [keyboard[2], keyboard["S"], keyboard["S"], keyboard["S"], keyboard["enter"]]
    # key_down_up_list(key_list)
    # # 3号位换6号位圣华，3号位释放2技能给2号位，key 3 6 3 s s enter 2
    # key_list = [keyboard[3], keyboard[6], keyboard[3], keyboard["S"], keyboard["S"], keyboard["enter"] ,keyboard[2]]
    # key_down_up_list(key_list)
    # key_down_up_n(keyboard["enter"], 1)

    # wait_until_bottom_appear(w, "zhandouchengguo", bottom["zhandouchengguo"])
    # click_bottom(w, bottom["zhandouchengguo"])
    # wait_until_bottom_appear(w, "zhandouchengguo", bottom["zhandouchengguo"])
    # click_bottom(w, bottom["zhandouchengguo"])
    # wait_until_bottom_appear(w, "shengdianmoshi_img", bottom["shengdianmoshi_img"])
    # pag.click(w.left + bottom["shengdianmoshi_bottom"][0], w.top + bottom["shengdianmoshi_bottom"][1])
    # time.sleep(0.5)
    # click_bottom(w, bottom["zaiwanyici"])
    pixel_list = config['compare']['xingdongkaishi']
    compare_images_by_pixel("./bottom.png", "./bottom/xingdongkaishi.png", pixel_list)