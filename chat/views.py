from django.shortcuts import render
from .rag_utils import search_knowledge_base
import ollama


def chat_view(request):
    # Inicjalizacja historii w sesji
    if 'history' not in request.session:
        request.session['history'] = []

    context_used = None

    if request.method == "POST":
        user_query = request.POST.get('query')


        if user_query == '/reset':
            request.session['history'] = []
            request.session.modified = True
            return render(request, 'chat.html', {'history': [], 'context': None})
        # --------------------------------------------

        if user_query:

            request.session['history'].append({'role': 'user', 'content': user_query})


            results = search_knowledge_base(user_query, limit=4)
            print(f"DEBUG - ZNALEZIONO: {results}")  # Podgląd w konsoli

            context_text = "\n\n".join([r['content'] for r in results])
            context_used = results


            system_instruction = f"""
            Jesteś Mistrzem Gry lub Kreatywnym Asystentem opierającym się na poniższym tekście.
            Twoim celem jest budowanie ciekawej narracji i pomoc użytkownikowi.

            ZASADY:
            1. BAZA WIEDZY (poniżej) to Twoje główne źródło faktów o świecie/zasadach.
            2. JEŚLI CZEGOŚ BRAKUJE W BAZIE -> IMPROWIZUJ w klimacie tekstu! (Nie mów "nie wiem").
            3. Opisuj otoczenie, dźwięki i detale. Bądź klimatyczny.
            4. Jeśli to gra RPG, reaguj na decyzje gracza i popychaj fabułę do przodu.

            BAZA WIEDZY:
            ###
            {context_text}
            ###
            """


            messages_payload = [{'role': 'system', 'content': system_instruction}]


            chat_history = request.session['history'][-5:]
            messages_payload.extend(chat_history)


            try:
                response = ollama.chat(
                    model='llama3.2',
                    messages=messages_payload,

                    options={'temperature': 0.15}
                )
                bot_response = response['message']['content']
            except Exception as e:
                bot_response = f"Błąd modelu: {str(e)}"


            request.session['history'].append({'role': 'assistant', 'content': bot_response})
            request.session.modified = True

    return render(request, 'chat.html', {
        'history': request.session['history'],
        'context': context_used
    })