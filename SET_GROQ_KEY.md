# Set Groq API Key in Railway Production

## Quick Steps

1. **Go to Railway Dashboard**
   - Visit https://railway.app
   - Log in to your account
   - Click on your project

2. **Navigate to Your Service**
   - Click on the service running your chatbot

3. **Open Variables Tab**
   - Click on the **"Variables"** tab in the top menu

4. **Add Groq API Key**
   - Click **"+ New Variable"** or **"Add Variable"**
   - **Variable Name:** `GROQ_API_KEY`
   - **Variable Value:** `your-groq-api-key-here` (get from https://console.groq.com)
   - Click **"Add"** or **"Save"**

5. **Wait for Redeploy**
   - Railway will automatically detect the new variable and redeploy
   - Wait 2-3 minutes for deployment to complete

6. **Verify It Works**
   - Visit your Railway app URL
   - Select "Groq" from the provider dropdown
   - Send a test message
   - It should work with Groq's Llama 3 model!

## Optional: Set Other Variables

You can also set these optional variables:

- `FLASK_ENV=production` (recommended for production)
- `WEB_CONCURRENCY=1` (if you still see Gunicorn errors)

## Troubleshooting

If Groq still doesn't work:

1. **Check Railway Logs**
   - Go to Deployments → Latest deployment → View logs
   - Look for any errors related to Groq

2. **Verify the Key**
   - Make sure the API key is correct (starts with `gsk_`)
   - Check that there are no extra spaces

3. **Check Health Endpoint**
   - Visit `https://your-app.railway.app/health`
   - Should show `"groq_configured": true`

4. **Redeploy Manually**
   - Go to Deployments tab
   - Click "Redeploy" on the latest deployment

