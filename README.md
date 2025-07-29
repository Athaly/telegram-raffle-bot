# 🎲 CaperuRaffleBot

**Bot exclusivo para la comunidad de @Caperubetabot.**  
Permite crear sorteos con nombre, agregar participantes y realizar sorteos aleatorios.  
Los sorteos son persistentes: podés ver ganadores anteriores, reutilizar listas o vaciarlas según sea necesario.

---

## 🚀 Instalación rápida

```bash
git clone git@github.com:valentinoloza/telegram-raffle-bot.git
cd telegram-raffle-bot
chmod +x install.sh
./install.sh
```

---

## ⚙️ Archivo `.env`

Antes de ejecutar el bot, creá un archivo `.env` con:

```env
BOT_TOKEN=123456789:AAEtcTuTokenPrivado
```

---

## ▶️ Cómo ejecutar el bot

```bash
source env/bin/activate
python main.py
```

---

## 📜 Comandos disponibles

```
/start - Inicia el bot
/help - Muestra los comandos disponibles
/newraffle <nombre> - Crea un nuevo sorteo
/add <sorteo> <nombre1,nombre2,...> - Agrega uno o varios participantes
/list <sorteo> - Muestra los participantes
/raffle <sorteo> - Sortea un ganador al azar
/winners <sorteo> - Muestra ganadores anteriores
/clear <sorteo> - Vacía participantes y ganadores
/delete <sorteo> - Elimina el sorteo por completo
```

---

## 👤 Desarrollado por

[@sshvalen](https://t.me/sshvalen) para la comunidad de @Caperubetabot
