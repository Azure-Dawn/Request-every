Minecraft UUID Checker

Ein einfaches Python-Skript, das UUIDs von everyuuid.com lädt und über die Mowojang API überprüft.

Funktionen

* Lädt UUIDs von everyuuid.com.
* Überprüft die UUIDs über die Mowojang API.
* Speichert bestätigte Minecraft-UUIDs in uuid.txt.
* Speichert jede UUID in einer eigenen Zeile.
* Überspringt UUIDs, die bereits gespeichert wurden.
* Wiederholt fehlgeschlagene Anfragen automatisch.

Voraussetzungen

* Python 3
* Eine Internetverbindung
* Die Python-Bibliothek requests

Installation

Installiere zuerst die benötigte Bibliothek:

python -m pip install requests

Lade anschliessend das Skript herunter oder klone das Repository.

Starten

Öffne ein Terminal im Ordner des Skripts und führe folgenden Befehl aus:

python main.py

Das Skript startet automatisch und beginnt mit der Überprüfung der gefundenen UUIDs.

Ausgabedatei

Bestätigte UUIDs werden in der Datei uuid.txt gespeichert.

Beispiel:

497dcba3-ecbf-4587-a2dd-5eb0665e6880
50e14f43-dd4e-412f-864d-78943ea28d91
7edb3b2e-869c-485b-af70-76a934e0fcfd

Jede UUID steht in einer eigenen Zeile.

Hinweise

* Bereits gespeicherte UUIDs werden übersprungen.
* Nicht bestätigte UUIDs werden nicht gespeichert.
* Die Anzahl der gefundenen UUIDs hängt davon ab, welche UUIDs everyuuid.com direkt bereitstellt.
* Bei API-Limits oder Verbindungsfehlern wartet das Skript und versucht die Anfrage erneut.

Verwendete Dienste

* everyuuid.com: Quelle der UUIDs
* Mowojang API: Überprüfung der Minecraft-Profile

Lizenz

Du kannst hier die gewünschte Lizenz für dein Projekt eintragen.
