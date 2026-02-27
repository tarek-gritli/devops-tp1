import socket
from flask import Flask
from redis import Redis

app = Flask(__name__)

redis = Redis(host='db-service', port=6379, decode_responses=True)

@app.route('/')
def hello():
    try:
        visits = redis.incr('hits')

        container_id = socket.gethostname()

        return f"""
        <html>
            <head>
                <title>Visit Counter</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    }}
                    .container {{
                        text-align: center;
                        background: white;
                        padding: 40px;
                        border-radius: 10px;
                        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
                    }}
                    h1 {{
                        color: #333;
                        margin-bottom: 20px;
                    }}
                    .info {{
                        color: #666;
                        font-size: 18px;
                        margin: 10px 0;
                    }}
                    .highlight {{
                        color: #667eea;
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🎉 Bonjour !</h1>
                    <p class="info">Cette page a été vue <span class="highlight">{visits}</span> fois.</p>
                    <p class="info">Je suis le conteneur <span class="highlight">{container_id}</span></p>
                </div>
            </body>
        </html>
        """
    except Exception as e:
        return f"Erreur de connexion à Redis : {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
