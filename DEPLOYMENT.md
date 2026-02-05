# Deployment Guide - HRMS Lite

Complete guide to deploy your HRMS Lite application to production.

## \ud83c\udfc1 Quick Start

- **Backend**: Render + PostgreSQL
- **Frontend**: Vercel
- **Time**: ~15 minutes

---

## \ud83d\udd34 Backend Deployment (Render)

### Step 1: Create PostgreSQL Database

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New** → **PostgreSQL**
3. Configure:
   - **Name**: `hrms-db`
   - **Database**: `hrms_db`
   - **User**: (auto-generated)
   - **Region**: Select nearest to you
   - **Plan**: Free or Starter
4. Click **Create Database**
5. Save connection details:
   - Internal Database URL
   - Hostname
   - Port
   - Database name
   - Username
   - Password

### Step 2: Create Web Service

1. Click **New** → **Web Service**
2. Connect your Git repository
3. Configure:
   - **Name**: `hrms-backend`
   - **Region**: Same as database
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**:
     ```bash
     pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
     ```
   - **Start Command**:
     ```bash
     gunicorn hrms.wsgi:application --bind 0.0.0.0:$PORT --workers 3
     ```

### Step 3: Environment Variables

Add these environment variables in Render:

```env
USE_POSTGRESQL=True
DATABASE_NAME=<from_postgresql_database>
DATABASE_USER=<from_postgresql_database>
DATABASE_PASSWORD=<from_postgresql_database>
DATABASE_HOST=<from_postgresql_database>
DATABASE_PORT=5432
SECRET_KEY=<generate_random_50_char_string>
DEBUG=False
CORS_ORIGINS=https://your-frontend-domain.vercel.app
```

**Generate SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 4: Deploy

1. Click **Create Web Service**
2. Wait for deployment (3-5 minutes)
3. Test your API: `https://hrms-backend.onrender.com/api/employees/`

---

## \ud83d\udd35 Frontend Deployment (Vercel)

### Step 1: Prepare Repository

Ensure your frontend code is in a `frontend` directory.

### Step 2: Deploy to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **Add New** → **Project**
3. Import your Git repository
4. Configure:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `yarn build`
   - **Output Directory**: `build`

### Step 3: Environment Variables

Add environment variable:

```env
REACT_APP_BACKEND_URL=https://hrms-backend.onrender.com
```

Replace with your actual Render backend URL.

### Step 4: Deploy

1. Click **Deploy**
2. Wait for build (2-3 minutes)
3. Your app is live: `https://your-app.vercel.app`

### Step 5: Update Backend CORS

Go back to Render and update `CORS_ORIGINS`:
```env
CORS_ORIGINS=https://your-app.vercel.app
```

---

## \ud83d\udfeb Alternative: Railway

### PostgreSQL + Backend on Railway

1. **Install Railway CLI**
```bash
npm i -g @railway/cli
```

2. **Login & Initialize**
```bash
railway login
cd backend
railway init
```

3. **Add PostgreSQL**
```bash
railway add --database postgresql
```

4. **Configure Variables**
```bash
railway variables set USE_POSTGRESQL=True
railway variables set DEBUG=False
railway variables set SECRET_KEY=<your-secret-key>
railway variables set CORS_ORIGINS=<your-frontend-url>
```

5. **Deploy**
```bash
railway up
```

---

## \ud83d\udfea Alternative: Supabase for Database

### Step 1: Create Supabase Project

1. Go to [Supabase](https://supabase.com/)
2. Create new project
3. Go to **Settings** → **Database**
4. Copy connection string

### Step 2: Configure Django

Update `.env`:
```env
USE_POSTGRESQL=True
DATABASE_HOST=db.xxxxxxxxxxxxx.supabase.co
DATABASE_PORT=5432
DATABASE_NAME=postgres
DATABASE_USER=postgres
DATABASE_PASSWORD=<your-password>
```

---

## \u2705 Verification Checklist

### Backend
- [ ] Database connected successfully
- [ ] Migrations applied
- [ ] Static files collected
- [ ] API endpoints responding
- [ ] CORS configured correctly

**Test:**
```bash
curl https://your-backend.onrender.com/api/employees/
```

### Frontend
- [ ] Environment variable set
- [ ] Build successful
- [ ] App loads correctly
- [ ] API calls working
- [ ] Navigation working

**Test:**
Visit `https://your-app.vercel.app`

---

## \ud83d\udd27 Troubleshooting

### Backend Issues

**Issue: Database connection failed**
```
Solution: Verify DATABASE_HOST, DATABASE_PORT, DATABASE_NAME are correct
Check: PostgreSQL is running and accessible
```

**Issue: Static files not loading**
```
Solution: Run python manage.py collectstatic
Check: STATIC_ROOT is configured correctly
```

**Issue: CORS errors**
```
Solution: Update CORS_ORIGINS with exact frontend URL (no trailing slash)
Example: CORS_ORIGINS=https://your-app.vercel.app
```

**Issue: 500 Server Error**
```
Solution: Check Render logs
Run: View logs in Render dashboard
Set: DEBUG=True temporarily to see detailed errors
```

### Frontend Issues

**Issue: API calls failing**
```
Solution: Verify REACT_APP_BACKEND_URL is correct
Check: Backend is deployed and running
Test: curl https://your-backend.onrender.com/api/employees/
```

**Issue: Build failing**
```
Solution: Check package.json dependencies
Run: yarn install locally to test
```

**Issue: Blank page after deployment**
```
Solution: Check browser console for errors
Verify: All environment variables are set
```

---

## \ud83d\udce6 Custom Domain Setup

### Vercel Custom Domain

1. Go to project settings
2. Click **Domains**
3. Add your domain
4. Update DNS records as instructed
5. Wait for propagation (5-10 minutes)

### Render Custom Domain

1. Go to service settings
2. Click **Custom Domains**
3. Add your domain
4. Update DNS:
   - Type: `CNAME`
   - Name: `api` (or your choice)
   - Value: `<your-app>.onrender.com`

---

## \ud83d\udd12 Production Security

### Django Security Settings

Update `settings.py` for production:

```python
# In production
DEBUG = False
ALLOWED_HOSTS = ['your-backend.onrender.com', 'your-domain.com']

# Security headers
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

### Environment Variables

**Never commit:**
- `.env` files
- Database credentials
- Secret keys

**Add to `.gitignore`:**
```
.env
*.sqlite3
__pycache__/
*.pyc
db.sqlite3
```

---

## \ud83d\udcca Monitoring

### Render Monitoring

- View logs in real-time
- Set up alerts for downtime
- Monitor database usage
- Track response times

### Vercel Monitoring

- Analytics dashboard
- Error tracking
- Performance metrics
- Build logs

---

## \ud83d\udd04 Continuous Deployment

Both Render and Vercel support automatic deployments:

1. **Push to Git** → Automatic deployment
2. **Rollback** available in dashboard
3. **Preview deployments** for pull requests

---

## \ud83d\udcb0 Cost Estimation

### Free Tier (Render + Vercel)
- **Render Free**: 750 hours/month
- **Vercel Free**: Unlimited deployments
- **Total**: $0/month
- **Limitations**: 
  - Backend sleeps after 15 min inactivity
  - Limited database storage (1GB)

### Starter Plan
- **Render Starter**: $7/month (backend)
- **Render PostgreSQL**: $7/month
- **Vercel Pro**: $20/month (optional)
- **Total**: $14-34/month
- **Benefits**:
  - No sleep
  - Better performance
  - More storage

---

## \ud83d\ude80 Performance Optimization

### Backend
```python
# settings.py
CONN_MAX_AGE = 600  # Database connection pooling

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    }
}
```

### Frontend
- Enable compression in Vercel
- Use code splitting
- Optimize images
- Enable CDN

---

## \ud83d\udcdd Post-Deployment Checklist

- [ ] Test all API endpoints
- [ ] Test employee CRUD operations
- [ ] Test attendance marking
- [ ] Test date filtering
- [ ] Verify dashboard statistics
- [ ] Test responsive design on mobile
- [ ] Check error handling
- [ ] Verify data persistence
- [ ] Test with multiple employees
- [ ] Load testing (optional)

---

## \ud83d\udce7 Support Resources

- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **Django Deployment**: https://docs.djangoproject.com/en/5.0/howto/deployment/
- **React Deployment**: https://create-react-app.dev/docs/deployment/

---

## \ud83c\udf89 You're Live!

Your HRMS Lite is now deployed and ready for production use!

**Share your deployed app:**
- Frontend: `https://your-app.vercel.app`
- Backend API: `https://hrms-backend.onrender.com/api/`

---

**Need help?** Check the troubleshooting section or review the logs in your deployment platform.
