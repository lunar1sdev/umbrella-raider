# Copyright (c) 2024-2026 Cwelium Inc.
# GUI Version by Kiro AI

import customtkinter as ctk
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import threading
import json
import os
import time
from datetime import datetime
from Cwelium import Raider, Files, scrape
import websocket

# Initialize files
Files.run_tasks()

# Load config
with open("config.json") as f:
    Config = json.load(f)

# Translations
TRANSLATIONS = {
    "en": {
        "title": "UMBRELLA RAIDER",
        "tokens": "Tokens",
        "proxies": "Proxies",
        "activity_log": "Activity Log",
        "clear_log": "Clear Log",
        "stop_all": "Stop All Actions",
        "info": "Info",
        "language": "Language",
        
        # Tabs
        "tab_token": "Token Management",
        "tab_server": "Server Actions",
        "tab_user": "User Actions",
        "tab_voice": "Voice Actions",
        "tab_advanced": "Advanced",
        
        # Token Management
        "load_tokens": "Load Tokens from File",
        "check_tokens": "Check Tokens",
        "format_tokens": "Format Tokens",
        "add_tokens": "Add Tokens (one per line):",
        "save_tokens": "Save Tokens",
        
        # Server Actions
        "invite_code": "Server Invite Code:",
        "join_server": "Join Server",
        "guild_id": "Guild ID:",
        "leave_server": "Leave Server",
        "channel_id": "Channel ID:",
        "message": "Message:",
        "start_spam": "Start Spamming",
        "thread_name": "Thread Name:",
        "thread_spam": "Start Thread Spam",
        "mass_ping": "Mass Ping (Guild ID for scraping):",
        "ping_count": "Ping Count:",
        "random_str": "Add Random String",
        "delay": "Delay (seconds):",
        
        # User Actions
        "user_id": "User ID:",
        "dm_message": "DM Message:",
        "dm_spam": "Start DM Spam",
        "new_bio": "New Bio:",
        "change_bio": "Change Bio",
        "username": "Username:",
        "friend_spam": "Send Friend Request",
        "call_spam": "Start Call Spam",
        "nickname": "Nickname:",
        "change_nick": "Change Nickname in Guild",
        "start_typing": "Start Typing Effect",
        
        # Voice Actions
        "voice_channel_id": "Voice Channel ID:",
        "join_vc": "Join Voice Channel",
        "set_online": "Set All Tokens Online",
        "soundboard": "Start Soundboard Spam",
        
        # Advanced
        "accept_rules": "Accept Rules",
        "bypass_onboard": "Bypass Onboarding",
        "check_guild": "Check Guild Access",
        "message_id": "Message ID:",
        "react_message": "Add Reactions",
        "click_button": "Click Button",
        
        # Messages
        "warning": "Warning",
        "no_tokens": "No tokens loaded!",
        "enter_invite": "Enter invite code!",
        "enter_guild": "Enter guild ID!",
        "enter_channel": "Enter channel ID!",
        "enter_message": "Enter message!",
        "enter_user": "Enter user ID!",
        "enter_bio": "Enter bio text!",
        "enter_username": "Enter username!",
        "enter_message_id": "Enter message ID!",
        "loaded_tokens": "Loaded {0} tokens",
        "saved_tokens": "Saved {0} tokens",
        "starting_check": "Starting token check...",
        "check_complete": "Token check completed",
        "formatting": "Formatting tokens...",
        "formatted": "Tokens formatted",
        "joining": "Joining server: {0}",
        "leaving": "Leaving guild: {0}",
        "starting_spam": "Starting spam in channel: {0}",
        "starting_dm": "Starting DM spam to: {0}",
        "changing_bio": "Changing bio to: {0}",
        "sending_friend": "Sending friend requests to: {0}",
        "joining_vc": "Joining VC: {0}",
        "setting_online": "Setting all tokens online...",
        "accepting_rules": "Accepting rules for guild: {0}",
        "bypassing_onboard": "Bypassing onboarding for guild: {0}",
        "checking_guild": "Checking guild access: {0}",
        "stopped": "🛑 All actions stopped",
        "stopping": "🛑 Stopping all actions...",
    },
    "ru": {
        "title": "UMBRELLA RAIDER",
        "tokens": "Токены",
        "proxies": "Прокси",
        "activity_log": "Журнал активности",
        "clear_log": "Очистить журнал",
        "stop_all": "Остановить все действия",
        "info": "Инфо",
        "language": "Язык",
        
        # Tabs
        "tab_token": "Управление токенами",
        "tab_server": "Действия с серверами",
        "tab_user": "Действия с пользователями",
        "tab_voice": "Голосовые действия",
        "tab_advanced": "Расширенные",
        
        # Token Management
        "load_tokens": "Загрузить токены из файла",
        "check_tokens": "Проверить токены",
        "format_tokens": "Форматировать токены",
        "add_tokens": "Добавить токены (по одному на строку):",
        "save_tokens": "Сохранить токены",
        
        # Server Actions
        "invite_code": "Код приглашения сервера:",
        "join_server": "Присоединиться к серверу",
        "guild_id": "ID сервера:",
        "leave_server": "Покинуть сервер",
        "channel_id": "ID канала:",
        "message": "Сообщение:",
        "start_spam": "Начать спам",
        "thread_name": "Название треда:",
        "thread_spam": "Начать спам тредами",
        "mass_ping": "Массовый пинг (ID сервера для скрапинга):",
        "ping_count": "Количество пингов:",
        "random_str": "Добавить случайную строку",
        "delay": "Задержка (секунды):",
        
        # User Actions
        "user_id": "ID пользователя:",
        "dm_message": "Сообщение в ЛС:",
        "dm_spam": "Начать спам в ЛС",
        "new_bio": "Новое био:",
        "change_bio": "Изменить био",
        "username": "Имя пользователя:",
        "friend_spam": "Отправить заявку в друзья",
        "call_spam": "Начать спам звонками",
        "nickname": "Никнейм:",
        "change_nick": "Изменить никнейм на сервере",
        "start_typing": "Начать эффект печатания",
        
        # Voice Actions
        "voice_channel_id": "ID голосового канала:",
        "join_vc": "Присоединиться к голосовому каналу",
        "set_online": "Установить все токены онлайн",
        "soundboard": "Начать спам звуками",
        
        # Advanced
        "accept_rules": "Принять правила",
        "bypass_onboard": "Обойти онбординг",
        "check_guild": "Проверить доступ к серверу",
        "message_id": "ID сообщения:",
        "react_message": "Добавить реакции",
        "click_button": "Нажать кнопку",
        
        # Messages
        "warning": "Предупреждение",
        "no_tokens": "Токены не загружены!",
        "enter_invite": "Введите код приглашения!",
        "enter_guild": "Введите ID сервера!",
        "enter_channel": "Введите ID канала!",
        "enter_message": "Введите сообщение!",
        "enter_user": "Введите ID пользователя!",
        "enter_bio": "Введите текст био!",
        "enter_username": "Введите имя пользователя!",
        "enter_message_id": "Введите ID сообщения!",
        "loaded_tokens": "Загружено {0} токенов",
        "saved_tokens": "Сохранено {0} токенов",
        "starting_check": "Начинаем проверку токенов...",
        "check_complete": "Проверка токенов завершена",
        "formatting": "Форматирование токенов...",
        "formatted": "Токены отформатированы",
        "joining": "Присоединение к серверу: {0}",
        "leaving": "Выход с сервера: {0}",
        "starting_spam": "Начинаем спам в канале: {0}",
        "starting_dm": "Начинаем спам в ЛС: {0}",
        "changing_bio": "Изменение био на: {0}",
        "sending_friend": "Отправка заявок в друзья: {0}",
        "joining_vc": "Присоединение к голосовому каналу: {0}",
        "setting_online": "Устанавливаем все токены онлайн...",
        "accepting_rules": "Принятие правил для сервера: {0}",
        "bypassing_onboard": "Обход онбординга для сервера: {0}",
        "checking_guild": "Проверка доступа к серверу: {0}",
        "stopped": "🛑 Все действия остановлены",
        "stopping": "🛑 Остановка всех действий...",
    }
}

class CweliumGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Umbrella Raider - GUI Edition")
        self.root.geometry("1400x900")
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Language
        self.current_lang = Config.get("language", "en")
        
        # Stop flag for actions
        self.stop_flag = False
        
        self.raider = Raider()
        self.tokens = []
        self.proxies = []
        self.load_data()
        
        self.setup_ui()
        
    def t(self, key):
        """Get translation"""
        return TRANSLATIONS[self.current_lang].get(key, key)
    
    def load_data(self):
        """Load tokens and proxies"""
        try:
            with open("data/tokens.txt", "r") as f:
                self.tokens = [line.strip() for line in f if line.strip()]
            with open("data/proxies.txt", "r") as f:
                self.proxies = [line.strip() for line in f if line.strip()]
        except:
            pass
    
    def setup_ui(self):
        """Setup main UI"""
        # Top bar
        top_bar = ctk.CTkFrame(self.root, height=60)
        top_bar.pack(fill="x", padx=20, pady=(20, 0))
        
        # Title
        title = ctk.CTkLabel(
            top_bar, 
            text=self.t("title"), 
            font=("Arial", 32, "bold")
        )
        title.pack(side="left", padx=20)
        
        # Language selector
        lang_frame = ctk.CTkFrame(top_bar)
        lang_frame.pack(side="right", padx=20)
        
        ctk.CTkLabel(lang_frame, text=self.t("language") + ":", font=("Arial", 12)).pack(side="left", padx=5)
        self.lang_var = ctk.StringVar(value=self.current_lang)
        lang_menu = ctk.CTkOptionMenu(
            lang_frame,
            values=["en", "ru"],
            variable=self.lang_var,
            command=self.change_language,
            width=80
        )
        lang_menu.pack(side="left", padx=5)
        
        # Info button
        info_btn = ctk.CTkButton(
            top_bar,
            text=self.t("info"),
            command=self.show_info,
            width=100,
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        info_btn.pack(side="right", padx=10)
        
        # Stats frame
        stats_frame = ctk.CTkFrame(self.root)
        stats_frame.pack(pady=10, padx=20, fill="x")
        
        self.token_label = ctk.CTkLabel(
            stats_frame, 
            text=f"{self.t('tokens')}: {len(self.tokens)}", 
            font=("Arial", 14)
        )
        self.token_label.pack(side="left", padx=20, pady=10)
        
        self.proxy_label = ctk.CTkLabel(
            stats_frame, 
            text=f"{self.t('proxies')}: {len(self.proxies)}", 
            font=("Arial", 14)
        )
        self.proxy_label.pack(side="left", padx=20, pady=10)
        
        # Main container
        main_container = ctk.CTkFrame(self.root)
        main_container.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Left side - Tabs
        self.tabview = ctk.CTkTabview(main_container, width=800)
        self.tabview.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Create tabs
        self.create_token_tab()
        self.create_server_tab()
        self.create_user_tab()
        self.create_voice_tab()
        self.create_advanced_tab()
        
        # Right side - Log
        log_frame = ctk.CTkFrame(main_container, width=500)
        log_frame.pack(side="right", fill="both", expand=True)
        
        log_title = ctk.CTkLabel(log_frame, text=self.t("activity_log"), font=("Arial", 16, "bold"))
        log_title.pack(pady=10)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame, 
            wrap=tk.WORD, 
            bg="#1e1e1e", 
            fg="#00ff00",
            font=("Consolas", 10)
        )
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(log_frame)
        buttons_frame.pack(pady=10, fill="x", padx=10)
        
        # Stop all button
        self.stop_btn = ctk.CTkButton(
            buttons_frame, 
            text=self.t("stop_all"), 
            command=self.stop_all_actions,
            fg_color="#ff9800",
            hover_color="#e68900"
        )
        self.stop_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        # Clear log button
        clear_btn = ctk.CTkButton(
            buttons_frame, 
            text=self.t("clear_log"), 
            command=self.clear_log,
            fg_color="#ff4444",
            hover_color="#cc0000"
        )
        clear_btn.pack(side="left", padx=5, expand=True, fill="x")

    def create_token_tab(self):
        """Token Management Tab"""
        tab = self.tabview.add(self.t("tab_token"))
        
        # Scrollable frame
        scroll = ctk.CTkScrollableFrame(tab)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Load tokens button
        load_btn = ctk.CTkButton(scroll, text=self.t("load_tokens"), command=self.load_tokens_file)
        load_btn.pack(pady=10, fill="x")
        
        # Token checker
        check_btn = ctk.CTkButton(scroll, text=self.t("check_tokens"), command=self.check_tokens)
        check_btn.pack(pady=10, fill="x")
        
        # Format tokens
        format_btn = ctk.CTkButton(scroll, text=self.t("format_tokens"), command=self.format_tokens)
        format_btn.pack(pady=10, fill="x")
        
        # Token input
        ctk.CTkLabel(scroll, text=self.t("add_tokens")).pack(pady=(20, 5))
        self.token_input = ctk.CTkTextbox(scroll, height=200)
        self.token_input.pack(pady=10, fill="both", expand=True)
        
        save_tokens_btn = ctk.CTkButton(scroll, text=self.t("save_tokens"), command=self.save_tokens)
        save_tokens_btn.pack(pady=10, fill="x")
    
    def create_server_tab(self):
        """Server Actions Tab"""
        tab = self.tabview.add(self.t("tab_server"))
        scroll = ctk.CTkScrollableFrame(tab)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Joiner
        ctk.CTkLabel(scroll, text=self.t("invite_code"), font=("Arial", 12)).pack(pady=(10, 5))
        self.invite_entry = ctk.CTkEntry(scroll, placeholder_text="discord.gg/CODE")
        self.invite_entry.pack(pady=5, fill="x")
        join_btn = ctk.CTkButton(scroll, text=self.t("join_server"), command=self.join_server)
        join_btn.pack(pady=10, fill="x")
        
        # Leaver
        ctk.CTkLabel(scroll, text=self.t("guild_id"), font=("Arial", 12)).pack(pady=(20, 5))
        self.guild_leave_entry = ctk.CTkEntry(scroll, placeholder_text="Guild ID")
        self.guild_leave_entry.pack(pady=5, fill="x")
        leave_btn = ctk.CTkButton(scroll, text=self.t("leave_server"), command=self.leave_server)
        leave_btn.pack(pady=10, fill="x")
        
        # Spammer
        ctk.CTkLabel(scroll, text=self.t("channel_id"), font=("Arial", 12)).pack(pady=(20, 5))
        self.channel_spam_entry = ctk.CTkEntry(scroll, placeholder_text="Channel ID")
        self.channel_spam_entry.pack(pady=5, fill="x")
        
        ctk.CTkLabel(scroll, text=self.t("message"), font=("Arial", 12)).pack(pady=(10, 5))
        self.message_entry = ctk.CTkEntry(scroll, placeholder_text="Message")
        self.message_entry.pack(pady=5, fill="x")
        
        # Mass ping options
        ctk.CTkLabel(scroll, text=self.t("mass_ping"), font=("Arial", 12)).pack(pady=(10, 5))
        self.mass_ping_guild = ctk.CTkEntry(scroll, placeholder_text="Guild ID (optional)")
        self.mass_ping_guild.pack(pady=5, fill="x")
        
        ctk.CTkLabel(scroll, text=self.t("ping_count"), font=("Arial", 12)).pack(pady=(10, 5))
        self.ping_count_entry = ctk.CTkEntry(scroll, placeholder_text="5")
        self.ping_count_entry.pack(pady=5, fill="x")
        
        self.random_str_var = ctk.BooleanVar()
        random_check = ctk.CTkCheckBox(scroll, text=self.t("random_str"), variable=self.random_str_var)
        random_check.pack(pady=5)
        
        ctk.CTkLabel(scroll, text=self.t("delay"), font=("Arial", 12)).pack(pady=(10, 5))
        self.delay_entry = ctk.CTkEntry(scroll, placeholder_text="0")
        self.delay_entry.pack(pady=5, fill="x")
        
        spam_btn = ctk.CTkButton(scroll, text=self.t("start_spam"), command=self.start_spam)
        spam_btn.pack(pady=10, fill="x")
        
        # Thread Spammer
        ctk.CTkLabel(scroll, text=self.t("thread_name"), font=("Arial", 12)).pack(pady=(20, 5))
        self.thread_name_entry = ctk.CTkEntry(scroll, placeholder_text="Thread Name")
        self.thread_name_entry.pack(pady=5, fill="x")
        
        ctk.CTkLabel(scroll, text=self.t("channel_id"), font=("Arial", 12)).pack(pady=(10, 5))
        self.thread_channel_entry = ctk.CTkEntry(scroll, placeholder_text="Channel ID")
        self.thread_channel_entry.pack(pady=5, fill="x")
        
        thread_btn = ctk.CTkButton(scroll, text=self.t("thread_spam"), command=self.thread_spam)
        thread_btn.pack(pady=10, fill="x")
    
    def create_user_tab(self):
        """User Actions Tab"""
        tab = self.tabview.add(self.t("tab_user"))
        scroll = ctk.CTkScrollableFrame(tab)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # DM Spammer
        ctk.CTkLabel(scroll, text=self.t("user_id"), font=("Arial", 12)).pack(pady=(10, 5))
        self.user_id_entry = ctk.CTkEntry(scroll, placeholder_text="User ID")
        self.user_id_entry.pack(pady=5, fill="x")
        
        ctk.CTkLabel(scroll, text=self.t("dm_message"), font=("Arial", 12)).pack(pady=(10, 5))
        self.dm_message_entry = ctk.CTkEntry(scroll, placeholder_text="Message")
        self.dm_message_entry.pack(pady=5, fill="x")
        
        dm_btn = ctk.CTkButton(scroll, text=self.t("dm_spam"), command=self.dm_spam)
        dm_btn.pack(pady=10, fill="x")
        
        # Call Spammer
        ctk.CTkLabel(scroll, text=self.t("user_id"), font=("Arial", 12)).pack(pady=(20, 5))
        self.call_user_entry = ctk.CTkEntry(scroll, placeholder_text="User ID")
        self.call_user_entry.pack(pady=5, fill="x")
        
        call_btn = ctk.CTkButton(scroll, text=self.t("call_spam"), command=self.call_spam)
        call_btn.pack(pady=10, fill="x")
        
        # Bio Changer
        ctk.CTkLabel(scroll, text=self.t("new_bio"), font=("Arial", 12)).pack(pady=(20, 5))
        self.bio_entry = ctk.CTkEntry(scroll, placeholder_text="New bio")
        self.bio_entry.pack(pady=5, fill="x")
        
        bio_btn = ctk.CTkButton(scroll, text=self.t("change_bio"), command=self.change_bio)
        bio_btn.pack(pady=10, fill="x")
        
        # Nick Changer
        ctk.CTkLabel(scroll, text=self.t("guild_id"), font=("Arial", 12)).pack(pady=(20, 5))
        self.nick_guild_entry = ctk.CTkEntry(scroll, placeholder_text="Guild ID")
        self.nick_guild_entry.pack(pady=5, fill="x")
        
        ctk.CTkLabel(scroll, text=self.t("nickname"), font=("Arial", 12)).pack(pady=(10, 5))
        self.nick_entry = ctk.CTkEntry(scroll, placeholder_text="Nickname")
        self.nick_entry.pack(pady=5, fill="x")
        
        nick_btn = ctk.CTkButton(scroll, text=self.t("change_nick"), command=self.change_nick)
        nick_btn.pack(pady=10, fill="x")
        
        # Friend Spammer
        ctk.CTkLabel(scroll, text=self.t("username"), font=("Arial", 12)).pack(pady=(20, 5))
        self.friend_entry = ctk.CTkEntry(scroll, placeholder_text="username")
        self.friend_entry.pack(pady=5, fill="x")
        
        friend_btn = ctk.CTkButton(scroll, text=self.t("friend_spam"), command=self.friend_spam)
        friend_btn.pack(pady=10, fill="x")
        
        # Typer
        ctk.CTkLabel(scroll, text=self.t("channel_id"), font=("Arial", 12)).pack(pady=(20, 5))
        self.typer_channel_entry = ctk.CTkEntry(scroll, placeholder_text="Channel ID")
        self.typer_channel_entry.pack(pady=5, fill="x")
        
        typer_btn = ctk.CTkButton(scroll, text=self.t("start_typing"), command=self.start_typing)
        typer_btn.pack(pady=10, fill="x")
    
    def create_voice_tab(self):
        """Voice Actions Tab"""
        tab = self.tabview.add(self.t("tab_voice"))
        scroll = ctk.CTkScrollableFrame(tab)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(scroll, text=self.t("guild_id"), font=("Arial", 12)).pack(pady=(10, 5))
        self.vc_guild_entry = ctk.CTkEntry(scroll, placeholder_text="Guild ID")
        self.vc_guild_entry.pack(pady=5, fill="x")
        
        ctk.CTkLabel(scroll, text=self.t("voice_channel_id"), font=("Arial", 12)).pack(pady=(10, 5))
        self.vc_channel_entry = ctk.CTkEntry(scroll, placeholder_text="Voice Channel ID")
        self.vc_channel_entry.pack(pady=5, fill="x")
        
        vc_join_btn = ctk.CTkButton(scroll, text=self.t("join_vc"), command=self.join_vc)
        vc_join_btn.pack(pady=10, fill="x")
        
        # Onliner
        online_btn = ctk.CTkButton(scroll, text=self.t("set_online"), command=self.set_online)
        online_btn.pack(pady=20, fill="x")
        
        # Soundboard
        ctk.CTkLabel(scroll, text=self.t("channel_id"), font=("Arial", 12)).pack(pady=(20, 5))
        self.soundboard_channel_entry = ctk.CTkEntry(scroll, placeholder_text="Channel ID")
        self.soundboard_channel_entry.pack(pady=5, fill="x")
        
        soundboard_btn = ctk.CTkButton(scroll, text=self.t("soundboard"), command=self.soundboard_spam)
        soundboard_btn.pack(pady=10, fill="x")
    
    def create_advanced_tab(self):
        """Advanced Actions Tab"""
        tab = self.tabview.add(self.t("tab_advanced"))
        scroll = ctk.CTkScrollableFrame(tab)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Accept Rules
        ctk.CTkLabel(scroll, text=self.t("guild_id"), font=("Arial", 12)).pack(pady=(10, 5))
        self.rules_guild_entry = ctk.CTkEntry(scroll, placeholder_text="Guild ID")
        self.rules_guild_entry.pack(pady=5, fill="x")
        
        rules_btn = ctk.CTkButton(scroll, text=self.t("accept_rules"), command=self.accept_rules)
        rules_btn.pack(pady=10, fill="x")
        
        # Onboard Bypass
        ctk.CTkLabel(scroll, text=self.t("guild_id"), font=("Arial", 12)).pack(pady=(20, 5))
        self.onboard_guild_entry = ctk.CTkEntry(scroll, placeholder_text="Guild ID")
        self.onboard_guild_entry.pack(pady=5, fill="x")
        
        onboard_btn = ctk.CTkButton(scroll, text=self.t("bypass_onboard"), command=self.bypass_onboard)
        onboard_btn.pack(pady=10, fill="x")
        
        # Guild Checker
        ctk.CTkLabel(scroll, text=self.t("guild_id"), font=("Arial", 12)).pack(pady=(20, 5))
        self.check_guild_entry = ctk.CTkEntry(scroll, placeholder_text="Guild ID")
        self.check_guild_entry.pack(pady=5, fill="x")
        
        check_guild_btn = ctk.CTkButton(scroll, text=self.t("check_guild"), command=self.check_guild)
        check_guild_btn.pack(pady=10, fill="x")
        
        # Reactor
        ctk.CTkLabel(scroll, text=self.t("channel_id"), font=("Arial", 12)).pack(pady=(20, 5))
        self.reactor_channel_entry = ctk.CTkEntry(scroll, placeholder_text="Channel ID")
        self.reactor_channel_entry.pack(pady=5, fill="x")
        
        ctk.CTkLabel(scroll, text=self.t("message_id"), font=("Arial", 12)).pack(pady=(10, 5))
        self.reactor_message_entry = ctk.CTkEntry(scroll, placeholder_text="Message ID")
        self.reactor_message_entry.pack(pady=5, fill="x")
        
        reactor_btn = ctk.CTkButton(scroll, text=self.t("react_message"), command=self.react_message)
        reactor_btn.pack(pady=10, fill="x")
        
        # Button Click
        ctk.CTkLabel(scroll, text=self.t("channel_id"), font=("Arial", 12)).pack(pady=(20, 5))
        self.button_channel_entry = ctk.CTkEntry(scroll, placeholder_text="Channel ID")
        self.button_channel_entry.pack(pady=5, fill="x")
        
        ctk.CTkLabel(scroll, text=self.t("message_id"), font=("Arial", 12)).pack(pady=(10, 5))
        self.button_message_entry = ctk.CTkEntry(scroll, placeholder_text="Message ID")
        self.button_message_entry.pack(pady=5, fill="x")
        
        ctk.CTkLabel(scroll, text=self.t("guild_id"), font=("Arial", 12)).pack(pady=(10, 5))
        self.button_guild_entry = ctk.CTkEntry(scroll, placeholder_text="Guild ID")
        self.button_guild_entry.pack(pady=5, fill="x")
        
        button_btn = ctk.CTkButton(scroll, text=self.t("click_button"), command=self.click_button)
        button_btn.pack(pady=10, fill="x")

    # Utility methods
    def log(self, message, color="green"):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
    
    def clear_log(self):
        """Clear log"""
        self.log_text.delete(1.0, tk.END)
    
    def stop_all_actions(self):
        """Stop all running actions"""
        self.stop_flag = True
        self.log(self.t("stopping"))
        
        # Reset flag after 2 seconds
        def reset_flag():
            time.sleep(2)
            self.stop_flag = False
            self.root.after(0, lambda: self.log(self.t("stopped")))
        
        threading.Thread(target=reset_flag, daemon=True).start()
    
    def load_data(self):
        """Load tokens and proxies"""
        try:
            with open("data/tokens.txt", "r") as f:
                self.tokens = [line.strip() for line in f if line.strip()]
            with open("data/proxies.txt", "r") as f:
                self.proxies = [line.strip() for line in f if line.strip()]
        except:
            pass
    
    def spammer_wrapper(self, token, channel, message, guild, massping, pings, random_str, delay):
        """Wrapper for spammer - NO LIMITS"""
        import tls_client
        session_local = tls_client.Session(client_identifier="chrome_138")
        
        try:
            while not self.stop_flag:
                if massping:
                    msg = self.raider.get_random_members(guild, int(pings))
                    payload = {"content": f"{message} {msg}"}
                else:
                    payload = {"content": f"{message}"}
                
                if random_str:
                    from Cwelium import get_random_str
                    payload["content"] += f" > {get_random_str(15)}"

                response = session_local.post(
                    f"https://discord.com/api/v9/channels/{channel}/messages",
                    headers=self.raider.headers(token),
                    json=payload
                )

                if response.status_code == 200:
                    self.root.after(0, lambda: self.log(f"✓ Отправлено: {token[:25]}..."))
                else:
                    self.root.after(0, lambda: self.log(f"✗ Ошибка: {token[:25]}..."))
                    
        except Exception as e:
            self.root.after(0, lambda err=str(e): self.log(f"✗ Ошибка: {err}"))
    
    def dm_spammer_wrapper(self, token, user_id, message):
        """Wrapper for DM spammer with stop flag check"""
        try:
            channel_id = self.raider.open_dm(token, user_id)
            if not channel_id:
                return
            
            import tls_client
            session_local = tls_client.Session(client_identifier="chrome_138")
            
            while not self.stop_flag:
                payload = {
                    "content": message,
                    "nonce": self.raider.nonce(),
                }

                response = session_local.post(
                    f"https://discord.com/api/v9/channels/{channel_id}/messages",
                    headers=self.raider.headers(token),
                    json=payload
                )

                if response.status_code == 200:
                    self.root.after(0, lambda: self.log(f"✓ DM отправлено: {token[:25]}..."))
                else:
                    self.root.after(0, lambda: self.log(f"✗ DM ошибка: {token[:25]}..."))
        except Exception as e:
            self.root.after(0, lambda err=str(e): self.log(f"✗ Ошибка: {err}"))
    
    def thread_spammer_wrapper(self, token, channel_id, name):
        """Wrapper for thread spammer with stop flag check"""
        import tls_client
        session_local = tls_client.Session(client_identifier="chrome_138")
        
        try:
            payload = {
                "name": name,
                "type": 11,
                "auto_archive_duration": 4320,
                "location": "Thread Browser Toolbar",
            }

            while not self.stop_flag:
                response = session_local.post(
                    f"https://discord.com/api/v9/channels/{channel_id}/threads",
                    headers=self.raider.headers(token),
                    json=payload
                )

                if response.status_code == 201:
                    self.root.after(0, lambda: self.log(f"✓ Тред создан: {token[:25]}..."))
                else:
                    self.root.after(0, lambda: self.log(f"✗ Ошибка треда: {token[:25]}..."))
        except Exception as e:
            self.root.after(0, lambda err=str(e): self.log(f"✗ Ошибка: {err}"))
    
    def typer_wrapper(self, token, channel_id):
        """Wrapper for typer - NO LIMITS"""
        import tls_client
        session_local = tls_client.Session(client_identifier="chrome_138")
        
        try:
            while not self.stop_flag:
                response = session_local.post(
                    f"https://discord.com/api/v9/channels/{channel_id}/typing", 
                    headers=self.raider.headers(token)
                )

                if response.status_code == 204:
                    self.root.after(0, lambda: self.log(f"✓ Печатает: {token[:25]}..."))
                else:
                    self.root.after(0, lambda: self.log(f"✗ Ошибка печати: {token[:25]}..."))
        except Exception as e:
            self.root.after(0, lambda err=str(e): self.log(f"✗ Ошибка: {err}"))
    
    def change_language(self, lang):
        """Change language"""
        self.current_lang = lang
        Config["language"] = lang
        with open("config.json", "w") as f:
            json.dump(Config, f, indent=4)
        messagebox.showinfo("Info", "Please restart the application to apply language changes.")
    
    def show_info(self):
        """Show info window"""
        info_window = ctk.CTkToplevel(self.root)
        info_window.title("Umbrella Info")
        info_window.geometry("800x600")
        
        # Title
        title = ctk.CTkLabel(info_window, text="UMBRELLA RAIDER - INFO", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Scrollable text
        info_text = scrolledtext.ScrolledText(
            info_window,
            wrap=tk.WORD,
            bg="#2b2b2b",
            fg="#ffffff",
            font=("Arial", 11)
        )
        info_text.pack(fill="both", expand=True, padx=20, pady=20)
        
        info_content = """
UMBRELLA RAIDER - COMPLETE GUIDE

═══════════════════════════════════════════════════════════════

TOKEN MANAGEMENT
────────────────────────────────────────────────────────────────
• Load Tokens: Load tokens from a text file
• Check Tokens: Verify which tokens are valid/invalid
• Format Tokens: Convert email:pass:token format to just token
• Add Tokens: Manually add tokens (one per line)

═══════════════════════════════════════════════════════════════

SERVER ACTIONS
────────────────────────────────────────────────────────────────
• Join Server: Join a Discord server using invite code
  - Enter: discord.gg/CODE or just CODE
  
• Leave Server: Leave a Discord server
  - Enter: Guild ID (right-click server → Copy ID)
  
• Message Spammer: Spam messages in a channel
  - Channel ID: Right-click channel → Copy ID
  - Message: Text to spam
  - Mass Ping: Enable to ping random members (needs Guild ID)
  - Ping Count: How many users to ping per message
  - Random String: Add random text to bypass filters
  - Delay: Seconds between messages
  
• Thread Spammer: Create spam threads
  - Thread Name: Name for threads
  - Channel ID: Channel to create threads in

═══════════════════════════════════════════════════════════════

USER ACTIONS
────────────────────────────────────────────────────────────────
• DM Spam: Send direct messages to a user
  - User ID: Right-click user → Copy ID
  - Message: Text to send
  
• Call Spam: Spam voice calls to a user
  - User ID: Target user ID
  
• Change Bio: Change profile bio for all tokens
  - New Bio: Text for bio (max 190 chars)
  
• Change Nickname: Change nickname in a server
  - Guild ID: Server ID
  - Nickname: New nickname
  
• Friend Spam: Send friend requests
  - Username: Target username (without #)
  
• Typing Effect: Show "typing..." indicator
  - Channel ID: Channel to type in

═══════════════════════════════════════════════════════════════

VOICE ACTIONS
────────────────────────────────────────────────────────────────
• Join Voice Channel: Join a voice channel
  - Guild ID: Server ID
  - Voice Channel ID: VC ID
  
• Set Online: Set all tokens to online status
  
• Soundboard Spam: Spam soundboard sounds
  - Channel ID: Voice channel ID

═══════════════════════════════════════════════════════════════

ADVANCED
────────────────────────────────────────────────────────────────
• Accept Rules: Accept server rules/verification
  - Guild ID: Server ID
  
• Bypass Onboarding: Complete server onboarding
  - Guild ID: Server ID
  
• Check Guild: Check which tokens have access
  - Guild ID: Server ID
  
• Add Reactions: React to a message
  - Channel ID: Channel with message
  - Message ID: Right-click message → Copy ID
  
• Click Button: Click buttons on messages
  - Channel ID: Channel with message
  - Message ID: Message with buttons
  - Guild ID: Server ID

═══════════════════════════════════════════════════════════════

HOW TO GET IDS
────────────────────────────────────────────────────────────────
1. Enable Developer Mode:
   Settings → Advanced → Developer Mode (ON)
   
2. Get IDs:
   - Server ID: Right-click server icon → Copy ID
   - Channel ID: Right-click channel → Copy ID
   - User ID: Right-click user → Copy ID
   - Message ID: Right-click message → Copy ID

═══════════════════════════════════════════════════════════════

TIPS
────────────────────────────────────────────────────────────────
• Use proxies to avoid rate limits
• Check tokens regularly to remove invalid ones
• Use delays in spammer to avoid bans
• Mass ping requires member scraping (takes time)
• Some features require tokens to be in the server
• Use "Stop All Actions" button to cancel running operations

═══════════════════════════════════════════════════════════════

STOP ALL ACTIONS
────────────────────────────────────────────────────────────────
The orange "Stop All Actions" button in the log panel will:
• Stop all spam operations (message, DM, thread, typing)
• Cancel ongoing loops
• Allow you to start new actions immediately

Note: Some actions (like join/leave) complete instantly and 
cannot be stopped. The stop button works for continuous actions.

═══════════════════════════════════════════════════════════════

DISCLAIMER
────────────────────────────────────────────────────────────────
This tool is for EDUCATIONAL PURPOSES ONLY.
The author takes no responsibility for misuse.
Use at your own risk.

═══════════════════════════════════════════════════════════════
"""
        
        info_text.insert(1.0, info_content)
        info_text.config(state="disabled")
    
    def load_tokens_file(self):
        """Load tokens from file dialog"""
        filename = filedialog.askopenfilename(
            title="Select tokens file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, "r") as f:
                tokens = [line.strip() for line in f if line.strip()]
            with open("data/tokens.txt", "w") as f:
                f.write("\n".join(tokens))
            self.load_data()
            self.token_label.configure(text=f"{self.t('tokens')}: {len(self.tokens)}")
            self.log(self.t("loaded_tokens").format(len(tokens)))
    
    def save_tokens(self):
        """Save tokens from input"""
        tokens_text = self.token_input.get("1.0", tk.END).strip()
        tokens = [line.strip() for line in tokens_text.split("\n") if line.strip()]
        
        with open("data/tokens.txt", "w") as f:
            f.write("\n".join(tokens))
        
        self.load_data()
        self.token_label.configure(text=f"{self.t('tokens')}: {len(self.tokens)}")
        self.log(self.t("saved_tokens").format(len(tokens)))
        self.token_input.delete("1.0", tk.END)
    
    def check_tokens(self):
        """Check token validity"""
        if not self.tokens:
            messagebox.showwarning(self.t("warning"), self.t("no_tokens"))
            return
        
        total = len(self.tokens)
        self.log(f"{self.t('starting_check')} | Всего токенов: {total}")
        threading.Thread(target=self._check_tokens_thread, daemon=True).start()
    
    def _check_tokens_thread(self):
        """Thread for checking tokens"""
        import tls_client
        
        valid = []
        invalid = []
        locked = []
        total = len(self.tokens)
        checked = 0
        
        session_check = tls_client.Session(client_identifier="chrome_138")
        
        for token in self.tokens:
            try:
                response = session_check.get(
                    "https://discordapp.com/api/v9/users/@me/library",
                    headers=self.raider.headers(token)
                )
                
                checked += 1
                
                if response.status_code == 200:
                    valid.append(token)
                    self.root.after(0, lambda t=token: self.log(f"✓ Валидный: {t[:25]}..."))
                elif response.status_code == 403:
                    locked.append(token)
                    self.root.after(0, lambda t=token: self.log(f"⚠ Заблокирован: {t[:25]}..."))
                elif response.status_code == 429:
                    self.root.after(0, lambda: self.log(f"⏳ Ratelimit - пропускаем"))
                    invalid.append(token)
                else:
                    invalid.append(token)
                    self.root.after(0, lambda t=token: self.log(f"✗ Невалидный: {t[:25]}..."))
                
                # Progress update
                if checked % 5 == 0 or checked == total:
                    self.root.after(0, lambda c=checked, t=total: self.log(f"Прогресс: {c}/{t}"))
                    
            except Exception as e:
                invalid.append(token)
                self.root.after(0, lambda t=token, err=str(e): self.log(f"✗ Ошибка {t[:25]}...: {err}"))
        
        # Save only valid tokens
        with open("data/tokens.txt", "w") as f:
            f.write("\n".join(valid))
        
        # Final statistics
        self.load_data()
        self.root.after(0, lambda: self.token_label.configure(text=f"{self.t('tokens')}: {len(self.tokens)}"))
        
        stats_msg = f"""
╔══════════════════════════════════════╗
║     РЕЗУЛЬТАТЫ ПРОВЕРКИ ТОКЕНОВ      ║
╠══════════════════════════════════════╣
║ Всего проверено: {total:>18} ║
║ ✓ Валидных:      {len(valid):>18} ║
║ ⚠ Заблокировано: {len(locked):>18} ║
║ ✗ Невалидных:    {len(invalid):>18} ║
╚══════════════════════════════════════╝
"""
        self.root.after(0, lambda: self.log(stats_msg))
        self.root.after(0, lambda: self.log(self.t("check_complete")))
    
    def format_tokens(self):
        """Format tokens"""
        if not self.tokens:
            messagebox.showwarning(self.t("warning"), self.t("no_tokens"))
            return
        
        self.log(self.t("formatting"))
        self.raider.format_tokens()
        self.load_data()
        self.token_label.configure(text=f"{self.t('tokens')}: {len(self.tokens)}")
        self.log(self.t("formatted"))
    
    def join_server(self):
        """Join server"""
        invite = self.invite_entry.get().strip()
        if not invite:
            messagebox.showwarning(self.t("warning"), self.t("enter_invite"))
            return
        
        invite = invite.replace("discord.gg/", "").replace("https://", "")
        self.log(self.t("joining").format(invite))
        threading.Thread(target=lambda: self.raider.joiner(invite), daemon=True).start()
    
    def leave_server(self):
        """Leave server"""
        guild_id = self.guild_leave_entry.get().strip()
        if not guild_id:
            messagebox.showwarning(self.t("warning"), self.t("enter_guild"))
            return
        
        self.log(self.t("leaving").format(guild_id))
        
        def leave_thread():
            for token in self.tokens:
                self.raider.leaver(token, guild_id)
        
        threading.Thread(target=leave_thread, daemon=True).start()
    
    def start_spam(self):
        """Start message spam"""
        channel_id = self.channel_spam_entry.get().strip()
        message = self.message_entry.get().strip()
        
        if not channel_id or not message:
            messagebox.showwarning(self.t("warning"), self.t("enter_channel") + " & " + self.t("enter_message"))
            return
        
        # Get optional parameters
        guild_id = self.mass_ping_guild.get().strip() or None
        ping_count = self.ping_count_entry.get().strip() or None
        random_str = self.random_str_var.get()
        delay = float(self.delay_entry.get().strip() or 0)
        
        # Scrape members if mass ping enabled
        if guild_id and ping_count:
            self.log(f"Scraping members from guild: {guild_id}")
            self.raider.member_scrape(guild_id, channel_id)
        
        self.log(self.t("starting_spam").format(channel_id))
        self.stop_flag = False
        
        def spam_thread():
            for token in self.tokens:
                if self.stop_flag:
                    break
                threading.Thread(
                    target=lambda t=token: self.spammer_wrapper(
                        t, channel_id, message, guild_id, 
                        bool(guild_id and ping_count), ping_count, random_str, delay
                    ),
                    daemon=True
                ).start()
        
        threading.Thread(target=spam_thread, daemon=True).start()
    
    def thread_spam(self):
        """Thread spam"""
        channel_id = self.thread_channel_entry.get().strip()
        thread_name = self.thread_name_entry.get().strip()
        
        if not channel_id or not thread_name:
            messagebox.showwarning(self.t("warning"), self.t("enter_channel") + " & name")
            return
        
        self.log(f"Starting thread spam: {thread_name}")
        self.stop_flag = False
        
        def thread_spam_func():
            for token in self.tokens:
                if self.stop_flag:
                    break
                threading.Thread(
                    target=lambda t=token: self.thread_spammer_wrapper(t, channel_id, thread_name),
                    daemon=True
                ).start()
        
        threading.Thread(target=thread_spam_func, daemon=True).start()
    
    def dm_spam(self):
        """DM spam"""
        user_id = self.user_id_entry.get().strip()
        message = self.dm_message_entry.get().strip()
        
        if not user_id or not message:
            messagebox.showwarning(self.t("warning"), self.t("enter_user") + " & " + self.t("enter_message"))
            return
        
        self.log(self.t("starting_dm").format(user_id))
        self.stop_flag = False
        
        def dm_thread():
            for token in self.tokens:
                if self.stop_flag:
                    break
                threading.Thread(
                    target=lambda t=token: self.dm_spammer_wrapper(t, user_id, message),
                    daemon=True
                ).start()
        
        threading.Thread(target=dm_thread, daemon=True).start()
    
    def call_spam(self):
        """Call spam"""
        user_id = self.call_user_entry.get().strip()
        
        if not user_id:
            messagebox.showwarning(self.t("warning"), self.t("enter_user"))
            return
        
        self.log(f"Starting call spam to: {user_id}")
        
        def call_thread():
            for token in self.tokens:
                threading.Thread(
                    target=lambda t=token: self.raider.call_spammer(t, user_id),
                    daemon=True
                ).start()
        
        threading.Thread(target=call_thread, daemon=True).start()
    
    def change_bio(self):
        """Change bio"""
        bio = self.bio_entry.get().strip()
        if not bio:
            messagebox.showwarning(self.t("warning"), self.t("enter_bio"))
            return
        
        self.log(self.t("changing_bio").format(bio))
        
        def bio_thread():
            for token in self.tokens:
                self.raider.bio_changer(token, bio)
        
        threading.Thread(target=bio_thread, daemon=True).start()
    
    def change_nick(self):
        """Change nickname"""
        guild_id = self.nick_guild_entry.get().strip()
        nickname = self.nick_entry.get().strip()
        
        if not guild_id or not nickname:
            messagebox.showwarning(self.t("warning"), self.t("enter_guild") + " & nickname")
            return
        
        self.log(f"Changing nickname to: {nickname}")
        
        def nick_thread():
            for token in self.tokens:
                self.raider.mass_nick(token, guild_id, nickname)
        
        threading.Thread(target=nick_thread, daemon=True).start()
    
    def friend_spam(self):
        """Friend spam"""
        username = self.friend_entry.get().strip()
        if not username:
            messagebox.showwarning(self.t("warning"), self.t("enter_username"))
            return
        
        self.log(self.t("sending_friend").format(username))
        
        def friend_thread():
            for token in self.tokens:
                self.raider.friender(token, username)
        
        threading.Thread(target=friend_thread, daemon=True).start()
    
    def start_typing(self):
        """Start typing effect"""
        channel_id = self.typer_channel_entry.get().strip()
        
        if not channel_id:
            messagebox.showwarning(self.t("warning"), self.t("enter_channel"))
            return
        
        self.log(f"Starting typing in: {channel_id}")
        self.stop_flag = False
        
        def typing_thread():
            for token in self.tokens:
                if self.stop_flag:
                    break
                threading.Thread(
                    target=lambda t=token: self.typer_wrapper(t, channel_id),
                    daemon=True
                ).start()
        
        threading.Thread(target=typing_thread, daemon=True).start()
    
    def join_vc(self):
        """Join voice channel"""
        guild_id = self.vc_guild_entry.get().strip()
        channel_id = self.vc_channel_entry.get().strip()
        
        if not guild_id or not channel_id:
            messagebox.showwarning(self.t("warning"), self.t("enter_guild") + " & " + self.t("enter_channel"))
            return
        
        self.log(self.t("joining_vc").format(channel_id))
        
        def vc_thread():
            for token in self.tokens:
                self.raider.join_voice_channel(token, guild_id, channel_id)
        
        threading.Thread(target=vc_thread, daemon=True).start()
    
    def set_online(self):
        """Set all tokens online"""
        self.log(self.t("setting_online"))
        
        def online_thread():
            for token in self.tokens:
                ws = websocket.WebSocket()
                self.raider.onliner(token, ws)
        
        threading.Thread(target=online_thread, daemon=True).start()
    
    def soundboard_spam(self):
        """Soundboard spam"""
        channel_id = self.soundboard_channel_entry.get().strip()
        
        if not channel_id:
            messagebox.showwarning(self.t("warning"), self.t("enter_channel"))
            return
        
        self.log(f"Starting soundboard spam in: {channel_id}")
        
        def soundboard_thread():
            for token in self.tokens:
                threading.Thread(
                    target=lambda t=token: self.raider.soundbord(t, channel_id),
                    daemon=True
                ).start()
        
        threading.Thread(target=soundboard_thread, daemon=True).start()
    
    def accept_rules(self):
        """Accept server rules"""
        guild_id = self.rules_guild_entry.get().strip()
        if not guild_id:
            messagebox.showwarning(self.t("warning"), self.t("enter_guild"))
            return
        
        self.log(self.t("accepting_rules").format(guild_id))
        threading.Thread(target=lambda: self.raider.accept_rules(guild_id), daemon=True).start()
    
    def bypass_onboard(self):
        """Bypass onboarding"""
        guild_id = self.onboard_guild_entry.get().strip()
        if not guild_id:
            messagebox.showwarning(self.t("warning"), self.t("enter_guild"))
            return
        
        self.log(self.t("bypassing_onboard").format(guild_id))
        threading.Thread(target=lambda: self.raider.onboard_bypass(guild_id), daemon=True).start()
    
    def check_guild(self):
        """Check guild access"""
        guild_id = self.check_guild_entry.get().strip()
        if not guild_id:
            messagebox.showwarning(self.t("warning"), self.t("enter_guild"))
            return
        
        self.log(self.t("checking_guild").format(guild_id))
        threading.Thread(target=lambda: self.raider.guild_checker(guild_id), daemon=True).start()
    
    def react_message(self):
        """React to message"""
        channel_id = self.reactor_channel_entry.get().strip()
        message_id = self.reactor_message_entry.get().strip()
        
        if not channel_id or not message_id:
            messagebox.showwarning(self.t("warning"), self.t("enter_channel") + " & " + self.t("enter_message_id"))
            return
        
        self.log(f"Adding reactions to message: {message_id}")
        threading.Thread(target=lambda: self.raider.reactor_main(channel_id, message_id), daemon=True).start()
    
    def click_button(self):
        """Click button"""
        channel_id = self.button_channel_entry.get().strip()
        message_id = self.button_message_entry.get().strip()
        guild_id = self.button_guild_entry.get().strip()
        
        if not channel_id or not message_id or not guild_id:
            messagebox.showwarning(self.t("warning"), self.t("enter_channel") + " & " + self.t("enter_message_id") + " & " + self.t("enter_guild"))
            return
        
        self.log(f"Clicking button on message: {message_id}")
        threading.Thread(target=lambda: self.raider.button_bypass(channel_id, message_id, guild_id), daemon=True).start()
    
    def run(self):
        """Start GUI"""
        self.root.mainloop()

if __name__ == "__main__":
    app = CweliumGUI()
    app.run()
