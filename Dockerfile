FROM nginx:alpine

# Statische Dateien kopieren
COPY . /usr/share/nginx/html

# Custom nginx-Config einbinden
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Nicht benötigte Dateien aus dem Image entfernen
RUN rm -f /usr/share/nginx/html/Dockerfile \
           /usr/share/nginx/html/nginx.conf \
           /usr/share/nginx/html/.htaccess

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
