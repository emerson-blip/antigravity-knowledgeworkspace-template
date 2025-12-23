# 🏗️ Notion OS: Database Schema & Relaties

De Emerson Agent gebruikt Notion als "Single Source of Truth". Hieronder staan de database IDs en hun relaties.

## Core Databases

| Database | Collection ID | Functie |
| :--- | :--- | :--- |
| Projects | `1ac354a7-949c-8138-82d8-000b3e8c983f` | Projectbeheer, leads en trajecten. |
| Tasks | `1ac354a7-949c-814c-a640-000b8b50090a` | Taken gekoppeld aan projecten. |
| Companies | `901d70b9-3c04-4a7a-9cc0-9761c04a7bbb` | CRM: Klanten en prospects. |
| People | `4bae9ced-3184-4a9f-9896-59cc808931ce` | Contactpersonen bij bedrijven. |
| Offertes | `4c95c3fa-217a-4810-bc79-3c9996db14ff` | Proposals en offertes. |
| Facturen | `de1c2574-729a-4bda-899b-166f4da50094` | Facturatie status. |
| Events | `1c5354a7-949c-8124-974a-000b5c38db4b` | Meetings en workshops. |
| Agent Logs | `197daeb1-7fbf-446d-a81b-b3ec716196be` | Systeem logs van de agent. |
| Prompts | `4384cf24-c692-413d-ba06-93c935cae521` | Herbruikbare AI prompts. |

## Relaties

- **Companies** hebben een relatie met **Projects** en **People**.
- **Projects** hebben een relatie met **Tasks**, **Offertes** en **Events**.
- **Offertes** leiden tot **Facturen**.

## Status Flows

### Projects

`Lead` ➔ `Qualification` ➔ `Proposal` ➔ `Negotiation` ➔ `Won/Lost` ➔ `Active` ➔ `Done`

### Companies

`Prospect` ➔ `Qualified` ➔ `Client` ➔ `Partner`

### Tasks

`To Do` ➔ `In Progress` ➔ `Done`
