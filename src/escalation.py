from enum import Enum
from typing import Optional
from src.models import Action

class EscalationResult(Enum):
    PROCEED = "PROCEED"
    CONFIRM = "CONFIRM"
    BLOCK = "BLOCK"

class EscalationHandler:
    """Implementeert de 10 Non-Negotiables en budgetlimitaties."""
    
    BUDGET_THRESHOLD = 500.0
    CRITICAL_THRESHOLD = 2000.0
    
    def check_action(self, action: Action) -> EscalationResult:
        """
        Controleert of een actie mag worden uitgevoerd op basis van regels.
        """
        # 1. Budget check
        if action.amount > self.CRITICAL_THRESHOLD:
            return EscalationResult.BLOCK
        
        if action.amount > self.BUDGET_THRESHOLD:
            return EscalationResult.CONFIRM
            
        # 2. Gevoeligheid check
        if action.sensitive:
            return EscalationResult.CONFIRM
            
        # 3. Type check (placeholder voor NEVER regels)
        if action.type in ["BANK_TRANSFER", "DELETE_DATABASE"]:
            return EscalationResult.BLOCK
            
        return EscalationResult.PROCEED
    
    def requires_confirmation(self, action: Action) -> bool:
        """Helper methode om te checken of bevestiging nodig is."""
        return self.check_action(action) == EscalationResult.CONFIRM
