#kevin fink
#kevin@shorecode.org
#Sun Apr 28 06:40:48 PM +07 2024
#surf_extensions.py

import re
import sys
from surf_logging import set_logging
from surf_filepaths import Files
from PySide6.QtWidgets import (QPlainTextEdit,
        QWidget, QTextEdit, QCompleter, QHBoxLayout, QVBoxLayout, QMessageBox,
        QLineEdit, QPushButton, QLabel, QTabWidget, QStyledItemDelegate, QTabBar,
        QTreeView, QSplitter, QLineEdit, QScrollArea, QCheckBox, QGridLayout)        
from PySide6.QtGui import (QSyntaxHighlighter, QTextCharFormat, QColor, QPainter,
        QColor, QTextFormat, QTextCursor, QKeyEvent, QIcon,
        QStandardItem, QStandardItemModel)
from PySide6.QtCore import (QRegularExpression, Qt,
        QTextStream, QFile, QRect, QObject, Slot, Signal)
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import  QWebEnginePage

class CustomDelegate(QStyledItemDelegate):
    """
    A custom delegate that modifies the size hint of auto-complete items to reduce their height.

    Inheritance:
    - QStyledItemDelegate: QT object used as a template.
    """
    
    def __init__(self, parent=None):
        super(CustomDelegate, self).__init__(parent)

    def sizeHint(self, option, index):
        """
        Returns the size hint for an item, with a modified height.
        
        The height of the item is reduced by 15 pixels from the default size hint.
        
        Parameters:
        - option: The option providing style options for the item.
        - index: The index of the item in the model.
        
        Returns:
        - QSize: The modified size hint for the item.
        """        
        size = super(CustomDelegate, self).sizeHint(option, index)
        # Reduce the height of each item, adjust according to your needs
        size.setHeight(size.height() - 15)
        return size

class HtmlCssJsHighlighter(QSyntaxHighlighter):
    """
    A syntax highlighter for HTML, CSS, and JavaScript code.
    
    This highlighter applies different text formatting rules for various elements of HTML, CSS,
    and JavaScript, such as tags, attributes, selectors, properties, keywords, and comments.
    
    Inheritance:
    - QSyntaxHighlighter: QT object of this highlighter used as a template.
    """    
    def __init__(self, parent=None):
        """
        Sets up the highlighting rules for different syntax elements.
        
        This internal method initializes text formatting for HTML tags, attributes, CSS selectors,
        properties, JavaScript keywords, special characters, strings, numbers, and comments.
        """        
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
        """
        Applies syntax highlighting to the given block of text.
        
        This method is called automatically by the QSyntaxHighlighter to apply the highlighting
        rules to each block of text in the document.
        
        Parameters:
        - text: The text block to highlight.
        """        
        for pattern, format in self.highlightingRules:
            expression = QRegularExpression(pattern)
            matchIterator = expression.globalMatch(text)
            while matchIterator.hasNext():
                match = matchIterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

class LineNumberArea(QWidget):
    """
    A widget for displaying line numbers in a QTextEdit or QPlainTextEdit.
    
    This widget is intended to be used as a child of a text editor widget to display line numbers
    adjacent to the text. It should be updated in response to changes in the editor's document or
    viewport.
    
    Inheritance:
    - QWidget: QT object used as a template.
    """    
    def __init__(self, editor):
        """
            Parameters:
            - editor: The text editor widget to which this line number area is associated.
        """         
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        """
         Returns the recommended size for the line number area.
         
         The width is determined by the associated code editor's lineNumberAreaWidth method,
         and the height is set to 0, allowing the layout to adjust dynamically.
         
         Returns:
         - QSize: The recommended size for the widget.
         """        
        return QSize(self.codeEditor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        """
        Handles the paint event for the line number area.
        
        This method is called whenever the line number area needs to be repainted, such as when
        the editor is scrolled or resized.
        
        Parameters:
        - event: The QPaintEvent object containing event details.
        """        
        self.codeEditor.lineNumberAreaPaintEvent(event)

class CodeEditor(QPlainTextEdit):
    """
    A custom code editor widget that extends QPlainTextEdit to support line numbers,
    syntax highlighting, and other features useful for coding.

    Attributes:
        - lineNumberArea (QWidget): A widget that displays line numbers adjacent to the editor.
    Inheritance:
        - QPlainTextEdit: QT object used as template.
    """    
    def __init__(self, parent=None):
        """
        Initializes the CodeEditor instance.

        Args:
            parent (QWidget, optional): The parent widget. Defaults to None.
        """        
        super().__init__(parent)
        self.lineNumberArea = LineNumberArea(self)

        self.textChanged.connect(self.updateLineNumberAreaWidth)
        self.verticalScrollBar().valueChanged.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)  # Initial update with default value

    def lineNumberAreaWidth(self):
        """
        Calculates the width of the line number area based on the number of lines in the document.
    
        Returns:
            int: The width of the line number area in pixels.
        """        
        lines = self.document().blockCount()
        digits = len(str(lines))
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _=0):
        """
        Updates the width of the line number area. This method is typically called when the number
        of lines in the document changes.
    
        Args:
            _ (int, optional): Placeholder parameter, not used. Defaults to 0.
        """        
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, _=0):
        """
        Redraws the line number area. This method is typically called when the document is scrolled
        or the line number area width is updated.
    
        Args:
            _ (int, optional): Placeholder parameter, not used. Defaults to 0.
        """                
        self.lineNumberArea.update()

    def resizeEvent(self, event):
        """
        Handles the resize event for the CodeEditor widget. This method is overridden to adjust
        the line number area's size and position accordingly.
    
        Args:
            event (QResizeEvent): The resize event.
        """        
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height())

    def lineNumberAreaPaintEvent(self, event):
        """
        Paints the line numbers in the line number area.
    
        Args:
            event (QPaintEvent): The paint event.
        """        
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
        """
        Highlights the current line where the cursor is located. This provides a visual cue for
        the user to easily identify the active line.
        """        
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
        """
        Handles key press events for the CodeEditor widget. This method is overridden to implement
        custom behavior for tab and shift+tab (indent and un-indent).
    
        Args:
            event (QKeyEvent): The key event.
        """        
        if event.key() == Qt.Key_Tab and event.modifiers() == Qt.NoModifier:
            self.indentText(True)
        elif event.key() == Qt.Key_Backtab:  # Shift+Tab is recognized as Backtab
            self.indentText(False)
        else:
            super().keyPressEvent(event)

    def indentText(self, increase=True):
        """
        Indents or un-indents the selected text or the current line if no text is selected.
    
        Args:
            increase (bool, optional): If True, indents the text. If False, un-indents the text. Defaults to True.
        """        
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
    """
    A widget that provides find and replace functionality for a text editor.

    Attributes:
        -text_editor (QPlainTextEdit): The text editor to which the find and replace functionality is applied.
    Inheritance:
        - QWidget: QT object used as template.
    """    
    def __init__(self, text_editor):
        """
        Initializes the FindReplaceWidget instance.

        Args:
            text_editor (QPlainTextEdit): The text editor to which the find and replace functionality will be applied.
        """        
        super().__init__()
        self.text_editor = text_editor
        self.initUI()

    def initUI(self):
        """
        Initializes the user interface components of the FindReplaceWidget.

        Sets up the layout, input fields, buttons, and connects button click events to their respective methods.
        """        
        # Main layout
        grid_layout = QGridLayout()
    
        # Find widgets
        self.find_input = QLineEdit()
        self.find_button = QPushButton("Find")
        self.find_button.clicked.connect(self.find_text)
    
        grid_layout.addWidget(QLabel("Find:"), 0, 0)  # Row 0, Column 0
        grid_layout.addWidget(self.find_input, 0, 1)  # Row 0, Column 1
        grid_layout.addWidget(self.find_button, 0, 2)  # Row 0, Column 2
    
        # Search area
        self.searchLineEdit = QLineEdit(self)
        self.searchButton = QPushButton("Find All", self)
        self.searchButton.clicked.connect(self.parseText)
    
        grid_layout.addWidget(QLabel("Find All:"), 1, 0)  # Row 1, Column 0
        grid_layout.addWidget(self.searchLineEdit, 1, 1)  # Row 1, Column 1
        grid_layout.addWidget(self.searchButton, 1, 2)  # Row 1, Column 2
    
        # Replacement area
        self.replaceLineEdit = QLineEdit(self)
        self.replaceButton = QPushButton("Replace Selected", self)
        self.replaceButton.clicked.connect(self.replaceChecked)
    
        grid_layout.addWidget(QLabel("Replace with:"), 3, 0)  # Row 2, Column 0
        grid_layout.addWidget(self.replaceLineEdit, 3, 1)  # Row 2, Column 1
        grid_layout.addWidget(self.replaceButton, 4, 0, 1, 2)  # Row 2, Column 2
    
        # Results area
        self.resultsWidget = QWidget()
        self.resultsLayout = QVBoxLayout(self.resultsWidget)
    
        # Scroll Area for results
        self.resultsScrollArea = QScrollArea()
        self.resultsScrollArea.setWidgetResizable(True)
        self.resultsScrollArea.setWidget(self.resultsWidget)
    
        self.selectAllButton = QPushButton("Select All", self)
        self.selectAllButton.clicked.connect(self.selectAllCheckboxes)
        grid_layout.addWidget(self.selectAllButton, 3, 3, 1, 1)  # Row 2, Column 0, Span 1 row, Span 2 columns
        
        self.unselectAllButton = QPushButton("Unselect All", self)
        self.unselectAllButton.clicked.connect(self.unselectAllCheckboxes)
        grid_layout.addWidget(self.unselectAllButton, 4, 3, 1, 1)  # Row 2, Column 1, Span 1 row, Span 2 columns    
        # Adding the results scroll area to the grid layout
        # Since the scroll area should span multiple columns, we use the addWidget method with row, column, rowspan, and colspan parameters
        grid_layout.addWidget(self.resultsScrollArea, 2, 0, 1, 3)  # Row 3, Column 0, Span 1 row, Span 3 columns

        # Set the main layout
        self.setLayout(grid_layout)

    def selectAllCheckboxes(self):
        """
        Selects all checkboxes in the results area, marking all found occurrences for replacement.
        """        
        for i in range(self.resultsLayout.count()):
            widget = self.resultsLayout.itemAt(i).widget()
            if isinstance(widget, QCheckBox):
                widget.setChecked(True)

    def unselectAllCheckboxes(self):
        """
        Unselects all checkboxes in the results area, clearing selection of found occurrences.
        """        
        for i in range(self.resultsLayout.count()):
            widget = self.resultsLayout.itemAt(i).widget()
            if isinstance(widget, QCheckBox):
                widget.setChecked(False)

    def find_text(self):
        """
        Initiates a search for the text entered in the find input field within the text editor.

        Displays a message if the search query is empty or if the text cannot be found.
        """        
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
        """
        Replaces the currently selected occurrence of the found text with the replacement text.

        If no text is selected, it attempts to find and replace the next occurrence.
        """        
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
            
    def parseText(self):
        """
        Finds all occurrences of the search term entered in the search input field and displays them as checkboxes
        in the results area, allowing the user to select which occurrences to replace.
        """        
        # Clear previous results
        while item := self.resultsLayout.takeAt(0):
            item.widget().deleteLater()

        search_term = self.searchLineEdit.text()
        text = self.text_editor.toPlainText()
        lines = text.split('\n')

        match_count = 0
        self.matches = dict()
        for i, line in enumerate(lines):
            if search_term in line:
                self.matches[match_count] = [i, line.strip()]
                cb = QCheckBox(f'line {i+1}: ' + line.strip())
                self.resultsLayout.addWidget(cb)
                match_count += 1 

    def replaceChecked(self):
        """
        Replaces all selected occurrences of the found text with the replacement text.

        Only occurrences that are marked by checked checkboxes in the results area will be replaced.
        """        
        # Save the current cursor position
        current_cursor = self.text_editor.textCursor()
        original_position = current_cursor.position()
    
        text = self.text_editor.toPlainText()
        replacement_text = self.replaceLineEdit.text()
        search_term = self.searchLineEdit.text()
        lines = text.split('\n')
    
        for i in range(self.resultsLayout.count()):
            checkbox = self.resultsLayout.itemAt(i).widget()
            if checkbox.isChecked():
                result_term = self.matches[i][1]
                line = self.matches[i][0]
                temp_replacement = result_term.replace(search_term, replacement_text)
                print(temp_replacement)
                lines[line] = lines[line].replace(result_term, temp_replacement)
    
        # Update the text in the editor
        self.text_editor.setPlainText('\n'.join(lines))
    
        # Restore the cursor position
        new_cursor = QTextCursor(self.text_editor.document())
        new_cursor.setPosition(min(original_position, self.text_editor.document().characterCount() - 1))
        self.text_editor.setTextCursor(new_cursor)    
        
    def updateEditor(self, editor):
        """
        Updates the reference to the text editor to a new editor.

        This allows the FindReplaceWidget to be used with a different text editor.

        Args:
            editor (QPlainTextEdit): The new text editor to apply the find and replace functionality to.
        """        
        self.text_editor = editor

class CustomCompleter(QCompleter):
    """
    A custom completer that provides auto-completion for a text editor, supporting dot notation and other features.

    Attributes:
        editor (QPlainTextEdit): The text editor to which the completer is attached.
        pop_up (QWidget): The popup widget used to display completion suggestions.
    Inheritance:
        - QCompleter: QT object used as template.
    """    
    def __init__(self, vocabulary, text_editor, parent=None):
        """
        Initializes the CustomCompleter instance.

        Args:
            vocabulary (list or QStringList): The list of words or phrases that the completer uses for suggestions.
            text_editor (QPlainTextEdit): The text editor to which the completer is attached.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """        
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
        #self.editor.textChanged.connect(self.onTextChanged)

    #def onTextChanged(self):
        #cursor_pos = self.editor.textCursor().position()
        #text_up_to_cursor = self.editor.toPlainText()[:cursor_pos]
        #last_word = text_up_to_cursor.split(' ')[-1]  # Adjust if you need to split by other characters
        #if '.' in last_word:
            #self.setCompletionPrefix(last_word.split('.')[-1])
        #if '(' in last_word:
            #self.setCompletionPrefix(last_word.split('(')[-1])
        #if '\n' in last_word:
            #self.setCompletionPrefix(last_word.split('\n')[-1])
        #else:
            #self.setCompletionPrefix(last_word)
            ## Only update the completion prefix if the last character is not a space
            #if not text_up_to_cursor.endswith(' '):
                #self.popup().show()
            #else:
                #self.popup().hide()        

    def eventFilter(self, obj, event):
        if event.type() == QKeyEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Tab.numerator and self.popup().isVisible():
                if self.popup().currentIndex().data():                    
                    self.insertCompletion(self.popup().currentIndex().data(), self.editor)
                else:
                    self.insertCompletion(self.currentCompletion(), self.editor)
                return True
        return super(CustomCompleter, self).eventFilter(obj, event)
    
    def insertCompletion(self, completion, text_editor):
        try:
            tc = text_editor.textCursor()
            full_text = text_editor.toPlainText()
            cursor_pos = tc.position()
            
            # Find the text from the start to the cursor position
            text_to_cursor = full_text[:cursor_pos]
            
            # Find the last occurrence of '.' before the cursor position
            dot_pos = text_to_cursor.rfind('.')
            
            if dot_pos != -1:
                # Calculate how much text to replace after the dot
                ##extra = len(completion) - len(self.completionPrefix())
                tc.setPosition(dot_pos + 1, QTextCursor.MoveAnchor)
                tc.movePosition(QTextCursor.MoveOperation.EndOfWord, QTextCursor.KeepAnchor)
                tc.insertText(completion[-extra:])
            else:
                # No dot found, fallback to default behavior
                extra = len(completion) - len(self.completionPrefix())
                tc.movePosition(QTextCursor.MoveOperation.EndOfWord)
                tc.insertText(completion[-extra:])
                
            text_editor.setTextCursor(tc)
        except AttributeError as e:
            self.logger.info(e)
            sys.exit()

    #def splitPath(self, path):
        ## Override splitPath to handle dot notation
        #if '.' in path:
            #return path.split('.')[-1]
        #return path

    #def pathFromIndex(self, index):
        ## Override pathFromIndex to ensure the completer works with dot notation
        #return super(CustomCompleter, self).pathFromIndex(index)    

class CssEditor(CodeEditor):
    """
    A specialized code editor designed for editing CSS files, extending the generic CodeEditor class.

    Attributes:
        highlighter: An instance of HtmlCssJsHighlighter for syntax highlighting within the document.
        container: A QWidget that serves as a container for the editor and additional UI elements.
        find_selector_button: A QPushButton used to initiate the search for a CSS selector within the document.
        parent: The parent widget, typically a QTabWidget, to which this editor is attached as a tab.

    Methods:
        __init__(self, parent): Initializes the CssEditor with a parent widget.
        get_button(self): Returns the find_selector_button.
        load_css_file(self, file_path): Loads a CSS file's content into the editor.
        find_selector(self, other_editor): Searches for a CSS selector based on the selection in another editor.
    Inheritance:
        - CodeEditor: Custom QT object used as template.
    """    
    def __init__(self, parent):
        """
        Initializes the CssEditor with syntax highlighting, layout configuration, and UI elements.

        Parameters:
            parent: The parent widget, typically a QTabWidget, to which this editor is attached.
        """        
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
        """
        Returns the QPushButton used to find a CSS selector within the document.

        Returns:
            QPushButton: The button used for initiating a search for a CSS selector.
        """        
        return self.find_selector_button

    def load_css_file(self, file_path):
        """
        Loads the content of a CSS file into the editor.

        Parameters:
            file_path (str): The path to the CSS file to be loaded.
        """        
        file = QFile(file_path)
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.css_editor.setPlainText(stream.readAll())
            file.close()

    def find_selector(self, other_editor):
        """
        Searches for a CSS selector in the document based on the selection in another editor.

        Parameters:
            other_editor (QTextEdit): Another text editor instance from which the selected text is used as the search query.
        """        
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
    """
    A class representing the syntax vocabulary for HTML, JavaScript, and CSS.

    Attributes:
        html_vocab (list): A list of HTML tags and elements.
        js_syntax (list): A list of JavaScript syntax elements and keywords.
        css_items (list): A list of CSS properties and selectors.

    Methods:
        add_end_tags(self, tags): Generates closing tags for a list of HTML opening tags.
        get_all_vocab(self): Returns a combined list of all vocabulary items.
        get_js_vocab(self): Returns the list of JavaScript vocabulary items.
    """    
    def __init__(self):
        """
        Initializes the SyntaxVocabulary with predefined lists of HTML, JavaScript, and CSS vocabulary.
        """        
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
            'arguments',
            'for...of', 'for...in', 'getter', 'setter', 'static',       
            'import.meta', 'WeakRef',
            'FinalizationRegistry', 'var', 'let', 'const', 'if', 'else', 'for', 'while',
            'do', 'function', 'return', 'break', 'continue', 'try', 'catch', 'finally',
            'throw', 'class', 'await', 'async', 'console.log', 'document', 'querySelector',
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
        """
        Generates closing tags for a list of HTML opening tags.

        Parameters:
            tags (list): A list of HTML opening tags.

        Returns:
            list: A list containing the corresponding closing tags for the input opening tags.
        """        
        return [f'</{tag[1:]}' for tag in tags]
    
    def get_all_vocab(self):
        """
        Returns a combined list of all vocabulary items across HTML, JavaScript, and CSS.

        Returns:
            list: A combined list of HTML tags, JavaScript syntax elements, and CSS properties.
        """        
        return self.html_vocab + self.js_syntax + self.css_items
    
    def get_js_vocab(self):
        """
        Returns the list of JavaScript vocabulary items.

        Returns:
            list: A list of JavaScript syntax elements and keywords.
        """        
        return self.js_syntax
    
class ClosableTabBar(QTabBar):
    """
    A custom QTabBar widget that supports closable tabs with a close icon.

    Attributes:
        closeIcon (QIcon): Icon displayed on each tab for closing the tab.

    Args:
        parent (QWidget, optional): The parent widget. Defaults to None.
    Inheritance:
        - QTabBar: QT object used as template.

    """    
    def __init__(self, parent=None):
        """
        Initializes the ClosableTabBar with a close icon for each tab.
        """        
        super().__init__(parent)
        files =  Files()
        filepaths = files.get_files_list()
        close_icon_fp = filepaths[4]
        # Enable mouse tracking to detect mouse movement over the widget
        self.setMouseTracking(True)
        # Load the close icon
        self.closeIcon = QIcon(close_icon_fp)  # Adjust path as necessary
        
    def tabSizeHint(self, index, width=20):
        """
        Provides a size hint for each tab, including extra width for the close button.

        Args:
            index (int): The index of the tab.
            width (int, optional): The additional width for the close button. Defaults to 20.

        Returns:
            QSize: The recommended size for the tab.
        """        
        size = super().tabSizeHint(index)
        # Add extra width for the close button
        size.setWidth(size.width() + width)  
        return size

    def paintEvent(self, event):
        """
        Custom paint event to draw the close icon on each tab.

        Args:
            event (QPaintEvent): The paint event.
        """        
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
        """
        Mouse press event to handle clicks on the close icon of tabs.

        Args:
            event (QMouseEvent): The mouse event.
        """        
        super().mousePressEvent(event)
        for index in range(self.count()):
            tabRect = self.tabRect(index)
            closeButtonRect = QRect(tabRect.right() - 16, tabRect.top() + (tabRect.height() - 20) // 2, 20, 20)
            if closeButtonRect.contains(event.pos()):
                # Emit the tabCloseRequested signal
                self.tabCloseRequested.emit(index)  
                break

class SkeletonTree(QTreeView):
    """
    A custom QTreeView widget designed to display a hierarchical structure of elements,
    typically representing the structure of a document or a piece of code.

    Attributes:
        model (QStandardItemModel): The model providing items to the view.
        last_clicked_item (QStandardItem, optional): The last item clicked in the tree view.
        last_found_position (int): The position of the last found item, used for navigation.

    Args:
        editor (QPlainTextEdit): The editor whose content is used to populate the tree view.    
    Inheritance:
        - QTreeView: QT object used as template.        
    """
    def __init__(self, editor):
        """
        Initializes the SkeletonTree with the content from the specified editor.
        """        
        super().__init__()
        self.setEditTriggers(QTreeView.NoEditTriggers)
        self.clicked.connect(self.on_item_clicked)

        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.update_tree_view(editor)

        # Attributes to track the last clicked item and its last found position
        self.last_clicked_item = None
        self.last_found_position = -1
        
    def filter_content(self, preserved_text):
        """
        Filters the content to simplify it for display in the tree view.

        Args:
            preserved_text (str): The text content to be filtered.

        Returns:
            str: The filtered text content.
        """        
        # Remove multiline comments from <script> content
        def clean_script_content(match):
            # Remove multiline comments within script tags
            script_content = re.sub(r'/\*[\s\S]*?\*/', '', match.group(0))
            return script_content

        # Apply cleaning function to <script> tags
        preserved_text = re.sub(r'<script[\s\S]*?</script>', clean_script_content, preserved_text)

        # Apply existing simplification rules outside of <script> tags
        filtered_text = re.sub(r'(\{[^}]*\})', lambda m: '{ }' if m.group(1).strip() != '{}' else '{}', preserved_text)
        filtered_text = re.sub(r'(function\s+\w+\s*\([^)]*\)\s*\{)\s*[^}]*', r'\1}', filtered_text)
        filtered_text = re.sub(r'</(img|br|hr|input|meta|link|area|base|col|command|embed|keygen|param|source|track|wbr)>', '', filtered_text)
        filtered_text = re.sub(r'</\w+>', '', filtered_text)
        filtered_text = re.sub(r'/\*[\s\S]*?\*/', '', filtered_text)
        filtered_text = re.sub(r'\{\s*\}', '', filtered_text)
        filtered_text = re.sub(r'\[\s*\]', '', filtered_text)
        filtered_text = re.sub(r'\(\s*\)', '', filtered_text)

        return filtered_text

    def update_tree_view(self, editor):
        """
        Updates the tree view based on the content of the specified editor.

        Args:
            editor (QPlainTextEdit): The editor whose content is used to update the tree view.
        """        
        self.editor = editor
        text = editor.toPlainText()
        text = self.filter_content(text)
    
        self.model.clear()
        last_item_at_level = {0: self.model.invisibleRootItem()}
    
        script_indentation_level = None
        inside_script_tag = False
        js_item = None
        for line in text.splitlines():
            indentation_level = len(line) - len(line.lstrip(' '))          
            level = indentation_level // 4
    
            item_text = line.strip()
            if not item_text:
                if js_item:
                    for i in range(8):
                        last_item_at_level[i] = js_item
                continue
    
            # Detect <script> tag to adjust nesting logic
            if '<script' in item_text and '</script>' not in item_text:
                inside_script_tag = True
                script_indentation_level = 0
                item = QStandardItem(item_text)
                js_item = item
                parent_item = last_item_at_level.get(level-1, self.model.invisibleRootItem())
                parent_item.appendRow(item)
                for i in range(5):                    
                    last_item_at_level[i] = item  # Adjust the level for children of <script>                    
                continue
            elif '</script>' in item_text:
                inside_script_tag = False
                script_indentation_level = None
                continue  # Skip adding </script> tag to the tree
    
            if inside_script_tag:
                # Adjust level for items inside script tag based on their indentation relative to the script tag
                adjusted_level = level
                if level == 0:
                    level = 1
                item = QStandardItem(item_text)
                parent_item = last_item_at_level.get(adjusted_level - 1, self.model.invisibleRootItem())
                parent_item.appendRow(item)
                for i in range(3):
                    last_item_at_level[adjusted_level+i] = item
            else:
                adjusted_level = level
                item = QStandardItem(item_text)
                parent_item = last_item_at_level.get(adjusted_level - 1, self.model.invisibleRootItem())
                parent_item.appendRow(item)
                last_item_at_level[adjusted_level] = item                
    
            # Clean up deeper levels from the tracking dict
            keys_to_delete = [key for key in last_item_at_level if key > adjusted_level]
            for key in keys_to_delete:
                del last_item_at_level[key]
                
    def on_item_clicked(self, index):
        """
        Handles the event when an item is clicked in the UI.
    
        This method searches for the text of the clicked item within a text editor widget,
        highlighting the found text and setting the cursor position to the start of this text.
        If the same item is clicked again, it continues the search from the last found position.
        If no more occurrences are found, it resets the search for this item.
    
        Parameters:
        - index: QModelIndex representing the index of the clicked item in the model.
        """        
        item = self.model.itemFromIndex(index)
        word = item.text()
        text = self.editor.toPlainText()

        # Check if the same item is clicked again
        if item == self.last_clicked_item:
            start_search_position = self.last_found_position + len(word)
        else:
            start_search_position = 0

        # Find the next matching item starting from the last found position + length of word
        start_index = text.find(word, start_search_position)

        if start_index != -1:
            self.editor.setFocus()
            cursor = self.editor.textCursor()
            cursor.setPosition(start_index, QTextCursor.MoveAnchor)
            cursor.setPosition(start_index + len(word), QTextCursor.KeepAnchor)
            self.editor.setTextCursor(cursor)

            # Update the last clicked item and its last found position
            self.last_clicked_item = item
            self.last_found_position = start_index
        else:
            # If no more matches are found, reset the search for this item
            if self.last_clicked_item == item:
                self.last_found_position = -1  # Reset for the current item
                self.on_item_clicked(index)  # Retry to find from the beginning
            self.last_clicked_item = None  # Reset if a different item is clicked
                                   
class Bridge(QObject):
    """
    A bridge class for logging messages from JavaScript to a Qt text widget.

    This class serves as a bridge between JavaScript running in a QWebEngineView and
    a Qt text widget, allowing messages to be logged to the Qt widget.

    Attributes:
    - output_console: A QTextEdit or similar widget used for displaying log messages.    
    Inheritance:
        - QObject: QT object used as template.
    """
    def __init__(self, output_console):
        """
        Initializes the Bridge object with an output console.

        Parameters:
        - output_console: QTextEdit or similar widget for displaying output.
        """        
        super().__init__()
        self.output_console = output_console

    @Slot(str)
    def log(self, message):
        """
        Appends a given message to the output console with a prefixed "> ".

        Parameters:
        - message: str, the message to log.
        """        
        self.output_console.append("> " + message)

class OutputConsole(QTextEdit):
    pass

class JsSandbox(QWidget):
    """
    A widget that provides an interface for running JavaScript in a sandboxed environment.

    This class combines a code editor for JavaScript, a button to execute the script,
    and an output console for displaying messages logged from the JavaScript code.
    It uses a QWebEngineView to run the JavaScript in a sandboxed environment.

    Attributes:
    - editor: CodeEditor, a text editor for writing JavaScript code.
    - output_console: OutputConsole, a widget for displaying logged messages.
    - view: QWebEngineView, the web view where JavaScript is executed.
    - bridge: Bridge, a bridge object for logging messages from JavaScript to the output console.
    - html_editor: QTextEdit, an editor for the HTML content that the JavaScript will interact with.
    
    Inheritance:
        - QWidget: QT object used as template.
    """
    
    def __init__(self, html_editor):
        """
        Initializes the JsSandbox widget with an HTML editor.

        Parameters:
        - html_editor: QTextEdit, an editor for the HTML content.
        """        
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.horizSplit = QSplitter(Qt.Vertical)

        # Plain text editor for HTML content
        self.editor = CodeEditor()
        self.horizSplit.addWidget(self.editor)
        
        # Output console for displaying messages from JavaScript
        self.output_console = OutputConsole()
        self.output_console.setReadOnly(True)  # Make the output console read-only
        self.horizSplit.addWidget(self.output_console)
        
        # WebEngineView for running JavaScript
        self.view = QWebEngineView()
        self.channel = QWebChannel()
        self.bridge = Bridge(self.output_console)
        self.channel.registerObject('surf', self.bridge)
        self.view.page().setWebChannel(self.channel)
        self.html_editor = html_editor
        
        self.view.setHtml(self.add_qbridge_html(init_text='''
surf.log('Hello from Shorecode');
surf.log('Your javascript debug will be displayed here,');
surf..og('use surf.log() like you would console.log()');
surf.log('Enter some javascript in the js sandbox editor, \
then hit run javascript to execute the sandbox code vs the code in the active Surf editor');'''))
        # Button to run JS code
        self.run_button = QPushButton("Run JavaScript")
        self.run_button.clicked.connect(self.run_javascript)
        self.layout.addWidget(self.horizSplit)  
        self.layout.addWidget(self.run_button)        

    def get_view(self):
        """
        Returns the QWebEngineView used for executing JavaScript.

        Returns:
        - QWebEngineView: The web view where JavaScript is executed.
        """        
        return self.view

    def run_javascript(self):
        """
        Executes the JavaScript code written in the code editor within the web view.
        """        
        # Example method to run JavaScript code and access the HTML content from the editor
        self.view.setHtml(self.add_qbridge_html())
        js_code = self.editor.toPlainText()
        self.view.page().runJavaScript(js_code)
        self.update_js_sandbox()
    
    def update_js_sandbox(self, editor=None):
        """
        Updates the HTML content in the web view with the content from the provided HTML editor.

        Parameters:
        - editor: QTextEdit, an optional editor containing new HTML content. If not provided,
                  the current html_editor's content is used.
        """        
        if editor != None:            
            self.html_editor = editor
        self.view.setHtml(self.add_qbridge_html())
        
    def add_qbridge_html(self, init_text=None):
        """
        Constructs the HTML content with the necessary JavaScript for the QWebChannel bridge.

        This method injects the bridge initialization script into the HTML content,
        allowing JavaScript executed in the web view to log messages to the output console.

        Parameters:
        - init_text: str, optional initial JavaScript to run when the page loads.

        Returns:
        - str: The constructed HTML content with the bridge initialization script.
        """        
        introduction = ''
        if init_text:
            introduction = init_text
        qbridge_html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <script type="text/javascript" src="qrc:///qtwebchannel/qwebchannel.js"></script>
            <script type="text/javascript">
                new QWebChannel(qt.webChannelTransport, function(channel) {
                    // Now the bridge object is available as channel.objects.surf
                    window.surf = channel.objects.surf;        
                    ''' + f'{introduction}' + '''                 
                });
            </script>       
        '''        
        editor_html = self.html_editor.toPlainText()
        html_injection = editor_html[editor_html.find('<head>') + len('<head>'):]
        if html_injection == -1:
            html_injection = editor_html[editor_html.find('<body>'):]
            html_injection = '</head>\n' + html_injection
        return qbridge_html + html_injection
    
class ConsoleWidget(QPlainTextEdit):
    """
    A read-only console widget for displaying log messages.

    Inheritance:
        - QPlainTextEdit: QT object used as template.
    """
    
    def __init__(self, parent=None):
        """
        Initializes the ConsoleWidget.

        :param parent: The parent widget.
        """        
        super().__init__(parent)
        self.setReadOnly(True)
    
    @Slot(str)
    def log_message(self, messages):
        """
        Logs a list of messages to the console.

        :param messages: A list of string messages to be logged.
        """        
        for message in messages:
            self.appendPlainText(message)
            
    def clear_console(self):
        """
        Clears the console and prints a new browser instance message.
        """        
        self.appendPlainText('')
        self.appendPlainText('---------------------------------------------------')
        self.appendPlainText('----------------New Browser Instance---------------')
        self.appendPlainText('---------------------------------------------------')
        self.appendPlainText('')

class ConsoleEnabledPage(QWebEnginePage):
    """
    A QWebEnginePage with the capability to handle and emit JavaScript console messages.
    
    Inheritance:
        - QWebEnginePage: QT object used as template.
    """
    
    newData = Signal(list)
    def __init__(self, *args, **kwargs):
        """
        Initializes the ConsoleEnabledPage.
        """        
        super().__init__(*args, **kwargs)

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        """
        Handles JavaScript console messages by emitting them as a signal.

        :param level: The message level.
        :param message: The message content.
        :param lineNumber: The line number where the message was generated.
        :param sourceID: The source ID of the message.
        """        
        l = message.split(",")
        l[0] = f'{sourceID}: Line {lineNumber} > ' + l[0]
        self.newData.emit(l)  # Emit the signal with the list
        
class AiWidget(QWidget):
    """
    A widget for interacting with an AI, allowing users to input queries and see responses.
    
    Inheritance:
        - QWidget: QT object used as template.
    """
    
    def __init__(self, ai_type):
        """
        Initializes the AiWidget with a specific AI type.

        :param ai_type: The type of AI interaction, e.g., 'bugfix' or 'refactor'.
        """        
        super().__init__()
        self.ai_type = ai_type
        self.query_placeholders = {'bugfix': "Enter the code block here to have AI fix the bugs...",
                                   'refactor': "Enter the code block here to have AI refactor it...",}
        self.initUI()

    def initUI(self):
        """
        Initializes the user interface components of the AiWidget.
        """        
        # Layout
        layout = QVBoxLayout()
        # Text entry area
        self.query_text_edit = QTextEdit()
        self.query_text_edit.setPlaceholderText(self.query_placeholders[self.ai_type])
        # Text display area
        self.answer_text_edit = QTextEdit()
        self.answer_text_edit.setReadOnly(True)
        # Button
        self.query_button = QPushButton("Query AI")
        # Add widgets to layout
        layout.addWidget(self.query_text_edit)
        layout.addWidget(self.answer_text_edit)
        layout.addWidget(self.query_button)
        # Set the layout on the application's window
        self.setLayout(layout)

class FlaskCompatWidget(QWidget):
    """
    A widget designed to facilitate Flask compatibility by parsing and modifying HTML content.
    
    Inheritance:
        - QWidget: QT object used as template.
    """

    def __init__(self, editor):
        """
        Initializes the FlaskCompatWidget with a reference to an HTML editor.

        :param editor: A QTextEdit instance used for editing HTML content.
        """        
        super().__init__()
        self.html_editor = editor
        self.matches_and_line_edits = []  # Store tuples of (match, QLineEdit)
        self.initUI()

    def initUI(self):
        """
        Initializes the user interface components of the FlaskCompatWidget.
        """        
        self.layout = QVBoxLayout()
        # Button to parse HTML
        self.parse_button = QPushButton("Parse HTML for Flask injections")
        self.parse_button.clicked.connect(self.parse_html)
        # Scroll area for matches and replacement UI
        self.scroll_area = QScrollArea()
        self.scroll_area_widget_contents = QWidget()
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_widget_contents)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_area_widget_contents)
        # Replace All button
        self.replace_all_button = QPushButton("Replace All")
        self.replace_all_button.clicked.connect(self.replace_all_matches)
        # Add widgets to layout
        self.layout.addWidget(self.parse_button)
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.replace_all_button)

        self.setLayout(self.layout)

    def parse_html(self):
        """
        Parses the HTML content from the editor and finds Jinja template code for potential replacement.
        """        
        html_content = self.html_editor.toPlainText()
        # Regex to find Jinja template code
        matches = re.findall(r"\{\{.*?\}\}", html_content)
        # Clear previous results
        while self.scroll_area_layout.count():
            layout_item = self.scroll_area_layout.takeAt(0)  # Take the first item from the layout
            if layout_item.widget():
                layout_item.widget().deleteLater()  # If it's a widget, delete it
            elif layout_item.layout():
                # If it's a layout, recursively delete all items in this layout
                while layout_item.layout().count():
                    child_item = layout_item.layout().takeAt(0)
                    if child_item.widget():
                        child_item.widget().deleteLater()
                    elif child_item.layout():
                        self.clear_layout(child_item.layout())  # Recursively clear nested layouts
                layout_item.layout().deleteLater()  # Finally, delete the empty layout
        self.matches_and_line_edits.clear()  # Clear previous matches and line edits
        # Create UI for each match
        for match in matches:
            self.add_match_ui(match)

    def add_match_ui(self, match):
        """
        Adds a user interface for a found match, allowing for its replacement.

        :param match: The matched string from the HTML content.
        """        
        layout = QHBoxLayout()
        label = QLabel(match)
        line_edit = QLineEdit()
        replace_button = QPushButton("Replace")
        replace_button.clicked.connect(lambda checked, m=match, le=line_edit: self.replace_match(m, le.text()))

        layout.addWidget(label)
        layout.addWidget(line_edit)
        layout.addWidget(replace_button)

        self.scroll_area_layout.addLayout(layout)
        self.matches_and_line_edits.append((match, line_edit))  # Store the match and its line edit

    def replace_match(self, match, replacement):
        """
        Replaces a single match in the HTML content with a user-provided replacement.

        :param match: The original matched string.
        :param replacement: The replacement string.
        """        
        current_html = self.html_editor.toPlainText()
        updated_html = current_html.replace(match, replacement, 1)
        self.html_editor.setPlainText(updated_html)

    def replace_all_matches(self):
        """
        Replaces all matches in the HTML content with their corresponding user-provided replacements.
        """        
        current_html = self.html_editor.toPlainText()
        for match, line_edit in self.matches_and_line_edits:
            replacement = line_edit.text()
            current_html = current_html.replace(match, replacement)
        self.html_editor.setPlainText(current_html)
        
    def update_editor(self, editor):
        """
        Updates the reference to the HTML editor.

        :param editor: A new QTextEdit instance for editing HTML content.
        """        
        self.html_editor = editor