import asyncio
import logging
import sys
import os
import shutil

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, BufferedInputFile
from aiogram.utils.markdown import hbold

import insta


TOKEN = "6479752461:AAEMkrzGKCgqyHxkNHPDDOhjy1YEc4ZIBrg"

dp = Dispatcher()
router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer('hi')

@router.message((F.entities[0].type == 'url') | (F.entities[0].type == 'text_link'))
async def any_command(message: Message) -> None:
    msg_entities = message.entities[0]
    if msg_entities.type == 'url':
        raw_url = msg_entities.extract_from(message.text)
    elif msg_entities.type == 'text_link':
        raw_url = msg_entities.url
    
    
    data = insta.download_post(url=raw_url)
    l = data[1]
    n = 10
    chunks = [l[i:i + n] for i in range(0, len(l), n)]
    for paths in chunks:
        media = []
        for path in paths:
            if str(path).endswith('mp4'):
                if not media:
                    media.append(types.input_media_video.InputMediaVideo(media=FSInputFile(path=path.absolute()), caption=f'👉[Instagram ссылка👈]({raw_url})\n[👉Бот для скачивание👈](https://t.me/samurai_inst_bot)', parse_mode=ParseMode.MARKDOWN_V2))
                    continue
                media.append(types.input_media_video.InputMediaVideo(media=FSInputFile(path=path.absolute())))
                
            if str(path).endswith(('jpg', 'png', 'jpeg')):
                if not media:
                    media.append(types.input_media_photo.InputMediaPhoto(media=FSInputFile(path=path.absolute()), caption=f'👉[Instagram ссылка👈]({raw_url})\n[👉Бот для скачивание👈](https://t.me/samurai_inst_bot)', parse_mode=ParseMode.MARKDOWN_V2))
                    continue
                media.append(types.input_media_photo.InputMediaPhoto(media=FSInputFile(path=path.absolute())))
        await message.reply_media_group(media=media)
            
    shutil.rmtree(data[0])


async def main() -> None:
    bot = Bot(TOKEN)
    dp.include_router(router=router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())