import base_command as bc;
import time
# click 633 353
# bottom tiaozhan 689 557 960 628
tiaozhan_location = [689, 557, 960, 628]
if __name__ == "__main__":
    count = 0
    w = bc.init_window(bc.target_window_title)
    # bc.click_bottom(w, [633, 353, 633, 353])
    while(True):
        time.sleep(1)
        bc.screenshot(w, tiaozhan_location).save("bottom.png")
        if bc.compare_images("bottom.png", bc.bottom_dir + "/tiaozhan.png"):
            bc.click_bottom(w, tiaozhan_location)
            print("开始第%d次挑战" % count)
            count = count + 1
        else:
            bc.click_bottom(w, [633, 353, 633, 353])