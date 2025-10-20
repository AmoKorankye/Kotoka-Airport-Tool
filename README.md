# 🛬 Kotoka Airport Chatbot API

AI-powered WhatsApp chatbot to assist travelers arriving at Kotoka International Airport in Accra, Ghana.

## 🌟 Features

- **AI-Powered Responses** - Uses OpenAI GPT-4o-mini for intelligent conversations
- **Local Knowledge Base** - Airport facilities, SIM cards, transportation, emergency services
- **Google Maps Integration** - Directions and nearby places
- **WhatsApp Integration** - Send and receive messages via Chatbots Africa API
- **Session Management** - Maintains conversation context per user
- **Multi-Channel** - Works via WhatsApp and web interface

## 🚀 Quick Start (Local Development)

### Prerequisites

- Python 3.12+
- API Keys:
  - OpenAI API Key
  - Google Maps API Key
  - Chatbots Africa API Key

### Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   # Create .env file
   cp .env.example .env
   
   # Add your API keys to .env
   OPENAI_API_KEY=your_key_here
   GOOGLE_MAPS_API_KEY=your_key_here
   CHATBOTS_AFRICA_API_KEY=your_key_here
   ```

3. **Run the server:**
   ```bash
   python3 api.py
   ```

4. **Server runs on:** http://localhost:5001

## 📡 API Endpoints

### Health Check
```bash
GET /api/health
```

### Chat (Web)
```bash
POST /api/chat
Content-Type: application/json

{
  "message": "Where can I buy a SIM card?",
  "session_id": "optional-session-id"
}
```

### WhatsApp Webhook (Receive Messages)
```bash
POST /webhook/whatsapp
Content-Type: application/json

{
  "sender": "0501149794",
  "message": "Hello"
}
```

### WhatsApp Send (Send Messages)
```bash
POST /api/whatsapp/send
Content-Type: application/json

{
  "destination": "0501149794",
  "message": "Welcome to Kotoka Airport!"
}
```

### Reset Conversation
```bash
POST /api/chat/reset
Content-Type: application/json

{
  "session_id": "your-session-id"
}
```

## 📂 Project Structure

```
server/
├── api.py                      # Main Flask application
├── kotoka_knowledge_base.json  # Airport information database
├── requirements.txt            # Python dependencies
├── Procfile                    # Process configuration
├── render.yaml                 # Render deployment config
├── runtime.txt                 # Python version
├── DEPLOY.md                   # Deployment guide
└── README.md                   # This file
```

## 🌐 Deployment

See **[DEPLOY.md](./DEPLOY.md)** for complete deployment instructions to Render.

**Quick Deploy to Render:**
1. Push code to GitHub
2. Create new Web Service on Render
3. Connect GitHub repo
4. Set root directory to `server`
5. Add environment variables
6. Deploy!

**Your webhook URL:**
```
https://your-app-name.onrender.com/webhook/whatsapp
```

## 🧪 Testing

### Test Health
```bash
curl http://localhost:5001/api/health
```

### Test Chat
```bash
curl -X POST http://localhost:5001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Where is the ATM?"}'
```

### Test WhatsApp Send
```bash
curl -X POST http://localhost:5001/api/whatsapp/send \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "0501149794",
    "message": "Test message"
  }'
```

## 📚 Knowledge Base

The chatbot knows about:
- ✈️ Airport facilities (WiFi, ATMs, restaurants, lounges)
- 📱 SIM card vendors and pricing
- 🚕 Transportation options (taxis, ride-hailing, car rentals)
- 🆘 Emergency services and contacts
- 📍 Location-based directions via Google Maps

## 🔧 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4o-mini | Yes |
| `GOOGLE_MAPS_API_KEY` | Google Maps API key | Yes |
| `CHATBOTS_AFRICA_API_KEY` | Chatbots Africa WhatsApp API key | Yes |
| `FLASK_ENV` | Set to `production` in production | No |
| `PORT` | Server port (default: 5001) | No |

## 📝 License

MIT

## 👤 Author

Amo Korankye

---

**Need help?** Check [DEPLOY.md](./DEPLOY.md) for detailed deployment instructions.


A helpful assistant for new arrivals at Kotoka International Airport (Accra, Ghana). This chatbot provides information about airport facilities, transportation options, emergency services, and more.

## Features

- **Airport Facilities**: Find ATMs, bathrooms, restaurants, SIM card vendors, currency exchange
- **Emergency Services**: Medical services, police contacts, lost & found
- **Live Location Data**: Google Maps integration for nearby services
- **Natural Conversation**: OpenAI GPT-4o-mini powered responses