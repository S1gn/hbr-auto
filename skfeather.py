# 2024.09.15
# 参考行动轴：https://nga.178.com/read.php?tid=41656241

import base_command as bc;
import ddddocr
import time

config_path = "./config.yaml"
class SKfeather:
    def __init__(self, daily_name, window):
        self.w = window
        self.daily_name = daily_name
        self.config = bc.read_config(config_path)
        self.ocr = ddddocr.DdddOcr()
        if self.daily_name not in self.config:
            print(f"找不到 '{self.daily_name}' 的配置。")
            exit()
        self.daily_config = self.config[self.daily_name]
        # 标记上回合是否有if指令，有的话先复原
        self.if_flag = 0
        self.swap_history = []
        self.dp_list = []
        self.true_loc = {i + 1: i for i in range(6)}
    
    
    def run(self):
        # 等待战斗开始
        self.wait_battle()
        # 释放技能表
        self.battle()
        

    def select_team(self):
        bc.click_bottom(w, bc.bottom["xuandui"])
        bc.key_down_up_n(bc.keyboard['S'], int(self.daily_config['select']))
        bc.key_down_up_n(bc.keyboard["enter"], 1)
        bc.click_bottom(w, bc.bottom["chuji"])
    
    def wait_battle(self):
        time.sleep(1)
        bc.wait_until_bottom_appear(self.w, "xingdongkaishi", bc.bottom["xingdongkaishi"], True)

    def battle(self, skill_list_name):
        turns = 0
        for round_skill in self.daily_config[skill_list_name]:
            keyboard_list = []
            bc.wait_until_bottom_appear(self.w, "xingdongkaishi", bc.bottom["xingdongkaishi"], True)
            self.true_loc = {i : i for i in range(1,  7)}
            # 上一回合有条件指令，不清楚角色具体位置，先全部还原
            if self.if_flag == 1:
                print(self.swap_history)
                # 倒序执行swap_history
                for i in range(len(self.swap_history) - 1, -1, -1):
                    keyboard_list.append(self.swap_history[i][0])
                    keyboard_list.append(self.swap_history[i][1])
                bc.key_down_up_list(keyboard_list)
                time.sleep(0.5)
                keyboard_list = []
                self.if_flag = 0
                self.swap_history = []
            self.dp_list = bc.get_dp_by_percent(self.w)
            print(self.dp_list)
            for i in range(0, 3):
                skill = round_skill[i]
                if_keybord_list = []
                if skill[0] == 'O':
                    keyboard_list.append('O')
                    break
                # 判断if指令
                if skill[1] == "max1":
                    # 先根据dp大小，从大到小，排序index
                    dp_index = list(range(0, 6))
                    dp_index.sort(key=lambda x: self.dp_list[x], reverse=True)
                    # 再依次看在不在skill[2]里
                    for j in range(0, 6):
                        if dp_index[j] in skill[2]:
                            max_index = dp_index[j]
                            break
                    keyboard_list.append(skill[0])
                    print(max_index, self.true_loc)
                    max_index = self.true_loc[max_index + 1]
                    keyboard_list.append(max_index)
                    self.swap_history.append([skill[0], max_index])
                    self.if_flag = 1
                    self.true_loc[max_index] = skill[0]
                    self.true_loc[skill[0]] = max_index
                elif skill[1] == "max2":
                    # 先根据dp大小，从大到小，排序index
                    dp_index = list(range(0, 6))
                    dp_index.sort(key=lambda x: self.dp_list[x], reverse=True)
                    max_count = 0
                    # 再依次看在不在skill[2]里
                    for j in range(0, 6):
                        if dp_index[j] in skill[2]:
                            max_count += 1
                            if max_count == 2:
                                max_index = dp_index[j]
                                break
                    keyboard_list.append(skill[0])
                    print(max_index, self.true_loc)
                    max_index = self.true_loc[max_index + 1]
                    keyboard_list.append(max_index)
                    self.swap_history.append([skill[0], max_index])
                    self.if_flag = 1
                    self.true_loc[max_index] = skill[0]
                    self.true_loc[skill[0]] = max_index
                elif skill[1] == "max3":
                    # 先根据dp大小，从大到小，排序index
                    dp_index = list(range(0, 6))
                    dp_index.sort(key=lambda x: self.dp_list[x], reverse=True)
                    # 再依次看在不在skill[2]里
                    max_count = 0
                    # 再依次看在不在skill[2]里
                    for j in range(0, 6):
                        if dp_index[j] in skill[2]:
                            max_count += 1
                            if max_count == 3:
                                max_index = dp_index[j]
                                break
                    keyboard_list.append(skill[0])
                    max_index = self.true_loc[max_index + 1]
                    keyboard_list.append(max_index)
                    self.swap_history.append([skill[0], max_index])
                    self.if_flag = 1
                    self.true_loc[max_index] = skill[0]
                    self.true_loc[skill[0]] = max_index
                else:
                    # 位置不变
                    if(skill[0] == skill[1]):
                        if(skill[2] != 0):
                            keyboard_list.append(skill[1])
                            bc.skillnum2keyboardlist(keyboard_list, skill[2])
                            if(skill[3] != 0):
                                keyboard_list.append(skill[3])
                        else:
                            continue
                    else:
                        self.true_loc[skill[0]] = self.true_loc[skill[1]]
                        if(skill[2] != 0):
                            keyboard_list.append(skill[0])
                            keyboard_list.append(skill[1])
                            keyboard_list.append(skill[0])
                            bc.skillnum2keyboardlist(keyboard_list, skill[2])
                            if(skill[3] != 0):
                                keyboard_list.append(skill[3])
                        # 位置变化，但是不释放技能
                        else:
                            keyboard_list.append(skill[0])
                            keyboard_list.append(skill[1])
            
            # 回合中释放OD，先放技能，然后一直按O，直到能按出来
            if len(round_skill) == 4:
                keyboard_list.append('enter')
                bc.wait_until_bottom_appear(self.w, "xingdongkaishi", bc.bottom["xingdongkaishi"], True)
                bc.key_down_up_list(keyboard_list)
                print(f"第{turns}轮", keyboard_list)
                bc.wait_untim_bottom_and_keyboard(self.w, "xingdongkaishi", bc.bottom["xingdongkaishi"], bc.keyboard["O"], True)
                turns += 1
                time.sleep(0.5)
                # 回合中释放OD，保留上次技能，先14， 24， 34全恢复到默认
                keyboard_list = [1, 4, 1, 4, 2, 4, 2, 4, 3, 4, 3, 4]
                bc.wait_until_bottom_appear(self.w, "xingdongkaishi", bc.bottom["xingdongkaishi"], True)
                bc.key_down_up_list(keyboard_list)
                time.sleep(0.5)
                
            else:
                keyboard_list.append('enter')
                bc.wait_until_bottom_appear(self.w, "xingdongkaishi", bc.bottom["xingdongkaishi"], True)
                turns += 1
                print(f"第{turns}轮", keyboard_list)
                time.sleep(0.5)
                bc.key_down_up_list(keyboard_list)
                time.sleep(5)


                    
            

if __name__ == "__main__":
    w = bc.init_window(bc.target_window_title)
    # daily = Daily("arachnelineA", w)
    daily = SKfeather("skfeather", w)
    bc.wait_until_bottom_and_click(w, "xingdongkaishi", bc.bottom["xingdongkaishi"], "skip", True)
    daily.battle("stage1-skill-list")
    bc.wait_until_bottom_and_click(w, "xingdongkaishi", bc.bottom["xingdongkaishi"], "skip", True)
    daily.battle("stage2-skill-list")
    daily.battle("stage3-skill-list")
    daily.battle("stage4-skill-list")
    bc.wait_until_bottom_and_click(w, "xingdongkaishi", bc.bottom["xingdongkaishi"], "skip", True)
    daily.battle("stage5-skill-list")

        

