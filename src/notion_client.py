import logging
from typing import List, Optional, Dict, Any
from notion_client import Client
from src.config import settings
from src.models import Project, Task, Company, Invoice

logger = logging.getLogger(__name__)

class EmersonNotionClient:
    """Wrapper rond Notion API voor Emerson-specifieke operaties."""
    
    def __init__(self):
        self.client = Client(auth=settings.NOTION_API_KEY)
    
    # Core CRUD & Queries
    def get_project(self, project_id: str) -> Optional[Project]:
        """Haalt een specifiek project op."""
        try:
            page = self.client.pages.retrieve(page_id=project_id)
            props = page.get("properties", {})
            
            # Map Properties
            name_prop = props.get("Project name", {}).get("title", [{}])
            name = name_prop[0].get("plain_text", "Unknown") if name_prop else "Unknown"
            
            status_obj = props.get("Status", {}).get("status", {})
            status = status_obj.get("name", "Unknown")
            
            code_prop = props.get("Code", {}).get("rich_text", [{}])
            project_code = code_prop[0].get("plain_text") if code_prop else None
            
            return Project(
                id=page["id"],
                url=page["url"],
                name=name,
                status=status,
                project_code=project_code
            )
        except Exception as e:
            logger.error(f"Error fetching project {project_id}: {e}")
            return None

    def list_projects(self, status: str = None) -> List[Project]:
        """Haalt een lijst van projecten op, optioneel gefilterd op status."""
        query = {}
        if status:
            query["filter"] = {
                "property": "Status",
                "status": {"equals": status}
            }
        
        results = self.client.data_sources.query(data_source_id=settings.NOTION_DATABASE_PROJECTS, **query).get("results", [])
        projects = []
        for page in results:
            props = page.get("properties", {})
            name_prop = props.get("Project name", {}).get("title", [{}])
            name = name_prop[0].get("plain_text", "Unknown") if name_prop else "Unknown"
            
            status_obj = props.get("Status", {}).get("status", {})
            status = status_obj.get("name", "Unknown")
            
            code_prop = props.get("Code", {}).get("rich_text", [{}])
            project_code = code_prop[0].get("plain_text") if code_prop else None
            
            projects.append(Project(
                id=page["id"],
                url=page["url"],
                name=name,
                status=status,
                project_code=project_code
            ))
        return projects

    def create_task(self, project_id: str, title: str, **kwargs) -> Optional[Task]:
        """Maakt een nieuwe taak aan in Notion, gekoppeld aan een project."""
        properties = {
            "Name": {"title": [{"text": {"content": title}}]},
            "Project": {"relation": [{"id": project_id}]}
        }
        
        if "due_date" in kwargs and kwargs["due_date"]:
            properties["Due Date"] = {"date": {"start": kwargs["due_date"]}}
            
        try:
            new_page = self.client.pages.create(
                parent={"database_id": settings.NOTION_DATABASE_TASKS},
                properties=properties
            )
            return Task(
                id=new_page["id"],
                url=new_page["url"],
                title=title,
                status="To Do",
                project_id=project_id
            )
        except Exception as e:
            logger.error(f"Error creating task: {e}")
            return None

    def log_event(self, priority: str, event: str, details: Dict[str, Any]) -> None:
        """Logt een event naar de Agent Logs database."""
        try:
            self.client.pages.create(
                parent={"database_id": settings.NOTION_DATABASE_LOGS},
                properties={
                    "Event": {"title": [{"text": {"content": event}}]},
                    "Priority": {"select": {"name": priority}},
                    "Details": {"rich_text": [{"text": {"content": str(details)}}]}
                }
            )
        except Exception as e:
            logger.error(f"Error logging event to Notion: {e}")
