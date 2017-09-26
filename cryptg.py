#!/usr/bin/python3

import sys
import os
import PySide
from PySide import QtGui

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Encrypter')

        self.field = QtGui.QTextEdit()
        self.field.setWordWrapMode(QtGui.QTextOption.WrapMode(3))
        self.openBtn = QtGui.QPushButton('Open file')
        self.enterBtn = QtGui.QPushButton('Enter text')
        self.newBtn = QtGui.QPushButton('New file')
        self.saveBtn = QtGui.QPushButton('Save file')
        self.passwordLine = QtGui.QLineEdit()
        self.passwordLine.setEchoMode(QtGui.QLineEdit.EchoMode(2))
        self.setpassBtn = QtGui.QPushButton('Set password')

        self.password = ''
        self.disabled = False
        self.edata = []
        self.ddata = []
        self.alphabet = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*(),./;'[]-=<>?:{} ")
        self.alphabet.append('"')

        vbox = QtGui.QVBoxLayout()
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.openBtn)
        hbox.addWidget(self.saveBtn)
        vbox.addLayout(hbox)
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.newBtn)
        hbox.addWidget(self.enterBtn)
        vbox.addLayout(hbox)
        vbox.addWidget(self.field)
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.passwordLine)
        hbox.addWidget(self.setpassBtn)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        

        self.openBtn.clicked.connect(self.openFunc)            
        self.enterBtn.clicked.connect(self.enterFunc)
        self.newBtn.clicked.connect(self.newFunc)
        self.saveBtn.clicked.connect(self.saveFunc)
        self.setpassBtn.clicked.connect(self.setpassFunc)

        self.passwordLine.cursorPositionChanged.connect(self.passwordLineFunc)
        self.passwordLine.textChanged.connect(self.passwordLineFunc)
        
        self.field.setPlainText = 'Test'
        
        self.show()

    def openFunc(self):
        file = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
        try:    
            with open(file[0],'r') as f:
                self.edata = f.readlines()
            self.ddata = []
            for line in self.edata:
                if line[-1] == '\n':
                    self.ddata.append(self.decrypt(line[:-1],self.password)+'\n')
                else:
                    self.ddata.append(self.decrypt(line,self.password))
            self.field.setText(''.join(self.ddata))
        except Exception as e:
            print('An error occurred',e)

    def enterFunc(self):
        self.text, self.ok = QtGui.QInputDialog.getText(self, 'Enter Message', 'Message')
        if self.ok:
            self.edata = self.text
            self.ddata = []
            if self.edata[-1] == '\n':
                self.ddata.append(self.decrypt(self.edata[:-1],self.password)+'\n')
            else:
                self.ddata.append(self.decrypt(self.edata,self.password))
            self.field.setText(''.join(self.ddata))
        else:
            pass

                
    def newFunc(self):
        self.ddata = []
        self.edata = []
        self.field.setText('')
        
    
    def saveFunc(self):
        if self.disabled == True:
            file = QtGui.QFileDialog.getSaveFileName(self, 'Save file')
            try:
                self.ddata = self.field.toPlainText().split('\n')
                if self.ddata[-1] == '':
                    self.ddata = self.ddata[:-1]
                self.edata = []
                for line in self.ddata:
                    self.edata.append(self.encrypt(line,self.password)+'\n')
                with open(file[0],'w') as f:
                    f.writelines(self.edata)
                self.field.setText('')
            except Exception as e:
                print('An error occurred',e)
        else:
            pass
    
    def setpassFunc(self):
        self.passwordLine.setCursorPosition(-1)
        self.password = self.passwordLine.text()
        self.setpassBtn.setDisabled(True)
        self.disabled = True

    def passwordLineFunc(self):
        if self.disabled == True:
            self.password = ''
            self.setpassBtn.setDisabled(False)
            self.disabled = False
            self.passwordLine.setText('')

    def encrypt(self,s,p):
        secret = list(s)
        for c in range(0,len(secret)):
            if not secret[c] in self.alphabet:
                secret[c] = '?'
        password = list(p)
        for x in range(0,len(password)):
            for y in range(0,len(secret)):
                key = (self.alphabet.index(password[x])+1)*(y+1)*(x+1)
                secret[y] = self.alphabet[(self.alphabet.index(secret[y])+key+1)%len(self.alphabet)]
                
        return str(''.join(secret))

    def decrypt(self,s,p):
        secret = list(s)
        password = list(p[::-1])
        for x in range(0,len(password)):
            for y in range(0,len(secret)):
                key = (self.alphabet.index(password[x])+1)*(y+1)*(len(password)-x)
                secret[y] = self.alphabet[(self.alphabet.index(secret[y])-key-1)%len(self.alphabet)]
                
        return str(''.join(secret))
        
        
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

