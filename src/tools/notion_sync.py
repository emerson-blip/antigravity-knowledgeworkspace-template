import os
import re
from pathlib import Path
from src.config import settings
from src.notion_client import EmersonNotionClient

def sync_project_data() -> str:
    """
    Synchroniseert projectgegevens vanuit Notion naar de lokale README.md.
    
    Zoekt naar markers <!-- NOTION_SYNC_START --> en <!-- NOTION_SYNC_END -->
    in de README.md en vervangt de inhoud door actuele data uit Notion.
    
    Returns:
        Een bericht over de status van de synchronisatie.
    """
    project_id = settings.NOTION_PROJECT_ID
    if not project_id:
        return "⚠️ Geen NOTION_PROJECT_ID geconfigureerd in .env."

    notion = EmersonNotionClient()
    project = notion.get_project(project_id)
    
    if not project:
        return f"❌ Kon project met ID {project_id} niet vinden in Notion."

    # Haal taken op (voor nu gesimuleerd/gekoppeld aan project in Notion)
    # TODO: Uitbreiden met echte taak ophalen als de API dat toelaat
    
    sync_content = f"""
### 📊 Project Status: {project.name}
- **Status**: {project.status}
- **Notion Link**: [Open in Notion]({project.url})
- **Laatste Sync**: {os.popen('date').read().strip()}
"""

    readme_path = Path("README.md")
    if not readme_path.exists():
        return "❌ README.md niet gevonden."

    content = readme_path.read_text(encoding="utf-8")
    
    start_marker = "<!-- NOTION_SYNC_START -->"
    end_marker = "<!-- NOTION_SYNC_END -->"
    
    pattern = re.compile(f"{start_marker}.*?{end_marker}", re.DOTALL)
    new_content = pattern.sub(f"{start_marker}\n{sync_content}\n{end_marker}", content)
    
    if new_content == content:
        if start_marker not in content:
            return f"⚠️ Marker {start_marker} niet gevonden in README.md."
        return "ℹ️ Geen wijzigingen nodig in README.md."

    readme_path.write_text(new_content, encoding="utf-8")
    return f"✅ README.md succesvol gesynchroniseerd met Notion project: {project.name}"
