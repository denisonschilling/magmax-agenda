from flask import Flask, request, jsonify
import datetime
import pytz
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)

# Autenticação Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
SERVICE_ACCOUNT_FILE = 'credentials.json'
CALENDAR_ID = 'dddseguros@gmail.com'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('calendar', 'v3', credentials=credentials)
timezone = pytz.timezone('America/Sao_Paulo')

@app.route('/')
def home():
    return '✅ Magma X Agenda Bot online com webhook!'

@app.route('/webhook', methods=['GET'])
def webhook():
    now = datetime.datetime.now(timezone)
    later = now + datetime.timedelta(minutes=30)

    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=now.isoformat(),
        timeMax=later.isoformat(),
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    if not events:
        return jsonify({'mensagem': 'Nenhum evento nas próximas 30min.'})

    resposta = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        resumo = event.get('summary', 'Sem título')
        resposta.append(f"{start} → {resumo}")

    return jsonify({'eventos_proximos': resposta})

if __name__ == '__main__':
    app.run(debug=True)
