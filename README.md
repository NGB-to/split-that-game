# split-that-game
Split a game or application across HDD storages and SSD/M.2 SSD devices

---

For reference the German language discussions about this tool(s) over at [NGB.to - Programmier-Idee-Teamwork "split-that-game"](https://ngb.to/threads/94111-Programmier-Idee-Teamwork-quot-split-that-game-quot)

---

**German language project outline:**

### Idee und Hintergrund
Die Grundidee ist einfach: *Spiele oder Anwendungen zu splitten bzw. aufzuteilen und höchstmögliche Performance versus Speichernutzung zu erreichen.*

Heißt, auf **SSD/M.2 SSD Medien Platz zu sparen** und auf **normalen HDDs nicht so häufig genutze Daten auszulagern**, welche nicht kritisch für die Performance von Spielen oder Anwendungen sind - aber viel Platz einnehmen würden.

Um dieses Ziel zu erreichen, sollen **Junctions in Windows** bzw. **Symlinks unter Linux** verwendet werden. Profile sollen diesen Prozess, mit vorher definierten Regeln, vereinfachen.

Und eine **Onlineschnittstelle durch eine Community unterstützt** könnte **Profile bzw. Presets** für Spiele und Anwendungen bereithalten die lokal angewendet werden können.

Zu guter letzt sollen **Helfer Werkzeuge (Helper Tools)** dafür sorgen mit dem eigentlichen Analyse-Prozess beginnen zu können um Profile, erfolgreich, zu kreieren.

---

### Gliederung
1. eine GUI-Desktop Anwendung

2. eine Onlineschnittstelle

3. Profil-Aufbau

4. Helper Tools und erste Schritte

5. Windows (DisableLastAccess)

---

### 1. Die GUI-Anwendung, möglicher Flow

##### Kernfunktionen der GUI-App
- Navigiere zu einem Ordner und setze diesen als "Quellordner" für das Spiel (idealerweise das langsamere Laufwerk wo die Daten permanent verbleiben)

- Setze den Namen für das Profil und eine eventuelle Version (leer = keine Angabe)

- Klick auf **"Analyze"** und lasse die App die LastAccess, ModificationTime, Größe erfassen aus dem Quellordner

- Selektiere Dateien oder ganzen Ordner aus dem Quellordner, die kopiert werden sollen, für die Symlinks

- Erstelle / Navigiere zu einem Zielordner, in den die Auswahl später kopiert werden soll
    (dies kann aus Optionen auch ein fixer Oberordner sein, mit Spielname als Titel aus der Eingabe für den Unterordner)

- Wähle **"split-that-game"** was:
    * Die Inhalte verschiebt und gegebenenfalls prüft, ob diese nicht schon in Zielordner existieren bzw. ob diese verändert worden sind (LastAccess, ModificationTime).
    
    * Die Symlinks in Quellordner setzt zu Dateien und Ordnern - so fern nicht vorhanden
    
    * Speichere die aktuelle Einstellung im aktiven Profil (bzw. das eigene lokale Profil) für das Spiel oder die Anwendung
        * (hier wäre eine File-Based Lösung gut: **/split-that-game/userProfiles/localId.stg**)
        *  Meta-Informationen landen ebenfalls in der lokalen Datenbank
    
    * Speichere die Dateninformation in der lokalen DB für spätere Vergleiche - dies könnt den JSON Output von **PayLoadTimer.py** verwenden und oder einer eigenen integrierten Funktion.
   
---

##### Weitere Features
- Eingabe der Profil Eckdaten, siehe 2.

- Erstellen/Verwalten einer MD5 Checksumme für die Spiel/Anwendungs Executable/EXE

- Aufgrund von Beschränkungen in Windows Symlink: Aktivieren / Deaktivieren von Symlinks aus Profilen on demand

- Anzeige der verfügbaren Symlinks/Softlinks die verlinkt werden können
    - Windows > **a limit of 63 reparse points on any given path.**
        - ***https://docs.microsoft.com/en-us/windows/win32/fileio/reparse-points***

- Downloaden von Profilen aus der Onlineschnittstelle über eine API
    * Beispiel: **/split-that-game/gameProfiles/authorName_profileId.stg**
      * Informationen über die Profile landen außerdem in der Datenbank und werden auf Wahl **Update profiles** aktualisiert.
    
- Auswahl einer Spielversion welche in den Profilen enthalten ist.

- Bewertung von Dateien für die Scores 0 >= 10, wobei:
    * 10 = High Latency (oft genutzt)
    * 0 = Low Latency (wenig oder nur einmal genutzt)

- Upload des eigenen Profils zur Onlineversion (nach Registrierung), gegebenfalls mit Freischaltung oder Bewertung

- Auswahl des Betriebssystems und der Version des Spieles und Benutzer-Kommentar zum Profil

- Auswahl von eigenen und Community-Profilen

- Übersicht über alle Profile zu einem Spiel

- Inkompatible Versionen bzw. Angabe mit Version x.x.x getestet

- Angabe von Spielordner, die gescannt werden auf bestehende Spiele. Beispielsweise Gog/Steam/Epic auf bekannte Titel mit Profilvorschlägen so fern vorhanden

- Anzeige des freien Speichers auf der Symlink SSD/M2 - und die neue Belegung durch neue Symlinks/Daten in einer Vorschau

- Schnelle Deinstallation/Unlinking von Spielen und Anwendungen einhergehend mit einer Visualisierung des von Anwendungen belegten Platzes auf Link-Laufwerk

- Wenn Steam/Client Spiele mit gesetzten Symlinks aktualisiert/updated und Zeitstempel abweichen - Daten von SSD auf HDD synchronisieren um die Stammdaten aktuell zu halten damit nur ein Update gefahren werden muss.
  * Hinweis auf zu aktualisierende Inhalte bei Klick auf **"Refresh game contents"** was ein Update durchführt zwischen HDD und SSD

  * Setzen von Prioritäten/Scores für Dateien/Inhalte für Performance vs. Disk Usage Tradeoffs in Profilen

---
  
### 2. Profil-Aufbau

Analysedaten von Dateien sollten in einer SQLite DB landen. Heruntergeladene Profile in Dateien im JSON Format.

Beispiel: **/split-that-game/gameProfiles/authorName_profileId.stg**
    

* Autor       
     * Autor Name                 => **name**  
  
     * Email                      => **email**  (Optional)
  

* Profile                         => **profile**
    * Id des Profiles             => **id**
  
    * Basiert auf/abgeleitet von  => **basedOn**  (Id)
  
    * Kommentar                   => **comment**     

    * Zeitstempel                 => **times**
          * Erstellt              => **created**
  
          * Aktualisiert          => **changed** 
    
    * Gesamt-Score (siehe Details) => **score**
  


* Spieldetails                      => **game**
    * MD5 Checksum (MainEXE)        => **gMd5**
    * Spielname                     => **gName**
    * Spielversion                  => **gVersion**
    * Betriebssystem                => **gOs**
    * Quellordner                   => **gBase**

* Details
    * Ordner /video => Relativ zu "gBase"
        * **stg_wholeLink** = true/false (ganzes Verzeichnis Symlinken)
        * **stg_fileList** (Dateiliste wenn nicht => **stg_wholeLink = true**)
            * Dateiname
                * Größe in Bytes => **size**
                * Linking-Status    => **status** aktiv/inaktiv
                * Performance-Score 0 >= 10
                    * 0 = **High Load** auf HDD
                    * 5 = **Medium Load** auf HDD
                    * 10 = **Low oder One time Load** auf HDD
                * Lokales Profil
                    * Änderungszeit => **mTime** (modificationTime)
                    * Zugriffszeit => **aTime** (accessTime)
   
---        

### 3. Die Onlineschnittstelle
- Download von aktuellen Profilen (ohne Registrierung) mittels API im JSON Format

- Eintragen/Upload von Profilen

- Registrierung mit Benutzername/Email - nur für das Eintragen von Profilen und auch aus der GUI-App heraus möglich

- Online-Suche in der Datenbank nach Spiel und Anwendungsprofilen

- Bewertung von Profilen (negative könnten rausfliegen aus der Ansicht und sind nur über extra Knopfdruck sichtbar, bleiben aber in der Datenbank erhalten)

---

### 4. Helper Tools

* PythonSkript **PayLoadTimer.py/exe**: Unter Linux und oder Windows die Zugriffe tracken um mögliche Profildaten zu gewinnen, soll in die GUI Anwendung fließen.
    * Um **PayLoadTimer.py bzw PayLoadTimer.exe** zu nutzen, muß der Pfad zum Spiel oder der Anwendung in einer Textdatei **src.txt** gespeichert sein, im gleichen Ordner in dem sich PayLoadTimer befindet.

Hier eine Kurzanleitung wie ein Spiel oder Anwendung protokolliert werden kann:
1. Unter Windows mittels fsutil die Option DisableLastAccess auf 0 (Null) stellen und ausschalten
2. Pfad zum Spiel in **src.txt** eintragen
3. **PayLoadTimer.py / PayloadTimer.exe** starten
4. Spiel oder Anwendung starten und spielen bzw. arbeiten
5. Spiel oder Anwendung beenden
6. PayLoadTimer mit **Strg + C beenden**, es wird eine **JSON** mit den Zugriffen erstellt, welche zur weiteren Analyse wichtig sind. Diese in das Verzeichniss von **VisualizePayLoad** kopieren und selbiges starten. Daraufhin wird eine Grafik mit den häufigkeiten der Zugriffen ersellt.

* PythonSkript **VisualizePayload.py/exe**: Visualisiert den Namen, die Häufigkeit der Zugriffe und Abständen von Zugriffen auf Dateien nach einer Sitzung mit Ausgabe von PayLoadTimer.py. - Auch ein Kandidate für die GUI Lösung, also alles in einem.


---

### 5. DisableLastAccess

Anleitung um "DisableLastAccess" unter Windows auszuschalten, was Standardmäßig aktiviert ist:

1. Windows **cmd**/Kommandozeile als Admin starten
2. Den Status prüfen: **fsutil behavior query DisableLastAccess** gibt den Status **!= 0 an** oder **0 = aus** zurück
3. Zugriffszeit **aktivieren**: **fsutil behavior set DisableLastAccess 0**, jetzt Windows neu starten
4. Nachdem die Option aktiviert ist, was die Performance etwas drücken kann, können mittels **PayLoadTimer.py/exe** die Zugriffe protokolliert werden.
5. Zeitstempel **deaktivieren**: **fsutil behavior set DisableLastAccess 1** und Windows neu starten
