import re
import time
from pathlib import Path

import requests

# ==========================================
# KONFIGURATION
# ==========================================

SOURCE_URL = "https://everyuuid.com/"

API_URL = (
    "https://mowojang.matdoes.dev"
    "/session/minecraft/profile/{}"
)

OUTPUT_FILE = Path("uuid.txt")

REQUEST_TIMEOUT = 20
REQUEST_DELAY = 1.0
RETRY_DELAY = 10.0
MAX_RETRIES = 5

UUID_PATTERN = re.compile(
    r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-"
    r"[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"
)

session = requests.Session()

session.headers.update({
    "User-Agent": "MinecraftUUIDChecker/1.0",
    "Accept": "application/json, text/html"
})


# ==========================================
# UUIDS VON EVERYUUID.COM LADEN
# ==========================================

def load_uuids():
    print(f"Lade UUIDs von {SOURCE_URL}")

    response = session.get(
        SOURCE_URL,
        timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()

    found = UUID_PATTERN.findall(response.text)

    # Duplikate entfernen und Reihenfolge beibehalten
    uuids = list(dict.fromkeys(
        uuid.lower() for uuid in found
    ))

    print(f"Gefundene UUIDs: {len(uuids)}")

    if not uuids:
        print(
            "Keine UUIDs im HTML gefunden. "
            "Die Website könnte UUIDs dynamisch laden "
            "oder eine andere Datenquelle verwenden."
        )

    return uuids


# ==========================================
# BEREITS GESPEICHERTE UUIDS LADEN
# ==========================================

def load_saved_uuids():
    if not OUTPUT_FILE.exists():
        return set()

    with OUTPUT_FILE.open("r", encoding="utf-8") as file:
        return {
            line.strip().lower()
            for line in file
            if line.strip()
        }


# ==========================================
# UUID ÜBER MOWOJANG API PRÜFEN
# ==========================================

def check_uuid(uuid):
    # Die API erhält die UUID ohne Bindestriche
    uuid_without_hyphens = uuid.replace("-", "")

    url = API_URL.format(uuid_without_hyphens)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = session.get(
                url,
                timeout=REQUEST_TIMEOUT
            )

            if response.status_code == 200:
                data = response.json()

                returned_id = str(
                    data.get("id", "")
                ).replace("-", "").lower()

                expected_id = uuid_without_hyphens.lower()

                if (
                    returned_id == expected_id
                    and data.get("name")
                ):
                    return "valid"

                return "unknown"

            if response.status_code in (204, 404):
                return "not_found"

            if response.status_code == 429:
                wait = min(30 * attempt, 120)
                print(
                    f"API-Limit erreicht. "
                    f"Warte {wait} Sekunden ..."
                )
                time.sleep(wait)
                continue

            if response.status_code >= 500:
                print(
                    f"API-Serverfehler "
                    f"({response.status_code})"
                )
            else:
                print(
                    f"Unerwarteter HTTP-Status: "
                    f"{response.status_code}"
                )

        except (requests.RequestException, ValueError) as error:
            print(f"Anfrage fehlgeschlagen: {error}")

        if attempt < MAX_RETRIES:
            time.sleep(RETRY_DELAY * attempt)

    return "unknown"


# ==========================================
# HAUPTPROGRAMM
# ==========================================

def main():
    try:
        uuids = load_uuids()
    except requests.RequestException as error:
        print(f"Fehler beim Laden der Website: {error}")
        return

    if not uuids:
        print("Keine UUIDs zum Überprüfen vorhanden.")
        return

    saved = load_saved_uuids()

    print(f"Bereits gespeichert: {len(saved)}")
    print("Starte Überprüfung über Mowojang API ...\n")

    checked = 0
    added = 0
    not_found = 0
    unknown = 0

    with OUTPUT_FILE.open("a", encoding="utf-8") as file:
        for index, uuid in enumerate(uuids, start=1):

            # Bereits gespeicherte UUIDs überspringen
            if uuid in saved:
                continue

            result = check_uuid(uuid)
            checked += 1

            if result == "valid":
                file.write(uuid + "\n")
                file.flush()

                saved.add(uuid)
                added += 1

                print(
                    f"[{index}/{len(uuids)}] "
                    f"BESTÄTIGT: {uuid}"
                )

            elif result == "not_found":
                not_found += 1

                print(
                    f"[{index}/{len(uuids)}] "
                    f"Kein Profil gefunden: {uuid}"
                )

            else:
                unknown += 1

                print(
                    f"[{index}/{len(uuids)}] "
                    f"NICHT BESTÄTIGT: {uuid}"
                )

            time.sleep(REQUEST_DELAY)

    print("\n========== FERTIG ==========")
    print(f"Überprüft:           {checked}")
    print(f"Neu gespeichert:     {added}")
    print(f"Kein Profil:         {not_found}")
    print(f"Unklar/Fehler:       {unknown}")
    print(f"Gesamt gespeichert:  {len(saved)}")
    print(f"Ausgabedatei:        {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    main()
