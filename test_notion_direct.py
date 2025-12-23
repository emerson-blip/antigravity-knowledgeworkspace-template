from src.notion_client import EmersonNotionClient
from dotenv import load_dotenv
import os

load_dotenv()

def test_notion_direct():
    print("🔌 Testing EmersonNotionClient direct...")
    client = EmersonNotionClient()
    
    try:
        # 1. Test Query Projects
        print("🔍 Querying projects...")
        projects = client.list_projects()
        print(f"✅ Found {len(projects)} projects.")
        for p in projects[:3]:
            print(f"   - {p.name} ({p.status})")
            
        # 2. Test Logging
        print("📝 Testing event logging...")
        client.log_event("P2", "Direct Client Test", {"status": "success"})
        print("✅ Event logged successfully.")
        
    except Exception as e:
        print(f"❌ Error during direct Notion test: {e}")

if __name__ == "__main__":
    test_notion_direct()
