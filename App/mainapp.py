from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QFormLayout, QDialog
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QValidator, QIntValidator

import sys
import pathlib
from datetime import datetime
from hashlib import md5

HEIGHT = 800
WIDTH = 600


class RegisterWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.setFixedSize(HEIGHT, WIDTH)

        self.email_user = QLineEdit()
        self.email_user.setValidator(QValidator())
        self.email_user.setMaxLength(50)
        self.email_user.setFont(('Consolas', 18))

        self.username = QLineEdit()
        self.username.setValidator(QValidator())
        self.username.setMaxLength(100)
        self.username.setFont(('Consolas', 18))

        self.password1 = QLineEdit()
        self.password1.setEchoMode(2)

        self.password2 = QLineEdit()
        self.password2.setEchoMode(2)

        submit_button = QPushButton('Register')
        submit_button.setFixedSize(100, 50)
        submit_button.setCheckable(True)
        submit_button.clicked.connect(self.save_form)

        go_login_window_button = QPushButton('Go to login window')
        go_login_window_button.setFixedSize(100, 50)
        go_login_window_button.setCheckable(True)
        go_login_window_button.clicked.connect(self.go_login_window)

        form = QFormLayout()
        form.addRow('Email: ', self.email_user)
        form.addRow('Username: ', self.username)
        form.addRow('Password: ', self.password1)
        form.addRow('Confirm password: ', self.password2)

        self.setLayout(form)

    def go_login_window(self):
        pass

    # Here must be validator (decorator)
    def save_form(self):
        """
        This function saves user data to file ONLY in this way: \n
        email_user \n
        username \n
        password
        :return:
        """
        if not self.password1 == self.password2:
            raise ValueError

        #     Here must be checked via decorator
        with open(f'users/{self.email_user}', 'w') as file:
            file.write(f'{self.email_user} \n')
            file.write(f'{self.username} \n')
            file.write(f'{md5(self.password1)} \n')

        self.log_register()

    def log_register(self):
        file_path = f'logs/register_logs'
        with open(file_path, 'w') as file:
            file.write(f'User with email {self.email_user} registered in in {datetime.now()} \n')


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.setFixedSize(HEIGHT, WIDTH)

        self.email_user = QLineEdit()
        self.email_user.setValidator(QValidator())
        self.email_user.setMaxLength(50)
        self.email_user.setFont(('Consolas', 18))

        self.password1 = QLineEdit()
        self.password1.setEchoMode(2)
        self.password1.setFont(('Consolas', 18))

        submit_button = QPushButton('Login')
        submit_button.setFixedSize(100, 50)
        submit_button.setCheckable(True)
        submit_button.clicked.connect(self.check_form)

        go_register_window_button = QPushButton("Aren't registered yet?")
        go_register_window_button.setFixedSize(100, 50)
        go_register_window_button.setCheckable(True)
        go_register_window_button.clicked.connect(self.go_register_window)

        form = QFormLayout()
        form.addRow('Email: ', self.email_user)
        form.addRow('Password: ', self.password1)

        self.setLayout(form)

    def go_register_window(self):
        # TODO Do navigation function at first
        self.cams = RegisterWindow()
        self.cams.show()
        self.close()

    # Here must be validator (decorator)
    def check_form(self):
        #     Here must be checked via decorator
        #     If all is right -> login()
        #     if not -> error
        self.login()

    def login(self):
        file_path = f'users/{self.email_user}'
        if pathlib.Path(file_path).exists():
            with open(file_path, 'r') as file:
                data = []
                lines = file.readlines()
                for _ in lines:
                    data.append(file.readline())

        if self.email_user == data[0] and md5(self.password1) == data[2]:
            self.log_login()
            return True

    def log_login(self):
        file_path = f'logs/user_logs'
        with open(file_path, 'w') as file:
            file.write(f'User with email {self.email_user} logged in in {datetime.now()} \n')


def create_main_window():
    app = QApplication(sys.argv)
    window = LoginWindow()

    # show window
    window.show()
    # run app
    app.exec()
