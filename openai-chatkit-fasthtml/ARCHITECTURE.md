# Architecture de ChatKit FastHTML

## Structure du projet

```
openai-chatkit-fasthtml/
├── app/                      # Code source principal
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastHTML app et routes HTML
│   ├── routes.py            # Handlers API
│   ├── config.py            # Configuration
│   ├── session.py           # Gestion de session
│   └── static/              # Assets statiques
│       ├── styles.css       # Styles CSS
│       └── chatkit.js       # Initialisation ChatKit
├── tests/                   # Tests unitaires
│   ├── test_config.py
│   └── test_session.py
├── .env.example             # Template variables d'environnement
├── requirements.txt         # Dépendances
├── pyproject.toml          # Configuration projet
├── Makefile                # Commandes développement
└── README.md               # Documentation
```

## Flux de requête

```
Client Browser
    ↓
GET / (FastHTML)
    ↓
app/main.py::home()
    ↓
HTML avec chatkit.js
    ↓
Script charge https://chatkit.openai.com/assets/chatkit.js
    ↓
app/static/chatkit.js::initChatKit()
    ↓
POST /api/create-session
    ↓
app/routes.py::handle_create_session()
    ↓
session.py::create_chatkit_session()
    ↓
OpenAI ChatKit API
    ↓
Returns: {token, session_id, expires_at}
    ↓
Retour au navigateur + Set-Cookie header
    ↓
openai-chatkit web component initializado
```

## Modules principaux

### 1. **config.py** - Configuration

Gère toute la configuration centralisée:

```python
class ChatKitConfig:
    """Configuration OpenAI ChatKit"""
    WORKFLOW_ID: str          # ID du workflow (de .env)
    API_BASE: str            # Base URL de l'API
    OPENAI_API_KEY: str      # Clé API OpenAI
    STARTER_PROMPTS: list    # Prompts suggérés
    PLACEHOLDER_INPUT: str   # Placeholder input
    GREETING: str            # Message de bienvenue

class AppConfig:
    """Configuration application"""
    HOST: str                # Host pour uvicorn
    PORT: int                # Port
    DEBUG: bool              # Mode debug
```

### 2. **session.py** - Gestion de session

Toute la logique concernant les sessions ChatKit:

```python
async def create_chatkit_session(
    api_key: str,
    workflow_id: str,
    user_id: Optional[str] = None,
    file_upload_enabled: bool = False,
    api_base: str = "https://api.openai.com",
) -> dict[str, Any]
    """Crée une session ChatKit"""

async def create_or_get_session_cookie(
    request_headers: dict[str, str],
) -> tuple[str, Optional[str]]
    """Gère les cookies de session"""
```

### 3. **routes.py** - Endpoints API

Handlers pour les requêtes HTTP:

```python
async def handle_create_session(request: Request) -> Response
    """POST /api/create-session - Crée une session"""

async def handle_health_check(request: Request) -> Response
    """GET /api/health - Vérifie la santé de l'app"""

async def handle_config(request: Request) -> Response
    """GET /api/config - Retourne la configuration"""
```

### 4. **main.py** - FastHTML App

Application principale et routes:

```python
app = FastHTML(debug=DEBUG, title="ChatKit Starter")

@app.get("/")
def home(request: Request) -> Html
    """Page d'accueil avec ChatKit"""

@app.post("/api/create-session")
async def create_session(request: Request) -> Response
    """Route API de création de session"""
```

### 5. **static/chatkit.js** - Client-side

Initialisation du composant ChatKit côté client:

```javascript
async function initChatKit()
    1. Attend que le web component soit chargé
    2. Appelle POST /api/create-session
    3. Initialise le composant openai-chatkit
    4. Gère les erreurs avec retry
```

## Gestion des erreurs

### Backend (Python)

```python
try:
    session = await create_chatkit_session(...)
except ValueError as e:
    return json_resp({"error": str(e)}, status_code=500)
except httpx.HTTPError as e:
    # Extrait le message d'erreur upstream
    error = extract_upstream_error(error_data)
    return json_resp({"error": error}, status_code=500)
```

### Frontend (JavaScript)

```javascript
try {
    const session = await fetch('/api/create-session', {...})
    if (!session.ok) throw new Error(...)
} catch (error) {
    showError(`Error: ${error.message}`)
    // Affiche retry button
}
```

## Sécurité

### Cookies
- **HttpOnly**: Pas accessible via JavaScript (XSS protection)
- **SameSite=Lax**: CSRF protection
- **Secure**: HTTPS only en production
- **Max-Age**: 30 jours

### Variables d'environnement
- **OPENAI_API_KEY**: Jamais exposée au client
- **CHATKIT_WORKFLOW_ID**: Safe pour le client (décorée en données publiques)

### Validation
- Type validation via Pydantic
- Validation d'entrée avec `CreateSessionRequest`
- Extraction sécurisée des erreurs (pas d'exposition d'infos sensibles)

## Tests

### Configuration

```python
# tests/test_config.py
def test_theme_config():
    light = ThemeConfig.get_theme_config(ColorScheme.LIGHT)
    assert light["color"]["accent"]["primary"] == "#0f172a"
```

### Session

```python
# tests/test_session.py
@pytest.mark.asyncio
async def test_create_chatkit_session():
    result = await create_chatkit_session(
        api_key="test-key",
        workflow_id="wf_test",
    )
    assert result["token"]
```

## Variables d'environnement

```bash
# Obligatoires
OPENAI_API_KEY=sk_...              # Clé API OpenAI
CHATKIT_WORKFLOW_ID=wf_...         # ID du workflow

# Optionnels
CHATKIT_API_BASE=https://api.openai.com  # Base URL custom
HOST=0.0.0.0                       # Host serveur
PORT=8000                          # Port serveur
DEBUG=True                         # Mode debug
```

## Développement

### Commandes

```bash
# Installation
make install
make install-dev

# Développement
make dev              # Démarre le serveur avec hot-reload

# Utilité
make test            # Lance les tests
make lint            # Lint le code
make format          # Formate le code
make clean           # Nettoie les artefacts
```

### Hot Reload

FastHTML inclut le hot-reload automatiquement en mode debug. Les modifications aux fichiers Python relanceront le serveur.

### Logging

```python
import logging
logger = logging.getLogger(__name__)

# Automatiquement configuré avec:
# - Level: DEBUG en debug, INFO en production
# - Format: timestamp - name - level - message
```

## Performance

### Optimisations

1. **ASGI Async**: Toutes les routes IO sont asynchrones
2. **Type Hints**: Validation dynamique avec Pydantic
3. **Static Files**: Servis directement par FastHTML
4. **Session Caching**: Réutilisation des sessions existantes

### Métriques

- Startup: < 100ms
- Request (HTML): < 50ms
- Request (API): < 200ms (dépend d'OpenAI)
- Memory: < 50MB

## Déploiement

### Heroku

```bash
git push heroku main
```

`.github/workflows/deploy.yml`:
```yaml
on: [push]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: python app/main.py
```

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app"]
```

### Environment Variables

En production, définir:
```bash
OPENAI_API_KEY=<votre clé>
CHATKIT_WORKFLOW_ID=<votre id>
DEBUG=False
HOST=0.0.0.0
PORT=8000
```

## Extensibilité

### Ajouter une nouvelle route

```python
# app/routes.py
async def handle_custom_endpoint(request: Request) -> Response:
    return json_resp({"data": "value"})

# app/main.py
@app.post("/api/custom")
async def custom_endpoint(request: Request):
    return await handle_custom_endpoint(request)
```

### Ajouter une nouvelle page HTML

```python
# app/main.py
@app.get("/about")
def about():
    return Html(
        Head(Title("À propos")),
        Body(
            H1("À propos"),
            P("Contenu..."),
        ),
    )
```

### Ajouter une dépendance

```bash
pip install new-package
pip freeze > requirements.txt
```

## Troubleshooting

### Port déjà utilisé
```bash
# Changer le port
PORT=3000 python app/main.py

# Ou tuer le processus
lsof -i :8000
kill -9 <PID>
```

### Erreur CORS
FastHTML gère les CORS automatiquement pour les routes API.

### Session non persistée
Vérifier que les cookies ne sont pas bloqués par le navigateur.

## Ressources

- [FastHTML Docs](https://docs.fast.ai/)
- [Uvicorn](https://www.uvicorn.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [OpenAI ChatKit](https://platform.openai.com/docs/concepts/chatkit)
