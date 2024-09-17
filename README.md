HBR-auto脚本
===========================
觉得有用能否给个star
##### 如何运行
1. 一个正常的python环境，python、conda、miniconda皆可，本代码使用python3.11
2. 下载本代码至非中文目录文件夹
3. 安装python依赖包，pip install requirements.txt，仍然报错缺什么装什么
4. 调整游戏至1280x720分辨率，**windows在100%缩放**
5. 根据功能运行合适的脚本，打分使用python score.py
6. 配置好队伍，进入打分，脚本自动运行

##### 相关链接
本期作业轴与技能顺序配置：https://docs.qq.com/sheet/DWU5KeGd4RHpZYkZt?tab=whe4fs 
v1.1懒人包：https://pan.baidu.com/s/1QSRvE62sn95zXgVPZX5r-g?pwd=rppe 提取码: rppe 
v1.0懒人包：https://pan.baidu.com/s/1JpuXL-5vWZ6ln_5HcGSchw?pwd=pjfz 提取码: pjfz       
b站运行视频：https://www.bilibili.com/video/BV1Jh4UecEaR/   
nga说明文章：https://nga.178.com/read.php?tid=41675664

##### 怎么配置自己的作业
~~打开config.yaml，如本期的score.py中59B打分，作业轴中每行包含三组，每组四个数字，分别代表x1号位置，上x2号人，释放第x3个技能，给x4角色~~    
~~有代码能力的可以自己修改~~   
按照模板配置actions.xlsx，运行python skill_list.py --log true，将输出指令在cmd_list.txt中，如果有bug，带上轴找作者反馈    
复制到config.yaml的打分技能列表区（70-85行），保证**对齐对齐对齐**，这样就有自己的专属作业了   
##### 环境依赖
python
一些常见库，opencv, pyautogui, win32api等等

##### 计划实现功能
- [X] 脚本基础操作实现
    - [x] 窗口查找、信息查看
    - [x] 键鼠操作模拟
    - [x] 识别图片，比较图库相似度
    - [x] 基础操作序列自动执行
- [ ] 简单日常脚本
    - [x] 脚本配置文件设计与执行
    - [x] 时修竞技场 demo
    - [x] 亚历山大石 demo
    - [ ] ...
- [ ] 高级日常脚本
    - [ ] ~~迷宫自动寻路~~
    - [ ] ~~迷宫自动出招~~
    - [x] 打分刷100w徽章
    - [ ] ...

##### 目录结构描述
├── Readme.md                   // help
├── score.py                    // 打分脚本实现，进入战斗界面，运行脚本即可
├── daily.py                    // 日常脚本实现  
├── base_command.py             // 基础的脚本操作指令实现  
├── scene                       // 个人用来截图找坐标的图片  
├── bottom                      // 需要寻找按钮比对的图片  
├── config.yaml                 // 配置文件，包含按钮坐标，日常脚本配置  
└── ...  

##### 更新情况
2024.1.11 编写基础脚本操作指令，手工实现时修脚本     
2024.1.12 编写通用的日常脚本与配置，实现了自动配置时修
          实现宝石棱镜战demo，开始构思地下城脚本  
2024.9.15 根据59B行动轴，设计了5带1纯路人稳定100w脚本
2024.9.17 v1.1：修复了有些电脑上的粘键，行动开始的判断更准了，增加了根据行动轴自动生成指令的功能
...