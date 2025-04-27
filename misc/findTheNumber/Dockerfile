FROM python:3.11-slim

RUN apt update && apt install -y socat && rm -rf /var/lib/apt/lists/*

RUN useradd -m ctfuser
USER ctfuser

WORKDIR /home/ctfuser

COPY binary.py .

EXPOSE 1337

CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"timeout 10s python3 binary.py",pty,stderr,setsid,sigint,sane
