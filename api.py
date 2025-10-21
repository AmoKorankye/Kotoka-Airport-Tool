"""
Kotoka International Airport Chatbot API
Flask API for the airport assistant

Endpoints:
- POST /api/chat - Send a question and get a response
- GET /api/health - Check if API is running
- POST /webhook/whatsapp - Receive WhatsApp messages
- POST /api/whatsapp/send - Send WhatsApp message
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from typing import Dict, List, Any
import openai
import googlemaps
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests


class KotokaAirportChatbot:
    """Main chatbot class for Kotoka International Airport assistance"""
    
    def __init__(self):
        """Initialize the chatbot with API keys and knowledge base"""
        self.openai_client = None
        self.gmaps_client = None
        self.knowledge_base = None
        
        # Load configuration
        self._load_api_keys()
        self._load_knowledge_base()
        
        # Airport coordinates for Google Maps queries
        self.airport_coords = {"lat": 5.6037, "lng": -0.1728}
        
    def _load_api_keys(self):
        """Load API keys from environment variables"""
        try:
            openai_key = os.getenv('OPENAI_API_KEY')
            gmaps_key = os.getenv('GOOGLE_MAPS_API_KEY')
            
            if openai_key:
                self.openai_client = openai.OpenAI(api_key=openai_key)
            else:
                print("Warning: OPENAI_API_KEY not found in environment variables")
                
            if gmaps_key:
                self.gmaps_client = googlemaps.Client(key=gmaps_key)
            else:
                print("Warning: GOOGLE_MAPS_API_KEY not found in environment variables")
                
        except Exception as e:
            print(f"Error loading API keys: {e}")
    
    def _load_knowledge_base(self):
        """Load the airport knowledge base from JSON file"""
        try:
            with open('kotoka_knowledge_base.json', 'r', encoding='utf-8') as f:
                self.knowledge_base = json.load(f)
        except FileNotFoundError:
            print("Error: kotoka_knowledge_base.json not found")
            self.knowledge_base = {}
        except json.JSONDecodeError as e:
            print(f"Error parsing knowledge base JSON: {e}")
            self.knowledge_base = {}
    
    def search_knowledge_base(self, query: str) -> Dict[str, Any]:
        """Search the knowledge base for relevant information"""
        if not self.knowledge_base:
            return {"error": "Knowledge base not available"}
        
        query_lower = query.lower()
        relevant_info = {}
        
        # Keywords mapping to knowledge base sections
        keyword_mappings = {
            'sim': ['sim_cards'],
            'wifi': ['facilities.wifi'],
            'internet': ['facilities.wifi'],
            'atm': ['facilities.atms_banking'],
            'money': ['facilities.atms_banking'],
            'currency': ['facilities.atms_banking'],
            'exchange': ['facilities.atms_banking'],
            'restaurant': ['facilities.restaurants_dining'],
            'food': ['facilities.restaurants_dining'],
            'eat': ['facilities.restaurants_dining'],
            'bathroom': ['facilities.bathrooms'],
            'toilet': ['facilities.bathrooms'],
            'restroom': ['facilities.bathrooms'],
            'emergency': ['emergency_services'],
            'medical': ['emergency_services.medical'],
            'doctor': ['emergency_services.medical'],
            'hospital': ['emergency_services.medical'],
            'police': ['emergency_services.security'],
            'lost': ['emergency_services.lost_and_found'],
            'taxi': ['transportation.taxis'],
            'uber': ['transportation.taxis.ride_hailing'],
            'bolt': ['transportation.taxis.ride_hailing'],
            'transport': ['transportation'],
            'car': ['transportation.car_rentals'],
            'rental': ['transportation.car_rentals'],
            'terminal': ['airport_info.terminals'],
            'lounge': ['facilities.lounges'],
            'shop': ['facilities.shopping'],
            'duty': ['facilities.shopping'],
            'check': ['check_in_services'],
            'baggage': ['check_in_services', 'emergency_services.lost_and_found']
        }
        
        # Find relevant sections based on keywords
        matched_sections = set()
        for keyword, sections in keyword_mappings.items():
            if keyword in query_lower:
                matched_sections.update(sections)
        
        # Extract relevant information
        for section_path in matched_sections:
            section_data = self._get_nested_value(self.knowledge_base, section_path)
            if section_data:
                relevant_info[section_path] = section_data
        
        # If no specific matches, return general airport info
        if not relevant_info:
            relevant_info = {
                "airport_info": self.knowledge_base.get("airport_info", {}),
                "facilities": self.knowledge_base.get("facilities", {})
            }
        
        return relevant_info
    
    def _get_nested_value(self, data: Dict, path: str) -> Any:
        """Get value from nested dictionary using dot notation"""
        keys = path.split('.')
        current = data
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        return current
    
    def _add_airport_maps_links(self, kb_info: Dict) -> Dict:
        """Add Google Maps links for airport facilities"""
        # Add maps link for duty-free and shopping
        if 'facilities.shopping' in kb_info:
            shopping_info = kb_info['facilities.shopping']
            if isinstance(shopping_info, dict):
                shopping_info['maps_link'] = f"https://maps.google.com/?q=Kotoka+International+Airport+Terminal+3+Duty+Free"
        
        # Add maps link for SIM card vendor
        if 'sim_cards' in kb_info:
            sim_info = kb_info['sim_cards']
            if isinstance(sim_info, dict) and 'vendor' in sim_info:
                sim_info['vendor']['maps_link'] = f"https://maps.google.com/?q=Kotoka+International+Airport+Arrival+Hall+SIM+Card"
        
        # Add maps link for airport terminals
        if 'airport_info.terminals' in kb_info:
            kb_info['airport_maps_link'] = f"https://maps.google.com/?q=Kotoka+International+Airport+Accra+Ghana"
        
        return kb_info
    
    def search_google_maps(self, query: str, location_type: str = None) -> List[Dict]:
        """Search Google Maps for nearby places"""
        if not self.gmaps_client:
            return [{"error": "Google Maps API not available"}]
        
        try:
            # Search for places near the airport
            places_result = self.gmaps_client.places_nearby(
                location=self.airport_coords,
                radius=15000,  # 15km radius
                keyword=query,
                type=location_type
            )
            
            places = []
            for place in places_result.get('results', [])[:5]:  # Limit to top 5
                # Get place coordinates for maps link
                location = place.get('geometry', {}).get('location', {})
                lat = location.get('lat')
                lng = location.get('lng')
                
                # Generate Google Maps link
                maps_link = f"https://maps.google.com/?q={lat},{lng}" if lat and lng else None
                
                place_details = {
                    'name': place.get('name'),
                    'rating': place.get('rating'),
                    'address': place.get('vicinity'),
                    'place_id': place.get('place_id'),
                    'types': place.get('types', []),
                    'open_now': place.get('opening_hours', {}).get('open_now'),
                    'maps_link': maps_link,
                    'coordinates': {'lat': lat, 'lng': lng} if lat and lng else None
                }
                places.append(place_details)
            
            return places
            
        except Exception as e:
            return [{"error": f"Google Maps search failed: {str(e)}"}]
    
    def _extract_search_terms(self, message: str) -> str:
        """Extract relevant search terms from user message for Google Maps"""
        stop_words = ['where', 'is', 'are', 'can', 'i', 'find', 'the', 'a', 'an', 'how', 'what', 'near', 'nearby']
        words = message.lower().split()
        search_terms = [word for word in words if word not in stop_words and len(word) > 2]
        return ' '.join(search_terms[:3])
    
    def _build_context(self, kb_info: Dict, maps_info: List[Dict]) -> str:
        """Build context string for OpenAI from knowledge base and maps info"""
        context_parts = []
        
        if kb_info and kb_info != {"error": "Knowledge base not available"}:
            context_parts.append(f"Airport Knowledge Base: {json.dumps(kb_info, indent=2)}")
        
        if maps_info and not any('error' in info for info in maps_info):
            context_parts.append(f"Nearby Places (Google Maps): {json.dumps(maps_info, indent=2)}")
        
        return "\n\n".join(context_parts) if context_parts else "Limited information available"
    
    def generate_response(self, user_message: str, conversation_history: List[Dict] = None) -> str:
        """Generate response using OpenAI API"""
        if not self.openai_client:
            return "Sorry, I'm unable to process your request right now. Please try again later."
        
        if conversation_history is None:
            conversation_history = []
        
        # Search knowledge base for relevant information
        kb_info = self.search_knowledge_base(user_message)
        
        # Add maps links to airport facilities
        kb_info = self._add_airport_maps_links(kb_info)
        
        # Determine if Google Maps search is needed
        maps_info = []
        location_keywords = ['restaurant', 'atm', 'bank', 'hotel', 'store', 'shop', 'near', 'nearby', 'directions']
        if any(keyword in user_message.lower() for keyword in location_keywords):
            search_terms = self._extract_search_terms(user_message)
            if search_terms:
                maps_info = self.search_google_maps(search_terms)
        
        # Build context for OpenAI
        context = self._build_context(kb_info, maps_info)
        
        try:
            # Create system prompt
            system_prompt = """You are a helpful assistant for new arrivals at Kotoka International Airport in Accra, Ghana. 
            
            Your role is to help travelers with:
            - Airport facilities (ATMs, bathrooms, restaurants, SIM cards, currency exchange)
            - Transportation options (Uber, Bolt, taxis, car rentals)
            - Emergency contacts and services
            - General airport navigation and tips
            
            Always be friendly, concise, and practical. Use the provided knowledge base information when available.
            If you don't have specific information, acknowledge it and suggest alternatives.
            
            CRITICAL FORMATTING RULES:
            1. DO NOT use markdown formatting (no **, *, #, etc.)
            2. Write in plain text with natural language
            3. Use simple line breaks for structure (press Enter for new lines)
            4. For links, use this EXACT format: [LINK_TEXT](URL) - nothing else
            5. For location links, use: [Open in Google Maps](maps_link_here)
            6. DO NOT use bullets with * or - symbols
            7. Instead of bullets, use simple numbered lists (1., 2., 3.) or write as flowing text
            
            Example GOOD response:
            "You can buy a SIM card at the Smice Digital SIM card store located on the left-hand side after exiting the arrival hall.
            
            Price: Around $4-$8 (higher than city prices)
            Opening hours: 9 AM - 10 PM (closes after midnight)
            
            [Open in Google Maps](https://maps.google.com/...)
            
            You'll need your passport for registration."
            
            Example BAD response (DO NOT DO THIS):
            "You can buy a SIM card at:
            * **Smice Digital** - Located in arrival hall
            * Price: $4-$8
            **Requirements:**
            - Passport required"
            
            Key guidelines:
            - Keep responses conversational and helpful in plain text
            - Provide specific details like locations, prices, and contact numbers
            - Suggest both airport facilities and nearby options when relevant
            - Always prioritize safety and official services
            - Include Google Maps navigation links in [text](url) format only
            """
            
            # Build messages
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "system", "content": f"Available information: {context}"}
            ]
            
            # Add conversation history (last 6 messages)
            messages.extend(conversation_history[-6:])
            messages.append({"role": "user", "content": user_message})
            
            # Generate response
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=400,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm sorry, I encountered an error while processing your request. Please try rephrasing your question."


# Initialize the chatbot
chatbot = KotokaAirportChatbot()

# Store conversation histories per session (simple in-memory storage)
conversation_sessions = {}


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'Kotoka Airport Chatbot API is running',
        'version': '1.0.0'
    }), 200


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Chat endpoint - receives a question and returns a response
    
    Request body:
    {
        "message": "Where can I buy a SIM card?",
        "session_id": "optional-session-id"
    }
    
    Response:
    {
        "response": "The chatbot response...",
        "session_id": "session-id"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Missing required field: message'
            }), 400
        
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({
                'error': 'Message cannot be empty'
            }), 400
        
        # Get or create session ID
        session_id = data.get('session_id', f"session_{len(conversation_sessions)}")
        
        # Get conversation history for this session
        if session_id not in conversation_sessions:
            conversation_sessions[session_id] = []
        
        conversation_history = conversation_sessions[session_id]
        
        # Generate response
        response_text = chatbot.generate_response(user_message, conversation_history)
        
        # Update conversation history
        conversation_history.append({"role": "user", "content": user_message})
        conversation_history.append({"role": "assistant", "content": response_text})
        
        # Keep only last 12 messages (6 exchanges)
        if len(conversation_history) > 12:
            conversation_sessions[session_id] = conversation_history[-12:]
        
        return jsonify({
            'response': response_text,
            'session_id': session_id
        }), 200
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({
            'error': 'An error occurred processing your request',
            'details': str(e)
        }), 500


@app.route('/api/chat/reset', methods=['POST'])
def reset_conversation():
    """
    Reset conversation history for a session
    
    Request body:
    {
        "session_id": "session-id"
    }
    """
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        if session_id and session_id in conversation_sessions:
            del conversation_sessions[session_id]
            return jsonify({
                'message': 'Conversation history reset successfully'
            }), 200
        
        return jsonify({
            'message': 'No conversation history found for this session'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'An error occurred',
            'details': str(e)
        }), 500


# WhatsApp Integration Functions
def send_whatsapp_message(destination: str, message: str) -> dict:
    """
    Send a WhatsApp message using Chatbots Africa API
    
    Args:
        destination: Phone number (e.g., "0501149794" or "233501149794")
        message: Text message (max 4096 characters)
    
    Returns:
        API response dictionary
    """
    url = "https://api.chatbotsafrica.com/api/v1.0/send/message"
    
    # Ensure message doesn't exceed WhatsApp limit
    truncated_message = message[:4096] if len(message) > 4096 else message
    
    # Get API key
    api_key = os.getenv('CHATBOTS_AFRICA_API_KEY')
    
    # Normalize destination to local Ghana format (0XXXXXXXXX)
    # Remove +233 or 233 prefix and ensure it starts with 0
    normalized_dest = destination.strip()
    if normalized_dest.startswith('+233'):
        normalized_dest = '0' + normalized_dest[4:]
    elif normalized_dest.startswith('233'):
        normalized_dest = '0' + normalized_dest[3:]
    elif not normalized_dest.startswith('0'):
        normalized_dest = '0' + normalized_dest
    
    # Correct payload format per Chatbots Africa documentation
    payload = {
        "apikey": api_key,
        "destination": normalized_dest,
        "message": truncated_message
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # DEBUG: Log request details (mask API key)
    print(f"\n🔍 DEBUG - WhatsApp API Request:")
    print(f"   URL: {url}")
    print(f"   Destination (original): {destination}")
    print(f"   Destination (normalized): {normalized_dest}")
    print(f"   API Key present: {bool(api_key)}")
    print(f"   API Key (masked): {'****' + api_key[-4:] if api_key else 'MISSING'}")
    print(f"   Message length: {len(truncated_message)}")
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        # DEBUG: Log response details
        print(f"\n📥 DEBUG - WhatsApp API Response:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Response Body: {response.text}")
        
        response.raise_for_status()
        result = response.json()
        
        # Check if API returned success
        if result.get('success'):
            print(f"✅ WhatsApp message sent to {destination}")
            print(f"   Status: {result.get('message', {}).get('message_status', 'unknown')}")
            print(f"   Message ID: {result.get('message', {}).get('message_id', 'N/A')}")
            return result
        else:
            print(f"⚠️  WhatsApp API returned success=false")
            print(f"   Reason: {result.get('reason', 'Unknown')}")
            return {"success": False, "error": result.get('reason', 'API returned success=false'), "details": result}
        
    except requests.exceptions.Timeout:
        print(f"❌ Timeout sending WhatsApp message to {destination}")
        return {"success": False, "error": "Request timeout"}
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending WhatsApp message to {destination}: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return {"success": False, "error": str(e)}


@app.route('/webhook/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """
    Webhook endpoint to receive incoming WhatsApp messages from Chatbots Africa
    
    Handles WhatsApp Business API format with nested structure
    """
    try:
        data = request.get_json()
        
        # DEBUG: Log the raw payload
        print(f"\n🔍 DEBUG - Webhook received payload:")
        print(f"   Raw JSON: {data}")
        
        if not data:
            return jsonify({'error': 'No data received'}), 400
        
        # Check if this is a verification/health check
        if 'challenge' in data or 'verify' in data:
            print("✅ Webhook verification request received")
            return jsonify({'challenge': data.get('challenge', 'ok')}), 200
        
        # Handle WhatsApp Business API format (nested structure)
        sender = None
        user_message = None
        
        if 'entry' in data:
            # WhatsApp Business API format
            try:
                entry = data['entry'][0]
                changes = entry['changes'][0]
                value = changes['value']
                
                # Check if this is a status update (not a message)
                if 'statuses' in value:
                    print("ℹ️  Status update received (ignoring)")
                    return jsonify({'status': 'ok', 'message': 'Status update received'}), 200
                
                messages = value.get('messages', [])
                
                if messages and len(messages) > 0:
                    message_obj = messages[0]
                    sender = message_obj.get('from')
                    
                    # Extract message text based on type
                    if message_obj.get('type') == 'text':
                        user_message = message_obj.get('text', {}).get('body')
                    
                    print(f"📱 Parsed WhatsApp Business format:")
                    print(f"   Sender: {sender}")
                    print(f"   Message: {user_message}")
            except (KeyError, IndexError, TypeError) as e:
                print(f"⚠️  Error parsing WhatsApp Business format: {e}")
        
        # Fallback to simple format (for direct testing)
        if not sender:
            sender = data.get('sender') or data.get('from') or data.get('phone')
        if not user_message:
            user_message = data.get('message') or data.get('text') or data.get('body')
        
        if not sender or not user_message:
            print("⚠️  Missing sender or message in webhook payload")
            print(f"   Available keys: {list(data.keys())}")
            return jsonify({'error': 'Missing required fields: sender and message', 'received_keys': list(data.keys())}), 400
        
        print(f"\n📱 Incoming WhatsApp message from {sender}")
        print(f"   Message: {user_message}")
        
        # Create or get session ID for this phone number
        session_id = f"whatsapp_{sender}"
        
        if session_id not in conversation_sessions:
            conversation_sessions[session_id] = []
        
        conversation_history = conversation_sessions[session_id]
        
        # Generate response using chatbot
        print("🤖 Generating response...")
        response_text = chatbot.generate_response(user_message, conversation_history)
        
        # Update conversation history
        conversation_history.append({"role": "user", "content": user_message})
        conversation_history.append({"role": "assistant", "content": response_text})
        
        # Keep only last 12 messages (6 exchanges)
        if len(conversation_history) > 12:
            conversation_sessions[session_id] = conversation_history[-12:]
        
        # Send response back via WhatsApp
        print("📤 Sending response via WhatsApp...")
        whatsapp_result = send_whatsapp_message(sender, response_text)
        
        if whatsapp_result.get('success'):
            print("✅ Response sent successfully\n")
            return jsonify({
                'status': 'success',
                'message': 'Response sent',
                'whatsapp_status': whatsapp_result
            }), 200
        else:
            print("⚠️  Failed to send WhatsApp response\n")
            return jsonify({
                'status': 'partial_success',
                'message': 'Response generated but failed to send',
                'error': whatsapp_result.get('error')
            }), 500
        
    except Exception as e:
        print(f"❌ Error in WhatsApp webhook: {e}\n")
        return jsonify({
            'error': 'An error occurred processing the webhook',
            'details': str(e)
        }), 500


@app.route('/api/whatsapp/send', methods=['POST'])
def send_whatsapp():
    """
    Manual endpoint to send WhatsApp messages
    
    Request body:
    {
        "destination": "0501149794",
        "message": "Welcome to Kotoka Airport!"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'destination' not in data or 'message' not in data:
            return jsonify({
                'error': 'Missing required fields: destination and message'
            }), 400
        
        destination = data['destination']
        message = data['message']
        
        # Send WhatsApp message
        result = send_whatsapp_message(destination, message)
        
        if result.get('success'):
            return jsonify({
                'status': 'success',
                'message': 'WhatsApp message sent successfully',
                'details': result
            }), 200
        else:
            return jsonify({
                'status': 'failed',
                'message': 'Failed to send WhatsApp message',
                'error': result.get('error')
            }), 500
        
    except Exception as e:
        print(f"Error in send WhatsApp endpoint: {e}")
        return jsonify({
            'error': 'An error occurred',
            'details': str(e)
        }), 500


if __name__ == '__main__':
    # Check for required environment variables
    required_vars = ['OPENAI_API_KEY', 'GOOGLE_MAPS_API_KEY']
    optional_vars = ['CHATBOTS_AFRICA_API_KEY']
    
    missing_required = [var for var in required_vars if not os.getenv(var)]
    missing_optional = [var for var in optional_vars if not os.getenv(var)]
    
    if missing_required:
        print("⚠️  Warning: Missing required environment variables:")
        for var in missing_required:
            print(f"   - {var}")
        print("\nThe API will start but some features may not work properly.")
    
    if missing_optional:
        print("\n💡 Optional features disabled (missing environment variables):")
        for var in missing_optional:
            print(f"   - {var} (WhatsApp integration disabled)")
    
    print("\n🛬 Starting Kotoka Airport Chatbot API...")
    print("📍 API running on http://localhost:5001")
    print("\nEndpoints:")
    print("  - GET  /api/health              - Health check")
    print("  - POST /api/chat                - Send a message (web)")
    print("  - POST /api/chat/reset          - Reset conversation")
    print("  - POST /webhook/whatsapp        - Receive WhatsApp messages")
    print("  - POST /api/whatsapp/send       - Send WhatsApp message")
    print("\n")
    
    # Get port from environment variable (for production) or use 5001 (for local dev)
    port = int(os.environ.get("PORT", 5001))
    
    # Run with debug=False in production
    debug_mode = os.environ.get("FLASK_ENV") != "production"
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
