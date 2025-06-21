# ------------------------------------------------------------------
#  Dockerfile – Python 3.11.6 + French UTF-8 locale + Gunicorn
# ------------------------------------------------------------------
FROM python:3.11.6-slim AS runtime

# 1. Base environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000 \
    LANG=fr_FR.UTF-8 \
    LANGUAGE=fr_FR:fr \
    LC_ALL=fr_FR.UTF-8 \
    PORT=8000

WORKDIR /app

# 2. OS packages:
#    - build-essential gcc       : only needed if any wheel must be compiled
#    - locales                   : to generate fr_FR.UTF-8
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential gcc \
        locales \
    && \
    # --- generate the French UTF-8 locale --------------------------
    echo "fr_FR.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen && \
    # ---------------------------------------------------------------
    # clean up apt cache to keep the image small
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 3. Install Python dependencies first for better cache utilisation
COPY requirements.txt .
RUN pip install -r requirements.txt

# 4. Copy the rest of your source code
COPY . .

# 5. Make the port visible for -p/-P mapping
EXPOSE 8000

# 6. Start the web app (same command as in your Procfile)
CMD gunicorn --bind 0.0.0.0:$PORT app:app