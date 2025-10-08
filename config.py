# -*- coding: utf-8 -*-
# config.py (Versão com suporte à tela do Editor)

import json
import os
import weakref

# --- CAMINHOS E VARIÁVEIS GLOBAIS ---
ADDON_PATH = os.path.dirname(__file__)
CONFIG_DECK_PATH = os.path.join(ADDON_PATH, "config_deck.json")
CONFIG_ADD_PATH = os.path.join(ADDON_PATH, "config_add.json")
CONFIG_EXT_PATH = os.path.join(ADDON_PATH, "config_ext.json")
CONFIG_OPTION_PATH = os.path.join(ADDON_PATH, "config_option.json")
CONFIG_REVIEW_PATH = os.path.join(ADDON_PATH, "config_review.json")
CONFIG_BROWSER_PATH = os.path.join(ADDON_PATH, "config_browser.json")
CONFIG_EDITOR_PATH = os.path.join(ADDON_PATH, "config_editor.json") # NOVO CAMINHO
CONFIG_SHARED_PATH = os.path.join(ADDON_PATH, "config_shared.json")

active_webviews = weakref.WeakSet()

# --- FUNÇÕES DE CONFIGURAÇÃO COMPARTILHADA (IDIOMA) ---
def load_shared_config():
    try:
        with open(CONFIG_SHARED_PATH, "r", encoding="utf-8") as f: return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError): return {"lang": "pt"}

def save_shared_config(data):
    try:
        with open(CONFIG_SHARED_PATH, "w", encoding="utf-8") as f: json.dump(data, f, indent=4)
    except Exception as e: print(f"[Ankifant] Erro ao salvar config compartilhada: {e}")

# --- FUNÇÕES DE CONFIGURAÇÃO DE POSIÇÃO ---
# ... (funções existentes para deck, add, ext, option, review, browser) ...
def load_deck_config():
    try:
        with open(CONFIG_DECK_PATH, "r", encoding="utf-8") as f: return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError): return {"pos": {"x": 800, "y": 150}, "visible": True}

def save_deck_config(data):
    try:
        with open(CONFIG_DECK_PATH, "w", encoding="utf-8") as f: json.dump(data, f, indent=4)
    except Exception as e: print(f"[Ankifant] Erro ao salvar config do Deck Browser: {e}")

def load_add_config():
    try:
        with open(CONFIG_ADD_PATH, "r", encoding="utf-8") as f: return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError): return {"pos": {"x": 800, "y": 150}, "visible": True}

def save_add_config(data):
    try:
        with open(CONFIG_ADD_PATH, "w", encoding="utf-8") as f: json.dump(data, f, indent=4)
    except Exception as e: print(f"[Ankifant] Erro ao salvar config de Adicionar: {e}")

def load_ext_config():
    try:
        with open(CONFIG_EXT_PATH, "r", encoding="utf-8") as f: return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError): return {"pos": {"x": 100, "y": 100}, "visible": True}

def save_ext_config(data):
    try:
        with open(CONFIG_EXT_PATH, "w", encoding="utf-8") as f: json.dump(data, f, indent=4)
    except Exception as e: print(f"[Ankifant] Erro ao salvar config de Extensões: {e}")

def load_option_config():
    try:
        with open(CONFIG_OPTION_PATH, "r", encoding="utf-8") as f: return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError): return {"pos": {"x": 100, "y": 100}, "visible": True}

def save_option_config(data):
    try:
        with open(CONFIG_OPTION_PATH, "w", encoding="utf-8") as f: json.dump(data, f, indent=4)
    except Exception as e: print(f"[Ankifant] Erro ao salvar config de Opções: {e}")

def load_review_config():
    try:
        with open(CONFIG_REVIEW_PATH, "r", encoding="utf-8") as f: return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError): return {"pos": {"x": 20, "y": 150}, "visible": True}

def save_review_config(data):
    try:
        with open(CONFIG_REVIEW_PATH, "w", encoding="utf-8") as f: json.dump(data, f, indent=4)
    except Exception as e: print(f"[Ankifant] Erro ao salvar config de Revisão: {e}")

def load_browser_config():
    try:
        with open(CONFIG_BROWSER_PATH, "r", encoding="utf-8") as f: return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError): return {"pos": {"x": 50, "y": 100}, "visible": True}

def save_browser_config(data):
    try:
        with open(CONFIG_BROWSER_PATH, "w", encoding="utf-8") as f: json.dump(data, f, indent=4)
    except Exception as e: print(f"[Ankifant] Erro ao salvar config do Navegador: {e}")

# --- NOVAS FUNÇÕES PARA A JANELA DO EDITOR ---
def load_editor_config():
    try:
        with open(CONFIG_EDITOR_PATH, "r", encoding="utf-8") as f: return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError): return {"pos": {"x": 20, "y": 150}, "visible": True}

def save_editor_config(data):
    try:
        with open(CONFIG_EDITOR_PATH, "w", encoding="utf-8") as f: json.dump(data, f, indent=4)
    except Exception as e: print(f"[Ankifant] Erro ao salvar config do Editor: {e}")

# --- FUNÇÃO DE SINCRONIZAÇÃO ---
def broadcast_language_change(lang):
    js_command = f"if (typeof setLanguageExternal === 'function') setLanguageExternal('{lang}');"
    for webview in active_webviews:
        try:
            if hasattr(webview, 'page'): webview.page().runJavaScript(js_command)
            else: webview.eval(js_command)
        except Exception as e: print(f"[Ankifant] Erro ao transmitir mudança de idioma: {e}")