"""
Business Tools for Emerson AI Workspace.

This module provides tools for business operations including project management,
research, product development, and service delivery.
"""

from datetime import datetime
from typing import Optional
import json
import os


# =============================================================================
# Project Management Tools
# =============================================================================

def create_project_artifact(
    project_name: str,
    artifact_type: str,
    content: str
) -> str:
    """Creates a project artifact file in the artifacts directory.

    Args:
        project_name: Name of the project.
        artifact_type: Type of artifact (plan, status, risk, resource).
        content: Content to write to the artifact.

    Returns:
        Path to the created artifact file.
    """
    # Ensure directory exists
    artifact_dir = "artifacts/plans"
    os.makedirs(artifact_dir, exist_ok=True)

    # Create filename
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"{artifact_type}_{project_name.lower().replace(' ', '_')}_{timestamp}.md"
    filepath = os.path.join(artifact_dir, filename)

    # Write content
    with open(filepath, 'w') as f:
        f.write(content)

    return f"Artifact created: {filepath}"


def get_project_template(template_type: str) -> str:
    """Returns a project document template.

    Args:
        template_type: Type of template (project_plan, status_report, risk_assessment).

    Returns:
        Template content as a string.
    """
    templates = {
        "project_plan": """# Project Plan: [Project Name]

## Executive Summary
[Brief overview of the project]

## Objectives
- [ ] Objective 1
- [ ] Objective 2
- [ ] Objective 3

## Scope
### In Scope
- Item 1
- Item 2

### Out of Scope
- Item 1
- Item 2

## Timeline
| Milestone | Target Date | Status |
|-----------|-------------|--------|
| Kickoff   | [Date]      | [ ]    |
| Phase 1   | [Date]      | [ ]    |
| Phase 2   | [Date]      | [ ]    |
| Launch    | [Date]      | [ ]    |

## Resources
| Role | Name | Allocation |
|------|------|------------|
| PM   | TBD  | 100%       |

## Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| TBD  | Medium      | High   | TBD        |

## Success Criteria
1. Criteria 1
2. Criteria 2
""",
        "status_report": """# Status Report: [Project Name]
**Date:** [Date]
**Reporter:** [Name]

## Overall Status: [Green/Yellow/Red]

## Summary
[Brief summary of progress]

## Completed This Period
- [ ] Item 1
- [ ] Item 2

## In Progress
- [ ] Item 1 (X% complete)
- [ ] Item 2 (X% complete)

## Upcoming
- [ ] Item 1
- [ ] Item 2

## Blockers
- None / [List blockers]

## Risks & Issues
| Item | Status | Action |
|------|--------|--------|
| TBD  | Open   | TBD    |

## Next Steps
1. Step 1
2. Step 2
""",
        "risk_assessment": """# Risk Assessment: [Project Name]
**Date:** [Date]
**Assessor:** [Name]

## Risk Register

| ID | Risk | Category | Probability | Impact | Score | Mitigation | Owner | Status |
|----|------|----------|-------------|--------|-------|------------|-------|--------|
| R1 | TBD  | Technical | High        | High   | 9     | TBD        | TBD   | Open   |

## Risk Matrix

|            | Low Impact | Medium Impact | High Impact |
|------------|------------|---------------|-------------|
| High Prob  |            |               | R1          |
| Med Prob   |            |               |             |
| Low Prob   |            |               |             |

## Top Risks
1. **R1**: [Description and mitigation plan]

## Recommendations
1. Recommendation 1
2. Recommendation 2
"""
    }

    return templates.get(template_type, f"Template '{template_type}' not found. Available: {list(templates.keys())}")


# =============================================================================
# Research Tools
# =============================================================================

def create_research_artifact(
    topic: str,
    research_type: str,
    content: str
) -> str:
    """Creates a research artifact file in the artifacts directory.

    Args:
        topic: Topic of the research.
        research_type: Type of research (market, competitive, insights, tech).
        content: Content to write to the artifact.

    Returns:
        Path to the created artifact file.
    """
    # Ensure directory exists
    artifact_dir = "artifacts/research"
    os.makedirs(artifact_dir, exist_ok=True)

    # Create filename
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"{research_type}_{topic.lower().replace(' ', '_')}_{timestamp}.md"
    filepath = os.path.join(artifact_dir, filename)

    # Write content
    with open(filepath, 'w') as f:
        f.write(content)

    return f"Research artifact created: {filepath}"


def get_research_template(template_type: str) -> str:
    """Returns a research document template.

    Args:
        template_type: Type of template (market_research, competitive_analysis, swot).

    Returns:
        Template content as a string.
    """
    templates = {
        "market_research": """# Market Research: [Topic]
**Date:** [Date]
**Analyst:** [Name]

## Executive Summary
[Key findings in 2-3 sentences]

## Methodology
- Data sources used
- Research approach
- Limitations

## Market Overview
### Market Size
- Current: $X
- Projected: $X by [Year]
- CAGR: X%

### Key Segments
1. Segment 1
2. Segment 2

## Key Players
| Company | Market Share | Strengths | Weaknesses |
|---------|-------------|-----------|------------|
| TBD     | X%          | TBD       | TBD        |

## Trends
1. **Trend 1**: [Description]
2. **Trend 2**: [Description]

## Opportunities
1. Opportunity 1
2. Opportunity 2

## Challenges
1. Challenge 1
2. Challenge 2

## Recommendations
1. Recommendation 1
2. Recommendation 2

## Sources
- Source 1
- Source 2
""",
        "competitive_analysis": """# Competitive Analysis: [Company/Product]
**Date:** [Date]
**Analyst:** [Name]

## Executive Summary
[Key findings in 2-3 sentences]

## Competitors Analyzed
1. Competitor 1
2. Competitor 2
3. Competitor 3

## Feature Comparison
| Feature | Us | Comp 1 | Comp 2 | Comp 3 |
|---------|-----|--------|--------|--------|
| Feature 1 | Yes | Yes | No | Yes |
| Feature 2 | Yes | No | Yes | Yes |

## Pricing Comparison
| Tier | Us | Comp 1 | Comp 2 | Comp 3 |
|------|-----|--------|--------|--------|
| Basic | $X | $X | $X | $X |
| Pro | $X | $X | $X | $X |

## Competitor Profiles

### Competitor 1
- **Strengths**:
- **Weaknesses**:
- **Strategy**:

## Positioning Map
[Description of market positioning]

## Strategic Recommendations
1. Recommendation 1
2. Recommendation 2
""",
        "swot": """# SWOT Analysis: [Subject]
**Date:** [Date]
**Analyst:** [Name]

## Strengths (Internal, Positive)
1. Strength 1
2. Strength 2
3. Strength 3

## Weaknesses (Internal, Negative)
1. Weakness 1
2. Weakness 2
3. Weakness 3

## Opportunities (External, Positive)
1. Opportunity 1
2. Opportunity 2
3. Opportunity 3

## Threats (External, Negative)
1. Threat 1
2. Threat 2
3. Threat 3

## Strategic Implications

### SO Strategies (Use Strengths to Capture Opportunities)
1. Strategy 1

### WO Strategies (Overcome Weaknesses Using Opportunities)
1. Strategy 1

### ST Strategies (Use Strengths to Avoid Threats)
1. Strategy 1

### WT Strategies (Minimize Weaknesses and Avoid Threats)
1. Strategy 1
"""
    }

    return templates.get(template_type, f"Template '{template_type}' not found. Available: {list(templates.keys())}")


# =============================================================================
# Product Development Tools
# =============================================================================

def create_product_artifact(
    product_name: str,
    artifact_type: str,
    content: str
) -> str:
    """Creates a product artifact file in the artifacts directory.

    Args:
        product_name: Name of the product.
        artifact_type: Type of artifact (roadmap, mvp, feature, stories).
        content: Content to write to the artifact.

    Returns:
        Path to the created artifact file.
    """
    # Ensure directory exists
    artifact_dir = "artifacts/plans"
    os.makedirs(artifact_dir, exist_ok=True)

    # Create filename
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"{artifact_type}_{product_name.lower().replace(' ', '_')}_{timestamp}.md"
    filepath = os.path.join(artifact_dir, filename)

    # Write content
    with open(filepath, 'w') as f:
        f.write(content)

    return f"Product artifact created: {filepath}"


def get_product_template(template_type: str) -> str:
    """Returns a product document template.

    Args:
        template_type: Type of template (roadmap, mvp, feature_spec, user_story).

    Returns:
        Template content as a string.
    """
    templates = {
        "roadmap": """# Product Roadmap: [Product Name]
**Version:** 1.0
**Last Updated:** [Date]

## Vision
[Product vision statement]

## Strategic Themes
1. Theme 1
2. Theme 2
3. Theme 3

## Roadmap Overview

### Q1 [Year]
**Theme:** [Focus area]
- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3

### Q2 [Year]
**Theme:** [Focus area]
- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3

### Q3 [Year]
**Theme:** [Focus area]
- [ ] Feature 1
- [ ] Feature 2

### Q4 [Year]
**Theme:** [Focus area]
- [ ] Feature 1
- [ ] Feature 2

## Success Metrics
| Metric | Current | Q1 Target | Q2 Target | Q3 Target | Q4 Target |
|--------|---------|-----------|-----------|-----------|-----------|
| Metric 1 | X | X | X | X | X |

## Dependencies
- Dependency 1
- Dependency 2

## Risks
- Risk 1
- Risk 2
""",
        "mvp": """# MVP Definition: [Product Name]
**Date:** [Date]
**Author:** [Name]

## Problem Statement
[What problem are we solving?]

## Target Users
[Who are we building for?]

## Proposed Solution
[High-level description of the solution]

## MVP Scope

### Must Have (Core MVP)
1. Feature 1
2. Feature 2
3. Feature 3

### Should Have (Post-MVP Phase 1)
1. Feature 1
2. Feature 2

### Could Have (Future)
1. Feature 1
2. Feature 2

### Won't Have (Out of Scope)
1. Feature 1
2. Feature 2

## User Flows
1. **Flow 1**: [Description]
2. **Flow 2**: [Description]

## Launch Criteria
- [ ] Criteria 1
- [ ] Criteria 2
- [ ] Criteria 3

## Validation Approach
1. How will we validate success?
2. What metrics will we track?

## Technical Considerations
- Consideration 1
- Consideration 2
""",
        "feature_spec": """# Feature Specification: [Feature Name]
**Version:** 1.0
**Date:** [Date]
**Author:** [Name]

## Overview
[Brief description of the feature]

## Problem Statement
[What problem does this feature solve?]

## User Stories

### Story 1
**As a** [user type]
**I want** [goal]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] Criteria 1
- [ ] Criteria 2

## Functional Requirements
1. Requirement 1
2. Requirement 2
3. Requirement 3

## Non-Functional Requirements
1. Performance: [requirements]
2. Security: [requirements]
3. Accessibility: [requirements]

## UI/UX Considerations
- Consideration 1
- Consideration 2

## Technical Design
[High-level technical approach]

## Dependencies
- Dependency 1
- Dependency 2

## Risks
| Risk | Mitigation |
|------|------------|
| Risk 1 | Mitigation 1 |

## Success Metrics
- Metric 1
- Metric 2
""",
        "user_story": """# User Story: [Title]
**ID:** US-XXX
**Epic:** [Epic Name]
**Priority:** [High/Medium/Low]
**Points:** [X]

## User Story
**As a** [user type]
**I want** [goal/desire]
**So that** [benefit/value]

## Acceptance Criteria

### Scenario 1: [Happy Path]
**Given** [context]
**When** [action]
**Then** [expected result]

### Scenario 2: [Edge Case]
**Given** [context]
**When** [action]
**Then** [expected result]

## Technical Notes
- Note 1
- Note 2

## Design Assets
- [Link to design]

## Dependencies
- Dependency 1

## Questions/Assumptions
- Question 1
- Assumption 1
"""
    }

    return templates.get(template_type, f"Template '{template_type}' not found. Available: {list(templates.keys())}")


# =============================================================================
# Delivery Tools
# =============================================================================

def create_deliverable_artifact(
    client_name: str,
    deliverable_type: str,
    content: str
) -> str:
    """Creates a deliverable artifact file in the artifacts directory.

    Args:
        client_name: Name of the client.
        deliverable_type: Type of deliverable (report, proposal, documentation, handoff).
        content: Content to write to the artifact.

    Returns:
        Path to the created artifact file.
    """
    # Ensure directory exists
    artifact_dir = "artifacts/deliverables"
    os.makedirs(artifact_dir, exist_ok=True)

    # Create filename
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"{deliverable_type}_{client_name.lower().replace(' ', '_')}_{timestamp}.md"
    filepath = os.path.join(artifact_dir, filename)

    # Write content
    with open(filepath, 'w') as f:
        f.write(content)

    return f"Deliverable created: {filepath}"


def get_deliverable_template(template_type: str) -> str:
    """Returns a deliverable document template.

    Args:
        template_type: Type of template (proposal, report, handoff).

    Returns:
        Template content as a string.
    """
    templates = {
        "proposal": """# Proposal: [Project Name]
**Prepared for:** [Client Name]
**Prepared by:** Emerson
**Date:** [Date]

---

## Executive Summary
[Brief overview of the proposal]

## Understanding Your Needs
[Demonstrate understanding of client's situation and requirements]

## Proposed Solution
[Overview of what we're proposing]

## Scope of Work

### Phase 1: [Name]
- Deliverable 1
- Deliverable 2

### Phase 2: [Name]
- Deliverable 1
- Deliverable 2

## Deliverables
| # | Deliverable | Description | Timeline |
|---|-------------|-------------|----------|
| 1 | TBD | TBD | Week X |

## Timeline
[Overall timeline with key milestones]

## Team
| Role | Responsibilities |
|------|-----------------|
| Role 1 | TBD |

## Investment
| Item | Cost |
|------|------|
| Phase 1 | $X |
| Phase 2 | $X |
| **Total** | **$X** |

## Terms & Conditions
[Key terms]

## Next Steps
1. Step 1
2. Step 2
3. Step 3

---
**Contact:** [Contact information]
""",
        "report": """# [Report Title]
**Prepared for:** [Client Name]
**Prepared by:** Emerson
**Date:** [Date]

---

## Executive Summary
[Key findings and recommendations in 2-3 paragraphs]

## Introduction
[Context and purpose of this report]

## Methodology
[How the work was conducted]

## Findings

### Finding 1: [Title]
[Details and supporting data]

### Finding 2: [Title]
[Details and supporting data]

### Finding 3: [Title]
[Details and supporting data]

## Analysis
[Interpretation of findings]

## Recommendations

### Recommendation 1
**Priority:** High/Medium/Low
[Details]

### Recommendation 2
**Priority:** High/Medium/Low
[Details]

## Next Steps
1. Step 1
2. Step 2
3. Step 3

## Appendices
### Appendix A: [Title]
[Supporting materials]

---
**Contact:** [Contact information]
""",
        "handoff": """# Project Handoff: [Project Name]
**Client:** [Client Name]
**Date:** [Date]
**Prepared by:** Emerson

---

## Project Summary
[Brief overview of the project and outcomes]

## Deliverables Checklist
- [ ] Deliverable 1
- [ ] Deliverable 2
- [ ] Deliverable 3
- [ ] Documentation
- [ ] Training materials

## Documentation Index
| Document | Location | Description |
|----------|----------|-------------|
| Doc 1 | [Link] | TBD |
| Doc 2 | [Link] | TBD |

## Access & Credentials
| System | Access Type | Notes |
|--------|-------------|-------|
| System 1 | [Details] | TBD |

*Note: Credentials shared separately via secure channel*

## Knowledge Transfer

### Key Processes
1. Process 1: [Description]
2. Process 2: [Description]

### Common Tasks
1. Task 1: [How to do it]
2. Task 2: [How to do it]

## Support Information

### Support Period
- Duration: [X weeks/months]
- Scope: [What's covered]

### Contact Information
| Contact | Role | Email | Phone |
|---------|------|-------|-------|
| TBD | Primary | TBD | TBD |

## FAQs
**Q: [Question 1]**
A: [Answer]

**Q: [Question 2]**
A: [Answer]

## Sign-off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Client Representative | | | |
| Project Lead | | | |

---
**Thank you for working with Emerson!**
"""
    }

    return templates.get(template_type, f"Template '{template_type}' not found. Available: {list(templates.keys())}")


# =============================================================================
# Utility Tools
# =============================================================================

def list_artifacts(artifact_type: Optional[str] = None) -> str:
    """Lists all artifacts in the artifacts directory.

    Args:
        artifact_type: Optional filter by type (plans, research, deliverables, logs).

    Returns:
        List of artifact files.
    """
    base_dir = "artifacts"
    results = []

    if artifact_type:
        dirs_to_check = [os.path.join(base_dir, artifact_type)]
    else:
        dirs_to_check = [
            os.path.join(base_dir, d)
            for d in ["plans", "research", "deliverables", "logs"]
        ]

    for dir_path in dirs_to_check:
        if os.path.exists(dir_path):
            files = os.listdir(dir_path)
            for f in files:
                if f.endswith('.md'):
                    results.append(os.path.join(dir_path, f))

    if not results:
        return "No artifacts found."

    return "Artifacts:\n" + "\n".join(f"- {r}" for r in sorted(results))


def log_activity(activity: str, details: str) -> str:
    """Logs an activity to the logs directory.

    Args:
        activity: Type of activity (e.g., "research", "meeting", "decision").
        details: Details of the activity.

    Returns:
        Confirmation message.
    """
    # Ensure directory exists
    log_dir = "artifacts/logs"
    os.makedirs(log_dir, exist_ok=True)

    # Create log entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_str = datetime.now().strftime("%Y%m%d")
    log_file = os.path.join(log_dir, f"activity_log_{date_str}.md")

    entry = f"\n## [{timestamp}] {activity}\n{details}\n"

    # Append to log file
    mode = 'a' if os.path.exists(log_file) else 'w'
    with open(log_file, mode) as f:
        if mode == 'w':
            f.write(f"# Activity Log - {datetime.now().strftime('%Y-%m-%d')}\n")
        f.write(entry)

    return f"Activity logged: {activity}"
