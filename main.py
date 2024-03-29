import sys
import csv
import time
import random
import sqlite3
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QDialog, QLineEdit, QMessageBox, QComboBox, QGridLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

conn = sqlite3.connect('users.db')
cursor = conn.cursor() #Создаем курсор к базе данных из файла users.db

#Начальное окно
class StartWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        #Устанавливаем интерфейс

        self.setWindowTitle('Лас Вегас')
        self.setGeometry(200, 200, 450, 450)

        self.setStyleSheet("background-color: black;")

        layout = QVBoxLayout()

        banner = QLabel()
        background_image = QPixmap("lasvegas_banner.png")
        banner.setPixmap(background_image)

        register_button = QPushButton('Зарегестрироваться')
        register_button.setStyleSheet("font: bold 12px; color: red; background-color: white;")
        register_button.clicked.connect(self.open_register_window)

        login_button = QPushButton('Войти')
        login_button.setStyleSheet("background-color: white;")
        login_button.clicked.connect(self.open_login_window)

        layout.addWidget(banner)
        layout.addWidget(register_button)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def open_register_window(self):
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()

    def open_login_window(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

#Окно авторизации
class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        #Устанавливаем интерфейс

        self.setStyleSheet("background-color: black;")
        self.setGeometry(200, 200, 300, 100)
        self.setWindowTitle('Лас Вегас - Вход')

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setStyleSheet("font: bold 12px; background-color: white")
        self.password_input = QLineEdit()
        self.password_input.setStyleSheet("font: bold 12px; background-color: white")

        self.password_input.setEchoMode(QLineEdit.Password)

        login_label = QLabel('Логин:')
        login_label.setStyleSheet("font: bold 12px; color: white")
        password_label = QLabel('Пароль:')
        password_label.setStyleSheet("font: bold 12px; color: white")

        layout.addWidget(login_label)
        layout.addWidget(self.username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)

        enter_button = QPushButton('Войти')
        enter_button.setStyleSheet("font: bold 12px; color: red; background-color: white;")
        enter_button.clicked.connect(self.login)

        back_button = QPushButton('На главную страницу')
        back_button.setStyleSheet("font: bold 12px; color: red")
        back_button.clicked.connect(self.back)

        layout.addWidget(enter_button)
        layout.addWidget(back_button)
        self.setLayout(layout)

    def back(self):
        self.login_window = StartWindow()
        self.login_window.show()
        self.close()
    
    def login(self):
        user_name = self.username_input.text()
        password = self.password_input.text()

        if not user_name or not password:
            self.window = MyDialog('Введите логин и пароль')
            self.window.show()
            self.window.close()

        else:
            #Проверка логина и пароля
            with open('users.csv', 'r') as file:
                reader = list(csv.reader(file, delimiter=';', quotechar='"'))

                users = list(map(lambda i: i[0], reader))
                passwords = list(map(lambda i: i[1], reader))
                coins = list(map(lambda i: i[2], reader))

                if user_name not in users:
                    #Ошибка в логине
                    self.window = MyDialog('Такого пользователя не существует')
                    self.window.show()
                    self.window.close()

                    self.username_input.setText('')
                    self.password_input.setText('')

                else:
                    if passwords[users.index(user_name)] == password:
                        self.window = MainWindow(int(coins[users.index(user_name)]), user_name)
                        self.window.show()
                        self.close()
                    else:
                        #Ошибка в пароле 
                        self.window = MyDialog('Неправильный пароль')
                        self.window.show()
                        self.window.close()

                        self.password_input.setText('')


#Окно регистрации
class RegisterWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        #Устанавливаем интерфейс

        self.setStyleSheet("background-color: black;")
        self.setGeometry(200, 200, 300, 100)
        self.setWindowTitle('Лас Вегас - Регистрация')

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setStyleSheet("font: bold 12px; background-color: white")
        self.password_input = QLineEdit()
        self.password_input.setStyleSheet("font: bold 12px; background-color: white")

        self.password_input.setEchoMode(QLineEdit.Password)

        login_label = QLabel('Логин:')
        login_label.setStyleSheet("font: bold 12px; color: white")
        password_label = QLabel('Пароль:')
        password_label.setStyleSheet("font: bold 12px; color: white")

        layout.addWidget(login_label)
        layout.addWidget(self.username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)

        create_button = QPushButton('Создать')
        create_button.setStyleSheet("font: bold 12px; color: red; background-color: white")
        create_button.clicked.connect(self.create_user)

        back_button = QPushButton('На главную страницу')
        back_button.setStyleSheet("font: bold 12px; color: red")
        back_button.clicked.connect(self.back)

        layout.addWidget(create_button)
        layout.addWidget(back_button)
        self.setLayout(layout)

    def create_user(self):
        user_name = self.username_input.text()
        password = self.password_input.text()

        if not user_name or not password:
            self.window = MyDialog('Введите логин и пароль')
            self.window.show()
            self.window.close()

        else:
            with open('users.csv', 'r') as file:
                reader = csv.reader(file, delimiter=';', quotechar='"')
                users = list(map(lambda i: i[0], reader))

            #Проверка логина и пароля
            if user_name in users:
                #Ошибка ввода логина
                self.window = MyDialog('Такой пользователь уже существует')
                self.window.show()
                self.window.close()

                self.username_input.setText('')

            else:
                with open('users.csv', 'a') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow([user_name, password, 10])

                #Добавляем в базу данных пользователя
                cursor.execute("INSERT INTO users (login, password, coins, level_id) VALUES (?, ?, ?, ?)", (user_name, password, '10', '1'))
                conn.commit()
    
                self.rules_window = RulesWindow(user_name)
                self.rules_window.show()
                self.close()
    
    def back(self):
        self.login_window = StartWindow()
        self.login_window.show()
        self.close()
        

#Окно игры
class MainWindow(QWidget):
    def __init__(self, coin, user, parent=None):
        super().__init__(parent)
        #Устанавливаем интерфейс

        self.setStyleSheet("background-color: black;")

        self.setGeometry(200, 200, 800, 600)
        self.user = user
        self.coin = coin

        self.setWindowTitle('Лас Вегас - Игра')

        layout = QVBoxLayout() 

        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()
        layout4 = QHBoxLayout()
        layout5 = QHBoxLayout()
        layout6 = QHBoxLayout()
        layout7 = QHBoxLayout()
        
        self.coins = QLabel()
        self.coins.setText(str(self.coin))
        self.coins.setStyleSheet("font: bold 12px; color: white")
        layout1.addWidget(self.coins)

        self.comboBox = QComboBox()
        self.comboBox.addItems(['1', '2', '3', '4', '5', '6'])
        self.comboBox.setStyleSheet("font: bold 12px; background-color: white")
        layout2.addWidget(self.comboBox)

        self.bet = QLineEdit('')
        self.bet.setStyleSheet("font: bold 12px; color: white")
        layout3.addWidget(self.bet)

        self.number1_label = QLabel()
        self.number1_label.setStyleSheet("font: bold 12px; color: white")
        layout4.addWidget(self.number1_label)

        self.number2_label = QLabel()
        self.number2_label.setStyleSheet("font: bold 12px; color: white")
        layout4.addWidget(self.number2_label)

        self.number1_pic = QLabel()
        layout5.addWidget(self.number1_pic)

        self.number2_pic = QLabel()
        layout5.addWidget(self.number2_pic)

        self.status = QLabel()
        layout6.addWidget(self.status)

        self.play_button = QPushButton('Играть')
        self.play_button.setStyleSheet("font: bold 12px; color: red; background-color: white")
        self.play_button.clicked.connect(self.play_game)

        back_button = QPushButton('Закончить игру')
        back_button.setStyleSheet("font: bold 12px; color: black; background-color: white")
        back_button.clicked.connect(self.rating)

        layout7.addWidget(self.play_button)
        layout7.addWidget(back_button)

        layout.addLayout(layout1)
        layout.addLayout(layout3)
        layout.addLayout(layout2)
        layout.addLayout(layout4)
        layout.addLayout(layout5)
        layout.addLayout(layout6)
        layout.addLayout(layout7)

        self.setLayout(layout)

    def keyPressEvent(self, event):
        #Проверка нажатие кнопки (если нажата, начинаем игру)
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            self.play_game()

    def rating(self):
        #Обновление пользовательские данные
        cursor.execute("UPDATE users SET coins = ? WHERE login = ?", (str(self.coin), self.user))
        conn.commit()

        with open('users.csv', 'r') as file:
            reader = list(csv.reader(file, delimiter=';', quotechar='"'))

            users = list(map(lambda i: i[0], reader))

            if self.coin <= 100:
                id_lev = 1
            elif self.coin >= 100 and self.coin <= 10000:
                id_lev = 2
            elif self.coin >= 10000:
                id_lev = 3

            reader[users.index(self.user)] = [self.user, reader[users.index(self.user)][1], self.coin, id_lev]

        with open('users.csv', 'w') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(reader)

        self.rating_window = RatingWindow(self.user)
        self.rating_window.show()
        self.close()

    def play_game(self):
        try:
            #Ошибка ввода ставки
            if int(self.bet.text()) > self.coin:
                self.window = MyDialog('Недостаточно средств')
                self.window.show()
                self.bet.setText('')
                self.window.close()
                
                self.bet.setText('')

            else:
                #'Бросаем кости'
                number = self.comboBox.currentText()
                bet = self.bet.text()

                self.coins.setText(str(self.coin))
                time.sleep(1)

                #Выбор ранжомных чисел 
                number1 = str(random.randint(1, 6))
                number2 = str(random.randint(1, 6))

                self.number1_label.setText(number1)
                self.number2_label.setText(number2)

                pixmap = QPixmap(f"cube{number1}.png")
                self.number1_pic.setGeometry(200, 200, 200, 200)
                self.number1_pic.setPixmap(pixmap)

                pixmap = QPixmap(f"cube{number2}.png")
                self.number2_pic.setPixmap(pixmap)

                #Вывод статуса на экран
                if int(self.number1_label.text()) == int(self.number2_label.text()) == number:
                    self.coin += 3 * int(self.bet.text())
                    self.coins.setText(str(self.coin))
                    self.status.setStyleSheet("font: bold 12px; color: red;")
                    self.status.setText('MEGAWIN!')

                elif self.number1_label.text() == number or self.number2_label.text() == number:
                    self.coin += int(bet)
                    self.coins.setText(str(self.coin))
                    self.status.setStyleSheet("font: bold 12px; color: white;")
                    self.status.setText('WIN!')

                else:
                    self.coin -= int(bet)
                    self.coins.setText(str(self.coin))
                    self.status.setStyleSheet("font: bold 12px; color: white;")
                    self.status.setText('O-oh(')

                if self.coin <= 0:
                    self.status.setText('GAME OVER')
                    self.status.setStyleSheet("font: bold 12px; color: red;")
                    self.play_button.setEnabled(False)

        except ValueError:
            #Ошибка ввода ставки
            self.window = MyDialog('Нельзя сделать такую ставку. Ставить можно только целое число')
            self.window.show()
            self.bet.setText('')
            self.window.close()


#Окно рейтинга
class RatingWindow(QWidget):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        #Устанавливаем интерфейс

        self.setGeometry(200, 200, 400, 200)

        self.rate_score = ''
        self.user = user

        self.setStyleSheet("background-color: black;")
        self.setWindowTitle('Лас Вегас - Рейтинг')

        self.setStyleSheet("background-color: black;")

        layout = QVBoxLayout()

        rating_layout = QHBoxLayout()

        rate = QPushButton('Общий')
        rate.setStyleSheet("font: bold 12px; color: white;")
        rate.clicked.connect(self.common)
        rating_layout.addWidget(rate)

        rate = QPushButton('Beginners')
        rate.setStyleSheet("font: bold 12px; color: white;")
        rate.clicked.connect(self.beginner)
        rating_layout.addWidget(rate)

        rate = QPushButton('Mediums')
        rate.setStyleSheet("font: bold 12px; color: white;")
        rate.clicked.connect(self.medium)
        rating_layout.addWidget(rate)

        rate = QPushButton('Ultras')
        rate.setStyleSheet("font: bold 12px; color: white;")
        rate.clicked.connect(self.ultra)
        rating_layout.addWidget(rate)

        labelname = QLabel()
        labelname.setText('Рейтинг')
        labelname.setStyleSheet("font: bold 12px; color: red;")
        layout.addWidget(labelname)

        layout.addLayout(rating_layout)

        self.rates = QLabel()
        self.rates.setStyleSheet("font: bold 12px; color: black; background-color: white")
        layout.addWidget(self.rates)

        #Выводим общий рейтинг
        self.common()

        play_button = QPushButton('Играть снова')
        play_button.setStyleSheet("font: bold 12px; color: red;")
        play_button.clicked.connect(self.play_game)
        layout.addWidget(play_button)

        back_button = QPushButton('Выйти из аккаунта')
        back_button.setStyleSheet("font: bold 12px; color: white;")
        back_button.clicked.connect(self.back_to_main)
        layout.addWidget(back_button)

        rules_button = QPushButton('Правила')
        rules_button.setStyleSheet("font: bold 12px; color: red; backround-color: white")
        rules_button.clicked.connect(self.rules)
        layout.addWidget(rules_button)

        self.setLayout(layout)

    def play_game(self):
        self.window = MainWindow(int(self.coin), self.user)
        self.window.show()
        self.close()

    def back_to_main(self):
        self.start_window = StartWindow()
        self.start_window.show()
        self.close()

    def rules(self):
        self.rules_window = RulesWindow(self.user)
        self.rules_window.show()
        self.close()

    def common(self):
        with open('users.csv', 'r') as file:
            def level(id_lev):
                result = conn.execute(f"SELECT name FROM levels WHERE id = {id_lev}").fetchone()
                return result[0]

            reader = csv.reader(file, delimiter=';', quotechar='"')
            
            reader = sorted(reader, key=lambda x: int(x[2]), reverse=True)

            users = list(map(lambda i: i[0], reader))
            coins = list(map(lambda i: i[2], reader))
            levels = list(map(lambda i: i[3], reader))

            self.coin = coins[users.index(self.user)]

            rating = [f'{str(i + 1)}: {users[i]} - {str(coins[i])} ({level(levels[i])})' for i in range(len(users))]

        if not rating:
            self.rates.setText('Рейтинг пуст')
            self.rates.setStyleSheet("font: bold 12px; color: red;")
        else:
            self.rates.setText('\n'.join(rating))
        
    def beginner(self):
        #Выводим рейтинг среди beginners
        with open('users.csv', 'r') as file:
            reader = csv.reader(file, delimiter=';', quotechar='"')
            reader = list(filter(lambda i: str(i[-1]) == '1', reader))
            
            reader = sorted(reader, key=lambda x: int(x[2]), reverse=True)

            users = list(map(lambda i: i[0], reader))
            coins = list(map(lambda i: i[2], reader))

            rating = [f'{str(i + 1)}: {users[i]} - {str(coins[i])} (beginner)' for i in range(len(users))]

        if not rating:
            self.rates.setText('Рейтинг пуст')
            self.rates.setStyleSheet("font: bold 12px; color: red;")
        else:
            self.rates.setText('\n'.join(rating))
        
    def medium(self):
        #Выводим рейтинг среди mediums
        with open('users.csv', 'r') as file:
            reader = csv.reader(file, delimiter=';', quotechar='"')
            reader = list(filter(lambda i: str(i[-1]) == '2', reader))
            
            reader = sorted(reader, key=lambda x: int(x[2]), reverse=True)

            users = list(map(lambda i: i[0], reader))
            coins = list(map(lambda i: i[2], reader))

            rating = [f'{str(i + 1)}: {users[i]} - {str(coins[i])} (medium)' for i in range(len(users))]

        if not rating:
            self.rates.setText('Рейтинг пуст')
            self.rates.setStyleSheet("font: bold 12px; color: red;")
        else:
            self.rates.setText('\n'.join(rating))

    def ultra(self):
        #Выводим рейтинг среди ultras
        with open('users.csv', 'r') as file:
            reader = csv.reader(file, delimiter=';', quotechar='"')
            reader = list(filter(lambda i: str(i[-1]) == '3', reader))
            
            reader = sorted(reader, key=lambda x: int(x[2]), reverse=True)

            users = list(map(lambda i: i[0], reader))
            coins = list(map(lambda i: i[2], reader))

            rating = [f'{str(i + 1)}: {users[i]} - {str(coins[i])} (ultra)' for i in range(len(users))]

        if not rating:
            self.rates.setText('Рейтинг пуст')
            self.rates.setStyleSheet("font: bold 12px; color: red;")
        else:
            self.rates.setText('\n'.join(rating))


#Окно с правилами
class RulesWindow(QWidget):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        #Устанавливаем интерфейс

        self.setGeometry(200, 200, 200, 400)
        self.setStyleSheet("background-color: black;")
        self.user = user
        self.setWindowTitle('Лас Вегас - Правила')

        layout = QVBoxLayout()

        rules = QLabel()
        rules.setStyleSheet("font: bold 12px; color: red;")
        rules.setText('''Правила игры:
        У нового игрока автоматически 10 фишек. 
        Вы должны выбрать число и поставить на него определенную сумму (не больше, чем у вас есть).
        После клика на кнопку "играть" или "enter" бросается два кубика:
        1) Если выпало загаданное число - вы получаете столько очков, сколько поставили.
        2) Если выпало загаданное число на обоих кубиках - получаете утроенную поставленную сумму.
        3) Если "ваше" число не выпадает - вы теряете такую же сумму очков.
        
        Испытайте свою удачу!''')
        layout.addWidget(rules)

        play_button = QPushButton('Играть')
        play_button.setStyleSheet("font: bold 12px; color: red; background-color: white")
        play_button.clicked.connect(self.play_game)
        layout.addWidget(play_button)

        back_button = QPushButton('Выйти из аккаунта')
        back_button.setStyleSheet("font: bold 12px; color: red")
        back_button.clicked.connect(self.back_to_main)
        layout.addWidget(back_button)

        self.setLayout(layout)
      
    def play_game(self):
        self.window = MainWindow(10, self.user)
        self.window.show()
        self.close()

    def back_to_main(self):
        self.start_window = StartWindow()
        self.start_window.show()
        self.close()

#Окно с ошибкой
class MyDialog(QDialog):
    def __init__(self, text, parent=None):
        super(MyDialog, self).__init__(parent)

        QMessageBox.warning(self, 'Ошибка', text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = StartWindow()
    login_window.show()
    sys.exit(app.exec_())