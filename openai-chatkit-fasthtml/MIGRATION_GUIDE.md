# Migration Guide: Next.js to FastHTML

Ce document explique comment la version Next.js/TypeScript a été refactorisée en Python/FastHTML.

## Vue d'ensemble des changements

### Architecture

**Next.js (JS/TS)**
- Frontend React avec composants réutilisables
- API routes serverless (`app/api/`)
- Build et compilation TypeScript
- Configuration via `next.config.ts`

**FastHTML (Python)**
- Framework web léger avec HTML natif
- Routes asynchrones via `@app.route()`
- Pas de compilation ni de build complexe
- Configuration via `.env` et `config.py`

## Mappages fichier par fichier

### Configuration

| Next.js | FastHTML | Description |
|---------|----------|-------------|
| `.env.local` | `.env` | Variables d'environnement |
| `lib/config.ts` | `app/config.py` | Configuration de l'application |
| `next.config.ts` | `pyproject.toml` | Configuration du projet |

### Routes et API

| Next.js | FastHTML | Description |
|---------|----------|-------------|
| `app/api/create-session/route.ts` | `app/routes.py` → `@app.post("/api/create-session")` | Endpoint de création de session |
| `app/page.tsx` | `app/main.py` → `@app.get("/")` | Page d'accueil |

### Composants

| Next.js | FastHTML | Description |
|---------|----------|-------------|
| `components/ChatKitPanel.tsx` | `app/static/chatkit.js` | Initialisation ChatKit (JS natif) |
| `components/ErrorOverlay.tsx` | HTML inline dans `app/main.py` | Overlay d'erreur |
| `app/layout.tsx` | HTML dans `app/main.py` | Layout principal |

### Styles

| Next.js | FastHTML |
|---------|----------|
| `app/globals.css` | `app/static/styles.css` |

## Améliorations principales

### 1. **Moins de dépendances**
```
Next.js: next, react, react-dom, @openai/chatkit-react + devDependencies
FastHTML: fasthtml, python-dotenv, httpx, uvicorn, pydantic
```

### 2. **Pas de système de build**
- Next.js requiert: `npm run build`
- FastHTML: exécution directe `python app/main.py`

### 3. **Type safety en Python**
```python
# config.py
class ChatKitConfig:
    WORKFLOW_ID: str = os.getenv("CHATKIT_WORKFLOW_ID", "").strip()
    API_BASE: str = os.getenv("CHATKIT_API_BASE", "https://api.openai.com")
```

### 4. **Routes asynchrones simples**
```python
# app/routes.py
async def handle_create_session(request: Request) -> Response:
    # Logique de création de session
    return json_resp(response_data, status_code=200)
```

### 5. **HTML déclaratif**
```python
# app/main.py
Html(
    Head(...),
    Body(
        Div(cls="header", children=[...]),
        Div(cls="main", children=[...]),
        Script(src="..."),
    ),
)
```

## Installation et exécution

### Development

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Lancer le serveur
make dev
# ou
python app/main.py
```

### Production

```bash
pip install -r requirements.txt
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

## Gestion de session

### Next.js
- Cookies gérés avec `Set-Cookie` headers
- Session stockée en mémoire côté client

### FastHTML
- Cookies gérés identiquement via `Response.headers["Set-Cookie"]`
- Cookies HttpOnly pour la sécurité
- Expiration 30 jours

## Gestion des erreurs

### Next.js
```tsx
const [errors, setErrors] = useState<ErrorState>(...)
// État React complexe
```

### FastHTML
```python
# Gestion d'erreur simple dans les routes
if not is_valid:
    return json_resp({"error": error_msg}, status_code=400)
```

## Performance

### FastHTML

1. **Startup time**: Immédiat (pas de compilation)
2. **Runtime**: ASGI async native
3. **Bundle size**: Aucun bundle (JS minimum)
4. **Memory**: Minimal comparé à Node.js

## Points de migration

### Si vous aviez du state React

```typescript
// Next.js
const [value, setValue] = useState(initialValue)
```

→ **FastHTML** : Utiliser HTMX ou JavaScript natif pour l'interactivité

```javascript
// JavaScript natif
let value = initialValue
// ou via HTMX pour les requêtes
```

### Si vous aviez des middleware

```typescript
// Next.js middleware
export function middleware(request: NextRequest) {
  // ...
}
```

→ **FastHTML** : Utiliser des intercepteurs ou des décorateurs FastHTML

### Si vous aviez des Server Components

```typescript
// Next.js Server Component
async function getData() { }
```

→ **FastHTML** : Routes asynchrones FastHTML

```python
@app.post("/api/data")
async def get_data():
    return json_resp(data)
```

## Testing

### Next.js
```bash
npm test
```

### FastHTML
```bash
make test
# ou
pytest -v
```

## Développement continu

### Hot reload
- **Next.js**: Intégré
- **FastHTML**: `--reload` flag dans uvicorn

```bash
python app/main.py  # Auto-reload enabled in debug mode
```

## Déploiement

### Options pour FastHTML

**Heroku**
```bash
git push heroku main
```

**Docker**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app .
CMD ["python", "app/main.py"]
```

**Vercel/Edge Runtime**
FastHTML supporte les déploiements Edge avec des adaptateurs

**Railway, Render, Fly.io**
Supportés nativement avec Python

## Ressources

- [FastHTML Documentation](https://docs.fast.ai/)
- [ChatKit API Documentation](https://platform.openai.com/docs/api-reference/chatkit)
- [ASGI Servers](https://asgi.readthedocs.io/)
