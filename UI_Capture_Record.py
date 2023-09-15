import tkinter as tk
from tkinter import filedialog
from threading import Thread
import pyautogui
import time
import cv2
import numpy as np


class ScreenCaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Capture App")
        self.root.geometry("400x200")

        # Tạo các thành phần giao diện
        self.capture_button = tk.Button(
            root, text="Chụp ảnh màn hình", command=self.capture_screen)
        self.record_button = tk.Button(
            root, text="Quay màn hình", command=self.record_screen)
        self.quit_button = tk.Button(root, text="Thoát", command=root.quit)

        # Đặt vị trí của các thành phần giao diện
        self.capture_button.pack(pady=20)
        self.record_button.pack(pady=20)
        self.quit_button.pack(pady=20)

    def capture_screen(self):
        file_name = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if file_name:
            # Thực hiện chụp màn hình trong một luồng riêng biệt
            capture_thread = Thread(
                target=self._capture_screen, args=(file_name,))
            capture_thread.start()

    def _capture_screen(self, file_name):
        # Đợi 5 giây để bạn có thời gian chuyển đến cửa sổ bạn muốn chụp
        time.sleep(5)

        # Chụp ảnh màn hình và lưu vào file
        screenshot = pyautogui.screenshot()
        screenshot.save(file_name)

        print(f"Đã chụp ảnh màn hình và lưu thành công vào {file_name}")

    def record_screen(self):
        file_name = filedialog.asksaveasfilename(
            defaultextension=".avi", filetypes=[("AVI Files", "*.avi")])
        if file_name:
            # Thực hiện quay màn hình trong một luồng riêng biệt
            record_thread = Thread(
                target=self._record_screen, args=(file_name,))
            record_thread.start()

    def _record_screen(self, file_name):
        # Khởi tạo VideoWriter để ghi video
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        # Kích thước màn hình, bạn có thể điều chỉnh
        screen_size = (1920, 1080)
        out = cv2.VideoWriter(file_name, fourcc, 20.0, screen_size)

        while True:
            # Chụp màn hình và chuyển thành mảng numpy
            screenshot = pyautogui.screenshot()
            frame = np.array(screenshot)

            # Đảo ngược kích thước mảng để đúng với kích thước màn hình
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)

            # Thoát vòng lặp nếu người dùng nhấn phím "q"
            if cv2.waitKey(1) == ord("q"):
                break

        out.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenCaptureApp(root)
    root.mainloop()
