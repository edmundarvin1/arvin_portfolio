"""
Portfolio Dashboards Backend API
Serves data to trading and gym analytics dashboards
"""

from flask import Flask, jsonify
from flask_cors import CORS
from api.trading import trading_bp
from api.gym import gym_bp

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Register blueprints
app.register_blueprint(trading_bp, url_prefix='/api/trading')
app.register_blueprint(gym_bp, url_prefix='/api/gym')

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
