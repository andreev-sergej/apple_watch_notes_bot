# Telegram AppleWatchNotes Bot

Этот бот конвертирует Markdown-текст или файлы в изображения для отображения на Apple Watch.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![GitHub License](https://img.shields.io/github/license/Engelsgeduld/PySATL_NMVM_Module?style=for-the-badge)

![Workflow](https://github.com/andreev-sergej/apple_watch_notes_bot/actions/workflows/ci.yml/badge.svg)

## 🔥 Возможности

- Преобразование Markdown в HTML и изображения.
- Поддержка различных моделей Apple Watch.
- Настраиваемые отступы, размер шрифта, тема.
- Генерация как одного изображения, так и разбивка на страницы.
- Конвертация markdown файла в pdf формат, с учетом особенностей часов
- Генерация QR кода с адресом или текстом. QR код адаптируется под размеры часов
- Выбор шаблонов оформления по которым генерируется картинка
- Генерация картинки по голосовому сообщению. На русском и английском

### 📋 Все команды:  
| Команда | Описание | Пример |  
|---------|----------|--------|  
| `/start` | Запуск бота | `/start` |  
| `/model` | Выбор модели часов | `/model` |  
| `/padding <число>` | Отступы от краёв (10-50px) | `/padding 25` |  
| `/fontsize` | Размер текста: Маленький/Средний/Большой | `/fontsize` |  
| `/theme` | Тема: Светлая/Тёмная | `/theme` |  
| `/layout` | Режим: Одна страница/Многостраничный | `/layout` |  
| `/template` | Стиль оформления (3 варианта) | `/template` |  
| `/preview` | Предпросмотр в HTML | `/preview Заголовок` |  
| `/pdf` | Конвертация в PDF | `/pdf Список` |  
| `/qr <текст>` | Генерация QR-кода | `/qr https://apple.com` |  

**Ваши часы заслуживают красивых заметок!**  
Просто отправьте текст, файл или голосовое сообщение — бот сделает всё остальное.
