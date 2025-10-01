from flask import Flask
from routes import resultPage, searchPage
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.register_blueprint(resultPage)
app.register_blueprint(searchPage)

app.secret_key = "QZZTHNHLcIy2RtctvfH"

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
