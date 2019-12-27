import pywinauto
import sys
import time
import configparser
from pywinauto.application import Application
from pywinauto.timings import Timings
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import pyqtSlot

config = configparser.ConfigParser()
config.read("config.ini")
# demo = config.get("myvars", "demo")
user = config.get("settings", "user")
password = config.get("settings", "password")
wait = int(config.get("settings", 'wait'))
path_to_sitelink = config.get("settings", "path_to_sitelink")

demo = '.*SiteLink Web Edition.*'
Timings.window_find_timeout = 10


class App(QWidget):
    print(f'User = {user},\nPassword = {password},\nTime to relogin {wait / 60} (minutes)\n')

    def __init__(self):
        super().__init__()
        self.title = 'title'
        self.left = 300
        self.top = 300
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.labl = QLabel(self)
        self.labl.setText('abc')

        button = QPushButton('button', self)
        button.move(170, 300)
        button.clicked.connect(self.check)

        self.show()

    @pyqtSlot()
    def check(self):
        app = Application()
        try:
            app.connect(title_re=demo, visible_only=False)
            app.top_window().set_focus()
            self.labl.setText('Found running app, connection...')
            self.labl.adjustSize()
            # print('Found running app, connection...')
            self.sod()
        except pywinauto.findwindows.ElementNotFoundError:
            self.labl.setText('No running application found, starting new app...')
            self.labl.adjustSize()
            # print("No running application found, starting new app...")
            app.start(path_to_sitelink, timeout=30)
            self.sod()

    def sod(self):
        try:
            app = Application(backend="uia").connect(title_re=demo, timeout=30, visible_only=False)
            s_o_d = app.window(title_re=demo)
            app.top_window().set_focus()
            s_o_d.wait('visible')
            s_o_d.child_window(title="Continue").type_keys('{ENTER}')
            print('Found SoD found')
            self.login_program()
        except pywinauto.findwindows.ElementNotFoundError:
            print('No SoD window, Logging')
            self.login_program()

    def login_program(self):
        app = Application(backend="uia").connect(title_re=demo, timeout=30, visible_only=False)
        login = app.window(title_re=demo)
        app.top_window().set_focus()
        login.wait('visible')
        # login.print_control_identifiers()
        login.Edit0.type_keys('^a{BACKSPACE}')
        login.Edit0.set_text(f"{user}")
        login.Edit4.type_keys('^a{BACKSPACE}')
        login.Edit4.set_text(f'{password}')
        login.child_window(title="Login").type_keys('{ENTER}')
        time.sleep(wait)
        self.relogin()

    def relogin(self):
        for i in range(100):
            app = Application(backend="uia").connect(title_re=demo, timeout=30, visible_only=False)
            app_scr = app.window(title_re=demo)
            app.top_window().set_focus()
            app_scr.child_window(title="Login Credentials", auto_id="SmdGroupBox2").Edit1.type_keys('^a{BACKSPACE}')
            app_scr.child_window(title="Login Credentials", auto_id="SmdGroupBox2").Edit1.set_text(f"{user}")
            app_scr.child_window(title="Login Credentials", auto_id="SmdGroupBox2").Edit4.type_keys('^a{BACKSPACE}')
            app_scr.child_window(title="Login Credentials", auto_id="SmdGroupBox2").Edit4.set_text(f"{password}")
            app_scr.child_window(title="Login", auto_id="btnOK", control_type="Pane").type_keys('{ENTER}')
            print(f'Relogin of user {user} number {i}')
            time.sleep(wait)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

# if __name__ == '__gui__':
#     check()
#     sod()
#     login_program()
#     relogin()
