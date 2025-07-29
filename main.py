import json
import os
import random
from telegram.ext import Updater, CommandHandler
from telegram import Update
from telegram.ext import CallbackContext
from dotenv import load_dotenv

# Carga el token del bot
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
# Ruta del archivo JSON
DATA_FILE = "raffles.json"

# Lista de administradores (usá tu user_id)
ADMINS = [618375676, 7340475915, 8089593517, 924633509]

# Diccionario principal de sorteos
raffles = {}

# ---------------------- Persistencia ----------------------


def load_data():
    """Load raffles from ``DATA_FILE`` if it exists."""
    global raffles
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            raffles = json.load(f)
    else:
        raffles = {}


def save_data():
    """Write the current raffle data to ``DATA_FILE``."""
    with open(DATA_FILE, "w") as f:
        json.dump(raffles, f, indent=4)

# ---------------------- Utilidades ------------------------


def is_admin(update: Update) -> bool:
    return update.effective_user.id in ADMINS

# ---------------------- Comandos --------------------------


# Inicia el bot en el chat correspondiente

def start(update: Update, context: CallbackContext):
    """Send a welcome message and basic instructions."""
    update.message.reply_text(
        "Bot de sorteos listo. Usá /help para ver comandos."
    )

# Comando help en telegram


def help_command(update: Update, context: CallbackContext):
    """Display the list of available commands."""
    update.message.reply_text(
        "/newraffle <nombre>\n"
        "/add <sorteo> <participante>\n"
        "/list <sorteo>\n"
        "/raffle <sorteo>\n"
        "/winners <sorteo>\n"
        "/clear <sorteo>"
    )

# Crea un nuevo sorteo


def new_raffle(update: Update, context: CallbackContext):
    """Create a raffle with the given name."""
    if not is_admin(update):
        update.message.reply_text("Solo admins pueden crear sorteos.")
        return
    if not context.args:
        update.message.reply_text("Uso: /newraffle <nombre_sorteo>")
        return
    name = context.args[0]
    if name in raffles:
        update.message.reply_text(f"Ya existe el sorteo '{name}'.")
        return
    raffles[name] = {"participantes": [], "ganadores": []}
    save_data()
    update.message.reply_text(f"Sorteo '{name}' creado.")

# Añadir participantes nuevo(s)


def add_participant(update: Update, context: CallbackContext):
    """Add one or more participants to a raffle."""
    if not is_admin(update):
        update.message.reply_text(
            "Solo los administradores pueden agregar participantes."
        )
        return

    if len(context.args) < 2:
        update.message.reply_text("Uso: /add <sorteo> <nombre1,nombre2,...>")
        return

    nombre_sorteo = context.args[0]
    if nombre_sorteo not in raffles:
        update.message.reply_text(f"El sorteo '{nombre_sorteo}' no existe.")
        return

    texto_nombres = " ".join(context.args[1:])
    nombres = [n.strip() for n in texto_nombres.split(",") if n.strip()]

    if not nombres:
        update.message.reply_text("No se encontraron nombres válidos.")
        return

    raffles[nombre_sorteo]["participantes"].extend(nombres)
    save_data()

    update.message.reply_text(
        f"Se agregaron {len(nombres)} participante(s) al sorteo "
        f"'{nombre_sorteo}':\n" + "\n".join(nombres)
    )


# Borrar el sorteo

def delete_raffle(update: Update, context: CallbackContext):
    """Delete a raffle and all its data."""
    if not is_admin(update):
        update.message.reply_text(
            "Solo los administradores pueden eliminar sorteos."
        )
        return

    if not context.args:
        update.message.reply_text("Uso: /delete <nombre_del_sorteo>")
        return

    nombre = context.args[0]
    if nombre not in raffles:
        update.message.reply_text(f"El sorteo '{nombre}' no existe.")
        return

    del raffles[nombre]
    save_data()
    update.message.reply_text(
        f"El sorteo '{nombre}' fue eliminado por completo."
    )


# Listar participantes
def list_participants(update: Update, context: CallbackContext):
    """Show all participants registered in a raffle."""
    if not context.args:
        update.message.reply_text("Uso: /list <sorteo>")
        return
    name = context.args[0]
    if name not in raffles:
        update.message.reply_text(f"No existe el sorteo '{name}'.")
        return
    lista = raffles[name]["participantes"]
    if not lista:
        update.message.reply_text(f"No hay participantes en '{name}'.")
    else:
        update.message.reply_text(
            f"Participantes en '{name}':\n" + "\n".join(lista)
        )


# Realiza el sorteo
def do_raffle(update: Update, context: CallbackContext):
    """Choose a random winner for the specified raffle."""
    if not context.args:
        update.message.reply_text("Uso: /raffle <sorteo>")
        return
    name = context.args[0]
    if name not in raffles:
        update.message.reply_text(f"No existe el sorteo '{name}'.")
        return
    participantes = raffles[name]["participantes"]
    if not participantes:
        update.message.reply_text(f"No hay participantes en '{name}'.")
        return
    ganador = random.choice(participantes)
    raffles[name]["ganadores"].append(ganador)
    save_data()
    update.message.reply_text(f"🎉 El ganador de '{name}' es: {ganador}")


# Ganador
def winners(update: Update, context: CallbackContext):
    """List winners of a raffle."""
    if not context.args:
        update.message.reply_text("Uso: /winners <sorteo>")
        return
    name = context.args[0]
    if name not in raffles:
        update.message.reply_text(f"No existe el sorteo '{name}'.")
        return
    ganadores = raffles[name]["ganadores"]
    if not ganadores:
        update.message.reply_text(f"Aún no hay ganadores en '{name}'.")
    else:
        update.message.reply_text(
            f"Ganadores de '{name}':\n" + "\n".join(ganadores)
        )


# Limpia la lista de nombres del sorteo especificado
def clear_raffle(update: Update, context: CallbackContext):
    """Remove all participants and winners from a raffle."""
    if not is_admin(update):
        update.message.reply_text(
            "Solo los administradores pueden vaciar sorteos."
        )
        return

    if not context.args:
        update.message.reply_text("Uso: /clear <nombre_del_sorteo>")
        return

    nombre_sorteo = context.args[0]
    if nombre_sorteo not in raffles:
        update.message.reply_text(f"El sorteo '{nombre_sorteo}' no existe.")
        return

    raffles[nombre_sorteo]["participantes"] = []
    raffles[nombre_sorteo]["ganadores"] = []
    save_data()

    update.message.reply_text(f"El sorteo '{nombre_sorteo}' ha sido vaciado.")

# ---------------------- Main ------------------------------


def main():
    """Set up handlers and start the bot."""
    load_data()
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("newraffle", new_raffle))
    dp.add_handler(CommandHandler("add", add_participant))
    dp.add_handler(CommandHandler("list", list_participants))
    dp.add_handler(CommandHandler("raffle", do_raffle))
    dp.add_handler(CommandHandler("winners", winners))
    dp.add_handler(CommandHandler("clear", clear_raffle))
    dp.add_handler(CommandHandler("delete", delete_raffle))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
