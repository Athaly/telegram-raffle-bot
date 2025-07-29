#!/bin/bash

echo "🐺 Instalador de CaperuRaffleBot"

# Verificar que se está en el directorio correcto
if [ ! -f main.py ]; then
    echo "🚫 Este script debe ejecutarse desde la raíz del proyecto (donde está main.py)."
    exit 1
fi

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
python3 -m venv env

# Activar entorno virtual
echo "⚙️ Activando entorno..."
source env/bin/activate

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt

# Verificar existencia del archivo .env
if [ ! -f .env ]; then
    echo "⚠️ No se encontró el archivo .env. Creá uno con tu BOT_TOKEN así:"
    echo "BOT_TOKEN=tu_token_de_bot"
else
    echo "✅ Archivo .env encontrado."
fi

echo "✅ Instalación completa. Ejecutá el bot con:"
echo "source env/bin/activate && python main.py"

