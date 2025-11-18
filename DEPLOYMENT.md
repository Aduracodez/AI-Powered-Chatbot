# Production Deployment Guide

This guide covers deploying the AI Power Chatbot to various production platforms.

## Prerequisites

- Production-ready database (PostgreSQL recommended for production)
- Environment variables configured
- Domain name (optional, for custom domains)

## Environment Variables

Set these in your production environment:

```bash
# Required: At least one AI provider
OPENAI_API_KEY=your-openai-api-key  # Optional
GROQ_API_KEY=your-groq-api-key      # Optional (get from https://console.groq.com)

# Database (optional - SQLite used by default)
DATABASE_URL=postgresql://user:password@host:port/dbname  # For PostgreSQL

# Production settings
FLASK_ENV=production
SECRET_KEY=your-secret-key-here  # For session security
```

## Deployment Options

### 1. Railway (Recommended - Easiest)

**Steps:**

1. Sign up at [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Connect your GitHub repository
4. Add environment variables in Railway dashboard:
   - **GROQ_API_KEY** (recommended - get from https://console.groq.com)
   - `OPENAI_API_KEY` (optional)
   - `DATABASE_URL` (optional - Railway can provision PostgreSQL automatically)
   - `FLASK_ENV=production` (optional but recommended)
5. Railway will auto-detect Python and deploy
6. Your app will be live at `https://your-app.railway.app`

**Important:** After adding environment variables, Railway will automatically redeploy. If changes don't reflect:
- Go to your Railway project → Settings → Variables
- Verify all environment variables are set correctly
- Click "Redeploy" in the Deployments tab to force a new deployment

**Railway will automatically:**
- Detect `Procfile` and use gunicorn
- Set `PORT` environment variable
- Handle HTTPS/SSL

---

### 2. Render

**Steps:**

1. Sign up at [render.com](https://render.com)
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn --bind 0.0.0.0:$PORT wsgi:app`
   - **Environment:** Python 3
5. Add environment variables in the dashboard
6. Add PostgreSQL database (optional, under "New" → "PostgreSQL")
7. Deploy!

**Free tier available** with some limitations.

---

### 3. Heroku

**Steps:**

1. Install Heroku CLI: `brew install heroku/brew/heroku` (Mac) or [download](https://devcenter.heroku.com/articles/heroku-cli)
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Add PostgreSQL: `heroku addons:create heroku-postgresql:mini`
5. Set environment variables:
   ```bash
   heroku config:set OPENAI_API_KEY=your-key
   ```
6. Deploy: `git push heroku main`
7. Open: `heroku open`

**Note:** Heroku free tier was discontinued, but paid plans start at $5/month.

---

### 4. AWS Elastic Beanstalk

**Steps:**

1. Install EB CLI: `pip install awsebcli`
2. Initialize: `eb init -p python-3.12 your-app-name`
3. Create environment: `eb create your-env-name`
4. Set environment variables:
   ```bash
   eb setenv OPENAI_API_KEY=your-key DATABASE_URL=your-db-url
   ```
5. Deploy: `eb deploy`
6. Open: `eb open`

**Cost:** Pay for what you use (EC2, RDS, etc.)

---

### 5. DigitalOcean App Platform

**Steps:**

1. Sign up at [digitalocean.com](https://digitalocean.com)
2. Go to "Apps" → "Create App"
3. Connect GitHub repository
4. Configure:
   - **Type:** Web Service
   - **Build Command:** `pip install -r requirements.txt`
   - **Run Command:** `gunicorn --bind 0.0.0.0:$PORT wsgi:app`
5. Add environment variables
6. Add PostgreSQL database (optional)
7. Deploy!

**Pricing:** Starts at $5/month.

---

### 6. Google Cloud Run (Serverless)

**Steps:**

1. Install Google Cloud SDK
2. Create `Dockerfile` (see below)
3. Build and deploy:
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT-ID/chatbot
   gcloud run deploy chatbot --image gcr.io/PROJECT-ID/chatbot --platform managed
   ```
4. Set environment variables in Cloud Run console

**Cost:** Pay per request (very cost-effective for low traffic).

---

### 7. Fly.io

**Steps:**

1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Login: `fly auth login`
3. Launch: `fly launch`
4. Set secrets:
   ```bash
   fly secrets set OPENAI_API_KEY=your-key
   ```
5. Deploy: `fly deploy`

**Free tier:** 3 shared VMs.

---

## Database Setup

### For Production (PostgreSQL Recommended)

1. **Railway/Render:** They can provision PostgreSQL automatically
2. **Heroku:** `heroku addons:create heroku-postgresql:mini`
3. **AWS:** Use RDS PostgreSQL
4. **Manual Setup:** Install PostgreSQL and set `DATABASE_URL`

**Update your `.env` or environment variables:**
```bash
DATABASE_URL=postgresql://user:password@host:port/dbname
```

The app will automatically use PostgreSQL if `DATABASE_URL` is set.

---

## Docker Deployment (Optional)

Create a `Dockerfile` for containerized deployment:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "2", "--timeout", "120", "wsgi:app"]
```

Then deploy to:
- Docker Hub + any container platform
- Google Cloud Run
- AWS ECS/Fargate
- Azure Container Instances

---

## Testing Production Locally

Test with gunicorn before deploying:

```bash
# Install gunicorn
pip install gunicorn

# Run production server
gunicorn --bind 0.0.0.0:5000 --workers 2 wsgi:app
```

---

## Security Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Use strong `SECRET_KEY` for sessions
- [ ] Enable HTTPS/SSL (most platforms do this automatically)
- [ ] Use PostgreSQL instead of SQLite for production
- [ ] Keep API keys secure (use environment variables, never commit)
- [ ] Set up proper CORS if needed
- [ ] Add rate limiting (consider Flask-Limiter)
- [ ] Monitor logs and errors

---

## Monitoring & Logs

Most platforms provide:
- **Logs:** View in dashboard or via CLI
- **Metrics:** CPU, memory, request counts
- **Alerts:** Set up for errors or downtime

**Recommended:** Add error tracking (Sentry, Rollbar) for production.

---

## Quick Deploy Commands

**Railway:**
```bash
railway up
```

**Render:**
```bash
# Auto-deploys on git push
git push origin main
```

**Heroku:**
```bash
git push heroku main
```

**Fly.io:**
```bash
fly deploy
```

---

## Troubleshooting

**App won't start:**
- Check logs: `heroku logs --tail` or platform dashboard
- Verify environment variables are set
- Ensure database is accessible

**Database errors:**
- Verify `DATABASE_URL` is correct
- Check database is running and accessible
- Run migrations if needed

**502 Bad Gateway:**
- Check gunicorn is running
- Verify `PORT` environment variable is set
- Check worker timeout settings

---

## Cost Comparison (Approximate)

| Platform | Free Tier | Paid Starting |
|----------|-----------|---------------|
| Railway  | $5 credit | $5/month |
| Render    | Limited   | $7/month |
| Heroku    | None      | $5/month |
| Fly.io    | 3 VMs     | Pay as you go |
| Cloud Run | Generous  | Pay per use |
| DigitalOcean | None   | $5/month |

---

## Recommended for Beginners

**Railway** or **Render** are the easiest:
- Automatic HTTPS
- Easy database setup
- Simple environment variable management
- Auto-deploy from GitHub

Choose based on your needs and budget!

