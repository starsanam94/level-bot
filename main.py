from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users[user_id] = users.get(user_id, 1)
    await update.message.reply_text(
        f"Welcome {update.effective_user.first_name}!\nYour level: {users[user_id]}"
    )

async def level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users[user_id] = users.get(user_id, 1)
    await update.message.reply_text(f"Your current level is: {users[user_id]}")

async def up(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users[user_id] = users.get(user_id, 1) + 1
    await update.message.reply_text(f"Level up! 🚀\nNew level: {users[user_id]}")

def main():
    import os
    TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("level", level))
    app.add_handler(CommandHandler("up", up))

    app.run_polling()

if __name__ == "__main__":
    main()
