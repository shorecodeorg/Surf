#kevin fink
#kevin@shorecode.org
#Sun Apr 28 06:40:48 PM +07 2024
#surf_main.py

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'surfKaVYLk.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

import PySide6
from qt_material import apply_stylesheet
import sys
from surf_logging import set_logging
from surf_filepaths import Files
from surf_extensions import  (HtmlCssJsHighlighter, CodeEditor, CssEditor, 
                              CustomCompleter, FindReplaceWidget,
                              SyntaxVocabulary, ClosableTabBar,
                              SkeletonTree, JsSandbox, ConsoleWidget,
                              ConsoleEnabledPage, AiWidget, FlaskCompatWidget)
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect, QStringListModel, QTimer, 
    QSize, QTime, QUrl, Qt, QEvent)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient, QTextFormat, 
    QIcon, QImage, QKeySequence, QLinearGradient, QKeyEvent, 
    QPainter, QPalette, QPixmap, QRadialGradient, QKeySequence, 
    QTransform, QTextCursor, QMouseEvent, QShortcut)
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy, QCompleter, 
    QStatusBar, QTabWidget, QTextEdit, QVBoxLayout,  
    QWidget, QFileDialog, QSplitter, QPlainTextEdit,
    QHBoxLayout)

class Ui_MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
    def setup_completer(self, text_editor, MainWindow):
        # Vocabulary for HTML, CSS, and JavaScript
        vocab = SyntaxVocabulary()
        self.vocabulary = vocab.get_all_vocab()
        self.completer = CustomCompleter(self.vocabulary, text_editor, text_editor)
        self.completer.setModel(QStringListModel(self.vocabulary))
        self.completer.setWidget(text_editor)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
                   
    def updateCompleterPosition(self, text_editor):
        tc = text_editor.textCursor()
        text = text_editor.toPlainText()
        pos = tc.position()
    
        # Do not show the completer if text is selected
        if tc.hasSelection():
            self.completer.popup().hide()
            return
    
        # Find the start of the word/tag
        start_pos = pos
        while start_pos > 0 and not text[start_pos - 1].isspace():
            start_pos -= 1
            if text[start_pos] in ['<', '>']:  # Adjust for HTML tags
                break
    
        # Find the end of the word/tag
        end_pos = pos
        while end_pos < len(text) and not text[end_pos].isspace():
            end_pos += 1
            if text[end_pos - 1] in ['<', '>']:  # Adjust for HTML tags
                break
    
        # Set the completion prefix based on the start and end positions
        completion_prefix = text[start_pos:end_pos]
        self.completer.setCompletionPrefix(completion_prefix)
    
        # Check if the completion prefix matches any vocabulary item
        matches = any(vocab.startswith(completion_prefix) for vocab in self.vocabulary)
        matches_list = [vocab for vocab in self.vocabulary if vocab.startswith(completion_prefix)]
    
        if completion_prefix and matches:
            cr = text_editor.cursorRect(tc)
            top = cr.top()
            bottom = cr.bottom()
            cr.setTop(top+10)
            cr.setBottom(bottom+10)    
            # Dynamically adjust the width of the completer popup
            popup = self.completer.popup()
            maxItemWidth = max(popup.fontMetrics().horizontalAdvance(item) for item in matches_list) + 25  # Adding a small padding
            popupWidth = max(cr.width(), maxItemWidth + popup.verticalScrollBar().sizeHint().width())
            cr.setWidth(popupWidth)
    
            self.completer.complete(cr)  # Popup it up!
        else:
            self.completer.popup().hide()  # Hide the popup if no match is found
        
    def setup_menu(self, MainWindow):
        """
        Creates the necessary UI elements for the top dropdown menus (File, Edit, Help, etc.)
        """
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
        self.actionNew_Preview_Window = QAction(MainWindow)
        self.actionNew_Preview_Window.setObjectName(u"actionNew_Preview_Window")
        self.actionSave_all = QAction(MainWindow)
        self.actionSave_all.setObjectName(u"actionSave_all")
        
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
        
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_all)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuSettings.addAction(self.actionPreferences)
        self.menuHelp.addAction(self.actionAbout_Surf)
        self.menuWindow.addAction(self.actionNew_Preview_Window)
        
        
    def setup_editor(self, MainWindow):
        """
        Creates the necessary UI elements for the code editor
        """
        self.gridLayout = QSplitter(Qt.Vertical)
        self.gridLayout.setObjectName(u"gridLayout")
        self.splitWidget = QTabWidget(self.centralwidget)
        self.splitWidget.setObjectName(u"splitWidget")
        self.splitWidget.setSizePolicy(self.sizePolicy)
        
        self.sizePolicy.setHeightForWidth(self.splitWidget.sizePolicy().hasHeightForWidth())
        self.splitWidget.setDocumentMode(True)
        self.splitWidget.setTabBar(ClosableTabBar(self))
        self.splitTab1 = QWidget()
        self.splitTab1.setObjectName(u"splitTab1")
        self.sizePolicy.setHeightForWidth(self.splitTab1.sizePolicy().hasHeightForWidth())
        self.splitTab1.setSizePolicy(self.sizePolicy)
        self.verticalLayout_8 = QVBoxLayout(self.splitTab1)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.textEdit_2 = CodeEditor(self.splitTab1)
        self.textEdit_2.setObjectName(u"textEdit_2")
        self.sizePolicy.setHeightForWidth(self.textEdit_2.sizePolicy().hasHeightForWidth())
        self.textEdit_2.setSizePolicy(self.sizePolicy)

        self.verticalLayout_8.addWidget(self.textEdit_2)
        #self.splitWidget.addTab(self.splitTab1, "")

        self.editorWidget = QTabWidget(self.centralwidget)        
        self.editorWidget.setObjectName(u"editorWidget")
        self.sizePolicy.setHeightForWidth(self.editorWidget.sizePolicy().hasHeightForWidth())
        self.editorWidget.setSizePolicy(self.sizePolicy)
        self.editorWidget.setElideMode(Qt.ElideLeft)
        self.editorWidget.setDocumentMode(True)
        self.editorWidget.setTabBarAutoHide(False)
        self.editorWidget.setTabBar(ClosableTabBar(self))
        self.fileTab1 = QWidget()
        self.fileTab1.setObjectName(u"fileTab1")
        self.sizePolicy1.setHeightForWidth(self.fileTab1.sizePolicy().hasHeightForWidth())
        self.fileTab1.setSizePolicy(self.sizePolicy1)
        self.verticalLayout_9 = QVBoxLayout(self.fileTab1)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.textEdit = CodeEditor(self.fileTab1)
        self.textEdit.setObjectName(u"textEdit")
        self.sizePolicy1.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(self.sizePolicy1)
        self.editor_tabs.append(self.textEdit)

        self.verticalLayout_9.addWidget(self.textEdit)

        self.editorWidget.addTab(self.fileTab1, "")

        self.gridLayout.addWidget(self.editorWidget)
        self.gridLayout.addWidget(self.splitWidget)
        self.highlighter = HtmlCssJsHighlighter(self.textEdit.document())
        self.highlighter = HtmlCssJsHighlighter(self.textEdit_2.document())
        self.setup_completer(self.textEdit, self)
        self.textEdit.cursorPositionChanged.connect(lambda: self.updateCompleterPosition(self.textEdit))
        #self.setup_completer(self.textEdit_2, MainWindow)
        #self.textEdit_2.cursorPositionChanged.connect(self.updateCompleterPosition)

    def setup_browser(self, MainWindow):
        """
        Creates the necessary UI elements for the web browser
        """
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(self.sizePolicy)
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
        self.sizePolicy2.setHeightForWidth(self.browserMobile.sizePolicy().hasHeightForWidth())
        self.browserMobile.setSizePolicy(self.sizePolicy2)
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
        self.consoleEnabledPage = ConsoleEnabledPage()
        self.browser1080.setPage(self.consoleEnabledPage)
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
        # Initialize the console widget
        self.console = ConsoleWidget(self.consoleTab)        

        self.verticalLayout_6.addWidget(self.console)

        self.tabWidget.addTab(self.consoleTab, "")
        
        self.networkTab = QWidget()
        self.networkTab.setObjectName(u"networkTab")
        self.verticalLayout_7 = QVBoxLayout(self.networkTab)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.widget_2 = QWidget(self.networkTab)
        self.widget_2.setObjectName(u"widget_2")

        self.verticalLayout_7.addWidget(self.widget_2)

        self.tabWidget.addTab(self.networkTab, "")


    def setup_surf_menu(self, MainWindow):
        """
        Creates the necessary UI elements for the folding left side 'Surf' menu
        """
        self.surfBtn = QPushButton(self.centralwidget)
        self.surfBtn.setObjectName(u"surfBtn")

        self.sizePolicy3.setHeightForWidth(self.surfBtn.sizePolicy().hasHeightForWidth())
        self.surfBtn.setSizePolicy(self.sizePolicy3)
        self.surfBtn.setMaximumSize(QSize(15, 16777215))
        self.surfBtn.setBaseSize(QSize(200, 20))
        self.surfBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.surfBtn.setAutoDefault(False)
        self.surfBtn.setFlat(False)

        self.mainGrid.addWidget(self.surfBtn, 0, 0, 1, 1)

        self.surfMenu = QFrame(self.centralwidget)
        self.surfMenu.setObjectName(u"surfMenu")

        self.sizePolicy4.setHeightForWidth(self.surfMenu.sizePolicy().hasHeightForWidth())
        self.surfMenu.setSizePolicy(self.sizePolicy4)
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
        
        self.flaskBtn = QPushButton(self.surfMenu)
        self.flaskBtn.setObjectName(u"flaskBtn")

        self.verticalLayout_10.addWidget(self.flaskBtn)        

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"SURF -- Shorecode LLC")
        MainWindow.resize(1800, 1000)
        MainWindow.setStyleSheet(
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
            }
            QScrollBar {
            background-color: #333333;
            }
            QLineEdit {
            color: grey;            
            }
            QLineEdit:focus {
            color: white;            
            }
            QPushButton:hover {
              background-color: #4d2600;
            }
            QPushButton:pressed {
              color: #ffd9b3;
            }
            OutputConsole {
              background-color: #001a1a;
              font-family: 'Courier New', monospace;
              font-size: 10px;
            }
            CodeEditor {
              font-family: 'Courier New', monospace;
              font-size: 13px;
            }
            ConsoleWidget {
              background-color: #001a1a;
              font-family: 'Courier New', monospace;
              font-size: 10px;
            }
            ''')
        files = Files()
        filepaths = files.get_files_list()
        self.logger = set_logging('surf', filepaths[0])
        MainWindow.setWindowIcon(QIcon(filepaths[1]))        
                
        self.editor_tabs = list()
        self.open_files = dict()
        
        palette = QPalette()
        MainWindow.setPalette(palette)
        MainWindow.setAutoFillBackground(True)

        self.sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.sizePolicy.setHorizontalStretch(0)
        self.sizePolicy.setVerticalStretch(0)
        self.sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.sizePolicy1.setHorizontalStretch(0)
        self.sizePolicy1.setVerticalStretch(0)                
        self.sizePolicy2 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.sizePolicy2.setHorizontalStretch(0)
        self.sizePolicy2.setVerticalStretch(0)
        self.sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)
        self.sizePolicy3.setHorizontalStretch(0)
        self.sizePolicy3.setVerticalStretch(0)        
        self.sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        self.sizePolicy4.setHorizontalStretch(0)
        self.sizePolicy4.setVerticalStretch(0)
        
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.mainGrid = QGridLayout()
        self.mainGrid.setObjectName(u"mainGrid")

        self.setup_menu(MainWindow)
        self.setup_editor(MainWindow)
        self.setup_browser(MainWindow)
        self.setup_surf_menu(MainWindow)

        self.horizSplit = QSplitter(Qt.Horizontal)
        self.horizSplit.addWidget(self.gridLayout)
        self.horizSplit.addWidget(self.tabWidget)
        self.mainGrid.addWidget(self.horizSplit, 0, 2)
        self.mainGrid.addWidget(self.surfMenu, 0, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.mainGrid)

        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.surfMenu.hide()

        # Signals are below
        self.retranslateUi(MainWindow)
        self.surfBtn.clicked.connect(self.toggle_surf)
        self.actionNew.triggered.connect(self.add_tab)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionSave.triggered.connect(lambda: self.save_tab(self.editorWidget.currentIndex()))
        # Setup Ctrl+S shortcut for saving the current tab
        self.save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.save_shortcut.activated.connect(lambda: self.save_tab(self.editorWidget.currentIndex()))
        self.actionSave_as.triggered.connect(lambda: self.save_tab(self.editorWidget.currentIndex(), dialog=True))
        self.actionQuit.triggered.connect(sys.exit)
        #self.actionPreferences.triggered.connect()
        #self.actionAbout_Surf.triggered.connect()
        #self.actionNew_Preview_Window.triggered.connect()
        self.actionSave_all.triggered.connect(self.save_all)
        self.aiRefactorBtn.clicked.connect(self.ai_refactor)
        self.aiBugFixBtn.clicked.connect(self.ai_bug_fix)
        #self.aiMetaDataBtn.clicked.connect()
        #self.aiTemplateBtn.clicked.connect()
        self.skeletonBtn.clicked.connect(self.skeleton)
        self.cssEditorBtn.clicked.connect(self.css_editor)
        self.findReplaceBtn.clicked.connect(self.find_replace)
        #self.externalDepsBtn.clicked.connect()
        self.jsSandboxBtn.clicked.connect(self.js_sandbox)
        #self.indentationBtn.clicked.connect()
        #self.gitBtn.clicked.connect()
        self.flaskBtn.clicked.connect(self.flask_compat)
        self.editorWidget.tabBar().tabBarClicked.connect(self.update_extensions)
        self.editorWidget.tabBar().tabCloseRequested.connect(lambda idx: self.remove_tab(idx, self.editorWidget, pop_from_list=True))
        self.splitWidget.tabBar().tabCloseRequested.connect(lambda idx2: self.remove_tab(idx2, self.splitWidget))
        self.consoleEnabledPage.newData.connect(self.console.log_message)
        # End of signals
                       
        self.splitWidget.setCurrentIndex(0)
        self.editorWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        self.surfBtn.setDefault(False)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi
    
    def update_extensions(self, i):
        """
        Updates various extensions based on the currently selected editor tab.
    
        This method is responsible for updating the state of flask compatibility, JS sandbox, skeleton,
        and find/replace widgets, as well as the browsers and console based on the content of the currently
        active editor tab.
    
        Args:
            i (int): The index of the currently selected tab in the editor widget.
        """        
        self.update_flask_compat(i)
        self.update_js_sandbox(i)
        self.update_skeleton(i)
        self.update_find_replace(i)
        try:            
            self.update_browsers(self.open_files[self.editorWidget.tabText(i)])
            self.update_console()
        except (TypeError,KeyError) as e:
            print(e)
    
    
    def flask_compat(self):
        """
        Initializes and displays the Flask Compatibility widget in a new tab.
    
        This slot creates a FlaskCompatWidget for the currently active editor and adds it to the splitWidget
        with the label 'Flask Compatibility'.
        """        
        editor_idx = self.editorWidget.currentIndex()
        editor = self.editor_tabs[editor_idx]                
        self.flask_compat_widget = FlaskCompatWidget(editor)
        self.splitWidget.addTab(self.flask_compat_widget, 'Flask Compatibility')
        
    def update_flask_compat(self, i):
        """
        Updates the Flask Compatibility widget with the content from the currently selected editor tab.
    
        Args:
            i (int): The index of the currently selected tab in the editor widget.
        """        
        try:            
            editor = self.editor_tabs[i]        
            self.flask_compat_widget.update_editor(editor)
        except AttributeError:
            pass                
    
    def ai_refactor(self):
        """
        Initializes and displays the AI Refactor widget in a new tab.
    
        This slot creates an AiWidget configured for code refactoring and adds it to the splitWidget
        with the label 'AI Refactor'.
        """        
        self.ai_refactor_widget = AiWidget('refactor')
        self.ai_refactor_widget.query_button.clicked.connect(self.ai_refactor_query)
        self.splitWidget.addTab(self.ai_refactor_widget, 'AI Refactor')
    
    def ai_refactor_query(self):
        """
        Processes the query for AI-based code refactoring and displays the response.
    
        Takes the input from the query text edit in the AI Refactor widget, processes it, and displays
        the AI-generated response in the answer text edit.
        """        
        query = self.ai_refactor_widget.query_text_edit.toPlainText()

        response = f"AI response to: {query}"
        self.ai_refactor_widget.answer_text_edit.setPlainText(response)         
    
    def ai_bug_fix(self):
        """
        Initializes and displays the AI Bug Fix widget in a new tab.
    
        This slot creates an AiWidget configured for bug fixing and adds it to the splitWidget
        with the label 'AI Bug Fix'.
        """        
        self.ai_bug = AiWidget('bugfix')
        self.ai_bug.query_button.clicked.connect(self.ai_bug_fix_query)
        self.splitWidget.addTab(self.ai_bug, 'AI Bug Fix')
    
    def ai_bug_fix_query(self):
        """
        Processes the query for AI-based bug fixing and displays the response.
    
        Takes the input from the query text edit in the AI Bug Fix widget, processes it, and displays
        the AI-generated response in the answer text edit.
        """        
        query = self.ai_bug.query_text_edit.toPlainText()

        response = f"AI response to: {query}"
        self.ai_bug.answer_text_edit.setPlainText(response)        
    
    def update_console(self):
        """
        Clears the content of the console widget.
    
        This slot is responsible for clearing any existing output or messages displayed in the console widget.
        """        
        self.console.clear_console()
        
    def js_sandbox(self):
        """
        Initializes and displays the JavaScript Sandbox in a new tab.
    
        This slot creates a JsSandbox for the currently active editor, adds it to the splitWidget with the label
        'JS Sandbox', and also adds its web view to the tabWidget.
        """        
        editor_idx = self.editorWidget.currentIndex()
        editor = self.editor_tabs[editor_idx]        
        sandbox = JsSandbox(editor)
        web_view = sandbox.get_view()
        self.splitWidget.addTab(sandbox, 'JS Sandbox')
        self.tabWidget.addTab(web_view, 'JS Sandbox')
        self.sandbox = sandbox
    
    def update_js_sandbox(self, i):
        """
        Updates the JavaScript Sandbox with the content from the currently selected editor tab.
    
        Args:
            i (int): The index of the currently selected tab in the editor widget.
        """        
        try:            
            editor = self.editor_tabs[i]        
            self.sandbox.update_js_sandbox(editor)
        except AttributeError:
            pass
    
    def update_skeleton(self, i):
        """
        Updates the skeleton tree view for the editor at the specified index.
    
        This slot is typically connected to a signal that indicates a change in the editor that requires
        the skeleton tree view to be refreshed.
    
        Args:
            i (int): The index of the editor in the editor tabs list.
        """        
        try:            
            editor = self.editor_tabs[i]        
            self.skele.update_tree_view(editor)
        except AttributeError:
            pass
    
    def skeleton(self):
        """
        Initializes and displays the skeleton tree view for the current active editor.
    
        This method creates a new SkeletonTree instance, sets up its UI components, and adds it to a new tab
        in the splitWidget. It connects the update button to refresh the skeleton tree view based on the current
        editor's content.
        """        
        editor_idx = self.editorWidget.currentIndex()
        editor = self.editor_tabs[editor_idx]
        self.skele = SkeletonTree(editor)        
        # Create a new QWidget that will serve as the container for the layout
        container_widget = QWidget()
        # Create a layout
        skele_layout = QVBoxLayout()
        # Add the SkeletonTree widget to the layout        
        skele_layout.addWidget(self.skele)
        updateButton = QPushButton("Update Tree View")
        skele_layout.addWidget(updateButton)
        updateButton.clicked.connect(lambda: self.skele.update_tree_view(editor))
        container_widget.setLayout(skele_layout)
        self.splitWidget.addTab(container_widget, 'Skeleton')

    def closeTab(self, index, tab_widget):
        """
        Closes the tab at the specified index and removes it from the tab widget and editor tabs list.
    
        Args:
            index (int): The index of the tab to be closed.
            tab_widget (QTabWidget): The tab widget from which the tab will be removed.
        """        
        tab_widget.removeTab(index)
        self.editor_tabs.pop(index)

    def css_editor(self):
        """
        Opens a CSS editor for the currently active editor tab.
    
        This method attempts to create and configure a CssEditor instance for the current editor. It will
        display a message if no editor is open.
        """        
        try:            
            current_tab_idx = self.editorWidget.currentIndex()
            editor = self.editor_tabs[current_tab_idx]        
            css_editor = CssEditor(self.splitWidget)
            button = css_editor.get_button()
            button.clicked.connect(lambda: css_editor.find_selector(editor))
        except IndexError:
            print('Cannot open CSS EDITOR, Open editor first')

    def find_replace(self):
        """
        Opens the find and replace widget for the currently active editor tab.
    
        This method initializes the FindReplaceWidget with the current editor and adds it to a new tab in the
        splitWidget. It also sets the tab order for the find and replace inputs and buttons.
        """        
        try:            
            current_tab_idx = self.editorWidget.currentIndex()
            editor = self.editor_tabs[current_tab_idx]
            self.find_replace = FindReplaceWidget(editor)
            self.splitWidget.addTab(self.find_replace, 'Find/Replace')
            # Setting the tab order explicitly
            self.setTabOrder(self.find_replace.find_input, self.find_replace.find_button)
            self.setTabOrder(self.find_replace.find_button, self.find_replace.searchLineEdit)
            self.setTabOrder(self.find_replace.searchLineEdit, self.find_replace.searchButton)
            self.setTabOrder(self.find_replace.searchButton, self.find_replace.replaceLineEdit)
            self.setTabOrder(self.find_replace.replaceLineEdit, self.find_replace.replaceButton)
            self.setTabOrder(self.find_replace.replaceButton, self.find_replace.selectAllButton)
            self.setTabOrder(self.find_replace.selectAllButton, self.find_replace.unselectAllButton)                        
        except IndexError:
            print('Cannot open find/replace, Open editor first')
            
    def update_find_replace(self, i):
        """
        Updates the editor instance in the find and replace widget for the editor at the specified index.
    
        This slot can be used to refresh the find and replace functionality when the active editor changes.
    
        Args:
            i (int): The index of the editor in the editor tabs list.
        """        
        try:            
            editor = self.editor_tabs[i]        
            self.find_replace.updateEditor(editor)
        except AttributeError:
            pass        
        
    def update_browsers(self, filename):
        """
        Loads the specified file in all browser preview widgets.
    
        Args:
            filename (str): The path to the file to be loaded in the browser previews.
        """        
        local_url = QUrl.fromLocalFile(filename)
        self.browser1080.load(local_url)
        self.browser720.load(local_url)
        self.browserMobile.load(local_url)

    def add_tab(self):
        """
        Adds a new tab with a default name 'untitled' to the editor widget.
        """        
        self.new_tab('untitled')

    def new_tab(self, tab_name):
        """
        Creates a new editor tab with the specified name.
    
        Args:
            tab_name (str): The name for the new tab.
        """        
        new_widget = QWidget(self.editorWidget)
        new_edit = CodeEditor(new_widget)       
        self.sizePolicy.setHeightForWidth(new_widget.sizePolicy().hasHeightForWidth())
        new_widget.setSizePolicy(self.sizePolicy)        
        self.sizePolicy1.setHeightForWidth(new_edit.sizePolicy().hasHeightForWidth())
        new_edit.setSizePolicy(self.sizePolicy1)
        self.highlighter = HtmlCssJsHighlighter(new_edit.document())
        # Create a QVBoxLayout and add the QTextEdit to it
        layout = QVBoxLayout()
        layout.addWidget(new_edit)
        # Set the layout to the new_widget        
        new_widget.setLayout(layout)        
        self.editor_tabs.append(new_edit)
        self.editorWidget.addTab(new_widget, tab_name)
        self.setup_completer(self.textEdit, self)
        self.textEdit.cursorPositionChanged.connect(lambda: self.updateCompleterPosition(self.textEdit))        
    
    def remove_tab(self, idx, editor, pop_from_list=False):
        """
        Removes the tab at the specified index from the editor widget and optionally from the editor tabs list.
    
        Args:
            idx (int): The index of the tab to be removed.
            editor (QTabWidget): The editor widget from which the tab will be removed.
            pop_from_list (bool): Whether to remove the editor from the editor tabs list. Defaults to False.
        """        
        active_tab_name = self.editorWidget.tabText(idx)
        editor.removeTab(idx)
        if pop_from_list:
            self.editor_tabs.pop(idx)
        if active_tab_name in self.open_files.keys():
            del self.open_files[active_tab_name]
    
    def save_tab(self, idx, dialog=False):
        """
        Saves the content of the tab at the specified index to a file.
    
        If the tab corresponds to an already opened file and dialog is False, it saves the content to that file.
        Otherwise, it prompts the user to select a file location.
    
        Args:
            idx (int): The index of the tab whose content is to be saved.
            dialog (bool): Whether to always show the save file dialog. Defaults to False.
        """        
        active_tab_name = self.editorWidget.tabText(idx)
        if active_tab_name in self.open_files.keys() and dialog == False:
            filename = self.open_files[active_tab_name]
        else:
            # Open the save file dialog
            options = QFileDialog.Options()
            filename, _ = QFileDialog.getSaveFileName(None, "Save as...", "",
                                "All Files (*);;HTML Files (*.html);;CSS Files (*.css);;Javascript Files (*.js)", options=options)
        if filename:
            html = self.editor_tabs[idx].toPlainText()
            with open(filename, 'w', encoding='utf-8') as fn:
                fn.writelines(html)
            self.update_browsers(filename)
            # Update the tab name with the filename extracted from the path
            new_tab_name = filename.split('/')[-1]
            self.editorWidget.setTabText(idx, new_tab_name)
            self.editorWidget.tabBar().tabSizeHint(idx, len(new_tab_name))
            self.open_files[new_tab_name] = filename
        
    def save_all(self):
        """
        Saves the content of all open tabs to their respective files.
    
        This method iterates through all tabs, saving each one's content to the associated file if it exists,
        or prompts the user to select a file location if not.
        """        
        for i in range(len(self.editor_tabs)):
            self.save_tab(i)
    
    def open_file(self):
        """
        Opens a file selected by the user and creates a new tab with its content.
    
        This method displays a file dialog for the user to select a file to open. If the file is not already
        open in a tab, it creates a new tab with the file's content.
        """        
        filename, _ = QFileDialog.getOpenFileName(None, "Open", "",
                    "All Files (*);;HTML Files (*.html);;CSS Files (*.css);;Javascript Files (*.js)")
        tab_name = filename.split('/')[-1]
        if filename:
            if tab_name not in self.open_files.keys():            
                self.open_files[tab_name] = filename
                self.new_tab(tab_name)
                with open(filename, 'r', encoding='utf-8') as fn:
                    text = fn.readlines()
                text = ''.join(text)
                self.editor_tabs[-1].insertPlainText(text)
            self.update_browsers(filename)
            self.editorWidget.setCurrentIndex(len(self.editor_tabs)-1)
            self.update_extensions(len(self.editor_tabs)-1)
            self.editorWidget.tabBar().tabSizeHint(-1, len(tab_name))
    
    def toggle_surf(self):
        """
        Toggles the visibility of the surf menu.
    
        If the surf menu is currently visible, it hides it; if it is hidden, it shows it.
        """        
        if self.surfMenu.isHidden():
            self.surfMenu.show()
        else:
            self.surfMenu.hide()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionSave_as.setText(QCoreApplication.translate("MainWindow", u"Save as..", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.actionPreferences.setText(QCoreApplication.translate("MainWindow", u"Preferences", None))
        self.actionAbout_Surf.setText(QCoreApplication.translate("MainWindow", u"About Surf", None))
        self.actionNew_Preview_Window.setText(QCoreApplication.translate("MainWindow", u"New Preview Window", None))
        self.actionSave_all.setText(QCoreApplication.translate("MainWindow", u"Save all", None))
        self.splitWidget.setTabText(self.splitWidget.indexOf(self.splitTab1), QCoreApplication.translate("MainWindow", u"untitled", None))
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
        self.flaskBtn.setText(QCoreApplication.translate("MainWindow", u"Flask Compat", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuWindow.setTitle(QCoreApplication.translate("MainWindow", u"Windows", None))
    # retranslateUi




if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Apply your UI setup to this main window instance
    ui = Ui_MainWindow()
    ui.setupUi(ui)  # Pass the instance to setupUi
    
    # setup stylesheet
    apply_stylesheet(app, theme='dark_orange.xml')
    # Show the main window
    ui.show()

    sys.exit(app.exec())
