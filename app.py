from flask import Flask, request
import requests
import os

app = Flask(__name__)

# TON TOKEN TELEGRAM (ne change pas)
TOKEN = "7839865738:AAEOXLRuMvXtyJogKC6Tm_jKD-D169JMdtE"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

# État des alertes (activé par défaut)
alerts_enabled = True

@app.route('/webhook', methods=['POST'])
def webhook():
    global alerts_enabled
    update = request.get_json()

    if 'message' in update and 'text' in update['message']:
        chat_id = update['message']['chat']['id']
        text = update['message']['text'].strip().lower()

        if text == '/on':
            alerts_enabled = True
            send_message(chat_id, "✅ Alertes ACTIVÉES ! Je t’envoie les trades maintenant.")
        elif text == '/off':
            alerts_enabled = False
            send_message(chat_id, "⛔ Alertes DÉSACTIVÉES. Plus de notifications pour le moment.")
        elif text == '/status':
            status = "activées" if alerts_enabled else "désactivées"
            send_message(chat_id, f"État actuel des alertes : {status}")
        else:
            send_message(chat_id, "Commandes disponibles :\n/on → activer\n/off → désactiver\n/status → voir l’état")

    return 'OK', 200

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

@app.route('/')
def home():
    return "Bot Telegram trading actif !"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
  flask==3.0.3
requests==2.31.0
gunicorn==22.0.0
