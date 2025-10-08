# -*- coding: utf-8 -*-
# option.py (Versão com menu corrigido e contextual)

import os
from aqt import mw
from aqt.qt import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMenu,
                    QMessageBox, QPoint, QCursor, QShortcut, QKeySequence, Qt)
from PyQt6.QtGui import QPixmap, QIcon, QAction

from . import config
from .texts import TEXTS

# Variável global para a instância do widget
ankifant_options_widget = None

def show_beautiful_dialog(title, content, parent):
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

def injetar_ankifant_nas_opcoes(options_dialog):
    global ankifant_options_widget

    if ankifant_options_widget:
        try:
            ankifant_options_widget.deleteLater()
        except RuntimeError:
            pass
    
    ankifant_options_widget = QWidget(options_dialog)
    widget = ankifant_options_widget

    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    widget.setStyleSheet("background: transparent;")

    opt_conf = config.load_option_config()
    
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
        mw.progress.timer(50, mw.reset, False)

    pt_button.clicked.connect(lambda: set_language("pt"))
    us_button.clicked.connect(lambda: set_language("en"))

    def show_menu(pos):
        menu = QMenu(widget)
        menu.setStyleSheet("QMenu { background-color: #3a3a3a; color: white; border: 1px solid #555; } QMenu::item:selected { background-color: #555; }")
        texts = TEXTS[config.load_shared_config().get("lang", "pt")]
        
        # Menu corrigido para usar chaves de texto dedicadas
        info_action = QAction(texts["options_menu_info"], widget)
        info_action.triggered.connect(lambda: show_beautiful_dialog(
            texts["options_menu_info"], 
            texts["options_info_alert"], 
            options_dialog
        ))
        menu.addAction(info_action)
        
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
        
        parent_rect = options_dialog.rect()
        max_x = parent_rect.width() - widget.width()
        max_y = parent_rect.height() - widget.height()
        
        constrained_x = max(0, min(new_pos.x(), max_x))
        constrained_y = max(0, min(new_pos.y(), max_y))
        
        widget.move(constrained_x, constrained_y)

    def mouseReleaseEvent(event):
        if widget._dragging:
            opt_conf["pos"] = {"x": widget.pos().x(), "y": widget.pos().y()}
            config.save_option_config(opt_conf)
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
        opt_conf["visible"] = is_visible
        config.save_option_config(opt_conf)

    shortcut = QShortcut(QKeySequence("Ctrl+X"), options_dialog)
    shortcut.activated.connect(toggle_visibility)
    
    def cleanup():
        global ankifant_options_widget
        try:
            shortcut.activated.disconnect()
        except (TypeError, RuntimeError):
            pass
        ankifant_options_widget = None
    options_dialog.finished.connect(cleanup)

    pos = opt_conf.get("pos", {"x": 100, "y": 100})
    widget.move(pos["x"], pos["y"])
    
    if opt_conf.get("visible", True):
        widget.show()
    
    widget.raise_()