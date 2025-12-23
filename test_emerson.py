from src.agent import GeminiAgent
import os
from dotenv import load_dotenv

load_dotenv()

def test_emerson():
    print("🚀 Start Emerson Agent Test...")
    agent = GeminiAgent()
    
    # Test 1: Daily Check (Read)
    print("\n--- Test 1: Dagelijkse Check ---")
    agent.run("Wat staat er vandaag op de planning?")
    
    # Test 2: Task Creation (Write + Escalation placeholder)
    print("\n--- Test 2: Taak Aanmaken ---")
    agent.run("Maak een taak 'Projectoverleg' voor project BZK")
    
    # Test 3: Budget Escalation (Escalation)
    print("\n--- Test 3: Budget Escalatie ---")
    agent.run("Boek €750 aan consultancy uren")

if __name__ == "__main__":
    if not os.getenv("NOTION_API_KEY"):
        print("❌ NOTION_API_KEY niet gevonden in omgeving.")
    else:
        test_emerson()
