"""
Chat API Routes
This module contains the API endpoints for chat functionality.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Create blueprint
chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')


# Mock data storage (replace with database in production)
chat_sessions = {}
messages_store = {}


@chat_bp.route('/sessions', methods=['POST'])
def create_session():
    """
    Create a new chat session
    
    Returns:
        JSON response with session_id and creation timestamp
    """
    try:
        session_id = f"session_{datetime.utcnow().timestamp()}"
        chat_sessions[session_id] = {
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat(),
            'message_count': 0
        }
        messages_store[session_id] = []
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'created_at': chat_sessions[session_id]['created_at']
        }), 201
    except Exception as e:
        logger.error(f"Error creating chat session: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to create chat session'
        }), 500


@chat_bp.route('/sessions/<session_id>', methods=['GET'])
def get_session(session_id):
    """
    Get chat session details
    
    Args:
        session_id: The ID of the chat session
        
    Returns:
        JSON response with session details
    """
    try:
        if session_id not in chat_sessions:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            **chat_sessions[session_id]
        }), 200
    except Exception as e:
        logger.error(f"Error retrieving chat session: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve chat session'
        }), 500


@chat_bp.route('/sessions/<session_id>/messages', methods=['POST'])
def send_message(session_id):
    """
    Send a message in a chat session
    
    Args:
        session_id: The ID of the chat session
        
    Request JSON:
        {
            "content": "User message content",
            "sender": "user" (or "bot")
        }
        
    Returns:
        JSON response with message details and bot response
    """
    try:
        if session_id not in chat_sessions:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        data = request.get_json()
        
        if not data or 'content' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: content'
            }), 400
        
        # Validate sender
        sender = data.get('sender', 'user')
        if sender not in ['user', 'bot']:
            return jsonify({
                'success': False,
                'error': 'Invalid sender. Must be "user" or "bot"'
            }), 400
        
        # Store user message
        message = {
            'message_id': f"msg_{datetime.utcnow().timestamp()}",
            'session_id': session_id,
            'content': data['content'],
            'sender': sender,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        messages_store[session_id].append(message)
        chat_sessions[session_id]['message_count'] += 1
        chat_sessions[session_id]['updated_at'] = datetime.utcnow().isoformat()
        
        # Generate bot response
        bot_response = generate_bot_response(data['content'])
        
        bot_message = {
            'message_id': f"msg_{datetime.utcnow().timestamp()}",
            'session_id': session_id,
            'content': bot_response,
            'sender': 'bot',
            'timestamp': datetime.utcnow().isoformat()
        }
        
        messages_store[session_id].append(bot_message)
        chat_sessions[session_id]['message_count'] += 1
        chat_sessions[session_id]['updated_at'] = datetime.utcnow().isoformat()
        
        return jsonify({
            'success': True,
            'user_message': message,
            'bot_response': bot_message
        }), 200
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to send message'
        }), 500


@chat_bp.route('/sessions/<session_id>/messages', methods=['GET'])
def get_messages(session_id):
    """
    Get all messages in a chat session
    
    Args:
        session_id: The ID of the chat session
        
    Returns:
        JSON response with list of messages
    """
    try:
        if session_id not in chat_sessions:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'messages': messages_store.get(session_id, []),
            'total_messages': len(messages_store.get(session_id, []))
        }), 200
    except Exception as e:
        logger.error(f"Error retrieving messages: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve messages'
        }), 500


@chat_bp.route('/sessions/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    """
    Delete a chat session and all its messages
    
    Args:
        session_id: The ID of the chat session
        
    Returns:
        JSON response indicating success or failure
    """
    try:
        if session_id not in chat_sessions:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        del chat_sessions[session_id]
        del messages_store[session_id]
        
        return jsonify({
            'success': True,
            'message': f'Session {session_id} deleted successfully'
        }), 200
    except Exception as e:
        logger.error(f"Error deleting chat session: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to delete chat session'
        }), 500


@chat_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for the chat API
    
    Returns:
        JSON response indicating API status
    """
    return jsonify({
        'success': True,
        'status': 'Chat API is running',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


def generate_bot_response(user_message):
    """
    Generate a bot response based on user message
    Replace this with actual AI/ML model integration
    
    Args:
        user_message: The user's message content
        
    Returns:
        str: The bot's response
    """
    # TODO: Integrate with AI model (e.g., OpenAI, Hugging Face, etc.)
    
    # Placeholder responses
    response_map = {
        'hello': 'Hi there! How can I help you today?',
        'help': 'I\'m here to assist you. What do you need help with?',
        'how are you': 'I\'m doing well, thank you for asking! How can I assist you?',
        'thanks': 'You\'re welcome! Feel free to ask if you need anything else.',
    }
    
    message_lower = user_message.lower().strip()
    
    for key, response in response_map.items():
        if key in message_lower:
            return response
    
    # Default response
    return f"I received your message: '{user_message}'. I'm still learning! Please check back later for more advanced responses."
