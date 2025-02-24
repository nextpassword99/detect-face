FROM python:3.10
WORKDIR /detect_face
COPY requirements.txt .
RUN apt update && apt install cmake -y \
    && pip install -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* 

COPY . .
EXPOSE 6743