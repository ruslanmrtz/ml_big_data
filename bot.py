from aiogram import Bot, Router, types, Dispatcher, F
from aiogram.filters import CommandStart
import aiohttp
import asyncio
import io
import librosa

bot_token = '5693644763:AAE3nxsQvjDwmIJSOzgjqnw6y6ShZ7Kudug'
router = Router()

@router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer('Привет, отправь сообщение!')


@router.message(F.audio)
async def preprocess_audio(message: types.Message, bot: Bot):
    audio_info = await bot.get_file(message.audio.file_id)
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.telegram.org/file/bot{bot_token}/{audio_info.file_path}') as response:
            bytes_audio = io.BytesIO(await response.read())
            audio, sr = librosa.load(bytes_audio)
            print(audio)


@router.message()
async def other(message: types.Message, bot: Bot):
    await message.answer('Жду аудио!')


async def main():
    bot = Bot(token='5693644763:AAE3nxsQvjDwmIJSOzgjqnw6y6ShZ7Kudug')
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())



