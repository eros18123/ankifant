# -*- coding: utf-8 -*-
# browser.py (Versão com menu simplificado)

import os
from aqt import mw, gui_hooks
from aqt.qt import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMenu,
                    QMessageBox, QPoint, QCursor, QShortcut, QKeySequence, Qt)
from PyQt6.QtGui import QPixmap, QIcon, QAction

from . import config
from .texts import TEXTS

# Variável global para a instância do widget
ankifant_browser_widget = None

def show_beautiful_dialog(title, content, parent):
    """Cria e exibe uma caixa de diálogo com o estilo customizado do Ankifant."""
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle("Ankifant")
    msg_box.setStyleSheet("""
        QMessageBox { background-color: #3a3a3a; }
        QLabel { color: white; font-size: 16px; }
        QPushButton {
            background-color: #0d6efd; color: white; border: none;
            border-radius: 5px; padding: 10px 30px; font-size: 16px; font-weight: bold;
        }
        QPushButton:hover { background-color: #0b5ed7; }
    """)
    msg_box.setTextFormat(Qt.TextFormat.RichText)
    msg_box.setText(f"<h2 style='color: white; border-bottom: 1px solid #666; padding-bottom: 10px;'>{title}</h2><div>{content}</div>")
    msg_box.addButton("OK", QMessageBox.ButtonRole.AcceptRole)
    msg_box.exec()

def injetar_ankifant_no_browser(browser):
    """Injeta o Ankifant como um widget Qt nativo e confinado na janela do Navegador."""
    global ankifant_browser_widget

    if ankifant_browser_widget:
        try:
            ankifant_browser_widget.deleteLater()
        except RuntimeError:
            pass
    
    ankifant_browser_widget = QWidget(browser)
    widget = ankifant_browser_widget

    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    widget.setStyleSheet("background: transparent;")

    browser_conf = config.load_browser_config()
    
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    addon_path = os.path.dirname(__file__)
    user_files_path = os.path.join(addon_path, "user_files")
    
    image_label = QLabel()
    pixmap = QPixmap(os.path.join(user_files_path, "ankidireita.png"))
    image_label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
    layout.addWidget(image_label)

    flags_container = QWidget()
    flags_layout = QHBoxLayout(flags_container)
    flags_layout.setContentsMargins(0, 5, 0, 0)
    flags_layout.setSpacing(5)
    flags_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    pt_button = QPushButton()
    us_button = QPushButton()

    for btn, flag_file in [(pt_button, "br.jpg"), (us_button, "us.jpg")]:
        icon = QIcon(os.path.join(user_files_path, flag_file))
        btn.setIcon(icon)
        btn.setIconSize(icon.pixmap(25, 25).size())
        btn.setFixedSize(30, 30)
        btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn.setStyleSheet("background-color: transparent; border-radius: 15px;")

    flags_layout.addWidget(pt_button)
    flags_layout.addWidget(us_button)
    layout.addWidget(flags_container)
    
    widget.setFixedSize(120, 140)
    widget.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def update_flag_styles():
        lang = config.load_shared_config().get("lang", "pt")
        base_style = "background-color: transparent; border-radius: 15px;"
        border_style = "border: 2px solid #8ab4f8;"
        no_border_style = "border: 2px solid transparent;"
        
        pt_button.setStyleSheet(base_style + (border_style if lang == "pt" else no_border_style))
        us_button.setStyleSheet(base_style + (border_style if lang == "en" else no_border_style))

    update_flag_styles()

    def set_language(lang):
        shared_conf = config.load_shared_config()
        if shared_conf.get("lang") == lang: return
        
        shared_conf["lang"] = lang
        config.save_shared_config(shared_conf)
        update_flag_styles()
        
        config.broadcast_language_change(lang)
        injetar_ankifant_no_browser(browser)

    pt_button.clicked.connect(lambda: set_language("pt"))
    us_button.clicked.connect(lambda: set_language("en"))

    def show_menu(pos):
        menu = QMenu(widget)
        menu.setStyleSheet("QMenu { background-color: #3a3a3a; color: white; border: 1px solid #555; } QMenu::item:selected { background-color: #555; }")
        texts = TEXTS[config.load_shared_config().get("lang", "pt")]
        
        # Itens de menu removidos conforme solicitado
        
        action_info = QAction(texts["browser_menu_info"], widget)
        action_info.triggered.connect(lambda: show_beautiful_dialog(texts["browser_menu_info"], texts["browser_info_alert"], browser))
        menu.addAction(action_info)
        
        menu.exec(widget.mapToGlobal(pos))

    widget._dragging = False
    widget._drag_start_pos = QPoint()

    def mousePressEvent(event):
        widget._drag_start_pos = event.pos()
        widget._dragging = False

    def mouseMoveEvent(event):
        if not (event.buttons() & Qt.MouseButton.LeftButton): return
        if (event.pos() - widget._drag_start_pos).manhattanLength() < 10: return

        widget._dragging = True
        new_pos = widget.mapToParent(event.pos() - widget._drag_start_pos)
        
        parent_rect = browser.rect()
        max_y = parent_rect.height() - widget.height()
        max_x = parent_rect.width() - widget.width()

        try:
            if browser.editor and browser.editor.widget and browser.editor.widget.isVisible():
                editor_pos_in_browser = browser.editor.widget.mapTo(browser, QPoint(0, 0))
                editor_x_pos = editor_pos_in_browser.x()
                
                if editor_x_pos > 0:
                    max_x = editor_x_pos - widget.width() - 5
        except Exception:
            pass

        constrained_x = max(0, min(new_pos.x(), max_x))
        constrained_y = max(0, min(new_pos.y(), max_y))
        
        widget.move(constrained_x, constrained_y)

    def mouseReleaseEvent(event):
        if widget._dragging:
            browser_conf["pos"] = {"x": widget.pos().x(), "y": widget.pos().y()}
            config.save_browser_config(browser_conf)
        else:
            if image_label.geometry().contains(event.pos()):
                show_menu(event.pos())
        
        widget._dragging = False

    widget.mousePressEvent = mousePressEvent
    widget.mouseMoveEvent = mouseMoveEvent
    widget.mouseReleaseEvent = mouseReleaseEvent

    def toggle_visibility():
        is_visible = not widget.isVisible()
        widget.setVisible(is_visible)
        browser_conf["visible"] = is_visible
        config.save_browser_config(browser_conf)

    shortcut = QShortcut(QKeySequence("Ctrl+X"), browser)
    shortcut.setContext(Qt.ShortcutContext.WindowShortcut)
    shortcut.activated.connect(toggle_visibility)
    
    def cleanup():
        global ankifant_browser_widget
        try:
            shortcut.activated.disconnect()
        except (TypeError, RuntimeError):
            pass
        ankifant_browser_widget = None
        
    browser.destroyed.connect(cleanup)

    pos = browser_conf.get("pos", {"x": 50, "y": 100})
    widget.move(pos["x"], pos["y"])
    
    if browser_conf.get("visible", True):
        widget.show()
    
    widget.raise_()