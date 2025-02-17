import os
import yt_dlp
import asyncio
import time
from telegram import InlineQueryResultVideo
from telegram.ext import Application, CommandHandler, InlineQueryHandler, CallbackContext
from telegram import Update

TOKEN = 'your_token_here'

async def inline_query(update: Update, context: CallbackContext):
    query = update.inline_query.query.strip()

    if not query or not any(domain in query for domain in ['tiktok.com', 'vm.tiktok.com', 'pinterest.com', 'pin.it']):
        return

    try:
        video_path = await asyncio.to_thread(download_video, query)
        
        if video_path:
            with open(video_path, 'rb') as video_file:
                sent_video = await context.bot.send_video(
                    chat_id=update.inline_query.from_user.id, 
                    video=video_file
                )
            
            result = InlineQueryResultVideo(
                id=str(time.time()),
                video_url=sent_video.video.file_id,
                mime_type="video/mp4",
                thumbnail_url="https://modkit.ct.ws/botimage.jpg?i=2",
                title="Держи свое видео!" 
            )
            await update.inline_query.answer([result], cache_time=0)
            os.remove(video_path)

    except Exception as e:
        print(f"Ошибка при обработке инлайн-запроса: {e}")

def download_video(url: str) -> str:
    ydl_opts = {
        'format': 'b[ext=mp4]/bv*+ba/b', 
        'outtmpl': 'video.mp4',     
        'noplaylist': True,         
        'quiet': True,              
        'restrict_filenames': True,
        'merge_output_format': 'mp4',  
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            return 'video.mp4'
    except Exception as e:
        print(f'Ошибка загрузки: {e}')
        return None

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(InlineQueryHandler(inline_query))

    app.run_polling()

if __name__ == '__main__':
    main()
