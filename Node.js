// Freeman - Keybase Bot
// Полезный бот для Keybase

const Bot = require('keybase-bot');

const bot = new Bot();

async function main() {
  try {
    // Инициализация бота
    await bot.init('Freeman', 'your-paper-key-here', {verbose: false});
    console.log('Бот успешно инициализирован');

    // Обработка сообщений
    const onMessage = async (message) => {
      try {
        if (message.content.type === 'text') {
          const channel = message.channel;
          const text = message.content.text.body.toLowerCase().trim();
          
          // Обработка команд
          // Обработчик команды help
if (text === '/help' || text === 'help') {
  let helpText = "Доступные команды:\\n";
  helpText += "/pay - /pay <сумма>\\n";
  await bot.chat.send(channel, { body: helpText });
  return;
}

// Обработчик команды pay
if (text === '/pay') {
  await bot.chat.send(channel, { body: "Заплатил , молодец!\nДелай добрые дела!" });
  return;
}

          
          // Если команда не распознана
          await bot.chat.send(channel, {
            body: "Извините, я не понимаю эту команду. Используйте /help для списка команд."
          });
        }
      } catch (error) {
        console.error('Ошибка обработки сообщения:', error);
      }
    };

    // Подписка на сообщения
    await bot.chat.watchAllChannelsForNewMessages(onMessage);
    
  } catch (error) {
    console.error('Ошибка инициализации бота:', error);
  }
}

// Запуск бота
main();