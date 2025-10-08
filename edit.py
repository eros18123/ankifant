# -*- coding: utf-8 -*-
# edit.py (Versão com atalho Ctrl+X corrigido)

import json
import os
import base64
from aqt import mw
from aqt.editor import Editor
from aqt.addcards import AddCards

from . import config
from .texts import TEXTS

def injetar_ankifant_no_editor(editor: Editor):
    if not editor or not editor.web:
        return

    config.active_webviews.add(editor.web)

    texts_json = json.dumps(TEXTS)
    pos_config_data = config.load_editor_config()
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
        image_uris["br"] = image_to_base64("br.jpg", "jpeg")
        image_uris["us"] = image_to_base64("us.jpg", "jpeg")
    except Exception as e:
        print(f"[Ankifant] ERRO AO LER IMAGENS (Editor): {e}")
        return
    image_uris_json = json.dumps(image_uris)

    js_script = f"""
    (function() {{
        if (document.getElementById('ankifant-container-editor')) return;

        const texts = {texts_json};
        const imageURIs = {image_uris_json};
        let config = {config_json};
        let currentLang = config.lang || 'pt';
        let menuOpen = false;

        function saveConfig() {{
            pycmd('ankifant_save_editor_config:' + JSON.stringify({{pos: config.pos, visible: config.visible}}));
        }}

        function setLanguageExternal(lang) {{
            currentLang = lang;
            brFlag.style.borderColor = lang === 'pt' ? '#8ab4f8' : 'transparent';
            usFlag.style.borderColor = lang === 'en' ? '#8ab4f8' : 'transparent';
            if (menuOpen) {{
                const oldMenu = document.getElementById('ankifant-menu-editor');
                if (oldMenu) oldMenu.remove();
                const newMenu = createMenu();
                container.appendChild(newMenu);
            }}
        }}

        function setLanguage(lang) {{
            setLanguageExternal(lang);
            config.lang = lang;
            pycmd('ankifant_save_lang:' + lang);
        }}

        const container = document.createElement('div');
        container.id = 'ankifant-container-editor';
        container.style.cssText = `
            position: fixed; left: ${{config.pos.x}}px; top: ${{config.pos.y}}px; 
            z-index: 10000; cursor: grab; display: ${{config.visible ? 'flex' : 'none'}};
            flex-direction: column; align-items: center;
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
        brFlag.onclick = (e) => {{ e.stopPropagation(); setLanguage('pt'); }};
        const usFlag = document.createElement('img');
        usFlag.src = imageURIs.us;
        usFlag.style.cssText = 'width: 25px; cursor: pointer; border: 1px solid transparent;';
        usFlag.onclick = (e) => {{ e.stopPropagation(); setLanguage('en'); }};
        flagsContainer.appendChild(brFlag);
        flagsContainer.appendChild(usFlag);
        container.appendChild(ankifantImg);
        container.appendChild(flagsContainer);
        document.body.appendChild(container);

        setLanguageExternal(currentLang);

        let isDragging = false;
        container.onmousedown = function(e) {{
            if (e.target.tagName === 'IMG' && e.target !== ankifantImg) return;
            isDragging = false;
            let clickTimeout = setTimeout(() => {{
                isDragging = true;
                container.style.cursor = 'grabbing';
                let offsetX = e.clientX - container.offsetLeft;
                let offsetY = e.clientY - container.offsetTop;
                document.onmousemove = function(e_move) {{
                    let newX = e_move.clientX - offsetX;
                    let newY = e_move.clientY - offsetY;
                    const minX = 0, minY = 0;
                    const maxX = window.innerWidth - container.offsetWidth;
                    const maxY = window.innerHeight - container.offsetHeight;
                    config.pos.x = Math.max(minX, Math.min(newX, maxX));
                    config.pos.y = Math.max(minY, Math.min(newY, maxY));
                    container.style.left = config.pos.x + 'px';
                    container.style.top = config.pos.y + 'px';
                }};
            }}, 150);

            document.onmouseup = function() {{
                clearTimeout(clickTimeout);
                container.style.cursor = 'grab';
                document.onmousemove = null;
                document.onmouseup = null;
                if (isDragging) {{
                    saveConfig();
                }}
                isDragging = false;
            }};
        }};
        
        ankifantImg.onclick = function() {{
            if (isDragging) return;
            const oldMenu = document.getElementById('ankifant-menu-editor');
            if (oldMenu) {{ oldMenu.remove(); menuOpen = false; return; }}
            menuOpen = true;
            const menu = createMenu();
            container.appendChild(menu);
            setTimeout(() => {{
                document.body.addEventListener('click', () => {{
                    if(document.getElementById('ankifant-menu-editor')) {{
                        document.getElementById('ankifant-menu-editor').remove();
                    }}
                    menuOpen = false;
                }}, {{ once: true }});
            }}, 0);
        }};
        
        function createMenu() {{
            const menu = document.createElement('div');
            menu.id = 'ankifant-menu-editor';
            menu.style.cssText = `position: absolute; top: 110px; left: 50%; transform: translateX(-50%); background: #3a3a3a; border: 1px solid #555; border-radius: 8px; padding: 5px; z-index: 10001; min-width: 220px; box-shadow: 0 4px 10px rgba(0,0,0,0.4);`;
            menu.onclick = (e) => e.stopPropagation();
            
            const menuItems = [
                {{ key: 'editor_menu_fields', contentKey: 'editor_fields_management' }},
                {{ key: 'editor_menu_cards', contentKey: 'editor_cards_management' }},
                {{ key: 'editor_menu_note_type', contentKey: 'editor_note_type_management' }}
            ];

            menuItems.forEach(item => {{
                const menuItem = document.createElement('div');
                menuItem.style.cssText = 'padding: 8px 12px; color: white; cursor: pointer; border-radius: 5px; font-size: 15px;';
                menuItem.onmouseover = () => menuItem.style.backgroundColor = '#555';
                menuItem.onmouseout = () => menuItem.style.backgroundColor = 'transparent';
                menuItem.onclick = (e) => {{ 
                    e.stopPropagation(); 
                    showDialog(texts[currentLang][item.key], `<p>${{texts[currentLang][item.contentKey]}}</p>`);
                    menu.remove(); 
                    menuOpen = false; 
                }};
                menuItem.innerHTML = texts[currentLang][item.key];
                menu.appendChild(menuItem);
            }});
            return menu;
        }}
        
        document.addEventListener('keydown', function(e) {{
            if (e.ctrlKey && e.key.toLowerCase() === 'x') {{
                if (document.activeElement.isContentEditable || ['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {{
                    return;
                }}
                config.visible = !config.visible;
                container.style.display = config.visible ? 'flex' : 'none';
                saveConfig();
            }}
        }});
        
        function showDialog(title, content) {{
            const overlay = document.createElement('div');
            overlay.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.7); z-index: 10010;';
            const dialog = document.createElement('div');
            dialog.style.cssText = 'position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background-color: #424242; color: white; padding: 25px; border-radius: 8px; z-index: 10011; width: 500px; max-width: 90%;';
            dialog.innerHTML = `<h2 style="margin-top: 0; border-bottom: 1px solid #666; padding-bottom: 10px;">${{title}}</h2><div>${{content}}</div>`;
            const okButton = document.createElement('button');
            okButton.textContent = 'OK';
            okButton.style.cssText = 'display: block; margin: 25px auto 0 auto; padding: 8px 25px; border-radius: 5px; border: none; background-color: #007bff; color: white; cursor: pointer; font-size: 16px;';
            okButton.onmouseover = () => okButton.style.backgroundColor = '#0056b3';
            okButton.onmouseout = () => okButton.style.backgroundColor = '#007bff';
            dialog.appendChild(okButton);
            overlay.appendChild(dialog);
            document.body.appendChild(overlay);
            const closeDialog = () => document.body.removeChild(overlay);
            okButton.onclick = closeDialog;
            overlay.onclick = (e) => {{ if (e.target === overlay) closeDialog(); }};
        }}
    }})();
    """
    
    editor.web.eval(js_script)