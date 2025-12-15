import os
import sqlite3
import asyncio
import uuid
import json
import time
import random
import requests
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
)

# --- CONFIGURATION ---
API_ID = #api id
API_HASH = "API_HASH"
BOT_TOKEN = "BOT_TOKEN"
ADMIN_ID = 8304425018  # Owner ID

DB_PATH = 'settings/qfind.db' # Bot Database
KEYS_PATH = 'settings/keys.json' #Key File
SCANNED_FOLDER = 'scanned_files' #

# Web API Configuration
API_URL = "AP_URL"  # Replace with your actual API URL - Do not use https://, just use http://
API_KEY = "API_KEY"  # Replace with your API key

# --- MEMBERSHIP PLANS (Durations in Seconds) ---
DURATIONS = {
    "30m": 1800,          # 30 Minutes
    "1h": 3600,           # 1 Hour
    "1w": 604800,         # 1 Week
    "1m": 2592000,        # 1 Month
    "1y": 31536000,       # 1 Year
    "lifetime": 9999999999 # Lifetime
}

# Plan Limits (Daily Scans, Line Limit, Balance Bonus)
PLAN_LIMITS = {
    "Free": {"daily_limit": 3, "line_limit": 3000, "balance_bonus": 5.0, "price": 0.0},
    "Bronze": {"daily_limit": 10, "line_limit": 10000, "balance_bonus": 10.0, "price": 5.0},
    "Silver": {"daily_limit": 20, "line_limit": 50000, "balance_bonus": 20.0, "price": 10.0},
    "Gold": {"daily_limit": 40, "line_limit": 100000, "balance_bonus": 50.0, "price": 20.0},
    "Platinum": {"daily_limit": 60, "line_limit": 200000, "balance_bonus": 100.0, "price": 30.0},
    "Diamond": {"daily_limit": 80, "line_limit": 300000, "balance_bonus": 200.0, "price": 50.0},
    "VIP": {"daily_limit": 100, "line_limit": 500000, "balance_bonus": 500.0, "price": 100.0},
    "Omniscience": {"daily_limit": 99999, "line_limit": 9999999, "balance_bonus": float('inf'), "price": 500.0},
    "Owner": {"daily_limit": 99999, "line_limit": 9999999, "balance_bonus": float('inf'), "price": 0.0}
}

# Pricing: Per 100 lines $0.80
PRICE_PER_100_LINES = 0.80

# Daily Reward Amount
DAILY_REWARD = 1.0  # 1$

# Referral Bonus
REFERRAL_BONUS = 5.0  # 5$ per successful referral

# --- LOCALIZATION (English, Turkish, Russian, Chinese) ---
LANG = {
    "en": {
        "welcome": "**Welcome to QFind**\n\n__Select an option from the menu below.__",
        "terms": "**Terms of Service**\n\n1. No illegal activities.\n2. Respect privacy.\n3. No abuse of the system.\n\nAccept to continue.",
        "menu_info": "📊 Info & Stats",
        "menu_me": "👤 My Account",
        "menu_search": "🔍 Search",
        "menu_shop": "🛒 Shop",
        "menu_leaderboard": "🏆 Leaderboard",
        "menu_help": "❓ Help",
        "menu_support": "📞 Support",
        "menu_settings": "⚙️ Settings",
        "menu_admin": "🛡️ Admin Panel",
        "menu_lang": "🌐 Language",
        "info_text": "**System Information**\n\n**Total Wordlists:** `{}` files\n**Total Lines (Data):** `{}` lines\n**Bot Version:** `0.2-Enhanced (QFind)`\n**API Status:** `{}`\n**Total Scans:** `{}`",
        "account_info": "**User Information**\n\n**ID:** `{}`\n**Plan:** **{}**\n**Expires:** `{}`\n**Daily Usage:** `{}/{}`\n**Balance:** `{}`\n**Referrals:** `{}`\n**Referral Code:** `{}`\n**Total Scans:** `{}`",
        "expired": "EXPIRED",
        "lifetime": "LIFETIME",
        "banned": "**🚫 You are BANNED from using this bot.**",
        "btn_redeem": "🔑 Redeem Key",
        "btn_daily": "🎁 Claim Daily Reward",
        "btn_terms_accept": "✅ Accept Terms",
        "ask_key": "**Enter your license key:**",
        "key_success": "**✅ Success!**\nPlan: **{}**\nDuration: **{}**",
        "key_invalid": "**❌ Invalid or used key.**",
        "search_output_select": "**Select Output Format**\n\n**Full Line:** Returns the raw line.\n**Combo:** Extracts User:Pass only.",
        "search_type_select": "**What are you searching for?**",
        "btn_full": "📄 url:login:pass",
        "btn_combo": "🔑 user:pass",
        "ask_query": "**Enter the {} you want to search:**",
        "searching": "__Searching {} in database...__",
        "search_count": "**Found {} lines.**\nCost: `${}`\n\nBuy to download?",
        "search_buy": "💳 Buy & Download",
        "search_cancel": "❌ Cancel",
        "search_done": "**✅ Search Completed!**\n\n**Type:** `{}`\n**Found:** `{}` lines",
        "no_results": "**❌ No results found.**",
        "limit_reached": "**⚠️ Plan limit reached or expired!**",
        "insufficient_balance": "**⚠️ Insufficient balance!**",
        "daily_claimed": "**✅ Daily reward claimed: +${}**",
        "daily_already": "**⚠️ Already claimed today!**",
        "referral_success": "**✅ Referral bonus: +${}**",
        "admin_panel": "**Admin Control Panel**",
        "btn_import": "📤 Import",
        "btn_keys": "🔑 Manage Keys",
        "btn_users": "👥 User Actions",
        "btn_broadcast": "📢 Broadcast",
        "btn_ban": "🚫 Ban User",
        "btn_revoke": "❌ Revoke Plan",
        "btn_unban": "✅ Unban User",
        "btn_add_balance": "💰 Add Balance",
        "ask_user_id": "**Enter User ID:**",
        "ask_balance": "**Enter amount to add:**",
        "action_success": "**✅ Action completed successfully.**",
        "key_gen_menu": "**Select Plan Type:**",
        "key_duration_menu": "**Select Duration:**",
        "key_created": "**✅ Key Created!**\n\nKey: `{}`\nPlan: **{}**\nTime: **{}**",
        "importing": "__Uploading to API...__",
        "import_success": "**✅ Imported!**\nFile: `{}`\nLines: `{}`",
        "lang_select": "**Select your language:**",
        "ask_file": "**Please send the file to import.**",
        "ask_broadcast": "**Enter the message to broadcast:**",
        "unlimited": "Unlimited",
        "shop_menu": "**Shop - Upgrade Your Plan**\n\nSelect a plan to purchase using your balance.",
        "shop_success": "**✅ Plan Purchased!**\nPlan: **{}**\nDuration: **1 Month** (Default)",
        "shop_insufficient": "**⚠️ Insufficient balance for {}! Price: ${}**",
        "leaderboard_text": "**🏆 Leaderboard - Top Referrers**\n\n{}",
        "help_text": "**Help & Guide**\n\n- /start: Start the bot\n- Search: Query database\n- Shop: Buy plans\n- Refer friends for bonuses!",
        "support_ask": "**Enter your support message:**",
        "support_sent": "**✅ Message sent to support!**",
        "settings_menu": "**Settings**\n\nToggle notifications or change preferences.",
        "btn_notify_on": "🔔 Notifications ON",
        "btn_notify_off": "🔕 Notifications OFF"
    },
    "tr": {
        # Similar translations with emojis added for beauty
        "welcome": "**QFind'e Hoş Geldiniz**\n\n__Aşağıdaki menüden bir seçenek seçin.__",
        "terms": "**Hizmet Şartları**\n\n1. Yasadışı faaliyetler yok.\n2. Gizliliğe saygı duyun.\n3. Sistemi kötüye kullanmayın.\n\nDevam etmek için kabul edin.",
        "menu_info": "📊 Bilgi & İstatistikler",
        "menu_me": "👤 Hesabım",
        "menu_search": "🔍 Arama",
        "menu_shop": "🛒 Mağaza",
        "menu_leaderboard": "🏆 Lider Tablosu",
        "menu_help": "❓ Yardım",
        "menu_support": "📞 Destek",
        "menu_settings": "⚙️ Ayarlar",
        "menu_admin": "🛡️ Yönetici Paneli",
        "menu_lang": "🌐 Dil",
        "info_text": "**Sistem Bilgisi**\n\n**Toplam Dosya:** `{}` adet\n**Toplam Veri (Satır):** `{}` satır\n**Bot Sürümü:** `0.2-Enhanced (QFind)`\n**API Durumu:** `{}`\n**Toplam Tarama:** `{}`",
        "account_info": "**Kullanıcı Bilgileri**\n\n**ID:** `{}`\n**Plan:** **{}**\n**Bitiş:** `{}`\n**Günlük Kullanım:** `{}/{}`\n**Bakiye:** `{}`\n**Yönlendirmeler:** `{}`\n**Yönlendirme Kodu:** `{}`\n**Toplam Tarama:** `{}`",
        "expired": "SÜRESİ DOLMUŞ",
        "lifetime": "ÖMÜR BOYU",
        "banned": "**🚫 Bu botu kullanmaktan banlandınız.**",
        "btn_redeem": "🔑 Anahtar Kullan",
        "btn_daily": "🎁 Günlük Ödül Talep Et",
        "btn_terms_accept": "✅ Şartları Kabul Et",
        "ask_key": "**Lisans anahtarınızı girin:**",
        "key_success": "**✅ Başarılı!**\nPlan: **{}**\nSüre: **{}**",
        "key_invalid": "**❌ Geçersiz veya kullanılmış anahtar.**",
        "search_output_select": "**Çıktı Formatı Seçin**\n\n**Tam Satır:** Ham satırı döner.\n**Combo:** Yalnızca User:Pass çıkarır.",
        "search_type_select": "**Ne arıyorsunuz?**",
        "btn_full": "📄 url:login:pass",
        "btn_combo": "🔑 user:pass",
        "ask_query": "**Aramak istediğiniz {} girin:**",
        "searching": "**Veritabanında {} aranıyor...**",
        "search_count": "**{} satır bulundu.**\nMaliyet: `${}`\n\nİndirmek için satın al?",
        "search_buy": "💳 Satın Al & İndir",
        "search_cancel": "❌ İptal",
        "search_done": "**✅ Arama Tamamlandı!**\n\n**Tip:** `{}`\n**Bulunan:** `{}` satır",
        "no_results": "**❌ Sonuç bulunamadı.**",
        "limit_reached": "**⚠️ Plan sınırı aşıldı veya süresi doldu!**",
        "insufficient_balance": "**⚠️ Yetersiz bakiye!**",
        "daily_claimed": "**✅ Günlük ödül talep edildi: +${}**",
        "daily_already": "**⚠️ Bugün zaten talep edildi!**",
        "referral_success": "**✅ Yönlendirme bonusu: +${}**",
        "admin_panel": "**Yönetici Kontrol Paneli**",
        "btn_import": "📤 İçe Aktar",
        "btn_keys": "🔑 Anahtarları Yönet",
        "btn_users": "👥 Kullanıcı İşlemleri",
        "btn_broadcast": "📢 Yayın",
        "btn_ban": "🚫 Kullanıcı Banla",
        "btn_revoke": "❌ Planı İptal Et",
        "btn_unban": "✅ Banı Kaldır",
        "btn_add_balance": "💰 Bakiye Ekle",
        "ask_user_id": "**Kullanıcı ID girin:**",
        "ask_balance": "**Eklenecek miktarı girin:**",
        "action_success": "**✅ İşlem başarıyla tamamlandı.**",
        "key_gen_menu": "**Plan Tipi Seçin:**",
        "key_duration_menu": "**Süre Seçin:**",
        "key_created": "**✅ Anahtar Oluşturuldu!**\n\nAnahtar: `{}`\nPlan: **{}**\nZaman: **{}**",
        "importing": "**API'ye Yükleniyor...**",
        "import_success": "**✅ İçe Aktarıldı!**\nDosya: `{}`\nSatır: `{}`",
        "lang_select": "**Dil seçin:**",
        "ask_file": "**Yüklemek için dosyayı gönderin.**",
        "ask_broadcast": "**Yayın mesajını girin:**",
        "unlimited": "Sınırsız",
        "shop_menu": "**Mağaza - Plan Yükselt**\n\nBakiyenizle bir plan seçin.",
        "shop_success": "**✅ Plan Satın Alındı!**\nPlan: **{}**\nSüre: **1 Ay** (Varsayılan)",
        "shop_insufficient": "**⚠️ {} için yetersiz bakiye! Fiyat: ${}**",
        "leaderboard_text": "**🏆 Lider Tablosu - En İyi Yönlendirenler**\n\n{}",
        "help_text": "**Yardım & Kılavuz**\n\n- /start: Botu başlat\n- Arama: Veritabanı sorgula\n- Mağaza: Plan satın al\n- Arkadaşlarını yönlendir bonus kazan!",
        "support_ask": "**Destek mesajınızı girin:**",
        "support_sent": "**✅ Mesaj desteğe gönderildi!**",
        "settings_menu": "**Ayarlar**\n\nBildirimleri aç/kapat veya tercihleri değiştir.",
        "btn_notify_on": "🔔 Bildirimler AÇIK",
        "btn_notify_off": "🔕 Bildirimler KAPALI"
    },
    # Add similar for "ru" and "zh" with emojis for consistency
    "ru": {
        "welcome": "**Добро пожаловать в QFind**\n\n__Выберите опцию из меню ниже.__",
        "terms": "**Условия обслуживания**\n\n1. Нет незаконных действий.\n2. Уважайте конфиденциальность.\n3. Не злоупотребляйте системой.\n\nПринять, чтобы продолжить.",
        "menu_info": "📊 Инфо & Статистика",
        "menu_me": "👤 Мой Аккаунт",
        "menu_search": "🔍 Поиск",
        "menu_shop": "🛒 Магазин",
        "menu_leaderboard": "🏆 Лидерборд",
        "menu_help": "❓ Помощь",
        "menu_support": "📞 Поддержка",
        "menu_settings": "⚙️ Настройки",
        "menu_admin": "🛡️ Панель Админа",
        "menu_lang": "🌐 Язык",
        "info_text": "**Система**\n\n**Файлов:** `{}`\n**Строк:** `{}`\n**Версия:** `0.2-Enhanced`\n**API Статус:** `{}`\n**Всего Поисков:** `{}`",
        "account_info": "**Инфо**\n\n**ID:** `{}`\n**План:** **{}**\n**Истекает:** `{}`\n**Лимит:** `{}/{}`\n**Баланс:** `{}`\n**Рефералы:** `{}`\n**Код:** `{}`\n**Всего Поисков:** `{}`",
        "expired": "ИСТЕК",
        "lifetime": "ПОЖИЗНЕННО",
        "banned": "**🚫 Вы ЗАБАНЕНЫ в использовании этого бота.**",
        "btn_redeem": "🔑 Активировать Ключ",
        "btn_daily": "🎁 Забрать Ежедневную Награду",
        "btn_terms_accept": "✅ Принять Условия",
        "ask_key": "**Введите ваш лицензионный ключ:**",
        "key_success": "**✅ Успех!**\nПлан: **{}**\nПродолжительность: **{}**",
        "key_invalid": "**❌ Недействительный или использованный ключ.**",
        "search_output_select": "**Выберите Формат Вывода**\n\n**Полная Строка:** Возвращает сырую строку.\n**Combo:** Извлекает только User:Pass.",
        "search_type_select": "**Что вы ищете?**",
        "btn_full": "📄 url:login:pass",
        "btn_combo": "🔑 user:pass",
        "ask_query": "**Введите {} который вы хотите найти:**",
        "searching": "__Поиск {} в базе данных...__",
        "search_count": "**Найдено {} строк.**\nСтоимость: `${}`\n\nКупить для скачивания?",
        "search_buy": "💳 Купить & Скачать",
        "search_cancel": "❌ Отмена",
        "search_done": "**✅ Поиск Завершен!**\n\n**Тип:** `{}`\n**Найдено:** `{}` строк",
        "no_results": "**❌ Результаты не найдены.**",
        "limit_reached": "**⚠️ Лимит плана достигнут или истек!**",
        "insufficient_balance": "**⚠️ Недостаточно баланса!**",
        "daily_claimed": "**✅ Ежедневная награда забрана: +${}**",
        "daily_already": "**⚠️ Уже забрано сегодня!**",
        "referral_success": "**✅ Реферальный бонус: +${}**",
        "admin_panel": "**Панель Управления Админа**",
        "btn_import": "📤 Импорт",
        "btn_keys": "🔑 Управление Ключами",
        "btn_users": "👥 Действия Пользователя",
        "btn_broadcast": "📢 Рассылка",
        "btn_ban": "🚫 Бан Пользователя",
        "btn_revoke": "❌ Отозвать План",
        "btn_unban": "✅ Разбан Пользователя",
        "btn_add_balance": "💰 Добавить Баланс",
        "ask_user_id": "**Введите ID Пользователя:**",
        "ask_balance": "**Введите сумму:**",
        "action_success": "**✅ Действие завершено успешно.**",
        "key_gen_menu": "**Выберите Тип Плана:**",
        "key_duration_menu": "**Выберите Продолжительность:**",
        "key_created": "**✅ Ключ Создан!**\n\nКлюч: `{}`\nПлан: **{}**\nВремя: **{}**",
        "importing": "__Загрузка в API...__",
        "import_success": "**✅ Импортировано!**\nФайл: `{}`\nСтроки: `{}`",
        "lang_select": "**Выберите язык:**",
        "ask_file": "**Отправьте файл для импорта.**",
        "ask_broadcast": "**Введите сообщение для рассылки:**",
        "unlimited": "Безлимит",
        "shop_menu": "**Магазин - Обновить План**\n\nВыберите план для покупки за баланс.",
        "shop_success": "**✅ План Куплен!**\nПлан: **{}**\nПродолжительность: **1 Месяц** (По умолчанию)",
        "shop_insufficient": "**⚠️ Недостаточно баланса для {}! Цена: ${}**",
        "leaderboard_text": "**🏆 Лидерборд - Топ Рефералов**\n\n{}",
        "help_text": "**Помощь & Руководство**\n\n- /start: Запустить бот\n- Поиск: Запрос в базу\n- Магазин: Купить планы\n- Приглашай друзей за бонусы!",
        "support_ask": "**Введите сообщение поддержки:**",
        "support_sent": "**✅ Сообщение отправлено в поддержку!**",
        "settings_menu": "**Настройки**\n\nВключить/выключить уведомления или изменить предпочтения.",
        "btn_notify_on": "🔔 Уведомления ВКЛ",
        "btn_notify_off": "🔕 Уведомления ВЫКЛ"
    },
    "zh": {
        "welcome": "**欢迎来到 QFind**\n\n__从下面的菜单中选择一个选项.__",
        "terms": "**服务条款**\n\n1. 禁止非法活动。\n2. 尊重隐私。\n3. 禁止滥用系统。\n\n接受继续.",
        "menu_info": "📊 信息 & 统计",
        "menu_me": "👤 我的账户",
        "menu_search": "🔍 搜索",
        "menu_shop": "🛒 商店",
        "menu_leaderboard": "🏆 排行榜",
        "menu_help": "❓ 帮助",
        "menu_support": "📞 支持",
        "menu_settings": "⚙️ 设置",
        "menu_admin": "🛡️ 管理面板",
        "menu_lang": "🌐 语言",
        "info_text": "**系统信息**\n\n**文件:** `{}`\n**行数:** `{}`\n**版本:** `0.2-Enhanced`\n**API 状态:** `{}`\n**总搜索:** `{}`",
        "account_info": "**用户信息**\n\n**ID:** `{}`\n**计划:** **{}**\n**到期:** `{}`\n**使用:** `{}/{}`\n**余额:** `{}`\n**推荐:** `{}`\n**代码:** `{}`\n**总搜索:** `{}`",
        "expired": "已过期",
        "lifetime": "终身",
        "banned": "**🚫 您已被禁止使用此机器人.**",
        "btn_redeem": "🔑 兑换密钥",
        "btn_daily": "🎁 领取每日奖励",
        "btn_terms_accept": "✅ 接受条款",
        "ask_key": "**输入您的许可证密钥:**",
        "key_success": "**✅ 成功!**\n计划: **{}**\n持续时间: **{}**",
        "key_invalid": "**❌ 无效或已使用的密钥.**",
        "search_output_select": "**选择输出格式**\n\n**完整行:** 返回原始行.\n**Combo:** 仅提取 User:Pass.",
        "search_type_select": "**您在搜索什么?**",
        "btn_full": "📄 url:login:pass",
        "btn_combo": "🔑 user:pass",
        "ask_query": "**输入您要搜索的 {}:**",
        "searching": "__在数据库中搜索 {}...__",
        "search_count": "**找到 {} 行.**\n成本: `${}`\n\n购买下载?",
        "search_buy": "💳 购买 & 下载",
        "search_cancel": "❌ 取消",
        "search_done": "**✅ 搜索完成!**\n\n**类型:** `{}`\n**找到:** `{}` 行",
        "no_results": "**❌ 未找到结果.**",
        "limit_reached": "**⚠️ 计划限制已达到或过期!**",
        "insufficient_balance": "**⚠️ 余额不足!**",
        "daily_claimed": "**✅ 每日奖励已领取: +${}**",
        "daily_already": "**⚠️ 今天已经领取!**",
        "referral_success": "**✅ 推荐奖金: +${}**",
        "admin_panel": "**管理控制面板**",
        "btn_import": "📤 导入",
        "btn_keys": "🔑 管理密钥",
        "btn_users": "👥 用户操作",
        "btn_broadcast": "📢 广播",
        "btn_ban": "🚫 禁用户",
        "btn_revoke": "❌ 撤销计划",
        "btn_unban": "✅ 解除禁令",
        "btn_add_balance": "💰 添加余额",
        "ask_user_id": "**输入用户 ID:**",
        "ask_balance": "**输入金额:**",
        "action_success": "**✅ 操作成功完成.**",
        "key_gen_menu": "**选择计划类型:**",
        "key_duration_menu": "**选择持续时间:**",
        "key_created": "**✅ 密钥创建!**\n\n密钥: `{}`\n计划: **{}**\n时间: **{}**",
        "importing": "__上传到 API...__",
        "import_success": "**✅ 已导入!**\n文件: `{}`\n行: `{}`",
        "lang_select": "**选择语言:**",
        "ask_file": "**请发送要导入的文件.**",
        "ask_broadcast": "**输入要广播的消息:**",
        "unlimited": "无限",
        "shop_menu": "**商店 - 升级计划**\n\n使用余额选择计划。",
        "shop_success": "**✅ 计划购买!**\n计划: **{}**\n持续时间: **1 个月** (默认)",
        "shop_insufficient": "**⚠️ {} 的余额不足! 价格: ${}**",
        "leaderboard_text": "**🏆 排行榜 - 顶级推荐者**\n\n{}",
        "help_text": "**帮助 & 指南**\n\n- /start: 启动机器人\n- 搜索: 查询数据库\n- 商店: 购买计划\n- 推荐朋友获奖金!",
        "support_ask": "**输入您的支持消息:**",
        "support_sent": "**✅ 消息发送到支持!**",
        "settings_menu": "**设置**\n\n切换通知或更改偏好。",
        "btn_notify_on": "🔔 通知 ON",
        "btn_notify_off": "🔕 通知 OFF"
    },
}

# --- STATE MANAGEMENT ---
user_states = {} 

# --- DATABASE & FILES SETUP ---
def init_system():
    if not os.path.exists('settings'): os.makedirs('settings')
    if not os.path.exists(SCANNED_FOLDER): os.makedirs(SCANNED_FOLDER)

    # Initialize JSON Key Store
    if not os.path.exists(KEYS_PATH):
        with open(KEYS_PATH, 'w') as f:
            json.dump({}, f)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Users Table (Updated with expiry, ban, lang, balance, referral, total_scans, notifications)
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        plan TEXT DEFAULT 'Free',
        daily_usage INTEGER DEFAULT 0,
        expiry_timestamp REAL DEFAULT 0,
        is_banned INTEGER DEFAULT 0,
        last_reset DATE,
        lang TEXT DEFAULT 'en',
        balance REAL DEFAULT 0.0,
        referral_code TEXT,
        referred_by INTEGER,
        referral_count INTEGER DEFAULT 0,
        last_claim DATE,
        accepted_terms INTEGER DEFAULT 0,
        total_scans INTEGER DEFAULT 0,
        notifications INTEGER DEFAULT 1  -- 1: ON, 0: OFF
    )''')
    
    # Stats Table
    c.execute('''CREATE TABLE IF NOT EXISTS stats (
        id INTEGER PRIMARY KEY,
        total_scans INTEGER DEFAULT 0
    )''')
    
    c.execute("INSERT OR IGNORE INTO stats (id, total_scans) VALUES (1, 0)")
    conn.commit()
    conn.close()

# --- KEY FUNCTIONS (JSON) ---
def load_keys():
    with open(KEYS_PATH, 'r') as f:
        return json.load(f)

def save_keys(keys):
    with open(KEYS_PATH, 'w') as f:
        json.dump(keys, f, indent=4)

def generate_key(plan, duration_key):
    keys = load_keys()
    unique_str = str(uuid.uuid4())[:10].upper()
    key_code = f"QFIND-{plan.upper()}-{unique_str}"
    
    keys[key_code] = {
        "plan": plan,
        "duration": duration_key,
        "created_at": time.time()
    }
    save_keys(keys)
    return key_code

def redeem_key_json(user_id, key_code):
    keys = load_keys()
    if key_code in keys:
        data = keys[key_code]
        plan = data['plan']
        duration_key = data['duration']
        seconds = DURATIONS.get(duration_key, 0)
        
        current_expiry = get_user(user_id)[3]
        now = time.time()
        new_expiry = now + seconds
        
        update_user_plan(user_id, plan, new_expiry)
        
        bonus = PLAN_LIMITS.get(plan, {"balance_bonus": 0})["balance_bonus"]
        if bonus == float('inf'):
            update_user_balance(user_id, float('inf'))
        else:
            update_user_balance(user_id, bonus)
        
        del keys[key_code]
        save_keys(keys)
        return True, plan, duration_key
    return False, None, None

# --- HELPER FUNCTIONS ---
def generate_referral_code():
    return str(uuid.uuid4())[:8].upper()

def get_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = c.fetchone()
    
    if not user:
        today = datetime.now().date().isoformat()
        plan = "Owner" if user_id == ADMIN_ID else "Free"
        expiry = time.time() + DURATIONS['lifetime'] if plan == "Owner" else 0
        ref_code = generate_referral_code()
        c.execute("""INSERT INTO users (user_id, plan, daily_usage, expiry_timestamp, is_banned, last_reset, lang, balance, referral_code, referred_by, referral_count, last_claim, accepted_terms, total_scans, notifications) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                  (user_id, plan, 0, expiry, 0, today, 'en', 0.0, ref_code, None, 0, None, 0, 0, 1))
        conn.commit()
        user = (user_id, plan, 0, expiry, 0, today, 'en', 0.0, ref_code, None, 0, None, 0, 0, 1)
    
    conn.close()
    return user

def update_user_balance(user_id, amount):
    conn = sqlite3.connect(DB_PATH)
    if amount == float('inf'):
        conn.execute("UPDATE users SET balance = 9999999999 WHERE user_id=?", (user_id,))
    else:
        conn.execute("UPDATE users SET balance = balance + ? WHERE user_id=?", (amount, user_id))
    conn.commit()
    conn.close()

def claim_daily(user_id):
    user = get_user(user_id)
    today = datetime.now().date().isoformat()
    if user[11] == today:
        return False
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE users SET last_claim=?, balance = balance + ? WHERE user_id=?", (today, DAILY_REWARD, user_id))
    conn.commit()
    conn.close()
    return True

def add_referral_bonus(referrer_id):
    update_user_balance(referrer_id, REFERRAL_BONUS)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE users SET referral_count = referral_count + 1 WHERE user_id=?", (referrer_id,))
    conn.commit()
    conn.close()

def get_text(user_id, key):
    user = get_user(user_id)
    lang = user[6]
    return LANG.get(lang, LANG['en']).get(key, key)

def set_user_lang(user_id, lang_code):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE users SET lang=? WHERE user_id=?", (lang_code, user_id))
    conn.commit()
    conn.close()

def toggle_notifications(user_id):
    conn = sqlite3.connect(DB_PATH)
    current = get_user(user_id)[14]
    new = 1 if current == 0 else 0
    conn.execute("UPDATE users SET notifications=? WHERE user_id=?", (new, user_id))
    conn.commit()
    conn.close()
    return new

def check_access(user_id):
    user = get_user(user_id)
    if user[4] == 1:
        return False, "banned"
    
    plan = user[1]
    usage = user[2]
    expiry = user[3]
    last_reset_str = user[5]
    
    if plan != "Free" and plan != "Owner":
        if time.time() > expiry:
            revoke_user_db(user_id)
            return True, "expired_reset"
    
    limit = PLAN_LIMITS.get(plan, PLAN_LIMITS['Free'])["daily_limit"]
    
    last_reset = datetime.strptime(last_reset_str, "%Y-%m-%d").date()
    today = datetime.now().date()
    
    if last_reset < today:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("UPDATE users SET daily_usage=0, last_reset=? WHERE user_id=?", (today.isoformat(), user_id))
        conn.commit()
        conn.close()
        return True, "ok"
    
    if usage >= limit:
        return False, "limit"
    
    return True, "ok"

def increment_usage(user_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE users SET daily_usage = daily_usage + 1, total_scans = total_scans + 1 WHERE user_id=?", (user_id,))
    conn.execute("UPDATE stats SET total_scans = total_scans + 1 WHERE id=1")
    conn.commit()
    conn.close()

def ban_user_db(target_id, status=1):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE users SET is_banned=? WHERE user_id=?", (status, target_id))
    conn.commit()
    conn.close()

def revoke_user_db(target_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE users SET plan='Free', expiry_timestamp=0 WHERE user_id=?", (target_id,))
    conn.commit()
    conn.close()

def update_user_plan(user_id, plan, expiry):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE users SET plan=?, expiry_timestamp=? WHERE user_id=?", (plan, expiry, user_id))
    conn.commit()
    conn.close()

def is_admin(user_id):
    return user_id == ADMIN_ID

def check_api_status():
    try:
        r = requests.get(f"{API_URL}/stats?apikey={API_KEY}")
        return "Online" if r.ok else "Offline"
    except:
        return "Offline"

def get_total_stats():
    conn = sqlite3.connect(DB_PATH)
    total_scans = conn.execute("SELECT total_scans FROM stats WHERE id=1").fetchone()[0]
    conn.close()
    return total_scans

def get_leaderboard():
    conn = sqlite3.connect(DB_PATH)
    top = conn.execute("SELECT user_id, referral_count FROM users ORDER BY referral_count DESC LIMIT 10").fetchall()
    conn.close()
    return top

# --- API FUNCTIONS ---
def get_total_lines():
    try:
        r = requests.get(f"{API_URL}/stats?apikey={API_KEY}")
        if r.ok:
            data = r.json()
            return data.get('files', 0), data.get('lines', 0)
        return 0, 0
    except:
        return 0, 0

def search_count_api(search_term, search_type, user_plan):
    max_lines = PLAN_LIMITS.get(user_plan, PLAN_LIMITS['Free'])["line_limit"]
    try:
        r = requests.get(f"{API_URL}/count?apikey={API_KEY}&query={search_term}&type={search_type}&max={max_lines}")
        return r.json().get('count', 0) if r.ok else 0
    except:
        return 0

def search_get_api(search_term, search_type, output_mode, user_plan):
    max_lines = PLAN_LIMITS.get(user_plan, PLAN_LIMITS['Free'])["line_limit"]
    try:
        r = requests.get(f"{API_URL}/query?apikey={API_KEY}&query={search_term}&type={search_type}&mode={output_mode}&max={max_lines}")
        return r.json().get('results', []) if r.ok else []
    except:
        return []

def import_to_api(file_path):
    try:
        with open(file_path, 'rb') as f:
            r = requests.post(f"{API_URL}/upload?apikey={API_KEY}", files={'file': f})
        if r.ok:
            data = r.json()
            return data.get('filename'), data.get('lines')
        return None, 0
    except:
        return None, 0

# --- KEYBOARDS ---
def main_menu_kb(user_id):
    t = lambda k: get_text(user_id, k)
    buttons = [
        [InlineKeyboardButton(t("menu_search"), callback_data="search_start"), InlineKeyboardButton(t("menu_me"), callback_data="my_account")],
        [InlineKeyboardButton(t("menu_shop"), callback_data="shop_menu"), InlineKeyboardButton(t("menu_leaderboard"), callback_data="leaderboard")],
        [InlineKeyboardButton(t("menu_info"), callback_data="info_stats"), InlineKeyboardButton(t("menu_help"), callback_data="help_menu")],
        [InlineKeyboardButton(t("menu_support"), callback_data="support_menu"), InlineKeyboardButton(t("menu_settings"), callback_data="settings_menu")],
        [InlineKeyboardButton(t("menu_lang"), callback_data="lang_menu")]
    ]
    if is_admin(user_id):
        buttons.append([InlineKeyboardButton(t("menu_admin"), callback_data="admin_panel")])
    return InlineKeyboardMarkup(buttons)

def admin_kb(user_id):
    t = lambda k: get_text(user_id, k)
    buttons = [
        [InlineKeyboardButton(t("btn_keys"), callback_data="adm_keys_menu"), InlineKeyboardButton(t("btn_users"), callback_data="adm_users_menu")],
        [InlineKeyboardButton(t("btn_import"), callback_data="adm_import"), InlineKeyboardButton(t("btn_broadcast"), callback_data="adm_broadcast")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(buttons)

def admin_users_kb(user_id):
    t = lambda k: get_text(user_id, k)
    buttons = [
        [InlineKeyboardButton(t("btn_ban"), callback_data="act_ban"), InlineKeyboardButton(t("btn_unban"), callback_data="act_unban")],
        [InlineKeyboardButton(t("btn_revoke"), callback_data="act_revoke"), InlineKeyboardButton(t("btn_add_balance"), callback_data="act_add_balance")],
        [InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]
    ]
    return InlineKeyboardMarkup(buttons)

def search_type_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌐 URL", callback_data="type_URL"), InlineKeyboardButton("👤 Username", callback_data="type_Username")],
        [InlineKeyboardButton("📧 Email", callback_data="type_Email"), InlineKeyboardButton("🔒 Password", callback_data="type_Password")],
        [InlineKeyboardButton("📮 Mailhost", callback_data="type_Mailhost")],
        [InlineKeyboardButton("🔙 Back", callback_data="search_start")]
    ])

def search_output_kb(user_id):
    t = lambda k: get_text(user_id, k)
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t("btn_full"), callback_data="out_full")],
        [InlineKeyboardButton(t("btn_combo"), callback_data="out_combo")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ])

def lang_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🇺🇸 English", callback_data="set_lang_en"), InlineKeyboardButton("🇹🇷 Türkçe", callback_data="set_lang_tr")],
        [InlineKeyboardButton("🇷🇺 Русский", callback_data="set_lang_ru"), InlineKeyboardButton("🇨🇳 中文", callback_data="set_lang_zh")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ])

def plan_kb(admin=False):
    if admin:
        callback_prefix = "plan_"
    else:
        callback_prefix = "shop_buy_"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🥉 Bronze - $5", callback_data=f"{callback_prefix}Bronze"), InlineKeyboardButton("🥈 Silver - $10", callback_data=f"{callback_prefix}Silver")],
        [InlineKeyboardButton("🥇 Gold - $20", callback_data=f"{callback_prefix}Gold"), InlineKeyboardButton("💎 Platinum - $30", callback_data=f"{callback_prefix}Platinum")],
        [InlineKeyboardButton("🔹 Diamond - $50", callback_data=f"{callback_prefix}Diamond"), InlineKeyboardButton("🌟 VIP - $100", callback_data=f"{callback_prefix}VIP")],
        [InlineKeyboardButton("🔮 Omniscience - $500", callback_data=f"{callback_prefix}Omniscience")],
        [InlineKeyboardButton("🔙 Back", callback_data="admin_panel" if admin else "main_menu")]
    ])

def duration_kb(plan):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⏱️ 30 Mins", callback_data=f"dur_{plan}_30m"), InlineKeyboardButton("🕒 1 Hour", callback_data=f"dur_{plan}_1h")],
        [InlineKeyboardButton("📅 1 Week", callback_data=f"dur_{plan}_1w"), InlineKeyboardButton("🗓️ 1 Month", callback_data=f"dur_{plan}_1m")],
        [InlineKeyboardButton("📆 1 Year", callback_data=f"dur_{plan}_1y"), InlineKeyboardButton("∞ Lifetime", callback_data=f"dur_{plan}_lifetime")],
        [InlineKeyboardButton("🔙 Back", callback_data="adm_keys_menu")]
    ])

def back_kb():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="main_menu")]])

def search_buy_kb(count, cost):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 Buy & Download", callback_data=f"buy_search_{count}_{cost}"), InlineKeyboardButton("❌ Cancel", callback_data="search_cancel")]
    ])

def settings_kb(user_id):
    t = lambda k: get_text(user_id, k)
    user = get_user(user_id)
    notify_btn = t("btn_notify_on") if user[14] == 0 else t("btn_notify_off")
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(notify_btn, callback_data="toggle_notify")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ])

# --- BOT CLIENT ---
app = Client("qfind_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- HANDLERS ---

@app.on_message(filters.command("start"))
async def start_command(client, message):
    init_system()
    user_id = message.from_user.id
    args = message.text.split()
    ref_code = args[1] if len(args) > 1 else None

    user = get_user(user_id)
    if ref_code and user[9] is None:  # referred_by
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT user_id FROM users WHERE referral_code=?", (ref_code,))
        referrer = c.fetchone()
        conn.close()
        if referrer:
            conn = sqlite3.connect(DB_PATH)
            conn.execute("UPDATE users SET referred_by=? WHERE user_id=?", (referrer[0], user_id))
            conn.commit()
            conn.close()
            add_referral_bonus(referrer[0])

    if user[12] == 0:  # accepted_terms
        lang = user[6]
        t = LANG.get(lang, LANG['en'])
        photo_path = "welcome.jpg"  # Assume you have a welcome.jpg
        kb = InlineKeyboardMarkup([[InlineKeyboardButton(t["btn_terms_accept"], callback_data="accept_terms")]])
        if os.path.exists(photo_path):
            await message.reply_photo(photo_path, caption=t["terms"], reply_markup=kb)
        else:
            await message.reply_text(t["terms"], reply_markup=kb)
    else:
        lang = user[6]
        t = LANG.get(lang, LANG['en'])
        photo_path = "welcome.jpg"
        kb = main_menu_kb(user_id)
        if os.path.exists(photo_path):
            await message.reply_photo(photo_path, caption=t["welcome"], reply_markup=kb)
        else:
            await message.reply_text(t["welcome"], reply_markup=kb)

@app.on_callback_query()
async def handle_callbacks(client, callback):
    user_id = callback.from_user.id
    data = callback.data
    
    # Access Check
    access, status = check_access(user_id)
    if status == "banned":
        await callback.message.edit_text(get_text(user_id, "banned"))
        return

    # Navigation
    if data == "main_menu":
        user_states.pop(user_id, None)
        await callback.message.edit_text(get_text(user_id, "welcome"), reply_markup=main_menu_kb(user_id))

    elif data == "info_stats":
        file_cnt, total_lines = get_total_lines()
        api_status = check_api_status()
        total_scans = get_total_stats()
        text = get_text(user_id, "info_text").format(file_cnt, "{:,}".format(total_lines), api_status, "{:,}".format(total_scans))
        await callback.message.edit_text(text, reply_markup=back_kb())

    elif data == "lang_menu":
        await callback.message.edit_text(get_text(user_id, "lang_select"), reply_markup=lang_kb())

    elif data.startswith("set_lang_"):
        set_user_lang(user_id, data.split("_")[-1])
        await callback.message.edit_text(get_text(user_id, "welcome"), reply_markup=main_menu_kb(user_id))

    # Account
    elif data == "my_account":
        user = get_user(user_id)
        limit = PLAN_LIMITS.get(user[1], PLAN_LIMITS['Free'])["daily_limit"]
        
        expiry_str = get_text(user_id, "lifetime")
        if user[1] != "Free" and user[1] != "Owner":
            if user[3] < time.time():
                expiry_str = get_text(user_id, "expired")
            else:
                expiry_str = datetime.fromtimestamp(user[3]).strftime('%Y-%m-%d %H:%M')
        
        balance_str = get_text(user_id, "unlimited") if user[7] > 999999 else f"${user[7]:.2f}"
        kb = InlineKeyboardMarkup([[InlineKeyboardButton(get_text(user_id, "btn_redeem"), callback_data="redeem_key"), InlineKeyboardButton(get_text(user_id, "btn_daily"), callback_data="claim_daily")], [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]])
        text = get_text(user_id, "account_info").format(user[0], user[1], expiry_str, user[2], limit, balance_str, user[10], user[8], user[13])
        await callback.message.edit_text(text, reply_markup=kb)

    elif data == "redeem_key":
        user_states[user_id] = "awaiting_key"
        await callback.message.edit_text(get_text(user_id, "ask_key"), reply_markup=back_kb())

    elif data == "claim_daily":
        if claim_daily(user_id):
            await callback.answer(get_text(user_id, "daily_claimed").format(DAILY_REWARD), show_alert=True)
        else:
            await callback.answer(get_text(user_id, "daily_already"), show_alert=True)

    elif data == "accept_terms":
        conn = sqlite3.connect(DB_PATH)
        conn.execute("UPDATE users SET accepted_terms=1 WHERE user_id=?", (user_id,))
        conn.commit()
        conn.close()
        await callback.message.edit_text(get_text(user_id, "welcome"), reply_markup=main_menu_kb(user_id))

    # Search Flow
    elif data == "search_start":
        if status == "limit":
            await callback.answer(get_text(user_id, "limit_reached"), show_alert=True)
            return
        await callback.message.edit_text(get_text(user_id, "search_output_select"), reply_markup=search_output_kb(user_id))

    elif data.startswith("out_"):
        user_states[user_id] = {"mode": data}
        await callback.message.edit_text(get_text(user_id, "search_type_select"), reply_markup=search_type_kb())

    elif data.startswith("type_"):
        current_state = user_states.get(user_id, {})
        if isinstance(current_state, dict):
            current_state["type"] = data.split("_")[1]
            user_states[user_id] = current_state
            await callback.message.edit_text(get_text(user_id, "ask_query").format(current_state["type"]), reply_markup=back_kb())

    elif data.startswith("buy_search_"):
        parts = data.split("_")
        count = int(parts[2])
        cost = float(parts[3])
        user = get_user(user_id)
        plan = user[1]
        if plan in ["Owner", "Omniscience"]:
            cost = 0
        if user[7] < cost:
            await callback.answer(get_text(user_id, "insufficient_balance"), show_alert=True)
            return
        update_user_balance(user_id, -cost)
        search_term = user_states[user_id]["query"] if "query" in user_states[user_id] else ""  
        output_mode = user_states[user_id]["mode"][4:]
        search_type = user_states[user_id]["type"]
        results = search_get_api(search_term, search_type, output_mode, plan)
        if results:
            fname = f"Search_{search_type}_{datetime.now().strftime('%H%M%S')}.txt"
            fpath = os.path.join(SCANNED_FOLDER, fname)
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write("\n".join(results))
            
            await callback.message.reply_document(fpath, caption=get_text(user_id, "search_done").format(search_type, len(results)))
            increment_usage(user_id)
            os.remove(fpath)
        else:
            await callback.message.reply_text(get_text(user_id, "no_results"))
        user_states.pop(user_id, None)

    elif data == "search_cancel":
        await callback.message.edit_text(get_text(user_id, "welcome"), reply_markup=main_menu_kb(user_id))
        user_states.pop(user_id, None)

    # New Features
    elif data == "shop_menu":
        await callback.message.edit_text(get_text(user_id, "shop_menu"), reply_markup=plan_kb(admin=False))

    elif data.startswith("shop_buy_"):
        plan = data.split("_")[2]
        price = PLAN_LIMITS.get(plan, {"price": 0})["price"]
        user = get_user(user_id)
        if user[7] < price:
            await callback.answer(get_text(user_id, "shop_insufficient").format(plan, price), show_alert=True)
            return
        update_user_balance(user_id, -price)
        seconds = DURATIONS.get("1m", 0)  # Default 1 month for shop purchases
        new_expiry = time.time() + seconds
        update_user_plan(user_id, plan, new_expiry)
        bonus = PLAN_LIMITS.get(plan, {"balance_bonus": 0})["balance_bonus"]
        update_user_balance(user_id, bonus)
        await callback.message.edit_text(get_text(user_id, "shop_success").format(plan), reply_markup=main_menu_kb(user_id))

    elif data == "leaderboard":
        top = get_leaderboard()
        lb_text = ""
        for i, (uid, count) in enumerate(top, 1):
            lb_text += f"{i}. User {uid}: {count} referrals\n"
        text = get_text(user_id, "leaderboard_text").format(lb_text or "No data yet.")
        await callback.message.edit_text(text, reply_markup=back_kb())

    elif data == "help_menu":
        await callback.message.edit_text(get_text(user_id, "help_text"), reply_markup=back_kb())

    elif data == "support_menu":
        user_states[user_id] = "support_msg"
        await callback.message.edit_text(get_text(user_id, "support_ask"), reply_markup=back_kb())

    elif data == "settings_menu":
        await callback.message.edit_text(get_text(user_id, "settings_menu"), reply_markup=settings_kb(user_id))

    elif data == "toggle_notify":
        new = toggle_notifications(user_id)
        await callback.answer("Notifications toggled!", show_alert=True)
        await callback.message.edit_text(get_text(user_id, "settings_menu"), reply_markup=settings_kb(user_id))

    # Admin Flow
    elif data == "admin_panel" and is_admin(user_id):
        await callback.message.edit_text(get_text(user_id, "admin_panel"), reply_markup=admin_kb(user_id))
    
    elif data == "adm_keys_menu" and is_admin(user_id):
        await callback.message.edit_text(get_text(user_id, "key_gen_menu"), reply_markup=plan_kb(admin=True))

    elif data.startswith("plan_") and is_admin(user_id):
        plan = data.split("_")[1]
        await callback.message.edit_text(get_text(user_id, "key_duration_menu"), reply_markup=duration_kb(plan))

    elif data.startswith("dur_") and is_admin(user_id):
        parts = data.split("_")
        plan = parts[1]
        dur = parts[2]
        key = generate_key(plan, dur)
        await callback.message.edit_text(get_text(user_id, "key_created").format(key, plan, dur), reply_markup=admin_kb(user_id))

    elif data == "adm_users_menu" and is_admin(user_id):
        await callback.message.edit_text("**User Management**", reply_markup=admin_users_kb(user_id))

    elif data in ["act_ban", "act_unban", "act_revoke", "act_add_balance"] and is_admin(user_id):
        user_states[user_id] = data
        await callback.message.edit_text(get_text(user_id, "ask_user_id"), reply_markup=back_kb())

    elif data == "adm_import" and is_admin(user_id):
        user_states[user_id] = "adm_import"
        await callback.message.edit_text(get_text(user_id, "ask_file"), reply_markup=back_kb())

    elif data == "adm_broadcast" and is_admin(user_id):
        user_states[user_id] = "adm_broadcast"
        await callback.message.edit_text(get_text(user_id, "ask_broadcast"), reply_markup=back_kb())

@app.on_message(filters.text & ~filters.command("start"))
async def text_handler(client, message):
    user_id = message.from_user.id
    state = user_states.get(user_id)
    
    if not state: return

    # Key Redemption
    if state == "awaiting_key":
        success, plan, dur = redeem_key_json(user_id, message.text.strip())
        if success:
            await message.reply_text(get_text(user_id, "key_success").format(plan, dur), reply_markup=main_menu_kb(user_id))
        else:
            await message.reply_text(get_text(user_id, "key_invalid"), reply_markup=back_kb())
        user_states.pop(user_id, None)

    # Admin Actions
    elif state in ["act_ban", "act_unban", "act_revoke"] and is_admin(user_id):
        try:
            target = int(message.text.strip())
            if state == "act_ban": ban_user_db(target, 1)
            elif state == "act_unban": ban_user_db(target, 0)
            elif state == "act_revoke": revoke_user_db(target)
            await message.reply_text(get_text(user_id, "action_success"), reply_markup=admin_kb(user_id))
        except:
            await message.reply_text("❌ Invalid ID", reply_markup=back_kb())
        user_states.pop(user_id, None)

    elif state == "act_add_balance" and is_admin(user_id):
        user_states[user_id] = {"act_add_balance": int(message.text.strip())}
        await message.reply_text(get_text(user_id, "ask_balance"), reply_markup=back_kb())

    elif isinstance(state, dict) and "act_add_balance" in state and is_admin(user_id):
        try:
            amount = float(message.text.strip())
            target_id = state["act_add_balance"]
            update_user_balance(target_id, amount)
            await message.reply_text(get_text(user_id, "action_success"), reply_markup=admin_kb(user_id))
        except:
            await message.reply_text("❌ Invalid amount", reply_markup=back_kb())
        user_states.pop(user_id, None)

    elif state == "adm_broadcast" and is_admin(user_id):
        conn = sqlite3.connect(DB_PATH)
        users = conn.execute("SELECT user_id FROM users").fetchall()
        conn.close()
        sent = 0
        m = await message.reply_text("🚀 Sending...")
        for u in users:
            try:
                await client.send_message(u[0], message.text)
                sent += 1
                await asyncio.sleep(0.05)
            except: pass
        await m.edit_text(f"✅ Sent to {sent} users.")
        user_states.pop(user_id, None)

    elif state == "support_msg":
        try:
            await client.send_message(ADMIN_ID, f"Support from {user_id}: {message.text}")
            await message.reply_text(get_text(user_id, "support_sent"))
        except:
            await message.reply_text("❌ Error sending message.")
        user_states.pop(user_id, None)

    # SEARCH EXECUTION
    elif isinstance(state, dict) and "type" in state:
        search_term = message.text.strip()
        state["query"] = search_term
        output_mode = state["mode"]
        search_type = state["type"]
        
        access, status = check_access(user_id)
        if not access:
            await message.reply_text(get_text(user_id, "limit_reached"))
            return

        wait_msg = await message.reply_text(get_text(user_id, "searching").format(search_type))
        
        user = get_user(user_id)
        plan = user[1]
        count = search_count_api(search_term, search_type, plan)
        cost = (count // 100 + 1) * PRICE_PER_100_LINES if count > 0 else 0
        if plan in ["Owner", "Omniscience"]:
            cost = 0
        
        if count > 0:
            await wait_msg.edit_text(get_text(user_id, "search_count").format(count, cost), reply_markup=search_buy_kb(count, cost))
        else:
            await wait_msg.edit_text(get_text(user_id, "no_results"))
        

@app.on_message(filters.document)
async def doc_handler(client, message):
    user_id = message.from_user.id
    
    if user_states.get(user_id) == "adm_import" and is_admin(user_id):
        status_msg = await message.reply_text("⏳ **Processing file...**")
        
        try:
            file_path = await message.download()
            
            await status_msg.edit_text(get_text(user_id, "importing"))
            filename, lines = import_to_api(file_path)
            
            if filename:
                await status_msg.edit_text(get_text(user_id, "import_success").format(filename, lines))
            else:
                await status_msg.edit_text("❌ Import failed.")
            
            os.remove(file_path)
        except Exception as e:
            await status_msg.edit_text(f"❌ **Error:** {str(e)}")
        
        user_states.pop(user_id, None)

if __name__ == "__main__":
    init_system()
    print("QFind V2 Enhanced Started...")
    app.run()