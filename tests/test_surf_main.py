#kevin fink
#kevin@shorecode.org
#May 13 24 06:40:48 PM +07 2024
#test_surf_main.py

from surf_main import Editor
import pytest


# ALL TESTS BROKEN< NEEDS WORK!

def test_update_extensions_calls_update_methods(mocker):
    editor = Editor()
    mocker.patch.object(editor, 'update_flask_compat')
    mocker.patch.object(editor, 'update_js_sandbox')
    mocker.patch.object(editor, 'update_skeleton')
    mocker.patch.object(editor, 'update_find_replace')
    mocker.patch.object(editor, 'update_browsers')
    mocker.patch.object(editor, 'update_console')
    mocker.patch.object(editor, 'open_files', {'file_name': 'content'})
    mocker.patch.object(editor, 'editorWidget', create=True)
    editor.editorWidget.tabText.return_value = 'file_name'

    editor.update_extensions(0)

    editor.update_flask_compat.assert_called_once_with(0)
    editor.update_js_sandbox.assert_called_once_with(0)
    editor.update_skeleton.assert_called_once_with(0)
    editor.update_find_replace.assert_called_once_with(0)
    editor.update_browsers.assert_called_once_with('content')
    editor.update_console.assert_called_once()

def test_update_extensions_handles_exceptions(mocker, capsys):
    editor = Editor()
    mocker.patch.object(editor, 'open_files', {})
    mocker.patch.object(editor, 'editorWidget', create=True)
    editor.editorWidget.tabText.return_value = 'nonexistent_file'

    editor.update_extensions(0)

    captured = capsys.readouterr()
    assert "KeyError" in captured.out
    
def test_flask_compat_initializes_widget(mocker):
    editor = Editor()
    flask_compat_widget_mock = mocker.patch('your_module.FlaskCompatWidget')
    add_tab_mock = mocker.patch.object(editor.splitWidget, 'addTab')
    mocker.patch.object(editor, 'editorWidget', create=True)
    editor.editorWidget.currentIndex.return_value = 0
    mocker.patch.object(editor, 'editor_tabs', ['editor_instance'])

    editor.flask_compat()

    flask_compat_widget_mock.assert_called_once_with('editor_instance')
    add_tab_mock.assert_called_once()

def test_ai_refactor_initializes_widget_and_connects_signal(mocker):
    editor = Editor()
    ai_widget_mock = mocker.patch('your_module.AiWidget', autospec=True)
    add_tab_mock = mocker.patch.object(editor.splitWidget, 'addTab')

    editor.ai_refactor()

    ai_widget_mock.assert_called_once_with('refactor')
    assert ai_widget_mock.return_value.query_button.clicked.connect.call_count == 1
    add_tab_mock.assert_called_once_with(ai_widget_mock.return_value, 'AI Refactor')