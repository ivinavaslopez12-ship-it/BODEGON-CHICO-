import os
import threading
import time
from flask import Flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import apihelper

# =====================================================================
# 1. SERVIDOR DE SOPORTE PARA DESPLIEGUE EN RENDER
# =====================================================================
app = Flask('')

@app.route('/')
def home():
    return "¡Servidor del Bot del Bodegón Totto Activo!"

def iniciar_servidor_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, use_reloader=False)

# =====================================================================
# 2. CONFIGURACIÓN DEL BOT
# =====================================================================
# Se obtiene el token desde las variables de entorno de Render
TOKEN = os.environ.get('TELEGRAM_TOKEN')

apihelper.CONNECT_TIMEOUT = 30
apihelper.READ_TIMEOUT = 30

bot = telebot.TeleBot(TOKEN)

# Datos del negocio
INFO_TIENDA = {
    "nombre": "Bodegón Totto",
    "telefono": "+58 424-8201709",
    "direccion": "Calle 16 Sur, entre Av. Francisco de Miranda y 4ta Carrera Sur, El Tigre, Anzoátegui",
    "horario": "Lunes a Sábado: 8:30 AM - 7:00 PM\nDomingo: 9:00 AM - 1:00 PM",
    "instagram": "https://www.instagram.com/bodegontotto",
    "maps": "https://maps.app.goo.gl/YMY7XLMM3P5bguqM9?g_st=iw"
}

# Menú principal con botones
def menu_principal():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    
    btn_info = InlineKeyboardButton("ℹ️ Información y Horarios", callback_data="info")
    btn_ubicacion = InlineKeyboardButton("📍 Ubicación", callback_data="ubicacion")
    btn_contacto = InlineKeyboardButton("📞 Contacto / WhatsApp", callback_data="contacto")
    btn_instagram = InlineKeyboardButton("📸 Instagram", url=INFO_TIENDA["instagram"])
    btn_catalogo = InlineKeyboardButton("🛒 Ver Catálogo / Productos", callback_data="catalogo")
    
    markup.add(btn_info, btn_ubicacion, btn_contacto, btn_instagram, btn_catalogo)
    return markup

# Comando /start o /menu
@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    try:
        texto = (
            f"¡Hola, {message.from_user.first_name}! 👋\n"
            f"Bienvenido a *{INFO_TIENDA['nombre']}* 🛒✨\n\n"
            f"\"Somos tu mejor aliado a la hora de comprar tu producto…\"\n\n"
            f"¿En qué te podemos ayudar hoy? Selecciona una opción del menú:"
        )
        bot.send_message(message.chat.id, texto, parse_mode="Markdown", reply_markup=menu_principal())
    except Exception as e:
        print(f"Error en send_welcome: {e}")

# Manejador de botones interactivos
@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    try:
        if call.data == "info":
            texto = (
                f"ℹ️ *Información del Negocio*\n\n"
                f"📌 *Nombre:* {INFO_TIENDA['nombre']}\n\n"
                f"🕒 *Horario de Atención:*\n"
                f"• Lunes a Sábado: 8:30 AM - 7:00 PM\n"
                f"• Domingo: 9:00 AM - 1:00 PM\n\n"
                f"💳 *Métodos de Pago:*\n"
                f"• Pago Móvil\n"
                f"• Punto de Venta\n"
                f"• Zelle\n"
                f"• Binance\n"
                f"• Efectivo\n\n"
                f"¡Te esperamos con la mejor atención! ✨"
            )
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("⬅️️ Volver al Menú", callback_data="volver"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto, parse_mode="Markdown", reply_markup=markup)

        elif call.data == "ubicacion":
            texto = (
                f"📍 *Nuestra Ubicación*\n\n"
                f"🏠 {INFO_TIENDA['direccion']}\n\n"
                f"Puedes ver la ubicación exacta en Google Maps haciendo clic abajo 👇"
            )
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("🗺️ Abrir en Google Maps", url=INFO_TIENDA["maps"]))
            markup.add(InlineKeyboardButton("⬅️ Volver al Menú", callback_data="volver"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto, parse_mode="Markdown", reply_markup=markup)

        elif call.data == "contacto":
            texto = (
                f"📞 *Contacto Directo*\n\n"
                f"📱 Teléfono / WhatsApp: {INFO_TIENDA['telefono']}\n"
                f"📧 Correo: andreacelisrondon@gmail.com\n\n"
                f"Haz clic abajo para chatear con nosotros por WhatsApp o realizar un pedido:"
            )
            url_whatsapp = f"https://wa.me/584248201709"
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("💬 Escribir al WhatsApp", url=url_whatsapp))
            markup.add(InlineKeyboardButton("⬅️ Volver al Menú", callback_data="volver"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto, parse_mode="Markdown", reply_markup=markup)

        elif call.data == "catalogo":
            texto = (
                f"🛒 *Catálogo de Productos*\n\n"
                f"Aquí puedes consultar nuestras promociones y productos disponibles.\n\n"
                f"Para pedidos directos, puedes escribirnos a nuestro WhatsApp."
            )
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("📲 Pedir por WhatsApp", url="https://wa.me/584248201709"))
            markup.add(InlineKeyboardButton("⬅️ Volver al Menú", callback_data="volver"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto, parse_mode="Markdown", reply_markup=markup)

        elif call.data == "volver":
            texto = (
                f"Bienvenido de nuevo a *{INFO_TIENDA['nombre']}* 🛒\n\n"
                f"Selecciona una opción del menú:"
            )
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto, parse_mode="Markdown", reply_markup=menu_principal())

    except Exception as e:
        print(f"Error en callback_listener: {e}")

# =====================================================================
# 3. EJECUCIÓN MULTIHILO CON RECONEXIÓN AUTOMÁTICA
# =====================================================================
if __name__ == '__main__':
    print(">>> Iniciando servidor Flask para Render...")
    server_thread = threading.Thread(target=iniciar_servidor_flask)
    server_thread.daemon = True
    server_thread.start()

    print(">>> Conectando con la API de Telegram...")
    while True:
        try:
            bot.remove_webhook()
            print(">>> ¡BOT DEL BODEGÓN ONLINE! Escuchando mensajes...")
            bot.infinity_polling(none_stop=True, timeout=60, long_polling_timeout=30)
        except Exception as e:
            print(f"⚠️ Error de conexión: {e}")
            print("🔄 Reintentando conexión en 10 segundos...")
            time.sleep(10)