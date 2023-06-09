# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 22:25:17 2023

@author: sabir
"""


import guiWidgets as gui

if __name__ == '__main__':
    app = gui.QtWidgets.QApplication([])
    ex = gui.MainWindow()
    gui.sys.exit(app.exec_())