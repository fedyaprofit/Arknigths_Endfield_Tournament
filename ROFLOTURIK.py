import streamlit as st
import json
import os
import time
import hashlib
from datetime import datetime
from typing import Dict, List, Tuple

# ============================
# 1. Константы и пути
# ============================

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

PLAYERS_DIR = "data/players"
JUDGES_FILE = "data/judges.json"
TOURNAMENTS_DIR = "data/tournaments/active/"

#STARTING_POINTS = {
#    "bo3": 12,
#    "bo5": 16,
#    "group": 20
#}

# ============================
# 2. Общие утилиты (хеширование, работа с файлами)
# ============================

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def get_player_file(nickname: str) -> str:
    safe = "".join(c for c in nickname if c.isalnum() or c in "._-")
    return os.path.join(PLAYERS_DIR, f"{safe}.json")

def load_player(nickname: str) -> dict:
    path = get_player_file(nickname)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_player(nickname: str, data: dict):
    os.makedirs(PLAYERS_DIR, exist_ok=True)
    with open(get_player_file(nickname), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def player_exists(nickname: str) -> bool:
    return os.path.exists(get_player_file(nickname))

def get_all_players() -> List[str]:
    if not os.path.exists(PLAYERS_DIR):
        return []
    players = []
    for fname in os.listdir(PLAYERS_DIR):
        if fname.endswith(".json"):
            with open(os.path.join(PLAYERS_DIR, fname), "r", encoding="utf-8") as f:
                data = json.load(f)
                players.append(data.get("nickname", fname[:-5]))
    return players

def get_mode_config(mode: str) -> dict:
    """Возвращает актуальный конфиг из data/configs/{mode}.json"""
    config_path = os.path.join("data", "configs", f"{mode}.json")
    if not os.path.exists(config_path):
        return {}
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_operator_image(name):
    """Загрузка изображения оперативника"""
    import os
    filename = f"{name}.png"
    path = os.path.join("Operators", filename)
    
    # Отладка: покажи путь
    print(f"Ищем изображение: {os.path.abspath(path)}")
    
    if os.path.exists(path):
        return path
    return None

def check_stage_completed(match_dir: str, players: list, stage: str) -> bool:
    """Проверяет, завершили ли все игроки текущий этап"""
    
    stage_key = {
        "approval": "finished_approval",
        "purchase": "finished_purchase",
        "protection": "finished_protection",
        "bans": "finished_bans",
        "picks": "finished_picks",
        "battle": "finished_battle",
    }.get(stage, None)
    
    if stage_key is None:
        return False
    
    for i, player in enumerate(players, 1):
        player_path = os.path.join(match_dir, f"player{i}.json")
        if os.path.exists(player_path):
            with open(player_path, "r", encoding="utf-8") as f:
                player_data = json.load(f)
            if not player_data.get(stage_key, False):
                return False
        else:
            return False
    
    return True

def calculate_ban_results(match_id: str):
    """Рассчитывает результаты банов и сохраняет в judge.json"""
    
    match_dir = os.path.join(TOURNAMENTS_DIR, match_id)
    judge_path = os.path.join(match_dir, "judge.json")
    
    # Загружаем текущий judge.json
    if os.path.exists(judge_path):
        with open(judge_path, "r", encoding="utf-8") as f:
            judge_data = json.load(f)
    else:
        judge_data = {}
    
    # Загружаем данные игроков
    players_data = {}
    for i in range(1, 5):
        player_path = os.path.join(match_dir, f"player{i}.json")
        if os.path.exists(player_path):
            with open(player_path, "r", encoding="utf-8") as f:
                player_data = json.load(f)
                if player_data.get("nickname"):
                    players_data[f"p{i}"] = {
                        "bans": player_data.get("bans", {}),
                        "protected_heroes": player_data.get("protected_heroes", [])
                    }
    
    # Сохраняем исходные данные в judge.json
    judge_data["players_data"] = players_data
    
    # Рассчитываем доступность
    p1_bans = players_data.get("p1", {}).get("bans", {})
    p2_bans = players_data.get("p2", {}).get("bans", {})
    p1_protected = set(str(h) for h in players_data.get("p1", {}).get("protected_heroes", []))
    p2_protected = set(str(h) for h in players_data.get("p2", {}).get("protected_heroes", []))
    
    # Собираем всех оперативников
    all_heroes = set()
    for hero_id in p1_bans.keys():
        all_heroes.add(str(hero_id))
    for hero_id in p2_bans.keys():
        all_heroes.add(str(hero_id))
    for hero_id in p1_protected:
        all_heroes.add(str(hero_id))
    for hero_id in p2_protected:
        all_heroes.add(str(hero_id))
    
    ban_results = {"p1": {}, "p2": {}}
    
    for hero_id in all_heroes:
        total_bans = p1_bans.get(str(hero_id), 0) + p2_bans.get(str(hero_id), 0)
        
        protect_p1 = 1 if str(hero_id) in p1_protected else 0
        protect_p2 = 1 if str(hero_id) in p2_protected else 0
        
        ban_results["p1"][hero_id] = (total_bans - protect_p1) <= 0
        ban_results["p2"][hero_id] = (total_bans - protect_p2) <= 0
    
    judge_data["ban_results"] = ban_results
    
    # Сохраняем
    with open(judge_path, "w", encoding="utf-8") as f:
        json.dump(judge_data, f, indent=2, ensure_ascii=False)
    
    return ban_results

def check_stage_completed(match_dir: str, players: list, stage: str) -> bool:
    st.write(f"DEBUG check_stage_completed: stage={stage}, players={players}")
    
    stage_key = {
        "approval": "finished_approval",
        "purchase": "finished_purchase",
        "protection": "finished_protection",
        "bans": "finished_bans",
        "picks": "finished_picks",
    }.get(stage, None)
    
    st.write(f"DEBUG: stage_key = {stage_key}")
    
    if stage_key is None:
        return False
    
    for i, player in enumerate(players, 1):
        player_path = os.path.join(match_dir, f"player{i}.json")
        st.write(f"DEBUG: проверяю {player} по пути {player_path}")
        
        if os.path.exists(player_path):
            with open(player_path, "r", encoding="utf-8") as f:
                player_data = json.load(f)
            finished = player_data.get(stage_key, False)
            st.write(f"DEBUG: {player} {stage_key} = {finished}")
            if not finished:
                return False
        else:
            st.write(f"DEBUG: файл {player_path} не найден")
            return False
    return True

def execute_stage_transition(match_dir, config_path, tournament_config, mode_config, players, current_stage, stages_order, stage_names, match_id):
    """Выполняет переход на следующий этап"""
    
    next_stage = stages_order[stages_order.index(current_stage) + 1]
    
    # Дополнительные действия при переходе
    if current_stage == "purchase":
        # Добавляем бесплатные ресурсы
        free_items = mode_config.get("free_items", {})
        for i, player in enumerate(players, 1):
            player_path = os.path.join(match_dir, f"player{i}.json")
            if os.path.exists(player_path):
                with open(player_path, "r", encoding="utf-8") as f:
                    p_data = json.load(f)
                
                for item_name, count in free_items.items():
                    p_data["resources"][item_name] = p_data["resources"].get(item_name, 0) + count
                    p_data["purchase_history"][item_name] = p_data["purchase_history"].get(item_name, 0) + count
                
                p_data["free_resources_added"] = True
                
                with open(player_path, "w", encoding="utf-8") as f:
                    json.dump(p_data, f, indent=2)
                
                st.info(f"🎁 {player}: добавлены бесплатные ресурсы ({', '.join(free_items.keys())})")
    
    if current_stage == "bans":
        # Рассчитываем результаты банов
        ban_results = calculate_ban_results(match_id)
        st.success("📊 Результаты банов рассчитаны и сохранены в judge.json!")
    
    if current_stage == "picks":
        # Проверяем, что все пачки собраны (хотя бы 1 оперативник в каждой)
        all_packs_ready = True
        for i, player in enumerate(players, 1):
            player_path = os.path.join(match_dir, f"player{i}.json")
            if os.path.exists(player_path):
                with open(player_path, "r", encoding="utf-8") as f:
                    p_data = json.load(f)
                picks = p_data.get("picks", [])
                for pack_idx, pack in enumerate(picks):
                    if all(slot is None for slot in pack):
                        all_packs_ready = False
                        st.warning(f"{player}: пачка {pack_idx + 1} пустая!")
                        break
        
        if not all_packs_ready:
            st.error("❌ Не все игроки собрали пачки!")
            return
    
    # Переключаем этап
    tournament_config["stage"] = next_stage
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(tournament_config, f, indent=2)
    
    # Очищаем временные переменные при переходе на бой
    if next_stage == "battle":
        if "battle_results" in st.session_state:
            del st.session_state.battle_results
    
    st.success(f"✅ Переход на этап {stage_names[next_stage]} выполнен!")
    st.rerun()

# ============================
# 3. Регистрация / аутентификация
# ============================

def register_player(nickname: str, password: str) -> Tuple[bool, str]:
    if player_exists(nickname):
        return False, "Никнейм уже занят"
    if not nickname or not password:
        return False, "Заполните оба поля"
    player_data = {
        "nickname": nickname,
        "password_hash": hash_password(password),
        "roster": {}           # будет заполняться отдельно
    }
    save_player(nickname, player_data)
    return True, "Регистрация успешна! Теперь войдите."

def authenticate_player(nickname: str, password: str) -> Tuple[bool, str]:
    data = load_player(nickname)
    if not data:
        return False, "Пользователь не найден"
    if data["password_hash"] != hash_password(password):
        return False, "Неверный пароль"
    return True, "Вход выполнен"

def authenticate_judge(login: str, password: str) -> Tuple[bool, str]:
    if not os.path.exists(JUDGES_FILE):
        return False, "Судьи не настроены"
    with open(JUDGES_FILE, "r", encoding="utf-8") as f:
        judges = json.load(f)
    if login not in judges:
        return False, "Судья не найден"
    if judges[login] != password:
        return False, "Неверный пароль"
    return True, "Вход выполнен"

# ============================
# 4. Профиль игрока (ростер)
# ============================

def display_roster_editor(roster: dict) -> dict:
    """Отображает форму редактирования ростера с картинками и вкладками"""
    st.subheader("⭐ Ваш ростер оперативников")
    st.caption("Укажите, какие оперативники у вас есть, их уровень (0–90) и потенциал (0–5).")
    st.info("💡 По умолчанию все оперативники отмечены как 'Есть'. Снимите галочку, если оперативника нет в аккаунте.")
    
    # Слайдер для выбора количества колонок
    cols_per_row = st.slider(
        "Настройка отображения оперативников",
        min_value=2,
        max_value=12,
        value=6,
        step=1,
        help="Настройте отображение под ваш экран"
    )
    
    new_roster = roster.copy()
    
    # Разделяем по редкости
    heroes_6star = {k: v for k, v in CHARACTERS_DB.items() if v["rarity"] == "6⭐"}
    heroes_5star = {k: v for k, v in CHARACTERS_DB.items() if v["rarity"] == "5⭐"}
    heroes_4star = {k: v for k, v in CHARACTERS_DB.items() if v["rarity"] == "4⭐"}
    
    # Сортируем по имени
    heroes_6star = dict(sorted(heroes_6star.items(), key=lambda x: x[1]["name"]))
    heroes_5star = dict(sorted(heroes_5star.items(), key=lambda x: x[1]["name"]))
    heroes_4star = dict(sorted(heroes_4star.items(), key=lambda x: x[1]["name"]))
    
    # Функция отображения сетки с заданным количеством колонок
    def render_grid(heroes_dict, cols_count):
        hero_list = list(heroes_dict.items())
        for i in range(0, len(hero_list), cols_count):
            row = hero_list[i:i + cols_count]
            cols = st.columns(len(row))
            for idx, (cid, info) in enumerate(row):
                with cols[idx]:
                    with st.container(border=True):
                        img_path = load_operator_image(info['name'])
                        if img_path:
                            st.image(img_path, width=80)
                        else:
                            st.write("🎴")
                        
                        st.markdown(f"**{info['name']}**")
                                                
                        # По умолчанию has = True (если в ростере нет записи)
                        current = roster.get(str(cid), {"has": True, "level": 90, "potential": 0})
                        has = st.checkbox("Есть", value=current["has"], key=f"has_{cid}")
                        
                        st.markdown("**Уровень**")
                        level = st.number_input(
                            "Уровень", 
                            0, 90, current["level"], 
                            key=f"lvl_{cid}", 
                            label_visibility="collapsed",
                            disabled=not has  # Блокируем, если нет оперативника
                        )
                        
                        st.markdown("**Потенциал**")
                        pot = st.number_input(
                            "Потенциал", 
                            0, 5, current["potential"], 
                            key=f"pot_{cid}", 
                            label_visibility="collapsed",
                            disabled=not has  # Блокируем, если нет оперативника
                        )
                        
                        new_roster[str(cid)] = {"has": has, "level": level, "potential": pot}
    
    # Три вкладки
    tab1, tab2, tab3 = st.tabs(["6⭐ Герои", "5⭐ Герои", "4⭐ Герои"])
    
    with tab1:
        if heroes_6star:
            render_grid(heroes_6star, cols_per_row)
        else:
            st.info("Нет 6⭐ оперативников")
    
    with tab2:
        if heroes_5star:
            render_grid(heroes_5star, cols_per_row)
        else:
            st.info("Нет 5⭐ оперативников")
    
    with tab3:
        if heroes_4star:
            render_grid(heroes_4star, cols_per_row)
        else:
            st.info("Нет 4⭐ оперативников")
    
    return new_roster
# ============================
# 5. Работа с Матчами (списки, создание, загрузка)
# ============================

def judge_approve_roster(match_id: str, player_nickname: str):
    """Отображает ростер игрока для подтверждения судьёй."""
    st.markdown(f"## ✅ Утверждение ростера: **{player_nickname}**")
    st.markdown(f"Матч: {match_id}")
    
    player_data = load_player(player_nickname)
    if not player_data:
        st.error("Ошибка загрузки профиля игрока")
        return
    
    roster = player_data.get("roster", {})
    
    st.subheader("Заявленный ростер")
    
    cols_per_row = st.slider(
        "Количество оперативников в строке",
        min_value=2,
        max_value=12,
        value=5,
        step=1
    )
    
    # Собираем оперативников с уровнем для сортировки
    has_heroes = []
    for cid, info in CHARACTERS_DB.items():
        data = roster.get(str(cid), {"has": False})
        if data.get("has", False):
            level = data.get('level', 90)
            has_heroes.append((cid, info, data, level))
    
    # Сортировка: сначала по уровню (выше → ниже), затем по имени
    def get_rarity_order(rarity):
        return {"6⭐": 0, "5⭐": 1, "4⭐": 2}.get(rarity, 3)

    has_heroes.sort(key=lambda x: (-x[3], get_rarity_order(x[1]["rarity"]), x[1]["name"]))
    
    if not has_heroes:
        st.warning("У игрока нет отмеченных оперативников!")
    else:
        for i in range(0, len(has_heroes), cols_per_row):
            row = has_heroes[i:i + cols_per_row]
            cols = st.columns(len(row))
            for idx, (cid, info, data, level) in enumerate(row):
                with cols[idx]:
                    with st.container(border=True):
                        img_path = load_operator_image(info['name'])
                        if img_path:
                            st.image(img_path, width=80)
                        else:
                            st.write("🎴")
                        
                        st.markdown(f"**{info['name']}**")
                        
                        potential = data.get('potential', 0)
                        rank = 6 if info["rarity"] == "6⭐" else (5 if info["rarity"] == "5⭐" else 4)
                        
                        st.caption(f"Lv.{level} | П{potential}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Подтвердить ростер", type="primary", use_container_width=True):
            # Обновляем статус в judge.json
            match_dir = os.path.join(TOURNAMENTS_DIR, match_id)
            judge_path = os.path.join(match_dir, "judge.json")
            with open(judge_path, "r", encoding="utf-8") as f:
                judge_data = json.load(f)
            judge_data["rosters_approval"][player_nickname]["status"] = "approved"
            judge_data["rosters_approval"][player_nickname]["checked_by"] = st.session_state.nickname
            with open(judge_path, "w", encoding="utf-8") as f:
                json.dump(judge_data, f, indent=2, ensure_ascii=False)
            st.success(f"Ростер {player_nickname} подтверждён")
            
            # Проверяем, все ли ростеры подтверждены
            with open(judge_path, "r", encoding="utf-8") as f:
                judge_data = json.load(f)
            
            all_approved = all(
                judge_data["rosters_approval"][p]["status"] == "approved"
                for p in judge_data["rosters_approval"].keys()
            )
            
            if all_approved:
                # Переводим Матч на этап закупки
                config_path = os.path.join(match_dir, "config.json")
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                config["stage"] = "purchase"
                with open(config_path, "w", encoding="utf-8") as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
                st.success(f"✅ Все ростеры подтверждены! Матч переведён на этап закупки.")
                time.sleep(2)
            
            # Возвращаемся в панель судьи
            del st.session_state.roster_check_match
            del st.session_state.roster_check_player
            st.rerun()
    
    with col2:
        if st.button("❌ Отклонить (требовать исправления)", use_container_width=True):
            match_dir = os.path.join(TOURNAMENTS_DIR, match_id)
            judge_path = os.path.join(match_dir, "judge.json")
            with open(judge_path, "r", encoding="utf-8") as f:
                judge_data = json.load(f)
            judge_data["rosters_approval"][player_nickname]["status"] = "rejected"
            with open(judge_path, "w", encoding="utf-8") as f:
                json.dump(judge_data, f, indent=2)
            st.error(f"Ростер {player_nickname} отклонён. Игрок должен исправить данные.")
            time.sleep(2)
            del st.session_state.roster_check_match
            del st.session_state.roster_check_player
            st.rerun()
    
    if st.button("🔙 Назад", use_container_width=True):
        del st.session_state.roster_check_match
        del st.session_state.roster_check_player
        st.rerun()

def get_active_tournaments_for_player(nickname: str) -> List[dict]:
    """Возвращает список Матчов, в которых участвует игрок."""
    active = []
    if not os.path.exists(TOURNAMENTS_DIR):
        return active
    for match_id in os.listdir(TOURNAMENTS_DIR):
        cfg_path = os.path.join(TOURNAMENTS_DIR, match_id, "config.json")
        if not os.path.exists(cfg_path):
            continue
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        if nickname in cfg.get("players", []):
            active.append({
                "match_id": match_id,
                "mode": cfg["mode"],
                "stage": cfg.get("stage", "resources"),
                "opponents": [p for p in cfg["players"] if p != nickname]
            })
    return active

def get_all_active_tournaments() -> List[dict]:
    tournaments = []
    if not os.path.exists(TOURNAMENTS_DIR):
        return tournaments
    for match_id in os.listdir(TOURNAMENTS_DIR):
        config_path = os.path.join(TOURNAMENTS_DIR, match_id, "config.json")
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            mode_config = get_mode_config(cfg.get("mode", "bo3"))
            tournaments.append({
                "match_id": match_id,
                "mode": cfg.get("mode", "unknown"),
                "players": cfg.get("players", []),
                "stage": cfg.get("stage", "resources"),
                "name": mode_config.get("name", cfg.get("mode", "unknown"))
            })
    return tournaments

def create_tournament(match_id: str, mode: str, players: List[str]) -> Tuple[bool, str]:
    match_dir = os.path.join(TOURNAMENTS_DIR, match_id)
    config_path = os.path.join(match_dir, "config.json")
    
    if os.path.exists(config_path):
        return False, "Матч с таким ID уже существует"
    
    os.makedirs(match_dir, exist_ok=True)
    
    mode_config = get_mode_config(mode)
    if not mode_config:
        return False, f"Режим {mode} не найден в data/configs/"
    
    # Сохраняем только минимальную информацию
    tournament_config = {
        "match_id": match_id,
        "mode": mode,
        "players": players,
        "players_count": mode_config.get("players", 2),
        "rooms": mode_config.get("rooms", 3),
        "stage": "approval",
        "created_at": time.time()
    }
    
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(tournament_config, f, indent=2, ensure_ascii=False)
    
    # Файлы игроков (без копирования shop)
    for i, player in enumerate(players, 1):
        player_data = {
            "nickname": player,
            "resources": {},
            "purchase_history": {},
            "protected_heroes": [],
            "bans": {},
            "picks": [[None for _ in range(4)] for _ in range(tournament_config["rooms"])],
            "finished_approval": False,
            "finished_purchase": False,
            "finished_protection": False,
            "finished_bans": False,
            "finished_picks": False,
            "free_resources_added": False
        }
        with open(os.path.join(match_dir, f"player{i}.json"), "w", encoding="utf-8") as f:
            json.dump(player_data, f, indent=2, ensure_ascii=False)
    
    # Файл судьи
    judge_data = {
        "rosters_approval": {player: {"status": "pending", "checked_by": None, "items": {}} for player in players},
        "battle_results": {}
    }
    with open(os.path.join(match_dir, "judge.json"), "w", encoding="utf-8") as f:
        json.dump(judge_data, f, indent=2, ensure_ascii=False)
    
    return True, f"Матч {match_id} создан (режим: {mode_config.get('name', mode)})"

def clear_tournament(match_id: str) -> Tuple[bool, str]:
    """Очищает файлы турнира, но оставляет пустую папку"""
    match_dir = os.path.join(TOURNAMENTS_DIR, match_id)
    if not os.path.exists(match_dir):
        return False, "Матч не найден"
    
    try:
        # Удаляем все JSON файлы в папке
        for filename in os.listdir(match_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(match_dir, filename)
                os.remove(file_path)
        return True, f"Матч {match_id} очищен"
    except Exception as e:
        return False, f"Ошибка: {e}"

def judge_match_interface(match_id: str, mode: str):
    """Интерфейс управления конкретным матчем"""
    
    match_dir = os.path.join(TOURNAMENTS_DIR, match_id)
    config_path = os.path.join(match_dir, "config.json")
    
    # Загружаем конфиг матча
    with open(config_path, "r", encoding="utf-8") as f:
        tournament_config = json.load(f)
    
    # Получаем актуальный конфиг режима
    mode_config = get_mode_config(mode)
    
    mode_name = mode_config.get("name", mode)
    players = tournament_config.get("players", [])
    current_stage = tournament_config.get("stage", "resources")
    
    # Порядок этапов
    stages_order = ["approval", "purchase", "protection", "bans", "picks", "battle", "finished"]
    stage_names = {
        "approval": "✅ Утверждение ростеров",
        "purchase": "🛒 Закупка ресурсов",
        "protection": "🛡️ Защита",
        "bans": "🔨 Баны",
        "picks": "⭐ Пики",
        "battle": "⚔️ Бой",
        "finished": "🏆 Завершён"
    }
    
    current_index = stages_order.index(current_stage)
    
    # Шапка матча
    st.markdown(f"## ⚖️ Управление матчем: {match_id}")
    st.markdown(f"**Режим:** {mode_name}")
    st.markdown(f"**Участники:** {', '.join(players)}")
    st.markdown(f"**Текущий этап:** {stage_names[current_stage]}")
    
    # Кнопки управления
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔙 Назад к списку матчей", use_container_width=True):
            del st.session_state.current_match
            del st.session_state.current_match_mode
            st.rerun()
    with col2:
        if st.button("🔄 Обновить", use_container_width=True):
            st.rerun()
    
    st.divider()
    
    # ========== РОСТЕРЫ УЧАСТНИКОВ ==========
    with st.expander("📋 Ростеры участников", expanded=False):
        selected_player = st.radio(
            "Выберите игрока",
            options=players,
            horizontal=True,
            key=f"judge_roster_select_{match_id}"
        )
        
        cols_per_row = st.slider(
            "Количество оперативников в строке",
            min_value=2,
            max_value=8,
            value=5,
            step=1,
            key=f"judge_rosters_cols_{match_id}"
        )
        
        roster = load_player_roster(selected_player)
        
        if not roster:
            st.caption("Нет данных")
        else:
            has_heroes = []
            for cid, info in CHARACTERS_DB.items():
                data = roster.get(str(cid), {"has": False})
                if data.get("has", False):
                    level = data.get('level', 90)
                    potential = data.get('potential', 0)
                    has_heroes.append((cid, info, level, potential))
            
            def get_rarity_order(rarity):
                return {"6⭐": 0, "5⭐": 1, "4⭐": 2}.get(rarity, 3)
            
            has_heroes.sort(key=lambda x: (-x[2], get_rarity_order(x[1]["rarity"]), x[1]["name"]))
            
            if not has_heroes:
                st.caption("Нет оперативников")
            else:
                for i in range(0, len(has_heroes), cols_per_row):
                    row = has_heroes[i:i + cols_per_row]
                    cols = st.columns(len(row))
                    for idx, (cid, info, level, potential) in enumerate(row):
                        with cols[idx]:
                            with st.container(border=True):
                                img = load_operator_image(info['name'])
                                if img:
                                    st.image(img, width=60)
                                else:
                                    st.write("🎴")
                                st.markdown(f"**{info['name']}**")
                                st.caption(f"Lv.{level} | П{potential}")
    
    # ========== НАЧАЛЬНЫЕ ПОКУПКИ УЧАСТНИКОВ ==========
    with st.expander("💰 Начальные покупки участников", expanded=False):
        resources_list = ["🛡️ Универсальная защита", "🔵 Защита 5⭐", "🔴 Универсальное воскрешение", 
                          "🔵 Воскрешение 5⭐", "🔴 Универсальный бан", "🔵 Бан 4-5⭐", "🔄 Рестарт"]
        
        players_data = {}
        for i, player in enumerate(players, 1):
            player_path = os.path.join(match_dir, f"player{i}.json")
            if os.path.exists(player_path):
                with open(player_path, "r", encoding="utf-8") as f:
                    p_data = json.load(f)
            else:
                p_data = {}
            players_data[player] = p_data.get("purchase_history", {})
        
        table_data = []
        for res_name in resources_list:
            row = {"Ресурс": res_name}
            for player in players:
                count = players_data.get(player, {}).get(res_name, 0)
                row[player] = count if count > 0 else "—"
            table_data.append(row)
        
        st.dataframe(table_data, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # ========== ОТОБРАЖЕНИЕ СТАТУСА ИГРОКОВ ==========
    st.markdown("### 📊 Статус игроков")
    
    for i, player in enumerate(players, 1):
        player_path = os.path.join(match_dir, f"player{i}.json")
        if os.path.exists(player_path):
            with open(player_path, "r", encoding="utf-8") as f:
                p_data = json.load(f)
            
            finished = False
            if current_stage == "approval":
                finished = p_data.get("finished_approval", False)
            elif current_stage == "purchase":
                finished = p_data.get("finished_purchase", False)
            elif current_stage == "protection":
                finished = p_data.get("finished_protection", False)
            elif current_stage == "bans":
                finished = p_data.get("finished_bans", False)
            elif current_stage == "picks":
                finished = p_data.get("finished_picks", False)
            elif current_stage == "battle":
                finished = p_data.get("finished_battle", False)
            
            if finished:
                st.success(f"✅ {player}: завершён")
            else:
                st.warning(f"⏳ {player}: ожидает")
        else:
            st.warning(f"⚠️ {player}: данные не найдены")
    
    st.divider()
    
    # ========== КНОПКИ УПРАВЛЕНИЯ ЭТАПАМИ ==========
    col_back, col_forward = st.columns(2)
    
    # Кнопка НАЗАД
    with col_back:
        if current_index > 0:
            if st.button("⬅️ Назад (сброс этапа)", use_container_width=True):
                st.session_state.confirm_back = True
                st.rerun()
        else:
            st.button("⬅️ Назад", disabled=True, use_container_width=True)
    
    # Кнопка ВПЕРЁД
    with col_forward:
        can_advance = check_stage_completed(match_dir, players, current_stage)
        
        if can_advance and current_index < len(stages_order) - 1:
            if st.button(f"➡️ Перейти к этапу: {stage_names[stages_order[current_index + 1]]}", type="primary", use_container_width=True):
                execute_stage_transition(match_dir, config_path, tournament_config, mode_config, players, current_stage, stages_order, stage_names, match_id)
        else:
            if current_index < len(stages_order) - 1:
                if st.button(f"⚠️ ПРИНУДИТЕЛЬНЫЙ ПЕРЕХОД к этапу: {stage_names[stages_order[current_index + 1]]}", use_container_width=True):
                    st.session_state.confirm_force = True
                    st.rerun()
            else:
                st.button("➡️ Перейти", disabled=True, use_container_width=True)
    
    # ========== ОБРАБОТКА ПОДТВЕРЖДЕНИЙ ==========
    
    # Подтверждение возврата
    if st.session_state.get("confirm_back", False):
        st.warning(f"⚠️ Возврат на этап {stage_names[stages_order[current_index - 1]]} сбросит прогресс текущего этапа у всех игроков!")
        
        col_yes, col_no = st.columns(2)
        with col_yes:
            if st.button("✅ Да, вернуться"):
                target_stage = stages_order[current_index - 1]
                
                for i, player in enumerate(players, 1):
                    player_path = os.path.join(match_dir, f"player{i}.json")
                    if os.path.exists(player_path):
                        with open(player_path, "r", encoding="utf-8") as f:
                            p_data = json.load(f)
                        
                        if current_stage == "purchase":
                            # Возврат с закупки на утверждение
                            p_data["resources"] = {}
                            p_data["purchase_history"] = {}
                            p_data["finished_purchase"] = False
                            p_data["free_resources_added"] = False
                            p_data["stage"] = target_stage
                            
                            # Очищаем временные переменные закупки
                            temp_key = f"temp_purchase_{match_id}_{i}"
                            if temp_key in st.session_state:
                                del st.session_state[temp_key]
                        
                        elif current_stage == "protection":
                            # Возврат с защиты на закупку — ПОЛНЫЙ СБРОС
                            p_data["resources"] = {}
                            p_data["purchase_history"] = {}
                            p_data["protected_heroes"] = []
                            p_data["finished_protection"] = False
                            p_data["finished_purchase"] = False  # Сбрасываем флаг закупки тоже!
                            p_data["free_resources_added"] = False
                            p_data["stage"] = target_stage
                            
                            # Очищаем временные переменные защиты
                            temp_protection_key = f"temp_protection_{match_id}_{i}"
                            if temp_protection_key in st.session_state:
                                del st.session_state[temp_protection_key]
                            
                            temp_universal_key = f"temp_universal_{match_id}_{i}"
                            if temp_universal_key in st.session_state:
                                del st.session_state[temp_universal_key]
                            
                            temp_five_key = f"temp_five_{match_id}_{i}"
                            if temp_five_key in st.session_state:
                                del st.session_state[temp_five_key]
                            
                            # Также очищаем временные переменные закупки (если есть)
                            temp_purchase_key = f"temp_purchase_{match_id}_{i}"
                            if temp_purchase_key in st.session_state:
                                del st.session_state[temp_purchase_key]
                        
                        elif current_stage == "bans":
                            # Возврат с банов на защиту
                            p_data["bans"] = {}
                            p_data["finished_bans"] = False
                            p_data["stage"] = target_stage
                            p_data["resources"] = p_data.get("purchase_history", {}).copy()
                            p_data["protected_heroes"] = []
                            
                            # Очищаем временные переменные банов
                            temp_key = f"temp_bans_{match_id}_{i}"
                            if temp_key in st.session_state:
                                del st.session_state[temp_key]
                            
                            temp_universal_key = f"temp_universal_ban_{match_id}_{i}"
                            if temp_universal_key in st.session_state:
                                del st.session_state[temp_universal_key]
                            
                            temp_five_key = f"temp_five_ban_{match_id}_{i}"
                            if temp_five_key in st.session_state:
                                del st.session_state[temp_five_key]

                        elif current_stage == "picks":
                            # Возврат с пиков на баны
                            p_data["picks"] = [[None for _ in range(4)] for _ in range(tournament_config.get("rooms", 3))]
                            p_data["finished_picks"] = False
                            p_data["stage"] = target_stage
                            p_data["resources"] = p_data.get("purchase_history", {}).copy()
                            p_data["protected_heroes"] = []
                            p_data["bans"] = {}
                            
                            # Очищаем временные переменные пиков
                            temp_key = f"picks_temp_{match_id}_{i}"
                            if temp_key in st.session_state:
                                del st.session_state[temp_key]
                            
                            selected_pack_key = f"selected_pack_{match_id}_{i}"
                            if selected_pack_key in st.session_state:
                                del st.session_state[selected_pack_key]
                        
                        elif current_stage == "battle":
                            # Возврат с боя на пики
                            p_data["finished_battle"] = False
                            p_data["stage"] = target_stage
                            
                            # Очищаем результаты боёв
                            if "battle_results" in st.session_state:
                                del st.session_state.battle_results
                        
                        with open(player_path, "w", encoding="utf-8") as f:
                            json.dump(p_data, f, indent=2)
                
                tournament_config["stage"] = target_stage
                with open(config_path, "w", encoding="utf-8") as f:
                    json.dump(tournament_config, f, indent=2)
                
                del st.session_state.confirm_back
                st.success(f"✅ Возврат на этап {stage_names[target_stage]} выполнен!")
                st.rerun()
        
        with col_no:
            if st.button("❌ Нет, отмена"):
                del st.session_state.confirm_back
                st.rerun()
        
        st.stop()
    
    # Подтверждение принудительного перехода
    if st.session_state.get("confirm_force", False):
        st.warning("⚠️ ВНИМАНИЕ! Принудительный переход завершит текущий этап для всех игроков!")
        
        col_yes, col_no = st.columns(2)
        with col_yes:
            if st.button("✅ Да, принудительно перейти"):
                # Принудительно завершаем этап для всех игроков
                for i, player in enumerate(players, 1):
                    player_path = os.path.join(match_dir, f"player{i}.json")
                    if os.path.exists(player_path):
                        with open(player_path, "r", encoding="utf-8") as f:
                            p_data = json.load(f)
                        
                        if current_stage == "approval":
                            p_data["finished_approval"] = True
                        elif current_stage == "purchase":
                            p_data["finished_purchase"] = True
                        elif current_stage == "protection":
                            p_data["finished_protection"] = True
                        elif current_stage == "bans":
                            p_data["finished_bans"] = True
                        elif current_stage == "picks":
                            p_data["finished_picks"] = True
                        
                        with open(player_path, "w", encoding="utf-8") as f:
                            json.dump(p_data, f, indent=2)
                
                del st.session_state.confirm_force
                execute_stage_transition(match_dir, config_path, tournament_config, mode_config, players, current_stage, stages_order, stage_names, match_id)
                st.rerun()
        
        with col_no:
            if st.button("❌ Нет, отмена"):
                del st.session_state.confirm_force
                st.rerun()
        
        st.stop()
    
    st.divider()
    
    # ========== СОДЕРЖИМОЕ ТЕКУЩЕГО ЭТАПА ==========
    if current_stage == "approval":
        st.info("✅ Этап утверждения ростеров")
        judge_path = os.path.join(match_dir, "judge.json")
        if os.path.exists(judge_path):
            with open(judge_path, "r", encoding="utf-8") as f:
                judge_data = json.load(f)
            
            for player in players:
                status = judge_data.get("rosters_approval", {}).get(player, {}).get("status", "pending")
                if status == "approved":
                    st.success(f"✅ {player}: ростер подтверждён")
                elif status == "rejected":
                    st.error(f"❌ {player}: ростер отклонён")
                    if st.button(f"📋 Проверить исправленный ростер {player}", key=f"recheck_{player}_{match_id}"):
                        st.session_state.roster_check_match = match_id
                        st.session_state.roster_check_player = player
                        st.rerun()
                else:
                    st.warning(f"⏳ {player}: ожидает проверки")
                    if st.button(f"📋 Проверить ростер {player}", key=f"check_{player}_{match_id}"):
                        st.session_state.roster_check_match = match_id
                        st.session_state.roster_check_player = player
                        st.rerun()
    
    elif current_stage == "purchase":
        st.info("🛒 Этап закупки ресурсов")
        st.caption("Управление у игроков. Судья только наблюдает.")
    
    elif current_stage == "protection":
        st.info("🛡️ Этап защиты")
        st.caption("Управление у игроков. Судья только наблюдает.")
    
    elif current_stage == "bans":
        st.info("🔨 Этап банов")
        st.caption("Управление у игроков. Судья только наблюдает.")
    
    elif current_stage == "picks":
        st.info("⭐ Этап пиков")
        st.caption("Управление у игроков. Судья только наблюдает.")
    
    elif current_stage == "battle":
        st.info("⚔️ Этап боя")
        battle_interface()
    
    elif current_stage == "finished":
        st.success("🏆 Матч завершён!")
        st.balloons()

def judge_interface():
    # Если судья проверяет конкретный ростер
    if "roster_check_match" in st.session_state:
        judge_approve_roster(
            st.session_state.roster_check_match, 
            st.session_state.roster_check_player
        )
        return
    
    # Если выбран конкретный матч для управления
    if "current_match" in st.session_state:
        judge_match_interface(
            st.session_state.current_match,
            st.session_state.current_match_mode
        )
        return 
      
    st.markdown("## ⚖️ Панель судьи")

    if st.button("🚪 Выйти из аккаунта"):
        st.session_state.logged_in_as = None
        st.session_state.user_type = None
        st.session_state.nickname = None
        st.rerun()

    tab1, tab2 = st.tabs(["📋 Создать Матч", "🎮 Активные Матчи"])

    # ========== ВКЛАДКА 1: СОЗДАНИЕ МатчА ==========
    with tab1:
        st.subheader("🏓 Создание нового матча")
        
        # Получаем список доступных конфигов
        configs_dir = os.path.join("data", "configs")
        if not os.path.exists(configs_dir):
            st.error("Папка data/configs/ не найдена")
            return
        
        config_files = [f for f in os.listdir(configs_dir) if f.endswith(".json")]
        if not config_files:
            st.error("Нет файлов конфигурации в data/configs/")
            return
        
        # Выбор режима
        mode_options = {}
        for f in config_files:
            with open(os.path.join(configs_dir, f), "r", encoding="utf-8") as file:
                config = json.load(file)
                mode_options[f[:-5]] = config.get("name", f[:-5])
        
        selected_mode = st.selectbox(
            "Режим",
            options=list(mode_options.keys()),
            format_func=lambda x: mode_options[x]
        )
        
        # Загружаем конфиг выбранного режима
        with open(os.path.join(configs_dir, f"{selected_mode}.json"), "r", encoding="utf-8") as f:
            mode_config = json.load(f)
        
        players_needed = mode_config.get("players", 2)
        table_num = st.number_input("Номер стола (1–8)", 1, 8, 1)
        match_id = f"table_{table_num}"
        
        all_players = get_all_players()
        if not all_players:
            st.warning("Нет зарегистрированных игроков")
            return
        
        # Динамический выбор игроков
        selected_players = []
        cols = st.columns(min(players_needed, 4))
        
        for i in range(players_needed):
            with cols[i % len(cols)]:
                player = st.selectbox(
                    f"Игрок {i+1}", 
                    ["Не выбран"] + all_players, 
                    key=f"player_{selected_mode}_{i}"
                )
                if player != "Не выбран":
                    selected_players.append(player)
        
        if len(selected_players) != len(set(selected_players)):
            st.error("❌ Игроки не должны повторяться!")
        elif len(selected_players) == players_needed:
            if st.button("🚀 Запуск матча", type="primary", use_container_width=True):
                ok, msg = create_tournament(match_id, selected_mode, selected_players)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
        else:
            st.warning(f"⚠️ Нужно выбрать {players_needed} игроков (сейчас {len(selected_players)})")

    # ========== ВКЛАДКА 2: АКТИВНЫЕ МАТЧИ ==========
    with tab2:
        st.subheader("🎮 Активные матчи")
        tournaments = get_all_active_tournaments()
        
        if not tournaments:
            st.info("Нет активных матчей")
        else:
            for t in tournaments:
                with st.container(border=True):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.markdown(f"**{t['match_id']}**")
                        st.caption(f"Игроки: {', '.join(t['players'])}")
                        st.caption(f"Этап: {t['stage']}")
                    with col2:
                        if st.button("🎮 Управлять", key=f"manage_{t['match_id']}"):
                            st.session_state.current_match = t['match_id']
                            st.session_state.current_match_mode = t['mode']
                            st.rerun()
                    with col3:
                        if st.button("🗑️ Очистить", key=f"clear_{t['match_id']}"):
                            ok, msg = clear_tournament(t['match_id'])
                            if ok:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)
# ============================
# 7. Интерфейс игрока (профиль + активные матчи)
# ============================
def load_player_roster(nickname: str) -> dict:
    """Загружает ростер игрока из его профиля"""
    player_data = load_player(nickname)
    if not player_data:
        return {}
    return player_data.get("roster", {})

def display_all_rosters(match_id: str, players: list, current_player_num: int = None):
    """Отображает ростеры всех участников с возможностью переключения"""
    
    # Слайдер для количества колонок
    cols_per_row = st.slider(
        "Количество оперативников в строке",
        min_value=2,
        max_value=12,
        value=5,
        step=1,
        key=f"all_rosters_cols_{match_id}"
    )
    
    # Выбор игрока для просмотра
    player_names = [f"{i}. {p}" for i, p in enumerate(players, 1)]
    selected_idx = st.radio(
        "Выберите игрока",
        options=range(len(player_names)),
        format_func=lambda x: player_names[x],
        horizontal=True,
        key=f"roster_select_{match_id}"
    )
    
    selected_player = players[selected_idx]
    selected_num = selected_idx + 1
    
    # Загружаем ростер выбранного игрока из профиля
    roster = load_player_roster(selected_player)
    
    st.markdown(f"### Ростер: **{selected_player}**")
    
    # Собираем оперативников с уровнем для сортировки
    has_heroes = []
    for cid, info in CHARACTERS_DB.items():
        data = roster.get(str(cid), {"has": False})
        if data.get("has", False):
            level = data.get('level', 90)
            has_heroes.append((cid, info, data, level))
    
    # Сортировка: уровень ↓, редкость (6→5→4), имя ↑
    def get_rarity_order(rarity):
        return {"6⭐": 0, "5⭐": 1, "4⭐": 2}.get(rarity, 3)
    
    has_heroes.sort(key=lambda x: (-x[3], get_rarity_order(x[1]["rarity"]), x[1]["name"]))
    
    if not has_heroes:
        st.info("У этого игрока нет отмеченных оперативников")
    else:
        for i in range(0, len(has_heroes), cols_per_row):
            row = has_heroes[i:i + cols_per_row]
            cols = st.columns(len(row))
            for idx, (cid, info, data, level) in enumerate(row):
                with cols[idx]:
                    with st.container(border=True):
                        img_path = load_operator_image(info['name'])
                        if img_path:
                            st.image(img_path, width=70)
                        else:
                            st.write("🎴")
                        st.markdown(f"**{info['name']}**")
                        rank = 6 if info["rarity"] == "6⭐" else (5 if info["rarity"] == "5⭐" else 4)
                        potential = data.get('potential', 0)
                        st.caption(f"Lv.{level} | П{potential}")
    
    # Если это не свой ростер, показываем предупреждение
    if current_player_num is not None and selected_num != current_player_num:
        st.info("ℹ️ Это ростер противника. Учитывайте его при выборе банов и защит.")

def load_player_data(match_id: str, nickname: str) -> dict:
    """Загружает данные игрока из файла турнира по никнейму"""
    match_dir = os.path.join(TOURNAMENTS_DIR, match_id)
    for i in range(1, 5):
        player_path = os.path.join(match_dir, f"player{i}.json")
        if os.path.exists(player_path):
            with open(player_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data.get("nickname") == nickname:
                return data
    return {}

def participant_match_interface(match_id: str, mode: str, nickname: str):
    """Интерфейс участника внутри конкретного матча"""
    
    # Загружаем конфиг матча
    config_path = os.path.join(TOURNAMENTS_DIR, match_id, "config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        tournament_config = json.load(f)
    
    players = tournament_config.get("players", [])
    
    # Определяем номер игрока
    player_num = None
    for i, p in enumerate(players, 1):
        if p == nickname:
            player_num = i
            break
    
    if player_num is None:
        st.error("Вы не участвуете в этом матче")
        if st.button("🔙 Назад"):
            del st.session_state.current_match
            del st.session_state.current_match_mode
            del st.session_state.current_player_nickname
            st.rerun()
        return
    
    current_stage = tournament_config.get("stage", "resources")
    
    # Получаем актуальный конфиг режима
    mode_config = get_mode_config(mode)
    mode_name = mode_config.get("name", mode)
    
    # Шапка матча
    st.markdown(f"## 🎮 Матч: {match_id}")
    st.markdown(f"**Режим:** {mode_name}")
    st.markdown(f"**Участники:** {', '.join(players)}")
    st.markdown(f"**Текущий этап:** {current_stage.upper()}")
   
    # Загружаем данные игрока
    player_path = os.path.join(TOURNAMENTS_DIR, match_id, f"player{player_num}.json")
    with open(player_path, "r", encoding="utf-8") as f:
        player_data = json.load(f)
    
    # ========== ОТОБРАЖЕНИЕ РОСТЕРОВ ВСЕХ УЧАСТНИКОВ ==========
    with st.expander("📋 Ростеры участников", expanded=False):
        display_all_rosters(match_id, players, player_num)

    # В participant_match_interface, после ростера:

    # ========== НАЧАЛЬНЫЕ ПОКУПКИ (только на этапах защиты, банов, пиков) ==========
    if current_stage in ["protection", "bans", "picks"]:
        with st.expander("💰 Ресурсы участников", expanded=False):
            mode_config = get_mode_config(mode)
            
            resources_list = ["🛡️ Универсальная защита", "🔵 Защита 5⭐", "🔴 Универсальное воскрешение", 
                            "🔵 Воскрешение 5⭐", "🔴 Универсальный бан", "🔵 Бан 4-5⭐", "🔄 Рестарт"]
            
            players_data = {}
            for i, player in enumerate(players, 1):
                player_path_res = os.path.join(TOURNAMENTS_DIR, match_id, f"player{i}.json")
                if os.path.exists(player_path_res):
                    with open(player_path_res, "r", encoding="utf-8") as f:
                        p_data = json.load(f)
                else:
                    p_data = {}
                
                players_data[player] = p_data.get("purchase_history", {})
            
            table_data = []
            for res_name in resources_list:
                row = {"Ресурс": res_name}
                for player in players:
                    count = players_data.get(player, {}).get(res_name, 0)
                    row[player] = count if count > 0 else "—"
                table_data.append(row)
            
            st.dataframe(table_data, use_container_width=True, hide_index=True)

    # ========== ЗАЩИТА УЧАСТНИКОВ (только на этапах банов и пиков) ==========
    if current_stage in ["bans", "picks"]:
        with st.expander("🛡️ Защита участников", expanded=False):
            data = []
            for i, player in enumerate(players, 1):
                player_path = os.path.join(TOURNAMENTS_DIR, match_id, f"player{i}.json")
                if os.path.exists(player_path):
                    with open(player_path, "r", encoding="utf-8") as f:
                        p_data = json.load(f)
                else:
                    p_data = {}
                
                protected = p_data.get("protected_heroes", [])
                protected_names = []
                for hero_id in protected:
                    hero_info = CHARACTERS_DB.get(int(hero_id) if isinstance(hero_id, str) else hero_id, {})
                    protected_names.append(hero_info.get("name", "?"))
                
                data.append({
                    "Участник": player,
                    "Защищено": len(protected),
                    "Кто защищён": ", ".join(protected_names) if protected_names else "—"
                })
            
            st.dataframe(data, use_container_width=True, hide_index=True)
    
    # ========== БАНЫ УЧАСТНИКОВ (только на этапах пиков) ==========
    if current_stage == "picks":
        # Загружаем результаты банов из judge.json
        judge_path = os.path.join(TOURNAMENTS_DIR, match_id, "judge.json")
        ban_results = {}
        if os.path.exists(judge_path):
            with open(judge_path, "r", encoding="utf-8") as f:
                judge_data = json.load(f)
                ban_results = judge_data.get("ban_results", {})
        
        # Получаем данные о банах для текущего игрока
        if player_num == 1:
            my_ban_results = ban_results.get("p1", {})
            opponent_ban_results = ban_results.get("p2", {})
        else:
            my_ban_results = ban_results.get("p2", {})
            opponent_ban_results = ban_results.get("p1", {})
        
        # ========== EXPANDER: КТО ЧТО ЗАБАНИЛ ==========
        with st.expander("🔨 Кто что забанил", expanded=False):
            # Собираем данные о банах
            players_bans = {}
            for player in players:
                # Баны, поставленные противником (загружаем из его файла)
                for i, p in enumerate(players, 1):
                    if p == player:
                        opp_path = os.path.join(TOURNAMENTS_DIR, match_id, f"player{i}.json")
                        if os.path.exists(opp_path):
                            with open(opp_path, "r", encoding="utf-8") as f:
                                opp_data = json.load(f)
                            players_bans[player] = opp_data.get("bans", {})
                        break
            
            # Отображаем таблицу
            table_data = []
            for player, bans in players_bans.items():
                for hero_id, count in bans.items():
                    hero_info = CHARACTERS_DB.get(int(hero_id) if isinstance(hero_id, str) else hero_id, {})
                    hero_name = hero_info.get("name", "?")
                    table_data.append({
                        "Кто забанил": player,
                        "Кого забанил": hero_name,
                        "Количество банов": count
                    })
            
            if table_data:
                st.dataframe(table_data, use_container_width=True, hide_index=True)
            else:
                st.caption("— нет банов —")
        
        # ========== EXPANDER: КАКИХ ПЕРСОНАЖЕЙ ОТСТРЕЛИЛИ ==========
        with st.expander("❌ Каких персонажей отстрелили (недоступны)", expanded=False):
            banned_for_me = []
            for hero_id, is_available in my_ban_results.items():
                if not is_available:
                    hero_info = CHARACTERS_DB.get(int(hero_id) if isinstance(hero_id, str) else hero_id, {})
                    banned_for_me.append(hero_info.get("name", "?"))
            
            if banned_for_me:
                for name in sorted(banned_for_me):
                    st.write(f"❌ {name}")
            else:
                st.caption("— никто не отстрелен —")

    # Кнопки управления
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔙 Назад к профилю", key="back_to_profile", use_container_width=True):
            del st.session_state.current_match
            del st.session_state.current_match_mode
            del st.session_state.current_player_nickname
            st.rerun()
    with col2:
        if st.button("🔄 Обновить", key="refresh_match", use_container_width=True):
            st.rerun()

    st.divider()

    # ========== ОТОБРАЖЕНИЕ НУЖНОГО ЭТАПА ==========
    
    # ЭТАП 1: УТВЕРЖДЕНИЕ РОСТЕРОВ
    if current_stage == "approval":
        # Загружаем статус утверждения из judge.json
        judge_path = os.path.join(TOURNAMENTS_DIR, match_id, "judge.json")
        with open(judge_path, "r", encoding="utf-8") as f:
            judge_data = json.load(f)
        
        approval_status = judge_data["rosters_approval"].get(nickname, {}).get("status", "pending")
        
        if approval_status == "approved":
            st.success("✅ Ваш ростер подтверждён судьёй! Ожидайте начала закупки.")
            st.info("Судья переведёт вас на следующий этап.")
            return
        elif approval_status == "rejected":
            st.error("❌ Ваш ростер был отклонён судьёй!")
            st.warning("Пожалуйста, исправьте данные в ростере и нажмите 'Сохранить ростер'.")
            st.info("После исправления уведомите судью — он проверит заново.")
            
            # Показываем ростер для редактирования
            player_profile = load_player(nickname)
            roster = player_profile.get("roster", {})
            
            with st.expander("⭐ Мой ростер (оперативники, уровни, потенциалы)", expanded=True):
                cols_per_row = st.slider("Количество оперативников в строке", 2, 8, 5, key=f"roster_cols_edit_{match_id}")
                new_roster = display_roster_editor(roster, cols_per_row)
                if st.button("💾 Сохранить ростер"):
                    player_profile["roster"] = new_roster
                    save_player(nickname, player_profile)
                    st.success("Ростер сохранён! Уведомите судью о готовности.")
                    st.rerun()
            return
        else:  # pending
            st.info("⏳ Ожидайте проверки ростера судьёй.")
            st.caption("Судья проверит ваши данные и подтвердит их.")
            return
    
    # ЭТАП 2: ЗАКУПКА РЕСУРСОВ
    elif current_stage == "purchase":
        purchase_interface(match_id, player_num, player_data, tournament_config)
    
    # ЭТАП 3: ЗАЩИТА
    elif current_stage == "protection":
        protection_interface(match_id, player_num, player_data, tournament_config)
    
    # ЭТАП 4: БАНЫ
    elif current_stage == "bans":
        if tournament_config.get("mode", "").startswith("group"):
            # Групповой режим
            opponents = [p for p in players if p != nickname]
            bans_interface_group(match_id, player_num, player_data, tournament_config, opponents)
        else:
            # Обычный режим (1v1)
            bans_interface(match_id, player_num, player_data, tournament_config)
    
    # ЭТАП 5: ПИКИ
    elif current_stage == "picks":
        # Загружаем результаты банов из judge.json
        judge_path = os.path.join(TOURNAMENTS_DIR, match_id, "judge.json")
        ban_results = {}
        if os.path.exists(judge_path):
            with open(judge_path, "r", encoding="utf-8") as f:
                judge_data = json.load(f)
                ban_results = judge_data.get("ban_results", {})
        
        # Определяем, какие оперативники недоступны из-за банов
        if player_num == 1:
            my_ban_results = ban_results.get("p1", {})
        else:
            my_ban_results = ban_results.get("p2", {})
        
        # Загружаем ростер игрока
        roster = load_player_roster(nickname)
        
        available_heroes = []
        for cid, info in CHARACTERS_DB.items():
            data = roster.get(str(cid), {"has": False})
            if data.get("has", False):
                # Проверяем, не забанен ли оперативник
                is_available = my_ban_results.get(str(cid), True)
                if is_available:
                    available_heroes.append((str(cid), {
                        "name": info["name"],
                        "rarity": info["rarity"],
                        "level": data.get("level", 90),
                        "potential": data.get("potential", 0)
                    }))
        
        picks_interface(match_id, player_num, player_data, tournament_config, available_heroes)
    
    # ЭТАП 6: БОЙ
    elif current_stage == "battle":
        st.info("⚔️ Этап боя")
        st.caption("Ожидайте начала боя. Судья объявит результаты.")
        
    
    # ЭТАП 7: ЗАВЕРШЁН
    elif current_stage == "finished":
        st.success("🏆 Матч завершён!")
        st.balloons()
        
        if st.button("📊 Посмотреть результаты", use_container_width=True):
            # TODO: показать результаты матча
            pass
    
def purchase_interface(match_id: str, player_num: int, player_data: dict, tournament_config: dict):
    """Интерфейс закупки ресурсов для участника с кнопками + и -"""
    
    st.markdown("## 🛒 Этап закупки ресурсов")
    
    mode_config = get_mode_config(tournament_config["mode"])
    
    shop = mode_config.get("shop", {})
    limits = mode_config.get("limits", {})
    starting_points = mode_config.get("starting_points", 12)
    free_items = mode_config.get("free_items", {})

    max_total_resurrections = limits.get("max_total_resurrections", 99)
    
    current_resources = player_data.get("resources", {})
    
    # Вычисляем потраченные очки (только купленные, без бесплатных)
    spent_points = 0
    for res_name, count in current_resources.items():
        if res_name in shop:
            free_count = free_items.get(res_name, 0)
            purchased_count = max(0, count - free_count)
            spent_points += purchased_count * shop[res_name]["cost"]
    
    points = max(0, starting_points - spent_points)
    
    # Если закупка завершена, показываем режим просмотра
    if player_data.get("finished_purchase", False):
        st.success("✅ Ваша закупка сохранена!")
        st.info("Вы можете редактировать закупку до тех пор, пока судья не переведёт турнир.")
    
        st.markdown("### 📦 Ваша корзина покупок")
        for res_name, count in current_resources.items():
            if count > 0:
                st.write(f"{res_name}: {count}")
    
        if st.button("✏️ Редактировать закупку", key=f"edit_purchase_{player_num}"):
            player_data["finished_purchase"] = False
            player_path = os.path.join(TOURNAMENTS_DIR, match_id, f"player{player_num}.json")
            with open(player_path, "w", encoding="utf-8") as f:
                json.dump(player_data, f, indent=2)
    
            # Очищаем временное хранилище
            temp_key = f"temp_purchase_{match_id}_{player_num}"
            if temp_key in st.session_state:
                del st.session_state[temp_key]
    
            st.rerun()
        return
    
    # Временное хранилище для покупок в сессии
    temp_key = f"temp_purchase_{match_id}_{player_num}"
    if temp_key not in st.session_state:
        # Инициализируем временные покупки из текущих ресурсов (без вычитания бесплатных)
        temp_purchases = {}
        for res_name in shop.keys():
            # Берём количество из current_resources (это только купленные, потому что бесплатные ещё не добавлены)
            temp_purchases[res_name] = current_resources.get(res_name, 0)
        st.session_state[temp_key] = temp_purchases
    
    temp_purchases = st.session_state[temp_key]
    
    # Слайдер для количества колонок
    items_per_row = st.slider(
        "Количество ресурсов в строке",
        min_value=1,
        max_value=4,
        value=2,
        step=1,
        key=f"purchase_cols_{match_id}_{player_num}"
    )
    
    # Отображение доступных очков
    total_cost = sum(temp_purchases[res] * shop[res]["cost"] for res in shop.keys())
    remaining = starting_points - total_cost

    col1, col2 = st.columns(2)
    with col1:
        st.metric("💎 Всего очков", f"{starting_points}")
    with col2:
        st.metric("💎 Осталось очков", f"{remaining}")
    
    # Отображение лимита воскрешений
    current_resurrections = (
        temp_purchases.get("🔴 Универсальное воскрешение", 0) + 
        temp_purchases.get("🔵 Воскрешение 5⭐", 0)
    )
    st.metric("🔴+🔵 Воскрешения", f"{current_resurrections} / {max_total_resurrections}")
    if current_resurrections > max_total_resurrections:
        st.error("❌ Превышен лимит воскрешений!")
    
    st.divider()

        # Отображение бесплатных ресурсов
    if free_items:
        st.markdown("### 🎁 Бесплатные ресурсы (добавятся автоматически)")
        free_cols = st.columns(min(len(free_items), 4))
        for idx, (item_name, count) in enumerate(free_items.items()):
            with free_cols[idx % 4]:
                st.info(f"{item_name}: {count} шт.")
        st.divider()
    
    # Сетка ресурсов с кнопками + и -
    res_list = list(shop.items())
    
    for i in range(0, len(res_list), items_per_row):
        row = res_list[i:i + items_per_row]
        cols = st.columns(len(row))
        for idx, (res_name, res_info) in enumerate(row):
            with cols[idx]:
                with st.container(border=True):
                    st.markdown(f"**{res_name}**")
                    st.caption(res_info.get("description", ""))
                    st.caption(f"💰 Цена: {res_info['cost']} 💎")
                    
                    current_count = temp_purchases.get(res_name, 0)
                    resource_max = res_info.get("max", 99)
                    free_count = free_items.get(res_name, 0)
                    
                    # Уже есть бесплатные?
                    has_free = free_count > 0
                    
                    col_btn1, col_val, col_btn2 = st.columns([1, 2, 1])
                    
                    with col_btn1:
                        # Кнопка "-" (с затемнением при недоступности)
                        if current_count > 0:
                            if st.button("➖", key=f"minus_{res_name}_{player_num}", use_container_width=True):
                                temp_purchases[res_name] = current_count - 1
                                st.session_state[temp_key] = temp_purchases
                                st.rerun()
                        else:
                            st.button("➖", key=f"minus_disabled_{res_name}_{player_num}", disabled=True, use_container_width=True)
                    
                    with col_val:
                        st.markdown(f"<div style='text-align: center; font-size: 20px; font-weight: bold;'>{current_count}</div>", unsafe_allow_html=True)
                    
                    with col_btn2:
                        # Проверка возможности увеличения
                        can_increase = True
    
                        # Проверка лимита ресурса
                        if (current_count + 1) > resource_max:
                            can_increase = False
    
                        # Проверка очков
                        if can_increase and res_info["cost"] > remaining:
                            can_increase = False
    
                        # Проверка лимита воскрешений
                        if can_increase and res_name in ["🔴 Универсальное воскрешение", "🔵 Воскрешение 5⭐"]:
                            current_res = temp_purchases.get("🔴 Универсальное воскрешение", 0) + temp_purchases.get("🔵 Воскрешение 5⭐", 0)
                            if current_res + 1 > max_total_resurrections:
                                can_increase = False
    
                        if can_increase:
                            if st.button("➕", key=f"plus_{res_name}_{player_num}", use_container_width=True):
                                temp_purchases[res_name] = current_count + 1
                                st.session_state[temp_key] = temp_purchases
                                st.rerun()
                        else:
                            st.button("❌", key=f"plus_disabled_{res_name}_{player_num}", disabled=True, use_container_width=True)
    
    st.divider()
    
    # Итог
    total_cost = sum(temp_purchases[res] * shop[res]["cost"] for res in shop.keys())
    remaining = starting_points - total_cost
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("💰 Итого к оплате", total_cost)
    with col2:
        st.metric("💎 Останется очков", remaining)
    
    # Кнопки управления
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Сохранить закупку", type="primary", use_container_width=True):
            # Сохраняем покупки
            new_resources = {}
            for res_name, quantity in temp_purchases.items():
                if quantity > 0:
                    new_resources[res_name] = quantity

            player_data["resources"] = new_resources
            player_data["purchase_history"] = new_resources.copy()
            player_data["finished_purchase"] = True
            
                        
            player_path = os.path.join(TOURNAMENTS_DIR, match_id, f"player{player_num}.json")
            with open(player_path, "w", encoding="utf-8") as f:
                json.dump(player_data, f, indent=2)
            
            del st.session_state[temp_key]
            
            st.success("✅ Закупка сохранена!")
            st.balloons()
            time.sleep(1)
            st.rerun()
    
    with col2:
        if st.button("🔄 Сбросить всё", use_container_width=True):
            st.session_state[temp_key] = {res: 0 for res in shop.keys()}
            st.rerun()

def protection_interface(match_id: str, player_num: int, player_data: dict, tournament_config: dict):
    """Интерфейс этапа защиты для участника"""
    
    st.markdown("## 🛡️ Этап защиты оперативников")
    
    # Получаем конфиг режима
    mode_config = get_mode_config(tournament_config["mode"])
    free_items = mode_config.get("free_items", {})
    
    # Получаем ресурсы защиты
    resources = player_data.get("resources", {})
    universal_protection = resources.get("🛡️ Универсальная защита", 0)
    five_star_protection = resources.get("🔵 Защита 5⭐", 0)
    
    # Проверяем, есть ли ресурсы для защиты
    if universal_protection == 0 and five_star_protection == 0:
        st.warning("⚠️ У вас нет ресурсов для защиты оперативников!")
        if st.button("✅ Пропустить этап защиты", key=f"skip_protection_{player_num}", use_container_width=True):
            player_data["protected_heroes"] = []
            player_data["finished_protection"] = True
            player_path = os.path.join(TOURNAMENTS_DIR, match_id, f"player{player_num}.json")
            with open(player_path, "w", encoding="utf-8") as f:
                json.dump(player_data, f, indent=2)
            st.success("Этап защиты пропущен!")
            st.rerun()
        return
    
    # Загружаем ростер игрока
    nickname = player_data.get("nickname", "")
    roster = load_player_roster(nickname)
    
    # Разделяем оперативников по редкости
    six_star_heroes = []
    other_heroes = []
    
    for cid, info in CHARACTERS_DB.items():
        data = roster.get(str(cid), {"has": False})
        if data.get("has", False):
            level = data.get('level', 90)
            potential = data.get('potential', 0)
            if info["rarity"] == "6⭐":
                six_star_heroes.append((cid, info, level, potential))
            else:
                other_heroes.append((cid, info, level, potential))
    
    # Сортировка
    def get_rarity_order(rarity):
        return {"6⭐": 0, "5⭐": 1, "4⭐": 2}.get(rarity, 3)
    
    six_star_heroes.sort(key=lambda x: (-x[2], x[1]["name"]))
    other_heroes.sort(key=lambda x: (-x[2], get_rarity_order(x[1]["rarity"]), x[1]["name"]))
    
    # Получаем уже защищённых
    protected_heroes = player_data.get("protected_heroes", [])
    
    # Временное хранилище для защищённых
    temp_key = f"temp_protection_{match_id}_{player_num}"
    if temp_key not in st.session_state:
        st.session_state[temp_key] = protected_heroes.copy()
    
    temp_protected = st.session_state[temp_key]

    st.write(f"DEBUG: temp_protected = {temp_protected}")

    # ID для подсчёта
    six_star_ids = [c for c, _, _, _ in six_star_heroes]
    other_ids = [c for c, _, _, _ in other_heroes]
    
    # Подсчёт защищённых и доступных ресурсов
    protected_six = len([h for h in temp_protected if h in six_star_ids])
    protected_other = len([h for h in temp_protected if h in other_ids])
    
    available_universal = universal_protection - protected_six
    available_total = (universal_protection + five_star_protection) - (protected_six + protected_other)
    
    # Отображение ресурсов
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🛡️ Универсальная защита", f"{universal_protection}")
    with col2:
        st.metric("🔵 Защита 5⭐", f"{five_star_protection}")
    
    st.divider()
    
    # Слайдер для количества колонок
    cols_per_row = st.slider(
        "Количество оперативников в строке",
        min_value=2,
        max_value=8,
        value=5,
        step=1,
        key=f"protection_cols_{match_id}_{player_num}"
    )
    
    # Вкладки
    tab1, tab2 = st.tabs(["6⭐ Оперативники", "5-4⭐ Оперативники"])
    
    # Функция отображения сетки
    def render_protection_grid(heroes, is_six_star):
        if not heroes:
            st.info("Нет оперативников этой редкости")
            return
        
        for i in range(0, len(heroes), cols_per_row):
            row = heroes[i:i + cols_per_row]
            cols = st.columns(len(row))
            for idx, (cid, info, level, potential) in enumerate(row):
                with cols[idx]:
                    with st.container(border=True):
                        img_path = load_operator_image(info['name'])
                        if img_path:
                            st.image(img_path, width=70)
                        else:
                            st.write("🎴")
                        
                        st.markdown(f"**{info['name']}**")
                        st.caption(f"Lv.{level} | П{potential}")
                        
                        is_protected = cid in temp_protected
                        
                        if is_six_star:
                            if is_protected:
                                if st.checkbox("✅ Защищён", value=True, key=f"protect_{cid}_{player_num}"):
                                    pass
                                else:
                                    temp_protected.remove(cid)
                                    st.session_state[temp_key] = temp_protected
                                    st.rerun()
                            else:
                                if available_universal > 0:
                                    if st.checkbox("🛡️ Защитить", value=False, key=f"protect_{cid}_{player_num}"):
                                        temp_protected.append(cid)
                                        st.session_state[temp_key] = temp_protected
                                        st.rerun()
                                else:
                                    st.checkbox("🛡️ Защитить", value=False, disabled=True, key=f"protect_{cid}_{player_num}")
                        else:
                            if is_protected:
                                if st.checkbox("✅ Защищён", value=True, key=f"protect_{cid}_{player_num}"):
                                    pass
                                else:
                                    temp_protected.remove(cid)
                                    st.session_state[temp_key] = temp_protected
                                    st.rerun()
                            else:
                                # Определяем, какой ресурс будет использован
                                remaining_five = five_star_protection - protected_other
                                use_five = remaining_five > 0
                                
                                if use_five:
                                    text = "🔵 Защитить (5⭐)"
                                else:
                                    text = "🛡️ Защитить (Универсальная)"
                                
                                if available_total > 0:
                                    if st.checkbox(text, value=False, key=f"protect_{cid}_{player_num}"):
                                        temp_protected.append(cid)
                                        st.session_state[temp_key] = temp_protected
                                        st.rerun()
                                else:
                                    st.checkbox("🛡️ Защитить", value=False, disabled=True, key=f"protect_{cid}_{player_num}")
    
    with tab1:
        if universal_protection == 0:
            st.warning("🔒 У вас нет универсальных защит. Защита 6⭐ оперативников недоступна.")
        elif not six_star_heroes:
            st.info("Нет 6⭐ оперативников")
        else:
            if available_universal == 0:
                st.warning("⚠️ У вас закончились универсальные защиты!")
            render_protection_grid(six_star_heroes, True)
    
    with tab2:
        if not other_heroes:
            st.info("Нет 5⭐ или 4⭐ оперативников")
        else:
            if available_total == 0:
                st.warning("⚠️ У вас закончились все защиты!")
            elif five_star_protection - protected_other == 0 and available_total > 0:
                st.warning(f"⚠️ Защита 5⭐ кончилась, будет использована Универсальная (осталось: {available_universal})")
            render_protection_grid(other_heroes, False)
    
    # Статистика
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🛡️ Защищено 6⭐", protected_six)
    with col2:
        st.metric("🛡️ Защищено 5-4⭐", protected_other)
    
    # Кнопки управления
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Сохранить защиту", type="primary", use_container_width=True):
            player_data["protected_heroes"] = temp_protected
            player_data["finished_protection"] = True
            
            player_path = os.path.join(TOURNAMENTS_DIR, match_id, f"player{player_num}.json")
            with open(player_path, "w", encoding="utf-8") as f:
                json.dump(player_data, f, indent=2)
            
            # Используй проверку:
            if temp_key in st.session_state:
                del st.session_state[temp_key]

            temp_universal_key = f"temp_universal_{match_id}_{player_num}"
            if temp_universal_key in st.session_state:
                del st.session_state[temp_universal_key]

            temp_five_key = f"temp_five_{match_id}_{player_num}"
            if temp_five_key in st.session_state:
                del st.session_state[temp_five_key]
            
            st.success(f"✅ Защищено {len(temp_protected)} оперативников!")
            st.rerun()
    
    with col2:
        if st.button("🔄 Сбросить всё", use_container_width=True):
            st.session_state[temp_key] = []
            st.rerun()

def bans_interface(match_id: str, player_num: int, player_data: dict, tournament_config: dict):
    """Интерфейс этапа банов для 1v1 режима"""
    
    st.markdown("## 🔨 Этап банов")
    st.caption("Вы баните оперативников противника")
    
    # Определяем противника
    players = tournament_config.get("players", [])
    if player_num == 1:
        opponent_num = 2
    else:
        opponent_num = 1
    
    # Загружаем данные противника
    opponent_path = os.path.join(TOURNAMENTS_DIR, match_id, f"player{opponent_num}.json")
    with open(opponent_path, "r", encoding="utf-8") as f:
        opponent_data = json.load(f)
    
    opponent_nickname = opponent_data.get("nickname", "Противник")
    
    # Получаем ресурсы для банов (начальные)
    resources = player_data.get("resources", {})
    universal_ban = resources.get("🔴 Универсальный бан", 0)
    five_star_ban = resources.get("🔵 Бан 4-5⭐", 0)
    
    # Защита противника
    opponent_protected = opponent_data.get("protected_heroes", [])
    
    # Получаем уже поставленные баны
    current_bans = player_data.get("bans", {})
    
    # Загружаем ростер противника
    opponent_roster = load_player_roster(opponent_nickname)
    
    # Разделяем оперативников противника
    six_star_enemies = []
    other_enemies = []
    
    for cid, info in CHARACTERS_DB.items():
        data = opponent_roster.get(str(cid), {"has": False})
        if data.get("has", False):
            level = data.get('level', 90)
            potential = data.get('potential', 0)
            is_protected = cid in opponent_protected
            if info["rarity"] == "6⭐":
                six_star_enemies.append((cid, info, level, potential, is_protected))
            else:
                other_enemies.append((cid, info, level, potential, is_protected))
    
    # Сортировка
    six_star_enemies.sort(key=lambda x: x[1]["name"])
    other_enemies.sort(key=lambda x: x[1]["name"])
    
    # Временное хранилище для банов (только словарь банов)
    temp_key = f"temp_bans_{match_id}_{player_num}"
    if temp_key not in st.session_state:
        st.session_state[temp_key] = current_bans.copy()
    
    temp_bans = st.session_state[temp_key]
    
    # Отображение ресурсов (начальные, не меняются)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🔴 Универсальный бан", f"{universal_ban}")
    with col2:
        st.metric("🔵 Бан 4-5⭐", f"{five_star_ban}")
    
    st.divider()
    
    # Слайдер для количества колонок
    cols_per_row = st.slider(
        "Количество оперативников в строке",
        min_value=2,
        max_value=8,
        value=5,
        step=1,
        key=f"bans_cols_{match_id}_{player_num}"
    )
    
    # Функция для подсчёта забаненных
    def get_banned_counts():
        banned_6 = sum(1 for h in six_star_enemies if str(h[0]) in temp_bans)
        banned_other = sum(1 for h in other_enemies if str(h[0]) in temp_bans)
        return banned_6, banned_other
    
   
    # Вкладки
    tab1, tab2 = st.tabs(["⭐ 6⭐ Оперативники противника", "⭐⭐ 5-4⭐ Оперативники противника"])
    
    def render_ban_grid(heroes, is_six_star):
        if not heroes:
            st.info("Нет оперативников этой редкости")
            return
        
        # Подсчёт суммарных банов
        total_bans_6 = 0
        total_bans_all = 0
        
        # Считаем баны на 6⭐
        for cid, count in temp_bans.items():
            hero_id = int(cid) if isinstance(cid, str) else cid
            # Проверяем, является ли оперативник 6⭐
            is_6 = False
            for h in six_star_enemies:
                if h[0] == hero_id:
                    is_6 = True
                    break
            if is_6:
                total_bans_6 += count
            total_bans_all += count
        
        # Доступность ресурсов
        universal_ban_available = universal_ban - total_bans_6
        total_ban_available = (universal_ban + five_star_ban) - total_bans_all
        
        # Условия для 6⭐
        condition1 = universal_ban > total_bans_6
        condition2 = total_ban_available > 0
        
        # Для 5-4⭐ достаточно условия 2
        can_place_6 = condition1 and condition2
        can_place_other = total_ban_available > 0
        
        cols_per_row = st.session_state.get(f"bans_cols_{match_id}_{player_num}", 5)
        
        for i in range(0, len(heroes), cols_per_row):
            row = heroes[i:i + cols_per_row]
            cols = st.columns(len(row))
            for idx, (cid, info, level, potential, is_protected) in enumerate(row):
                with cols[idx]:
                    with st.container(border=True):
                        img_path = load_operator_image(info['name'])
                        if img_path:
                            st.image(img_path, width=70)
                        else:
                            st.write("🎴")
                        
                        st.markdown(f"**{info['name']}**")
                        st.caption(f"Lv.{level} | П{potential}")
                        
                        if is_protected:
                            st.info("🛡️ Защищён противником")
                        
                        current_ban = temp_bans.get(str(cid), 0)
                        
                        # Определяем, сколько чекбоксов нужно
                        max_bans = 2 if is_protected else 1
                        
                        # Для хранения состояния, выбран ли первый чекбокс
                        first_checked = current_ban >= 1
                        
                        # Чекбокс #1
                        # Доступность зависит от редкости
                        if is_six_star:
                            can_place = can_place_6
                        else:
                            can_place = can_place_other
                        
                        # Дополнительно: для второго чекбокса нужен первый
                        # Блокировка первого, если выбран второй
                        if current_ban >= 2:
                            can_place_first = False  # первый заблокирован
                        else:
                            can_place_first = can_place
                        
                        # Чекбокс #1
                        label1 = "🔫 Выстрелить" if is_protected else "🔨 Забанить"

                        # Первый чекбокс блокируется, если выбран второй
                        if current_ban >= 2:
                            st.checkbox(label1, value=True, disabled=True, key=f"ban1_{cid}_{player_num}")
                        else:
                            if first_checked:
                                # Уже выбран — можно снять всегда
                                if st.checkbox(label1, value=True, key=f"ban1_{cid}_{player_num}"):
                                    pass
                                else:
                                    del temp_bans[str(cid)]
                                    st.session_state[temp_key] = temp_bans
                                    st.rerun()
                            else:
                                # Не выбран — можно поставить только если есть ресурсы
                                if can_place_first:
                                    if st.checkbox(label1, value=False, key=f"ban1_{cid}_{player_num}"):
                                        temp_bans[str(cid)] = 1
                                        st.session_state[temp_key] = temp_bans
                                        st.rerun()
                                else:
                                    st.checkbox(label1, value=False, disabled=True, key=f"ban1_{cid}_{player_num}")
                        
                        # Чекбокс #2 (только если защищён)
                        if is_protected:
                            second_checked = current_ban >= 2
                            
                            # Оставшиеся ресурсы с учётом того, что второй бан ещё не потрачен
                            if not second_checked:
                                # Проверяем возможность поставить второй бан
                                temp_total_bans_6 = total_bans_6 + (1 if is_six_star else 0)
                                temp_total_bans_all = total_bans_all + 1
                            else:
                                # Уже есть второй бан, проверяем для снятия (всегда true)
                                temp_total_bans_6 = total_bans_6
                                temp_total_bans_all = total_bans_all
                            
                            remaining_universal = universal_ban - temp_total_bans_6
                            remaining_total = (universal_ban + five_star_ban) - temp_total_bans_all
                            
                            if is_six_star:
                                can_place_second = first_checked and (remaining_universal >= 0) and (remaining_total >= 0)
                            else:
                                can_place_second = first_checked and (remaining_total >= 0)
                            
                            if second_checked:
                                if st.checkbox("💀 Контрольный", value=True, key=f"ban2_{cid}_{player_num}"):
                                    pass
                                else:
                                    # Снимаем второй бан
                                    temp_bans[str(cid)] = 1
                                    st.session_state[temp_key] = temp_bans
                                    st.rerun()
                            else:
                                if can_place_second:
                                    if st.checkbox("💀 Контрольный", value=False, key=f"ban2_{cid}_{player_num}"):
                                        temp_bans[str(cid)] = 2
                                        st.session_state[temp_key] = temp_bans
                                        st.rerun()
                                else:
                                    st.checkbox("💀 Контрольный", value=False, disabled=True, key=f"ban2_{cid}_{player_num}")
                                    
    with tab1:
        if universal_ban == 0:
            st.warning("🔒 Вы не покупали 🔴 Универсальный бан. Бан 6⭐ оперативников недоступен.")
        elif not six_star_enemies:
            st.info("У противника нет 6⭐ оперативников")
        else:
            render_ban_grid(six_star_enemies, True)
    
    with tab2:
        if not other_enemies:
            st.info("У противника нет 5⭐ или 4⭐ оперативников")
        else:
            render_ban_grid(other_enemies, False)
    
    # Статистика
    st.divider()
    total_bans_6 = sum(count for cid, count in temp_bans.items() if int(cid) in [h[0] for h in six_star_enemies])
    total_bans_other = sum(count for cid, count in temp_bans.items() if int(cid) in [h[0] for h in other_enemies])

    total_used_universal = total_bans_6 + max(0, total_bans_other - five_star_ban)

    remaining_universal = max(0, universal_ban - total_used_universal)
    remaining_five = max(0, five_star_ban - total_bans_other)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("🔨 Забанено 6⭐", total_bans_6)
    with col2:
        st.metric("🔨 Забанено 5-4⭐", total_bans_other)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("🔴 Осталось универсальных", remaining_universal)
    with col2:
        st.metric("🔵 Осталось банов 5⭐", remaining_five)

    # Кнопки управления
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Сохранить баны", type="primary", use_container_width=True):
            # Пересчитываем остатки ресурсов
            total_bans_6 = sum(count for cid, count in temp_bans.items() if int(cid) in [h[0] for h in six_star_enemies])
            total_bans_other = sum(count for cid, count in temp_bans.items() if int(cid) in [h[0] for h in other_enemies])
            
            total_used_universal = total_bans_6 + max(0, total_bans_other - five_star_ban)
            remaining_universal = max(0, universal_ban - total_used_universal)
            remaining_five = max(0, five_star_ban - total_bans_other)
            
            player_data["bans"] = temp_bans
            player_data["finished_bans"] = True
            player_data["resources"]["🔴 Универсальный бан"] = remaining_universal
            player_data["resources"]["🔵 Бан 4-5⭐"] = remaining_five
            
            player_path = os.path.join(TOURNAMENTS_DIR, match_id, f"player{player_num}.json")
            with open(player_path, "w", encoding="utf-8") as f:
                json.dump(player_data, f, indent=2)
            
            del st.session_state[temp_key]
            
            st.success("✅ Баны сохранены!")
            st.balloons()
            time.sleep(1)
            st.rerun()
    
    with col2:
        if st.button("🔄 Сбросить всё", use_container_width=True):
            st.session_state[temp_key] = {}
            st.rerun()

def bans_interface_group(match_id: str, player_num: int, player_data: dict, tournament_config: dict, opponents: list):
    """Интерфейс этапа банов для группового режима"""
    
    st.markdown("## 🔨 Этап банов (групповой)")
    st.caption("Вы баните оперативников глобально — бан действует на всех противников")
    
    # Получаем ресурсы для банов
    resources = player_data.get("resources", {})
    universal_ban = resources.get("🔴 Универсальный бан", 0)
    five_star_ban = resources.get("🔵 Бан 4-5⭐", 0)
    
    # Получаем уже поставленные баны
    current_bans = player_data.get("bans", {})
    # Структура: {hero_id: {"count": int, "protected_owners": list}}
    
    # Загружаем защиту противников
    protected_by_opponent = {}
    for opp in opponents:
        opp_data = load_player_data(match_id, opp)
        opp_protected = opp_data.get("protected_heroes", [])
        for hero_id in opp_protected:
            if hero_id not in protected_by_opponent:
                protected_by_opponent[hero_id] = []
            protected_by_opponent[hero_id].append(opp)
    
    # Собираем всех оперативников от всех противников
    all_heroes = {}  # {hero_id: {"info": {}, "owners": [], "levels": {}, "potentials": {}}}
    
    for opp in opponents:
        roster = load_player_roster(opp)
        for cid, info in CHARACTERS_DB.items():
            data = roster.get(str(cid), {"has": False})
            if data.get("has", False):
                if cid not in all_heroes:
                    all_heroes[cid] = {
                        "info": info,
                        "owners": [],
                        "levels": {},
                        "potentials": {}
                    }
                all_heroes[cid]["owners"].append(opp)
                all_heroes[cid]["levels"][opp] = data.get("level", 90)
                all_heroes[cid]["potentials"][opp] = data.get("potential", 0)
    
    # Временное хранилище для банов
    temp_key = f"temp_bans_group_{match_id}_{player_num}"
    if temp_key not in st.session_state:
        st.session_state[temp_key] = current_bans.copy()
    if f"temp_universal_ban_{match_id}_{player_num}" not in st.session_state:
        st.session_state[f"temp_universal_ban_{match_id}_{player_num}"] = universal_ban
    if f"temp_five_ban_{match_id}_{player_num}" not in st.session_state:
        st.session_state[f"temp_five_ban_{match_id}_{player_num}"] = five_star_ban
    
    temp_bans = st.session_state[temp_key]
    temp_universal = st.session_state[f"temp_universal_ban_{match_id}_{player_num}"]
    temp_five = st.session_state[f"temp_five_ban_{match_id}_{player_num}"]
    
    # Отображение ресурсов
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🔴 Универсальный бан", f"{temp_universal}")
    with col2:
        st.metric("🔵 Бан 4-5⭐", f"{temp_five}")
    
    st.divider()
    
    # Слайдер для количества колонок
    cols_per_row = st.slider(
        "Количество оперативников в строке",
        min_value=1,
        max_value=4,
        value=2,
        step=1,
        key=f"bans_group_cols_{match_id}_{player_num}"
    )
    
    # Функция для отображения карточки оперативника
    def render_hero_card(hero_id, hero_data):
        info = hero_data["info"]
        owners = hero_data["owners"]
        levels = hero_data["levels"]
        potentials = hero_data["potentials"]
        
        # Текущее количество банов
        current_count = temp_bans.get(str(hero_id), {}).get("count", 0)
        
        # Проверяем, есть ли защита у кого-то из владельцев
        protected_owners = protected_by_opponent.get(hero_id, [])
        has_protection = len(protected_owners) > 0
        
        # Определяем доступность кнопок
        can_ban_1 = False
        can_ban_2 = False
        
        # Проверка ресурсов для 1 бана
        if info["rarity"] == "6⭐":
            can_ban_1 = temp_universal >= 1
            can_ban_2 = temp_universal >= 2
        else:
            can_ban_1 = (temp_five >= 1) or (temp_universal >= 1)
            can_ban_2 = (temp_five + temp_universal) >= 2
        
        # Если уже есть баны, блокируем кнопки
        if current_count >= 2:
            can_ban_1 = False
            can_ban_2 = False
        elif current_count >= 1:
            can_ban_1 = False
        
        with st.container(border=True):
            # Фото
            img_path = load_operator_image(info['name'])
            if img_path:
                st.image(img_path, width=80)
            else:
                st.write("🎴")
            
            # Имя и характеристики
            st.markdown(f"**{info['name']}**")
            rank = 6 if info["rarity"] == "6⭐" else (5 if info["rarity"] == "5⭐" else 4)
            # Показываем средний уровень или первый
            first_owner = owners[0] if owners else None
            avg_level = levels[first_owner] if first_owner else 90
            avg_potential = potentials[first_owner] if first_owner else 0
            st.caption(f"{info['rarity']} | Lv.{avg_level} | П{avg_potential}")
            
            # Владельцы
            st.markdown("**Владельцы:**")
            for owner in owners:
                level = levels.get(owner, 90)
                potential = potentials.get(owner, 0)
                is_protected = owner in protected_owners
                protection_icon = "🛡️" if is_protected else "❌"
                st.caption(f"{protection_icon} {owner} (Lv.{level} | П{potential})")
            
            # Баны
            st.markdown("---")
            col1, col2 = st.columns(2)
            
            with col1:
                if current_count >= 1:
                    st.button("🔫 Застрелить (1)", disabled=True, key=f"ban1_{hero_id}_{player_num}", use_container_width=True)
                else:
                    if st.button("🔫 Застрелить (1)", disabled=not can_ban_1, key=f"ban1_{hero_id}_{player_num}", use_container_width=True):
                        # Тратим ресурс
                        if info["rarity"] == "6⭐":
                            temp_universal -= 1
                        else:
                            if temp_five > 0:
                                temp_five -= 1
                            else:
                                temp_universal -= 1
                        
                        # Сохраняем бан
                        temp_bans[str(hero_id)] = {"count": 1, "protected_owners": protected_owners}
                        st.session_state[temp_key] = temp_bans
                        st.session_state[f"temp_universal_ban_{match_id}_{player_num}"] = temp_universal
                        st.session_state[f"temp_five_ban_{match_id}_{player_num}"] = temp_five
                        st.rerun()
            
            with col2:
                if current_count >= 2:
                    st.button("💀 Контрольный (2)", disabled=True, key=f"ban2_{hero_id}_{player_num}", use_container_width=True)
                else:
                    if st.button("💀 Контрольный (2)", disabled=not can_ban_2, key=f"ban2_{hero_id}_{player_num}", use_container_width=True):
                        # Тратим 2 ресурса
                        if info["rarity"] == "6⭐":
                            temp_universal -= 2
                        else:
                            remaining_five = temp_five
                            if remaining_five >= 2:
                                temp_five -= 2
                            elif remaining_five == 1:
                                temp_five = 0
                                temp_universal -= 1
                            else:
                                temp_universal -= 2
                        
                        # Сохраняем бан
                        temp_bans[str(hero_id)] = {"count": 2, "protected_owners": protected_owners}
                        st.session_state[temp_key] = temp_bans
                        st.session_state[f"temp_universal_ban_{match_id}_{player_num}"] = temp_universal
                        st.session_state[f"temp_five_ban_{match_id}_{player_num}"] = temp_five
                        st.rerun()
            
            # Если уже есть баны, показываем счётчик
            if current_count > 0:
                st.info(f"✅ Забанен (уровень бана: {current_count})")
    
    # Сортируем оперативников по редкости
    heroes_6star = {k: v for k, v in all_heroes.items() if v["info"]["rarity"] == "6⭐"}
    heroes_5star = {k: v for k, v in all_heroes.items() if v["info"]["rarity"] == "5⭐"}
    heroes_4star = {k: v for k, v in all_heroes.items() if v["info"]["rarity"] == "4⭐"}
    
    # Сортировка по имени
    heroes_6star = dict(sorted(heroes_6star.items(), key=lambda x: x[1]["info"]["name"]))
    heroes_5star = dict(sorted(heroes_5star.items(), key=lambda x: x[1]["info"]["name"]))
    heroes_4star = dict(sorted(heroes_4star.items(), key=lambda x: x[1]["info"]["name"]))
    
    # Отображение вкладок
    tab1, tab2, tab3 = st.tabs(["⭐ 6⭐ Оперативники", "⭐⭐ 5⭐ Оперативники", "⭐⭐⭐ 4⭐ Оперативники"])
    
    def render_grid(heroes_dict):
        hero_list = list(heroes_dict.items())
        for i in range(0, len(hero_list), cols_per_row):
            row = hero_list[i:i + cols_per_row]
            cols = st.columns(len(row))
            for idx, (hero_id, hero_data) in enumerate(row):
                with cols[idx]:
                    render_hero_card(hero_id, hero_data)
    
    with tab1:
        if heroes_6star:
            render_grid(heroes_6star)
        else:
            st.info("Нет 6⭐ оперативников у противников")
    
    with tab2:
        if heroes_5star:
            render_grid(heroes_5star)
        else:
            st.info("Нет 5⭐ оперативников у противников")
    
    with tab3:
        if heroes_4star:
            render_grid(heroes_4star)
        else:
            st.info("Нет 4⭐ оперативников у противников")
    
    # Кнопки управления
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Сохранить баны", type="primary", use_container_width=True):
            player_data["bans"] = temp_bans
            player_data["finished_bans"] = True
            # Обновляем ресурсы
            player_data["resources"]["🔴 Универсальный бан"] = temp_universal
            player_data["resources"]["🔵 Бан 4-5⭐"] = temp_five
            
            player_path = os.path.join(TOURNAMENTS_DIR, match_id, f"player{player_num}.json")
            with open(player_path, "w", encoding="utf-8") as f:
                json.dump(player_data, f, indent=2)
            
            # Очищаем временные данные
            del st.session_state[temp_key]
            del st.session_state[f"temp_universal_ban_{match_id}_{player_num}"]
            del st.session_state[f"temp_five_ban_{match_id}_{player_num}"]
            
            st.success("✅ Баны сохранены!")
            st.balloons()
            time.sleep(1)
            st.rerun()
    
    with col2:
        if st.button("🔄 Сбросить всё", use_container_width=True):
            temp_key = f"temp_purchase_{match_id}_{player_num}"
            if temp_key in st.session_state:
                del st.session_state[temp_key]
            st.rerun()

def picks_interface(match_id: str, player_num: int, player_data: dict, tournament_config: dict, available_heroes: list):
    """Интерфейс выбора пиков (3 пачки по 4 оперативника)"""
    
    st.markdown("## ⭐ Этап пиков оперативников")
    
    # Получаем ресурсы воскрешений
    resources = player_data.get("resources", {})
    universal_resurrection = resources.get("🔴 Универсальное воскрешение", 0)
    five_star_resurrection = resources.get("🔵 Воскрешение 5⭐", 0)
    total_resurrections = universal_resurrection + five_star_resurrection
    
    # Получаем текущие пики
    current_picks = player_data.get("picks", [[None for _ in range(4)] for _ in range(3)])
    
    # Временное хранилище
    temp_key = f"picks_temp_{match_id}_{player_num}"
    if temp_key not in st.session_state:
        st.session_state[temp_key] = [row[:] for row in current_picks]
    if f"selected_pack_{match_id}_{player_num}" not in st.session_state:
        st.session_state[f"selected_pack_{match_id}_{player_num}"] = None
    
    picks = st.session_state[temp_key]
    selected_pack = st.session_state[f"selected_pack_{match_id}_{player_num}"]
    
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
        # Находим информацию об оперативнике
        hero_info = None
        for cid, info in CHARACTERS_DB.items():
            if str(cid) == hero_id:
                hero_info = info
                break
        if hero_info:
            if hero_info["rarity"] == "6⭐":
                unique_six.add(hero_id)
                total_six += count
            elif hero_info["rarity"] == "5⭐":
                unique_five.add(hero_id)
                total_five += count
    
    # Повторные использования
    repeats_six = total_six - len(unique_six)
    repeats_total = (total_six + total_five) - (len(unique_six) + len(unique_five))
    
    # Доступные воскрешения для 5⭐ (за вычетом использованных на 6⭐)
    available_for_five = total_resurrections - repeats_six
    
    # Отображение статистики лимитов
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🔴 Универсальное", universal_resurrection)
    with col2:
        st.metric("🔵 Воскрешение 5⭐", five_star_resurrection)
    with col3:
        if repeats_six > universal_resurrection:
            st.metric("⭐ 6⭐ повторы", f"{repeats_six}/{universal_resurrection}", delta="!❌!", delta_color="inverse")
        else:
            remaining_six = universal_resurrection - repeats_six
            st.metric("⭐ 6⭐ повторы", f"{repeats_six}/{universal_resurrection}", delta=f"осталось {remaining_six}")
    with col4:
        if repeats_total > total_resurrections:
            st.metric("⭐⭐ повторы (5⭐)", f"{repeats_total}/{total_resurrections}", delta="!❌!", delta_color="inverse")
        else:
            remaining_total = total_resurrections - repeats_total
            st.metric("⭐⭐ повторы (5⭐)", f"{repeats_total}/{total_resurrections}", delta=f"осталось {remaining_total}")
    
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
            # Слайдер для количества колонок
            cols_per_row = st.slider(
                "Количество оперативников в строке",
                min_value=2,
                max_value=8,
                value=5,
                step=1,
                key=f"picks_cols_{match_id}_{player_num}"
            )
            
            hero_list = available_heroes
            
            for i in range(0, len(hero_list), cols_per_row):
                row_heroes = hero_list[i:i + cols_per_row]
                cols = st.columns(len(row_heroes))
                
                for idx, (hero_id, hero_info) in enumerate(row_heroes):
                    with cols[idx]:
                        with st.container(border=True):
                            img_path = load_operator_image(hero_info['name'])
                            if img_path:
                                st.image(img_path, width=60)
                            else:
                                st.write("🎴")
                            
                            rank = 6 if hero_info["rarity"] == "6⭐" else (5 if hero_info["rarity"] == "5⭐" else 4)
                            st.markdown(f"**{hero_info['name']}**")
                            st.caption(f"Lv.{hero_info.get('level', 90)} | П{hero_info.get('potential', 0)}")
                            
                            count = usage_count.get(hero_id, 0)
                            
                            # Проверка возможности добавления
                            can_add = True
                            reason = ""
                            
                            if selected_pack is not None:
                                is_duplicate = hero_id in picks[selected_pack]
                                if is_duplicate:
                                    can_add = False
                                    reason = "уже в пачке"
                                else:
                                    if hero_info["rarity"] == "6⭐":
                                        if count > 0:
                                            # Проверяем лимит 6⭐
                                            if repeats_six >= universal_resurrection:
                                                can_add = False
                                                reason = "нет универсальных воскрешений"
                                    elif hero_info["rarity"] == "5⭐":
                                        if count > 0:
                                            # Проверяем лимит 5⭐
                                            if repeats_total >= total_resurrections:
                                                can_add = False
                                                reason = "нет воскрешений"
                                    # 4⭐ всегда можно
                            
                            if selected_pack is not None:
                                is_duplicate = hero_id in picks[selected_pack]
                                if is_duplicate:
                                    st.button(f"❌", key=f"hero_dup_{hero_id}_{player_num}_{i}_{idx}", disabled=True, use_container_width=True)
                                elif not can_add:
                                    st.button(f"🚫", key=f"hero_blocked_{hero_id}_{player_num}_{i}_{idx}", disabled=True, use_container_width=True)
                                    st.caption(reason)
                                else:
                                    if st.button(f"➕", key=f"hero_add_{hero_id}_{player_num}_{i}_{idx}", use_container_width=True):
                                        # Находим первый свободный слот в выбранной пачке
                                        first_empty = None
                                        for slot_idx in range(4):
                                            if picks[selected_pack][slot_idx] is None:
                                                first_empty = slot_idx
                                                break
                                        
                                        if first_empty is not None:
                                            picks[selected_pack][first_empty] = hero_id
                                            st.session_state[temp_key] = picks
                                            st.success(f"✅ {hero_info['name']} добавлен в пачку {selected_pack + 1}")
                                            st.rerun()
                                        else:
                                            st.error(f"❌ В пачке {selected_pack + 1} нет свободных слотов!")
                            else:
                                st.button(f"🔒", key=f"hero_disabled_{hero_id}_{player_num}_{i}_{idx}", disabled=True, use_container_width=True)
    
    # ========== ПРАВАЯ ЧАСТЬ: ТАБЛИЦА ПИКОВ ==========
    with right_col:
        st.markdown("### 🎮 Пачки")
        st.caption("Кнопка: выбор/очистка пачки")
        
        for pack_idx in range(3):
            cols = st.columns(5)
            
            with cols[0]:
                if selected_pack == pack_idx:
                    button_type = "primary"
                    button_text = f"✅ Пачка {pack_idx + 1}"
                else:
                    button_type = "secondary"
                    button_text = f"📦 Пачка {pack_idx + 1}"
                
                if st.button(button_text, key=f"pack_btn_{pack_idx}_{match_id}_{player_num}", use_container_width=True, type=button_type):
                    if selected_pack == pack_idx:
                        # Очистка всей пачки
                        picks[pack_idx] = [None, None, None, None]
                        st.session_state[temp_key] = picks
                        st.session_state[f"selected_pack_{match_id}_{player_num}"] = None
                        st.success(f"Пачка {pack_idx + 1} очищена")
                        st.rerun()
                    else:
                        st.session_state[f"selected_pack_{match_id}_{player_num}"] = pack_idx
                        st.rerun()
            
            for slot_idx in range(4):
                with cols[slot_idx + 1]:
                    current_hero_id = picks[pack_idx][slot_idx]
                    
                    with st.container(border=True):
                        if current_hero_id:
                            # Находим информацию об оперативнике
                            hero_info = None
                            for cid, info in CHARACTERS_DB.items():
                                if str(cid) == current_hero_id:
                                    hero_info = info
                                    break
                            
                            if hero_info:
                                img = load_operator_image(hero_info['name'])
                                if img:
                                    st.image(img, width=50)
                                else:
                                    st.write("🎴")
                                
                                rank = 6 if hero_info["rarity"] == "6⭐" else (5 if hero_info["rarity"] == "5⭐" else 4)
                                st.markdown(f"**{hero_info['name'][:12]}**")
                                st.caption(f"Lv.{hero_info.get('level', 0)} | П{hero_info.get('potential', 0)}")
                            else:
                                st.markdown("*???*")
                        else:
                            st.markdown("*⬜*")
                            st.caption(f"слот {slot_idx + 1}")
        
        st.divider()
        
        # Статистика пачек
        packs_ready = 0
        for pack_idx in range(3):
            if any(picks[pack_idx][slot] is not None for slot in range(4)):
                packs_ready += 1
        
        total_filled = sum(1 for pack in picks for slot in pack if slot is not None)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Заполнено слотов", f"{total_filled}/12")
        with col2:
            if packs_ready == 3:
                st.success(f"✅ Пачек готово: {packs_ready}/3")
            else:
                st.warning(f"⚠️ Пачек готово: {packs_ready}/3")
    
    # ========== КНОПКИ УПРАВЛЕНИЯ ==========
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Сбросить всё", key=f"reset_picks_{match_id}_{player_num}", use_container_width=True):
            st.session_state[temp_key] = [[None for _ in range(4)] for _ in range(3)]
            st.session_state[f"selected_pack_{match_id}_{player_num}"] = None
            st.rerun()
    
    with col2:
        if st.button("✅ Сохранить пики", type="primary", use_container_width=True):
            # Валидация
            errors = []
            
            # Проверка: в каждой пачке должен быть хотя бы 1 оперативник
            empty_packs = []
            for pack_idx in range(3):
                if all(picks[pack_idx][slot] is None for slot in range(4)):
                    empty_packs.append(pack_idx + 1)
            
            if empty_packs:
                errors.append(f"❌ Пачка {', '.join(map(str, empty_packs))} пустая. В каждой пачке должен быть хотя бы 1 оперативник!")
            
            # Проверка дубликатов в пачках
            for pack_idx, pack in enumerate(picks):
                seen = set()
                for hero_id in pack:
                    if hero_id:
                        if hero_id in seen:
                            errors.append(f"❌ Дубликат в пачке {pack_idx + 1}")
                            break
                        seen.add(hero_id)
            
            # Финальный подсчёт повторов для проверки лимитов
            final_usage = {}
            for pack in picks:
                for hero_id in pack:
                    if hero_id:
                        final_usage[hero_id] = final_usage.get(hero_id, 0) + 1
            
            final_unique_six = set()
            final_unique_five = set()
            final_six_usage = 0
            final_five_usage = 0
            
            for hero_id, count in final_usage.items():
                # Находим информацию об оперативнике
                hero_info = None
                for cid, info in CHARACTERS_DB.items():
                    if str(cid) == hero_id:
                        hero_info = info
                        break
                if hero_info:
                    if hero_info["rarity"] == "6⭐":
                        final_unique_six.add(hero_id)
                        final_six_usage += count
                    elif hero_info["rarity"] == "5⭐":
                        final_unique_five.add(hero_id)
                        final_five_usage += count
            
            final_repeats_six = final_six_usage - len(final_unique_six)
            final_repeats_total = (final_six_usage + final_five_usage) - (len(final_unique_six) + len(final_unique_five))
            
            if final_repeats_six > universal_resurrection:
                errors.append(f"❌ Превышен лимит 6⭐: {final_repeats_six} повторов, доступно {universal_resurrection}")
            
            if final_repeats_total > total_resurrections:
                errors.append(f"❌ Превышен лимит воскрешений: {final_repeats_total} повторов, доступно {total_resurrections}")
            
            if errors:
                for err in errors:
                    st.error(err)
            else:
                player_data["picks"] = picks
                player_data["finished_picks"] = True
                
                player_path = os.path.join(TOURNAMENTS_DIR, match_id, f"player{player_num}.json")
                with open(player_path, "w", encoding="utf-8") as f:
                    json.dump(player_data, f, indent=2)
                
                # Очищаем временные данные
                del st.session_state[temp_key]
                del st.session_state[f"selected_pack_{match_id}_{player_num}"]
                
                st.success("✅ Пачки сохранены!")
                st.balloons()
                time.sleep(1)
                st.rerun()

def player_interface():
    nickname = st.session_state.nickname
    
    # Если выбран конкретный матч
    if "current_match" in st.session_state:
        participant_match_interface(
            st.session_state.current_match,
            st.session_state.current_match_mode,
            nickname
        )
        return
        
    st.markdown(f"## 🎮 Профиль игрока: **{nickname}**")

    # Кнопки управления
    col1, col2 = st.columns([4, 1])
    with col1:
        if st.button("🚪 Выйти из аккаунта", use_container_width=True):
            st.session_state.logged_in_as = None
            st.session_state.user_type = None
            st.session_state.nickname = None
            st.rerun()
    with col2:
        if st.button("🔄 Обновить", use_container_width=True):
            st.rerun()

    st.divider()

    # Загружаем данные игрока
    player_data = load_player(nickname)
    if not player_data:
        st.error("Ошибка загрузки профиля")
        return

    # Вкладка "Мой ростер"
    with st.expander("⭐ Мой ростер (оперативники, уровни, потенциалы)", expanded=True):
        
        new_roster = display_roster_editor(player_data.get("roster", {}))
        if st.button("💾 Сохранить ростер"):
            player_data["roster"] = new_roster
            save_player(nickname, player_data)
            st.success("Ростер сохранён")

    st.divider()

    # Активные матчи
    st.subheader("🏆 Ваши активные матчи")
    tournaments = get_active_tournaments_for_player(nickname)
    if not tournaments:
        st.info("Вы не участвуете ни в одном матче.")
        return

    for t in tournaments:
        with st.container(border=True):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"**{t['match_id']}** ({t['mode'].upper()})")
                st.write(f"Противники: {', '.join(t['opponents'])}")
            with col2:
                stage_names = {
                    "approval": "Утверждение ростеров",
                    "purchase": "Закупка",
                    "protection": "Защита",
                    "bans": "Баны",
                    "picks": "Пики",
                    "battle": "Бой",
                    "finished": "Завершён"
                }
                st.metric("Этап", stage_names.get(t['stage'], t['stage']))
            with col3:
                if t['stage'] == "approval":
                    st.info("Ожидайте подтверждения судьи")
                else:
                    if st.button("🎮 Войти", key=f"enter_{t['match_id']}"):
                        st.session_state.current_match = t['match_id']
                        st.session_state.current_match_mode = t['mode']
                        st.session_state.current_player_nickname = nickname
                        st.rerun()

# ============================
# 8. Главная точка входа
# ============================

def main():
    st.set_page_config(page_title="Arknights: Endfield Tournament", layout="wide")
    st.title("⚔️ Arknights: Endfield Tournament Manager")
    st.caption("Система банов и пиков оперативников")
    st.divider()

    # Инициализация состояния
    if "logged_in_as" not in st.session_state:
        st.session_state.logged_in_as = None
    if "user_type" not in st.session_state:
        st.session_state.user_type = None
    if "nickname" not in st.session_state:
        st.session_state.nickname = None

    # Если уже вошли – показываем соответствующий интерфейс
    if st.session_state.logged_in_as == "player":
        player_interface()
        return
    elif st.session_state.logged_in_as == "judge":
        judge_interface()
        return

    # ------------------- Главное меню (вход / регистрация) -------------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎮 Участник")
        with st.form("player_login_form"):
            p_nick = st.text_input("Никнейм")
            p_pass = st.text_input("Пароль", type="password")
            col_login, col_reg = st.columns(2)
            with col_login:
                submitted_login = st.form_submit_button("🔑 Войти")
            with col_reg:
                submitted_reg = st.form_submit_button("📝 Зарегистрироваться")
            if submitted_login:
                ok, msg = authenticate_player(p_nick, p_pass)
                if ok:
                    st.session_state.logged_in_as = "player"
                    st.session_state.user_type = "player"
                    st.session_state.nickname = p_nick
                    st.rerun()
                else:
                    st.error(msg)
            if submitted_reg:
                ok, msg = register_player(p_nick, p_pass)
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)

    with col2:
        st.markdown("### ⚖️ Судья")
        with st.form("judge_login_form"):
            j_login = st.text_input("Логин")
            j_pass = st.text_input("Пароль", type="password")
            submitted_judge = st.form_submit_button("🔑 Войти как судья")
            if submitted_judge:
                ok, msg = authenticate_judge(j_login, j_pass)
                if ok:
                    st.session_state.logged_in_as = "judge"
                    st.session_state.user_type = "judge"
                    st.session_state.nickname = j_login
                    st.rerun()
                else:
                    st.error(msg)

    st.divider()
    st.caption("Для судей: создайте файл data/judges.json со структурой {\"логин\": \"хеш_пароля\"}")

if __name__ == "__main__":
    main()