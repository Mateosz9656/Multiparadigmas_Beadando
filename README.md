# Python Időjárás Alkalmazás (Mikroszerviz Architektúra)

Ez a projekt egy mikroszerviz-alapú webalkalmazás, amely a **FastAPI** (Backend) és **Streamlit** (Frontend) keretrendszereket használja. Az alkalmazás képes időjárási adatok lekérésére külső API-ból (WeatherAPI.com), azok adatbázisba mentésére (SQLite), időzített háttérfolyamatok futtatására és az adatok vizualizációjára.

A Beadandó követelményeinek megfelelően készült.

## Funkciók

*   **Backend (FastAPI):** REST API végpontok az adatok kezeléséhez.
*   **Frontend (Streamlit):** Felhasználói felület az adatok megjelenítéséhez és diagramokhoz.
*   **Adatbázis (SQLAlchemy + SQLite):** Adatok tartós tárolása.
*   **Automatizáció:** 1 oránként automatikus adatmentés (háttérszolgáltatás).
*   **Tesztelés:** Pytest alapú egységtesztek.

## Architektúra

A rendszer három fő rétegre tagolódik:

1.  **Frontend (`frontend/`):** Streamlit alkalmazás, amely HTTP kéréseket küld a Backendnek.
2.  **Backend (`backend/`):** FastAPI alkalmazás, amely kezeli az üzleti logikát és az adatbázist.
    *   `api/`: Végpontok definíciója.
    *   `services/`: Üzleti logika (WeatherService).
    *   `db/`: Adatbázis modellek és kapcsolat.
    *   `config/`: Környezeti változók (.env) kezelése.
    *   `tasks/`: Háttérfolyamatok (Scheduler).
3.  **Adatbázis (`weather.db`):** Helyi SQLite fájl.

## Telepítés és Indítás

### 1. Előfeltételek
*   Python 3.9+ telepítve.
*   Git telepítve.

### 2. Telepítés
```bash
# Repository klónozása (ha gitből jön)
# git clone ...

# Belépés a mappába
cd Multiparadigmas_Beadand-

# Virtuális környezet létrehozása
python -m venv venv

# Aktiválás (Windows)
.\venv\Scripts\activate
# Aktiválás (Linux/Mac)
# source venv/bin/activate

# Függőségek telepítése
pip install -r requirements.txt
```

### 3. Konfiguráció
Hozd létre a `.env` fájlt a gyökérkönyvtárban és add meg az API kulcsodat (WeatherAPI.com):
```
WEATHER_API_KEY=az_te_api_kulcsod
```

### 4. Indítás
A teljes rendszer (Backend + Frontend) egyetlen paranccsal indítható:

```bash
python run_app.py
```

Alternatív módon külön terminálokban:
*   Backend: `uvicorn backend.main:app --reload`
*   Frontend: `streamlit run frontend/app.py`

## Tesztek futtatása
```bash
pytest
```
