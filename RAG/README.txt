============================================================
PROJEKT: WŁASNY SYSTEM RAG (DJANGO + OLLAMA)
INSTRUKCJA INSTALACJI I URUCHOMIENIA
============================================================

1. WYMAGANIA WSTĘPNE
------------------------------------------------------------
Upewnij się, że masz zainstalowane:
- Python (wersja 3.10 lub nowsza)
- Ollama (musi być uruchomiona w tle)

2. PRZYGOTOWANIE MODELI AI (W TERMINALU)
------------------------------------------------------------
Wpisz poniższe komendy w terminalu (CMD/PowerShell), aby pobrać modele 
(jeśli jeszcze ich nie masz):

ollama pull llama3.2
ollama pull nomic-embed-text

3. INSTALACJA BIBLIOTEK PYTHON
------------------------------------------------------------
Zainstaluj Django oraz bibliotekę do obsługi Ollama. 
Będąc w folderze projektu (tam gdzie jest plik manage.py), wpisz:

pip install django ollama

4. PIERWSZE URUCHOMIENIE BAZY DANYCH (MIGRACJE)
------------------------------------------------------------
Aby system mógł zapisywać historię rozmów (sesje), musisz utworzyć 
strukture bazy danych. Wpisz:

python manage.py migrate

5. ŁADOWANIE BAZY WIEDZY (INDEKSOWANIE) - KLUCZOWE!
------------------------------------------------------------
To jest komenda, o którą pytałeś. Wykonuj ją za każdym razem, 
gdy zmienisz treść w pliku "base.txt".

Upewnij się, że plik "base.txt" znajduje się w głównym folderze 
(obok manage.py) i zawiera Twoją wiedzę.

Komenda do przetworzenia tekstu na bazę wektorową:

python manage.py build_index

(Jeśli zobaczysz błąd, upewnij się, że masz pobrany model nomic-embed-text 
z punktu 2).

6. URUCHOMIENIE APLIKACJI
------------------------------------------------------------
Aby włączyć serwer deweloperski, wpisz:

python manage.py runserver

7. ADRES STRONY WWW
------------------------------------------------------------
Po wpisaniu komendy "runserver", w terminalu zobaczysz komunikat 
z poprawnym adresem. Będzie on wyglądał np. tak:

"Starting development server at http://127.0.0.1:8000/"

Skopiuj ten adres z Twojego terminala i wklej go do przeglądarki. 
To da Ci pewność, że wchodzisz na dobry adres.

8. DODATKOWE FUNKCJE
------------------------------------------------------------
- Czyszczenie historii: Wpisz komendę /reset w oknie czatu.
- Debugowanie: W konsoli/terminalu zobaczysz fragmenty tekstu, 
  które system znalazł w bazie wiedzy.