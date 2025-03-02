import time
import language_tool_python
from pynput import keyboard
from pynput.keyboard import Key, Controller
import pyperclip

controller = Controller()

tool = language_tool_python.LanguageTool('es')  # Cargar herramienta para español

def fix_text(text):
    matches = tool.check(text)
    corrected_text = text
    for match in reversed(matches):  # Recorremos los "matches" en orden inverso
        start, end = match.offset, match.offset + match.errorLength
        corrected_text = corrected_text[:start] + match.replacements[0] + corrected_text[end:]
    return corrected_text

def fix_current_line():
    # Windows shortcut to select current line: Ctrl+Shift+Left
    controller.press(Key.ctrl)
    controller.press(Key.shift)
    controller.press(Key.left)

    controller.release(Key.ctrl)
    controller.release(Key.shift)
    controller.release(Key.left)

    fix_selection()

def fix_selection():
    # 1. Copy selection to clipboard
    with controller.pressed(Key.ctrl):
        controller.tap("c")

    # 2. Get the clipboard string
    time.sleep(0.1)
    text = pyperclip.paste()

    # 3. Fix string
    if not text:
        return
    fixed_text = fix_text(text)
    if not fixed_text:
        return

    # 4. Paste the fixed string to the clipboard
    pyperclip.copy(fixed_text)
    time.sleep(0.1)

    # 5. Paste the clipboard and replace the selected text
    with controller.pressed(Key.ctrl):
        controller.tap("v")

def on_f9():
    fix_current_line()

def on_f10():
    fix_selection()

def on_escape(key):
    if key == Key.esc:
        return False  # Returns False to stop the listener

def for_canonical(f):
    return lambda k: f(l.canonical(k))

with keyboard.GlobalHotKeys({"<f9>": on_f9, "<f10>": on_f10}) as h:
    with keyboard.Listener(on_press=for_canonical(on_escape)) as l:
        h.join()
        l.stop()
