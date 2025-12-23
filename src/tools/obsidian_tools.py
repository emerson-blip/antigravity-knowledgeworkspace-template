import os
import shutil
from pathlib import Path
from src.config import settings

def add_markdown_metadata(content: str, project_name: str, project_id: str, project_code: Optional[str] = None) -> str:
    """
    Voegt YAML frontmatter toe aan Markdown content voor Obsidian.
    Inclusief 'Projects' linking voor Obsidian organisatie.
    """
    from src.models import Project
    # Gebruik de model-logica voor consistente short_id
    temp_project = Project(id=project_id, url="", name=project_name, status="", project_code=project_code)
    short_id = temp_project.short_id
    
    frontmatter = f"""---
project: "{project_name}"
project_id: "{project_id}"
short_id: "{short_id}"
Projects: 
  - "[[{project_name}]]"
agent_sync: "{os.popen('date').read().strip()}"
---

"""
    if content.startswith("---"):
        # Als er al frontmatter is, voeg deze velden toe (simpele versie voor nu)
        return content # Voor nu laten we het even zo om complexiteit te beperken
        
    return frontmatter + content

def sync_to_obsidian(file_path: str, category: str = "Artifacts", project_id: Optional[str] = None) -> str:
    """
    Kopieert een bestand naar de Obsidian Vault, optioneel met project-specifieke naamgeving.
    
    Args:
        file_path: Het lokale pad naar het bestand.
        category: De submap in de Obsidian Vault.
        project_id: Optioneel Notion Project ID om project_code op te halen voor hernoeming.
        
    Returns:
        Statusbericht van de synchronisatie.
    """
    vault_path = settings.OBSIDIAN_VAULT_PATH
    if not vault_path:
        return "⚠️ Geen OBSIDIAN_VAULT_PATH geconfigureerd."

    vault_root = Path(vault_path)
    target_dir = vault_root / "_Agents" / "Emerson" / category
    target_dir.mkdir(parents=True, exist_ok=True)
    
    source_path = Path(file_path)
    if not source_path.exists():
        return f"❌ Bronbestand {file_path} niet gevonden."
        
    filename = source_path.name
    
    # Als er een project_id is, probeer de short_id te bemachtigen voor hernoeming
    if project_id:
        from src.notion_client import EmersonNotionClient
        notion = EmersonNotionClient()
        project = notion.get_project(project_id)
        if project:
            filename = f"{project.short_id}_{filename}"
            
            # Als het een Markdown bestand is, injecteer metadata
            if source_path.suffix == ".md":
                content = source_path.read_text(encoding="utf-8")
                new_content = add_markdown_metadata(content, project.name, project.id, project.project_code)
                # Schrijf tijdelijk naar een nieuw pad of hergebruik de bron als dat veilig is
                # Voor nu schrijven we direct naar de target met de nieuwe content
                target_path = target_dir / filename
                target_path.write_text(new_content, encoding="utf-8")
                return f"✅ Bestand (met metadata) gesynchroniseerd naar Obsidian: {target_path}"

    target_path = target_dir / filename
    
    try:
        shutil.copy2(source_path, target_path)
        return f"✅ Bestand gesynchroniseerd naar Obsidian: {target_path}"
    except Exception as e:
        return f"❌ Fout bij synchroniseren naar Obsidian: {e}"

def list_obsidian_context() -> str:
    """
    Lijst alle relevante contextbestanden uit de Obsidian Vault op.
    """
    vault_path = settings.OBSIDIAN_VAULT_PATH
    if not vault_path:
        return "⚠️ Geen OBSIDIAN_VAULT_PATH geconfigureerd."

    context_dir = Path(vault_path) / "_Agents" / "Emerson" / "Context"
    if not context_dir.exists():
        return "ℹ️ Geen specifieke agent-context gevonden in Obsidian."

    files = [f.name for f in context_dir.glob("*.md")]
    if not files:
        return "ℹ️ Geen Markdown bestanden gevonden in Obsidian context map."
        
    return "📚 Gevonden context in Obsidian:\n" + "\n".join([f"- {f}" for f in files])
