import sys
import configparser
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QAction, QWidget, QVBoxLayout, QHBoxLayout, QRadioButton, QTextEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtGui import QIcon
import pyautogui
import time
import pyperclip

CONFIG_FILE = 'config.ini'

class SystemTrayApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("反洗Q神器，版权归田阳农商行发哥所有")
        self.setWindowIcon(QIcon("icon.png"))  # 替换为你的图标文件路径

        self.initUI()

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon.png"))  # 替换为你的图标文件路径

        tray_menu = QMenu(self)
        restore_action = QAction("还原", self)
        quit_action = QAction("退出", self)

        restore_action.triggered.connect(self.show)
        quit_action.triggered.connect(QApplication.instance().quit)

        tray_menu.addAction(restore_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        self.hide()

    def initUI(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # 单选按钮
        self.low_risk_radio = QRadioButton("较低风险")
        self.medium_risk_radio = QRadioButton("中风险")
        self.other_radio = QRadioButton("其它")

        layout.addWidget(self.low_risk_radio)
        layout.addWidget(self.medium_risk_radio)
        layout.addWidget(self.other_radio)

        # 多行文本框和修改按钮
        self.txt1 = QTextEdit()
        self.txt2 = QTextEdit()
        self.txt3 = QTextEdit()

        self.txt1.setFixedHeight(60)
        self.txt2.setFixedHeight(60)
        self.txt3.setFixedHeight(60)

        self.load_config()

        self.modify_button = QPushButton("修改")
        self.modify_button.setFixedSize(100, 30)

        self.execute_button = QPushButton("执行")
        self.execute_button.setFixedSize(100, 30)

        self.modify_button.clicked.connect(self.save_config)
        self.execute_button.clicked.connect(self.execute_action)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.modify_button)
        button_layout.addWidget(self.execute_button)

        layout.addWidget(QLabel("文本框1:"))
        layout.addWidget(self.txt1)
        layout.addWidget(QLabel("文本框2:"))
        layout.addWidget(self.txt2)
        layout.addWidget(QLabel("文本框3:"))
        layout.addWidget(self.txt3)
        layout.addLayout(button_layout)

        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.setFixedWidth(600)

    def load_config(self):
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)

        self.txt1.setText(config.get('Settings', 'text1', fallback=''))
        self.txt2.setText(config.get('Settings', 'text2', fallback=''))
        self.txt3.setText(config.get('Settings', 'text3', fallback=''))

    def save_config(self):
        config = configparser.ConfigParser()
        config['Settings'] = {
            'text1': self.txt1.toPlainText(),
            'text2': self.txt2.toPlainText(),
            'text3': self.txt3.toPlainText()
        }

        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)
        self.show_message("配置已保存")

    def execute_action(self):
        if self.low_risk_radio.isChecked():
            self.low_risk_action()
        elif self.medium_risk_radio.isChecked():
            self.medium_risk_action()
        elif self.other_radio.isChecked():
            self.other_action()
        else:
            self.show_message("请选择一个风险等级")

    def low_risk_action(self):
        while True:
            # 1. 查找并移动到系统初评.png
            try:
                x, y = pyautogui.locateCenterOnScreen("act/007.png", grayscale=True, confidence=0.8, region=(0, 0, 1920, 1080))
                pyautogui.moveTo(x, y)
                print("【系统初评】位置：", x, y)
            except:
                print("【系统初评】处失败")            
                self.show_message("未找到记录")
                return

            time.sleep(1)

            # 2. 查找"小人图标.png"
            try:
                x, y = pyautogui.locateCenterOnScreen("act/004.png", grayscale=True, confidence=0.8, region=(0, 0, 1920, 1080))
                pyautogui.click(x, y)
                print("【小人图标】位置：", x, y)
            except:
                print("【小人图标】处失败")            
                self.show_message("【小人图标】处失败")
                return
                
            time.sleep(1)

            # 3. 按下END键
            pyautogui.press('end')
            
            time.sleep(1)
            
            # 4.处理客户号多个。
            while True:
                # 4.0 先看一下是否存在”未处理“
                try:
                    location = pyautogui.locateCenterOnScreen("act/006.png", grayscale=True, confidence=0.8, region=(0, 0, 1920, 1080))
                except:
                    break

                #if location is not None:
                # 4.1 找”未处理“，并点击它。
                try:
                    x, y = pyautogui.locateCenterOnScreen("act/006.png", grayscale=True, confidence=0.8, region=(0, 0, 1920, 1080))
                    print("【未处理】位置：", x, y)
                    pyautogui.click(x, y)
                except:
                    print("【未处理】处失败")
                    self.show_message("【未处理】处失败")
                    return                
                
                time.sleep(1)
                
                # 4.2 找到“处理意见.jpg”，偏移50，然后点击，再把txt1的内容复制进去
                try:
                    x, y = pyautogui.locateCenterOnScreen("act/003.png", grayscale=True, confidence=0.8, region=(0, 0, 1920, 1080))
                    print("【处理意见位置】位置：", x, y)
                    pyautogui.click(x+50, y)    # 偏移50，然后点击，再把txt1的内容复制进去
                    pyperclip.copy(self.txt1.toPlainText())
                    pyautogui.hotkey('ctrl', 'v')  # 粘贴意见
                except:
                    print("【处理意见】处失败")
                    self.show_message("【处理意见】处失败")
                    return  
                    
                
                time.sleep(1)
                    
                # 4.3 找到“保存.jpg“，点击它
                try:
                    x, y = pyautogui.locateCenterOnScreen("act/002.png", grayscale=True, confidence=0.8, region=(0, 0, 1920, 1080))
                    print("【保存】位置：", x, y)
                    pyautogui.click(x, y)
                except:
                    print("【保存】处失败")
                    self.show_message("【保存】处失败")
                    return                

                time.sleep(1)
                
            
            # 5. 找到“调整等级.png"，偏移20后点击
            try:
                x, y = pyautogui.locateCenterOnScreen("act/008.png", grayscale=True, confidence=0.8, region=(0, 0, 1920, 1080))
                pyautogui.click(x+50, y)    # 偏移50才能够找到下拉选项
                print("【调整等级】位置：", x, y)
            except:
                print("【调整等级】处失败")            
                self.show_message("【调整等级】处失败")
                return
                
            time.sleep(1)
            
            # 6. 找到"较低风险.png“，点击它
            try:
                x, y = pyautogui.locateCenterOnScreen("act/009.png", grayscale=True, confidence=0.8, region=(0, 0, 1920, 1080))
                pyautogui.click(x, y)    
                print("【较低风险】位置：", x, y)
            except:
                print("【较低风险】处失败")            
                self.show_message("【较低风险】处失败")
                return
                
            time.sleep(1)
     
            # 7. 找到"人工意见.png"，偏移50点击它
            try:
                x, y = pyautogui.locateCenterOnScreen("act/001.png", grayscale=True, confidence=0.8, region=(0, 0, 1920, 1080))
                print("【人工意见】位置：", x, y)
                pyautogui.click(x, y)
                pyperclip.copy(self.txt1.toPlainText())
                pyautogui.hotkey('ctrl', 'v')  # 粘贴意见
            except:
                print("【人工意见】处失败")            
                self.show_message("【人工意见】处失败")
                return
                
            time.sleep(1)
     
            # 8. 找到“提交.jpg“，点击它
            try:
                x, y = pyautogui.locateCenterOnScreen("act/005.png", grayscale=True, confidence=0.8, region=(0, 0, 1920, 1080))
                # pyautogui.moveTo(x, y)
                pyautogui.click(x, y)
                print("【提交】位置：", x, y)
            except:
                print("【提交】处失败")            
                self.show_message("【提交】处失败")
                return
                
            time.sleep(5)
            
            print("一个客户执行完毕执行完毕")


    def medium_risk_action(self):
        # 实现中风险操作
        self.show_message("执行中风险操作")
        # 在这里添加具体的中风险操作代码

    def other_action(self):
        # 实现其它操作
        self.show_message("执行其它操作")
        # 在这里添加具体的其它操作代码


    def show_message(self, message):
        QMessageBox.information(self, "信息", message)

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "反洗Q神器",
            "计划按F6停止",
            QSystemTrayIcon.Information,
            2000
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SystemTrayApp()
    window.show()
    sys.exit(app.exec_())
