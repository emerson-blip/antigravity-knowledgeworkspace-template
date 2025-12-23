# 🤖 Notion AI Prompt: Agent Mission Generator (Notion-First)

Gebruik deze prompt in Notion AI om een gestructureerde `mission.md` voor de Emerson Agent te genereren.

---

**Prompt Tekst (Kopieer hieronder):**

> Jij bent een expert in het configureren van AI Agents. Ik wil een `mission.md` bestand genereren voor mijn Emerson Agent. Mijn filosofie is: **Notion is de Single Source of Truth**. Volg deze stappen:
>
> ### Stap 1: Analyseer de Notion Pagina
>
> Scan deze pagina en identificeer alle context:
>
> - **Project Info**: Naam, ID (UUID of URL slug), Status, Budget, Deadline.
> - **Inhoudelijke Focus**: Zoek naar workshop resultaten, briefing teksten of vergadernotities in de body van deze pagina. Vat de kernpunten kort samen.
>
> ### Stap 2: Vraag om Verfijning
>
> Stel mij (de gebruiker) de volgende drie vragen:
>
> 1. **Sessie Doel**: Wat is het primaire doel van deze specifieke sessie?
> 2. **Prioritaire Taken**: Welke drie concrete acties moet de agent nu uitvoeren op basis van de info op deze pagina?
> 3. **Output Map**: Naar welke map in de Obsidian Vault moeten de resultaten van deze sessie worden gearchiveerd?
>
> ### Stap 3: Genereer Output
>
> Maak een Markdown codeblok voor `mission.md`:
>
> ```markdown
> # 🚀 Mission: [Project Naam]
> 
> **Status:** [Huidige Status]
> **Project ID:** `[Project ID]`
> **Primary Source:** Notion Project Page (Body & Properties)
> 
> ## 🎯 Objective
> [Doel uit stap 2.1]
> 
> ## 📥 Inputs & Context
> 1. **Notion (All Context)**: De agent leest zowel de properties als de pagina-inhoud van dit project in Notion voor de volledige briefing.
> 2. **Human Context**: Gebaseerd op de direct verstrekte prioritering in deze missie.
> 
> ## 🛠️ Tasks voor deze sessie
> - [ ] **Context Sync**: Synchroniseer de laatste feiten en briefing uit de Notion projectpagina.
> - [ ] [Taak 1 uit stap 2.2]
> - [ ] [Taak 2 uit stap 2.2]
> - [ ] [Taak 3 uit stap 2.2]
> 
> ## ⚖️ Constraints
> - Respecteer de budget drempels uit de Notion property ([Budget]).
> - Gebruik Obsidian enkel voor artifact-archivering in de map [Map uit stap 2.3].
> ```
>
> **Wacht tot ik "START" zeg en stel me dan de vragen uit Stap 2.**

---

## Hoe te gebruiken

1. Open een **Project** pagina in Notion.
2. Activeer Notion AI (spatiebalk) of maak een "AI block" aan.
3. Plak de bovenstaande tekst.
4. Beantwoord de vragen van de AI.
5. Kopieer het resultaat naar je lokale `mission.md`.
