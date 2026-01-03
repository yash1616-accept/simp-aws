# Base image
FROM python:3.12-slim

# ------------------------
# Backend
# ------------------------
WORKDIR /app/backend
COPY backend/ ./ 
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000

# ------------------------
# Frontend
# ------------------------
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN apt-get update && apt-get install -y nodejs npm
RUN npm install
COPY frontend/ ./
EXPOSE 3000

# ------------------------
# Start both services
# ------------------------
CMD ["sh", "-c", "cd /app/backend && python app.py & cd /app/frontend && node server.js"]
