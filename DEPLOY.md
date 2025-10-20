# 🚀 Deploying Kotoka Airport API to Render

This guide will help you deploy the Flask API to Render in under 10 minutes.

## 📋 Prerequisites

- GitHub account
- Render account (sign up at [render.com](https://render.com))
- Your API keys:
  - OpenAI API Key
  - Google Maps API Key
  - Chatbots Africa API Key: `d4166711-2395-4c1e-b11d-ff0146393df3`

---

## 🎯 Quick Deploy (Recommended)

### Step 1: Push to GitHub

Make sure your code is pushed to GitHub:

```bash
cd /Users/amo-korankye/Desktop/amokorankye/dev/mnotify/ghana-airports
git add .
git commit -m "Prepare server for Render deployment"
git push origin main
```

### Step 2: Create New Web Service on Render

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com/
   - Click **"New +"** → **"Web Service"**

2. **Connect Repository**
   - Click **"Connect account"** to link GitHub
   - Find and select: `AmoKorankye/Kotoka-Airport-Tool`
   - Click **"Connect"**

3. **Configure Service**

   Fill in these details:

   | Field | Value |
   |-------|-------|
   | **Name** | `kotoka-airport-api` |
   | **Region** | Choose closest to Ghana (e.g., Frankfurt) |
   | **Branch** | `main` |
   | **Root Directory** | `server` |
   | **Runtime** | `Python 3` |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `gunicorn api:app` |
   | **Instance Type** | `Free` (or `Starter` for better performance) |

4. **Add Environment Variables**

   Click **"Advanced"** → **"Add Environment Variable"**

   Add these three variables:

   ```
   OPENAI_API_KEY=your_openai_key_here
   GOOGLE_MAPS_API_KEY=your_google_maps_key_here
   CHATBOTS_AFRICA_API_KEY=d4166711-2395-4c1e-b11d-ff0146393df3
   ```

   Also add:
   ```
   FLASK_ENV=production
   ```

5. **Create Web Service**
   - Click **"Create Web Service"**
   - Render will start building and deploying your API

### Step 3: Wait for Deployment

- Initial deployment takes 2-5 minutes
- Watch the logs in real-time
- Look for: `Your service is live 🎉`

### Step 4: Get Your API URL

Once deployed, your API will be available at:

```
https://kotoka-airport-api.onrender.com
```

**Your Webhook URL for Chatbots Africa:**
```
https://kotoka-airport-api.onrender.com/webhook/whatsapp
```

---

## ✅ Testing Your Deployment

### 1. Test Health Endpoint

```bash
curl https://kotoka-airport-api.onrender.com/api/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "message": "Kotoka Airport Chatbot API is running",
  "version": "1.0.0"
}
```

### 2. Test WhatsApp Send

```bash
curl -X POST https://kotoka-airport-api.onrender.com/api/whatsapp/send \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "0501149794",
    "message": "🛬 Hello from production! Testing Kotoka Airport Chatbot."
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "channel": "whatsapp",
  "message": {
    "message_status": "sent",
    "message_id": "wamid.xxx..."
  }
}
```

### 3. Test Webhook (Simulate Incoming Message)

```bash
curl -X POST https://kotoka-airport-api.onrender.com/webhook/whatsapp \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "0501149794",
    "message": "Where can I get a SIM card?"
  }'
```

This should:
- Process the message
- Generate AI response
- Send reply via WhatsApp
- Return success status

---

## 🔧 Configure Chatbots Africa Webhook

Now that your API is live, configure the webhook:

### Step 1: Copy Your Webhook URL

```
https://kotoka-airport-api.onrender.com/webhook/whatsapp
```

### Step 2: Add to Chatbots Africa Dashboard

1. Login to Chatbots Africa dashboard
2. Find **Webhook Settings** or **Callback URL**
3. Paste your webhook URL:
   ```
   https://kotoka-airport-api.onrender.com/webhook/whatsapp
   ```
4. Save the settings

### Step 3: Test with Real WhatsApp

Send a WhatsApp message to: **0209949003**

Example messages to try:
- "Where can I buy a SIM card?"
- "How do I get to the city center?"
- "Tell me about airport facilities"
- "Where is the nearest ATM?"

You should receive an AI-generated response within seconds! 🎉

---

## 📊 Monitoring Your API

### View Logs

1. Go to Render Dashboard
2. Click on your service: `kotoka-airport-api`
3. Click **"Logs"** tab
4. View real-time logs

**Look for these log messages:**

```
🛬 Starting Kotoka Airport Chatbot API...
📍 API running on http://localhost:10000
📱 WhatsApp message received from 0501149794
💬 Message: Where can I buy a SIM card?
🤖 Generating response...
✅ WhatsApp message sent to 0501149794
```

### Check Service Health

```bash
curl https://kotoka-airport-api.onrender.com/api/health
```

---

## 🔄 Updating Your Deployment

When you make code changes:

```bash
git add .
git commit -m "Update: description of changes"
git push origin main
```

Render will automatically:
1. Detect the push
2. Rebuild the service
3. Deploy the new version
4. Zero-downtime deployment (on paid plans)

---

## 📁 Production Files

Your server directory now contains only essential files:

```
server/
├── api.py                      # Main Flask application
├── kotoka_knowledge_base.json  # Airport data
├── requirements.txt            # Python dependencies
├── Procfile                    # Process configuration
├── render.yaml                 # Render deployment config
├── runtime.txt                 # Python version
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

**Note:** `.env` file is NOT pushed to Git (it's in .gitignore). Environment variables are set in Render dashboard.

---

## 💰 Render Pricing

### Free Tier
- **Cost:** $0/month
- **Limitations:**
  - Spins down after 15 minutes of inactivity
  - Cold start takes 30-60 seconds
  - 750 hours/month free
- **Best for:** Testing and low-traffic apps

### Starter Plan
- **Cost:** $7/month
- **Benefits:**
  - Always on (no spin down)
  - Instant response times
  - Better for production use
  - Custom domains

**Recommendation:** Start with free tier, upgrade if you need faster response times.

---

## 🐛 Troubleshooting

### Deployment Failed

**Check build logs:**
1. Go to Render dashboard
2. Click on your service
3. Check "Logs" tab for errors

**Common issues:**
- Missing dependencies in requirements.txt
- Wrong Python version
- Syntax errors in code

### Environment Variables Not Working

**Check if variables are set:**
1. Go to service settings
2. Click "Environment" tab
3. Verify all three API keys are present
4. Click "Save Changes" if you made updates

### API Returns 500 Error

**Check application logs:**
```bash
# In Render dashboard, view logs
# Look for Python errors or stack traces
```

**Common causes:**
- Missing API keys
- Knowledge base file not found
- OpenAI API quota exceeded

### Webhook Not Receiving Messages

**Verify webhook URL:**
1. Check Chatbots Africa dashboard
2. Ensure URL is exactly:
   ```
   https://kotoka-airport-api.onrender.com/webhook/whatsapp
   ```
3. Must be HTTPS (not HTTP)
4. No trailing slash

**Test webhook manually:**
```bash
curl -X POST https://kotoka-airport-api.onrender.com/webhook/whatsapp \
  -H "Content-Type: application/json" \
  -d '{"sender": "0501149794", "message": "test"}'
```

### Free Tier Spin Down

On free tier, service sleeps after 15 minutes of inactivity.

**Solutions:**
1. Upgrade to Starter plan ($7/month) for always-on
2. Use a ping service to keep it awake
3. Accept 30-60 second delay on first request

---

## 🔒 Security Best Practices

### 1. Never Commit API Keys
- ✅ API keys are in Render environment variables
- ✅ `.env` is in `.gitignore`
- ❌ Never put keys in code

### 2. Use HTTPS Only
- ✅ Render provides SSL automatically
- ✅ Webhook requires HTTPS

### 3. Monitor Logs
- Check logs regularly for errors
- Watch for unusual activity
- Set up error alerts (Render supports Slack/email notifications)

---

## 📞 Support

### Render Support
- Documentation: https://render.com/docs
- Community: https://community.render.com/
- Email: support@render.com

### Chatbots Africa Support
- Check their dashboard for support contact
- Review API documentation

### Your API Endpoints

```
GET  https://kotoka-airport-api.onrender.com/api/health
POST https://kotoka-airport-api.onrender.com/api/chat
POST https://kotoka-airport-api.onrender.com/api/chat/reset
POST https://kotoka-airport-api.onrender.com/webhook/whatsapp
POST https://kotoka-airport-api.onrender.com/api/whatsapp/send
```

---

## 🎉 Success Checklist

- [ ] Code pushed to GitHub
- [ ] Render service created
- [ ] Environment variables configured
- [ ] Service deployed successfully
- [ ] Health check passes
- [ ] WhatsApp send test works
- [ ] Webhook URL configured in Chatbots Africa
- [ ] Real WhatsApp message test successful
- [ ] Logs show messages being processed
- [ ] AI responses being sent

---

## 🚀 You're Live!

Congratulations! Your Kotoka Airport Chatbot API is now live and ready to help travelers!

**Next Steps:**
1. Share your WhatsApp business number: **0209949003**
2. Monitor logs for usage patterns
3. Update knowledge base as needed
4. Consider upgrading to paid plan for better performance

Need to make updates? Just push to GitHub and Render will auto-deploy! 🎊
