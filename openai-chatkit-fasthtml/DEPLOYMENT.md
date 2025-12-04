# Guides de Déploiement

## Déploiement sur Heroku

### Prérequis
- Compte Heroku
- Heroku CLI installé
- Git

### Steps

1. **Créer l'application Heroku**
```bash
heroku create your-app-name
```

2. **Configurer les variables d'environnement**
```bash
heroku config:set OPENAI_API_KEY=sk_...
heroku config:set CHATKIT_WORKFLOW_ID=wf_...
heroku config:set DEBUG=False
```

3. **Déployer**
```bash
git push heroku main
```

4. **Vérifier les logs**
```bash
heroku logs -t
```

## Déploiement avec Docker

### Construire et exécuter localement

```bash
# Construire l'image
docker build -t chatkit-fasthtml:latest .

# Exécuter le container
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=sk_... \
  -e CHATKIT_WORKFLOW_ID=wf_... \
  chatkit-fasthtml:latest

# Accéder à http://localhost:8000
```

### Utiliser docker-compose

```bash
# Configurer .env
cp .env.example .env
# Éditer .env avec vos credentials

# Démarrer les services
docker-compose up

# Arrêter
docker-compose down
```

## Déploiement sur Railway

### Prérequis
- Compte Railway
- Railway CLI

### Steps

1. **Lier le projet**
```bash
railway login
railway init
```

2. **Configurer les variables**
```bash
railway variables set OPENAI_API_KEY=sk_...
railway variables set CHATKIT_WORKFLOW_ID=wf_...
```

3. **Déployer**
```bash
railway up
```

## Déploiement sur Render

### Prérequis
- Compte Render
- GitHub repository

### Steps

1. **Connecter votre repo GitHub**
   - Aller sur [render.com](https://render.com)
   - Créer un "New Web Service"
   - Sélectionner votre repository

2. **Configurer**
   - Environment: Python 3.11
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app`

3. **Ajouter les variables d'environnement**
   - OPENAI_API_KEY
   - CHATKIT_WORKFLOW_ID
   - DEBUG=False

4. **Déployer**
   - Cliquer "Create Web Service"

## Déploiement sur Fly.io

### Prérequis
- Compte Fly.io
- Fly CLI installé

### Steps

1. **Initialiser l'application**
```bash
fly launch
```

2. **Configurer les secrets**
```bash
fly secrets set OPENAI_API_KEY=sk_...
fly secrets set CHATKIT_WORKFLOW_ID=wf_...
```

3. **Déployer**
```bash
fly deploy
```

4. **Vérifier le statut**
```bash
fly status
fly logs
```

## Déploiement sur Google Cloud Run

### Prérequis
- Compte Google Cloud
- `gcloud` CLI installé

### Steps

1. **Construire et pousser l'image**
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/chatkit-fasthtml
```

2. **Déployer le service**
```bash
gcloud run deploy chatkit-fasthtml \
  --image gcr.io/PROJECT_ID/chatkit-fasthtml \
  --platform managed \
  --region us-central1 \
  --set-env-vars OPENAI_API_KEY=sk_...,CHATKIT_WORKFLOW_ID=wf_...
```

3. **Accéder à l'URL du service**
```bash
gcloud run services describe chatkit-fasthtml --platform managed --region us-central1
```

## Déploiement sur AWS Lambda + API Gateway

### Utiliser Chalice

```bash
# Installer Chalice
pip install chalice

# Créer et configurer
chalice new chatkit-fasthtml
# Ajouter FastHTML app à chalice app.py

# Déployer
chalice deploy
```

## Déploiement sur PythonAnywhere

### Steps

1. **Uploader le code**
   - Web file uploader ou Git

2. **Créer une web app Python**
   - Choisir FastAPI/Uvicorn

3. **Configurer le fichier WSGI**
```python
from app.main import app
application = app
```

4. **Ajouter variables d'environnement**
   - Web > Environment variables

## Variables d'environnement essentielles

| Variable | Obligatoire | Description |
|----------|---|---|
| OPENAI_API_KEY | ✅ | Clé API OpenAI |
| CHATKIT_WORKFLOW_ID | ✅ | ID du workflow ChatKit |
| DEBUG | ❌ | Mode debug (True/False) |
| HOST | ❌ | Host (par défaut: 0.0.0.0) |
| PORT | ❌ | Port (par défaut: 8000) |
| CHATKIT_API_BASE | ❌ | Base URL de l'API ChatKit |

## Monitoring et Logging

### Heroku
```bash
# Logs en temps réel
heroku logs -t

# Accéder à Dyno logs
heroku logs --dyno=web --num=100
```

### Docker
```bash
# Logs du container
docker logs -f <container_id>

# Logs de docker-compose
docker-compose logs -f app
```

### Sentry (pour error tracking)

1. **Installer Sentry**
```bash
pip install sentry-sdk
```

2. **Ajouter à app/main.py**
```python
import sentry_sdk

sentry_sdk.init(
    dsn="https://examplePublicKey@o0.ingest.sentry.io/0",
    traces_sample_rate=1.0
)
```

## Health Checks

Tous les déploiements doivent configurer un health check:

```bash
GET /api/health
```

Response:
```json
{
  "status": "healthy",
  "workflow_id": "wf_..."
}
```

## Scaling

### Heroku
```bash
# Scale dynos
heroku dyno:resize standard-2x
heroku ps:scale web=2
```

### Docker Compose
```bash
# Scale services
docker-compose up --scale app=3
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chatkit-fasthtml
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: app
        image: chatkit-fasthtml:latest
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: chatkit-secrets
              key: openai-api-key
```

## Performance Tips

1. **Ajouter Redis pour les sessions**
```python
# app/session.py
import redis
cache = redis.Redis()
```

2. **Utiliser un CDN pour les assets statiques**
```python
# app/main.py
# Configurer CloudFront ou CloudFlare
```

3. **Ajouter Gzip compression**
```python
from fasthtml.middleware import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

## Troubleshooting

### Port déjà utilisé
```bash
# Trouver le processus
lsof -i :8000
# Tuer
kill -9 <PID>
```

### Variables d'environnement non chargées
```bash
# Vérifier les variables
echo $OPENAI_API_KEY

# Pour Heroku
heroku config
```

### Performance lente
```bash
# Augmenter les workers
gunicorn -w 8 -k uvicorn.workers.UvicornWorker app.main:app

# En Docker
docker run -e GUNICORN_CMD_ARGS="--workers=4" ...
```

## Ressources

- [Heroku Python Deployment](https://devcenter.heroku.com/articles/python-support)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Railway Docs](https://railway.app/docs)
- [Render Deployment](https://render.com/docs/deploy-fastapi)
- [Fly.io Deployment](https://fly.io/docs/)
