import asyncio
import logging
from nio import AsyncClient, MatrixRoom, RoomMessageText
import os
from dotenv import load_dotenv
import json
from datetime import datetime

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HardcoreMatrixBot:
    def __init__(self):
        self.homeserver = os.getenv("MATRIX_HOMESERVER", "https://matrix.org")
        self.user_id = os.getenv("MATRIX_USER_ID")
        self.password = os.getenv("MATRIX_PASSWORD")
        self.device_id = "HARDCORE_BOT"
        
        self.client = AsyncClient(self.homeserver, self.user_id)
        self.client.device_id = self.device_id
        
        # Жесткие команды бота
        self.commands = {
            "!help": self.cmd_help,
            "!ping": self.cmd_ping,
            "!time": self.cmd_time,
            "!calc": self.cmd_calc,
            "!ban": self.cmd_ban,
            "!kick": self.cmd_kick,
            "!stats": self.cmd_stats,
            "!spam": self.cmd_spam,
            "!flood": self.cmd_flood,
        }
        
        self.user_stats = {}
        self.admin_users = ["@your_admin:matrix.org"]  # Замени на своих админов

    async def cmd_help(self, room: MatrixRoom, event: RoomMessageText):
        """Показать все команды"""
        help_text = """
🔥 **HARDCORE BOT COMMANDS:** 🔥

**Основные:**
`!ping` - Проверка работы
`!time` - Текущее время
`!calc 2+2` - Калькулятор

**Админские:**
`!kick @user` - Кикнуть пользователя
`!ban @user` - Забанить пользователя
`!stats` - Статистика пользователей
`!spam @user 5` - Спамнуть пользователя
`!flood 10` - Флуд сообщениями

**Жесткие:**
`!destroy` - Уничтожить комнату (шутка)
`!hack` - Взлом матрицы (шутка)
"""
        await self.client.room_send(
            room_id=room.room_id,
            message_type="m.room.message",
            content={"msgtype": "m.text", "body": help_text}
        )

    async def cmd_ping(self, room: MatrixRoom, event: RoomMessageText):
        """Проверка работы бота"""
        await self.client.room_send(
            room_id=room.room_id,
            message_type="m.room.message",
            content={"msgtype": "m.text", "body": "🏓 PONG! Бот жив и готов к разрушениям!"}
        )

    async def cmd_time(self, room: MatrixRoom, event: RoomMessageText):
        """Текущее время"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await self.client.room_send(
            room_id=room.room_id,
            message_type="m.room.message",
            content={"msgtype": "m.text", "body": f"🕐 Текущее время: {current_time}"}
        )

    async def cmd_calc(self, room: MatrixRoom, event: RoomMessageText):
        """Простой калькулятор"""
        try:
            expr = event.body.split(" ", 1)[1]
            result = eval(expr)
            await self.client.room_send(
                room_id=room.room_id,
                message_type="m.room.message",
                content={"msgtype": "m.text", "body": f"🧮 Результат: {expr} = {result}"}
            )
        except:
            await self.client.room_send(
                room_id=room.room_id,
                message_type="m.room.message",
                content={"msgtype": "m.text", "body": "❌ Ошибка в выражении!"}
            )

    async def cmd_ban(self, room: MatrixRoom, event: RoomMessageText):
        """Забанить пользователя (имитация)"""
        if event.sender not in self.admin_users:
            await self.client.room_send(
                room_id=room.room_id,
                message_type="m.room.message",
                content={"msgtype": "m.text", "body": "❌ Ты не админ!"}
            )
            return
            
        target = event.body.split(" ")[1] if len(event.body.split(" ")) > 1 else None
        if target:
            await self.client.room_send(
                room_id=room.room_id,
                message_type="m.room.message",
                content={"msgtype": "m.text", "body": f"🔨 БАН ХАММЕРОМ! {target} УНИЧТОЖЕН!"}
            )

    async def cmd_kick(self, room: MatrixRoom, event: RoomMessageText):
        """Кикнуть пользователя (имитация)"""
        if event.sender not in self.admin_users:
            await self.client.room_send(
                room_id=room.room_id,
                message_type="m.room.message",
                content={"msgtype": "m.text", "body": "❌ Ты не админ!"}
            )
            return
            
        target = event.body.split(" ")[1] if len(event.body.split(" ")) > 1 else None
        if target:
            await self.client.room_send(
                room_id=room.room_id,
                message_type="m.room.message",
                content={"msgtype": "m.text", "body": f"👢 КИК! {target} вылетел из комнаты!"}
            )

    async def cmd_stats(self, room: MatrixRoom, event: RoomMessageText):
        """Статистика пользователей"""
        user_id = event.sender
        if user_id not in self.user_stats:
            self.user_stats[user_id] = {"messages": 0, "commands": 0}
        
        self.user_stats[user_id]["commands"] += 1
        
        stats_text = "📊 **СТАТИСТИКА БОТА:**\n"
        for user, data in self.user_stats.items():
            stats_text += f"{user}: {data['messages']} сообщ., {data['commands']} команд\n"
        
        await self.client.room_send(
            room_id=room.room_id,
            message_type="m.room.message",
            content={"msgtype": "m.text", "body": stats_text}
        )

    async def cmd_spam(self, room: MatrixRoom, event: RoomMessageText):
        """Спам сообщениями"""
        if event.sender not in self.admin_users:
            return
            
        try:
            parts = event.body.split(" ")
            target = parts[1]
            count = int(parts[2]) if len(parts) > 2 else 3
            count = min(count, 10)  # Ограничение
        except:
            return
        
        for i in range(count):
            await self.client.room_send(
                room_id=room.room_id,
                message_type="m.room.message",
                content={"msgtype": "m.text", "body": f"🔔 {target}, это спам #{i+1}!"}
            )
            await asyncio.sleep(1)

    async def cmd_flood(self, room: MatrixRoom, event: RoomMessageText):
        """Флуд сообщениями"""
        if event.sender not in self.admin_users:
            return
            
        try:
            count = int(event.body.split(" ")[1])
            count = min(count, 20)  # Ограничение
        except:
            count = 5
        
        for i in range(count):
            await self.client.room_send(
                room_id=room.room_id,
                message_type="m.room.message",
                content={"msgtype": "m.text", "body": f"🌊 ФЛУД #{i+1}! ЗАТОПИМ ВСЕХ!"}
            )
            await asyncio.sleep(0.5)

    async def on_message(self, room: MatrixRoom, event: RoomMessageText):
        """Обработка входящих сообщений"""
        # Игнорируем собственные сообщения
        if event.sender == self.user_id:
            return
        
        # Обновляем статистику
        if event.sender not in self.user_stats:
            self.user_stats[event.sender] = {"messages": 0, "commands": 0}
        self.user_stats[event.sender]["messages"] += 1
        
        # Обрабатываем команды
        for cmd, handler in self.commands.items():
            if event.body.startswith(cmd):
                await handler(room, event)
                break

    async def start(self):
        """Запуск бота"""
        try:
            # Логинимся
            await self.client.login(self.password)
            logger.info(f"Бот {self.user_id} успешно залогинился!")
            
            # Синхронизируем и слушаем сообщения
            await self.client.sync_forever(timeout=30000, full_state=True)
            
        except Exception as e:
            logger.error(f"Ошибка: {e}")
        finally:
            await self.client.close()

# Создаем и запускаем бота
async def main():
    bot = HardcoreMatrixBot()
    
    # Добавляем обработчик сообщений
    bot.client.add_event_callback(bot.on_message, RoomMessageText)
    
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())