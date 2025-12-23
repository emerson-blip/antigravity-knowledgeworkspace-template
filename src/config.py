import os
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class MCPServerConfig(BaseSettings):
    """Configuration for a single MCP server."""

    name: str = Field(description="Unique name for the MCP server")
    transport: str = Field(
        default="stdio", description="Transport type: stdio, http, sse"
    )
    command: Optional[str] = Field(
        default=None, description="Command to run for stdio transport"
    )
    args: List[str] = Field(
        default_factory=list, description="Arguments for the command"
    )
    url: Optional[str] = Field(default=None, description="URL for http/sse transport")
    env: dict = Field(
        default_factory=dict, description="Environment variables for the server"
    )
    enabled: bool = Field(default=True, description="Whether this server is enabled")

    model_config = SettingsConfigDict(extra="ignore")


class Settings(BaseSettings):
    """Application settings managed by Pydantic."""

    # Google GenAI Configuration
    GOOGLE_API_KEY: str = ""
    GEMINI_MODEL_NAME: str = "gemini-2.0-flash-exp"  # Default to latest

    # Agent Configuration
    AGENT_NAME: str = "AntigravityAgent"
    DEBUG_MODE: bool = False

    # External LLM (OpenAI-compatible) Configuration
    OPENAI_BASE_URL: str = Field(
        default="",
        description="Base URL for OpenAI-compatible API (e.g., https://api.openai.com/v1 or http://localhost:11434/v1)",
    )
    OPENAI_API_KEY: str = Field(
        default="",
        description="API key for OpenAI-compatible endpoint. Leave blank if not required.",
    )
    OPENAI_MODEL: str = Field(
        default="gpt-4o-mini",
        description="Default model name for OpenAI-compatible chat completions.",
    )

    # Memory Configuration
    MEMORY_FILE: str = "agent_memory.json"

    # MCP Configuration
    MCP_ENABLED: bool = Field(default=False, description="Enable MCP integration")
    MCP_SERVERS_CONFIG: str = Field(
        default="mcp_servers.json", description="Path to MCP servers configuration file"
    )
    MCP_CONNECTION_TIMEOUT: int = Field(
        default=30, description="Timeout in seconds for MCP server connections"
    )
    MCP_TOOL_PREFIX: str = Field(
        default="mcp_", description="Prefix for MCP tool names to avoid conflicts"
    )

    # Emerson Notion Configuration
    NOTION_API_KEY: str = Field(default="", description="Notion Integration Secret")
    NOTION_PROJECT_ID: str = Field(default="", description="The specific Notion Project ID for this workspace")
    NOTION_DATABASE_PROJECTS: str = "1ac354a7-949c-8138-82d8-000b3e8c983f"
    NOTION_DATABASE_TASKS: str = "1ac354a7-949c-814c-a640-000b8b50090a"
    NOTION_DATABASE_COMPANIES: str = "901d70b9-3c04-4a7a-9cc0-9761c04a7bbb"
    NOTION_DATABASE_PEOPLE: str = "4bae9ced-3184-4a9f-9896-59cc808931ce"
    NOTION_DATABASE_OFFERTES: str = "4c95c3fa-217a-4810-bc79-3c9996db14ff"
    NOTION_DATABASE_FACTUREN: str = "de1c2574-729a-4bda-899b-166f4da50094"
    NOTION_DATABASE_EVENTS: str = "1c5354a7-949c-8124-974a-000b5c38db4b"
    NOTION_DATABASE_LOGS: str = "197daeb1-7fbf-446d-a81b-b3ec716196be"
    NOTION_DATABASE_PROMPTS: str = "4384cf24-c692-413d-ba06-93c935cae521"

    # Obsidian Configuration
    OBSIDIAN_VAULT_PATH: str = Field(default="", description="The absolute path to the Obsidian Vault")

    # Escalation Settings
    BUDGET_THRESHOLD: float = 500.0
    CRITICAL_THRESHOLD: float = 2000.0

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


# Global settings instance
settings = Settings()
