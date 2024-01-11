import base_command as bc;
import time

config_path = "./config.yaml"
class Daily:
    def __init__(self, daily_name, window):
        self.w = window
        self.daily_name = daily_name
        self.config = bc.read_config(config_path)['daily']
        if self.daily_name not in self.config:
            print(f"找不到 '{self.daily_name}' 的配置。")
            exit()
        self.daily_config = self.config[self.daily_name]
    
    def isMainScene(self):
        return True
    
    def run(self):
        # 先检查是否在主界面
        self.isMainScene()
        # 进入日常，直到选队界面
        self.start()
        # 选队
        self.select_team()
        # 等待战斗开始
        self.wait_battle()
        # 释放技能表
        self.battle()
        # 退出战斗
        self.end()
        
    def start(self):
        bc.act_cmd_list(self.w, self.daily_config['start'])
        pass

    def select_team(self):
        bc.click_bottom(w, bc.bottom["xuandui"])
        bc.key_down_up_n(bc.keyboard['S'], int(self.daily_config['select']))
        bc.key_down_up_n(bc.keyboard["enter"], 1)
        bc.click_bottom(w, bc.bottom["chuji"])
    
    def wait_battle(self):
        time.sleep(5)
        bc.wait_until_bottom_appear(self.w, "xingdongkaishi", bc.bottom["xingdongkaishi"])

    def battle(self):
        for round_skill in self.daily_config['skill-list']:
            keyboard_list = []
            for skill in round_skill:
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
                    if(skill[2] != 0):
                        keyboard_list.append(skill[0])
                        keyboard_list.append(skill[1])
                        keyboard_list.append(skill[0])
                        bc.skillnum2keyboardlist(keyboard_list, skill[2])
                        if(skill[3] != 0):
                            keyboard_list.append(skill[3])
                    else:
                        continue
            keyboard_list.append('enter')
            bc.wait_until_bottom_appear(self.w, "xingdongkaishi", bc.bottom["xingdongkaishi"])
            bc.key_down_up_list(keyboard_list)
    
    def end(self):
        bc.act_cmd_list(self.w, self.daily_config['end'])
        pass

                    
            

if __name__ == "__main__":
    w = bc.init_window(bc.target_window_title)
    daily = Daily("shixiu", w)
    daily.start()
    daily.select_team()
    daily.wait_battle()
    daily.battle()
    daily.end()
        

