from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return 'API Magmax Agenda OK!'

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        data = request.json
        return f"Recebido via POST: {data}", 200
    else:
        return 'Webhook funcionando!', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')
