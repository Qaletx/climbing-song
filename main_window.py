from threading import Thread
import sys
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog, QApplication
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from reptile import Ui_Form
class MainWindow(QWidget,Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi_2()
    def setupUi_2(self):
        #初始化控件
        self.label_back = QLabel(self)
        self.label_back.setObjectName("back_ground")
        self.label_back.resize(self.geometry().width(), self.geometry().height())

        self.label_back2 = QLabel(self)
        self.label_back2.setObjectName("back_ground2")
        self.label_back2.resize(self.geometry().width(), self.geometry().height())
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.pushButton_3.setText("")
        self.pushButton_4.setText("")
        self.pushButton_5.setText("")
        self.icon1 = QIcon("./image/最小化.png")
        self.icon2 = QIcon("./image/最大化all.png")
        self.icon3 = QIcon("./image/关  闭.png")
        self.icon4 = QIcon("./image/最大化s.png")
        self.icon5 = QIcon("./image/搜索--1.png")
        self.icon6 = QIcon("./image/文件.png")
        self.pushButton_3.setIcon(self.icon1)
        self.pushButton_4.setIcon(self.icon2)
        self.pushButton_5.setIcon(self.icon3)
        self.pushButton.setIcon(self.icon5)
        self.pushButton_2.setIcon(self.icon6)
        self.textBrowser.setPlaceholderText("信息提示...\n")
        self.lineEdit.setPlaceholderText("关键词")
        self.lineEdit_2.setPlaceholderText("文件夹路径")
        self.pushButton.setText("")
        self.pushButton_2.setText("")
        self.setWindowOpacity(0.95)
        self.event_self()    #事件监听


    def event_self(self):

        #槽
        def reptile_song():
            def download(name, image_url, mp3_url):
                file_name_mp3 = self.lineEdit_2.text() +'/' + name + ".mp3"
                file_name_jpg = self.lineEdit_2.text() +'/'  + name + ".jpg"
                with open(file_name_jpg, 'wb') as file:
                    file.write(requests.get(image_url).content)

                with open(file_name_mp3, 'wb') as file:
                    file.write(requests.get(mp3_url).content)

            self.lineEdit.setEnabled(False)
            self.lineEdit_2.setEnabled(False)
            self.pushButton.setEnabled(False)
            self.pushButton_2.setEnabled(False)
            op = Options()
            op.add_argument("--headless")
            op.add_argument("--disbale-gpu")  # 经验证这行不加也成
            op.add_argument(r"user-data-dir=C:\Users\33001\AppData\Local\Google\Chrome\User Data")
            # 此为提取平时所用的浏览器历史，并设置该浏览器的调用，注意要关闭全部该浏览器不然会报错
            web = Chrome(options=op)

            web.get("https://www.kugou.com/")

            time.sleep(1)
            web.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]/div/input").send_keys(self.lineEdit.text(), Keys.ENTER)
            time.sleep(1)
            lis = web.find_elements_by_xpath('html/body[1]/div[4]/div[1]/div[2]/ul[2]/li')
            print(lis)
            with ThreadPoolExecutor(40) as t:
                for i in lis:
                    i.find_element_by_xpath("./div[1]/a[1]").click()
                    time.sleep(1)
                    web.switch_to.window(web.window_handles[-1])
                    try:
                        image_url = web.find_element_by_xpath(
                            '/html/body/div[1]/div[3]/div[1]/div[1]/div[1]/a/img').get_attribute("src")
                        mp3_url = web.find_element_by_xpath('//*[@id="myAudio"]').get_attribute("src")
                        name_singer = web.find_element_by_xpath(
                            '/html/body/div[1]/div[3]/div[1]/div[1]/div[3]/div/div[1]').get_attribute("title")
                        name_song = web.find_element_by_xpath(
                            '/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/span').get_attribute("title")
                        name = name_singer + '-' + name_song
                        self.textBrowser.append(f"{name}下载成功\n")
                    except:
                        continue
                    finally:
                        web.close()
                        time.sleep(1)
                        web.switch_to.window(web.window_handles[0])
                    t.submit(download, name, image_url, mp3_url)
                web.quit()

            self.textBrowser.append("爬取完成...\n")
            self.lineEdit.setEnabled(True)
            self.lineEdit_2.setEnabled(True)
            self.pushButton.setEnabled(True)
            self.pushButton_2.setEnabled(True)


        def p_reptile_song():
            self.textBrowser.clear()
            if self.lineEdit.text() != "" and self.lineEdit_2.text() != "":
                t = Thread(target=reptile_song)
                t.start()
                self.textBrowser.append("连接系统中...\n")
                time.sleep(1)
                self.textBrowser.append("请稍等...\n")
                time.sleep(1)
                self.textBrowser.append("连接成功...\n")
                time.sleep(1)
                self.textBrowser.append("开始爬取...\n")
            else:
                self.textBrowser.append("请输入正确的关键词或路径\n")
                self.lineEdit.clear()
                self.lineEdit_2.clear()
                return


        def file_path():
            serve = QFileDialog.getExistingDirectory(self,"选择一个文件夹存放歌曲","./")
            self.lineEdit_2.setText(serve)


        def max_minC():
            if MainWindow.MAX_MIN_CHANGE == 1:
                self.setWindowState(Qt.WindowFullScreen)
                self.label_back.resize(self.geometry().width(), self.geometry().height())
                self.label_back2.resize(self.geometry().width(), self.geometry().height())

                self.pushButton_4.setIcon(self.icon4)
            else:
                self.setWindowState(Qt.WindowNoState)
                self.label_back.resize(self.geometry().width(), self.geometry().height())
                self.label_back2.resize(self.geometry().width(), self.geometry().height())
                self.pushButton_4.setIcon(self.icon2)
            MainWindow.MAX_MIN_CHANGE = -MainWindow.MAX_MIN_CHANGE





        #信号监听
        self.pushButton_3.clicked.connect(lambda: self.setWindowState(Qt.WindowMinimized))
        self.pushButton_4.clicked.connect(max_minC)
        self.pushButton_5.clicked.connect(lambda: self.close())
        self.pushButton.clicked.connect(p_reptile_song)
        self.pushButton_2.clicked.connect(file_path)
        self.lineEdit.returnPressed.connect(lambda : self.pushButton.click())   #可见回车并不会输入到文本框中
        self.lineEdit_2.returnPressed.connect(lambda :self.pushButton_2.click())


    #重写父类事件，窗口拖动
    def mousePressEvent(self,evt):
        if evt.button() == Qt.LeftButton and evt.y() < 50:
            MainWindow.MOUSE_MOVE = 1
            self.window_x = self.x()
            self.window_y = self.y()
            self.m_global_x = evt.globalX()
            self.m_global_y = evt.globalY()

    def mouseMoveEvent(self,evt):
        if MainWindow.MOUSE_MOVE == 1:
            self.now_window_x_num = evt.globalX() - self.m_global_x
            self.now_window_y_num = evt.globalY() - self.m_global_y
            self.move(self.window_x+self.now_window_x_num,self.window_y+self.now_window_y_num)
    def mouseReleaseEvent(self,evt):
        MainWindow.MOUSE_MOVE = 0





    #类属性，枚举值
    MOUSE_MOVE = 0
    MAX_MIN_CHANGE = 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    #读入qss文件样式
    with open("style.qss","r",encoding="utf-8") as file:
        content = file.read()
        app.setStyleSheet(content)
    sys.exit(app.exec_())