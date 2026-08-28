FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir \
      "aiogram>=3.30,<4" \
      "SQLAlchemy>=2.0,<3" \
      "asyncpg>=0.30,<1" \
      "python-dotenv>=1.0,<2" \
      "aiohttp>=3.10,<4" \
      "tzdata>=2025.2" \
    && useradd --create-home --uid 10001 appuser \
    && install -d -o appuser -g appuser /app

COPY runtime.py /usr/local/bin/izmail-runtime.py

WORKDIR /app
USER appuser

EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import os, urllib.request; urllib.request.urlopen('http://127.0.0.1:' + os.getenv('PORT', '8080') + '/health', timeout=3)"

CMD ["python", "/usr/local/bin/izmail-runtime.py"]
