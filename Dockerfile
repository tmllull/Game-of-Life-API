FROM python:3.13-slim-bookworm

WORKDIR /app

# Increase performance
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ARG WORKERS=1
ARG PORT=5000
ENV WORKERS=${WORKERS}
ENV PORT=${PORT}

# CMD ["uvicorn", "app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "5000"]
# CMD ["gunicorn", "app:app", "-k", "uvicorn.workers.UvicornWorker", "--workers", "$WORKERS", "--bind", "0.0.0.0:$PORT"]
CMD ["sh", "-c", "gunicorn app:app -k uvicorn.workers.UvicornWorker --workers $WORKERS --bind 0.0.0.0:$PORT"]
