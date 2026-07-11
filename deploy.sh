#!/bin/bash
# deploy.sh – Fit.Physio.Katrin → Hetzner via SSH
# Aufruf: ./deploy.sh

set -e

SERVER="root@138.199.193.193"
REMOTE_DIR="/opt/fitphysiokatrin"
IMAGE="fitphysiokatrin"
CONTAINER="fitphysiokatrin"

echo "🚀 Deploy Fit.Physio.Katrin..."

# 1. Dateien auf Server synchronisieren
echo "📦 Dateien übertragen..."
rsync -az --delete \
  --exclude='.git' \
  --exclude='deploy.sh' \
  --exclude='ColorCodes.jpg' \
  --exclude='node_modules' \
  . "$SERVER:$REMOTE_DIR/"

# 2. Docker Image auf Server bauen
echo "🔨 Docker Image bauen..."
ssh "$SERVER" "cd $REMOTE_DIR && docker build -t $IMAGE ."

# 3. Alten Container stoppen & entfernen
echo "🔄 Container aktualisieren..."
ssh "$SERVER" "docker stop $CONTAINER 2>/dev/null || true && docker rm $CONTAINER 2>/dev/null || true"

# 4. Neuen Container starten (mit Traefik-Labels für Coolify)
echo "▶️  Container starten..."
RUN_CMD="docker run -d \
  --name '$CONTAINER' \
  --restart unless-stopped \
  --network coolify \
  --label 'traefik.enable=true' \
  --label 'traefik.http.routers.${CONTAINER}-http.entryPoints=http' \
  --label 'traefik.http.routers.${CONTAINER}-http.rule=Host(\`fitphysiokatrin.com\`)' \
  --label 'traefik.http.routers.${CONTAINER}-http.middlewares=${CONTAINER}-https-redirect' \
  --label 'traefik.http.middlewares.${CONTAINER}-https-redirect.redirectscheme.scheme=https' \
  --label 'traefik.http.middlewares.${CONTAINER}-https-redirect.redirectscheme.permanent=true' \
  --label 'traefik.http.routers.${CONTAINER}-https.entryPoints=https' \
  --label 'traefik.http.routers.${CONTAINER}-https.rule=Host(\`fitphysiokatrin.com\`)' \
  --label 'traefik.http.routers.${CONTAINER}-https.tls=true' \
  --label 'traefik.http.routers.${CONTAINER}-https.tls.certresolver=letsencrypt' \
  --label 'traefik.http.services.${CONTAINER}.loadbalancer.server.port=80' \
  '$IMAGE'"
ssh "$SERVER" "$RUN_CMD"

echo "✅ Deployed! https://fitphysiokatrin.com/6am"
