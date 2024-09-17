### 1. **Imports (Lijnen 1-6):**
   - De benodigde modules en bibliotheken worden geïmporteerd:
     - `os`: Voor het werken met besturingssysteem-functionaliteiten, zoals het wissen van de terminal of het controleren van bestandspaden.
     - `re`: Voor reguliere expressies, gebruikt voor tekstmanipulatie.
     - `datetime`: Voor het genereren van tijdstempels voor logbestanden.
     - `collections.defaultdict`: Voor het automatisch toekennen van standaardwaarden aan de dictionary die wordt gebruikt om pagina-scores bij te houden.
     - `colorama`: Voor het gebruik van kleuren in de terminal (kleurcodering voor vragen en meldingen).

### 2. **TEMPLATES en KEYWORDS dictionaries (Lijnen 8-12):**
   - Hier worden lege dictionaries gedefinieerd (`TEMPLATES` en `KEYWORDS`). Deze worden later gebruikt om de templates van de pagina en de bijbehorende zoekwoorden te definiëren.

### 3. **Functie `sanitize_filename` (Lijnen 14-19):**
   - Deze functie verwijdert ongewenste karakters uit een bestandsnaam en vervangt spaties door underscores. 
   - Het is belangrijk om ervoor te zorgen dat de bestandsnaam geldig is binnen verschillende besturingssystemen.

### 4. **Functie `parse_color` (Lijnen 21-37):**
   - Deze functie bepaalt hoe een kleur wordt toegepast op een HTML-element:
     - Controleert of de ingevoerde kleur een hexadecimale kleurcode of RGB-waarde is.
     - Als de ingevoerde kleur een van de standaard Bootstrap-kleuren is (zoals `primary`, `danger`, etc.), wordt de juiste klasse toegevoegd.
     - Als het gewoon een kleurnaam is, wordt deze gebruikt in een inline `background-color` stijl.

### 5. **Functie `get_page_from_description` (Lijnen 39-49):**
   - Deze functie bepaalt op basis van een omschrijving welke pagina (template) het beste past.
   - De zoekwoorden in `KEYWORDS` worden gebruikt om de beste pagina te kiezen door het tellen van hoeveel keer de zoekwoorden in de omschrijving voorkomen.

### 6. **Functie `modify_template` (Lijnen 51-95):**
   - De belangrijkste functie die een bestaande template aanpast op basis van ingevoerde gegevens:
     - Vervangt verschillende secties van de HTML-template, zoals de titel, header-tekst, primaire/secondaire kleuren, afbeeldingsbeschrijvingen, knoppen, enz.
     - Dit gebeurt door de juiste secties van de template te zoeken en te vervangen door nieuwe waarden.
     - Het resultaat wordt weggeschreven naar een nieuw HTML-bestand.

### 7. **Functie `log_creation` (Lijnen 97-107):**
   - Deze functie logt elke gemaakte pagina door de omschrijving en het type pagina toe te voegen aan een logbestand, samen met een tijdstempel.

### 8. **Functie `ask_question` (Lijnen 109-113):**
   - Deze functie stelt een vraag in de terminal en retourneert het antwoord van de gebruiker.
   - De vraag wordt weergegeven in een bepaalde kleur (standaard `Fore.RED`), wat wordt gebruikt voor visuele consistentie.

### 9. **Functie `create_page` (Lijnen 115-179):**
   - Deze functie beheert het volledige proces voor het maken van een pagina:
     - Eerst wordt gevraagd of de gebruiker de 'easy' of 'hard' modus wil gebruiken, wat bepaalt hoeveel gegevens de gebruiker moet invoeren.
     - In de 'hard' modus worden er meer vragen gesteld over de inhoud van de website, zoals afbeeldingsbeschrijvingen en knoppen.
     - Op basis van de ingevoerde beschrijving wordt een pagina-template gekozen.
     - Daarna wordt de pagina gegenereerd, opgeslagen, en de creatie wordt gelogd.

### 10. **Hoofdfunctie `if __name__ == "__main__":` (Lijnen 181-183):**
   - Dit blok zorgt ervoor dat het script wordt uitgevoerd als het bestand direct wordt uitgevoerd. Het roept de `create_page` functie aan om het proces te starten.
