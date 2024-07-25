import base_command as bc;
import time
import numpy as np
import cv2
# import pytesseract
from PIL import ImageFilter, Image
import ddddocr
class Dungeon:
    def __init__(self, window):
        self.w = window
        self.dungeon_config = bc.read_config(bc.config_path)['dungeon']
        self.shanguang = np.array([1, 0, 1, 0, 0, 0])

    def set_SP(self, SP):
        self.SP = SP
    
    def load_skill(self):
        self.buff_skill_list = []
        self.aoe_skill_list = []
        for i in range(1, 7):
            if(self.dungeon_config['team' + str(i)]['job'] == 'buffer'):
                skill = self.dungeon_config['team' + str(i)]['skill']
                for j in skill:
                    self.buff_skill_list.append(j)
            elif(self.dungeon_config['team' + str(i)]['job'] == 'aoer'):
                skill = self.dungeon_config['team' + str(i)]['skill']
                for j in skill:
                    self.aoe_skill_list.append(j)

    def once_attack_sp(self):
        # 闪光角色SP+1，识图到时已经触发闪光，先驱
        # self.SP = self.SP + self.shanguang
        # 先驱
        # self.SP[3:6] = self.SP[3:6] + np.array([1, 1, 1])
        self.SP = self.SP + np.array([2, 2, 2, 2, 2, 2])

    def wait_battle(self):
        bc.wait_until_bottom_appear(self.w, "xingdongkaishi", bc.bottom["xingdongkaishi"], True)
        bc.key_down_up_n(bc.keyboard["O"], 1)
        time.sleep(2)

    def get_skill(self):
        pass


def get_sp_from_img(img):
    sp_location = bc.config['dungeon']['sp_location']
    img = np.array(img)
    # 按照位置切分图片并保存
    sp_img_list = []
    sp_list = []
    ocr = ddddocr.DdddOcr()
    for i in range(6):
        sp_img_list.append(img[sp_location[i][1]:sp_location[i][3], sp_location[i][0]:sp_location[i][2]])
        sp_img_list[i] = Image.fromarray(sp_img_list[i])
        sp = str2num(ocr.classification(sp_img_list[i]))
        sp_list.append(sp)
        sp_img_list[i].save(f"./sp/{i}.jpg")
    
    # 根据红色判断是否孔明欠费
    distance = np.sqrt(np.sum(np.square(img[351][548] - [185, 166, 183])))
    if(distance < 10 and sp_list[1] > 0):
        sp_list[1] = -sp_list[1]
    return np.array(sp_list)

def str2num(str):
    str = str.replace('l', '1')
    str = str.replace('I', '1')
    str = str.replace('O', '0')
    return int(str)
            


if __name__ == "__main__":
    w = bc.init_window(bc.target_window_title)
    # bc.click_bottom(w, bc.bottom["ditu"])
    # time.sleep(0.5)
    # bc.click_img_in_scene(w, './bottom/dungeon-40.jpg')
    # bc.key_down_up_n(bc.keyboard["D"], 1)
    # bc.key_down_up_n(bc.keyboard["enter"], 1)
    # bc.key_down_up_n(bc.keyboard["enter"], 1)
    dungeon = Dungeon(w)
    dungeon.load_skill()
    dungeon.wait_battle()
    img = bc.screenshot(w, [0, 0, bc.window_weight, bc.window_height])
    dungeon.set_SP(get_sp_from_img(img))
    dungeon.once_attack_sp()
    print(dungeon.SP)

