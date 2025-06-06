from flask import Flask, request, jsonify
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Magma X Agenda Bot está online!"

@app.route("/agendar", methods=["POST"])
def agendar():
    data = request.json
    titulo = data.get("titulo")
    data_evento = data.get("data")  # formato: AAAA-MM-DD
    hora = data.get("hora")         # formato: HH:MM

    if not titulo or not data_evento or not hora:
        return jsonify({"erro": "Dados incompletos"}), 400

    try:
        start_time = f"{data_evento}T{hora}:00"
        end_time = f"{data_evento}T{hora}:30"

        creds = Credentials.from_authorized_user_file("token.json", [
            'https://www.googleapis.com/auth/calendar'
        ])
        service = build("calendar", "v3", credentials=creds)

        evento = {
            "summary": titulo,
            "start": {"dateTime": start_time, "timeZone": "America/Sao_Paulo"},
            "end": {"dateTime": end_time, "timeZone": "America/Sao_Paulo"},
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "popup", "minutes": 60},
                    {"method": "popup", "minutes": 1440}
                ]
            }
        }

        service.events().insert(calendarId="primary", body=evento).execute()
        return jsonify({"status": "Evento agendado com sucesso!"})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
