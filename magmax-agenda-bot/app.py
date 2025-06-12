from flask import Flask, request, jsonify
import datetime
import pytz
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)

# Configurações
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'credentials.json'
CALENDAR_ID = 'dddseguros@gmail.com'  # Agenda da Magma X

# Autenticação
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('calendar', 'v3', credentials=credentials)

# Fuso horário
timezone = pytz.timezone('America/Sao_Paulo')

@app.route('/')
def home():
    return '✅ Magma X Agenda Bot ativo!'

@app.route('/criar_evento', methods=['POST'])
def criar_evento():
    dados = request.get_json()

    titulo = dados.get('titulo')
    descricao = dados.get('descricao')
    data = dados.get('data')       # Formato: AAAA-MM-DD
    hora = dados.get('hora')       # Formato: HH:MM (24h)

    # Data e hora formatadas
    inicio = datetime.datetime.strptime(f"{data} {hora}", "%Y-%m-%d %H:%M")
    inicio = timezone.localize(inicio)
    fim = inicio + datetime.timedelta(minutes=30)

    evento = {
        'summary': titulo,
        'description': descricao,
        'start': {
            'dateTime': inicio.isoformat(),
            'timeZone': 'America/Sao_Paulo',
        },
        'end': {
            'dateTime': fim.isoformat(),
            'timeZone': 'America/Sao_Paulo',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 10}
            ],
        }
    }

    evento_criado = service.events().insert(calendarId=CALENDAR_ID, body=evento).execute()
    return jsonify({'status': 'sucesso', 'id': evento_criado.get('id')})

if __name__ == '__main__':
    app.run(debug=True)
