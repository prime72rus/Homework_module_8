FROM nginx:latest

RUN mkdir -p /app/staticfiles && chmod -R 755 /app/staticfiles
RUN mkdir -p /app/media && chmod -R 755 /app/media
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80