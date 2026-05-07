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
MAX_RESTART = 3  # Максимум Рестарта не более 2


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
    """Сохраняет данные судьи, включая комнаты и результаты банов"""
    
    # Загружаем старые данные, чтобы не потерять комнаты и баны
    old_selected_rooms = []
    old_ban_results = {}
    
    if os.path.exists(JUDGE_FILE):
        try:
            with open(JUDGE_FILE, "r", encoding="utf-8") as f:
                old_data = json.load(f)
                old_selected_rooms = old_data.get("selected_rooms", [])
                old_ban_results = old_data.get("ban_results", {})
        except:
            pass
    
    # Сохраняем всё вместе
    judge_state = {
        "p1": st.session_state.p1,
        "p2": st.session_state.p2,
        "selected_rooms": st.session_state.get("temp_selected_rooms", old_selected_rooms),
        "ban_results": st.session_state.get("ban_results", old_ban_results)
    }
    
    with open(JUDGE_FILE, "w", encoding="utf-8") as f:
        json.dump(judge_state, f, ensure_ascii=False, indent=2, default=str)
    
    return True

def load_judge_data():
    """Загружает данные из файла судьи"""
    if os.path.exists(JUDGE_FILE):
        try:
            with open(JUDGE_FILE, "r", encoding="utf-8") as f:
                judge_data = json.load(f)
                for key, value in judge_data.get("p1", {}).items():
                    st.session_state.p1[key] = value
                for key, value in judge_data.get("p2", {}).items():
                    st.session_state.p2[key] = value
                if "selected_rooms" in judge_data:
                    st.session_state.temp_selected_rooms = judge_data["selected_rooms"]
                if "ban_results" in judge_data:
                    st.session_state.ban_results = judge_data["ban_results"]
                return True
        except Exception as e:
            print(f"Ошибка загрузки judge_data.json: {e}")
    return False
    

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
        "purchase_history": {r: 0 for r in RESOURCES_DB},
        "free_resources_added": False,
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
                # Загружаем свежие данные из judge_data.json
                if os.path.exists(JUDGE_FILE):
                    try:
                        with open(JUDGE_FILE, "r", encoding="utf-8") as f:
                            judge_data = json.load(f)
                            if player_num == 1:
                                for key, value in judge_data.get("p1", {}).items():
                                    st.session_state.p1[key] = value
                                for key, value in judge_data.get("p2", {}).items():
                                    st.session_state.p2[key] = value
                            else:
                                for key, value in judge_data.get("p2", {}).items():
                                    st.session_state.p2[key] = value
                                for key, value in judge_data.get("p1", {}).items():
                                    st.session_state.p1[key] = value
                            if "selected_rooms" in judge_data:
                                st.session_state.temp_selected_rooms = judge_data["selected_rooms"]
                            if "ban_results" in judge_data:
                                st.session_state.ban_results = judge_data["ban_results"]
                    except:
                        pass
                
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
            # Загружаем свежие данные из judge_data.json
            if os.path.exists(JUDGE_FILE):
                try:
                    with open(JUDGE_FILE, "r", encoding="utf-8") as f:
                        judge_data = json.load(f)
                        if player_num == 1:
                            for key, value in judge_data.get("p1", {}).items():
                                st.session_state.p1[key] = value
                            for key, value in judge_data.get("p2", {}).items():
                                st.session_state.p2[key] = value
                        else:
                            for key, value in judge_data.get("p2", {}).items():
                                st.session_state.p2[key] = value
                            for key, value in judge_data.get("p1", {}).items():
                                st.session_state.p1[key] = value
                        if "selected_rooms" in judge_data:
                            st.session_state.temp_selected_rooms = judge_data["selected_rooms"]
                        if "ban_results" in judge_data:
                            st.session_state.ban_results = judge_data["ban_results"]
                except:
                    pass
            
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
                # Загружаем свежие данные из judge_data.json
                if os.path.exists(JUDGE_FILE):
                    try:
                        with open(JUDGE_FILE, "r", encoding="utf-8") as f:
                            judge_data = json.load(f)
                            if player_num == 1:
                                for key, value in judge_data.get("p1", {}).items():
                                    st.session_state.p1[key] = value
                                for key, value in judge_data.get("p2", {}).items():
                                    st.session_state.p2[key] = value
                            else:
                                for key, value in judge_data.get("p2", {}).items():
                                    st.session_state.p2[key] = value
                                for key, value in judge_data.get("p1", {}).items():
                                    st.session_state.p1[key] = value
                            if "selected_rooms" in judge_data:
                                st.session_state.temp_selected_rooms = judge_data["selected_rooms"]
                            if "ban_results" in judge_data:
                                st.session_state.ban_results = judge_data["ban_results"]
                    except:
                        pass
                
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
                # Загружаем свежие данные из judge_data.json
                if os.path.exists(JUDGE_FILE):
                    try:
                        with open(JUDGE_FILE, "r", encoding="utf-8") as f:
                            judge_data = json.load(f)
                            if player_num == 1:
                                for key, value in judge_data.get("p1", {}).items():
                                    st.session_state.p1[key] = value
                                for key, value in judge_data.get("p2", {}).items():
                                    st.session_state.p2[key] = value
                            else:
                                for key, value in judge_data.get("p2", {}).items():
                                    st.session_state.p2[key] = value
                                for key, value in judge_data.get("p1", {}).items():
                                    st.session_state.p1[key] = value
                            if "selected_rooms" in judge_data:
                                st.session_state.temp_selected_rooms = judge_data["selected_rooms"]
                            if "ban_results" in judge_data:
                                st.session_state.ban_results = judge_data["ban_results"]
                    except:
                        pass
                
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
                # Загружаем свежие данные из judge_data.json
                if os.path.exists(JUDGE_FILE):
                    try:
                        with open(JUDGE_FILE, "r", encoding="utf-8") as f:
                            judge_data = json.load(f)
                            if player_num == 1:
                                for key, value in judge_data.get("p1", {}).items():
                                    st.session_state.p1[key] = value
                                for key, value in judge_data.get("p2", {}).items():
                                    st.session_state.p2[key] = value
                            else:
                                for key, value in judge_data.get("p2", {}).items():
                                    st.session_state.p2[key] = value
                                for key, value in judge_data.get("p1", {}).items():
                                    st.session_state.p1[key] = value
                            if "selected_rooms" in judge_data:
                                st.session_state.temp_selected_rooms = judge_data["selected_rooms"]
                            if "ban_results" in judge_data:
                                st.session_state.ban_results = judge_data["ban_results"]
                    except:
                        pass
                
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
                # Загружаем свежие данные из judge_data.json
                if os.path.exists(JUDGE_FILE):
                    try:
                        with open(JUDGE_FILE, "r", encoding="utf-8") as f:
                            judge_data = json.load(f)
                            if player_num == 1:
                                for key, value in judge_data.get("p1", {}).items():
                                    st.session_state.p1[key] = value
                                for key, value in judge_data.get("p2", {}).items():
                                    st.session_state.p2[key] = value
                            else:
                                for key, value in judge_data.get("p2", {}).items():
                                    st.session_state.p2[key] = value
                                for key, value in judge_data.get("p1", {}).items():
                                    st.session_state.p1[key] = value
                            if "selected_rooms" in judge_data:
                                st.session_state.temp_selected_rooms = judge_data["selected_rooms"]
                            if "ban_results" in judge_data:
                                st.session_state.ban_results = judge_data["ban_results"]
                    except:
                        pass
                
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
                # Загружаем свежие данные из judge_data.json
                if os.path.exists(JUDGE_FILE):
                    try:
                        with open(JUDGE_FILE, "r", encoding="utf-8") as f:
                            judge_data = json.load(f)
                            if player_num == 1:
                                for key, value in judge_data.get("p1", {}).items():
                                    st.session_state.p1[key] = value
                                for key, value in judge_data.get("p2", {}).items():
                                    st.session_state.p2[key] = value
                            else:
                                for key, value in judge_data.get("p2", {}).items():
                                    st.session_state.p2[key] = value
                                for key, value in judge_data.get("p1", {}).items():
                                    st.session_state.p1[key] = value
                            if "selected_rooms" in judge_data:
                                st.session_state.temp_selected_rooms = judge_data["selected_rooms"]
                            if "ban_results" in judge_data:
                                st.session_state.ban_results = judge_data["ban_results"]
                    except:
                        pass
                
                load_my_data(player_num)
                load_opponent_data(player_num)
                st.rerun()
    
    elif current_stage == "waiting_room":
        waiting_room_interface(player_num)
    
    elif current_stage == "battle":
        st.success("🏆 ПОЗДРАВЛЯЮ! Все этапы пройдены!")
        st.info("⚔️ Ожидайте начала боев от Судьи.")
        
        if st.button("🔄 Проверить статус", key=f"check_status_battle_{player_num}"):
            if os.path.exists(JUDGE_FILE):
                try:
                    with open(JUDGE_FILE, "r", encoding="utf-8") as f:
                        judge_data = json.load(f)
                        if player_num == 1:
                            for key, value in judge_data.get("p1", {}).items():
                                st.session_state.p1[key] = value
                            for key, value in judge_data.get("p2", {}).items():
                                st.session_state.p2[key] = value
                        else:
                            for key, value in judge_data.get("p2", {}).items():
                                st.session_state.p2[key] = value
                            for key, value in judge_data.get("p1", {}).items():
                                st.session_state.p1[key] = value
                except:
                    pass
            load_my_data(player_num)
            load_opponent_data(player_num)
            st.rerun()
    
    elif current_stage == "finished":
        st.success("🏆 ПОЗДРАВЛЯЮ! Турнир завершен!")

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
                # Добавляем базовую комплектацию (только один раз)
                if not data.get("free_resources_added", False):
                    current_resources["🔄 Рестарт"] = current_resources.get("🔄 Рестарт", 0) + 1
                    current_resources["🔴 Универсальный бан"] = current_resources.get("🔴 Универсальный бан", 0) + 1
                    data["free_resources_added"] = True
                    data["purchase_history"] = current_resources.copy()
                    st.info("🎁 Добавлены бесплатные ресурсы: 🔄 Рестарт x1, 🔴 Универсальный бан x1")
                
                data["resources"] = current_resources
                data["finished_resources"] = True
                
                if player_num == 1:
                    st.session_state.p1 = data
                else:
                    st.session_state.p2 = data
                
                save_player_data(player_num)
                st.success("✅ Этап закупки пропущен! Бесплатные ресурсы добавлены.")
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
                    
                    # Добавляем базовую комплектацию (только один раз)
                    if not data.get("free_resources_added", False):
                        current_resources["🔄 Рестарт"] = current_resources.get("🔄 Рестарт", 0) + 1
                        current_resources["🔴 Универсальный бан"] = current_resources.get("🔴 Универсальный бан", 0) + 1
                        data["free_resources_added"] = True
                        data["purchase_history"] = current_resources.copy()
                        st.info("🎁 Добавлены бесплатные ресурсы: 🔄 Рестарт x1, 🔴 Универсальный бан x1")
                    
                    data["points"] = remaining_points
                    data["resources"] = current_resources
                    data["finished_resources"] = True
                    
                    if player_num == 1:
                        st.session_state.p1 = data
                    else:
                        st.session_state.p2 = data
                    
                    save_player_data(player_num)
                    st.success("✅ Закупка успешно завершена!")
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
            
            if char_info["rarity"] in ["5⭐", "4⭐"]:
                default_potential = 5
            else:
                default_potential = 0
            
            modified_db[char_id] = {
                "name": char_info["name"],
                "rarity": char_info["rarity"],
                "full_name": char_info["full_name"],
                "image_path": f"Operators/{image_name}",  # Путь к изображению в папке Operators
                "has_operator": True,  # ПО УМОЛЧАНИЮ ВСЕ ОПЕРАТИВНИКИ В НАЛИЧИИ
                "level": 90,  # Уровень по умолчанию
                "potential": default_potential,  # Потенциал по умолчанию
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
                # Устанавливаем потенциал по умолчанию в зависимости от редкости
                if char_info["rarity"] == "6⭐":
                    default_potential = char_info.get("potential", 0)
                else:  # 5⭐ и 4⭐
                    default_potential = char_info.get("potential", 5)

                potential = st.number_input(
                    "Потенциал",
                    min_value=0,
                    max_value=5,
                    value=default_potential,
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
    st.info("💡 По умолчанию все оперативники отмечены как 'В наличии'. Снимите галочку, если оперативника нет на аккаунте.")
    st.warning("Внимание: заполнение этого этапа лежит на вашей совести. При несоответсвии данных заполненных тут с реальным положением дел, вам будет присвоено техническое поражение (но сейчас только за наличие/отсутсвие оперативника)")

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
    
    st.caption("ℹ️ Вы можете отметить любое количество оперативников - это просто список того, что есть на вашем аккаунте.")
    st.divider()
    
    # Создаем вкладки для разных редкостей
    tab1, tab2, tab3 = st.tabs(["6⭐ Герои", "5⭐ Герои", "4⭐ Герои"])
    
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
    

    # Получаем ресурсы участника
    resources = data.get("resources", {})
    universal_protection = resources.get("🛡️ Универсальная защита", 0)
    five_star_protection = resources.get("🔵 Защита 5⭐", 0)
    
    # ========== ПОЛНАЯ ИНФОРМАЦИЯ О ЗАКУПКАХ ==========
    st.markdown("### 📊 Список ресурсов у участников")
    
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
        history = data.get("purchase_history", {})
        for name, count in history.items():
            if count > 0:
                st.write(f"{name}: {count}")
    with col2:
        st.markdown(f"**{opponent_data.get('nickname', 'Участник 2')}**")
        history = opponent_data.get("purchase_history", {})
        for name, count in history.items():
            if count > 0:
                st.write(f"{name}: {count}")
    
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
    if universal_protection == 0 and five_star_protection == 0:
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
        st.session_state[f"universal_temp_{player_num}"] = universal_protection
    if f"five_star_temp_{player_num}" not in st.session_state:
        st.session_state[f"five_star_temp_{player_num}"] = five_star_protection
    
    protected_heroes = st.session_state[f"protected_temp_{player_num}"]
    remaining_universal = st.session_state[f"universal_temp_{player_num}"]
    remaining_five_star = st.session_state[f"five_star_temp_{player_num}"]
    
    # Создаем вкладки
    tab1, tab2 = st.tabs(["⭐ 6⭐ Оперативники", "⭐⭐ 5-4⭐ Оперативники"])
    
    # Вкладка 6⭐ - проверяем НЕ остаток, а БЫЛ ЛИ КУПЛЕН ресурс
    with tab1:
        # Проверяем, покупал ли участник универсальную защиту (по начальному значению)
        if universal_protection == 0:
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
            used_five_star = min(protected_other_count, five_star_protection)
            # Сколько универсальных защит использовано на 5-4⭐
            used_universal_on_other = max(0, protected_other_count - five_star_protection)
            
            # Остаток ресурсов
            remaining_five_star = five_star_protection - used_five_star
            remaining_universal = universal_protection - used_universal_on_six - used_universal_on_other
            
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
                                    if len(protected_other_ids) > five_star_protection:
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
            time.sleep(1)
            st.rerun()
    
    with col_btn2:
        if st.button("🔄 Сбросить все защиты", key=f"reset_{player_num}", use_container_width=True):
            st.session_state[f"protected_temp_{player_num}"] = []
            st.session_state[f"universal_temp_{player_num}"] = universal_protection
            st.session_state[f"five_star_temp_{player_num}"] = five_star_protection
            st.rerun()

# ========== 6. ИНТЕРФЕЙС БАНА  ==========

def ban_interface(player_num):
    """Интерфейс банов оперативников противника"""
    
    # Загружаем свои данные
    load_my_data(player_num)
    load_opponent_data(player_num)
    
    if player_num == 1:
        data = st.session_state.p1
        opponent_data = st.session_state.p2
    else:
        data = st.session_state.p2
        opponent_data = st.session_state.p1
    
    st.markdown("## 🔨 Этап банов оперативников")
    st.markdown(f"Вы баните оперативников **{opponent_data.get('nickname', 'Противника')}**")
    st.divider()
    # ========== ПОЛНАЯ ИНФОРМАЦИЯ О ЗАКУПКАХ ==========
    st.markdown("### 📊 Список ресурсов у участников")
    
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
        history = data.get("purchase_history", {})
        for name, count in history.items():
            if count > 0:
                st.write(f"{name}: {count}")
    with col2:
        st.markdown(f"**{opponent_data.get('nickname', 'Участник 2')}**")
        history = opponent_data.get("purchase_history", {})
        for name, count in history.items():
            if count > 0:
                st.write(f"{name}: {count}")
    
    st.divider()

    # ========== ИНФОРМАЦИЯ О ВЫБРАННЫХ КОМНАТАХ ==========
    selected_rooms = get_selected_rooms()
    if selected_rooms:
        st.markdown("### 🏟️ Информация о турнире")
        st.markdown("**Судья подобрал для вас следующие комнаты:**")
        for idx, room in enumerate(selected_rooms, 1):
            st.markdown(f"**Комната {room}**")
        st.divider()
    
    # Получаем ресурсы для банов
    resources = data.get("resources", {})
    universal_ban_count = resources.get("🔴 Универсальный бан", 0)
    five_star_ban_count = resources.get("🔵 Бан 4-5⭐", 0)
    
    # Защита (своя и противника)
    my_protected = data.get("protected_heroes", [])
    opponent_protected = opponent_data.get("protected_heroes", [])
    
    # Получаем доступных оперативников противника
    opponent_character_db = opponent_data.get("character_db", {})
    opponent_available = []
    for char_id, char_info in opponent_character_db.items():
        if char_info.get("has_operator", False):
            opponent_available.append(char_id)
    
    if not opponent_available:
        st.warning("⚠️ У противника нет доступных оперативников!")
        if st.button("✅ Завершить этап банов", key=f"finish_bans_empty_{player_num}"):
            data["finished_bans"] = True
            data["bans"] = {}
            save_player_data(player_num)
            st.rerun()
        return
    
    if universal_ban_count == 0 and five_star_ban_count == 0:
        st.info("ℹ️ У вас нет ресурсов для банов.")
        if st.button("✅ Завершить этап банов", key=f"finish_bans_no_resources_{player_num}"):
            data["finished_bans"] = True
            data["bans"] = {}
            save_player_data(player_num)
            st.rerun()
        return
    
    # Временное хранилище
    temp_key = f"temp_bans_{player_num}"
    if temp_key not in st.session_state:
        existing = data.get("bans", {})
        st.session_state[temp_key] = existing.copy() if existing else {}
    
    current_bans = st.session_state[temp_key]
    
    # Функции-помощники
    def get_hero_rarity_from_id(hero_id):
        char_info = opponent_character_db.get(hero_id, {})
        return char_info.get("rarity", "4⭐")
    
    # Подсчёт ресурсов
    def get_usage_stats(bans_dict):
        total_bans = sum(bans_dict.values())
        bans_on_6star = sum(count for hid, count in bans_dict.items() if get_hero_rarity_from_id(hid) == "6⭐")
        
        universal_used = bans_on_6star
        remaining_universal = universal_ban_count - universal_used
        five_used = 0
        remaining_universal_temp = remaining_universal
        
        for hid, count in bans_dict.items():
            if get_hero_rarity_from_id(hid) != "6⭐":
                if five_star_ban_count - five_used > 0:
                    take = min(count, five_star_ban_count - five_used)
                    five_used += take
                    remaining = count - take
                    if remaining > 0 and remaining_universal_temp > 0:
                        take_univ = min(remaining, remaining_universal_temp)
                        remaining_universal_temp -= take_univ
                else:
                    if remaining_universal_temp > 0:
                        take_univ = min(count, remaining_universal_temp)
                        remaining_universal_temp -= take_univ
        
        universal_used_total = universal_ban_count - remaining_universal_temp
        return universal_used_total, five_used, total_bans
    
    def get_remaining(bans_dict):
        univ_used, five_used, _ = get_usage_stats(bans_dict)
        return {
            'univ': universal_ban_count - univ_used,
            'five': five_star_ban_count - five_used,
            'total': (universal_ban_count + five_star_ban_count) - sum(bans_dict.values())
        }
    
    def can_add_ban(hero_id, bans_dict, additional=1):
        hero_rarity = get_hero_rarity_from_id(hero_id)
        current_count = bans_dict.get(hero_id, 0)
        new_count = current_count + additional
        
        if new_count > 2:
            return False
        
        remaining = get_remaining(bans_dict)
        if remaining['total'] < additional:
            return False
        
        if hero_rarity == "6⭐":
            return remaining['univ'] >= additional
        else:
            return remaining['five'] > 0 or remaining['univ'] > 0
    
    def get_protection_type(hero_id):
        is_my = hero_id in my_protected
        is_opp = hero_id in opponent_protected
        
        if is_my and is_opp:
            return "both"
        elif is_opp:
            return "opponent"
        elif is_my:
            return "mine_only"
        else:
            return "none"
    
    # Получаем остаток ресурсов для уведомлений
    remaining = get_remaining(current_bans)
    
    st.divider()
    
    # Разделяем оперативников (с полной информацией)
    heroes_6star = []
    heroes_other = []
    
    for hero_id in opponent_available:
        char_info = opponent_character_db.get(hero_id, {})
        if char_info.get("rarity") == "6⭐":
            heroes_6star.append((hero_id, char_info))
        else:
            heroes_other.append((hero_id, char_info))
    
    # Функция отображения сетки
    def render_hero_grid(heroes_list, hero_type):
        if not heroes_list:
            return
        
        items_per_row = 7
        for i in range(0, len(heroes_list), items_per_row):
            row = heroes_list[i:i + items_per_row]
            cols = st.columns(len(row))
            
            for idx, (hero_id, char_info) in enumerate(row):
                with cols[idx]:
                    with st.container(border=True):
                        hero_name = char_info.get("name", "???")
                        hero_rarity = char_info.get("rarity", "4⭐")
                        img_path = load_operator_image(hero_name)
                        current_count = current_bans.get(hero_id, 0)
                        protection = get_protection_type(hero_id)
                        
                        if img_path:
                            st.image(img_path, width=80)
                        else:
                            st.write("🎴")
                        
                        st.markdown(f"**{hero_name}**")
                        
                        # Подпись: уровень, потенциал, ранг
                        rank = 6 if hero_rarity == "6⭐" else (5 if hero_rarity == "5⭐" else 4)
                        st.caption(f"Lv.{char_info.get('level', 90)} | П{char_info.get('potential', 0)} | {rank}")
                        
                        if protection == "both":
                            st.warning("🛡️🔰 Защищён обоими")
                        elif protection == "opponent":
                            st.info("🛡️ Защищён противником")
                        elif protection == "mine_only":
                            st.info("🔰 Защищён мною")
                        
                        show_second = (protection == "opponent") or (protection == "both")
                        
                        # Первый чекбокс
                        if current_count >= 1:
                            if current_count >= 2:
                                ban1_disabled = True
                            else:
                                ban1_disabled = False
                        else:
                            ban1_disabled = not can_add_ban(hero_id, current_bans, 1)
                        
                        ban1 = st.checkbox(
                            "🔫 Застрелить", 
                            value=(current_count >= 1), 
                            key=f"ban1_{hero_type}_{i}_{idx}_{hero_id}",
                            disabled=ban1_disabled
                        )
                        
                        if show_second:
                            if current_count >= 2:
                                ban2_disabled = False
                            elif current_count == 1:
                                ban2_disabled = not can_add_ban(hero_id, current_bans, 1)
                            else:
                                ban2_disabled = True
                            
                            ban2 = st.checkbox(
                                "💀 Контрольный", 
                                value=(current_count >= 2), 
                                key=f"ban2_{hero_type}_{i}_{idx}_{hero_id}",
                                disabled=ban2_disabled
                            )
                            new_count = (1 if ban1 else 0) + (1 if ban2 else 0)
                        else:
                            new_count = 1 if ban1 else 0
                        
                        if new_count != current_count:
                            if new_count == 0:
                                if hero_id in current_bans:
                                    del current_bans[hero_id]
                            else:
                                current_bans[hero_id] = new_count
                            st.rerun()
    
    # Вкладки
    tab1, tab2 = st.tabs(["6⭐ Оперативники противника", "5-4⭐ Оперативники противника"])
    
    with tab1:
        if universal_ban_count == 0:
            st.warning("🔒 Вы не покупали 🔴 Универсальный бан. Бан 6⭐ оперативников недоступен.")
        elif not heroes_6star:
            st.info("У противника нет 6⭐ оперативников.")
        else:
            remaining_univ = remaining['univ']
            
            if remaining_univ <= 0:
                st.warning("⚠️ У вас закончились универсальные баны! Вы можете снимать баны, но новые поставить нельзя.")
            else:
                st.info(f"🔴 Осталось универсальных банов: {remaining_univ}")
            
            render_hero_grid(heroes_6star, "6")
    
    with tab2:
        if not heroes_other:
            st.info("У противника нет 5⭐ или 4⭐ оперативников.")
        else:
            remaining_five_val = remaining['five']
            remaining_univ_val = remaining['univ']
            
            if remaining_five_val == 0 and remaining_univ_val == 0:
                st.error("❌ У вас закончились все баны! Подтвердите текущий выбор или сбросьте его.")
            elif remaining_five_val == 0 and remaining_univ_val > 0:
                st.warning(f"⚠️ У вас закончились баны 5⭐! Будет использован универсальный бан (осталось: {remaining_univ_val})")
            else:
                total_bans_left = remaining_five_val + remaining_univ_val
                st.info(f"📊 **Доступно банов:** {total_bans_left} (🔵 {remaining_five_val} + 🔄 {remaining_univ_val})")
            
            render_hero_grid(heroes_other, "other")
    
    # Итоговая статистика
    final_bans = st.session_state[temp_key]
    final_univ, final_five, final_total = get_usage_stats(final_bans)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("✅ Универсальный бан", f"{final_univ} / {universal_ban_count}")
    with col2:
        st.metric("✅ Бан 5⭐", f"{final_five} / {five_star_ban_count}")
    with col3:
        st.metric("✅ Всего банов", f"{final_total} / {universal_ban_count + five_star_ban_count}")
    
    if final_bans:
        with st.expander("📋 Выбранные оперативники для бана"):
            for hid, count in final_bans.items():
                hero_name = opponent_character_db.get(hid, {}).get("name", "???")
                st.write(f"- {hero_name}: {count} бан(а)")
    
    # Проверка ошибок
    has_error = False
    if final_univ > universal_ban_count:
        st.error("❌ Превышен лимит универсальных банов!")
        has_error = True
    if final_five > five_star_ban_count:
        st.error("❌ Превышен лимит банов 5⭐!")
        has_error = True
    
    st.divider()
    
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("🗑️ ОЧИСТИТЬ ВСЁ", key=f"clear_bans_{player_num}", use_container_width=True):
            st.session_state[temp_key] = {}
            st.rerun()
    
    with col_btn2:
        if st.button("✅ ПОДТВЕРДИТЬ БАНЫ", key=f"confirm_bans_{player_num}", type="primary", use_container_width=True, disabled=has_error):
            data["bans"] = final_bans.copy()
            data["finished_bans"] = True
            save_player_data(player_num)
            del st.session_state[temp_key]
            st.success(f"✅ Баны подтверждены! Всего банов: {final_total}")
            time.sleep(1)
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
    
    # ========== ИНФОРМАЦИЯ О ВЫБРАННЫХ КОМНАТАХ ==========
    selected_rooms = get_selected_rooms()
    if selected_rooms:
        st.markdown("### 🏟️ Информация о турнире")
        st.markdown("**Судья подобрал для вас следующие комнаты:**")
        for idx, room in enumerate(selected_rooms, 1):
            st.markdown(f"**Комната {room}**")
        st.divider()
    
    # Получаем ресурсы воскрешений
    resources = data.get("resources", {})
    universal_resurrection = resources.get("🔴 Универсальное воскрешение", 0)
    five_star_resurrection = resources.get("🔵 Воскрешение 5⭐", 0)
    total_resurrections = universal_resurrection + five_star_resurrection
    

    # ========== СТАТИСТИКА БАНОВ ==========
    st.markdown("### 📋 Забаненные для меня оперативники")
    
    # Загружаем исходные данные банов из файла судьи
    p1_bans = {}
    p2_bans = {}
    p1_protected = []
    p2_protected = []
    
    if os.path.exists(JUDGE_FILE):
        try:
            with open(JUDGE_FILE, "r", encoding="utf-8") as f:
                judge_data = json.load(f)
                p1_bans = judge_data.get("p1", {}).get("bans", {})
                p2_bans = judge_data.get("p2", {}).get("bans", {})
                p1_protected = judge_data.get("p1", {}).get("protected_heroes", [])
                p2_protected = judge_data.get("p2", {}).get("protected_heroes", [])
        except:
            pass
    
    # Собираем всех оперативников участника
    character_db = data.get("character_db", {})
    
    banned_by_me = []      # 1 категория: только я забанил (и мне недоступен)
    banned_by_both = []    # 2 категория: забанили оба (и мне недоступен)
    banned_by_opponent = [] # 3 категория: только противник забанил (и мне недоступен)
    
    for hero_id, char_info in character_db.items():
        if not char_info.get("has_operator", False):
            continue
        
        hero_name = char_info.get("name", "???")
        
        # Получаем количество банов от каждого участника
        if player_num == 1:
            my_ban_count = p1_bans.get(str(hero_id), 0)
            opp_ban_count = p2_bans.get(str(hero_id), 0)
            my_protected = 1 if hero_id in p1_protected else 0
        else:
            my_ban_count = p2_bans.get(str(hero_id), 0)
            opp_ban_count = p1_bans.get(str(hero_id), 0)
            my_protected = 1 if hero_id in p2_protected else 0
        
        total_bans = my_ban_count + opp_ban_count
        is_available = (total_bans - my_protected) <= 0
        
        # Если оперативник НЕ доступен мне
        if not is_available:
            if my_ban_count > 0 and opp_ban_count == 0:
                banned_by_me.append(hero_name)
            elif my_ban_count > 0 and opp_ban_count > 0:
                banned_by_both.append(hero_name)
            elif my_ban_count == 0 and opp_ban_count > 0:
                banned_by_opponent.append(hero_name)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🔴 Забанены мною**")
        if banned_by_me:
            for name in banned_by_me:
                st.write(f"- {name}")
        else:
            st.caption("— нет —")
    
    with col2:
        st.markdown("**🟣 Забанены единогласно**")
        if banned_by_both:
            for name in banned_by_both:
                st.write(f"- {name}")
        else:
            st.caption("— нет —")
    
    with col3:
        st.markdown("**🔵 Забанены противником**")
        if banned_by_opponent:
            for name in banned_by_opponent:
                st.write(f"- {name}")
        else:
            st.caption("— нет —")
    
    st.divider()
    
    # ========== СТАТИСТИКА ВОСКРЕШЕНИЙ ==========
    st.markdown("### 🔄 Ресурсы воскрешений")
    
    # Получаем запрещённых оперативников (баны от противника)
    opponent_bans = opponent_data.get("bans", {}).get("opponent_bans", [])
    
    # Получаем результаты банов для доступности
    ban_results_loaded = {}
    if os.path.exists(JUDGE_FILE):
        try:
            with open(JUDGE_FILE, "r", encoding="utf-8") as f:
                judge_data = json.load(f)
                ban_results_loaded = judge_data.get("ban_results", {})
        except:
            pass
    
    p1_ban_results = ban_results_loaded.get("p1", {})
    p2_ban_results = ban_results_loaded.get("p2", {})
    
    if player_num == 1:
        my_ban_results = p1_ban_results
    else:
        my_ban_results = p2_ban_results

    # Получаем список доступных оперативников
    available_heroes = []
    for char_id, char_info in character_db.items():
        if char_info.get("has_operator", False) and char_id not in opponent_bans:
            is_available = my_ban_results.get(str(char_id), True)
            if not is_available:
                continue
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
    

    # Отображение статистики лимитов
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🔴 Универсальное", universal_resurrection)
    with col2:
        st.metric("🔵 Воскрешение 5⭐", five_star_resurrection)
    with col3:
        if repeats_six > six_limit:
            st.metric("Воскрешено 6⭐", f"{repeats_six}/{six_limit}", delta="!❌!", delta_color="inverse")
        else:
            st.metric("Воскрешено 6⭐", f"{repeats_six}/{six_limit}", delta=f"осталось {remaining_six}")
    with col4:
        if repeats_total > five_limit:
            st.metric("Воскрешено всего", f"{repeats_total}/{five_limit}", delta="!❌!", delta_color="inverse")
        else:
            st.metric("Воскрешено всего", f"{repeats_total}/{five_limit}", delta=f"осталось {remaining_total}")
    
    st.divider()
    
    # ========== ОСНОВНОЙ ИНТЕРФЕЙС ==========
    left_col, right_col = st.columns([0.65, 0.35])
    
    # ========== ЛЕВАЯ ЧАСТЬ: СПИСОК ОПЕРАТИВНИКОВ ==========
    with left_col:
        st.markdown("### 📋 Оперативники")
        
        if selected_pack is not None:
            st.success(f"✅ Пачка {selected_pack + 1} выбрана")
        else:
            st.warning("⚠️ Сначала выберите пачку")
        
        if not available_heroes:
            st.error("❌ Нет доступных оперативников для выбора!")
        else:
            items_per_row = 8
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
                            
                            rank = 6 if char_info["rarity"] == "6⭐" else (5 if char_info["rarity"] == "5⭐" else 4)
                            st.markdown(f"**{char_info['name']}**")
                            st.caption(f"Lv.{char_info['level']} | П{char_info['potential']} | {rank}")
                            
                            count = usage_count.get(char_id, 0)
                                                        
                            # Проверка возможности добавления
                            can_add = True
                            reason = ""
                            
                            if selected_pack is not None:
                                is_duplicate = char_id in picks[selected_pack]
                                if is_duplicate:
                                    can_add = False
                                else:
                                    count = usage_count.get(char_id, 0)
                                                                                                           
                                    # Расчёты
                                    total_duplicates = repeats_total
                                    total_resurrections = universal_resurrection + five_star_resurrection
                                    
                                    # Общее условие (для любых дубликатов)
                                    can_add_duplicate = (total_resurrections - total_duplicates) >= 1
                                    
                                    # Дополнительное условие для 6⭐
                                    can_add_six = (universal_resurrection - repeats_six) >= 1
                                    
                                    if char_info["rarity"] == "4⭐":
                                        can_add = True
                                    
                                    elif char_info["rarity"] == "6⭐":
                                        if count == 0:
                                            can_add = True
                                        else:
                                            # Дубликат 6⭐ требует выполнения ОБОИХ условий
                                            if can_add_duplicate and can_add_six:
                                                can_add = True
                                            else:
                                                can_add = False
                                    
                                    elif char_info["rarity"] == "5⭐":
                                        if count == 0:
                                            can_add = True
                                        else:
                                            # Дубликат 5⭐ требует только общего условия
                                            if can_add_duplicate:
                                                can_add = True
                                            else:
                                                can_add = False

                            if selected_pack is not None:
                                is_duplicate = char_id in picks[selected_pack]
                                if is_duplicate:
                                    st.button(f"❌", key=f"hero_dup_{char_id}_{player_num}_{i}_{idx}", disabled=True, use_container_width=True)
                                elif not can_add:
                                    st.button(f"🚫", key=f"hero_blocked_{char_id}_{player_num}_{i}_{idx}", disabled=True, use_container_width=True)
                                
                                else:
                                    if st.button(f"➕", key=f"hero_add_{char_id}_{player_num}_{i}_{idx}", use_container_width=True):
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
                                            st.error(f"❌ УВЫ")
                            else:
                                st.button(f"🔒", key=f"hero_disabled_{char_id}_{player_num}_{i}_{idx}", disabled=True, use_container_width=True)
    
    # ========== ПРАВАЯ ЧАСТЬ: ТАБЛИЦА ПИКОВ ==========
    with right_col:
        st.markdown("### 🎮 Пачки")
        st.caption("Кнопка: выбор/очистка пачки")
        
        for pack_idx in range(3):
            room_for_pack = selected_rooms[pack_idx] if pack_idx < len(selected_rooms) else "?"
            
            cols = st.columns(5)
            
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
        
        packs_ready = 0
        for pack_idx in range(3):
            if any(picks[pack_idx][slot] is not None for slot in range(4)):
                packs_ready += 1
        
        total_filled = sum(1 for pack in picks for slot in pack if slot is not None)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Всего слотов", "12")
        with col2:
            if packs_ready == 3:
                st.success(f"✅ Пачек готово: {packs_ready}/3")
            else:
                st.warning(f"⚠️ Пачек готово: {packs_ready}/3")
    
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
            errors = []
            
            # ========== НОВАЯ ПРОВЕРКА: В КАЖДОЙ ПАЧКЕ ХОТЯ БЫ 1 ОПЕРАТИВНИК ==========
            empty_packs = []
            for pack_idx in range(3):
                if all(picks[pack_idx][slot] is None for slot in range(4)):
                    empty_packs.append(pack_idx + 1)
            
            if empty_packs:
                errors.append(f"❌ Пачка {', '.join(map(str, empty_packs))} пустая. В каждой пачке должен быть хотя бы 1 оперативник!")
            
            # ========== ПРОВЕРКА ДУБЛИКАТОВ В ПАЧКАХ ==========
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
    
        # ========== ПОЛНАЯ ИНФОРМАЦИЯ О ЗАКУПКАХ ==========    
    all_resources = [
        "🛡️ Универсальная защита",
        "🔵 Защита 5⭐", 
        "🔴 Универсальное воскрешение",
        "🔵 Воскрешение 5⭐",
        "🔴 Универсальный бан",
        "🔵 Бан 4-5⭐",
        "🔄 Рестарт"
    ]
   
    with col1:
        history = data.get("purchase_history", {})
        for name, count in history.items():
            if count > 0:
                st.write(f"{name}: {count}")
   
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
    
    # ========== РАСЧЁТ РЕЗУЛЬТАТОВ БАНОВ ==========
    ban_results = calculate_ban_results({"p1": p1, "p2": p2})
    
    # Сохраняем результаты в session_state для использования в других местах
    st.session_state.ban_results = ban_results

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
        if st.button("📥 Собрать данные участников", key="sync_btn", use_container_width=True):
            # Загружаем старый judge_state, чтобы сохранить комнаты
            old_judge_state = {}
            if os.path.exists(JUDGE_FILE):
                try:
                    with open(JUDGE_FILE, "r", encoding="utf-8") as f:
                        old_judge_state = json.load(f)
                except:
                    pass
            
            # Сохраняем старые комнаты
            old_selected_rooms = old_judge_state.get("selected_rooms", [])
            
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
            
            # Сохраняем в файл судьи, сохраняя комнаты
            judge_state = {
                "p1": st.session_state.p1,
                "p2": st.session_state.p2,
                "selected_rooms": st.session_state.get("temp_selected_rooms", old_selected_rooms)
            }
            
            with open(JUDGE_FILE, "w", encoding="utf-8") as f:
                json.dump(judge_state, f, ensure_ascii=False, indent=2, default=str)
            
            st.success("📁 Данные участников и выбранные комнаты сохранены в judge_data.json!")
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
        # Переход по этапам
        if p1.get("ready") and p2.get("ready"):
            current_stage = p1.get("stage", "resources")
            
            can_advance = False
            next_stage = current_stage
            
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
            
            if can_advance:
                # ОСОБЫЙ СЛУЧАЙ: переход на этап выбора оперативников
                if next_stage == "available":
                    if st.button(f"➡️ Перейти к этапу: {get_stage_name(next_stage)}", key="advance_btn_available", use_container_width=True, type="primary"):
                        # Переводим участников
                        p1["stage"] = next_stage
                        p2["stage"] = next_stage
                        p1["finished_available"] = False
                        p2["finished_available"] = False
                        
                        st.session_state.p1 = p1
                        st.session_state.p2 = p2
                        save_player_data(1)
                        save_player_data(2)
                        
                        # Сохраняем в файл судьи
                        judge_state = {
                            "p1": st.session_state.p1,
                            "p2": st.session_state.p2,
                            "selected_rooms": st.session_state.get("temp_selected_rooms", [])
                        }
                        with open(JUDGE_FILE, "w", encoding="utf-8") as f:
                            json.dump(judge_state, f, ensure_ascii=False, indent=2, default=str)
                        
                        # ПЕРЕКЛЮЧАЕМ СУДЬЮ В РЕЖИМ ВЫБОРА КОМНАТ
                        st.session_state.rooms_selection_mode = True
                        st.success(f"✅ Переход на {get_stage_name(next_stage)} выполнен!")
                        st.info("🏠 Теперь выберите комнаты для турнира")
                        st.rerun()
                
                
                # Обычный переход для других этапов
                else:
                    if st.button(f"➡️ Перейти к этапу: {get_stage_name(next_stage)}", key="advance_btn_other", use_container_width=True, type="primary"):
                        p1["stage"] = next_stage
                        p2["stage"] = next_stage
                        
                        if next_stage == "protection":
                            p1["finished_protection"] = False
                            p2["finished_protection"] = False
                        elif next_stage == "bans":
                            p1["finished_bans"] = False
                            p2["finished_bans"] = False
                        elif next_stage == "picks":
                            p1["finished_picks"] = False
                            p2["finished_picks"] = False
                            
                            # Пересчитываем результаты банов
                            ban_results = calculate_ban_results({"p1": p1, "p2": p2})
                            
                            # Сохраняем в файл судьи
                            judge_state = {
                                "p1": p1,
                                "p2": p2,
                                "selected_rooms": st.session_state.get("temp_selected_rooms", []),
                                "ban_results": ban_results
                            }
                            with open(JUDGE_FILE, "w", encoding="utf-8") as f:
                                json.dump(judge_state, f, ensure_ascii=False, indent=2, default=str)
                            
                        st.session_state.p1 = p1
                        st.session_state.p2 = p2
                        save_player_data(1)
                        save_player_data(2)
                        save_judge_data()
                        
                        st.success(f"✅ Переход на {get_stage_name(next_stage)} выполнен!")
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
    
    # Информация о выбранных комнатах (загружаем из JUDGE_FILE)
    with st.expander("🏠 Выбранные комнаты", expanded=False):
        if os.path.exists(JUDGE_FILE):
            try:
                with open(JUDGE_FILE, "r", encoding="utf-8") as f:
                    judge_data = json.load(f)
                    selected_rooms = judge_data.get("selected_rooms", [])
                    if selected_rooms:
                        for idx, room in enumerate(selected_rooms, 1):
                            st.write(f"{idx}. Комната {room}")
                    else:
                        st.info("Комнаты еще не выбраны")
            except:
                st.info("Комнаты еще не выбраны")
        else:
            st.info("Комнаты еще не выбраны")
    
    # Информация о ресурсах
    with st.expander("💰 Ресурсы участников", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**{p1.get('nickname', 'Участник 1')}**")
            history = p1.get("purchase_history", {})
            for name, count in history.items():
                if count > 0:
                    st.write(f"{name}: {count}")
        with col2:
            st.markdown(f"**{p2.get('nickname', 'Участник 2')}**")
            history = p2.get("purchase_history", {})
            for name, count in history.items():
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
                time.sleep(1)
                st.session_state.rooms_selection_mode = False
                st.rerun()
        else:
            st.button("✅ Подтвердить и продолжить", disabled=True, use_container_width=True)
            st.caption(f"⚠️ Нужно выбрать 3 комнаты (выбрано {len(st.session_state.temp_selected_rooms)})")


def calculate_ban_results(judge_data):
    """Расчёт доступности оперативников после банов (математическая формула)"""
    
    p1 = judge_data.get("p1", {})
    p2 = judge_data.get("p2", {})
    
    p1_bans = p1.get("bans", {})
    p2_bans = p2.get("bans", {})
    p1_protected = set(p1.get("protected_heroes", []))
    p2_protected = set(p2.get("protected_heroes", []))
    
    # Собираем всех оперативников
    all_heroes = set(p1_bans.keys()) | set(p2_bans.keys()) | p1_protected | p2_protected
    
    results = {"p1": {}, "p2": {}}
    
    for hero_id in all_heroes:
        total_bans = p1_bans.get(hero_id, 0) + p2_bans.get(hero_id, 0)
        
        protect_p1 = 1 if hero_id in p1_protected else 0
        protect_p2 = 1 if hero_id in p2_protected else 0
        
        results["p1"][hero_id] = (total_bans - protect_p1) <= 0
        results["p2"][hero_id] = (total_bans - protect_p2) <= 0
    
    return results

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
    
    if len(selected_rooms) < 3:
        st.error("❌ Не выбраны комнаты для боя!")
        return
    
    # Функция для подсчёта очков (ничья = 0.5)
    def calculate_scores():
        score_p1 = 0.0
        score_p2 = 0.0
        draws = 0
        for room, result in st.session_state.get("battle_results", {}).items():
            if result.get("winner") == "p1":
                score_p1 += 1
            elif result.get("winner") == "p2":
                score_p2 += 1
            elif result.get("winner") == "draw":
                score_p1 += 0.5
                score_p2 += 0.5
                draws += 1
        return score_p1, score_p2, draws
    
    # Функция валидации времени
    def validate_time_format(time_str):
        import re
        if not time_str:
            return True
        pattern = r'^(\d{1,2}):(\d{1,2})$'
        match = re.match(pattern, time_str.strip())
        if match:
            seconds = int(match.group(2))
            return 0 <= seconds < 60
        return False
    
    def format_time_display(time_str):
        if not time_str:
            return ""
        time_str = time_str.strip()
        if ":" not in time_str and time_str.isdigit():
            if len(time_str) <= 2:
                return f"0:{time_str}"
            elif len(time_str) == 3:
                return f"{time_str[0]}:{time_str[1:3]}"
            elif len(time_str) == 4:
                return f"{time_str[:2]}:{time_str[2:4]}"
        return time_str
    
    # Инициализация результатов боёв
    if "battle_results" not in st.session_state:
        st.session_state.battle_results = {}
        for i, room in enumerate(selected_rooms):
            st.session_state.battle_results[room] = {
                "winner": None,
                "time_p1": "",
                "time_p2": "",
                "restart_used_p1": False,
                "restart_used_p2": False,
                "active": i == 0
            }
    
    # Получаем пачки
    picks_p1 = p1.get("picks", [[None for _ in range(4)] for _ in range(3)])
    picks_p2 = p2.get("picks", [[None for _ in range(4)] for _ in range(3)])
    
    # Получаем ресурсы рестартов
    restart_p1 = p1.get("resources", {}).get("🔄 Рестарт", 0)
    restart_p2 = p2.get("resources", {}).get("🔄 Рестарт", 0)
    
    # Кнопка сброса
    col_reset1, col_reset2, col_reset3 = st.columns([1, 2, 1])
    with col_reset2:
        if st.button("🗑️ СБРОСИТЬ ВСЕ РЕЗУЛЬТАТЫ", key="reset_all_battles", use_container_width=True):
            for i, room in enumerate(selected_rooms):
                st.session_state.battle_results[room] = {
                    "winner": None,
                    "time_p1": "",
                    "time_p2": "",
                    "restart_used_p1": False,
                    "restart_used_p2": False,
                    "active": (i == 0)  # только первая комната активна
                }
            st.rerun()
    
    st.divider()
    
    # Функция отображения пачки
    def render_pack(pack, room_idx):
        if room_idx < len(pack):
            heroes = pack[room_idx]
            cols = st.columns(4)
            for idx, hero_id in enumerate(heroes):
                with cols[idx]:
                    if hero_id:
                        hero_info = p1.get("character_db", {}).get(hero_id, {}) or p2.get("character_db", {}).get(hero_id, {})
                        img = load_operator_image(hero_info.get("name", ""))
                        if img:
                            st.image(img, width=152)
                        else:
                            st.write("🎴")
                    else:
                        st.write("⬜")
    
    # Получаем текущий счёт перед циклом
    score_p1, score_p2, draws = calculate_scores()
    
    # Определяем, нужна ли третья комната
    need_third_room = not ((score_p1 >= 2 and score_p2 == 0) or (score_p2 >= 2 and score_p1 == 0))
    
    # Формируем список комнат для отображения
    rooms_to_display = []
    for i, room in enumerate(selected_rooms):
        if i == 2 and not need_third_room:
            continue
        rooms_to_display.append(room)
    
    # Обновляем активность комнат (без rerun)
    for i, room in enumerate(rooms_to_display):
        if i == 0:
            # Первая комната активна по умолчанию
            if st.session_state.battle_results[room].get("active") is None:
                st.session_state.battle_results[room]["active"] = True
        else:
            prev_room = rooms_to_display[i - 1]
            # Активируем, если предыдущая завершена и эта ещё не активна
            if (st.session_state.battle_results[prev_room].get("winner") is not None and 
                not st.session_state.battle_results[room].get("active", False)):
                st.session_state.battle_results[room]["active"] = True
                st.rerun()  # Один rerun при активации
                break
    
    # Основной цикл по комнатам, которые нужно показать
    for room_idx, room in enumerate(rooms_to_display):
        real_idx = selected_rooms.index(room)
        result = st.session_state.battle_results[room]
        is_active = result.get("active", False)
        
        if is_active:
            st.markdown(f"### ⭐ КОМНАТА {room} (АКТИВНА) ⭐")
        else:
            st.markdown(f"### 🏠 КОМНАТА {room}")
        
        col_left, col_center, col_right = st.columns([0.4, 0.2, 0.4])
        
        # ========== ЛЕВАЯ КОЛОНКА (Участник 2) ==========
        with col_left:
            render_pack(picks_p2, room_idx)
        
        # ========== ПРАВАЯ КОЛОНКА (Участник 1) ==========
        with col_right:
            render_pack(picks_p1, room_idx)
        
        # ========== ЦЕНТРАЛЬНАЯ КОЛОНКА ==========
        with col_center:
            # Два поля времени в ряд (две строки)
            # Строка 1: заголовки
            time_col1, time_col2 = st.columns(2)
            with time_col1:
                st.markdown(f"**{p2.get('nickname', 'Участник 2')}**")
            with time_col2:
                st.markdown(f"**{p1.get('nickname', 'Участник 1')}**")
            
            # Строка 2: поля ввода времени
            time_col1, time_col2 = st.columns(2)
            with time_col1:
                time_p2_val = st.text_input(
                    "⏱️",
                    value=result["time_p2"],
                    key=f"time_p2_{room}",
                    placeholder="м:сс",
                    label_visibility="collapsed"
                )
                if time_p2_val != result["time_p2"]:
                    if validate_time_format(time_p2_val):
                        result["time_p2"] = format_time_display(time_p2_val)
                        st.session_state.battle_results[room] = result
                    else:
                        st.warning("Неверный формат")
            
            with time_col2:
                time_p1_val = st.text_input(
                    "⏱️",
                    value=result["time_p1"],
                    key=f"time_p1_{room}",
                    placeholder="м:сс",
                    label_visibility="collapsed"
                )
                if time_p1_val != result["time_p1"]:
                    if validate_time_format(time_p1_val):
                        result["time_p1"] = format_time_display(time_p1_val)
                        st.session_state.battle_results[room] = result
                    else:
                        st.warning("Неверный формат")
            
            st.markdown("---")
            
            # Рестарты в три колонки
            restart_col1, restart_col2, restart_col3 = st.columns([1, 1, 1])
            
            with restart_col1:
                # Считаем, сколько рестартов уже использовано в ЭТОЙ комнате
                used_in_this_room_p2 = result.get("restart_count_p2", 0)
                remaining_restarts_p2 = restart_p2 - sum(r.get("restart_count_p2", 0) for r in st.session_state.battle_results.values())
                
                if remaining_restarts_p2 > 0 and is_active and result.get("winner") is None:
                    if st.button(f"🔄 Рестарт {p2.get('nickname', 'Участник 2')} ({remaining_restarts_p2})", key=f"restart_p2_{room}", use_container_width=True):
                        result["time_p2"] = ""
                        result["winner"] = None
                        # Увеличиваем счётчик рестартов в этой комнате
                        result["restart_count_p2"] = used_in_this_room_p2 + 1
                        st.session_state.battle_results[room] = result
                        st.rerun()
                elif result.get("restart_count_p2", 0) > 0:
                    st.caption(f"🔄 ({result.get('restart_count_p2', 0)} раз)")
                else:
                    st.caption("—")
            
            with restart_col2:
                st.markdown("<div style='text-align: center; font-weight: bold;'>VS</div>", unsafe_allow_html=True)
            
            with restart_col3:
                used_in_this_room_p1 = result.get("restart_count_p1", 0)
                remaining_restarts_p1 = restart_p1 - sum(r.get("restart_count_p1", 0) for r in st.session_state.battle_results.values())
                
                if remaining_restarts_p1 > 0 and is_active and result.get("winner") is None:
                    if st.button(f"🔄 Рестарт {p1.get('nickname', 'Участник 1')} ({remaining_restarts_p1})", key=f"restart_p1_{room}", use_container_width=True):
                        result["time_p1"] = ""
                        result["winner"] = None
                        result["restart_count_p1"] = used_in_this_room_p1 + 1
                        st.session_state.battle_results[room] = result
                        st.rerun()
                elif result.get("restart_count_p1", 0) > 0:
                    st.caption(f"🔄 ({result.get('restart_count_p1', 0)} раз)")
                else:
                    st.caption("—")
            
            st.markdown("---")
            
            # Выбор победителя (только если комната активна)
            st.markdown("**🏆 Победитель**")
            
            if is_active:
                winner_options = {
                    None: "— не выбран —",
                    "p2": f"{p2.get('nickname', 'Участник 2')} (слева)",
                    "p1": f"{p1.get('nickname', 'Участник 1')} (справа)",
                    "draw": "Ничья"
                }
                
                current_winner = result["winner"]
                
                selected_winner = st.selectbox(
                    "Выберите победителя",
                    options=list(winner_options.keys()),
                    format_func=lambda x: winner_options[x],
                    key=f"winner_select_{room}",
                    label_visibility="collapsed"
                )
                
                if selected_winner != current_winner and selected_winner is not None:
                    result["winner"] = selected_winner
                    st.session_state.battle_results[room] = result
                    
                    if selected_winner == "p1":
                        st.success(f"✅ Молодец {p1.get('nickname', 'Участник 1')}! 🎉")
                    elif selected_winner == "p2":
                        st.success(f"✅ Молодец {p2.get('nickname', 'Участник 2')}! 🎉")
                    elif selected_winner == "draw":
                        st.info("🤝 Держи член")
                    
                    # Деактивируем текущую комнату и активируем следующую
                    result["active"] = False
                    st.session_state.battle_results[room] = result
                    
                    if room_idx + 1 < len(selected_rooms):
                        next_room = selected_rooms[room_idx + 1]
                        st.session_state.battle_results[next_room]["active"] = True
                    
                    st.rerun()
                
                if result["winner"] is not None:
                    if result["winner"] == "p1":
                        st.success(f"✅ Молодец {winner_options[result['winner']]}")
                    elif result["winner"] == "p2":
                        st.success(f"✅ Молодец {winner_options[result['winner']]}")
                    else:
                        st.info("🤝 Держи член")
            else:
                if result["winner"] is not None:
                    if result["winner"] == "p1":
                        st.success(f"🏆 Подебитель {p1.get('nickname', 'Участник 1')} (справа)")
                    elif result["winner"] == "p2":
                        st.success(f"🏆 Подебитель {p2.get('nickname', 'Участник 2')} (слева)")
                    elif result["winner"] == "draw":
                        st.info("🤝 Держи член")
                else:
                    st.caption("—")
        
        st.divider()
    
    # ========== ПОДСЧЁТ СЧЁТА ПОСЛЕ ЦИКЛА ==========
    final_score_p1, final_score_p2, final_draws = calculate_scores()
    
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(p1.get("nickname", "Участник 1"), f"{final_score_p1:.1f}")
    with col2:
        st.metric("Ничьи", final_draws)
    with col3:
        st.metric(p2.get("nickname", "Участник 2"), f"{final_score_p2:.1f}")
    
    # Проверка, все ли комнаты завершены (включая третью, если она была нужна)
    all_completed = all(
        st.session_state.battle_results[room]["winner"] is not None 
        for room in selected_rooms
    )
    
    # Проверка, можно ли завершить турнир досрочно (при счёте 2:0)
    can_finish_early = (final_score_p1 >= 2 and final_score_p2 == 0) or (final_score_p2 >= 2 and final_score_p1 == 0)
    
    # ========== КНОПКА ЗАВЕРШЕНИЯ ==========
    st.divider()
    
    if all_completed or can_finish_early:
        if final_score_p1 > final_score_p2:
            st.success(f"🏆 ПОБЕДИТЕЛЬ ТУРНИРА: {p1.get('nickname', 'Участник 1')}!!! 🏆")
        elif final_score_p2 > final_score_p1:
            st.success(f"🏆 ПОБЕДИТЕЛЬ ТУРНИРА: {p2.get('nickname', 'Участник 2')}!!! 🏆")
        else:
            if final_draws > 0:
                st.warning("🤝 НИЧЬЯ! ТРЕБУЕТСЯ ТАЙ-БРЕЙК 🤝")
        
        # Кнопка завершения турнира (всегда показываем, если есть победитель или все комнаты завершены)
        if st.button("🏁 ЗАВЕРШИТЬ ТУРНИР", key="finish_tournament", type="primary", use_container_width=True):
            p1["stage"] = "finished"
            p2["stage"] = "finished"
            st.session_state.p1 = p1
            st.session_state.p2 = p2
            save_player_data(1)
            save_player_data(2)
            save_judge_data()
            
            if "battle_results" in st.session_state:
                del st.session_state.battle_results
            
            st.success("🏆 ТУРНИР ЗАВЕРШЁН! 🏆")
            time.sleep(2)
            st.rerun()
    else:
        # Активация следующей комнаты, если текущая завершена
        for i, room in enumerate(selected_rooms):
            if st.session_state.battle_results[room]["winner"] is not None:
                if i + 1 < len(selected_rooms):
                    next_room = selected_rooms[i + 1]
                    if not st.session_state.battle_results[next_room].get("active", False):
                        # Проверяем, нужна ли третья комната
                        if i + 1 == 2:  # это третья комната
                            if (final_score_p1 >= 2 and final_score_p2 == 0) or (final_score_p2 >= 2 and final_score_p1 == 0):
                                # Третья комната не нужна, пропускаем
                                continue
                        st.session_state.battle_results[next_room]["active"] = True
                        st.rerun()
                break
        
        st.info("⏳ Ожидание фиксации всех комнат...")


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