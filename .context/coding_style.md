# Emerson Development Standards & Best Practices

## Architecture

### 1. Tool Isolation
All external interactions (API calls, file I/O, system commands) MUST be encapsulated in functions within the `src/tools/` directory.

**Why?** This allows agents to easily discover and use these capabilities as distinct tools.

### 2. Pydantic Everywhere
Use `pydantic` models for function arguments and return values where complex data is involved.

**Why?** This ensures strict schema validation and provides clear type definitions.

## Python Style

### 1. Type Hints
Mandatory for all function signatures:
```python
def create_project_plan(name: str, objectives: list[str]) -> dict:
```

### 2. Docstrings
Google-style docstrings are required:
```python
def analyze_market(industry: str, region: str) -> str:
    """Analyzes market conditions for a given industry and region.

    Args:
        industry: The industry sector to analyze.
        region: Geographic region for the analysis.

    Returns:
        A formatted market analysis report.

    Raises:
        ValueError: If industry or region is not recognized.
    """
```

**Why?** Agents use docstrings to understand how to use tools.

## Business Tool Design

### 1. Stateless Operations
Tools should be stateless. Pass necessary context as arguments.

### 2. Graceful Failure
Tools should return error messages or status codes rather than crashing:
```python
def get_project_status(project_id: str) -> dict:
    """Gets the current status of a project."""
    try:
        # Implementation
        return {"status": "success", "data": project_data}
    except ProjectNotFoundError:
        return {"status": "error", "message": f"Project {project_id} not found"}
```

### 3. Structured Outputs
Return structured data that can be easily processed:
```python
from pydantic import BaseModel

class ProjectStatus(BaseModel):
    project_id: str
    name: str
    status: str
    progress: float
    next_milestone: str | None
```

## Business Document Standards

### Project Plans
- Executive summary
- Objectives and scope
- Timeline with milestones
- Resource allocation
- Risk assessment
- Success criteria

### Research Reports
- Key findings (lead with insights)
- Methodology
- Data and analysis
- Recommendations
- Sources and references

### Product Specifications
- Problem statement
- Proposed solution
- Feature requirements
- User stories
- Acceptance criteria
- Technical considerations

### Client Deliverables
- Professional formatting
- Clear structure
- Actionable content
- Quality assurance checklist
