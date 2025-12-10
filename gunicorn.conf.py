# gunicorn.conf.py
# Configuration pour Gunicorn sur Render

# Temps d'attente maximum pour une requête (en secondes)
timeout = 120

# Garder la connexion alive
keepalive = 5

# Type de worker (sync est le plus simple)
worker_class = 'sync'

# Nombre de workers (adapté au plan free de Render)
workers = 2

# Nombre maximum de requêtes par worker avant redémarrage
max_requests = 1000
max_requests_jitter = 50

# Journalisation
accesslog = '-'  # Log vers stdout
errorlog = '-'   # Log d'erreur vers stdout
loglevel = 'info'

# Redémarrer les workers qui prennent trop de temps
graceful_timeout = 30