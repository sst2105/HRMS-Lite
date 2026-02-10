# 🚀 DEPLOYMENT GUIDE - HRMS Lite

## Quick Deployment Options

### Option 1: Railway (Recommended - Easiest)

#### Backend + Database
1. Go to [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Add PostgreSQL database:
   - Click "New" → "Database" → "PostgreSQL"
5. Configure backend service:
   - Root directory: `/backend`
   - Add environment variables:
     ```
     DATABASE_URL: ${{Postgres.DATABASE_URL}}
     CORS_ORIGINS: https://your-frontend-url.vercel.app
     ENVIRONMENT: production
     ```
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### Frontend (Vercel)
1. Go to [Vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Configure:
   - Framework Preset: Vite
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
4. Add environment variable:
   ```
   VITE_API_URL: https://your-backend.railway.app
   ```

### Option 2: Render

#### Database
1. Create PostgreSQL database on Render
2. Note the Internal Database URL

#### Backend
1. New Web Service
2. Connect GitHub repo
3. Settings:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Environment Variables:
   ```
   DATABASE_URL: [your-postgres-internal-url]
   CORS_ORIGINS: https://your-frontend.onrender.com
   ENVIRONMENT: production
   ```

#### Frontend
1. New Static Site
2. Settings:
   - Root Directory: `frontend`
   - Build Command: `npm install && npm run build`
   - Publish Directory: `dist`
3. Environment Variable:
   ```
   VITE_API_URL: https://your-backend.onrender.com
   ```

### Option 3: Docker on VPS (DigitalOcean, AWS, etc.)

1. **SSH into your server**
```bash
ssh user@your-server-ip
```

2. **Install Docker and Docker Compose**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

3. **Clone repository**
```bash
git clone <your-repo-url>
cd hrms-lite
```

4. **Set environment variables**
```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
# Edit both .env files
```

5. **Deploy**
```bash
docker-compose up -d --build
```

6. **Set up reverse proxy (Nginx)**
```bash
sudo apt install nginx
sudo nano /etc/nginx/sites-available/hrms
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

7. **Enable and restart**
```bash
sudo ln -s /etc/nginx/sites-available/hrms /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Environment Variables Checklist

### Backend (.env)
- ✅ DATABASE_URL
- ✅ CORS_ORIGINS (include your frontend URL)
- ✅ ENVIRONMENT=production

### Frontend (.env)
- ✅ VITE_API_URL (your backend URL)

## Post-Deployment Checklist

- [ ] Backend health check: `https://your-backend/health`
- [ ] Frontend loads: `https://your-frontend`
- [ ] API docs accessible: `https://your-backend/api/docs`
- [ ] Can create employee
- [ ] Can mark attendance
- [ ] Dashboard shows correct stats
- [ ] CORS is working (no console errors)

## Troubleshooting

### CORS Errors
- Add frontend URL to backend `CORS_ORIGINS`
- Include protocol (https://)
- No trailing slash

### Database Connection Errors
- Check DATABASE_URL format
- Ensure database is running
- Check firewall rules

### Build Failures
- Check Node version (20+)
- Check Python version (3.11+)
- Clear cache and rebuild

### API Not Responding
- Check backend logs
- Verify PORT environment variable
- Check health endpoint

## Monitoring

### Logs
**Railway**: Built-in logs viewer
**Render**: Logs tab in dashboard
**VPS**: 
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Database Backups
**Railway**: Automatic backups
**Render**: Automatic backups on paid plans
**VPS**: Set up pg_dump cron job

## Scaling Considerations

### Database
- Connection pooling (already configured)
- Add read replicas for heavy read workloads
- Implement caching (Redis)

### Backend
- Horizontal scaling with load balancer
- Add rate limiting
- Implement CDN for static assets

### Frontend
- CDN (Vercel/Cloudflare)
- Asset optimization
- Code splitting (already implemented)

## Security Hardening

1. **Use HTTPS** - Get free SSL with Let's Encrypt
2. **Environment Variables** - Never commit .env files
3. **Database** - Use strong passwords, enable SSL
4. **API** - Add rate limiting, implement authentication
5. **Headers** - Security headers already configured

## Estimated Costs (Monthly)

### Free Tier
- Railway: 500 hours ($0)
- Vercel: Unlimited hobby projects ($0)
- Render: Free tier available ($0)

### Production (Low Traffic)
- Railway: ~$5-10
- Render: ~$7-15
- VPS: ~$5-12 (DigitalOcean droplet)

## Need Help?

Check deployment logs first:
- Railway: View logs in dashboard
- Render: Logs tab
- VPS: `docker-compose logs`

Common issues are usually:
1. Environment variables not set
2. CORS misconfiguration
3. Database connection string wrong
4. Build command incorrect

## Success! 🎉

Your HRMS Lite application is now live and production-ready!

Next steps:
- Set up monitoring (Sentry, LogRocket)
- Configure backups
- Set up CI/CD pipeline
- Add custom domain
