import base_command as bc;
import time
import numpy as np
class dungeon:
    def __init__(self, window):
        self.w = window
        self.config = bc.read_config(bc.config_path)['dungeon']
        self.dungeon_config = self.config['dungeon']
        self.shanguang = np.array([1, 0, 1, 0, 0, 0])

    def set_SP(self, SP):
        self.SP = SP
    
    def once_attack_sp(self, used_skill):
        # 闪光角色SP+1
        self.SP = self.SP + self.shanguang
        # 先驱
        self.SP[3:6] = self.SP[3:6] + np.array([1, 1, 1])
        # 第一回合技能
        skill_sp = used_skill[0]

if __name__ == "__main__":
    w = bc.init_window(bc.target_window_title)
    # bc.click_bottom(w, bc.bottom["ditu"])
    # time.sleep(0.5)
    # bc.click_img_in_scene(w, './bottom/dungeon-40.jpg')
    # bc.key_down_up_n(bc.keyboard["D"], 1)
    # bc.key_down_up_n(bc.keyboard["enter"], 1)
    # bc.key_down_up_n(bc.keyboard["enter"], 1)
    w.set_SP(np.array([6, 1, 2, 15, 14, 15]))

