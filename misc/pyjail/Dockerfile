FROM python:3.11-slim

RUN apt update && apt install -y socat && rm -rf /var/lib/apt/lists/*

RUN useradd -m ctfuser
USER ctfuser

WORKDIR /home/ctfuser

COPY app.py .
COPY flag.txt .

EXPOSE 1337

CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"python3 app.py",pty,stderr,setsid,sigint,sane