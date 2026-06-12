# ValAuto — Aplikacja do Wyceny Pojazdów

## Dla Klienta

**ValAuto** to  aplikacja webowa do szybkiej i dokładnej wyceny pojazdów samochodowych. Aplikacja wykorzystuje zaawansowany model uczenia maszynowego, który analizuje parametry pojazdu (markę, model, rok produkcji, przebieg, typ paliwa, skrzynię biegów) i podaje dokładną wycenę rynkową.

### Główne korzyści:
**Szybka wycena** — wynik w kilka sekund
**Dokładna wycena** — model trenowany na dużych zbiorach danych rynkowych
**Łatwy dostęp** — przejrzysty interfejs webowy dostępny z każdego urządzenia
**Zmienne rynkowe** — wycena uwzględnia aktualną markę, model i parametry techniczne

---

## Dla Administratora

### Wymagania systemowe

- **System operacyjny**: Windows 10/11 lub Linux (np. Ubuntu 22.04 LTS / Debian 12)
- **Miejsce na dysku**: minimum 20 GB
- **Pamięć RAM**: minimum 8 GB (rekomendacja: 16 GB)
- **Połączenie internetowe**: do pobrania obrazów Docker i pakietów

#### Windows z Docker Desktop:
- WSL2 (Windows Subsystem for Linux 2) — skonfigurowany
- Docker Desktop — zainstalowany z backendem WSL2

---

## Instalacja

### 1. Zainstaluj wymagane narzędzia

#### Git
- **Windows**: Pobierz z https://git-scm.com/download/win
- **Linux (Ubuntu/Debian)**:
  ```bash
  sudo apt update
  sudo apt install -y git
  ```

#### Docker
- **Windows**: Pobierz Docker Desktop z https://www.docker.com/products/docker-desktop i zaznacz opcję "Use WSL2"
- **Linux (Ubuntu/Debian)**:
  ```bash
  sudo apt update
  sudo apt install -y docker.io docker-compose-plugin
  sudo systemctl enable --now docker
  ```

#### Git LFS (dla obsługi dużych plików)
- **Windows**: Pobierz z https://git-lfs.github.com/
- **Linux (Ubuntu/Debian)**:
  ```bash
  sudo apt update
  sudo apt install -y git-lfs
  git lfs install
  ```

### 2. Sklonuj repozytoria

W katalog roboczym (np. `Downloads`):

```bash
# Sklonuj branch aplikacji
git clone --branch SUML-valauto https://github.com/s24118-ui/SUML.git SUML-valauto

# Sklonuj branch z danymi i modelem
git clone --branch SUML-main https://github.com/s24118-ui/SUML.git SUML-main
```

**Struktura katalogów:**
```
Downloads/
  ├── SUML-valauto/          (aplikacja z branch `SUML-valauto`)
  └── SUML-main/             (dane i model z branch `SUML-main`)
```

### 3. Konfiguracja (.env)

Skopiuj plik konfiguracyjny:

**Windows (PowerShell)**:
```powershell
cd SUML-valauto
Copy-Item .env.example .env
```

**Windows (CMD)**:
```cmd
cd SUML-valauto
copy .env.example .env
```

**Linux**:
```bash
cd SUML-valauto
cp .env.example .env
```

Edytuj `.env` i ustaw:
```env
VITE_API_URL=http://localhost:8000/evaluate
MODEL_PATH=/mnt/SUML-main/models/autogluon_price_model
SUML_ROOT=/mnt/SUML-main
CORS_ORIGINS=http://localhost:5173,https://localhost
```

---

## Uruchomienie aplikacji

### Startowanie

```bash
cd  (ścieżka do katalogu)/SUML-valauto

# Uruchom wszystko w tle
docker compose up -d

# LUB wyświetlaj logi (Ctrl+C aby zatrzymać)
docker compose up
```

Podczas pierwszego uruchomienia aplikacja automatycznie:
1. Pobiera i przetwarza dane
2. Trenuje model uczenia maszynowego jeśli nie istnieje (może zająć około godziny)
3. Udostępnia interfejs webowy


### Dostęp do aplikacji

Po uruchomieniu, aplikacja jest dostępna pod:

- **Aplikacja webowa**: https://localhost/
- **Dokumentacja API**: http://localhost:8000/docs

---

## Zarządzanie aplikacją

### Sprawdzenie statusu

```bash
docker compose ps
```

### Wyświetlanie logów

```bash
# Logi wszystkich serwisów
docker compose logs

# Logi konkretnego serwisu
docker compose logs api
docker compose logs front
```

### Zatrzymanie

```bash
# Wstrzymaj bez usuwania danych
docker compose stop

# Usunięcie kontenerów (dane pozostają)
docker compose down

# Pełne czyszczenie (usuwa także wolumeny - OSTROŻNIE!)
docker compose down -v
```

### Restartowanie

```bash
docker compose restart
```

---

