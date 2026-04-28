import time
import requests
import feedparser
import os
import csv

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def buscar_vagas():
    url = "https://www.indeed.com/rss?q=remote+customer+support&l="
    feed = feedparser.parse(url)

    vagas = []
    for entry in feed.entries:
        vagas.append({
            "titulo": entry.title,
            "descricao": entry.summary,
            "link": entry.link
        })
    return vagas

def analisar_vaga(descricao):
    prompt = f"""
You are a hiring expert.

Analyze this job and return JSON:

Criteria:
- Must be remote
- Entry level or junior
- No strict country restriction
- Avoid scams

Return:
{{
  "approved": true/false,
  "score": 0-10,
  "reason": "short explanation"
}}

JOB:
{descricao}
"""

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    return response.json()

def salvar_vaga(vaga):
    with open("vagas.csv", "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([vaga["titulo"], vaga["link"]])

def executar():
    print("🔍 Buscando vagas...")

    vagas = buscar_vagas()

    print(f"📊 {len(vagas)} vagas encontradas")

    if len(vagas) == 0:
        print("❌ Nenhuma vaga encontrada")
        return

    for vaga in vagas:
        print("📌 Vaga:", vaga["titulo"])
        print("🔗 Link:", vaga["link"])
        print("-" * 40)
if __name__ == "__main__":
    while True:
        executar()
        print("Aguardando 15 minutos...")
        time.sleep(900)
