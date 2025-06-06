from flask import Flask, request, jsonify
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import datetime
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "Magma X Agenda Bot está online!"

@app.route("/agendar", methods=["POST"])
def agendar():
    data = request.json
    titulo = data.get("titulo")
    data_evento = data.get("data")  # Formato: "2025-06-13"
    hora = data.get("hora")         # Formato: "09:00"

    if not titulo or not data_evento or not hora:
        return jsonify({"erro": "Dados incompletos"}), 400

    try:
        # Preparar horários de início e fim
        start_time = f"{data_evento}T{hora}:00"
        end_time = f"{data_evento}T{hora}:30"

        # Carregar credenciais do Google
        creds = Credentials.from_authorized_user_file("token.json", [
            'https://www.googleapis.com/auth/calendar'
        ])
        service = build("calendar", "v3", credentials=creds)

        # Criar evento
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