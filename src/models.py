from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class NotionBase(BaseModel):
    """Base class for Notion objects."""
    id: str
    url: str

class Project(NotionBase):
    """Pydantic model for a Project from Notion."""
    name: str
    status: str
    project_code: Optional[str] = None
    company_id: Optional[str] = None
    financials: Optional[Dict[str, Any]] = None

    @property
    def short_id(self) -> str:
        """Returns project_code if set, otherwise tries to extract it from the name."""
        if self.project_code:
            return self.project_code.upper()
        
        # Fallback: probeer een patroon als 'PRO-123' of 'AAA-001' uit de naam te halen
        import re
        match = re.search(r'([A-Z]{2,}-\d+)', self.name)
        if match:
            return match.group(1).upper()
            
        return self.name[:4].upper()

class Task(NotionBase):
    """Pydantic model for a Task from Notion."""
    title: str
    status: str
    project_id: Optional[str] = None
    due_date: Optional[datetime] = None

class Company(NotionBase):
    """Pydantic model for a Company/CRM entry."""
    name: str
    type: str # Prospect, Qualified, Client, Partner
    projects: List[str] = []

class Invoice(NotionBase):
    """Pydantic model for an Invoice."""
    amount: float
    status: str
    project_id: str

class Action(BaseModel):
    """Represents an action for escalation checking."""
    type: str
    description: str
    amount: Optional[float] = 0.0
    sensitive: bool = False
