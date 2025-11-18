# Railway Production Fix - WEB_CONCURRENCY Error

## Quick Fix (Required)

**You MUST set this environment variable in Railway:**

1. Go to Railway Dashboard → Your Service
2. Click on **Variables** tab
3. Add new variable:
   - **Name:** `WEB_CONCURRENCY`
   - **Value:** `1`
4. Click **Add**
5. Railway will automatically redeploy

This will fix the Gunicorn error immediately.

## Why This Happens

Railway sets `WEB_CONCURRENCY=""` (empty string) by default, which causes Gunicorn to crash when it tries to convert it to an integer.

## Alternative: If Setting Environment Variable Doesn't Work

If Railway is still calling gunicorn directly (bypassing our wrapper), you can:

1. **Option 1:** Set `WEB_CONCURRENCY=1` in Railway Variables (recommended)
2. **Option 2:** Railway might be auto-detecting. Check Railway settings to disable auto-detection
3. **Option 3:** Use a different WSGI server temporarily (not recommended)

## Verify Fix

After setting the variable:
1. Check Railway logs - should see Gunicorn starting successfully
2. Visit your app URL - should load
3. Test `/health` endpoint

