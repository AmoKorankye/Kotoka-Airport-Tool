# ✅ Render Deployment Checklist

Use this checklist to ensure smooth deployment of your Kotoka Airport API.

## Before Deployment

- [ ] All code changes committed to git
- [ ] Code pushed to GitHub (main branch)
- [ ] API keys ready:
  - [ ] OpenAI API Key
  - [ ] Google Maps API Key
  - [ ] Chatbots Africa API Key: `d4166711-2395-4c1e-b11d-ff0146393df3`

## Render Setup

- [ ] Signed up for Render account at https://render.com
- [ ] GitHub account connected to Render
- [ ] Created new Web Service
- [ ] Selected repository: `AmoKorankye/Kotoka-Airport-Tool`
- [ ] Set root directory: `server`
- [ ] Configured build command: `pip install -r requirements.txt`
- [ ] Configured start command: `gunicorn api:app`
- [ ] Selected instance type (Free or Starter)

## Environment Variables

Add these in Render dashboard (Settings → Environment):

- [ ] `OPENAI_API_KEY` = `your_key`
- [ ] `GOOGLE_MAPS_API_KEY` = `your_key`
- [ ] `CHATBOTS_AFRICA_API_KEY` = `d4166711-2395-4c1e-b11d-ff0146393df3`
- [ ] `FLASK_ENV` = `production`

## Deployment

- [ ] Clicked "Create Web Service"
- [ ] Deployment started (watch logs)
- [ ] Deployment completed successfully
- [ ] Service is live (green indicator)

## Testing

- [ ] Health check works:
  ```bash
  curl https://your-app.onrender.com/api/health
  ```

- [ ] WhatsApp send works:
  ```bash
  curl -X POST https://your-app.onrender.com/api/whatsapp/send \
    -H "Content-Type: application/json" \
    -d '{"destination": "0501149794", "message": "Test"}'
  ```

- [ ] Webhook endpoint accessible:
  ```bash
  curl -X POST https://your-app.onrender.com/webhook/whatsapp \
    -H "Content-Type: application/json" \
    -d '{"sender": "0501149794", "message": "Hello"}'
  ```

## Chatbots Africa Configuration

- [ ] Logged into Chatbots Africa dashboard
- [ ] Found webhook/callback URL settings
- [ ] Added webhook URL: `https://your-app.onrender.com/webhook/whatsapp`
- [ ] Saved webhook configuration

## Final Testing

- [ ] Sent test WhatsApp message to: **0209949003**
- [ ] Received AI-generated response
- [ ] Checked Render logs for message processing
- [ ] Tested multiple questions to verify context retention
- [ ] Verified response quality and accuracy

## Monitoring

- [ ] Bookmarked Render dashboard for logs
- [ ] Set up email/Slack alerts (optional)
- [ ] Tested cold start time (for free tier)
- [ ] Documented API URL for future reference

## Documentation

- [ ] Updated team/client with WhatsApp number: **0209949003**
- [ ] Shared API endpoint URL
- [ ] Documented any custom configurations
- [ ] Added monitoring/logging procedures

## Post-Deployment

- [ ] Monitor logs for first 24 hours
- [ ] Check for any errors or warnings
- [ ] Verify response times are acceptable
- [ ] Consider upgrading to paid tier if needed

---

## Quick Reference

**Your API URL:** `https://your-app-name.onrender.com`

**Webhook URL:** `https://your-app-name.onrender.com/webhook/whatsapp`

**WhatsApp Business Number:** `0209949003`

**Support:**
- Render: https://render.com/docs
- See DEPLOY.md for detailed troubleshooting

---

## Notes

_Add any deployment-specific notes here_

**Deployed on:** _____________________

**Deployed by:** Amo Korankye

**Instance Type:** Free / Starter / Standard

**Region:** _____________________

---

✅ All checks passed? You're ready to go live! 🚀
