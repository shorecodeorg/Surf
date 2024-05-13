#kevin fink
#kevin@shorecode.org
#May 13 24 06:40:48 PM +07 2024
#test_surf_extensions.py

import unittest
from PySide6.QtWidgets import (QApplication, QStyledItemDelegate, QTextEdit, 
            QStyleOptionViewItem)
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
from PySide6.QtCore import QSize, QRegularExpression
from surf_extensions import CustomDelegate, HtmlCssJsHighlighter  # Adjust the import based on your project structure

app = QApplication([])  # Create an application object for the test environment

class TestHtmlCssJsHighlighter(unittest.TestCase):
    def setUp(self):
        """Set up a QTextEdit widget to test the highlighter."""
        self.editor = QTextEdit()
        self.highlighter = HtmlCssJsHighlighter(self.editor.document())

    def test_highlighting_rules(self):
        """Test that highlighting rules are applied correctly."""
        test_string = '<html>var x = 5;</html> // comment'
        self.editor.setPlainText(test_string)
        # Check to make sure highlight rules are loaded
        self.assertNotEqual(len(self.highlighter.highlightingRules), 0, "Highlighting rules should be defined.")

# MORE TESTS NEEDED!