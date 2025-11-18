# Production Setup Checklist

## Quick Fix: Make Changes Reflect in Production

### Step 1: Verify Local Changes are Committed and Pushed

```bash
# Check if there are uncommitted changes
git status

# If there are changes, commit them
git add .
git commit -m "Add Groq support and update configuration"

# Push to GitHub
git push origin main
```

### Step 2: Set Environment Variables in Railway

1. Go to your Railway project dashboard
2. Click on your service
3. Go to **Variables** tab
4. Add/Update these environment variables:

```
GROQ_API_KEY=your-groq-api-key-here
FLASK_ENV=production
```

5. **Important:** After adding variables, Railway will auto-redeploy. Wait 1-2 minutes.

### Step 3: Force Redeploy (if needed)

If changes still don't reflect:

1. Go to Railway dashboard → Your service
2. Click on **Deployments** tab
3. Click **"Redeploy"** on the latest deployment
4. Wait for deployment to complete (usually 2-3 minutes)

### Step 4: Verify Deployment

1. Check Railway logs for any errors:
   - Go to **Deployments** → Click on latest deployment → View logs
2. Test your app:
   - Visit your Railway URL
   - Try selecting "Groq" provider
   - Send a test message

## Common Issues and Solutions

### Issue: Changes not showing up
**Solution:** 
- Ensure code is pushed to GitHub: `git push origin main`
- Check Railway is connected to the correct branch (usually `main`)
- Force redeploy in Railway dashboard

### Issue: Groq not working in production
**Solution:**
- Verify `GROQ_API_KEY` is set in Railway Variables
- Check Railway logs for API errors
- Ensure the key starts with `gsk_`

### Issue: App crashes on startup
**Solution:**
- Check Railway logs for error messages
- Verify all required environment variables are set
- Ensure `requirements.txt` includes `groq>=0.5.0`

### Issue: Database errors
**Solution:**
- If using PostgreSQL, ensure `DATABASE_URL` is set correctly
- Railway can auto-provision PostgreSQL - check the Resources tab

## Railway Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | Yes* | Your Groq API key (get from console.groq.com) |
| `OPENAI_API_KEY` | No | OpenAI API key (alternative to Groq) |
| `DATABASE_URL` | No | PostgreSQL connection string (auto-provisioned by Railway) |
| `FLASK_ENV` | No | Set to `production` for production mode |
| `PORT` | Auto | Automatically set by Railway |

*At least one AI provider key (Groq or OpenAI) is recommended.

## Verify Your Setup

Run this locally to test before deploying:

```bash
# Activate virtual environment
source mychatbot/bin/activate

# Test Groq connection
python -c "import os; from dotenv import load_dotenv; load_dotenv(); from app import groq_client; print('Groq ready!' if groq_client else 'Groq not configured')"
```

If this works locally, the same setup should work in production once environment variables are set in Railway.

