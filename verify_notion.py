import asyncio
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from src.mcp_client import MCPClientManager
from src.config import settings

async def main():
    print(f"Checking MCP status (Enabled: {settings.MCP_ENABLED})...")
    
    manager = MCPClientManager()
    await manager.initialize()
    
    status = manager.get_status()
    print("\nMCP Status:")
    for name, info in status.get("servers", {}).items():
        conn = "✅" if info["connected"] else "❌"
        print(f"  - {name}: {conn} ({info['tools_count']} tools)")
        if info.get("error"):
            print(f"    Error: {info['error']}")
            
    if "notion" in manager.servers and manager.servers["notion"].connected:
        print("\nNotion Tools Discovered:")
        tools = manager.get_all_tools()
        notion_tools = [t for t in tools if t.server_name == "notion"]
        for tool in notion_tools:
            print(f"  • {tool.name}")
        
        print("\n✅ Notion MCP verification successful!")
    else:
        print("\n❌ Notion MCP verification failed.")
        
    await manager.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
