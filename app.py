"""
Flask Application Setup for Truenester Chatbot
Author: truenester4u-cyber
Date: 2025-12-16
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime

# Initialize Flask application
app = Flask(__name__)

# Configure CORS
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Application configuration
app.config['DEBUG'] = True
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Routes
@app.route('/', methods=['GET'])
def index():
    """Home route"""
    logger.info("Index page accessed")
    return jsonify({
        'message': 'Welcome to Truenester Chatbot API',
        'status': 'online',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    logger.info("Health check endpoint accessed")
    return jsonify({
        'status': 'healthy',
        'service': 'Truenester Chatbot',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat endpoint for processing user messages"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Missing message field'}), 400
        
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        logger.info(f"Received message: {user_message}")
        
        # Process the message (placeholder for chatbot logic)
        response = {
            'user_message': user_message,
            'bot_response': 'This is a placeholder response. Implement your chatbot logic here.',
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

# Application context
@app.before_request
def before_request():
    """Log incoming requests"""
    logger.debug(f"Request: {request.method} {request.path}")

@app.after_request
def after_request(response):
    """Log response status"""
    logger.debug(f"Response status: {response.status_code}")
    return response

if __name__ == '__main__':
    # Run the Flask application
    logger.info("Starting Truenester Chatbot Flask Application")
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )