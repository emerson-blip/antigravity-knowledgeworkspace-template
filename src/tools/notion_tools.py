from datetime import datetime
from typing import Optional
from src.notion_client import EmersonNotionClient
from src.escalation import EscalationHandler, EscalationResult
from src.models import Action

# Initialize clients
notion = EmersonNotionClient()
escalation = EscalationHandler()

def get_project_status(project_name: str) -> str:
    """Haal status en details van een project op uit Notion.
    
    Args:
        project_name: De naam van het project om te zoeken.
        
    Returns:
        Een geformatteerde string met projectdetails en de Notion URL.
    """
    projects = notion.list_projects()
    # Simpele fuzzy search op naam
    project = next((p for p in projects if project_name.lower() in p.name.lower()), None)
    
    if not project:
        return f"Project '{project_name}' niet gevonden."
        
    return f"Project: {project.name}\nStatus: {project.status}\nLink: {project.url}"

def create_task(project_name: str, title: str, due_date: Optional[str] = None) -> str:
    """Maak een nieuwe taak aan in Notion, gekoppeld aan een project.
    
    Args:
        project_name: De naam van het project waar de taak bij hoort.
        title: De titel van de taak.
        due_date: Optionele deadline (YYYY-MM-DD).
        
    Returns:
        Bevestigingsbericht met de link naar de nieuwe taak.
    """
    projects = notion.list_projects()
    project = next((p for p in projects if project_name.lower() in p.name.lower()), None)
    
    if not project:
        return f"Kon taak niet aanmaken: Project '{project_name}' niet gevonden."
        
    task = notion.create_task(project_id=project.id, title=title, due_date=due_date)
    
    if task:
        notion.log_event("P2", f"Taak aangemaakt: {title}", {"project": project.name})
        return f"✅ Taak '{title}' aangemaakt voor project {project.name}.\nLink: {task.url}"
    else:
        return "❌ Er is een fout opgetreden bij het aanmaken van de taak."

def daily_check() -> str:
    """Genereer een dagelijks overzicht van actieve projecten en taken.
    
    Returns:
        Een samenvatting van de status van vandaag.
    """
    active_projects = notion.list_projects(status="Active")
    
    if not active_projects:
        return "Geen actieve projecten gevonden voor vandaag."
        
    lines = ["📅 **Dagelijks Overzicht**", ""]
    for p in active_projects:
        lines.append(f"- **{p.name}**: {p.status}")
        
    return "\n".join(lines)

def search_projects(query: str) -> str:
    """Zoek naar projecten in Notion op basis van een zoekterm.
    
    Args:
        query: De zoekterm (naam, klant, etc.)
        
    Returns:
        Lijst met gevonden projecten.
    """
    all_projects = notion.list_projects()
    matches = [p for p in all_projects if query.lower() in p.name.lower()]
    
    if not matches:
        return f"Geen projecten gevonden die voldoen aan '{query}'."
        
    lines = [f"Gevonden projecten voor '{query}':"]
    for m in matches:
        lines.append(f"• {m.name} ({m.status}) - {m.url}")
        
    return "\n".join(lines)
