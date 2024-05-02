#kevin fink
#kevin@shorecode.org
#Sun Apr 28 06:40:48 PM +07 2024
#surf_extensions.py

import sys
from surf_logging import set_logging
from surf_filepaths import Files
from PySide6.QtWidgets import (QApplication, QMainWindow, QPlainTextEdit,
        QWidget, QTextEdit, QCompleter, QHBoxLayout, QVBoxLayout, QMessageBox,
        QLineEdit, QPushButton, QLabel, QTabWidget, QStyledItemDelegate, QTabBar)        
from PySide6.QtGui import (QSyntaxHighlighter, QTextCharFormat, QColor, QPainter,
        QColor, QTextFormat, QTextCursor, QKeyEvent, QFont, QIcon)
from PySide6.QtCore import (QRegularExpression, Qt, QStringListModel,
        QTextStream, QFile, QRect)

class CustomDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(CustomDelegate, self).__init__(parent)

    def sizeHint(self, option, index):
        size = super(CustomDelegate, self).sizeHint(option, index)
        # Reduce the height of each item, adjust according to your needs
        size.setHeight(size.height() - 15)
        return size

class HtmlCssJsHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlightingRules = []

        # HTML Tags
        tagFormat = QTextCharFormat()
        tagFormat.setForeground(QColor(255, 192, 203))
        self.highlightingRules.append((QRegularExpression('</?\w+\s*(\s+[^>]*)?>'), tagFormat))

        # HTML Attributes
        attributeFormat = QTextCharFormat()
        attributeFormat.setForeground(QColor(152, 255, 152))
        self.highlightingRules.append((QRegularExpression("\\w+(?=\\=)"), attributeFormat))

        # CSS Selectors
        cssSelectorFormat = QTextCharFormat()
        cssSelectorFormat.setForeground(QColor(255, 0, 0))
        self.highlightingRules.append((QRegularExpression("\\b[a-zA-Z0-9_]+(?=\\s*\\{)"), cssSelectorFormat))
        
        # CSS Properties (Keywords inside the curly braces)
        cssPropertyFormat = QTextCharFormat()
        cssPropertyFormat.setForeground(QColor(64, 224, 208))
        self.highlightingRules.append((QRegularExpression("\\b[a-zA-Z-]+(?=\\s*:)"), cssPropertyFormat))        

        # JavaScript Keywords
        jsKeywordFormat = QTextCharFormat()
        jsKeywordFormat.setForeground(QColor(57, 255, 20))
        sv = SyntaxVocabulary()
        js_vocab = sv.get_js_vocab()
        keywordPatterns = [f'\\b{item}\\b' for item in js_vocab]
        for pattern in keywordPatterns:
            self.highlightingRules.append((QRegularExpression(pattern), jsKeywordFormat))

        # JavaScript Keywords 2
        jsKeywordFormat = QTextCharFormat()
        jsKeywordFormat.setForeground(QColor(135, 206, 235))
        keywordPatterns = [
            "\\bvar\\b", "\\blet\\b", "\\bconst\\b", "\\breturn\\b", "\\bnew\\b",
            "\\bclass\\b", "\\bsuper\\b", "\\bimport\\b", "\\bexport\\b", "\\bdefault\\b"
        ]              
        for pattern in keywordPatterns:
            self.highlightingRules.append((QRegularExpression(pattern), jsKeywordFormat))

        # JavaScript Special Characters
        jsSpecialCharFormat = QTextCharFormat()
        jsSpecialCharFormat.setForeground(QColor(0, 255, 255))
        self.highlightingRules.append((QRegularExpression("[{}();,\\[\\].]"), jsSpecialCharFormat))

        # JavaScript Strings
        jsStringFormat = QTextCharFormat()
        jsStringFormat.setForeground(QColor(255, 254, 106))
        self.highlightingRules.append((QRegularExpression("\".*\"|'.*'"), jsStringFormat))

        # JavaScript Numbers
        jsNumberFormat = QTextCharFormat()
        jsNumberFormat.setForeground(QColor(191, 64, 191))
        self.highlightingRules.append((QRegularExpression("\\b[+-]?[0-9]+(\\.[0-9]+)?\\b"), jsNumberFormat))
        
        # Single-line Comments
        singleLineCommentFormat = QTextCharFormat()
        singleLineCommentFormat.setForeground(QColor(180, 180, 180))
        singleLineCommentPattern = QRegularExpression('//[^\n]*')
        self.highlightingRules.append((singleLineCommentPattern, singleLineCommentFormat))        

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegularExpression(pattern)
            matchIterator = expression.globalMatch(text)
            while matchIterator.hasNext():
                match = matchIterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.codeEditor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)

class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = LineNumberArea(self)

        self.textChanged.connect(self.updateLineNumberAreaWidth)
        self.verticalScrollBar().valueChanged.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)  # Initial update with default value

    def lineNumberAreaWidth(self):
        lines = self.document().blockCount()
        digits = len(str(lines))
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _=0):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, _=0):
        self.lineNumberArea.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height())

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor(Qt.white))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Adjust the starting block number to account for any initial blocks that are not visible
        blockNumber += 1

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(), self.fontMetrics().height(),
                                 Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def highlightCurrentLine(self):
        extraSelections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            lineColor = QColor(Qt.black).lighter(160)

            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)

        self.setExtraSelections(extraSelections)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab and event.modifiers() == Qt.NoModifier:
            self.indentText(True)
        elif event.key() == Qt.Key_Backtab:  # Shift+Tab is recognized as Backtab
            self.indentText(False)
        else:
            super().keyPressEvent(event)

    def indentText(self, increase=True):
        cursor = self.textCursor()
    
        # Initialize start and end variables at the beginning
        start = cursor.position()
        end = start
    
        # Start operation
        cursor.beginEditBlock()
    
        if cursor.hasSelection():
            start = cursor.selectionStart()
            end = cursor.selectionEnd()
    
            cursor.setPosition(start, QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.MoveAnchor)
            start = cursor.position()
    
            cursor.setPosition(end, QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.MoveAnchor)
            end = cursor.position()
    
            cursor.setPosition(start)
            while cursor.position() <= end:  # Ensure the last line is included
                cursor.movePosition(QTextCursor.StartOfLine)
                lineText = cursor.block().text()
    
                if increase:
                    cursor.insertText("    ")  # Increase indentation
                    end += 4  # Adjust end position because we've added text
                else:
                    if lineText.startswith("    "):
                        cursor.movePosition(QTextCursor.StartOfLine)
                        cursor.deleteChar()
                        cursor.deleteChar()
                        cursor.deleteChar()
                        cursor.deleteChar()
                        end -= 4  # Adjust end position because we've removed text
    
                cursor.movePosition(QTextCursor.EndOfLine)
                if cursor.position() < end:
                    cursor.movePosition(QTextCursor.Down)
                else:
                    break
    
        else:
            cursor.select(QTextCursor.LineUnderCursor)
            lineText = cursor.block().text()
            if increase:
                # Move cursor to the start of the line before inserting text
                cursor.movePosition(QTextCursor.StartOfLine)
                cursor.insertText("    ")  # Increase indentation
                # Adjust end position after adding text
                end = start + 4
            else:
                if lineText.startswith("    "):
                    cursor.movePosition(QTextCursor.StartOfLine)
                    for _ in range(4):  # Remove four spaces
                        cursor.deleteChar()
                    end = start - 4  # Adjust end position since we've changed the text
    
        # End operation
        cursor.endEditBlock()
    
        # Restore cursor position to its original selection
        cursor.setPosition(start, QTextCursor.MoveAnchor)
        cursor.setPosition(end, QTextCursor.KeepAnchor)
        self.setTextCursor(cursor)

class FindReplaceWidget(QWidget):
    def __init__(self, text_editor):
        super().__init__()
        self.text_editor = text_editor
        self.initUI()

    def initUI(self):
        # Layouts
        main_layout = QVBoxLayout()
        find_layout = QHBoxLayout()
        replace_layout = QHBoxLayout()

        # Find widgets
        self.find_input = QLineEdit()
        self.find_button = QPushButton("Find")
        self.find_button.clicked.connect(self.find_text)

        find_layout.addWidget(QLabel("Find:"))
        find_layout.addWidget(self.find_input)
        find_layout.addWidget(self.find_button)

        # Replace widgets
        self.replace_input = QLineEdit()
        self.replace_button = QPushButton("Replace")
        self.replace_button.clicked.connect(self.replace_text)

        replace_layout.addWidget(QLabel("Replace with:"))
        replace_layout.addWidget(self.replace_input)
        replace_layout.addWidget(self.replace_button)

        # Add layouts to main layout
        main_layout.addLayout(find_layout)
        main_layout.addLayout(replace_layout)

        self.setLayout(main_layout)

    def find_text(self):
        text = self.find_input.text()
        if text == "":
            QMessageBox.information(self, "Find", "The search query is empty.")
            return
    
        # Try to find the text from the current cursor position
        if not self.text_editor.find(text):
            # If not found, wrap the search to the beginning and try again
            cursor = self.text_editor.textCursor()
            cursor.movePosition(QTextCursor.Start)
            self.text_editor.setTextCursor(cursor)
            if not self.text_editor.find(text):
                # If still not found, inform the user
                QMessageBox.information(self, "Find", f"Cannot find '{text}' anymore.")

    
    def replace_text(self):
        text = self.find_input.text()
        replace_with = self.replace_input.text()
    
        # Move cursor to the beginning to ensure all instances are replaced
        cursor = self.text_editor.textCursor()
        cursor.movePosition(QTextCursor.Start)
        self.text_editor.setTextCursor(cursor)
    
        found = False
        while self.text_editor.find(text):
            found = True
            cursor = self.text_editor.textCursor()
            cursor.insertText(replace_with)
    
        if found:
            QMessageBox.information(self, "Replace", f"All occurrences of '{text}' have been replaced.")
        else:
            QMessageBox.information(self, "Replace", f"Cannot find '{text}'")

        
class CustomCompleter(QCompleter):
    def __init__(self, vocabulary, text_editor, parent=None):
        super(CustomCompleter, self).__init__(vocabulary, parent)
        self.setPopup(QCompleter.popup(self))  # Ensure the popup is created
        self.pop_up = QCompleter.popup(self)
        self.pop_up.setItemDelegate(CustomDelegate())        
        self.editor = text_editor
        self.installEventFilter(self)
        self.activated.connect(lambda completion: self.insertCompletion(completion, text_editor))
        files = Files()
        filepaths = files.get_files_list()
        self.logger = set_logging('surf2', filepaths[0])        
        
    def eventFilter(self, obj, event):
        if event.type() == QKeyEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Tab.numerator and self.popup().isVisible():
                self.insertCompletion(self.currentCompletion(), self.editor)
                return True
        return super(CustomCompleter, self).eventFilter(obj, event)
    
    def insertCompletion(self, completion, text_editor):
        try:
            
            tc = text_editor.textCursor()
            extra = len(completion) - len(self.completionPrefix())
            tc.movePosition(QTextCursor.MoveOperation.EndOfWord)
            tc.insertText(completion[-extra:])
            text_editor.setTextCursor(tc)

        except AttributeError as e:
            self.logger.info(e)
            sys.exit()


class CssEditor(CodeEditor):
    def __init__(self, parent):
        super().__init__(parent)
        # Add syntax highlighting
        self.highlighter = HtmlCssJsHighlighter(self.document())
        
        # Create a container widget and a layout for it
        self.container = QWidget()
        layout = QHBoxLayout()
        
        # Add the CssEditor itself to the layout
        layout.addWidget(self)
        
        # Button to find CSS selector
        self.find_selector_button = QPushButton("Find Selector")
        layout.addWidget(self.find_selector_button)
        
        # Set the layout on the container widget
        self.container.setLayout(layout)
        
        # Assuming parent is a QTabWidget, add the container as a tab
        if isinstance(parent, QTabWidget):
            parent.addTab(self.container, 'CSSEdit')

        self.parent = parent
        
    def get_button(self):
        return self.find_selector_button

    def load_css_file(self, file_path):
        file = QFile(file_path)
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.css_editor.setPlainText(stream.readAll())
            file.close()

    def find_selector(self, other_editor):
        # Assuming another editor is a QTextEdit instance named `self.other_editor`
        # For demonstration, let's just assume other_editor is passed as an argument
        selector = other_editor.textCursor().selectedText()

        if selector:
            # No longer move cursor to the beginning of the document by default

            # Try to find the selector from the current cursor position
            found = self.find(selector)
            if not found:
                # If not found, try searching from the beginning to catch any occurrences before the current cursor position
                cursor = self.textCursor()
                cursor.movePosition(QTextCursor.Start)
                self.setTextCursor(cursor)

                if not self.find(selector):
                    # If still not found, then the selector does not exist in the document
                    print(f"Selector '{selector}' not found in the CSS file.")

class SyntaxVocabulary:
    def __init__(self):
        
        self.html_vocab = ['<a>', '<abbr>', '<address>', '<area>', '<article>', '<aside>',
                      '<audio>', '<b>', '<base>', '<bdi>', '<bdo>', '<blockquote>', '<body>',
                      '<br>', '<button>', '<canvas>', '<caption>', '<cite>', '<code>',
                      '<col>', '<colgroup>', '<data>', '<datalist>', '<dd>', '<del>',
                      '<details>', '<dfn>', '<dialog>', '<div>', '<dl>', '<dt>', '<em>',
                      '<embed>', '<fieldset>', '<figcaption>', '<figure>', '<footer>',
                      '<form>', '<h1>', '<h2>', '<h3>', '<h4>', '<h5>', '<h6>', '<head>',
                      '<header>', '<hr>', '<html>', '<i>', '<iframe>', '<img>', '<input>',
                      '<ins>', '<kbd>', '<keygen>', '<label>', '<legend>', '<li>', '<link>',
                      '<main>', '<map>', '<mark>', '<menu>', '<menuitem>', '<meta>',
                      '<meter>', '<nav>', '<noscript>', '<object>', '<ol>', '<optgroup>',
                      '<option>', '<output>', '<p>', '<param>', '<picture>', '<pre>',
                      '<progress>', '<q>', '<rp>', '<rt>', '<ruby>', '<s>', '<samp>',
                      '<script>', '<section>', '<select>', '<small>', '<source>', '<span>',
                      '<strong>', '<style>', '<sub>', '<summary>', '<sup>', '<table>',
                      '<tbody>', '<td>', '<template>', '<textarea>', '<tfoot>', '<th>',
                      '<thead>', '<time>', '<title>', '<tr>', '<track>', '<u>', '<ul>',
                      '<var>', '<video>', '<wbr>',   '<acronym>', '<applet>', '<basefont>',
                      '<bgsound>', '<big>', '<blink>', '<center>',   '<content>', '<dir>',
                      '<element>', '<font>', '<frame>', '<frameset>', '<hgroup>', 
                      '<image>', '<isindex>', '<keygen>', '<listing>', '<marquee>', '<multicol>', 
                      '<nextid>', '<nobr>', '<noembed>', '<noframes>', '<plaintext>', '<shadow>', 
                      '<spacer>', '<strike>', '<tt>', '<xmp>'
                      ]
        #html_vocab = html_vocab + self.add_end_tags(html_vocab)
        self.js_syntax = [
            'switch', 'case', 'default', 'delete', 'typeof', 'void', 'instanceof', 'in',
            'yield', 'yield*', 'with', 'debugger', 'eval', 'parseInt', 'parseFloat',
            'isNaN', 'isFinite', 'encodeURI', 'encodeURIComponent', 'decodeURI',
            'decodeURIComponent', 'Math', 'Date', 'RegExp', 'Infinity', 'NaN',
            'setTimeout', 'setInterval', 'clearTimeout', 'clearInterval', 'Promise', 'Map',
            'Set', 'WeakMap', 'WeakSet', 'Symbol', 'BigInt', 'ArrayBuffer',
            'SharedArrayBuffer', 'DataView', 'TypedArray', 'Proxy', 'Reflect', 'eval',
            'arguments', 'template literals', 'destructuring assignment',
            'spread operator', 'rest parameters', 'arrow functions', 'default parameters',
            'for...of', 'for...in', 'getter', 'setter', 'static', 'private field', '#',
            'public field', 'optional chaining', '?.', 'nullish coalescing operator', '??',
            'logical assignment operators', 'bitwise operators', 'template tags',
            'dynamic import', 'BigInt literals', 'lookbehind assertion in RegExp',
            'named capture groups in RegExp', 'Unicode property escapes in RegExp',
            's (dotAll) flag for RegExp', 'private methods in classes',
            'static blocks in classes', 'logical nullish assignment (??=)',
            'numeric separators', 'top-level await', 'import.meta', 'WeakRef',
            'FinalizationRegistry', 'var', 'let', 'const', 'if', 'else', 'for', 'while',
            'do', 'function', 'return', 'break', 'continue', 'try', 'catch', 'finally',
            'throw', 'class', 'await', 'async', 'console.log', 'document.querySelector',
            'fetch', 'Array', 'String', 'Object', 'Number', 'Boolean', 'null', 'undefined',
            'new', 'this', 'super', 'import', 'export'
        ]
        
        self.css_items = [
            'color', 'display', 'block', 'inline', 'flex', 'grid', 'none', 'position',
            'static', 'relative', 'absolute', 'fixed', 'sticky', 'font-size',
            'background-color', 'margin', 'margin-top', 'margin-right', 'margin-bottom',
            'margin-left', 'padding', 'padding-top', 'padding-right', 'padding-bottom',
            'padding-left', 'border', 'border-width', 'border-style', 'border-color',
            'border-top', 'border-right', 'border-bottom', 'border-left', 'border-radius',
            'width', 'height', 'min-width', 'min-height', 'max-width', 'max-height',
            'box-sizing', 'overflow', 'overflow-x', 'overflow-y', 'background',
            'background-image', 'background-repeat', 'background-position',
            'background-size', 'background-attachment', 'font-family', 'font-weight',
            'font-style', 'line-height', 'letter-spacing', 'text-align', 'text-decoration',
            'text-transform', 'text-shadow', 'color', 'opacity', 'visibility', 'z-index',
            'box-shadow', 'transform', 'transform-origin', 'transition',
            'transition-property', 'transition-duration', 'transition-timing-function',
            'transition-delay', 'animation', 'animation-name', 'animation-duration',
            'animation-timing-function', 'animation-delay', 'animation-iteration-count',
            'animation-direction', 'animation-fill-mode', 'flex-direction', 'flex-wrap',
            'flex-flow', 'justify-content', 'align-items', 'align-content', 'flex-grow',
            'flex-shrink', 'flex-basis', 'grid-template-columns', 'grid-template-rows',
            'grid-column-gap', 'grid-row-gap', 'grid-gap', 'grid-auto-rows',
            'grid-auto-columns', 'grid-auto-flow', 'grid', 'grid-template',
            'grid-template-areas', 'grid-area', 'justify-items', 'align-self',
            'justify-self', 'list-style', 'list-style-type', 'list-style-position',
            'list-style-image', 'cursor', 'filter', 'object-fit', 'object-position',
            'content', 'quotes', 'outline', 'outline-width', 'outline-style',
            'outline-color', 'outline-offset', 'clip-path', 'backface-visibility',
            'perspective', 'perspective-origin', 'user-select', 'pointer-events', 'resize',
            'scroll-behavior', 'will-change', 'white-space', 'word-wrap', 'word-break',
            'vertical-align', 'table-layout', 'caption-side', 'empty-cells',
            'border-collapse', 'border-spacing', 'direction', 'unicode-bidi',
            'writing-mode', 'text-orientation', 'ruby-align', 'ruby-position', 'gap',
            'align-tracks', 'justify-tracks', 'place-content', 'place-items', 'place-self',
            'aspect-ratio', '@media', '@supports', '@keyframes', '@font-face', '@import',
            '@charset', '@namespace', 'var()', 'calc()', 'min()', 'max()', 'clamp()',
            'inherit', 'initial', 'unset', 'revert'
        ]

        
    def add_end_tags(self, tags):
        return [f'</{tag[1:]}' for tag in tags]
    
    def get_all_vocab(self):
        return self.html_vocab + self.js_syntax + self.css_items
    
    def get_js_vocab(self):
        return self.js_syntax
    
class ClosableTabBar(QTabBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        files =  Files()
        filepaths = files.get_files_list()
        close_icon_fp = filepaths[4]
        # Enable mouse tracking to detect mouse movement over the widget
        self.setMouseTracking(True)
        # Load the close icon
        self.closeIcon = QIcon(close_icon_fp)  # Adjust path as necessary
        
    def tabSizeHint(self, index, width=20):
        size = super().tabSizeHint(index)
        # Add extra width for the close button
        size.setWidth(size.width() + width)  
        return size

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        for index in range(self.count()):
            tabRect = self.tabRect(index)
            #tabText = self.tabText(index)

            # Draw the tab text
            #painter.drawText(tabRect, Qt.AlignCenter, tabText)

            # Draw the close icon
            closeButtonRect = QRect(tabRect.right() - 16, tabRect.top() + (tabRect.height() - 20) // 2, 20, 20)
            self.closeIcon.paint(painter, closeButtonRect)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        for index in range(self.count()):
            tabRect = self.tabRect(index)
            closeButtonRect = QRect(tabRect.right() - 16, tabRect.top() + (tabRect.height() - 20) // 2, 20, 20)
            if closeButtonRect.contains(event.pos()):
                # Emit the tabCloseRequested signal
                self.tabCloseRequested.emit(index)  
                break
