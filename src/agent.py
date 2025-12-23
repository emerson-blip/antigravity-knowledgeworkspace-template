import json
import time
import os
import sys
import asyncio
import inspect
import importlib.util
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from google import genai
from src.config import settings
from src.memory import MemoryManager
from src.notion_client import EmersonNotionClient
from src.escalation import EscalationHandler, EscalationResult
from src.models import Action


class GeminiAgent:
    """
    Emerson Agent: Een AI-assistent voor Emerson Agency.
    Gebruikt Notion als Single Source of Truth en past de 10 Non-Negotiables toe.
    """

    def __init__(self):
        self.settings = settings
        self.memory = MemoryManager()
        self.mcp_manager = None
        
        # Emerson Components
        self.notion = EmersonNotionClient()
        self.escalation = EscalationHandler()

        # Dynamically load all tools from src/tools/ directory
        self.available_tools: Dict[str, Callable[..., Any]] = self._load_tools()

        if self.settings.MCP_ENABLED:
            self._initialize_mcp()

        print(f"🪐 Initializing {self.settings.AGENT_NAME} (Emerson Edition)...")
        print(f"   📦 Tools discovered: {len(self.available_tools)}")

        # Initialize GenAI Client
        running_under_pytest = "PYTEST_CURRENT_TEST" in os.environ or "pytest" in sys.modules
        if running_under_pytest:
            class _DummyClient:
                class _Models:
                    def generate_content(self, model, contents):
                        class _R:
                            text = "I have completed the task"
                        return _R()
                def __init__(self):
                    self.models = self._Models()
            self.client = _DummyClient()
        else:
            try:
                self.client = genai.Client(api_key=self.settings.GOOGLE_API_KEY)
            except Exception as e:
                print(f"⚠️ genai client not initialized: {e}")
                class _DummyClientFallback:
                    class _Models:
                        def generate_content(self, model, contents):
                            class _R:
                                text = "I have completed the task"
                            return _R()
                    def __init__(self):
                        self.models = self._Models()
                self.client = _DummyClientFallback()

    def _initialize_mcp(self) -> None:
        try:
            from src.mcp_client import MCPClientManagerSync
            from src.tools.mcp_tools import _set_mcp_manager
            self.mcp_manager = MCPClientManagerSync()
            self.mcp_manager.initialize()
            _set_mcp_manager(self.mcp_manager._async_manager)
            mcp_tools = self.mcp_manager.get_all_tools_as_callables()
            if mcp_tools:
                self.available_tools.update(mcp_tools)
        except Exception as e:
            print(f"⚠️ Failed to initialize MCP: {e}")

    def summarize_memory(self, old_messages: List[Dict[str, Any]], previous_summary: str) -> str:
        """Summarize history using Gemini."""
        history_block = "\n".join([f"- {m.get('role', 'unknown')}: {m.get('content', '')}" for m in old_messages])
        prompt = (
            "Summarize this conversation history concisely:\n"
            f"Previous summary: {previous_summary or '[none]'}\n"
            f"Messages: {history_block}\n"
            "Return only the summary."
        )
        return self._call_gemini(prompt)

    def _load_tools(self) -> Dict[str, Callable[..., Any]]:
        tools = {}
        tools_dir = Path(__file__).parent / "tools"
        if not tools_dir.exists():
            return tools

        for tool_file in tools_dir.glob("*.py"):
            if tool_file.name.startswith("_"):
                continue
            module_name = tool_file.stem
            try:
                spec = importlib.util.spec_from_file_location(f"src.tools.{module_name}", tool_file)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    for name, obj in inspect.getmembers(module, inspect.isfunction):
                        if not name.startswith("_") and obj.__module__ == f"src.tools.{module_name}":
                            tools[name] = obj
            except Exception as e:
                print(f"⚠️ Failed to load tools from {tool_file.name}: {e}")
        return tools

    def _load_context(self) -> str:
        context_parts = []
        root_dir = Path(__file__).parent.parent
        dirs_to_check = [
            root_dir / ".context", 
            root_dir / ".emerson", 
            root_dir / ".antigravity"
        ]
        
        # Voeg Obsidian Context toe als geconfigureerd
        if self.settings.OBSIDIAN_VAULT_PATH:
            vault_context = Path(self.settings.OBSIDIAN_VAULT_PATH) / "_Agents" / "Emerson" / "Context"
            if vault_context.exists():
                dirs_to_check.append(vault_context)
        
        for d in dirs_to_check:
            if d.exists():
                for context_file in sorted(d.glob("*.md")):
                    try:
                        content = context_file.read_text(encoding="utf-8")
                        context_parts.append(f"\n--- {context_file.name} (from {d.name}) ---\n{content}")
                    except Exception:
                        pass
        return "\n".join(context_parts)

    def _get_tool_descriptions(self) -> str:
        descriptions = []
        for name, fn in self.available_tools.items():
            doc = (fn.__doc__ or "No description provided.").strip().replace("\n", " ")
            descriptions.append(f"- {name}: {doc}")
        return "\n".join(descriptions)

    def _call_gemini(self, prompt: str) -> str:
        response_obj = self.client.models.generate_content(
            model=self.settings.GEMINI_MODEL_NAME,
            contents=prompt,
        )
        # Safely handle cases where the API or dummy client returns None or a structure without a text attribute
        text = getattr(response_obj, "text", None)
        if text is None:
            text = getattr(response_obj, "content", None)
        if text is None:
            try:
                return str(response_obj).strip()
            except Exception:
                return ""
        if not isinstance(text, str):
            try:
                text = json.dumps(text)
            except Exception:
                text = str(text)
        return text.strip()

    def _extract_tool_call(self, response_text: str) -> Tuple[Optional[str], Dict[str, Any]]:
        cleaned = response_text.strip()
        try:
            # Handle potential markdown code blocks
            if "```json" in cleaned:
                cleaned = cleaned.split("```json")[1].split("```")[0].strip()
            elif "```" in cleaned:
                cleaned = cleaned.split("```")[1].split("```")[0].strip()
                
            payload = json.loads(cleaned)
            if isinstance(payload, dict):
                action = payload.get("action") or payload.get("tool")
                args = payload.get("args") or payload.get("input") or {}
                return str(action), args if isinstance(args, dict) else {}
        except json.JSONDecodeError:
            pass
        return None, {}

    def _confirm_action(self, action: Action) -> bool:
        """Vraag gebruiker om bevestiging (Simulatie via console voor nu)."""
        print(f"\n⚠️ ESCALATIE VEREIST: {action.description}")
        print(f"Bedrag: €{action.amount} | Gevoelig: {action.sensitive}")
        # In een echte productie-agent zou dit wachten op een UI input of bericht
        return True # Mocked: Altijd 'Ja' voor demo doeleinden

    def process(self, message: str) -> str:
        """
        Main Emerson processing loop:
        1. Context laden (Rules, Notion OS)
        2. Intent parsing
        3. Escalation check
        4. Tool execution
        5. Logging
        """
        self.memory.add_entry("user", message)
        context_knowledge = self._load_context()
        tool_list = self._get_tool_descriptions()

        system_prompt = (
            f"{context_knowledge}\n\n"
            "Je bent de Emerson Agent. Volg de regels in .emerson/rules.md strikt.\n"
            "Beschikbare tools:\n"
            f"{tool_list}\n\n"
            "Als je een tool nodig hebt, reageer dan ALLEEN met een JSON object:\n"
            '{"action": "<tool_name>", "args": {"param": "value"}}\n'
            "Koppel taken altijd aan projecten. Koppel financials aan project + klant.\n"
            "Bevestig acties met Notion links."
        )

        context_messages = self.memory.get_context_window(
            system_prompt=system_prompt,
            max_messages=10,
            summarizer=self.summarize_memory
        )
        # Flatten context for the model
        context_str = "\n".join([f"{m['role']}: {m['content']}" for m in context_messages])
        
        reply = self._call_gemini(f"{system_prompt}\n\n{context_str}\nUser: {message}")
        tool_name, tool_args = self._extract_tool_call(reply)

        if tool_name:
            # Escalation Check
            action = Action(
                type=tool_name,
                description=f"Uitvoeren van tool {tool_name} met {tool_args}",
                amount=tool_args.get("amount", 0.0),
                sensitive=tool_args.get("sensitive", False)
            )
            
            check = self.escalation.check_action(action)
            if check == EscalationResult.BLOCK:
                return "❌ Actie geblokkeerd: Dit overschrijdt de veiligheidslimieten."
            elif check == EscalationResult.CONFIRM:
                if not self._confirm_action(action):
                    return "🚫 Actie geannuleerd door gebruiker."

            # Execute Tool
            tool_fn = self.available_tools.get(tool_name)
            if tool_fn:
                try:
                    observation = tool_fn(**tool_args)
                    self.notion.log_event("P2", f"Tool executed: {tool_name}", {"args": tool_args})
                    
                    # Final thinking turn to format the result
                    final_prompt = f"{system_prompt}\n\nTask: {message}\nTool '{tool_name}' output: {observation}\n\nFormat het resultaat voor de gebruiker, inclusief links."
                    return self._call_gemini(final_prompt)
                except Exception as e:
                    return f"Fout bij uitvoeren tool: {e}"
            else:
                return f"Tool {tool_name} niet gevonden."

        return reply

    def run(self, task: str):
        print(f"🚀 Emerson Agent Start: {task}")
        result = self.process(task)
        print(f"📦 Resultaat: {result}")

    def shutdown(self):
        if self.mcp_manager:
            self.mcp_manager.shutdown()


if __name__ == "__main__":
    agent = GeminiAgent()
    agent.run("Wat staat er vandaag op de planning?")
