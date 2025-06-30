FROM python:3.11-slim

WORKDIR /app

COPY req.txt .
RUN pip install --no-cache-dir -r req.txt

COPY . .

EXPOSE 8501

# ✅ Fixed: Added --server.address=0.0.0.0
CMD ["streamlit", "run", "chat.py", "--server.port=8501", "--server.address=0.0.0.0"]
