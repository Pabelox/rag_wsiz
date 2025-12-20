from django.core.management.base import BaseCommand
from django.conf import settings
import os
import json
from RAG.chat.rag_utils import get_embedding


class Command(BaseCommand):
    help = 'Tworzy bazę wektorową z pliku base.txt'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'base.txt')
        output_path = os.path.join(settings.BASE_DIR, 'vector_db.json')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR('Brak pliku base.txt!'))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        # Inteligentne cięcie po pustych liniach (akapitach)
        chunks = [c.strip() for c in text.split('\n\n') if c.strip()]

        database = []
        self.stdout.write(f"Znaleziono {len(chunks)} akapitów. Generuję wektory...")

        for i, chunk in enumerate(chunks):
            vector = get_embedding(chunk)
            if vector:
                database.append({'id': i, 'content': chunk, 'vector': vector})
                self.stdout.write(f"Zindeksowano: {i + 1}/{len(chunks)}")

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(database, f)

        self.stdout.write(self.style.SUCCESS('Sukces! Baza vector_db.json gotowa.'))