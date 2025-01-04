from flask import Flask
from routes.home import home_bp
from routes.video_routes import video_bp

app = Flask(__name__)

app.register_blueprint(home_bp)
app.register_blueprint(video_bp, url_prefix="/video")

if __name__ == "__main__":
    app.run(debug=True)
