#!/usr/bin/python3

#     by Andrew Sotnikov 
#        aka Luca Brasi 
#            email: andruha.sota@mail.ru

# #               #              #              #              #              
#                ПРИЛОЖЕНИЕ ДЛЯ ПОДМЕНЫ ВРЕМЕНИ
# #               #              #              #              #              
#    Требования:

#        -установленный PyQt4 для Питона 3-ей версии
#        -файл view_change_date.py на одном файловом уровне с данным скриптом

#    Описание:

#    Выбираешь в календаре время и нажимаешь кнопку выбора даты. 
#    С этого момнета в системе вытавлена дата выбранная в каленадре.
#    По истечении времени delay - время возвращется обратно.
#    Для изменения времени нужны права root, поэтому в passwd вписан пароль.
#    appcmd - это команда спомощью которой можно запустить bricscad через
#    консоль.



from PyQt4 import QtGui
from PyQt4 import QtCore
import  sys, re, time, threading
import view_change_date
from subprocess import *


class Main(QtGui.QWidget, view_change_date.Ui_Form):

#-----------------------------------------------------------------
#            Переменные которые возможно прийдеться менять
#-----------------------------------------------------------------
#    Задержка в секундах
    delay=40

#   Пароль от твоего профиля
    passwd='12'

#   команда для запуска приложения
    appcmd='bricscadv16'
#-----------------------------------------------------------------



    def __init__(self, parent=None):

        QtGui.QWidget.__init__(self,parent)
        self.setupUi(self)
        self.center()
        self.getCurrentDate()
        self.pushButton_2.clicked.connect(self.showDate)
        self.pushButton.clicked.connect(self.runBricsCad)

#   Центрирует приложение
    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

#    Запоминает текущую дату
    def getCurrentDate(self):
        
        self.currDate=round(time.time())
        print('Текущая дата - {0}'.format(self.currDate))


    #Выводит дату в формате YYYY,mm,dd. Сохраняет ее в атрибут self.new_date
    def showDate(self):

        raw_date=self.calendarWidget.selectedDate()
        raw_date=str(raw_date)
        pattern=r'((?<=\().+?(?=\)))'
        date=re.search(pattern,raw_date)
        date=date.group(0); date=date.split(',')

        #Преобразует формат. Дописывает нули в начале, если таковых нету
        format_date=[]
        for x in date:
            x = x.strip()
            if len(x) == 1:
                format_date.append('0{0}'.format(x))

            else:
                format_date.append(x)
        #Конечный формат уже гото
        self.new_date=format_date
        print(self.new_date)
        
        #Спустя время delay автоматически ставит реальную дату
        th1=threading.Thread(target=self.setNewDate)
        th1.start()
        th2=threading.Thread(target=self.setCurrDate)
        th2.start()
        
        
#   Устанавливает реальную дату
    def setCurrDate(self):

        time.sleep(self.delay)
        utc = self.currDate + self.delay
        query='echo \'{0}\' | sudo -S date +%s --set=\'@{1}\''.format(
        self.passwd, utc)
#        print(query)
        call(query, shell=True)
        print('Выставлена актуальная дата!')

#   Ставит фейковую дату
    def setNewDate(self):
        
        new_date=''.join(self.new_date)
        query='echo \'{0}\' | sudo -S date +%Y%m%d --set=\'{1}\''.format(
        self.passwd,new_date)
#        print(query)
        call(query, shell=True)
        print('выставлена новая дата!')


#   Запускает bricscadv16
    def runBricsCad(self):
        
        call(self.appcmd, shell=True)


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    window=Main()
    window.show()
    app.exec_()
