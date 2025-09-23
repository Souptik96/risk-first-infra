FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY req.py model.py ledger.py app.py /app/
COPY ../../state /app/state
COPY ../../features /app/features
COPY ../../business /app/business
EXPOSE 8000
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]
