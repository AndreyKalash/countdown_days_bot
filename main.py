from telegram import Update
from telegram.ext import (ApplicationBuilder, CallbackContext, CommandHandler,  filters)
from datetime import date, time, timedelta, timezone


TOKEN = 'YOUR TOKEN '
CHANNEL_ID = 'YOUR CHANNEL_ID'
START_MESSAGE = 'YOUR START_MESSAGE'
EVENT_MSG = 'YOUR START_MESSAGE'

bot = ApplicationBuilder().token(TOKEN).build()

# Дата до которой считаются дни
coma_time = date(2024, 11, 12)
# Время в которое будет отправляться сообщение
send_time = time(12, 0, 0, tzinfo=timezone(timedelta(hours=3)))


async def start(upd: Update, ctx: CallbackContext):
    await ctx.bot.send_message(
        chat_id=upd.effective_chat.id,
        text=START_MESSAGE
    )
   

async def send_msg_to_channel(ctx: CallbackContext):
    end_days = (coma_time - date.today()).days
    if end_days >= 0:
        wdays = wdays_format(end_days)
        await ctx.bot.send_message(
            chat_id=CHANNEL_ID,
            text=EVENT_MSG
        )


def wdays_format(days: int):
    wday_format = ''
    if days == 0:
        wday_format = 'сегодня'
    elif days == 1:
        wday_format = 'завтра'
    elif str(days)[-1] == '1' and str(days)[-2:] != '11':
        wday_format = f'через {days} день'
    elif str(days)[-1] in ['2', '3', '4'] and str(days)[-2:] not in ['12', '13', '14']:
        wday_format = f'через {days} дня'
    else:
        wday_format = f'через {days} дней'

    return wday_format


start_command = CommandHandler('start', start)
bot.add_handler(start_command)

job_queue = bot.job_queue
job_queue.run_daily(send_msg_to_channel, time=send_time, days=tuple(range(7)))

bot.run_polling()