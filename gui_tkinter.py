import tkinter, win32api, win32con, pywintypes


def close_window(event):
    key = event.keysym
    print(f"按键按下：{key}")
    # event.widget.master.destroy()

label = tkinter.Label(text='Text on the screen', font=('Times New Roman','80'), fg='black', bg='white')
# 全屏显示，消除边框
label.master.overrideredirect(True)
# 设置位置
label.master.geometry("100x100+750+250")
# 保持在最上层
label.master.lift()
# 窗口置顶
label.master.wm_attributes("-topmost", True)
# 窗口禁用
label.master.wm_attributes("-disabled", True)
# 透明色
label.master.wm_attributes("-transparentcolor", "white")
# 获取窗口句柄
hWindow = pywintypes.HANDLE(int(label.master.frame(), 16))
# The WS_EX_TRANSPARENT flag makes events (like mouse clicks) fall through the window.
exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED  | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
# exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT

win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)

label.pack()
# 绑定esc键退出
label.bind("<KeyPress>", close_window)
label.mainloop()