import streamlit as st
import time
import json
import os

# ========== НАСТРОЙКИ ВРЕМЕНИ ЭТАПОВ ==========
TIME_LIMITS = {
    "choose_resources": 180,      # 3 минуты на закупку ресурсов
    "choose_available": 120,      # 2 минуты на выбор доступных оперативников
    "choose_protection": 300,     # 5 минут на выбор защиты
    "choose_bans": 300,           # 5 минут на выбор банов
    "choose_picks": 600,          # 10 минут на выбор пиков
}
# ========== БАЗА ДАННЫХ ПЕРСОНАЖЕЙ ==========
# 6⭐ Оперативники (ID 1-300)
# 5⭐ Оперативники (ID 301-600)
# 4⭐ Оперативники (ID 601-900)

CHARACTERS_DB = {
    # ========== 6⭐ герои (ID 1-300) ==========
    1: {
        "name": "Эндминистратор", 
        "rarity": "6⭐", 
        "full_name": "Эндминистратор (6⭐)",
        "image_path": "heroes_images/Эндминистратор.png"
    },
    2: {
        "name": "Арделия", 
        "rarity": "6⭐", 
        "full_name": "Арделия (6⭐)",
        "image_path": "heroes_images/Арделия.png"
    },
    3: {
        "name": "Лифэн", 
        "rarity": "6⭐", 
        "full_name": "Лифэн (6⭐)",
        "image_path": "heroes_images/Лифэн.png"
    },
    4: {
        "name": "Пограничник", 
        "rarity": "6⭐", 
        "full_name": "Пограничник (6⭐)",
        "image_path": "heroes_images/Пограничник.png"
    },
    5: {
        "name": "Панихида", 
        "rarity": "6⭐", 
        "full_name": "Панихида (6⭐)",
        "image_path": "heroes_images/Панихида.png"
    },
    6: {
        "name": "Эмбер", 
        "rarity": "6⭐", 
        "full_name": "Эмбер (6⭐)",
        "image_path": "heroes_images/Эмбер.png"
    },
    7: {
        "name": "Лэватейн", 
        "rarity": "6⭐", 
        "full_name": "Лэватейн (6⭐)",
        "image_path": "heroes_images/Лэватейн.png"
    },
    8: {
        "name": "Гилберта", 
        "rarity": "6⭐", 
        "full_name": "Гилберта (6⭐)",
        "image_path": "heroes_images/Гилберта.png"
    },
    9: {
        "name": "Ивонна", 
        "rarity": "6⭐", 
        "full_name": "Ивонна (6⭐)",
        "image_path": "heroes_images/Ивонна.png"
    },
    10: {
        "name": "Тантан", 
        "rarity": "6⭐", 
        "full_name": "Тантан (6⭐)",
        "image_path": "heroes_images/Тантан.png"
    },
    11: {
        "name": "Росси", 
        "rarity": "6⭐", 
        "full_name": "Росси (6⭐)",
        "image_path": "heroes_images/Росси.png"
    },
    12: {
        "name": "Чжуан Фанъи", 
        "rarity": "6⭐", 
        "full_name": "Чжуан Фанъи (6⭐)",
        "image_path": "heroes_images/Чжуан Фанъи.png"
    },
    
    # ========== 5⭐ герои (ID 301-600) ==========
    301: {
        "name": "Авивенна", 
        "rarity": "5⭐", 
        "full_name": "Авивенна (5⭐)",
        "image_path": "heroes_images/Авивенна.png"
    },
    302: {
        "name": "Арклайт", 
        "rarity": "5⭐", 
        "full_name": "Арклайт (5⭐)",
        "image_path": "heroes_images/Арклайт.png"
    },
    303: {
        "name": "Перлика", 
        "rarity": "5⭐", 
        "full_name": "Перлика (5⭐)",
        "image_path": "heroes_images/Перлика.png"
    },
    304: {
        "name": "Чэнь Цяньюй", 
        "rarity": "5⭐", 
        "full_name": "Чэнь Цяньюй (5⭐)",
        "image_path": "heroes_images/Чэнь Цяньюй.png"
    },
    305: {
        "name": "Сайхи", 
        "rarity": "5⭐", 
        "full_name": "Сайхи (5⭐)",
        "image_path": "heroes_images/Сайхи.png"
    },
    306: {
        "name": "Да Пан", 
        "rarity": "5⭐", 
        "full_name": "Да Пан (5⭐)",
        "image_path": "heroes_images/Да Пан.png"
    },
    307: {
        "name": "Вулфгард", 
        "rarity": "5⭐", 
        "full_name": "Вулфгард (5⭐)",
        "image_path": "heroes_images/Вулфгард.png"
    },
    308: {
        "name": "Алеш", 
        "rarity": "5⭐", 
        "full_name": "Алеш (5⭐)",
        "image_path": "heroes_images/Алеш.png"
    },
    309: {
        "name": "Светоснежка", 
        "rarity": "5⭐", 
        "full_name": "Светоснежка (5⭐)",
        "image_path": "heroes_images/Светоснежка.png"
    },
    
    # ========== 4⭐ герои (ID 601-900) ==========
    601: {
        "name": "Акэкури", 
        "rarity": "4⭐", 
        "full_name": "Акэкури (4⭐)",
        "image_path": "heroes_images/Акэкури.png"
    },
    602: {
        "name": "Антал", 
        "rarity": "4⭐", 
        "full_name": "Антал (4⭐)",
        "image_path": "heroes_images/Антал.png"
    },
    603: {
        "name": "Флюорит", 
        "rarity": "4⭐", 
        "full_name": "Флюорит (4⭐)",
        "image_path": "heroes_images/Флюорит.png"
    },
    604: {
        "name": "Эстелла", 
        "rarity": "4⭐", 
        "full_name": "Эстелла (4⭐)",
        "image_path": "heroes_images/Эстелла.png"
    },
    605: {
        "name": "Кэтчер", 
        "rarity": "4⭐", 
        "full_name": "Кэтчер (4⭐)",
        "image_path": "heroes_images/Кэтчер.png"
    },
}




# Обратные отображения
ID_TO_CHAR = CHARACTERS_DB
CHAR_TO_ID = {v["full_name"]: k for k, v in CHARACTERS_DB.items()}
NAME_TO_ID = {v["name"]: k for k, v in CHARACTERS_DB.items()}
ID_TO_NAME = {k: v["name"] for k, v in CHARACTERS_DB.items()}
ID_TO_RARITY = {k: v["rarity"] for k, v in CHARACTERS_DB.items()}
ID_TO_FULL_NAME = {k: v["full_name"] for k, v in CHARACTERS_DB.items()}
ID_TO_IMAGE_PATH = {k: v["image_path"] for k, v in CHARACTERS_DB.items()}


# ========== БАЗА ДАННЫХ РЕСУРСОВ ==========
RESOURCES_DB = {
    "🛡️ Универсальная защита": {
        "cost": 7,
        "effect": "Выдерживает одно попадание Бана",
        "max": 99,
        "description": "Защищает ЛЮБОГО оперативника от одного бана",
        "emoji": "🛡️"
    },
    "🔵 Защита 5⭐": {
        "cost": 2,
        "effect": "Выдерживает одно попадание Бана",
        "max": 99,
        "description": "Защищает оперативника 5⭐ или 4⭐ от одного бана",
        "emoji": "🔵"
    },
    "🔴 Универсальное воскрешение": {
        "cost": 3,
        "effect": "Позволяет использовать оперативника в нескольких пачках",
        "max": 3,
        "description": "Работает на ЛЮБЫХ оперативников (6⭐, 5⭐, 4⭐)",
        "emoji": "🔴"
    },
    "🔵 Воскрешение 5⭐": {
        "cost": 2,
        "effect": "Позволяет использовать 5⭐ и 4⭐ в нескольких пачках",
        "max": 3,
        "description": "Работает только на 5⭐ и 4⭐ оперативников",
        "emoji": "🔵"
    },
    "🔴 Универсальный бан": {
        "cost": 4,
        "effect": "Банит одного оперативника чужого участника",
        "max": 99,
        "description": "Банит ЛЮБОГО оперативника противника",
        "emoji": "🔴"
    },
    "🔵 Бан 4-5⭐": {
        "cost": 3,
        "effect": "Банит оперативника 4-5⭐ чужого участника",
        "max": 2,
        "description": "Банит оперативника 5⭐ или 4⭐ противника",
        "emoji": "🔵"
    },
    "🔄 Рестарт": {
        "cost": 1,
        "effect": "Позволяет переиграть комнату",
        "max": 2,
        "description": "Даёт второй шанс на переигровку комнаты",
        "emoji": "🔄"
    }
}

# Константы
STARTING_POINTS = 12
MAX_TOTAL_RESURRECTIONS = 3  # Максимум воскрешений (Универсальное + 5⭐) не более 3
MAX_BAN_4_5 = 2  # Максимум Бана 4-5⭐ не более 2
MAX_RESTART = 2  # Максимум Рестарта не более 2


PLAYER1_FILE = "player1_data.json"
PLAYER2_FILE = "player2_data.json"
JUDGE_FILE = "judge_data.json"

def save_player_data(player_num):
    """Сохраняет данные только своего участника"""
    if player_num == 1:
        data = st.session_state.p1
        with open(PLAYER1_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    else:
        data = st.session_state.p2
        with open(PLAYER2_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)

def load_my_data(player_num):
    """Загружает данные ТОЛЬКО своего участника из своего файла"""
    if player_num == 1:
        if os.path.exists(PLAYER1_FILE):
            try:
                with open(PLAYER1_FILE, "r", encoding="utf-8") as f:
                    st.session_state.p1 = json.load(f)
                return True
            except:
                pass
    else:
        if os.path.exists(PLAYER2_FILE):
            try:
                with open(PLAYER2_FILE, "r", encoding="utf-8") as f:
                    st.session_state.p2 = json.load(f)
                return True
            except:
                pass
    return False

def load_opponent_data(player_num):
    """Загружает данные противника из файла судьи"""
    if os.path.exists(JUDGE_FILE):
        try:
            with open(JUDGE_FILE, "r", encoding="utf-8") as f:
                judge_data = json.load(f)
                
                if player_num == 1:
                    # Участник 1 загружает данные участника 2 из файла судьи
                    st.session_state.p2 = judge_data.get("p2", get_empty_participant_data())
                else:
                    # Участник 2 загружает данные участника 1 из файла судьи
                    st.session_state.p1 = judge_data.get("p1", get_empty_participant_data())
                return True
        except:
            pass
    return False

def save_judge_data():
    """Судья собирает данные обоих участников и сохраняет в свой файл"""
    # Загружаем последние данные участников из их файлов
    if os.path.exists(PLAYER1_FILE):
        try:
            with open(PLAYER1_FILE, "r", encoding="utf-8") as f:
                p1_data = json.load(f)
                st.session_state.p1 = p1_data
        except:
            pass
    
    if os.path.exists(PLAYER2_FILE):
        try:
            with open(PLAYER2_FILE, "r", encoding="utf-8") as f:
                p2_data = json.load(f)
                st.session_state.p2 = p2_data
        except:
            pass
    
    # Сохраняем в файл судьи
    judge_state = {
        "p1": st.session_state.p1,
        "p2": st.session_state.p2
    }
    with open(JUDGE_FILE, "w", encoding="utf-8") as f:
        json.dump(judge_state, f, ensure_ascii=False, indent=2, default=str)
    
    return True

def load_judge_data():
    """Загружает данные из файла судьи (для судьи или для синхронизации)"""
    if os.path.exists(JUDGE_FILE):
        try:
            with open(JUDGE_FILE, "r", encoding="utf-8") as f:
                judge_data = json.load(f)
                st.session_state.p1 = judge_data.get("p1", get_empty_participant_data())
                st.session_state.p2 = judge_data.get("p2", get_empty_participant_data())
                return True
        except:
            pass
    return False
    
    st.success("📁 Данные участников и выбранные комнаты сохранены в judge_data.json!")
    time.sleep(1)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
OPERATORS_DIR = os.path.join(CURRENT_DIR, "Operators")

def load_operator_image(operator_name):
    """Загрузка изображения оперативника из папки Operators"""
    
    # Имя файла
    filename = f"{operator_name}.png"
    
    # Полный путь к файлу
    image_path = os.path.join(OPERATORS_DIR, filename)
    
    # Проверяем существование файла
    if os.path.exists(image_path):
        return image_path
    
    # Если не нашли, пробуем без учета регистра (для Windows)
    try:
        if os.path.exists(OPERATORS_DIR):
            for file in os.listdir(OPERATORS_DIR):
                if file.lower() == filename.lower():
                    return os.path.join(OPERATORS_DIR, file)
    except:
        pass
    
    return None


def ensure_operators_folder():
    """Проверяет существование папки Operators"""
    if not os.path.exists(OPERATORS_DIR):
        os.makedirs(OPERATORS_DIR)
        st.warning(f"📁 Создана папка 'Operators' по пути: {OPERATORS_DIR}")
        st.info("Пожалуйста, добавьте изображения оперативников в формате PNG")
        return False
    
    # Проверяем, есть ли файлы в папке
    files = [f for f in os.listdir(OPERATORS_DIR) if f.endswith('.png')]
    if not files:
        st.info(f"📁 Папка Operators существует, но в ней нет PNG файлов")
        st.code(f"Путь: {OPERATORS_DIR}")
        return False
    
    return True

#def ensure_operators_folder():
    #"""Проверяет существование папки Operators и создает файл-заглушку"""
   # if not os.path.exists("Operators"):
       # os.makedirs("Operators")
        #st.warning("📁 Создана папка 'Operators'. Пожалуйста, добавьте изображения оперативников в формате PNG.")
    
    # Создаем заглушку default.png если её нет
    #if not os.path.exists("Operators/default.png"):
       # st.info("🖼️ Для отображения изображений добавьте файлы в папку 'Operators'") 

def get_empty_participant_data():
    """Создаёт пустые данные для нового участника"""
    return {
        "nickname": "",
        "ready": False,
        "points": STARTING_POINTS,
        "resources": {r: 0 for r in RESOURCES_DB},
        "available_heroes": [],
        "protected_heroes": [],
        "bans": {},
        "picks": [[None for _ in range(4)] for _ in range(3)],
        "stage": "resources",
        "finished_resources": False,
        "finished_available": False,
        "finished_protection": False,
        "finished_bans": False,
        "finished_picks": False
    }
def get_selected_rooms():
    """Возвращает список выбранных комнат из файла судьи"""
    if os.path.exists(JUDGE_FILE):
        try:
            with open(JUDGE_FILE, "r", encoding="utf-8") as f:
                judge_data = json.load(f)
                return judge_data.get("selected_rooms", [])
        except:
            pass
    return []

def update_participant_data(player_num, data):
    """Обновляет данные участника в session_state"""
    if player_num == 1:
        st.session_state.p1 = data
    else:
        st.session_state.p2 = data

def force_exit_stage(stage_name, player_num):
    """Принудительное завершение этапа (команда от Судьи)"""
    st.session_state[f"exit_{stage_name}_{player_num}"] = True

def get_next_stage(current_stage):
    """Возвращает следующий этап по порядку"""
    stages = ["resources", "available", "protection", "bans", "picks"]
    if current_stage in stages:
        idx = stages.index(current_stage)
        if idx + 1 < len(stages):
            return stages[idx + 1]
    return "finished"

def get_stage_name(stage_key):
    """Возвращает русское название этапа"""
    stages = {
        "resources": "Закупка ресурсов",
        "available": "Выбор оперативников",
        "protection": "Защита",
        "bans": "Баны",
        "picks": "Пики",
        "finished": "Завершено"
    }
    return stages.get(stage_key, stage_key)

# ========== 3. ИНТЕРФЕЙС УЧАСТНИКА ==========

def participant_interface(player_num):
    """Интерфейс участника"""
    
    # Принудительно загружаем свои данные из файла
    load_my_data(player_num)
    
    if player_num == 1:
        data = st.session_state.p1
        player_key = "player1_2024"
        player_title = "Участник 1"
    else:
        data = st.session_state.p2
        player_key = "player2_2024"
        player_title = "Участник 2"
    
    current_stage = data.get("stage", "resources")
    is_ready = data.get("ready", False)
    nickname = data.get("nickname", "")
    
    # Если участник еще не готов или не ввел ник - показываем простой интерфейс
    if not is_ready or not nickname:
        # Информационная панель сверху
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"## ⚔️ {player_title}")
        with col2:
            st.caption(f"Ключ: `{player_key}`")
        with col3:
            if st.button("🚪 Выйти", key=f"exit_p{player_num}", use_container_width=True):
                if player_num == 1:
                    st.session_state.auth_player1 = False
                else:
                    st.session_state.auth_player2 = False
                st.session_state.current_role = None
                save_player_data(player_num)
                st.rerun()
        
        st.divider()
        
        # Строка 1: Поле для ввода ника
        nickname_input = st.text_input(
            "Ваш никнейм:",
            value=nickname if nickname else "",
            placeholder="Введите ваш никнейм",
            key=f"nickname_{player_num}",
            disabled=is_ready
        )
        
        # Строка 2: Приветствие
        if nickname_input and nickname_input.strip():
            st.success(f"✨ Добро пожаловать на турнир, **{nickname_input.strip()}**! ✨")
            if not is_ready and nickname_input != nickname:
                data["nickname"] = nickname_input.strip()
                if player_num == 1:
                    st.session_state.p1 = data
                else:
                    st.session_state.p2 = data
                save_player_data(player_num)
        elif nickname:
            st.success(f"✨ Добро пожаловать на турнир, **{nickname}**! ✨")
        else:
            st.info("👋 Введите ваш никнейм, чтобы продолжить")
        
        # Строка 3: Кнопка готовности
        if not is_ready:
            if nickname_input and nickname_input.strip():
                if st.button("✅ Я ГОТОВ", key=f"ready_{player_num}", type="primary", use_container_width=True):
                    data["ready"] = True
                    if player_num == 1:
                        st.session_state.p1 = data
                    else:
                        st.session_state.p2 = data
                    save_player_data(player_num)
                    st.success(f"✅ {nickname_input.strip()}, вы готовы! Ожидайте команду от Судьи.")
                    st.rerun()
            else:
                st.button("✅ Я ГОТОВ", key=f"ready_disabled_{player_num}", disabled=True, use_container_width=True)
                st.caption("⚠️ Сначала введите никнейм")
        else:
            st.success("✅ Статус: ГОТОВ")
        
        # Строка 4: Кнопка обновления
        if is_ready:
            if st.button("🔄 Проверить статус", key=f"refresh_p{player_num}_simple", use_container_width=True):
                load_my_data(player_num)
                load_opponent_data(player_num)
                st.success("Статус обновлен!")
                time.sleep(0.5)
                st.rerun()
            
            st.caption("⚠️ **Важно:** Переход на следующий этап возможен только после команды Судьи.")
        
        return
    
    # Если участник готов - показываем интерфейс текущего этапа
    st.markdown(f"## ⚔️ {player_title}")
    st.caption(f"Участник: {nickname}")
    
    # Кнопки управления
    col1, col2, col3 = st.columns([3, 1, 1])
    with col2:
        if st.button("🚪 Выйти", key=f"exit_p{player_num}_main", use_container_width=True):
            if player_num == 1:
                st.session_state.auth_player1 = False
            else:
                st.session_state.auth_player2 = False
            st.session_state.current_role = None
            save_player_data(player_num)
            st.rerun()
    with col3:
        if st.button("🔄 Обновить", key=f"refresh_p{player_num}_main", use_container_width=True):
            load_my_data(player_num)
            load_opponent_data(player_num)
            st.rerun()
    
    st.divider()
    
    # Отображаем текущий этап
    current_stage_name = get_stage_name(current_stage)
    st.info(f"📌 Текущий этап: **{current_stage_name}**")
    
    # Отображение нужного этапа
    if current_stage == "resources":
        if not data.get("finished_resources", False):
            purchase_interface(player_num)
        else:
            st.success("✅ Этап закупки ресурсов завершен!")
            st.info("⏳ Ожидайте команду Судьи для перехода на следующий этап.")
            
            if st.button("🔄 Проверить статус", key=f"check_status_resources_{player_num}"):
                load_my_data(player_num)
                load_opponent_data(player_num)
                st.rerun()
    
    elif current_stage == "available":
        if not data.get("finished_available", False):
            operators_selection_interface(player_num)
        else:
            st.success("✅ Этап выбора оперативников завершен!")
            st.info("⏳ Ожидайте команду Судьи для перехода на следующий этап.")
            
            if st.button("🔄 Проверить статус", key=f"check_status_available_{player_num}"):
                load_my_data(player_num)
                load_opponent_data(player_num)
                st.rerun()
    
    elif current_stage == "protection":
        if not data.get("finished_protection", False):
            protection_interface(player_num)
        else:
            st.success("✅ Этап защиты завершен!")
            st.info("⏳ Ожидайте команду Судьи для перехода на следующий этап.")
            
            if st.button("🔄 Проверить статус", key=f"check_status_protection_{player_num}"):
                load_my_data(player_num)
                load_opponent_data(player_num)
                st.rerun()
    
    elif current_stage == "bans":
        if not data.get("finished_bans", False):
            ban_interface(player_num)
        else:
            st.success("✅ Этап банов завершен!")
            st.info("⏳ Ожидайте команду Судьи для перехода на следующий этап.")
            
            if st.button("🔄 Проверить статус", key=f"check_status_bans_{player_num}"):
                load_my_data(player_num)
                load_opponent_data(player_num)
                st.rerun()
    
    elif current_stage == "picks":
        if not data.get("finished_picks", False):
            picks_interface(player_num)
        else:
            st.success("✅ Этап пиков завершен!")
            st.info("⏳ Ожидайте команду Судьи для перехода в комнату ожидания.")
            
            if st.button("🔄 Проверить статус", key=f"check_status_picks_{player_num}"):
                load_my_data(player_num)
                load_opponent_data(player_num)
                st.rerun()
    
    elif current_stage == "waiting_room":
        waiting_room_interface(player_num)
    
    elif current_stage == "battle":
        st.success("🏆 ПОЗДРАВЛЯЮ! Все этапы пройдены!")
        st.info("⚔️ Ожидайте начала боев от Судьи.")
        
        if st.button("🔄 Проверить статус", key=f"check_status_battle_{player_num}"):
            load_my_data(player_num)
            load_opponent_data(player_num)
            st.rerun()
    
    elif current_stage == "finished":
        st.success("🏆 ПОЗДРАВЛЯЮ! Турнир завершен!")
        st.balloons()

# ========== 4. ИНТЕРФЕЙС ЗАКУПОК ==========

def purchase_interface(player_num):
    """Интерфейс закупки ресурсов"""
    
    if player_num == 1:
        data = st.session_state.p1
    else:
        data = st.session_state.p2
    
    st.markdown("## 🛒 Этап закупки ресурсов")
    st.caption("Используйте ваши 12 очков Увыкоинов для покупки ресурсов")
    
    # Получаем текущие ресурсы
    current_resources = data.get("resources", {})
    points = data.get("points", STARTING_POINTS)
    
    # Отображаем доступные очки
    st.metric("💰 Доступно Увыкоинов", f"{points} / {STARTING_POINTS}")
    
    # Отображаем лимиты
    with st.expander("📋 Правила и ограничения"):
        st.markdown("""
        **Ограничения на покупку:**
        - 🔴 Универсальное воскрешение + 🔵 Воскрешение 5⭐ ≤ 3 (в сумме)
        - 🔵 Бан 4-5⭐ ≤ 2
        - 🔄 Рестарт ≤ 2
        
        **Базовая комплектация (бесплатно):**
        - 🔄 Рестарт x1
        - 🔴 Универсальный бан x1
        """)
    
    # Базовая комплектация (бесплатно)
    st.markdown("### 📦 Базовая комплектация (бесплатно)")
    col1, col2 = st.columns(2)
    with col1:
        st.info("🔄 Рестарт x1 (бесплатно)")
    with col2:
        st.info("🔴 Универсальный бан x1 (бесплатно)")
    
    st.divider()
    
    # Таблица закупки ресурсов
    st.markdown("### 🛍️ Магазин ресурсов")
    
    # Создаем таблицу
    purchases = {}
    total_cost = 0
    
    # Отслеживаем текущие суммы для проверки лимитов
    current_universal_res = current_resources.get("🔴 Универсальное воскрешение", 0)
    current_five_star_res = current_resources.get("🔵 Воскрешение 5⭐", 0)
    current_ban_4_5 = current_resources.get("🔵 Бан 4-5⭐", 0)
    current_restart = current_resources.get("🔄 Рестарт", 0)
    
    for res_name, res_info in RESOURCES_DB.items():
        col1, col2, col3, col4 = st.columns([2, 1, 1.5, 1])
        
        # Текущее количество ресурса
        current_count = current_resources.get(res_name, 0)
        
        # 1-й столбец: название и описание
        with col1:
            st.markdown(f"**{res_info['emoji']} {res_name}**")
            st.caption(res_info['description'])
            st.caption(f"💰 Цена: {res_info['cost']} 💎")
        
        # 2-й столбец: базовая комплектация
        with col2:
            if res_name == "🔄 Рестарт":
                st.write("**1 шт.** (бесплатно)")
                st.caption(f"Макс: {MAX_RESTART}")
            elif res_name == "🔴 Универсальный бан":
                st.write("**1 шт.** (бесплатно)")
                st.caption("Макс: 99")
            elif res_name == "🔴 Универсальное воскрешение":
                st.caption(f"Макс: {MAX_TOTAL_RESURRECTIONS}")
            elif res_name == "🔵 Воскрешение 5⭐":
                st.caption(f"Макс: {MAX_TOTAL_RESURRECTIONS}")
            elif res_name == "🔵 Бан 4-5⭐":
                st.caption(f"Макс: {MAX_BAN_4_5}")
            else:
                st.caption("Макс: 99")
        
        # 3-й столбец: счетчик закупки
        with col3:
            # Рассчитываем максимальное количество для покупки с учетом лимитов
            max_buyable = res_info["max"] - current_count
            
            # Дополнительные проверки по лимитам
            if res_name == "🔴 Универсальное воскрешение":
                remaining_res_limit = MAX_TOTAL_RESURRECTIONS - (current_universal_res + current_five_star_res)
                max_buyable = min(max_buyable, remaining_res_limit)
            elif res_name == "🔵 Воскрешение 5⭐":
                remaining_res_limit = MAX_TOTAL_RESURRECTIONS - (current_universal_res + current_five_star_res)
                max_buyable = min(max_buyable, remaining_res_limit)
            elif res_name == "🔵 Бан 4-5⭐":
                remaining_ban_limit = MAX_BAN_4_5 - current_ban_4_5
                max_buyable = min(max_buyable, remaining_ban_limit)
            elif res_name == "🔄 Рестарт":
                remaining_restart_limit = MAX_RESTART - current_restart
                max_buyable = min(max_buyable, remaining_restart_limit)
            
            # Ограничение по очкам
            max_by_points = points // res_info["cost"]
            max_buyable = min(max_buyable, max_by_points)
            
            if max_buyable < 0:
                max_buyable = 0
            
            quantity = st.number_input(
                f"Количество {res_name}",
                min_value=0,
                max_value=max_buyable,
                value=0,
                step=1,
                key=f"purchase_{res_name}_{player_num}",
                label_visibility="collapsed"
            )
            purchases[res_name] = quantity
        
        # 4-й столбец: стоимость
        with col4:
            cost = quantity * res_info["cost"]
            if cost > 0:
                st.write(f"💰 {cost} 💎")
                total_cost += cost
            else:
                st.write("—")
        
        # Отображаем текущее количество после покупки
        free_items = 0
        if res_name == "🔄 Рестарт":
            free_items = 1
        elif res_name == "🔴 Универсальный бан":
            free_items = 1
        
        total_count = current_count + quantity + free_items
        if total_count > 0:
            if res_name in ["🔴 Универсальное воскрешение", "🔵 Воскрешение 5⭐"]:
                st.caption(f"📦 Всего: {total_count} шт. (макс {MAX_TOTAL_RESURRECTIONS})")
            elif res_name == "🔵 Бан 4-5⭐":
                st.caption(f"📦 Всего: {total_count} шт. (макс {MAX_BAN_4_5})")
            elif res_name == "🔄 Рестарт":
                st.caption(f"📦 Всего: {total_count} шт. (макс {MAX_RESTART})")
            else:
                st.caption(f"📦 Всего: {total_count} шт.")
        
        st.divider()
    
    # Итоговая информация
    st.markdown("### 📊 Итог закупки")
    
    # Рассчитываем итоговые значения для проверки лимитов
    final_universal_res = current_universal_res + purchases.get("🔴 Универсальное воскрешение", 0)
    final_five_star_res = current_five_star_res + purchases.get("🔵 Воскрешение 5⭐", 0)
    final_ban_4_5 = current_ban_4_5 + purchases.get("🔵 Бан 4-5⭐", 0)
    final_restart = current_restart + purchases.get("🔄 Рестарт", 0) + 1
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💎 Итого к оплате", f"{total_cost}")
    
    with col2:
        remaining_points = points - total_cost
        st.metric("💰 Останется Увыкоинов", f"{remaining_points}")
    
    with col3:
        st.metric("🔴+🔵 Воскрешения", f"{final_universal_res + final_five_star_res} / {MAX_TOTAL_RESURRECTIONS}")
        if final_universal_res + final_five_star_res > MAX_TOTAL_RESURRECTIONS:
            st.error("❌ Превышен лимит!")
    
    with col4:
        st.metric("🔵 Бан 4-5⭐", f"{final_ban_4_5} / {MAX_BAN_4_5}")
        if final_ban_4_5 > MAX_BAN_4_5:
            st.error("❌ Превышен лимит!")
    
    # Кнопки действий
    col_button1, col_button2 = st.columns(2)
    
    with col_button1:
        if total_cost > points:
            st.error("❌ Недостаточно Увыкоинов!")
            st.button("✅ Подтвердить закупку", disabled=True, use_container_width=True)
        elif total_cost == 0 and not any(purchases.values()):
            st.warning("⚠️ Вы ничего не купили")
            if st.button("⏭️ Пропустить закупку", key=f"skip_purchase_{player_num}", use_container_width=True):
                # Добавляем базовую комплектацию
                if "🔄 Рестарт" not in current_resources:
                    current_resources["🔄 Рестарт"] = 1
                if "🔴 Универсальный бан" not in current_resources:
                    current_resources["🔴 Универсальный бан"] = 1
                
                data["resources"] = current_resources
                data["finished_resources"] = True
                
                if player_num == 1:
                    st.session_state.p1 = data
                else:
                    st.session_state.p2 = data
                
                save_player_data(player_num)
                st.success("✅ Этап закупки пропущен! Ожидайте Судью.")
                st.rerun()
        else:
            if st.button("✅ Подтвердить закупку", key=f"confirm_purchase_{player_num}", type="primary", use_container_width=True):
                # Финальная проверка лимитов
                if (final_universal_res + final_five_star_res) > MAX_TOTAL_RESURRECTIONS:
                    st.error(f"❌ Сумма воскрешений ({final_universal_res + final_five_star_res}) превышает лимит {MAX_TOTAL_RESURRECTIONS}!")
                elif final_ban_4_5 > MAX_BAN_4_5:
                    st.error(f"❌ Количество банов 4-5⭐ ({final_ban_4_5}) превышает лимит {MAX_BAN_4_5}!")
                elif final_restart > MAX_RESTART:
                    st.error(f"❌ Количество рестартов ({final_restart}) превышает лимит {MAX_RESTART}!")
                else:
                    # Применяем покупки
                    for res_name, quantity in purchases.items():
                        if quantity > 0:
                            current_resources[res_name] = current_resources.get(res_name, 0) + quantity
                    
                    # Добавляем базовую комплектацию
                    current_resources["🔄 Рестарт"] = current_resources.get("🔄 Рестарт", 0) + 1
                    current_resources["🔴 Универсальный бан"] = current_resources.get("🔴 Универсальный бан", 0) + 1
                    
                    data["points"] = remaining_points
                    data["resources"] = current_resources
                    data["finished_resources"] = True
                    
                    if player_num == 1:
                        st.session_state.p1 = data
                    else:
                        st.session_state.p2 = data
                    
                    save_player_data(player_num)
                    st.success("✅ Закупка успешно завершена! Ожидайте Судью.")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
    
    with col_button2:
        if st.button("🔄 Сбросить выбор", key=f"reset_purchase_{player_num}", use_container_width=True):
            st.rerun()


def check_purchase_limits(resources):
    """Проверка ограничений на покупки"""
    # Проверка лимита воскрешений
    universal_res = resources.get("🔴 Универсальное воскрешение", 0)
    five_star_res = resources.get("🔵 Воскрешение 5⭐", 0)
    
    if universal_res + five_star_res > MAX_TOTAL_RESURRECTIONS:
        st.error(f"❌ Сумма воскрешений ({universal_res + five_star_res}) превышает лимит {MAX_TOTAL_RESURRECTIONS}")
        return False
    
    # Проверка лимита банов 4-5⭐
    ban_4_5 = resources.get("🔵 Бан 4-5⭐", 0)
    if ban_4_5 > MAX_BAN_4_5:
        st.error(f"❌ Количество банов 4-5⭐ ({ban_4_5}) превышает лимит {MAX_BAN_4_5}")
        return False
    
    # Проверка лимита рестартов
    restart = resources.get("🔄 Рестарт", 0)
    if restart > MAX_RESTART:
        st.error(f"❌ Количество рестартов ({restart}) превышает лимит {MAX_RESTART}")
        return False
    
    return True

# ========== 5. ИНТЕРФЕЙС РОСТЕРА ==========

def get_modified_character_db_for_player(player_num):
    """Получить модифицированную базу персонажей для конкретного участника"""
    
    load_my_data(player_num)

    if player_num == 1:
        data = st.session_state.p1
    else:
        data = st.session_state.p2
    
    # Если у участника еще нет своей модифицированной базы, создаем копию
    if "modified_character_db" not in data:
        data["modified_character_db"] = {}
    
    # Копируем глобальную базу в модифицированную
    modified_db = data["modified_character_db"]
    
    # Если база пустая, копируем из глобальной
    if not modified_db:
        for char_id, char_info in CHARACTERS_DB.items():
            # Извлекаем имя файла из image_path или используем name
            image_filename = char_info.get("image_path", "")
            if image_filename:
                # Если путь содержит полный путь, извлекаем только имя файла
                image_name = image_filename.split("/")[-1] if "/" in image_filename else image_filename
            else:
                image_name = f"{char_info['name']}.png"
            
            modified_db[char_id] = {
                "name": char_info["name"],
                "rarity": char_info["rarity"],
                "full_name": char_info["full_name"],
                "image_path": f"Operators/{image_name}",  # Путь к изображению в папке Operators
                "has_operator": True,  # ПО УМОЛЧАНИЮ ВСЕ ОПЕРАТИВНИКИ В НАЛИЧИИ
                "level": 90,  # Уровень по умолчанию
                "potential": 0,  # Потенциал по умолчанию
                "is_restricted": False  # Ограничен ли (Увынск)
            }
        
        data["modified_character_db"] = modified_db
        if player_num == 1:
            st.session_state.p1 = data
        else:
            st.session_state.p2 = data
        save_player_data(player_num)
    
    return modified_db


def display_operators_table(character_db, rarity, player_num):
    """Отображает таблицу оперативников определенной редкости"""
    
    # Фильтруем по редкости
    operators = {char_id: info for char_id, info in character_db.items() 
                 if info["rarity"] == rarity}
    
    # Сортируем по имени
    sorted_operators = sorted(operators.items(), key=lambda x: x[1]["name"])
    
    # Создаем заголовки таблицы (6 колонок)
    cols = st.columns([0.8, 1.2, 0.8, 0.8, 0.8, 1.2])
    with cols[0]:
        st.markdown("**Оперативник**")
    with cols[1]:
        st.markdown("**Имя**")
    with cols[2]:
        st.markdown("**Наличие**")
    with cols[3]:
        st.markdown("**Уровень**")
    with cols[4]:
        st.markdown("**Потенциал**")
    with cols[5]:
        st.markdown("**Статус**")
    
    st.divider()
    
    # Отображаем каждого оперативника
    for char_id, char_info in sorted_operators:
        cols = st.columns([0.8, 1.2, 0.8, 0.8, 0.8, 1.2])
        
        # 1-й столбец: фото (152x212, масштабируется по ширине)
        with cols[0]:
            image_path = load_operator_image(char_info['name'])
            if image_path:
                try:
                    # Используем width для контроля размера
                    st.image(image_path, width=60)
                except:
                    st.write("🎴")
            else:
                st.write("🎴")
        
        # 2-й столбец: имя и ранг
        with cols[1]:
            st.markdown(f"**{char_info['name']}**")
            st.caption(char_info["rarity"])
            # Добавляем отступ для выравнивания с фото (опционально)
            st.caption(" ")
        
        # 3-й столбец: чекбокс наличия
        with cols[2]:
            has_operator = st.checkbox(
                "Есть",
                value=char_info["has_operator"],
                key=f"has_{char_id}_{player_num}",
                label_visibility="collapsed"
            )
            char_info["has_operator"] = has_operator
        
        if has_operator:
            # 4-й столбец: уровень (0-90)
            with cols[3]:
                level = st.number_input(
                    "Ур.",
                    min_value=0,
                    max_value=90,
                    value=char_info["level"],
                    step=1,
                    key=f"level_{char_id}_{player_num}",
                    label_visibility="collapsed"
                )
                char_info["level"] = level
            
            # 5-й столбец: потенциал (0-5)
            with cols[4]:
                potential = st.number_input(
                    "Пот.",
                    min_value=0,
                    max_value=5,
                    value=char_info["potential"],
                    step=1,
                    key=f"potential_{char_id}_{player_num}",
                    label_visibility="collapsed"
                )
                char_info["potential"] = potential
            
            # 6-й столбец: статус
            with cols[5]:
                if char_info["rarity"] == "6⭐" and potential >= 3:
                    char_info["is_restricted"] = True
                    st.warning("⚠️ Оперативник будет подвержен УВЫНСКУ!")
                elif char_info["rarity"] == "6⭐":
                    char_info["is_restricted"] = False
                    st.success("✅ Без ограничений")
                else:
                    char_info["is_restricted"] = False
                    st.info("ℹ️ Без ограничений")
        else:
            # Если оперативник не выбран
            char_info["level"] = 90
            char_info["potential"] = 0
            char_info["is_restricted"] = False
        
        st.divider()

def operators_selection_interface(player_num):
    """Интерфейс выбора оперативников - участник отмечает тех, кто есть в аккаунте"""
    
    if player_num == 1:
        data = st.session_state.p1
    else:
        data = st.session_state.p2
    
    st.markdown("## 📋 Выбор оперативников")
    st.caption("Отметьте оперативников, которые есть в вашем распоряжении")
    st.info("💡 По умолчанию все оперативники отмечены как 'В наличии'. Снимите галочку, если оперативника нет в аккаунте.")
    
    # Получаем модифицированную базу для участника
    character_db = get_modified_character_db_for_player(player_num)
    
    # Просто считаем выбранных для информации (без ограничений)
    selected_6star = sum(1 for char in character_db.values() 
                        if char["has_operator"] and char["rarity"] == "6⭐")
    selected_5star = sum(1 for char in character_db.values() 
                        if char["has_operator"] and char["rarity"] == "5⭐")
    selected_4star = sum(1 for char in character_db.values() 
                        if char["has_operator"] and char["rarity"] == "4⭐")
    
    # Отображение статистики (только информативно, без ограничений)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("6⭐ Оперативники в наличии", f"{selected_6star}")
    with col2:
        st.metric("5⭐ Оперативники в наличии", f"{selected_5star}")
    with col3:
        st.metric("4⭐ Оперативники в наличии", f"{selected_4star}")
    
    st.caption("ℹ️ Вы можете отметить любое количество оперативников - это просто список того, что есть в вашем аккаунте.")
    st.divider()
    
    # Создаем вкладки для разных редкостей
    tab1, tab2, tab3 = st.tabs(["⭐ 6⭐ Герои", "⭐⭐ 5⭐ Герои", "⭐⭐⭐ 4⭐ Герои"])
    
    with tab1:
        st.markdown("### 6⭐ Оперативники")
        display_operators_table(character_db, "6⭐", player_num)
    
    with tab2:
        st.markdown("### 5⭐ Оперативники")
        display_operators_table(character_db, "5⭐", player_num)
    
    with tab3:
        st.markdown("### 4⭐ Оперативники")
        display_operators_table(character_db, "4⭐", player_num)
    
    st.divider()
    
    # Кнопка подтверждения (без проверки лимитов)
    col_button1, col_button2 = st.columns([1, 2])
    
    with col_button1:
        if st.button("✅ Подтвердить выбор", key=f"confirm_operators_{player_num}", type="primary", use_container_width=True):
            # Сохраняем выбранных оперативников (всех, у кого стоит галочка)
            selected_heroes = []
            for char_id, char_info in character_db.items():
                if char_info["has_operator"]:
                    selected_heroes.append(char_id)
            
            data["available_heroes"] = selected_heroes
            data["character_db"] = character_db
            data["finished_available"] = True
            
            if player_num == 1:
                st.session_state.p1 = data
            else:
                st.session_state.p2 = data
            
            save_player_data(player_num)
            st.success(f"✅ Отмечено {len(selected_heroes)} оперативников (6⭐: {selected_6star}, 5⭐: {selected_5star}, 4⭐: {selected_4star})!")
            st.balloons()
            time.sleep(1)
            st.rerun()
    
    with col_button2:
        if st.button("🔄 Сбросить всё", key=f"reset_operators_{player_num}", use_container_width=True):
            # Сбрасываем выбор (ставим всем has_operator = True)
            for char_id in character_db:
                character_db[char_id]["has_operator"] = True
                character_db[char_id]["level"] = 90
                character_db[char_id]["potential"] = 0
                character_db[char_id]["is_restricted"] = False
            
            data["character_db"] = character_db
            if player_num == 1:
                st.session_state.p1 = data
            else:
                st.session_state.p2 = data
            save_player_data(player_num)
            st.rerun()

# ========== 5. ИНТЕРФЕЙС ЗАЩИТЫ  ==========

def protection_interface(player_num):
    """Интерфейс защиты оперативников"""
    
    # Загружаем свои данные
    load_my_data(player_num)
    # Загружаем данные противника из файла судьи
    load_opponent_data(player_num)
    
    if player_num == 1:
        data = st.session_state.p1
        opponent_data = st.session_state.p2
    else:
        data = st.session_state.p2
        opponent_data = st.session_state.p1
    
    st.markdown("## 🛡️ Этап защиты оперативников")
    
    # Получаем ресурсы участника
    resources = data.get("resources", {})
    universal_protection_initial = resources.get("🛡️ Универсальная защита", 0)  # Сколько было куплено
    five_star_protection_initial = resources.get("🔵 Защита 5⭐", 0)
    
    # ========== ПОЛНАЯ ИНФОРМАЦИЯ О ЗАКУПКАХ ==========
    st.markdown("### 📊 Полная информация о закупках ресурсов")
    
    all_resources = [
        "🛡️ Универсальная защита",
        "🔵 Защита 5⭐", 
        "🔴 Универсальное воскрешение",
        "🔵 Воскрешение 5⭐",
        "🔴 Универсальный бан",
        "🔵 Бан 4-5⭐",
        "🔄 Рестарт"
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**{data.get('nickname', 'Участник 1')}**")
        st.markdown("**🎁 Бесплатно:** 🔄 Рестарт x1, 🔴 Универсальный бан x1")
        st.markdown("**💰 Куплено:**")
        for res in all_resources:
            count = resources.get(res, 0)
            if res in ["🔄 Рестарт", "🔴 Универсальный бан"]:
                purchased = max(0, count - 1)
                if purchased > 0:
                    st.write(f"{res}: {purchased}")
            else:
                if count > 0:
                    st.write(f"{res}: {count}")
        remaining_points = data.get("points", STARTING_POINTS)
        st.markdown(f"💎 Осталось Увыкоинов: {remaining_points}")
    
    with col2:
        st.markdown(f"**{opponent_data.get('nickname', 'Участник 2')}**")
        st.markdown("**🎁 Бесплатно:** 🔄 Рестарт x1, 🔴 Универсальный бан x1")
        st.markdown("**💰 Куплено:**")
        opponent_resources = opponent_data.get("resources", {})
        for res in all_resources:
            count = opponent_resources.get(res, 0)
            if res in ["🔄 Рестарт", "🔴 Универсальный бан"]:
                purchased = max(0, count - 1)
                if purchased > 0:
                    st.write(f"{res}: {purchased}")
            else:
                if count > 0:
                    st.write(f"{res}: {count}")
        opponent_remaining_points = opponent_data.get("points", STARTING_POINTS)
        st.markdown(f"💎 Осталось Увыкоинов: {opponent_remaining_points}")
    
    st.divider()
    
    # ========== ИНФОРМАЦИЯ О ВЫБРАННЫХ КОМНАТАХ ==========
    selected_rooms = get_selected_rooms()
    if selected_rooms:
        st.markdown("### 🏟️ Информация о турнире")
        st.markdown("**Судья подобрал для вас следующие комнаты:**")
        for idx, room in enumerate(selected_rooms, 1):
            st.markdown(f"**Комната {room}**")
        st.divider()

    # Проверяем, есть ли вообще ресурсы для защиты
    if universal_protection_initial == 0 and five_star_protection_initial == 0:
        st.error("❌ У вас нет ресурсов для защиты оперативников!")
        
        if st.button("✅ Пропустить этап защиты", key=f"skip_protection_{player_num}", type="primary"):
            data["protected_heroes"] = []
            data["finished_protection"] = True
            save_player_data(player_num)
            st.success("Этап защиты пропущен! Ожидайте Судью.")
            st.rerun()
        return
    
    # Получаем список оперативников
    character_db = data.get("character_db", {})
    
    six_star_heroes = []
    other_heroes = []
    
    for char_id, char_info in character_db.items():
        if char_info.get("has_operator", False):
            if char_info["rarity"] == "6⭐":
                six_star_heroes.append((char_id, char_info))
            else:
                other_heroes.append((char_id, char_info))
    
    # Временное хранилище для защит
    if f"protected_temp_{player_num}" not in st.session_state:
        st.session_state[f"protected_temp_{player_num}"] = data.get("protected_heroes", []).copy()
    if f"universal_temp_{player_num}" not in st.session_state:
        st.session_state[f"universal_temp_{player_num}"] = universal_protection_initial
    if f"five_star_temp_{player_num}" not in st.session_state:
        st.session_state[f"five_star_temp_{player_num}"] = five_star_protection_initial
    
    protected_heroes = st.session_state[f"protected_temp_{player_num}"]
    remaining_universal = st.session_state[f"universal_temp_{player_num}"]
    remaining_five_star = st.session_state[f"five_star_temp_{player_num}"]
    
    # Создаем вкладки
    tab1, tab2 = st.tabs(["⭐ 6⭐ Оперативники", "⭐⭐ 5-4⭐ Оперативники"])
    
    # Вкладка 6⭐ - проверяем НЕ остаток, а БЫЛ ЛИ КУПЛЕН ресурс
    with tab1:
        # Проверяем, покупал ли участник универсальную защиту (по начальному значению)
        if universal_protection_initial == 0:
            st.warning("🔒 Вы не покупали 🛡️ Универсальную защиту. Защита 6⭐ недоступна.")
        elif not six_star_heroes:
            st.info("Нет 6⭐ оперативников.")
        else:
            # ПОКАЗЫВАЕМ вкладку всегда, даже если защит не осталось
            st.caption(f"🛡️ Осталось универсальных защит: {remaining_universal}")
            
            # Если защиты закончились - показываем предупреждение
            if remaining_universal <= 0:
                st.warning("⚠️ Все универсальные защиты потрачены. Вы можете снимать защиты, но новые добавить нельзя.")
            
            # Отображаем сеткой по 5 в ряд
            items_per_row = 5
            hero_list = six_star_heroes
            
            for i in range(0, len(hero_list), items_per_row):
                row_heroes = hero_list[i:i + items_per_row]
                cols = st.columns(len(row_heroes))
                
                for idx, (char_id, char_info) in enumerate(row_heroes):
                    with cols[idx]:
                        with st.container(border=True):
                            # Фото
                            img = load_operator_image(char_info['name'])
                            if img:
                                st.image(img, width=80)
                            else:
                                st.write("🎴")
                            
                            # Имя и характеристики
                            st.markdown(f"**{char_info['name']}**")
                            st.caption(f"{char_info['rarity']} | Lv.{char_info['level']} | П{char_info['potential']}")
                            
                            # Чекбокс защиты
                            is_protected = char_id in protected_heroes
                            
                            if is_protected:
                                # Если уже защищен - можно снять защиту ВСЕГДА
                                if st.checkbox("✅ Защищен", value=True, key=f"protect6_{char_id}_{player_num}"):
                                    pass
                                else:
                                    # Снимаем защиту - возвращаем ресурс
                                    protected_heroes.remove(char_id)
                                    remaining_universal += 1
                                    st.session_state[f"protected_temp_{player_num}"] = protected_heroes
                                    st.session_state[f"universal_temp_{player_num}"] = remaining_universal
                                    st.rerun()
                            else:
                                # Если НЕ защищен - кнопка активна ТОЛЬКО если есть остаток защит
                                if remaining_universal <= 0:
                                    st.checkbox("🛡️ Защитить", value=False, disabled=True, key=f"protect6_{char_id}_{player_num}")
                                    st.caption("❌ Нет защит")
                                else:
                                    if st.checkbox("🛡️ Защитить", value=False, key=f"protect6_{char_id}_{player_num}"):
                                        protected_heroes.append(char_id)
                                        remaining_universal -= 1
                                        st.session_state[f"protected_temp_{player_num}"] = protected_heroes
                                        st.session_state[f"universal_temp_{player_num}"] = remaining_universal
                                        st.rerun()
    
    # Вкладка 5-4⭐
    with tab2:
        if not other_heroes:
            st.info("Нет 5⭐ или 4⭐ оперативников.")
        else:
            # Подсчитываем сколько универсальных защит использовано на 6⭐
            used_universal_on_six = len([h for h in protected_heroes if h in [hid for hid, _ in six_star_heroes]])
            
            # Подсчитываем сколько каких защит использовано на 5-4⭐
            protected_other_ids = [h for h in protected_heroes if h in [hid for hid, _ in other_heroes]]
            protected_other_count = len(protected_other_ids)
            
            # Сколько защит 5⭐ использовано (не больше чем было)
            used_five_star = min(protected_other_count, five_star_protection_initial)
            # Сколько универсальных защит использовано на 5-4⭐
            used_universal_on_other = max(0, protected_other_count - five_star_protection_initial)
            
            # Остаток ресурсов
            remaining_five_star = five_star_protection_initial - used_five_star
            remaining_universal = universal_protection_initial - used_universal_on_six - used_universal_on_other
            
            # Обновляем временные переменные
            st.session_state[f"five_star_temp_{player_num}"] = remaining_five_star
            st.session_state[f"universal_temp_{player_num}"] = remaining_universal
            
            st.caption(f"🔵 Осталось защит 5⭐: {remaining_five_star}")
            if remaining_five_star == 0 and remaining_universal > 0:
                st.warning(f"⚠️ Защита 5⭐ кончилась, будет использована Универсальная (осталось: {remaining_universal})")
            
            # Отображаем сеткой по 5 в ряд
            items_per_row = 5
            hero_list = other_heroes
            
            for i in range(0, len(hero_list), items_per_row):
                row_heroes = hero_list[i:i + items_per_row]
                cols = st.columns(len(row_heroes))
                
                for idx, (char_id, char_info) in enumerate(row_heroes):
                    with cols[idx]:
                        with st.container(border=True):
                            # Фото
                            img = load_operator_image(char_info['name'])
                            if img:
                                st.image(img, width=80)
                            else:
                                st.write("🎴")
                            
                            # Имя и характеристики
                            st.markdown(f"**{char_info['name']}**")
                            st.caption(f"{char_info['rarity']} | Lv.{char_info['level']} | П{char_info['potential']}")
                            
                            # Чекбокс защиты
                            is_protected = char_id in protected_heroes
                            
                            if is_protected:
                                if st.checkbox("✅ Защищен", value=True, key=f"protect5_{char_id}_{player_num}"):
                                    pass
                                else:
                                    # Снимаем защиту - возвращаем ресурс
                                    protected_heroes.remove(char_id)
                                    # Определяем какой ресурс возвращать
                                    # Если количество защищенных 5-4⭐ больше чем было защит 5⭐, то последние использовали универсальную
                                    if len(protected_other_ids) > five_star_protection_initial:
                                        remaining_universal += 1
                                    else:
                                        remaining_five_star += 1
                                    
                                    st.session_state[f"protected_temp_{player_num}"] = protected_heroes
                                    st.session_state[f"five_star_temp_{player_num}"] = remaining_five_star
                                    st.session_state[f"universal_temp_{player_num}"] = remaining_universal
                                    st.rerun()
                            else:
                                # Проверяем доступность защиты
                                can_use_five = remaining_five_star > 0
                                can_use_universal = remaining_universal > 0
                                
                                if not can_use_five and not can_use_universal:
                                    st.checkbox("🛡️ Защитить", value=False, disabled=True, key=f"protect5_{char_id}_{player_num}")
                                    st.caption("❌ Нет защит")
                                else:
                                    # Текст кнопки
                                    if can_use_five:
                                        button_text = "🛡️ Защитить (🔵 5⭐)"
                                    else:
                                        button_text = "🛡️ Защитить (🛡️ Универсальная)"
                                    
                                    if st.checkbox(button_text, value=False, key=f"protect5_{char_id}_{player_num}"):
                                        protected_heroes.append(char_id)
                                        if can_use_five:
                                            remaining_five_star -= 1
                                        else:
                                            remaining_universal -= 1
                                        st.session_state[f"protected_temp_{player_num}"] = protected_heroes
                                        st.session_state[f"five_star_temp_{player_num}"] = remaining_five_star
                                        st.session_state[f"universal_temp_{player_num}"] = remaining_universal
                                        st.rerun()
    
    # Отображение остатка
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        protected_six = len([h for h in protected_heroes if h in [hid for hid, _ in six_star_heroes]])
        st.metric("🛡️ Защищено 6⭐", protected_six)
    with col2:
        protected_other = len([h for h in protected_heroes if h in [hid for hid, _ in other_heroes]])
        st.metric("🛡️ Защищено 5-4⭐", protected_other)
    with col3:
        st.metric("🛡️ Универсальных осталось", remaining_universal)
        st.metric("🔵 Защит 5⭐ осталось", remaining_five_star)
    
    # Кнопка завершения
    st.divider()
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("✅ Сохранить и завершить", key=f"finish_{player_num}", type="primary", use_container_width=True):
            data["protected_heroes"] = protected_heroes
            data["finished_protection"] = True
            # Обновляем ресурсы
            data["resources"]["🛡️ Универсальная защита"] = remaining_universal
            data["resources"]["🔵 Защита 5⭐"] = remaining_five_star
            
            if player_num == 1:
                st.session_state.p1 = data
            else:
                st.session_state.p2 = data
            
            save_player_data(player_num)
            
            # Очищаем временные данные
            del st.session_state[f"protected_temp_{player_num}"]
            del st.session_state[f"universal_temp_{player_num}"]
            del st.session_state[f"five_star_temp_{player_num}"]
            
            st.success(f"✅ Защищено {len(protected_heroes)} оперативников!")
            st.balloons()
            time.sleep(1)
            st.rerun()
    
    with col_btn2:
        if st.button("🔄 Сбросить все защиты", key=f"reset_{player_num}", use_container_width=True):
            st.session_state[f"protected_temp_{player_num}"] = []
            st.session_state[f"universal_temp_{player_num}"] = universal_protection_initial
            st.session_state[f"five_star_temp_{player_num}"] = five_star_protection_initial
            st.rerun()

# ========== 6. ИНТЕРФЕЙС БАНА  ==========

def ban_interface(player_num):
    """Интерфейс банов оперативников противника"""
    
    # Загружаем свои данные
    load_my_data(player_num)
    # Загружаем данные противника из файла судьи
    load_opponent_data(player_num)
    
    if player_num == 1:
        data = st.session_state.p1
        opponent_data = st.session_state.p2
    else:
        data = st.session_state.p2
        opponent_data = st.session_state.p1
    
    st.markdown("## 🔨 Этап банов оперативников")
    st.markdown(f"Вы баните оперативников **{opponent_data.get('nickname', 'Противника')}**")
    
    # Получаем ресурсы участника для банов
    resources = data.get("resources", {})
    universal_ban_initial = resources.get("🔴 Универсальный бан", 0)
    five_star_ban_initial = resources.get("🔵 Бан 4-5⭐", 0)
    
    # Базовая комплектация: 1 универсальный бан бесплатно
    if universal_ban_initial > 0:
        universal_ban_initial = universal_ban_initial  # уже включает бесплатный
    
    # ========== ПОЛНАЯ ИНФОРМАЦИЯ О ЗАКУПКАХ ==========
    st.markdown("### 📊 Полная информация о закупках ресурсов")
    
    all_resources = [
        "🛡️ Универсальная защита",
        "🔵 Защита 5⭐", 
        "🔴 Универсальное воскрешение",
        "🔵 Воскрешение 5⭐",
        "🔴 Универсальный бан",
        "🔵 Бан 4-5⭐",
        "🔄 Рестарт"
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**{data.get('nickname', 'Участник 1')}**")
        st.markdown("**🎁 Бесплатно:** 🔄 Рестарт x1, 🔴 Универсальный бан x1")
        st.markdown("**💰 Куплено:**")
        for res in all_resources:
            count = resources.get(res, 0)
            if res in ["🔄 Рестарт", "🔴 Универсальный бан"]:
                purchased = max(0, count - 1)
                if purchased > 0:
                    st.write(f"{res}: {purchased}")
            else:
                if count > 0:
                    st.write(f"{res}: {count}")
        remaining_points = data.get("points", STARTING_POINTS)
        st.markdown(f"💎 Осталось Увыкоинов: {remaining_points}")
    
    with col2:
        st.markdown(f"**{opponent_data.get('nickname', 'Участник 2')}**")
        st.markdown("**🎁 Бесплатно:** 🔄 Рестарт x1, 🔴 Универсальный бан x1")
        st.markdown("**💰 Куплено:**")
        opponent_resources = opponent_data.get("resources", {})
        for res in all_resources:
            count = opponent_resources.get(res, 0)
            if res in ["🔄 Рестарт", "🔴 Универсальный бан"]:
                purchased = max(0, count - 1)
                if purchased > 0:
                    st.write(f"{res}: {purchased}")
            else:
                if count > 0:
                    st.write(f"{res}: {count}")
        opponent_remaining_points = opponent_data.get("points", STARTING_POINTS)
        st.markdown(f"💎 Осталось Увыкоинов: {opponent_remaining_points}")
    
    st.divider()
    
    # ========== ИНФОРМАЦИЯ О ВЫБРАННЫХ КОМНАТАХ ==========
    selected_rooms = get_selected_rooms()
    if selected_rooms:
        st.markdown("### 🏟️ Информация о турнире")
        st.markdown("**Судья подобрал для вас следующие комнаты:**")
        for idx, room in enumerate(selected_rooms, 1):
            st.markdown(f"**Комната {room}**")
        st.divider()

    # Проверяем, есть ли вообще ресурсы для банов
    if universal_ban_initial == 0 and five_star_ban_initial == 0:
        st.error("❌ У вас нет ресурсов для банов оперативников!")
        
        if st.button("✅ Пропустить этап банов", key=f"skip_ban_{player_num}", type="primary"):
            data["bans"] = {"opponent_bans": []}
            data["finished_bans"] = True
            save_player_data(player_num)
            st.success("Этап банов пропущен! Ожидайте Судью.")
            st.rerun()
        return
    
    # Получаем список оперативников ПРОТИВНИКА
    opponent_character_db = opponent_data.get("character_db", {})
    
    # Разделяем оперативников противника по редкости
    # Также учитываем защиту противника - забаненного оперативника нельзя защитить, но банить можно
    six_star_enemies = []
    other_enemies = []
    
    for char_id, char_info in opponent_character_db.items():
        if char_info.get("has_operator", False):
            # Проверяем, защитил ли противник этого оперативника
            is_protected = char_id in opponent_data.get("protected_heroes", [])
            
            if char_info["rarity"] == "6⭐":
                six_star_enemies.append((char_id, char_info, is_protected))
            else:
                other_enemies.append((char_id, char_info, is_protected))
    
    # Получаем уже забаненных (сохраняем в data)
    current_bans = data.get("bans", {})
    banned_heroes = current_bans.get("opponent_bans", [])
    
    # Временное хранилище для банов
    if f"bans_temp_{player_num}" not in st.session_state:
        st.session_state[f"bans_temp_{player_num}"] = banned_heroes.copy()
    if f"universal_ban_temp_{player_num}" not in st.session_state:
        st.session_state[f"universal_ban_temp_{player_num}"] = universal_ban_initial
    if f"five_star_ban_temp_{player_num}" not in st.session_state:
        st.session_state[f"five_star_ban_temp_{player_num}"] = five_star_ban_initial
    
    temp_banned = st.session_state[f"bans_temp_{player_num}"]
    remaining_universal_ban = st.session_state[f"universal_ban_temp_{player_num}"]
    remaining_five_star_ban = st.session_state[f"five_star_ban_temp_{player_num}"]
    
    # Создаем вкладки
    tab1, tab2 = st.tabs(["⭐ 6⭐ Оперативники противника", "⭐⭐ 5-4⭐ Оперативники противника"])
    
    # Вкладка 6⭐
    with tab1:
        if universal_ban_initial == 0:
            st.warning("🔒 Вы не покупали 🔴 Универсальный бан. Бан 6⭐ оперативников недоступен.")
        elif not six_star_enemies:
            st.info("У противника нет 6⭐ оперативников.")
        else:
            st.caption(f"🔴 Осталось универсальных банов: {remaining_universal_ban}")
            
            if remaining_universal_ban <= 0 and universal_ban_initial > 0:
                st.warning("⚠️ Все универсальные баны потрачены. Вы можете снимать баны, но новые добавить нельзя.")
            
            # Отображаем сеткой по 5 в ряд
            items_per_row = 5
            hero_list = six_star_enemies
            
            for i in range(0, len(hero_list), items_per_row):
                row_heroes = hero_list[i:i + items_per_row]
                cols = st.columns(len(row_heroes))
                
                for idx, (char_id, char_info, is_protected) in enumerate(row_heroes):
                    with cols[idx]:
                        with st.container(border=True):
                            # Фото
                            img = load_operator_image(char_info['name'])
                            if img:
                                st.image(img, width=80)
                            else:
                                st.write("🎴")
                            
                            # Имя и характеристики
                            st.markdown(f"**{char_info['name']}**")
                            st.caption(f"{char_info['rarity']} | Lv.{char_info['level']} | П{char_info['potential']}")
                            
                            # Статус защиты противника
                            if is_protected:
                                st.success("🛡️ Защищен противником")
                            else:
                                st.caption("❌ Не защищен")
                            
                            # Чекбокс бана
                            is_banned = char_id in temp_banned
                            
                            if is_banned:
                                if st.checkbox("🔨 Забанен", value=True, key=f"ban6_{char_id}_{player_num}"):
                                    pass
                                else:
                                    # Снимаем бан - возвращаем ресурс (всегда универсальный для 6⭐)
                                    temp_banned.remove(char_id)
                                    remaining_universal_ban += 1
                                    st.session_state[f"bans_temp_{player_num}"] = temp_banned
                                    st.session_state[f"universal_ban_temp_{player_num}"] = remaining_universal_ban
                                    st.rerun()
                            else:
                                # Кнопка активна только если есть остаток универсальных банов
                                if remaining_universal_ban <= 0:
                                    st.checkbox("🔨 Забанить", value=False, disabled=True, key=f"ban6_{char_id}_{player_num}")
                                    st.caption("❌ Нет банов")
                                else:
                                    if st.checkbox("🔨 Забанить", value=False, key=f"ban6_{char_id}_{player_num}"):
                                        temp_banned.append(char_id)
                                        remaining_universal_ban -= 1
                                        st.session_state[f"bans_temp_{player_num}"] = temp_banned
                                        st.session_state[f"universal_ban_temp_{player_num}"] = remaining_universal_ban
                                        st.rerun()
    
    # Вкладка 5-4⭐
    with tab2:
        if not other_enemies:
            st.info("У противника нет 5⭐ или 4⭐ оперативников.")
        else:
            # Подсчитываем использованные баны
            banned_other_ids = [h for h in temp_banned if h in [hid for hid, _, _ in other_enemies]]
            banned_other_count = len(banned_other_ids)
            
            used_five_star_ban = min(banned_other_count, five_star_ban_initial)
            remaining_five_star_ban_display = five_star_ban_initial - used_five_star_ban
            
            st.caption(f"🔵 Осталось банов 5⭐: {remaining_five_star_ban_display}")
            
            if remaining_five_star_ban_display == 0 and remaining_universal_ban > 0:
                st.warning(f"⚠️ Баны 5⭐ кончились, будет использован Универсальный бан (осталось: {remaining_universal_ban})")
            
            # Отображаем сеткой по 5 в ряд
            items_per_row = 5
            hero_list = other_enemies
            
            for i in range(0, len(hero_list), items_per_row):
                row_heroes = hero_list[i:i + items_per_row]
                cols = st.columns(len(row_heroes))
                
                for idx, (char_id, char_info, is_protected) in enumerate(row_heroes):
                    with cols[idx]:
                        with st.container(border=True):
                            # Фото
                            img = load_operator_image(char_info['name'])
                            if img:
                                st.image(img, width=80)
                            else:
                                st.write("🎴")
                            
                            # Имя и характеристики
                            st.markdown(f"**{char_info['name']}**")
                            st.caption(f"{char_info['rarity']} | Lv.{char_info['level']} | П{char_info['potential']}")
                            
                            # Статус защиты противника
                            if is_protected:
                                st.success("🛡️ Защищен противником")
                            else:
                                st.caption("❌ Не защищен")
                            
                            # Чекбокс бана
                            is_banned = char_id in temp_banned
                            
                            if is_banned:
                                if st.checkbox("🔨 Забанен", value=True, key=f"ban5_{char_id}_{player_num}"):
                                    pass
                                else:
                                    # Снимаем бан - определяем какой ресурс возвращать
                                    # Находим позицию в списке забаненных 5-4⭐
                                    banned_order = [h for h in temp_banned if h in [hid for hid, _, _ in other_enemies]]
                                    position = banned_order.index(char_id)
                                    
                                    if position < five_star_ban_initial:
                                        remaining_five_star_ban_display += 1
                                    else:
                                        remaining_universal_ban += 1
                                    
                                    temp_banned.remove(char_id)
                                    st.session_state[f"bans_temp_{player_num}"] = temp_banned
                                    st.session_state[f"five_star_ban_temp_{player_num}"] = remaining_five_star_ban_display
                                    st.session_state[f"universal_ban_temp_{player_num}"] = remaining_universal_ban
                                    st.rerun()
                            else:
                                # Проверяем доступность бана
                                can_use_five = remaining_five_star_ban_display > 0
                                can_use_universal = remaining_universal_ban > 0
                                
                                if not can_use_five and not can_use_universal:
                                    st.checkbox("🔨 Забанить", value=False, disabled=True, key=f"ban5_{char_id}_{player_num}")
                                    st.caption("❌ Нет банов")
                                else:
                                    # Текст кнопки
                                    if can_use_five:
                                        button_text = "🔨 Забанить (🔵 5⭐)"
                                    else:
                                        button_text = "🔨 Забанить (🔴 Универсальный)"
                                    
                                    if st.checkbox(button_text, value=False, key=f"ban5_{char_id}_{player_num}"):
                                        temp_banned.append(char_id)
                                        if can_use_five:
                                            remaining_five_star_ban_display -= 1
                                        else:
                                            remaining_universal_ban -= 1
                                        st.session_state[f"bans_temp_{player_num}"] = temp_banned
                                        st.session_state[f"five_star_ban_temp_{player_num}"] = remaining_five_star_ban_display
                                        st.session_state[f"universal_ban_temp_{player_num}"] = remaining_universal_ban
                                        st.rerun()
    
    # Отображение остатка
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        banned_six = len([h for h in temp_banned if h in [hid for hid, _, _ in six_star_enemies]])
        st.metric("🔨 Забанено 6⭐", banned_six)
    with col2:
        banned_other = len([h for h in temp_banned if h in [hid for hid, _, _ in other_enemies]])
        st.metric("🔨 Забанено 5-4⭐", banned_other)
    with col3:
        st.metric("🔴 Универсальных банов осталось", remaining_universal_ban)
        st.metric("🔵 Банов 5⭐ осталось", remaining_five_star_ban_display)
    
    # Кнопка завершения
    st.divider()
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("✅ Сохранить и завершить баны", key=f"finish_bans_{player_num}", type="primary", use_container_width=True):
            # Сохраняем баны
            data["bans"] = {"opponent_bans": temp_banned}
            data["finished_bans"] = True
            
            # Обновляем ресурсы банов
            data["resources"]["🔴 Универсальный бан"] = remaining_universal_ban
            data["resources"]["🔵 Бан 4-5⭐"] = remaining_five_star_ban_display
            
            if player_num == 1:
                st.session_state.p1 = data
            else:
                st.session_state.p2 = data
            
            save_player_data(player_num)
            
            # Очищаем временные данные
            del st.session_state[f"bans_temp_{player_num}"]
            del st.session_state[f"universal_ban_temp_{player_num}"]
            del st.session_state[f"five_star_ban_temp_{player_num}"]
            
            st.success(f"✅ Забанено {len(temp_banned)} оперативников противника!")
            st.balloons()
            time.sleep(1)
            st.rerun()
    
    with col_btn2:
        if st.button("🔄 Сбросить все баны", key=f"reset_bans_{player_num}", use_container_width=True):
            st.session_state[f"bans_temp_{player_num}"] = []
            st.session_state[f"universal_ban_temp_{player_num}"] = universal_ban_initial
            st.session_state[f"five_star_ban_temp_{player_num}"] = five_star_ban_initial
            st.rerun()


# ========== 7. ИНТЕРФЕЙС ПИКОВ  ==========

def picks_interface(player_num):
    """Интерфейс выбора пиков (3 пачки по 4 оперативника)"""
    
    # Загружаем свои данные
    load_my_data(player_num)
    # Загружаем данные противника из файла судьи
    load_opponent_data(player_num)
    
    if player_num == 1:
        data = st.session_state.p1
        opponent_data = st.session_state.p2
    else:
        data = st.session_state.p2
        opponent_data = st.session_state.p1
    
    st.markdown("## ⭐ Этап пиков оперативников")
    st.markdown(f"Формирование пачек для **{data.get('nickname', 'Участника')}**")
    
    # Получаем ресурсы воскрешений
    resources = data.get("resources", {})
    universal_resurrection = resources.get("🔴 Универсальное воскрешение", 0)
    five_star_resurrection = resources.get("🔵 Воскрешение 5⭐", 0)
    total_resurrections = universal_resurrection + five_star_resurrection
    
    # Получаем список доступных оперативников
    character_db = data.get("character_db", {})
    opponent_bans = opponent_data.get("bans", {}).get("opponent_bans", [])
    
    available_heroes = []
    for char_id, char_info in character_db.items():
        if char_info.get("has_operator", False) and char_id not in opponent_bans:
            available_heroes.append((char_id, char_info))
    
    # Сортируем по редкости
    def rarity_order(r):
        if r == "6⭐":
            return 0
        elif r == "5⭐":
            return 1
        else:
            return 2
    
    available_heroes.sort(key=lambda x: rarity_order(x[1]["rarity"]))
    
    # Получаем текущие пики
    current_picks = data.get("picks", [[None for _ in range(4)] for _ in range(3)])
    
    # Временное хранилище
    if f"picks_temp_{player_num}" not in st.session_state:
        st.session_state[f"picks_temp_{player_num}"] = [row[:] for row in current_picks]
    if f"selected_pack_{player_num}" not in st.session_state:
        st.session_state[f"selected_pack_{player_num}"] = None
    
    picks = st.session_state[f"picks_temp_{player_num}"]
    selected_pack = st.session_state[f"selected_pack_{player_num}"]
    
    # ========== ПОДСЧЁТ ИСПОЛЬЗОВАНИЙ ==========
    usage_count = {}
    for pack in picks:
        for hero_id in pack:
            if hero_id:
                usage_count[hero_id] = usage_count.get(hero_id, 0) + 1
    
    unique_six = set()
    unique_five = set()
    total_six = 0
    total_five = 0
    
    for hero_id, count in usage_count.items():
        char_info = character_db.get(hero_id, {})
        rarity = char_info.get("rarity", "4⭐")
        if rarity == "6⭐":
            unique_six.add(hero_id)
            total_six += count
        elif rarity == "5⭐":
            unique_five.add(hero_id)
            total_five += count
    
    # Повторные использования
    repeats_six = total_six - len(unique_six)
    repeats_total = (total_six + total_five) - (len(unique_six) + len(unique_five))
    
    six_limit = universal_resurrection
    five_limit = total_resurrections
    
    remaining_six = max(0, six_limit - repeats_six)
    remaining_total = max(0, five_limit - repeats_total)
    
    # Отображение статистики
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🔴 Универсальное", universal_resurrection)
    with col2:
        st.metric("🔵 Воскрешение 5⭐", five_star_resurrection)
    with col3:
        if repeats_six > six_limit:
            st.metric("⭐ 6⭐", f"{repeats_six}/{six_limit}", delta="❌", delta_color="inverse")
        else:
            st.metric("⭐ 6⭐", f"{repeats_six}/{six_limit}", delta=f"↓{remaining_six}")
    with col4:
        if repeats_total > five_limit:
            st.metric("⭐⭐ 5⭐", f"{repeats_total}/{five_limit}", delta="❌", delta_color="inverse")
        else:
            st.metric("⭐⭐ 5⭐", f"{repeats_total}/{five_limit}", delta=f"↓{remaining_total}")
    
    st.divider()
    
    # ========== ИНФОРМАЦИЯ О КОМНАТАХ ==========
    selected_rooms = get_selected_rooms()
    if selected_rooms:
        st.markdown("🏟️ **Комнаты:** " + ", ".join(selected_rooms))
        st.divider()
    
    # ========== ОСНОВНОЙ ИНТЕРФЕЙС ==========
    # Левая часть 70%, правая 30%
    left_col, right_col = st.columns([0.65, 0.35])
    
    # ========== ЛЕВАЯ ЧАСТЬ ==========
    with left_col:
        st.markdown("### 📋 Оперативники")
        
        if selected_pack is not None:
            st.success(f"✅ Пачка {selected_pack + 1} выбрана")
        else:
            st.warning("⚠️ Сначала выберите пачку")
        
        # Определяем количество ячеек в строке
        hero_count = len(available_heroes)
        items_per_row = 8 if hero_count < 25 else 9
        
        hero_list = available_heroes
        
        for i in range(0, len(hero_list), items_per_row):
            row_heroes = hero_list[i:i + items_per_row]
            cols = st.columns(len(row_heroes))
            
            for idx, (char_id, char_info) in enumerate(row_heroes):
                with cols[idx]:
                    with st.container(border=True):
                        img = load_operator_image(char_info['name'])
                        if img:
                            st.image(img, width=60)
                        else:
                            st.write("🎴")
                        
                        st.markdown(f"**{char_info['name']}**")
                        
                        # Информация: уровень, потенциал, ранг
                        rank = 6 if char_info["rarity"] == "6⭐" else (5 if char_info["rarity"] == "5⭐" else 4)
                        st.caption(f"Lv.{char_info['level']} | П{char_info['potential']} | {rank}")
                        
                        count = usage_count.get(char_id, 0)
                        
                        # Проверка возможности добавления
                        can_add = True
                        is_duplicate = False
                        
                        if selected_pack is not None:
                            is_duplicate = char_id in picks[selected_pack]
                            if is_duplicate:
                                can_add = False
                            elif char_info["rarity"] == "6⭐":
                                if char_id in usage_count:
                                    new_repeats = repeats_six + 1
                                else:
                                    new_repeats = repeats_six
                                if new_repeats > six_limit:
                                    can_add = False
                            elif char_info["rarity"] == "5⭐":
                                if char_id in usage_count:
                                    new_repeats_total = repeats_total + 1
                                else:
                                    new_repeats_total = repeats_total
                                if new_repeats_total > five_limit:
                                    can_add = False
                        
                        # Кнопка выбора (только иконка)
                        if selected_pack is not None:
                            if is_duplicate:
                                st.button(f"❌", key=f"hero_{char_id}_{player_num}", disabled=True, use_container_width=True)
                            elif not can_add:
                                st.button(f"🚫", key=f"hero_{char_id}_{player_num}", disabled=True, use_container_width=True)
                            else:
                                if st.button(f"➕", key=f"hero_{char_id}_{player_num}", use_container_width=True):
                                    first_empty = None
                                    for slot_idx in range(4):
                                        if picks[selected_pack][slot_idx] is None:
                                            first_empty = slot_idx
                                            break
                                    
                                    if first_empty is not None:
                                        picks[selected_pack][first_empty] = char_id
                                        st.session_state[f"picks_temp_{player_num}"] = picks
                                        st.success(f"✅ {char_info['name']} добавлен")
                                        st.rerun()
                                    else:
                                        st.error(f"❌ Нет свободных слотов!")
                        else:
                            st.button(f"🔒", key=f"hero_disabled_{char_id}_{player_num}", disabled=True, use_container_width=True)
    
    # ========== ПРАВАЯ ЧАСТЬ ==========
    with right_col:
        st.markdown("### 🎮 Пачки")
        st.caption("Кнопка: выбор/очистка пачки")
        
        for pack_idx in range(3):
            cols = st.columns(5)
            
            # Получаем комнату для этой пачки (если комнаты выбраны)
            room_for_pack = selected_rooms[pack_idx] if pack_idx < len(selected_rooms) else "?"
            
            with cols[0]:
                if selected_pack == pack_idx:
                    button_type = "primary"
                    button_text = f"✅ Пачка {pack_idx + 1} → Комната {room_for_pack}"
                else:
                    button_type = "secondary"
                    button_text = f"📦 Пачка {pack_idx + 1} → Комната {room_for_pack}"
                
                if st.button(button_text, key=f"pack_btn_{pack_idx}_{player_num}", use_container_width=True, type=button_type):
                    if selected_pack == pack_idx:
                        picks[pack_idx] = [None, None, None, None]
                        st.session_state[f"picks_temp_{player_num}"] = picks
                        st.session_state[f"selected_pack_{player_num}"] = None
                        st.success(f"Пачка {pack_idx + 1} (Комната {room_for_pack}) очищена")
                        st.rerun()
                    else:
                        st.session_state[f"selected_pack_{player_num}"] = pack_idx
                        st.rerun()
            
            for slot_idx in range(4):
                with cols[slot_idx + 1]:
                    current_hero_id = picks[pack_idx][slot_idx]
                    
                    with st.container(border=True):
                        if current_hero_id:
                            hero_info = character_db.get(current_hero_id, {})
                            
                            img = load_operator_image(hero_info.get('name', ''))
                            if img:
                                st.image(img, width=50)
                            else:
                                st.write("🎴")
                            
                            rank = 6 if hero_info.get("rarity") == "6⭐" else (5 if hero_info.get("rarity") == "5⭐" else 4)
                            st.markdown(f"**{hero_info.get('name', '???')[:12]}**")
                            st.caption(f"Lv.{hero_info.get('level', 0)} | П{hero_info.get('potential', 0)} | {rank}")
                        else:
                            st.markdown("*⬜*")
                            st.caption(f"слот {slot_idx + 1}")
        
        st.divider()
        
        # Новая логика: пачка считается готовой, если есть хотя бы один оперативник
        packs_ready = 0
        for pack_idx in range(3):
            if any(picks[pack_idx][slot] is not None for slot in range(4)):
                packs_ready += 1
        
        total_filled = sum(1 for pack in picks for slot in pack if slot is not None)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Заполнено слотов", f"{total_filled}/12")
        with col2:
            st.metric("Готовых пачек", f"{packs_ready}/3")
    
    # ========== КНОПКИ УПРАВЛЕНИЯ ==========
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Сбросить выбор пачки", key=f"clear_selected_pack_{player_num}", use_container_width=True):
            st.session_state[f"selected_pack_{player_num}"] = None
            st.rerun()
    
    with col2:
        if st.button("🗑️ Сбросить всё", key=f"reset_all_picks_{player_num}", use_container_width=True):
            st.session_state[f"picks_temp_{player_num}"] = [[None for _ in range(4)] for _ in range(3)]
            st.session_state[f"selected_pack_{player_num}"] = None
            st.rerun()
    
    with col3:
        if st.button("✅ Сохранить и завершить", key=f"finish_picks_{player_num}", type="primary", use_container_width=True):
            # Валидация
            errors = []
            
            # Проверяем, что есть хотя бы одна непустая пачка
            if packs_ready == 0:
                errors.append(f"❌ Нужно заполнить хотя бы одну пачку")
            
            # Дубликаты в пачках
            for pack_idx, pack in enumerate(picks):
                seen = set()
                for hero_id in pack:
                    if hero_id:
                        if hero_id in seen:
                            errors.append(f"❌ Дубликат в пачке {pack_idx + 1}")
                            break
                        seen.add(hero_id)
            
            # Финальный пересчёт повторов
            final_usage = {}
            for pack in picks:
                for hero_id in pack:
                    if hero_id:
                        final_usage[hero_id] = final_usage.get(hero_id, 0) + 1
            
            final_unique_six = set()
            final_unique_five = set()
            final_total_six = 0
            final_total_five = 0
            
            for hero_id, count in final_usage.items():
                char_info = character_db.get(hero_id, {})
                rarity = char_info.get("rarity", "4⭐")
                if rarity == "6⭐":
                    final_unique_six.add(hero_id)
                    final_total_six += count
                elif rarity == "5⭐":
                    final_unique_five.add(hero_id)
                    final_total_five += count
            
            final_repeats_six = final_total_six - len(final_unique_six)
            final_repeats_total = (final_total_six + final_total_five) - (len(final_unique_six) + len(final_unique_five))
            
            if final_repeats_six > universal_resurrection:
                errors.append(f"❌ Превышен лимит 6⭐: {final_repeats_six} повторов, доступно {universal_resurrection}")
            
            if final_repeats_total > total_resurrections:
                errors.append(f"❌ Превышен лимит воскрешений: {final_repeats_total} повторов, доступно {total_resurrections}")
            
            if errors:
                for err in errors:
                    st.error(err)
            else:
                data["picks"] = picks
                data["finished_picks"] = True
                
                if player_num == 1:
                    st.session_state.p1 = data
                else:
                    st.session_state.p2 = data
                
                save_player_data(player_num)
                
                del st.session_state[f"picks_temp_{player_num}"]
                del st.session_state[f"selected_pack_{player_num}"]
                
                st.success("✅ Пачки сохранены!")
                st.balloons()
                time.sleep(1)
                st.rerun()

# ========== 8. КОМНАТА ОЖИДАНИЯ УЧАСТНИКА  ==========

def waiting_room_interface(player_num):
    """Комната ожидания — отображение итоговой информации перед боем в реальной игре"""
    
    # Загружаем свои данные
    load_my_data(player_num)
    # Загружаем данные противника
    load_opponent_data(player_num)
    
    if player_num == 1:
        data = st.session_state.p1
        opponent_data = st.session_state.p2
    else:
        data = st.session_state.p2
        opponent_data = st.session_state.p1
    
    st.markdown("## 🏨 Комната ожидания")
    st.markdown(f"**{data.get('nickname', 'Участник')}**, вы завершили все этапы!")
    st.caption("Ожидайте начала реальных боёв в игре. После завершения турнира вы можете выйти.")
    
    st.divider()
    
    # Кнопка выхода (единственная активная кнопка)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚪 Выйти из турнира", key=f"exit_waiting_{player_num}", use_container_width=True):
            if player_num == 1:
                st.session_state.auth_player1 = False
            else:
                st.session_state.auth_player2 = False
            st.session_state.current_role = None
            save_player_data(player_num)
            st.rerun()
    
    st.divider()
    
    # ========== ТАБЛИЦА 2x5 ==========
    st.markdown("### 📊 Сводная информация")
    
    # Создаём 5 колонок для заголовков
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown("**Ресурсы**")
    with col2:
        st.markdown("**Защита**")
    with col3:
        st.markdown("**Бан (ваш)**")
    with col4:
        st.markdown("**Бан (противник)**")
    with col5:
        st.markdown("**Пачки**")
    
    # Вторая строка — данные
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        resources = data.get("resources", {})
        bought = []
        for res_name, count in resources.items():
            if count > 0:
                if res_name == "🔄 Рестарт":
                    purchased = max(0, count - 1)
                    if purchased > 0:
                        bought.append(f"{res_name}: +{purchased}")
                    else:
                        bought.append(f"{res_name}: 1 (бесплатно)")
                elif res_name == "🔴 Универсальный бан":
                    purchased = max(0, count - 1)
                    if purchased > 0:
                        bought.append(f"{res_name}: +{purchased}")
                    else:
                        bought.append(f"{res_name}: 1 (бесплатно)")
                else:
                    bought.append(f"{res_name}: {count}")
        
        if bought:
            for item in bought:
                st.write(item)
        else:
            st.write("—")
        
        st.write(f"💎 Осталось: {data.get('points', 12)}")
    
    with col2:
        protected = data.get("protected_heroes", [])
        character_db = data.get("character_db", {})
        if protected:
            for hero_id in protected:
                hero_info = character_db.get(hero_id, {})
                st.write(f"🛡️ {hero_info.get('name', '???')}")
        else:
            st.write("—")
    
    with col3:
        bans = data.get("bans", {}).get("opponent_bans", [])
        if bans:
            for hero_id in bans:
                hero_info = opponent_data.get("character_db", {}).get(hero_id, {})
                st.write(f"🔨 {hero_info.get('name', '???')}")
        else:
            st.write("—")
    
    with col4:
        opponent_bans = opponent_data.get("bans", {}).get("opponent_bans", [])
        if opponent_bans:
            for hero_id in opponent_bans:
                hero_info = data.get("character_db", {}).get(hero_id, {})
                st.write(f"🔨 {hero_info.get('name', '???')}")
        else:
            st.write("—")
    
    with col5:
        picks = data.get("picks", [])
        pack_count = 0
        for pack in picks:
            if any(slot is not None for slot in pack):
                pack_count += 1
        st.write(f"✅ Пачек: {pack_count}/3")
        if pack_count > 0:
            st.caption("(подробнее ниже)")
    
    st.divider()
    
    # ========== ПОДРОБНАЯ ИНФОРМАЦИЯ О ПАЧКАХ ==========
    st.markdown("### 🎮 Ваши пачки")
    
    picks = data.get("picks", [[None for _ in range(4)] for _ in range(3)])
    character_db = data.get("character_db", {})
    
    for pack_idx in range(3):
        pack = picks[pack_idx]
        if any(slot is not None for slot in pack):
            st.markdown(f"#### Пачка {pack_idx + 1}")
            
            cols = st.columns(4)
            for slot_idx, hero_id in enumerate(pack):
                with cols[slot_idx]:
                    with st.container(border=True):
                        if hero_id:
                            hero_info = character_db.get(hero_id, {})
                            img = load_operator_image(hero_info.get('name', ''))
                            if img:
                                st.image(img, width=80)
                            else:
                                st.write("🎴")
                            rank = 6 if hero_info.get("rarity") == "6⭐" else (5 if hero_info.get("rarity") == "5⭐" else 4)
                            st.markdown(f"**{hero_info.get('name', '???')}**")
                            st.caption(f"Lv.{hero_info.get('level', 0)} | П{hero_info.get('potential', 0)} | {rank}")
                        else:
                            st.markdown("*⬜*")
                            st.caption("Пусто")
            st.divider()
        else:
            st.markdown(f"#### Пачка {pack_idx + 1} — пустая")
            st.divider()
    
    # ========== ИНФОРМАЦИЯ О ПРОТИВНИКЕ (кратко) ==========
    with st.expander("👤 Информация о противнике", expanded=False):
        st.markdown(f"**{opponent_data.get('nickname', 'Противник')}**")
        
        # Защита противника
        opponent_protected = opponent_data.get("protected_heroes", [])
        if opponent_protected:
            st.markdown("**Защита противника:**")
            for hero_id in opponent_protected:
                hero_info = opponent_data.get("character_db", {}).get(hero_id, {})
                st.write(f"🛡️ {hero_info.get('name', '???')}")
        
        # Пачки противника
        opponent_picks = opponent_data.get("picks", [])
        st.markdown("**Пачки противника:**")
        for pack_idx, pack in enumerate(opponent_picks):
            if any(slot is not None for slot in pack):
                hero_names = []
                for hero_id in pack:
                    if hero_id:
                        hero_info = opponent_data.get("character_db", {}).get(hero_id, {})
                        hero_names.append(f"{hero_info.get('name', '?')}")
                st.write(f"Пачка {pack_idx + 1}: {', '.join(hero_names) if hero_names else 'пустая'}")
            else:
                st.write(f"Пачка {pack_idx + 1}: пустая")
    
    st.divider()
    st.caption("🏆 После завершения реальных боёв в игре, судья объявит результаты и завершит турнир.")


# ========== 9. ИНТЕРФЕЙС СУДЬИ ==========

def judge_interface():
    """Интерфейс судьи"""
    
    # Инициализация состояния выбора комнат
    if "rooms_selection_mode" not in st.session_state:
        st.session_state.rooms_selection_mode = False
    
    # Если в режиме выбора комнат - показываем только интерфейс выбора
    if st.session_state.rooms_selection_mode:
        rooms_selection_only_interface()
        return
    
    # Загружаем данные
    load_judge_data()
    
    p1 = st.session_state.get("p1", {})
    p2 = st.session_state.get("p2", {})
    
    # ========== ЕСЛИ ЭТАП БОЯ - ПОКАЗЫВАЕМ ИНТЕРФЕЙС БОЯ ==========
    if p1.get("stage") == "battle" or p2.get("stage") == "battle":
        battle_interface()
        return

    # Информационная панель
    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
    with col1:
        st.markdown("## ⚖️ Панель Судьи")
    with col2:
        st.caption("Ключ: `judge_2024`")
    with col3:
        if st.button("📥 Собрать данные", key="sync_btn", use_container_width=True):
            # Загружаем данные из файлов участников
            if os.path.exists(PLAYER1_FILE):
                try:
                    with open(PLAYER1_FILE, "r", encoding="utf-8") as f:
                        p1_data = json.load(f)
                        for key, value in p1_data.items():
                            st.session_state.p1[key] = value
                    st.success("✅ Данные Участника 1 загружены!")
                except Exception as e:
                    st.error(f"Ошибка загрузки Участника 1: {e}")
            
            if os.path.exists(PLAYER2_FILE):
                try:
                    with open(PLAYER2_FILE, "r", encoding="utf-8") as f:
                        p2_data = json.load(f)
                        for key, value in p2_data.items():
                            st.session_state.p2[key] = value
                    st.success("✅ Данные Участника 2 загружены!")
                except Exception as e:
                    st.error(f"Ошибка загрузки Участника 2: {e}")
            
            # Сохраняем в файл судьи
            judge_state = {
                "p1": st.session_state.p1,
                "p2": st.session_state.p2,
                "selected_rooms": st.session_state.get("temp_selected_rooms", [])
            }
            with open(JUDGE_FILE, "w", encoding="utf-8") as f:
                json.dump(judge_state, f, ensure_ascii=False, indent=2, default=str)
            
            st.success("📁 Данные сохранены в judge_data.json!")
            time.sleep(1)
            st.rerun()
    
    with col4:
        if st.button("🔄 Обновить", key="refresh_judge_btn", use_container_width=True):
            load_judge_data()
            st.rerun()
    
    with col5:
        if st.button("🚪 Выйти", key="exit_judge", use_container_width=True):
            st.session_state.auth_judge = False
            st.session_state.current_role = None
            st.rerun()
    
    st.divider()
    
    # Загружаем данные из файла судьи
    load_judge_data()
    
    # Получаем данные
    p1 = st.session_state.get("p1", {})
    p2 = st.session_state.get("p2", {})
    
    # Отображение статуса участников
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⚔️ Участник 1")
        st.caption("Ключ: player1_2024")
        st.write(f"**Никнейм:** {p1.get('nickname', 'Не указан')}")
        st.write(f"**Готовность:** {'✅ Готов' if p1.get('ready') else '⏳ Ожидание'}")
        st.write(f"**Этап:** {get_stage_name(p1.get('stage', 'resources'))}")
        
        with st.expander("📋 Детальный статус"):
            st.write(f"Закупка: {'✅' if p1.get('finished_resources') else '⏳'}")
            st.write(f"Выбор оперативников: {'✅' if p1.get('finished_available') else '⏳'}")
            st.write(f"Защита: {'✅' if p1.get('finished_protection') else '⏳'}")
            st.write(f"Баны: {'✅' if p1.get('finished_bans') else '⏳'}")
            st.write(f"Пики: {'✅' if p1.get('finished_picks') else '⏳'}")
        
        available = p1.get("available_heroes", [])
        st.write(f"**Оперативников:** {len(available)}")
        protected = p1.get("protected_heroes", [])
        st.write(f"**Защищено:** {len(protected)}")
        banned = p1.get("bans", {}).get("opponent_bans", [])
        st.write(f"**Забанено:** {len(banned)}")
    
    with col2:
        st.markdown("### ⚔️ Участник 2")
        st.caption("Ключ: player2_2024")
        st.write(f"**Никнейм:** {p2.get('nickname', 'Не указан')}")
        st.write(f"**Готовность:** {'✅ Готов' if p2.get('ready') else '⏳ Ожидание'}")
        st.write(f"**Этап:** {get_stage_name(p2.get('stage', 'resources'))}")
        
        with st.expander("📋 Детальный статус"):
            st.write(f"Закупка: {'✅' if p2.get('finished_resources') else '⏳'}")
            st.write(f"Выбор оперативников: {'✅' if p2.get('finished_available') else '⏳'}")
            st.write(f"Защита: {'✅' if p2.get('finished_protection') else '⏳'}")
            st.write(f"Баны: {'✅' if p2.get('finished_bans') else '⏳'}")
            st.write(f"Пики: {'✅' if p2.get('finished_picks') else '⏳'}")
        
        available = p2.get("available_heroes", [])
        st.write(f"**Оперативников:** {len(available)}")
        protected = p2.get("protected_heroes", [])
        st.write(f"**Защищено:** {len(protected)}")
        banned = p2.get("bans", {}).get("opponent_bans", [])
        st.write(f"**Забанено:** {len(banned)}")
    
    st.divider()
    
    # Кнопки управления этапами
    col_advance, col_waiting, col_reset = st.columns(3)
    
    with col_advance:
        # Переход по этапам (resources -> available -> protection -> bans -> picks)
        if p1.get("ready") and p2.get("ready"):
            current_stage = p1.get("stage", "resources")
            
            can_advance = False
            if current_stage == "resources":
                can_advance = p1.get("finished_resources") and p2.get("finished_resources")
                next_stage = "available"
            elif current_stage == "available":
                can_advance = p1.get("finished_available") and p2.get("finished_available")
                next_stage = "protection"
            elif current_stage == "protection":
                can_advance = p1.get("finished_protection") and p2.get("finished_protection")
                next_stage = "bans"
            elif current_stage == "bans":
                can_advance = p1.get("finished_bans") and p2.get("finished_bans")
                next_stage = "picks"
            else:
                can_advance = False
                next_stage = current_stage
            
            if can_advance and next_stage != current_stage:
                if st.button(f"➡️ Перейти к этапу: {get_stage_name(next_stage)}", key="advance_btn", use_container_width=True, type="primary"):
                    p1["stage"] = next_stage
                    p2["stage"] = next_stage
                    
                    # Сбрасываем флаги для нового этапа
                    if next_stage == "available":
                        p1["finished_available"] = False
                        p2["finished_available"] = False
                    elif next_stage == "protection":
                        p1["finished_protection"] = False
                        p2["finished_protection"] = False
                    elif next_stage == "bans":
                        p1["finished_bans"] = False
                        p2["finished_bans"] = False
                    elif next_stage == "picks":
                        p1["finished_picks"] = False
                        p2["finished_picks"] = False
                    
                    st.session_state.p1 = p1
                    st.session_state.p2 = p2
                    save_player_data(1)
                    save_player_data(2)
                    save_judge_data()
                    
                    st.success(f"✅ Переход на {get_stage_name(next_stage)} выполнен!")
                    time.sleep(1)
                    st.rerun()
            else:
                st.info(f"⏳ {get_stage_name(current_stage)}...")
        else:
            st.info("⏳ Ожидание готовности...")
    
    with col_waiting:
        # Отправка в комнату ожидания (после пиков)
        if p1.get("finished_picks") and p2.get("finished_picks"):
            if p1.get("stage") != "waiting_room" and p2.get("stage") != "waiting_room":
                if st.button("🏨 В комнату ожидания", key="to_waiting", use_container_width=True, type="primary"):
                    p1["stage"] = "waiting_room"
                    p2["stage"] = "waiting_room"
                    st.session_state.p1 = p1
                    st.session_state.p2 = p2
                    save_player_data(1)
                    save_player_data(2)
                    save_judge_data()
                    st.success("✅ Участники в комнате ожидания!")
                    st.rerun()
            else:
                st.success("✅ Участники в комнате ожидания")
                
                # ========== ЗДЕСЬ КНОПКА НАЧАЛА БОЁВ ==========
                if st.button("⚔️ НАЧАТЬ БОИ", key="start_battle", use_container_width=True, type="primary"):
                    p1["stage"] = "battle"
                    p2["stage"] = "battle"
                    st.session_state.p1 = p1
                    st.session_state.p2 = p2
                    save_player_data(1)
                    save_player_data(2)
                    save_judge_data()
                    st.success("⚔️ БОИ НАЧАЛИСЬ! ⚔️")
                    st.balloons()
                    time.sleep(2)
                    st.rerun()
        else:
            st.info("⏳ Ожидание завершения пиков")
    
    with col_reset:
        if st.button("🔄 Сбросить всё", key="reset_all_btn", use_container_width=True):
            st.session_state.p1 = get_empty_participant_data()
            st.session_state.p2 = get_empty_participant_data()
            st.session_state.temp_selected_rooms = []
            save_player_data(1)
            save_player_data(2)
            save_judge_data()
            st.success("Турнир сброшен!")
            st.rerun()
    
    st.divider()
    
    # Информация о выбранных комнатах
    with st.expander("🏠 Выбранные комнаты", expanded=False):
        selected_rooms = get_selected_rooms()
        if selected_rooms:
            for idx, room in enumerate(selected_rooms, 1):
                st.write(f"{idx}. Комната {room}")
        else:
            st.info("Комнаты не выбраны")
    
    # Информация о ресурсах
    with st.expander("💰 Ресурсы участников", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**{p1.get('nickname', 'Участник 1')}**")
            resources = p1.get("resources", {})
            for name, count in resources.items():
                if count > 0:
                    st.write(f"{name}: {count}")
        with col2:
            st.markdown(f"**{p2.get('nickname', 'Участник 2')}**")
            resources = p2.get("resources", {})
            for name, count in resources.items():
                if count > 0:
                    st.write(f"{name}: {count}")
    
    # Информация о ключах
    with st.expander("ℹ️ Ключи доступа", expanded=False):
        st.markdown("""
        | Роль | Ключ |
        |------|------|
        | 🎮 Участник 1 | `player1_2024` |
        | 🎮 Участник 2 | `player2_2024` |
        | ⚖️ Судья | `judge_2024` |
        """)

def rooms_selection_only_interface():
    """Отдельный интерфейс для выбора комнат (без остального)"""
    
    st.markdown("# 🏠 Выбор комнат для турнира")
    st.markdown("### Выберите 3 комнаты, в которых будут проходить бои")
    st.caption("Порядок выбора = порядок использования комнат")
    
    # Инициализация
    if "temp_selected_rooms" not in st.session_state:
        st.session_state.temp_selected_rooms = []
    
    # Список всех комнат
    rooms = [
        "1-1", "1-2", "1-3",
        "2-1", "2-2", "2-3",
        "3-1", "3-2", "3-3",
        "4-1", "4-2", "4-3"
    ]
    
    # Статистика выбора
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Выбрано комнат", f"{len(st.session_state.temp_selected_rooms)} / 3")
    with col2:
        if st.button("🗑️ Очистить всё", key="clear_rooms", use_container_width=True):
            st.session_state.temp_selected_rooms = []
            st.rerun()
    with col3:
        if st.button("🎲 Случайный выбор", key="random_rooms", use_container_width=True):
            import random
            all_rooms = rooms.copy()
            random.shuffle(all_rooms)
            st.session_state.temp_selected_rooms = all_rooms[:3]
            st.rerun()
    
    st.divider()
    
    # Таблица кнопок 4x3
    st.markdown("### Нажмите на комнату для выбора:")
    
    for row in range(4):
        cols = st.columns(3)
        for col_idx in range(3):
            room_number = f"{row + 1}-{col_idx + 1}"
            with cols[col_idx]:
                is_selected = room_number in st.session_state.temp_selected_rooms
                
                if is_selected:
                    order = st.session_state.temp_selected_rooms.index(room_number) + 1
                    button_text = f"✅ Комната {room_number} (№{order})"
                    button_type = "primary"
                else:
                    button_text = f"⬜ Комната {room_number}"
                    button_type = "secondary"
                
                if st.button(button_text, key=f"room_{room_number}", use_container_width=True, type=button_type):
                    if is_selected:
                        st.session_state.temp_selected_rooms.remove(room_number)
                    else:
                        if len(st.session_state.temp_selected_rooms) < 3:
                            st.session_state.temp_selected_rooms.append(room_number)
                        else:
                            st.warning("⚠️ Нельзя выбрать больше 3 комнат!")
                    st.rerun()
    
    st.divider()
    
    # Отображение выбранных комнат в порядке очереди
    if st.session_state.temp_selected_rooms:
        st.markdown("### ✅ Выбранные комнаты (в порядке использования):")
        for idx, room in enumerate(st.session_state.temp_selected_rooms, 1):
            st.success(f"{idx}. Комната {room}")
    else:
        st.info("Комнаты не выбраны")
    
    st.divider()
    
    # Кнопки управления
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔙 Назад", key="back_to_judge", use_container_width=True):
            st.session_state.rooms_selection_mode = False
            st.rerun()
    
    with col2:
        if len(st.session_state.temp_selected_rooms) == 3:
            if st.button("✅ Подтвердить и продолжить", key="confirm_rooms", type="primary", use_container_width=True):
                # Сохраняем выбранные комнаты
                judge_state = {
                    "p1": st.session_state.p1,
                    "p2": st.session_state.p2,
                    "selected_rooms": st.session_state.temp_selected_rooms
                }
                with open(JUDGE_FILE, "w", encoding="utf-8") as f:
                    json.dump(judge_state, f, ensure_ascii=False, indent=2, default=str)
                
                st.success("✅ Комнаты выбраны и сохранены!")
                st.balloons()
                time.sleep(1)
                st.session_state.rooms_selection_mode = False
                st.rerun()
        else:
            st.button("✅ Подтвердить и продолжить", disabled=True, use_container_width=True)
            st.caption(f"⚠️ Нужно выбрать 3 комнаты (выбрано {len(st.session_state.temp_selected_rooms)})")


# ========== 10. ИНТЕРФЕЙС БОЯ ==========

def battle_interface():
    """Интерфейс этапа боя для судьи"""
    
    st.markdown("## ⚔️ ЭТАП БОЯ ⚔️")
    st.caption("Фиксация результатов реальных сражений в игре")
    
    # Загружаем данные
    load_judge_data()
    
    p1 = st.session_state.get("p1", {})
    p2 = st.session_state.get("p2", {})
    selected_rooms = get_selected_rooms()
    
    # Инициализация результатов боёв в session_state
    if "battle_results" not in st.session_state:
        st.session_state.battle_results = {}
        for i in range(3):
            st.session_state.battle_results[i] = {
                "winner": None,  # "p1", "p2", "draw"
                "restart_used_p1": False,
                "restart_used_p2": False
            }
    
    # Информация об участниках
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### ⚔️ {p1.get('nickname', 'Участник 1')}")
        # Отображение пачек участника 1
        picks_p1 = p1.get("picks", [[None for _ in range(4)] for _ in range(3)])
        for room_idx in range(3):
            if room_idx < len(selected_rooms):
                st.markdown(f"**Комната {selected_rooms[room_idx]}**")
            else:
                st.markdown(f"**Комната {room_idx + 1}**")
            pack = picks_p1[room_idx] if room_idx < len(picks_p1) else []
            if any(pack):
                hero_names = []
                for hero_id in pack:
                    if hero_id:
                        hero_info = p1.get("character_db", {}).get(hero_id, {})
                        hero_names.append(hero_info.get("name", "?"))
                st.write(" → ".join(hero_names))
            else:
                st.write("*пустая пачка*")
    
    with col2:
        st.markdown(f"### ⚔️ {p2.get('nickname', 'Участник 2')}")
        picks_p2 = p2.get("picks", [[None for _ in range(4)] for _ in range(3)])
        for room_idx in range(3):
            if room_idx < len(selected_rooms):
                st.markdown(f"**Комната {selected_rooms[room_idx]}**")
            else:
                st.markdown(f"**Комната {room_idx + 1}**")
            pack = picks_p2[room_idx] if room_idx < len(picks_p2) else []
            if any(pack):
                hero_names = []
                for hero_id in pack:
                    if hero_id:
                        hero_info = p2.get("character_db", {}).get(hero_id, {})
                        hero_names.append(hero_info.get("name", "?"))
                st.write(" → ".join(hero_names))
            else:
                st.write("*пустая пачка*")
    
    st.divider()
    
    # ========== ВВОД РЕЗУЛЬТАТОВ БОЁВ ==========
    st.markdown("### 📋 Результаты комнат")
    
    # Получаем ресурсы участников для проверки рестартов
    resources_p1 = p1.get("resources", {})
    resources_p2 = p2.get("resources", {})
    restart_p1 = resources_p1.get("🔄 Рестарт", 0)
    restart_p2 = resources_p2.get("🔄 Рестарт", 0)
    
    # Счёт побед
    score_p1 = 0
    score_p2 = 0
    
    for room_idx in range(3):
        room_name = selected_rooms[room_idx] if room_idx < len(selected_rooms) else f"Комната {room_idx + 1}"
        
        st.markdown(f"#### {room_name}")
        
        result = st.session_state.battle_results[room_idx]
        current_winner = result["winner"]
        
        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
        
        with col1:
            st.write("**Победитель:**")
            winner_options = {
                None: "— не выбран —",
                "p1": f"{p1.get('nickname', 'Участник 1')}",
                "p2": f"{p2.get('nickname', 'Участник 2')}",
                "draw": "Ничья"
            }
            selected_winner = st.selectbox(
                "Победитель",
                options=list(winner_options.keys()),
                format_func=lambda x: winner_options[x],
                key=f"winner_{room_idx}"
            )
            if selected_winner != current_winner:
                st.session_state.battle_results[room_idx]["winner"] = selected_winner
                st.rerun()
        
        with col2:
            if current_winner == "p1":
                st.success("🏆")
                score_p1 += 1
            elif current_winner == "p2":
                st.success("🏆")
                score_p2 += 1
            elif current_winner == "draw":
                st.info("🤝")
        
        with col3:
            # Рестарт для участника 1
            restart_used = result.get("restart_used_p1", False)
            if restart_used:
                st.success("✅ Рестарт использован")
            else:
                if restart_p1 > 0:
                    if st.button(f"🔄 Рестарт ({p1.get('nickname', 'Участник 1')})", key=f"restart_p1_{room_idx}"):
                        st.session_state.battle_results[room_idx]["restart_used_p1"] = True
                        # Сбрасываем победителя
                        st.session_state.battle_results[room_idx]["winner"] = None
                        # Уменьшаем ресурс рестарта в временных данных
                        st.session_state[f"temp_restart_update_p1"] = st.session_state.get(f"temp_restart_update_p1", 0) + 1
                        st.rerun()
                else:
                    st.button(f"❌ Нет рестарта", key=f"restart_p1_disabled_{room_idx}", disabled=True)
        
        with col4:
            # Рестарт для участника 2
            restart_used = result.get("restart_used_p2", False)
            if restart_used:
                st.success("✅ Рестарт использован")
            else:
                if restart_p2 > 0:
                    if st.button(f"🔄 Рестарт ({p2.get('nickname', 'Участник 2')})", key=f"restart_p2_{room_idx}"):
                        st.session_state.battle_results[room_idx]["restart_used_p2"] = True
                        st.session_state.battle_results[room_idx]["winner"] = None
                        st.session_state[f"temp_restart_update_p2"] = st.session_state.get(f"temp_restart_update_p2", 0) + 1
                        st.rerun()
                else:
                    st.button(f"❌ Нет рестарта", key=f"restart_p2_disabled_{room_idx}", disabled=True)
        
        with col5:
            # Кнопка сброса результата комнаты
            if st.button(f"🗑️ Сбросить", key=f"reset_room_{room_idx}"):
                st.session_state.battle_results[room_idx]["winner"] = None
                st.rerun()
        
        st.divider()
    
    # ========== ОТОБРАЖЕНИЕ СЧЁТА ==========
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(f"{p1.get('nickname', 'Участник 1')}", score_p1)
    with col2:
        st.metric(f"{p2.get('nickname', 'Участник 2')}", score_p2)
    with col3:
        if score_p1 > score_p2:
            st.metric("Счёт", f"{score_p1} : {score_p2}", delta="Ведёт Участник 1")
        elif score_p2 > score_p1:
            st.metric("Счёт", f"{score_p1} : {score_p2}", delta="Ведёт Участник 2")
        else:
            st.metric("Счёт", f"{score_p1} : {score_p2}", delta="Ничья")
    
    st.divider()
    
    # ========== КНОПКИ УПРАВЛЕНИЯ ==========
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Применяем использованные рестарты к данным участников
        temp_restart_p1 = st.session_state.get(f"temp_restart_update_p1", 0)
        temp_restart_p2 = st.session_state.get(f"temp_restart_update_p2", 0)
        
        if temp_restart_p1 > 0 or temp_restart_p2 > 0:
            if st.button("💾 Составить протокол рестартов", key="apply_restarts", use_container_width=True):
                # Обновляем ресурсы участников в файлах
                if temp_restart_p1 > 0:
                    new_restart_p1 = max(0, restart_p1 - temp_restart_p1)
                    p1["resources"]["🔄 Рестарт"] = new_restart_p1
                    st.session_state.p1 = p1
                    save_player_data(1)
                
                if temp_restart_p2 > 0:
                    new_restart_p2 = max(0, restart_p2 - temp_restart_p2)
                    p2["resources"]["🔄 Рестарт"] = new_restart_p2
                    st.session_state.p2 = p2
                    save_player_data(2)
                
                # Обновляем файл судьи
                save_judge_data()
                
                st.session_state[f"temp_restart_update_p1"] = 0
                st.session_state[f"temp_restart_update_p2"] = 0
                st.success("✅ Рестарты списаны!")
                st.rerun()
    
    with col2:
        if st.button("🏆 ЗАВЕРШИТЬ ТУРНИР", key="finish_tournament", use_container_width=True, type="primary"):
            # Проверяем, что все комнаты имеют результат
            all_rooms_set = all(
                st.session_state.battle_results[room_idx]["winner"] is not None 
                for room_idx in range(3)
            )
            
            if not all_rooms_set:
                st.error("❌ Укажите результаты всех трёх комнат!")
            else:
                # Объявляем победителя
                if score_p1 > score_p2:
                    winner = p1.get('nickname', 'Участник 1')
                    st.balloons()
                    st.success(f"🏆 ПОБЕДИТЕЛЬ ТУРНИРА: {winner}!!! 🏆")
                elif score_p2 > score_p1:
                    winner = p2.get('nickname', 'Участник 2')
                    st.balloons()
                    st.success(f"🏆 ПОБЕДИТЕЛЬ ТУРНИРА: {winner}!!! 🏆")
                else:
                    st.info("🤝 НИЧЬЯ В ТУРНИРЕ!")
                
                # Переводим участников на финальный этап
                p1["stage"] = "finished"
                p2["stage"] = "finished"
                st.session_state.p1 = p1
                st.session_state.p2 = p2
                save_player_data(1)
                save_player_data(2)
                save_judge_data()
                
                # Очищаем временные данные
                if "battle_results" in st.session_state:
                    del st.session_state.battle_results
                if "temp_restart_update_p1" in st.session_state:
                    del st.session_state.temp_restart_update_p1
                if "temp_restart_update_p2" in st.session_state:
                    del st.session_state.temp_restart_update_p2
                
                st.success("🏆 ТУРНИР ЗАВЕРШЁН! 🏆")
                time.sleep(3)
                st.rerun()
    
    with col3:
        if st.button("🔄 Сбросить все результаты", key="reset_all_results", use_container_width=True):
            for room_idx in range(3):
                st.session_state.battle_results[room_idx]["winner"] = None
            st.rerun()
    
    st.caption("💡 **Инструкция:** Выберите победителя для каждой комнаты. При необходимости используйте кнопки 'Рестарт' — они спишут ресурс у участника. После заполнения всех комнат нажмите 'Завершить турнир'.")

def get_stage_name(stage_key):
    """Возвращает русское название этапа"""
    stages = {
        "resources": "Закупка ресурсов",
        "available": "Выбор оперативников",
        "protection": "Защита",
        "bans": "Баны",
        "picks": "Пики",
        "finished": "Завершено"
    }
    return stages.get(stage_key, stage_key)


def get_next_stage(current_stage):
    """Возвращает следующий этап"""
    stages = ["resources", "available", "protection", "bans", "picks"]
    if current_stage in stages:
        idx = stages.index(current_stage)
        if idx + 1 < len(stages):
            return stages[idx + 1]
    return "finished"

# ========== 5. ГЛАВНЫЙ ИНТЕРФЕЙС ==========


def main():
    st.set_page_config(page_title="Arknights: Endfield", page_icon="⚔️", layout="wide")
    
    # Инициализация session_state
    if "p1" not in st.session_state:
        st.session_state.p1 = get_empty_participant_data()
    if "p2" not in st.session_state:
        st.session_state.p2 = get_empty_participant_data()
    if "auth_player1" not in st.session_state:
        st.session_state.auth_player1 = False
    if "auth_player2" not in st.session_state:
        st.session_state.auth_player2 = False
    if "auth_judge" not in st.session_state:
        st.session_state.auth_judge = False
    if "current_role" not in st.session_state:
        st.session_state.current_role = None
    
    # ФОРМА ВХОДА
    if not (st.session_state.auth_player1 or st.session_state.auth_player2 or st.session_state.auth_judge):
        st.title("⚔️ Arknights: Endfield")
        st.caption("Система банов и пиков оперативников")
        st.divider()
        
        st.markdown("### 🔐 Вход в систему")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### ⚔️ Участник 1")
            st.caption("Ключ: **player1_2024**")
            p1_pass = st.text_input("Ключ доступа", type="password", key="p1_login", placeholder="Введите ключ")
            if st.button("Войти как Участник 1", use_container_width=True):
                if p1_pass == "player1_2024":
                    st.session_state.auth_player1 = True
                    st.session_state.current_role = "player1"
                    load_my_data(1)  # Загружаем свои данные
                    st.rerun()
                else:
                    st.error("❌ Неверный ключ доступа!")
        
        with col2:
            st.markdown("#### ⚔️ Участник 2")
            st.caption("Ключ: **player2_2024**")
            p2_pass = st.text_input("Ключ доступа", type="password", key="p2_login", placeholder="Введите ключ")
            if st.button("Войти как Участник 2", use_container_width=True):
                if p2_pass == "player2_2024":
                    st.session_state.auth_player2 = True
                    st.session_state.current_role = "player2"
                    load_my_data(2)  # Загружаем свои данные
                    st.rerun()
                else:
                    st.error("❌ Неверный ключ доступа!")
        
        with col3:
            st.markdown("#### ⚖️ Судья")
            st.caption("Ключ: **judge_2024**")
            judge_pass = st.text_input("Ключ доступа", type="password", key="judge_login", placeholder="Введите ключ")
            if st.button("Войти как Судья", use_container_width=True):
                if judge_pass == "judge_2024":
                    st.session_state.auth_judge = True
                    st.session_state.current_role = "judge"
                    load_judge_data()  # Загружаем данные из файла судьи
                    st.rerun()
                else:
                    st.error("❌ Неверный ключ доступа!")
        
        st.divider()
        with st.expander("ℹ️ Информация о ключах доступа"):
            st.markdown("""
            **Ключи доступа для входа:**
            
            - 🎮 **Участник 1:** `player1_2024`
            - 🎮 **Участник 2:** `player2_2024`
            - ⚖️ **Судья:** `judge_2024`
            
            ⚠️ Каждый участник получает свой уникальный ключ!
            """)
        
        st.stop()
    
    # ========== ПОСЛЕ ВХОДА ==========
    # Скрываем боковую панель
    st.markdown("""
        <style>
            [data-testid="stSidebar"] { display: none; }
            [data-testid="stSidebarCollapsedControl"] { display: none; }
        </style>
    """, unsafe_allow_html=True)
    
    # Маршрутизация
    if st.session_state.current_role == "player1":
        participant_interface(1)
    elif st.session_state.current_role == "player2":
        participant_interface(2)
    elif st.session_state.current_role == "judge":
        judge_interface()
    
if __name__ == "__main__":
    main()