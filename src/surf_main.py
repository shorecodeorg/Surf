#kevin fink
#kevin@shorecode.org
#Sun Apr 28 06:40:48 PM +07 2024
#surf_main.py

from qt_material import apply_stylesheet
import sys
from surf_logging import set_logging
from surf_filepaths import Files

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'surfKaVYLk.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QTabWidget, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1800, 1000)
        palette = QPalette()
        MainWindow.setPalette(palette)
        MainWindow.setAutoFillBackground(True)
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionSave_as = QAction(MainWindow)
        self.actionSave_as.setObjectName(u"actionSave_as")
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionPreferences = QAction(MainWindow)
        self.actionPreferences.setObjectName(u"actionPreferences")
        self.actionAbout_Surf = QAction(MainWindow)
        self.actionAbout_Surf.setObjectName(u"actionAbout_Surf")
        self.actionJoin = QAction(MainWindow)
        self.actionJoin.setObjectName(u"actionJoin")
        self.actionHide_Preview = QAction(MainWindow)
        self.actionHide_Preview.setObjectName(u"actionHide_Preview")
        self.actionNew_Preview_Window = QAction(MainWindow)
        self.actionNew_Preview_Window.setObjectName(u"actionNew_Preview_Window")
        self.actionSave_all = QAction(MainWindow)
        self.actionSave_all.setObjectName(u"actionSave_all")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.mainGrid = QGridLayout()
        self.mainGrid.setObjectName(u"mainGrid")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.splitWidget = QTabWidget(self.centralwidget)
        self.splitWidget.setObjectName(u"splitWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitWidget.sizePolicy().hasHeightForWidth())
        self.splitWidget.setSizePolicy(sizePolicy)
        self.splitWidget.setDocumentMode(True)
        self.splitTab1 = QWidget()
        self.splitTab1.setObjectName(u"splitTab1")
        sizePolicy.setHeightForWidth(self.splitTab1.sizePolicy().hasHeightForWidth())
        self.splitTab1.setSizePolicy(sizePolicy)
        self.verticalLayout_8 = QVBoxLayout(self.splitTab1)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.textEdit_2 = QTextEdit(self.splitTab1)
        self.textEdit_2.setObjectName(u"textEdit_2")
        sizePolicy.setHeightForWidth(self.textEdit_2.sizePolicy().hasHeightForWidth())
        self.textEdit_2.setSizePolicy(sizePolicy)

        self.verticalLayout_8.addWidget(self.textEdit_2)

        self.splitWidget.addTab(self.splitTab1, "")

        self.gridLayout.addWidget(self.splitWidget, 1, 0, 1, 1)

        self.editorWidget = QTabWidget(self.centralwidget)
        self.editorWidget.setObjectName(u"editorWidget")
        sizePolicy.setHeightForWidth(self.editorWidget.sizePolicy().hasHeightForWidth())
        self.editorWidget.setSizePolicy(sizePolicy)
        self.editorWidget.setStyleSheet(
            u'''QMenuBar::item:pressed{
              spacing:2px;
              padding:3px 4px;
              background: #ffa458;
            color:#000000;
            }
            QMenuBar::item:selected{
              background-color:#ffa458;
            color:#000000;
            }
            QMenu::item:selected{
            background-color:#ffa458;
            color:#000000;
            }''')
        self.editorWidget.setElideMode(Qt.ElideLeft)
        self.editorWidget.setDocumentMode(True)
        self.editorWidget.setTabBarAutoHide(False)
        self.fileTab1 = QWidget()
        self.fileTab1.setObjectName(u"fileTab1")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.fileTab1.sizePolicy().hasHeightForWidth())
        self.fileTab1.setSizePolicy(sizePolicy1)
        self.verticalLayout_9 = QVBoxLayout(self.fileTab1)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.textEdit = QTextEdit(self.fileTab1)
        self.textEdit.setObjectName(u"textEdit")
        sizePolicy1.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy1)
        self.textEdit.setStyleSheet(u"")

        self.verticalLayout_9.addWidget(self.textEdit)

        self.editorWidget.addTab(self.fileTab1, "")

        self.gridLayout.addWidget(self.editorWidget, 0, 0, 1, 1)


        self.mainGrid.addLayout(self.gridLayout, 0, 2, 1, 1)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setSizeIncrement(QSize(0, 0))
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setDocumentMode(False)
        self.previewTab = QWidget()
        self.previewTab.setObjectName(u"previewTab")
        self.verticalLayout = QVBoxLayout(self.previewTab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.previewLayout = QVBoxLayout()
        self.previewLayout.setObjectName(u"previewLayout")
        self.tabWidget_2 = QTabWidget(self.previewTab)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tabWidget_2.setTabPosition(QTabWidget.South)
        self.tabWidget_2.setIconSize(QSize(16, 16))
        self.tabWidget_2.setElideMode(Qt.ElideNone)
        self.tabWidget_2.setDocumentMode(False)
        self.previewMobile = QWidget()
        self.previewMobile.setObjectName(u"previewMobile")
        self.previewMobile.setMaximumSize(QSize(360, 16777215))
        self.verticalLayout_4 = QVBoxLayout(self.previewMobile)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.mobileLayout = QVBoxLayout()
        self.mobileLayout.setObjectName(u"mobileLayout")
        self.browserMobile = QWebEngineView(self.previewMobile)
        self.browserMobile.setObjectName(u"browserMobile")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.browserMobile.sizePolicy().hasHeightForWidth())
        self.browserMobile.setSizePolicy(sizePolicy2)
        self.browserMobile.setUrl(QUrl(u"about:blank"))

        self.mobileLayout.addWidget(self.browserMobile)


        self.verticalLayout_4.addLayout(self.mobileLayout)

        self.tabWidget_2.addTab(self.previewMobile, "")
        self.preview720p = QWidget()
        self.preview720p.setObjectName(u"preview720p")
        self.preview720p.setMaximumSize(QSize(1240, 16777215))
        self.verticalLayout_5 = QVBoxLayout(self.preview720p)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.browserLayout720 = QVBoxLayout()
        self.browserLayout720.setObjectName(u"browserLayout720")
        self.browser720 = QWebEngineView(self.preview720p)
        self.browser720.setObjectName(u"browser720")
        self.browser720.setUrl(QUrl(u"about:blank"))

        self.browserLayout720.addWidget(self.browser720)


        self.verticalLayout_5.addLayout(self.browserLayout720)

        self.tabWidget_2.addTab(self.preview720p, "")
        self.preview1080p = QWidget()
        self.preview1080p.setObjectName(u"preview1080p")
        self.preview1080p.setMaximumSize(QSize(1920, 16777215))
        self.verticalLayout_3 = QVBoxLayout(self.preview1080p)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.browserLayout1080 = QVBoxLayout()
        self.browserLayout1080.setObjectName(u"browserLayout1080")
        self.browser1080 = QWebEngineView(self.preview1080p)
        self.browser1080.setObjectName(u"browser1080")
        self.browser1080.setStyleSheet(u"")
        self.browser1080.setUrl(QUrl(u"about:blank"))

        self.browserLayout1080.addWidget(self.browser1080)


        self.verticalLayout_3.addLayout(self.browserLayout1080)

        self.tabWidget_2.addTab(self.preview1080p, "")

        self.previewLayout.addWidget(self.tabWidget_2)


        self.verticalLayout.addLayout(self.previewLayout)

        self.tabWidget.addTab(self.previewTab, "")
        self.consoleTab = QWidget()
        self.consoleTab.setObjectName(u"consoleTab")
        self.verticalLayout_6 = QVBoxLayout(self.consoleTab)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.widget = QWidget(self.consoleTab)
        self.widget.setObjectName(u"widget")

        self.verticalLayout_6.addWidget(self.widget)

        self.tabWidget.addTab(self.consoleTab, "")
        self.networkTab = QWidget()
        self.networkTab.setObjectName(u"networkTab")
        self.verticalLayout_7 = QVBoxLayout(self.networkTab)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.widget_2 = QWidget(self.networkTab)
        self.widget_2.setObjectName(u"widget_2")

        self.verticalLayout_7.addWidget(self.widget_2)

        self.tabWidget.addTab(self.networkTab, "")

        self.mainGrid.addWidget(self.tabWidget, 0, 3, 1, 1)

        self.surfBtn = QPushButton(self.centralwidget)
        self.surfBtn.setObjectName(u"surfBtn")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.surfBtn.sizePolicy().hasHeightForWidth())
        self.surfBtn.setSizePolicy(sizePolicy3)
        self.surfBtn.setMaximumSize(QSize(15, 16777215))
        self.surfBtn.setBaseSize(QSize(200, 20))
        self.surfBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.surfBtn.setAutoDefault(False)
        self.surfBtn.setFlat(False)

        self.mainGrid.addWidget(self.surfBtn, 0, 0, 1, 1)

        self.surfMenu = QFrame(self.centralwidget)
        self.surfMenu.setObjectName(u"surfMenu")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.surfMenu.sizePolicy().hasHeightForWidth())
        self.surfMenu.setSizePolicy(sizePolicy4)
        self.surfMenu.setMinimumSize(QSize(110, 0))
        self.surfMenu.setMaximumSize(QSize(180, 16777215))
        self.surfMenu.setAutoFillBackground(True)
        self.surfMenu.setFrameShape(QFrame.StyledPanel)
        self.surfMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.surfMenu)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.aiRefactorBtn = QPushButton(self.surfMenu)
        self.aiRefactorBtn.setObjectName(u"aiRefactorBtn")

        self.verticalLayout_10.addWidget(self.aiRefactorBtn)

        self.aiBugFixBtn = QPushButton(self.surfMenu)
        self.aiBugFixBtn.setObjectName(u"aiBugFixBtn")

        self.verticalLayout_10.addWidget(self.aiBugFixBtn)

        self.aiMetaDataBtn = QPushButton(self.surfMenu)
        self.aiMetaDataBtn.setObjectName(u"aiMetaDataBtn")

        self.verticalLayout_10.addWidget(self.aiMetaDataBtn)

        self.aiTemplateBtn = QPushButton(self.surfMenu)
        self.aiTemplateBtn.setObjectName(u"aiTemplateBtn")

        self.verticalLayout_10.addWidget(self.aiTemplateBtn)

        self.skeletonBtn = QPushButton(self.surfMenu)
        self.skeletonBtn.setObjectName(u"skeletonBtn")

        self.verticalLayout_10.addWidget(self.skeletonBtn)

        self.cssEditorBtn = QPushButton(self.surfMenu)
        self.cssEditorBtn.setObjectName(u"cssEditorBtn")

        self.verticalLayout_10.addWidget(self.cssEditorBtn)

        self.findReplaceBtn = QPushButton(self.surfMenu)
        self.findReplaceBtn.setObjectName(u"findReplaceBtn")

        self.verticalLayout_10.addWidget(self.findReplaceBtn)

        self.externalDepsBtn = QPushButton(self.surfMenu)
        self.externalDepsBtn.setObjectName(u"externalDepsBtn")

        self.verticalLayout_10.addWidget(self.externalDepsBtn)

        self.jsSandboxBtn = QPushButton(self.surfMenu)
        self.jsSandboxBtn.setObjectName(u"jsSandboxBtn")

        self.verticalLayout_10.addWidget(self.jsSandboxBtn)

        self.indentationBtn = QPushButton(self.surfMenu)
        self.indentationBtn.setObjectName(u"indentationBtn")

        self.verticalLayout_10.addWidget(self.indentationBtn)

        self.gitBtn = QPushButton(self.surfMenu)
        self.gitBtn.setObjectName(u"gitBtn")

        self.verticalLayout_10.addWidget(self.gitBtn)


        self.mainGrid.addWidget(self.surfMenu, 0, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.mainGrid)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 927, 20))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName(u"menuSettings")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuWindow = QMenu(self.menubar)
        self.menuWindow.setObjectName(u"menuWindow")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addSeparator()
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_all)
        self.menuFile.addAction(self.actionQuit)
        self.menuSettings.addAction(self.actionPreferences)
        self.menuHelp.addAction(self.actionAbout_Surf)
        self.menuWindow.addAction(self.actionJoin)
        self.menuWindow.addAction(self.actionHide_Preview)
        self.menuWindow.addAction(self.actionNew_Preview_Window)

        self.retranslateUi(MainWindow)
        self.surfBtn.clicked.connect(self.surfMenu.show)

        self.splitWidget.setCurrentIndex(0)
        self.editorWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        self.surfBtn.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionSave_as.setText(QCoreApplication.translate("MainWindow", u"Save as..", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.actionPreferences.setText(QCoreApplication.translate("MainWindow", u"Preferences", None))
        self.actionAbout_Surf.setText(QCoreApplication.translate("MainWindow", u"About Surf", None))
        self.actionJoin.setText(QCoreApplication.translate("MainWindow", u"Join", None))
        self.actionHide_Preview.setText(QCoreApplication.translate("MainWindow", u"Hide Preview", None))
        self.actionNew_Preview_Window.setText(QCoreApplication.translate("MainWindow", u"New Preview Window", None))
        self.actionSave_all.setText(QCoreApplication.translate("MainWindow", u"Save all", None))
        self.textEdit_2.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">sf</p></body></html>", None))
        self.splitWidget.setTabText(self.splitWidget.indexOf(self.splitTab1), QCoreApplication.translate("MainWindow", u"untitled", None))
        self.textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">sdfa</p></body></html>", None))
        self.editorWidget.setTabText(self.editorWidget.indexOf(self.fileTab1), QCoreApplication.translate("MainWindow", u"untitled", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.previewMobile), QCoreApplication.translate("MainWindow", u"Mobile", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.preview720p), QCoreApplication.translate("MainWindow", u"720p", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.preview1080p), QCoreApplication.translate("MainWindow", u"1080p", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.previewTab), QCoreApplication.translate("MainWindow", u"Preview", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.consoleTab), QCoreApplication.translate("MainWindow", u"Console", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.networkTab), QCoreApplication.translate("MainWindow", u"Network", None))
        self.surfBtn.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.aiRefactorBtn.setText(QCoreApplication.translate("MainWindow", u"Ai refactor", None))
        self.aiBugFixBtn.setText(QCoreApplication.translate("MainWindow", u"Ai bug fix", None))
        self.aiMetaDataBtn.setText(QCoreApplication.translate("MainWindow", u"Ai Metadata", None))
        self.aiTemplateBtn.setText(QCoreApplication.translate("MainWindow", u"Ai Template", None))
        self.skeletonBtn.setText(QCoreApplication.translate("MainWindow", u"Skeleton", None))
        self.cssEditorBtn.setText(QCoreApplication.translate("MainWindow", u"Css Editor", None))
        self.findReplaceBtn.setText(QCoreApplication.translate("MainWindow", u"Find & Replace", None))
        self.externalDepsBtn.setText(QCoreApplication.translate("MainWindow", u"External Deps", None))
        self.jsSandboxBtn.setText(QCoreApplication.translate("MainWindow", u"JS Sandbox", None))
        self.indentationBtn.setText(QCoreApplication.translate("MainWindow", u"Indentation", None))
        self.gitBtn.setText(QCoreApplication.translate("MainWindow", u"GIT", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuWindow.setTitle(QCoreApplication.translate("MainWindow", u"Windows", None))
    # retranslateUi




if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create an instance of QMainWindow or a subclass of it
    mainWindow = QMainWindow()
    
    # Apply your UI setup to this main window instance
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)  # Pass the instance to setupUi
    
    # setup stylesheet
    apply_stylesheet(app, theme='dark_orange.xml')
    # Show the main window
    mainWindow.show()

    sys.exit(app.exec())
