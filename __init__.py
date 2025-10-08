# -*- coding: utf-8 -*-
# __init__.py (Versão com menu de posição inteligente aprimorado)

import json
import os
import base64
from aqt import mw, gui_hooks
from aqt.editor import Editor
from aqt.utils import showInfo 
from aqt.addcards import AddCards
from .texts import TEXTS
from . import add
from . import config
from . import ext 
from . import option
from . import review
from . import browser
from . import edit

# --- MANIPULADOR DE MENSAGENS JS ---
def on_js_message(handled, message, context):
    if message.startswith("ankifant_save_lang:"):
        try:
            lang = message.split(":", 1)[1]
            shared_conf = config.load_shared_config()
            if shared_conf.get('lang') != lang:
                shared_conf['lang'] = lang
                config.save_shared_config(shared_conf)
                config.broadcast_language_change(lang)
                mw.progress.timer(50, mw.reset, False)
        except Exception as e:
            print(f"[Ankifant] Erro ao processar mudança de idioma: {e}")
        return (True, None)

    if message.startswith("ankifant_save_deck_config:"):
        try:
            config_data = json.loads(message.split(":", 1)[1])
            config.save_deck_config(config_data)
        except Exception as e:
            print(f"[Ankifant] Erro ao salvar config do deck: {e}")
        return (True, None)

    if message.startswith("ankifant_save_add_config:"):
        try:
            config_data = json.loads(message.split(":", 1)[1])
            config.save_add_config(config_data)
        except Exception as e:
            print(f"[Ankifant] Erro ao salvar config de add: {e}")
        return (True, None)

    if message.startswith("ankifant_save_editor_config:"):
        try:
            config_data = json.loads(message.split(":", 1)[1])
            config.save_editor_config(config_data)
        except Exception as e:
            print(f"[Ankifant] Erro ao salvar config do editor: {e}")
        return (True, None)

    return handled

# --- FUNÇÃO PARA INJETAR NA TELA PRINCIPAL ---
def injetar_ankifant_no_deck_browser(deck_browser):
    if not deck_browser or not hasattr(deck_browser, "web") or not deck_browser.web:
        return

    editor_web = deck_browser.web
    if editor_web not in config.active_webviews:
        config.active_webviews.add(editor_web)

    texts_json = json.dumps(TEXTS)
    pos_config_data = config.load_deck_config()
    shared_config_data = config.load_shared_config()
    full_config = {**pos_config_data, **shared_config_data}
    config_json = json.dumps(full_config)

    image_uris = {}
    try:
        user_files_path = os.path.join(config.ADDON_PATH, "user_files")
        def image_to_base64(filename, file_extension):
            path = os.path.join(user_files_path, filename)
            with open(path, "rb") as image_file:
                encoded = base64.b64encode(image_file.read()).decode('utf-8')
                return f"data:image/{file_extension};base64,{encoded}"
        
        image_uris["ankidireita"] = image_to_base64("ankidireita.png", "png")
        image_uris["ankicima"] = image_to_base64("ankicima.png", "png")
        image_uris["ankibaixo"] = image_to_base64("ankibaixo.png", "png")
        image_uris["br"] = image_to_base64("br.jpg", "jpeg")
        image_uris["us"] = image_to_base64("us.jpg", "jpeg")

    except Exception as e:
        print(f"[Ankifant] ERRO CRÍTICO AO LER IMAGENS: {e}")
        return
    image_uris_json = json.dumps(image_uris)

    js_template = """
    (function() {
        if (document.getElementById('ankifant-container-deck')) {
            document.getElementById('ankifant-container-deck').remove();
        }
        
        const texts = __TEXTS_JSON__;
        const imageURIs = __IMAGE_URIS_JSON__;
        let config = __CONFIG_JSON__;
        let currentLang = config.lang || 'pt';
        let menuOpen = false;

        function saveConfig() {
            pycmd('ankifant_save_deck_config:' + JSON.stringify({pos: config.pos, visible: config.visible}));
        }

        function setLanguageExternal(lang) {
            currentLang = lang;
            brFlag.style.borderColor = lang === 'pt' ? '#8ab4f8' : 'transparent';
            usFlag.style.borderColor = lang === 'en' ? '#8ab4f8' : 'transparent';
            
            const tooltip = document.getElementById('ankifant-tooltip-deck');
            if (tooltip) {
                tooltip.innerHTML = texts[currentLang].deck_browser_initial_message;
            }

            if (menuOpen) {
                const oldMenu = document.getElementById('ankifant-menu-deck');
                if (oldMenu) oldMenu.remove();
                const newMenu = createMenu();
                container.appendChild(newMenu);
            }
        }

        function setLanguage(lang) {
            setLanguageExternal(lang);
            config.lang = lang;
            pycmd('ankifant_save_lang:' + lang);
        }

        const container = document.createElement('div');
        container.id = 'ankifant-container-deck';
        container.style.cssText = `
            position: fixed; left: ${config.pos.x}px; top: ${config.pos.y}px; 
            z-index: 10000; display: ${config.visible ? 'flex' : 'none'};
            flex-direction: column; align-items: center; cursor: grab;
            transition: top 0.8s ease-in-out, left 0.8s ease-in-out;
        `;

        const ankifantImg = document.createElement('img');
        ankifantImg.src = imageURIs.ankidireita;
        ankifantImg.style.width = '100px';
        ankifantImg.style.userSelect = 'none';
        ankifantImg.addEventListener('dragstart', (e) => e.preventDefault());

        const flagsContainer = document.createElement('div');
        flagsContainer.style.marginTop = '5px';
        const brFlag = document.createElement('img');
        brFlag.src = imageURIs.br;
        brFlag.style.cssText = 'width: 25px; cursor: pointer; margin-right: 5px; border: 1px solid transparent;';
        brFlag.onclick = (e) => { e.stopPropagation(); setLanguage('pt'); };
        const usFlag = document.createElement('img');
        usFlag.src = imageURIs.us;
        usFlag.style.cssText = 'width: 25px; cursor: pointer; border: 1px solid transparent;';
        usFlag.onclick = (e) => { e.stopPropagation(); setLanguage('en'); };
        
        flagsContainer.appendChild(brFlag);
        flagsContainer.appendChild(usFlag);
        container.appendChild(ankifantImg);
        container.appendChild(flagsContainer);
        
        const tooltip = document.createElement('div');
        tooltip.id = 'ankifant-tooltip-deck';
        tooltip.style.cssText = `
            position: absolute; left: 110px; top: 10px;
            background-color: #3a3a3a; color: white;
            padding: 10px 15px; border-radius: 8px; border: 1px solid #555;
            z-index: 9999; width: 250px; box-shadow: 0 3px 8px rgba(0,0,0,0.5);
            font-size: 14px; line-height: 1.5;
            display: none; opacity: 0;
            transition: opacity 0.3s ease;
            pointer-events: none;
        `;
        tooltip.innerHTML = texts[currentLang].deck_browser_initial_message;
        container.appendChild(tooltip);

        document.body.appendChild(container);

        setLanguageExternal(currentLang);

        function showTooltip() {
            tooltip.style.display = 'block';
            setTimeout(() => { tooltip.style.opacity = '1'; }, 10);
        }

        function hideTooltip() {
            tooltip.style.opacity = '0';
            setTimeout(() => { tooltip.style.display = 'none'; }, 300);
        }

        container.addEventListener('mouseenter', showTooltip);
        container.addEventListener('mouseleave', hideTooltip);

        function pointTo(direction) {
            let newX, newY;
            const centerX = (window.innerWidth / 2) - (container.offsetWidth / 2);

            if (direction === 'top') { 
                ankifantImg.src = imageURIs.ankicima; 
                newX = centerX - 150; 
                newY = 20; 
            } else if (direction === 'bottom') { 
                ankifantImg.src = imageURIs.ankibaixo; 
                newX = centerX; 
                newY = window.innerHeight - container.offsetHeight - 20; 
            } else if (direction === 'sync') {
                ankifantImg.src = imageURIs.ankicima;
                newX = centerX + 150; // Movido para a direita do centro
                newY = 20;
            } else if (direction === 'tools') {
                ankifantImg.src = imageURIs.ankicima;
                newX = 80;
                newY = 20;
            } else { 
                return; 
            }
            
            const minX = 0, minY = 0;
            const maxX = window.innerWidth - container.offsetWidth;
            const maxY = window.innerHeight - container.offsetHeight;
            const finalX = Math.max(minX, Math.min(newX, maxX));
            const finalY = Math.max(minY, Math.min(newY, maxY));

            container.style.left = finalX + 'px'; 
            container.style.top = finalY + 'px';
            config.pos.x = finalX; 
            config.pos.y = finalY;
            saveConfig();
        }
        
        let isDragging = false;
        container.onmousedown = function(e) {
            if (e.target.tagName === 'IMG' && e.target !== ankifantImg) return;
            isDragging = false;
            container.style.transition = 'none';
            
            let clickTimeout = setTimeout(() => {
                isDragging = true;
                container.style.cursor = 'grabbing';
                ankifantImg.src = imageURIs.ankidireita;
                let offsetX = e.clientX - container.offsetLeft;
                let offsetY = e.clientY - container.offsetTop;
                document.onmousemove = function(e_move) {
                    let newX = e_move.clientX - offsetX;
                    let newY = e_move.clientY - offsetY;
                    const minX = 0, minY = 0;
                    const maxX = window.innerWidth - container.offsetWidth;
                    const maxY = window.innerHeight - container.offsetHeight;
                    config.pos.x = Math.max(minX, Math.min(newX, maxX));
                    config.pos.y = Math.max(minY, Math.min(newY, maxY));
                    container.style.left = config.pos.x + 'px';
                    container.style.top = config.pos.y + 'px';
                };
            }, 150);

            document.onmouseup = function() {
                clearTimeout(clickTimeout);
                container.style.cursor = 'grab';
                container.style.transition = 'top 0.8s ease-in-out, left 0.8s ease-in-out';
                document.onmousemove = null;
                document.onmouseup = null;
                if (isDragging) {
                    saveConfig();
                }
                isDragging = false;
            };
        };
        
        ankifantImg.onclick = function() {
            if (isDragging) return;
            const oldMenu = document.getElementById('ankifant-menu-deck');
            if (oldMenu) { oldMenu.remove(); menuOpen = false; return; }
            menuOpen = true;
            const menu = createMenu();
            container.appendChild(menu);
            setTimeout(() => {
                document.body.addEventListener('click', () => {
                    if(document.getElementById('ankifant-menu-deck')) {
                        document.getElementById('ankifant-menu-deck').remove();
                        menuOpen = false;
                    }
                }, { once: true });
            }, 0);
        };
        
        function createMenu() {
            const menu = document.createElement('div');
            menu.id = 'ankifant-menu-deck';
            
            const menuMinWidth = 220;
            const menuMinHeight = 220; // Altura estimada do menu

            const isTooFarRight = (container.offsetLeft + container.offsetWidth / 2 + menuMinWidth) > window.innerWidth;
            const isTooFarBottom = (container.offsetTop + 110 + menuMinHeight) > window.innerHeight;

            let cssText = `
                position: absolute; background: #3a3a3a; border: 1px solid #555; 
                border-radius: 8px; padding: 5px; z-index: 10001; min-width: ${menuMinWidth}px; 
                box-shadow: 0 4px 10px rgba(0,0,0,0.4); cursor: default;
            `;

            if (isTooFarBottom) {
                // Prioridade 1: Se estiver muito embaixo, o menu abre para CIMA.
                cssText += `bottom: 110px; left: 50%; transform: translateX(-50%);`;
            } else if (isTooFarRight) {
                // Prioridade 2: Se estiver muito à direita (e não muito embaixo), o menu abre para a ESQUERDA.
                cssText += `top: 10px; right: 110px; transform: none;`;
            } else {
                // Padrão: O menu abre para BAIXO, centralizado.
                cssText += `top: 110px; left: 50%; transform: translateX(-50%);`;
            }
            
            menu.style.cssText = cssText;
            menu.onclick = (e) => e.stopPropagation();
            const closeMenu = () => { menu.remove(); menuOpen = false; };
            const menuItems = [
                { textKey: 'menu_create_card', contentKey: 'deck_browser_create_card_content', pointDirection: 'top' },
                { textKey: 'menu_create_deck', contentKey: 'deck_browser_create_deck_content', pointDirection: 'bottom' },
                { textKey: 'menu_login', contentKey: 'deck_browser_login_content', pointDirection: 'sync' },
                { textKey: 'menu_share_deck', contentKey: 'deck_browser_share_deck_content' },
                { textKey: 'menu_install_addon', contentKey: 'deck_browser_install_addon_content', pointDirection: 'tools' },
                { textKey: 'menu_deck_options', contentKey: 'deck_browser_deck_options_content' },
                { key: 'separator' }, { textKey: 'menu_close', action: closeMenu }
            ];
            menuItems.forEach(item => {
                if (item.key === 'separator') { const separator = document.createElement('hr'); separator.style.cssText = 'border: none; border-top: 1px solid #555; margin: 4px 0;'; menu.appendChild(separator); return; }
                const menuItem = document.createElement('div');
                menuItem.style.cssText = 'padding: 8px 12px; color: white; cursor: pointer; border-radius: 5px; font-size: 15px;';
                menuItem.onmouseover = () => menuItem.style.backgroundColor = '#555';
                menuItem.onmouseout = () => menuItem.style.backgroundColor = 'transparent';
                
                if (item.action) {
                    menuItem.onclick = (e) => { e.stopPropagation(); item.action(); };
                } else {
                    menuItem.onclick = (e) => {
                        e.stopPropagation();
                        closeMenu();
                        showDialog(texts[currentLang][item.textKey], `<p>${texts[currentLang][item.contentKey]}</p>`);
                        if (item.pointDirection) {
                            pointTo(item.pointDirection);
                        }
                    };
                }
                
                menuItem.innerHTML = texts[currentLang][item.textKey];
                menu.appendChild(menuItem);
            });
            return menu;
        }
        
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key.toLowerCase() === 'x') {
                config.visible = !config.visible;
                container.style.display = config.visible ? 'flex' : 'none';
                saveConfig();
            }
        });
        
        function showDialog(title, content) {
            const overlay = document.createElement('div');
            overlay.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.75); z-index: 20000;';
            const dialog = document.createElement('div');
            dialog.style.cssText = 'position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background-color: #3a3a3a; color: white; padding: 25px; border-radius: 10px; z-index: 20001; width: 550px; max-width: 95%; border: 1px solid #555; box-shadow: 0 5px 20px rgba(0,0,0,0.5);';
            dialog.innerHTML = `<h2 style="margin-top: 0; border-bottom: 1px solid #666; padding-bottom: 10px; font-size: 1.2em;">${title}</h2><div style="font-size: 1.05em; line-height: 1.6;">${content}</div>`;
            const okButton = document.createElement('button');
            okButton.textContent = 'OK';
            okButton.style.cssText = 'display: block; margin: 25px auto 0 auto; padding: 10px 30px; border-radius: 5px; border: none; background-color: #0d6efd; color: white; cursor: pointer; font-size: 16px; font-weight: bold;';
            okButton.onmouseover = () => okButton.style.backgroundColor = '#0b5ed7';
            okButton.onmouseout = () => okButton.style.backgroundColor = '#0d6efd';
            dialog.appendChild(okButton);
            overlay.appendChild(dialog);
            document.body.appendChild(overlay);
            const closeDialog = () => document.body.removeChild(overlay);
            okButton.onclick = closeDialog;
            overlay.onclick = (e) => { if (e.target === overlay) closeDialog(); };
        }
    })();
    """

    # Injeta os dados nos placeholders
    js_script = js_template.replace("__TEXTS_JSON__", texts_json)
    js_script = js_script.replace("__IMAGE_URIS_JSON__", image_uris_json)
    js_script = js_script.replace("__CONFIG_JSON__", config_json)

    editor_web.eval(js_script)

# --- HOOKS (GATILHOS DO ANKI) ---
gui_hooks.deck_browser_did_render.append(injetar_ankifant_no_deck_browser)
gui_hooks.webview_did_receive_js_message.append(on_js_message)
gui_hooks.addons_dialog_will_show.append(ext.injetar_ankifant_nos_addons)
gui_hooks.deck_options_did_load.append(option.injetar_ankifant_nas_opcoes)
gui_hooks.reviewer_did_show_question.append(review.injetar_ankifant_no_revisor)
gui_hooks.browser_will_show.append(browser.injetar_ankifant_no_browser)
gui_hooks.add_cards_did_init.append(add.injetar_ankifant_no_addcards)

def on_editor_did_init(editor: Editor):
    if isinstance(editor.parentWindow, AddCards):
        return
    edit.injetar_ankifant_no_editor(editor)

gui_hooks.editor_did_init.append(on_editor_did_init)

print("[Ankifant] Carregado com sucesso em todas as telas.")