# 2024.09.24
# 专门用于处理条件指令

def translate_if_cmd(ifname, iftarget, ifcmd, skill_list, now_pos, character_name):
    trans_cmd = max(iftarget, ifcmd, skill_list, now_pos, character_name)
    trans_cmd[1] = ifname
    return trans_cmd



# 取最大DP的角色
def max(iftarget, ifcmd, skill_list, now_pos, character_name):
    # 获得target里所有角色的位置
    trans_cmd = [0]
    target_pos = []
    for i in range(0, len(iftarget)):
        target_pos.append(now_pos.index(character_name.index(iftarget[i])))
    target_pos.sort()
    trans_cmd.append("max")
    trans_cmd.append(target_pos)
    trans_cmd.append(0)
    return trans_cmd
    