from src.agent import GeminiAgent
from src.config import settings

def list_projects():
    agent = GeminiAgent()
    print(f"🔍 Zoeken in database: {settings.NOTION_DATABASE_PROJECTS}")
    try:
        projects = agent.notion.list_projects()
        if not projects:
            print("ℹ️ Geen projecten gevonden.")
            return
        
        print("\n📂 Gevonden Projecten:")
        for p in projects[:5]:  # Laat er 5 zien
            print(f"- {p.name} (ID: {p.id}) [Status: {p.status}]")
    except Exception as e:
        print(f"❌ Fout bij ophalen projecten: {e}")

if __name__ == "__main__":
    list_projects()
