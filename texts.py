# -*- coding: utf-8 -*-
# texts.py (Versão com link do SuperMemo)

TEXTS = {
    'pt': {
        # --- TEXTOS PARA A TELA PRINCIPAL (DECK BROWSER) ---
        "deck_browser_initial_message": """<p style="margin: 2px 0;">Olá, eu sou o Ankifant.</p><p style="margin: 2px 0;">Clique em mim para mais opções.</p><p style="margin: 2px 0;">Pressione <b>Ctrl+X</b> para me ocultar.</p>""",
        "menu_create_card": "➕ Criar Cartão",
        "deck_browser_create_card_content": "Abre a janela de adição de novos cartões.",
        "menu_create_deck": "📚 Criar Baralho",
        "deck_browser_create_deck_content": "Cria um novo baralho em sua coleção. Você pode colocar um baralho dentro do outro, apenas arrastando-o para cima do baralho principal. Eles são chamados de sub-baralhos (subdecks).",
        "menu_login": "🔒 Fazer Login",
        "deck_browser_login_content": """<b>1. Crie uma conta:</b> Você precisa ter uma conta gratuita no AnkiWeb. Cadastre-se pelo link:<br><a href='https://ankiweb.net/account/signup' style='color: #8ab4f8;'>https://ankiweb.net/account/signup</a><br><br><b>2. Sincronize:</b> Se já tiver uma conta, clique no botão 'Sincronizar' na tela principal do Anki e insira seu login e senha do AnkiWeb. Se precisar logar no site, use o link:<br><a href='https://ankiweb.net/account/login' style='color: #8ab4f8;'>https://ankiweb.net/account/login</a>""",
        "menu_share_deck": "🔗 Compartilhar Baralho",
        "deck_browser_share_deck_content": """<b>Opção 1: Compartilhar online via AnkiWeb</b><br>Acesse sua lista de baralhos no site:<br><a href='https://ankiweb.net/decks' style='color: #8ab4f8;'>https://ankiweb.net/decks</a><br>Clique em 'Actions' ao lado do baralho e depois em 'Share'. Siga as instruções para obter um link compartilhável.<br><br><b>Opção 2: Exportar como arquivo</b><br>Passe o mouse sobre o baralho, clique na engrenagem ⚙️ e escolha 'Exportar'. Lembre-se de selecionar o formato <b>.apkg</b>.<br><br><b>Para importar:</b> Se você baixou um arquivo .apkg, basta arrastá-lo e soltá-lo nesta tela principal do Anki.""",
        "menu_install_addon": "🧩 Instalar Addon",
        "deck_browser_install_addon_content": "1- Para colocar um addon, vá até a página de addons e copie o código do addon:<br><a href='https://ankiweb.net/shared/addons' style='color: #8ab4f8;'>https://ankiweb.net/shared/addons</a><br>2- Depois clique no menu Ferramentas > Extensões > Obter extensões, cole o código lá e clique em OK.<br>3- Espere baixar o addon, feche o Anki e abra novamente.",
        "menu_deck_options": "⚙️ Opções do Baralho",
        "deck_browser_deck_options_content": """Para acessar as opções, passe o mouse sobre um baralho para revelar o ícone de engrenagem ⚙️. Clique nele e depois em 'Opções'.<br><br>Lá você pode:<br>• Definir quantos cards novos quer ver por dia em 'Limites Diários'.<br>• Habilitar o <b>FSRS</b>, um algoritmo de repetição mais moderno e eficiente.<br>• Ajustar a 'Retenção desejada' (geralmente entre 0.85 e 0.95).<br>• Clicar em 'Otimizar' sempre que fizer ajustes no FSRS.""",
        "menu_close": "❌ Fechar Menu",

        # --- TEXTOS PARA A JANELA DE ADICIONAR (ADD WINDOW) ---
        "add_menu_tips": "💡 Dicas para bons cards",
        "add_card_tips_title": "Dicas para Bons Cards",
        "add_card_tips_content": "<b>1. Seja simples:</b> Um fato por card.<br><b>2. Use imagens:</b> Uma imagem vale mais que mil palavras.<br><b>3. Crie seus próprios cards:</b> O processo de criação ajuda a memorizar.<br><b>4. Use Cloze Deletion:</b> Para ocultar partes de uma frase.<br><br>Para mais dicas, leia as <a href='https://www.supermemo.com/en/articles/20rules' style='color: #8ab4f8;'>20 regras do SuperMemo</a>.",
        
        # --- TEXTOS PARA A JANELA DO EDITOR (BROWSER/REVIEW) ---
        "editor_menu_fields": "📝 Gerenciar Campos",
        "editor_fields_management": "Clique no botão 'Campos...' para adicionar, remover ou renomear os campos do seu tipo de nota (ex: 'Frente', 'Verso', 'Exemplo').",
        "editor_menu_cards": "🃏 Gerenciar Modelos de Cards",
        "editor_cards_management": "Clique no botão 'Cartões...' para customizar a aparência dos seus cards usando HTML e CSS.",
        "editor_menu_note_type": "📑 Gerenciar Tipos de Nota",
        "editor_note_type_management": "Clique no botão com o nome do tipo de nota (ex: 'Básico') para escolher um tipo de nota diferente ou para gerenciá-los.",

        # --- TEXTOS PARA A JANELA DE REVISÃO ---
        "undo_option": "↩️ Desfazer",
        "filtered_deck_option": "🔍 Deck Filtrado",
        "back_to_decks_option": "📚 Voltar aos Baralhos",
        "shortcuts_option": "⌨️ Atalhos",
        "more_options_option": "⚙️ Mais Opções",
        "undo_alert": "Esta ação volta para o card anterior que você acabou de revisar.<br>Para fazer isso rapidamente, use o atalho <b>Ctrl+Z</b> ou a tecla <b>U</b>.",
        "filtered_deck_alert": "Para criar um Deck Filtrado, aperte a tecla <b>F</b>.<br>Dê um nome, remova o texto 'is:due' do campo 'Procurar'.<br>Desmarque a opção 'Reagendar cartões' e clique em 'Criar'.<br>Isso permite que você revise o mesmo baralho várias vezes no mesmo dia sem afetar o agendamento original.",
        "back_to_decks_alert": "Para voltar à tela principal, clique em 'Baralhos' no topo da janela.<br>Ou simplesmente aperte a tecla <b>D</b>.",
        "shortcuts_alert": "<b>Atalhos Comuns:</b><br><b>Enter/Espaço:</b> Mostrar resposta / Responder 'Bom'<br><b>1:</b> Responder 'Errei'<br><b>2:</b> Responder 'Difícil'<br><b>3:</b> Responder 'Bom'<br><b>4:</b> Responder 'Fácil'<br><b>Ctrl+Z:</b> Desfazer",
        "more_options_alert": "Clique no botão 'Mais' no canto inferior direito da tela.<br>Lá você encontrará outras opções para o card atual, como:<br>• Adicionar bandeiras (marcadores)<br>• Ocultar a nota<br>• Suspender o card.",

        # --- TEXTOS PARA O NAVEGADOR (BROWSER) ---
        "browser_menu_info": "ℹ️ Sobre o Navegador",
        "browser_info_alert": "O Navegador é uma ferramenta poderosa para gerenciar seus cartões. Você pode buscar, editar em massa, marcar, suspender e muito mais.<br><br><b>Dica:</b> Clique com o <b>botão direito</b> sobre um ou mais cartões para ver um menu com todas as opções disponíveis.",

        # --- TEXTOS PARA A JANELA DE EXTENSÕES (ADD-ONS) ---
        "addons_menu_info": "ℹ️ Sobre esta Janela",
        "addons_info_alert": "Esta janela permite que você instale, configure, ative ou desative extensões (add-ons) para personalizar sua experiência no Anki.<br><br>Use o botão 'Obter extensões...' para adicionar novas funcionalidades usando um código.",

        # --- TEXTOS PARA A JANELA DE OPÇÕES DO BARALHO ---
        "options_menu_info": "ℹ️ Sobre as Opções",
        "options_info_alert": "Esta janela permite customizar o comportamento de um grupo de opções. As mudanças aqui afetam todos os baralhos que usam este grupo.<br><br><b>Dica:</b> Use a aba 'Repetição' para configurar o FSRS e a 'Limites Diários' para controlar o número de cards novos e de revisão por dia."
    },
    'en': {
        # --- TEXTS FOR THE DECK BROWSER ---
        "deck_browser_initial_message": """<p style="margin: 2px 0;">Hi, I'm Ankifant.</p><p style="margin: 2px 0;">Click me for more options.</p><p style="margin: 2px 0;">Press <b>Ctrl+X</b> to hide me.</p>""",
        "menu_create_card": "➕ Create Card",
        "deck_browser_create_card_content": "Opens the window to add new cards.",
        "menu_create_deck": "📚 Create Deck",
        "deck_browser_create_deck_content": "Creates a new deck in your collection. You can place a deck inside another by dragging it onto the main deck. These are called sub-decks.",
        "menu_login": "🔒 Log In",
        "deck_browser_login_content": """<b>1. Create an account:</b> You need a free AnkiWeb account. Sign up at:<br><a href='https://ankiweb.net/account/signup' style='color: #8ab4f8;'>https://ankiweb.net/account/signup</a><br><br><b>2. Sync:</b> If you already have an account, click the 'Sync' button on Anki's main screen and enter your AnkiWeb ID and password. To log in to the website, use this link:<br><a href='https://ankiweb.net/account/login' style='color: #8ab4f8;'>https://ankiweb.net/account/login</a>""",
        "menu_share_deck": "🔗 Share Deck",
        "deck_browser_share_deck_content": """<b>Option 1: Share online via AnkiWeb</b><br>Access your deck list on the website:<br><a href='https://ankiweb.net/decks' style='color: #8ab4f8;'>https://ankiweb.net/decks</a><br>Click 'Actions' next to the deck, then 'Share'. Follow the instructions to get a shareable link.<br><br><b>Option 2: Export as a file</b><br>Hover over the deck, click the gear icon ⚙️, and choose 'Export'. Remember to select the <b>.apkg</b> format.<br><br><b>To import:</b> If you have downloaded an .apkg file, just drag and drop it onto this main Anki screen.""",
        "menu_install_addon": "🧩 Install Add-on",
        "deck_browser_install_addon_content": "1- To install an add-on, go to the add-ons page and copy the add-on's code:<br><a href='https://ankiweb.net/shared/addons' style='color: #8ab4f8;'>https://ankiweb.net/shared/addons</a><br>2- Then click on the Tools > Add-ons > Get Add-ons... menu, paste the code, and click OK.<br>3- Wait for the add-on to download, then close and reopen Anki.",
        "menu_deck_options": "⚙️ Deck Options",
        "deck_browser_deck_options_content": """To access the options, hover over a deck to reveal the gear icon ⚙️. Click it, and then select 'Options'.<br><br>There you can:<br>• Set how many new cards you want to see per day under 'Daily Limits'.<br>• Enable <b>FSRS</b>, a more modern and efficient repetition algorithm.<br>• Adjust the 'Desired retention' (usually between 0.85 and 0.95).<br>• Click 'Optimize' whenever you make adjustments to FSRS.""",
        "menu_close": "❌ Close Menu",

        # --- TEXTS FOR THE ADD WINDOW ---
        "add_menu_tips": "💡 Tips for good cards",
        "add_card_tips_title": "Tips for Good Cards",
        "add_card_tips_content": "<b>1. Keep it simple:</b> One fact per card.<br><b>2. Use images:</b> A picture is worth a thousand words.<br><b>3. Make your own cards:</b> The creation process helps you remember.<br><b>4. Use Cloze Deletion:</b> To hide parts of a sentence.<br><br>For more tips, read the <a href='https://www.supermemo.com/en/articles/20rules' style='color: #8ab4f8;'>20 rules from SuperMemo</a>.",

        # --- TEXTS FOR THE EDITOR WINDOW (BROWSER/REVIEW) ---
        "editor_menu_fields": "📝 Manage Fields",
        "editor_fields_management": "Click the 'Fields...' button to add, remove, or rename the fields of your note type (e.g., 'Front', 'Back', 'Example').",
        "editor_menu_cards": "🃏 Manage Card Templates",
        "editor_cards_management": "Click the 'Cards...' button to customize the appearance of your cards using HTML and CSS.",
        "editor_menu_note_type": "📑 Manage Note Types",
        "editor_note_type_management": "Click the button with the note type's name (e.g., 'Basic') to choose a different note type or to manage them.",

        # --- TEXTS FOR THE REVIEW WINDOW ---
        "undo_option": "↩️ Undo",
        "filtered_deck_option": "🔍 Filtered Deck",
        "back_to_decks_option": "📚 Back to Decks",
        "shortcuts_option": "⌨️ Shortcuts",
        "more_options_option": "⚙️ More Options",
        "undo_alert": "This action goes back to the previous card you just reviewed.<br>To do this quickly, use the shortcut <b>Ctrl+Z</b> or the <b>U</b> key.",
        "filtered_deck_alert": "To create a Filtered Deck, press the <b>F</b> key.<br>Give it a name, remove the 'is:due' text from the 'Search' field.<br>Uncheck the 'Reschedule cards' option, and click 'Build'.<br>This allows you to review the same deck multiple times in one day without affecting its original schedule.",
        "back_to_decks_alert": "To return to the main screen, click 'Decks' at the top of the window.<br>Or simply press the <b>D</b> key.",
        "shortcuts_alert": "<b>Common Shortcuts:</b><br><b>Enter/Space:</b> Show Answer / Answer 'Good'<br><b>1:</b> Answer 'Again'<br><b>2:</b> Answer 'Hard'<br><b>3:</b> Answer 'Good'<br><b>4:</b> Answer 'Easy'<br><b>Ctrl+Z:</b> Undo",
        "more_options_alert": "Click the 'More' button in the bottom right corner of the screen.<br>There you will find other options for the current card, such as:<br>• Adding flags (markers)<br>• Burying the note<br>• Suspending the card.",

        # --- TEXTS FOR THE BROWSER ---
        "browser_menu_info": "ℹ️ About the Browser",
        "browser_info_alert": "The Browser is a powerful tool for managing your cards. You can search, bulk edit, flag, suspend, and much more.<br><br><b>Tip:</b> <b>Right-click</b> on one or more cards to see a menu with all available options.",

        # --- TEXTS FOR THE ADD-ONS WINDOW ---
        "addons_menu_info": "ℹ️ About this Window",
        "addons_info_alert": "This window allows you to install, configure, enable, or disable add-ons to customize your Anki experience.<br><br>Use the 'Get Add-ons...' button to add new features using a code.",

        # --- TEXTS FOR THE DECK OPTIONS WINDOW ---
        "options_menu_info": "ℹ️ About Options",
        "options_info_alert": "This window allows you to customize the behavior of an options group. Changes here will affect all decks that use this group.<br><br><b>Tip:</b> Use the 'Repetition' tab to configure FSRS and the 'Daily Limits' tab to control the number of new and review cards per day."
    }
}