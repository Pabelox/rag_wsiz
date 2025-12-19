import math
import ollama
import json
import os
from django.conf import settings

# Plik bazy wektorowej
DB_PATH = os.path.join(settings.BASE_DIR, 'vector_db.json')


def get_embedding(text):
    """
    Do wektorów używamy specjalistycznego modelu.
    Upewnij się, że masz go pobranego: `ollama pull nomic-embed-text`
    """
    response = ollama.embeddings(model="nomic-embed-text", prompt=text)
    return response["embedding"]


def cosine_similarity(v1, v2):
    """Twój własny algorytm liczący podobieństwo."""
    dot_product = sum(a * b for a, b in zip(v1, v2))
    norm_a = math.sqrt(sum(x ** 2 for x in v1))
    norm_b = math.sqrt(sum(x ** 2 for x in v2))

    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def search_knowledge_base(query, limit=3):
    """Wyszukiwarka."""
    if not os.path.exists(DB_PATH):
        return []

    # Zamieniamy pytanie użytkownika na wektor
    query_vec = get_embedding(query)

    with open(DB_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    results = []
    for item in data:
        score = cosine_similarity(query_vec, item['vector'])
        results.append({'content': item['content'], 'score': score})

    # Sortujemy od najlepszego wyniku
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:limit]