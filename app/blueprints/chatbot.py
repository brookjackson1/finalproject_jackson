from flask import Blueprint, render_template, request, jsonify, g
from groq import Groq
import os

chatbot = Blueprint('chatbot', __name__)

def get_groq_client():
    """Get Groq client instance"""
    api_key = os.environ.get('GROQ_API_KEY')
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set")
    return Groq(api_key=api_key)

def get_business_context():
    """Get context about NailsbyBrookJ services and offerings"""
    try:
        cursor = g.db.cursor()

        # Get services
        cursor.execute("SELECT name, base_price, description FROM Services WHERE is_active = 1")
        services = cursor.fetchall()

        # Get popular tags
        cursor.execute("""
            SELECT t.name, t.category, COUNT(pt.photo_id) as usage_count
            FROM Tags t
            LEFT JOIN PhotoTags pt ON t.tag_id = pt.tag_id
            GROUP BY t.tag_id
            ORDER BY usage_count DESC
            LIMIT 15
        """)
        tags = cursor.fetchall()

        cursor.close()
    except Exception as e:
        print(f"Database error in get_business_context: {e}")
        services = []
        tags = []

    # Build context string
    context = "You are a helpful AI assistant for NailsbyBrookJ, a professional nail salon. Here's information about our business:\n\n"

    context += "SERVICES WE OFFER:\n"
    for service in services:
        context += f"- {service['name']}: ${service['base_price']}"
        if service['description']:
            context += f" - {service['description']}"
        context += "\n"

    context += "\nPOPULAR NAIL STYLES & TRENDS:\n"
    for tag in tags:
        context += f"- {tag['name']}"
        if tag['category']:
            context += f" ({tag['category']})"
        context += "\n"

    context += "\nYou can help customers with:\n"
    context += "- Choosing the right service for their needs\n"
    context += "- Suggesting nail designs and styles\n"
    context += "- Answering questions about prices and duration\n"
    context += "- Providing care tips for nails\n"
    context += "- Recommending seasonal or occasion-appropriate designs\n\n"
    context += "Be friendly, professional, and enthusiastic about nail art!"

    return context

@chatbot.route('/')
def index():
    """Display the chatbot interface"""
    return render_template('chatbot/index.html')

@chatbot.route('/ask', methods=['POST'])
def ask():
    """Process user question and return AI response"""
    try:
        user_message = request.json.get('message', '').strip()

        if not user_message:
            return jsonify({'error': 'Message is required'}), 400

        # Get business context
        business_context = get_business_context()

        # Get Groq client
        client = get_groq_client()

        # Create chat completion with context
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": business_context
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            model="llama-3.3-70b-versatile",  # Latest Llama 70B model on Groq
            temperature=0.7,
            max_tokens=500
        )

        ai_response = chat_completion.choices[0].message.content

        return jsonify({
            'response': ai_response,
            'success': True
        })

    except Exception as e:
        return jsonify({
            'error': f'Error processing request: {str(e)}',
            'success': False
        }), 500

@chatbot.route('/suggestions')
def get_suggestions():
    """Get AI-powered style suggestions based on criteria"""
    try:
        occasion = request.args.get('occasion', '')
        season = request.args.get('season', '')
        color_pref = request.args.get('color', '')

        business_context = get_business_context()

        prompt = f"Based on our available services and popular styles, suggest 3 specific nail designs for:\n"
        if occasion:
            prompt += f"Occasion: {occasion}\n"
        if season:
            prompt += f"Season: {season}\n"
        if color_pref:
            prompt += f"Color preference: {color_pref}\n"

        prompt += "\nProvide creative, detailed suggestions with design elements."

        # Get Groq client
        client = get_groq_client()

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": business_context},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",  # Latest Llama 70B model on Groq
            temperature=0.8,
            max_tokens=400
        )

        suggestions = chat_completion.choices[0].message.content

        return jsonify({
            'suggestions': suggestions,
            'success': True
        })

    except Exception as e:
        return jsonify({
            'error': f'Error getting suggestions: {str(e)}',
            'success': False
        }), 500
