"""
Project Manager Agent - Specialist for project planning and management.

This agent handles all project management tasks including planning, tracking,
resource allocation, timeline management, and stakeholder communication.
"""

from src.agents.base_agent import BaseAgent


class ProjectManagerAgent(BaseAgent):
    """
    Project Manager agent responsible for project planning and execution.

    Handles sprint planning, resource allocation, timeline management,
    risk assessment, and stakeholder communication.
    """

    def __init__(self):
        system_prompt = """You are the Project Manager Agent for Emerson, a specialist in project planning and execution.

Your expertise includes:
1. **Project Planning**: Creating comprehensive project plans with clear objectives, scope, and deliverables
2. **Timeline Management**: Developing realistic timelines with milestones and dependencies
3. **Resource Allocation**: Assigning resources efficiently based on skills and availability
4. **Risk Assessment**: Identifying risks and developing mitigation strategies
5. **Stakeholder Communication**: Creating status reports and updates for all stakeholders
6. **Agile & Traditional Methods**: Proficient in both Agile (Scrum, Kanban) and Waterfall approaches

When creating project plans, always include:
- Executive Summary
- Project Objectives
- Scope (In-scope and Out-of-scope)
- Timeline with Milestones
- Resource Requirements
- Risk Register
- Success Criteria
- Communication Plan

Output Format:
- Use clear headers and sections
- Include tables for timelines and resources
- Provide actionable next steps
- Flag any blockers or dependencies

Example outputs:
- Project Plans (artifacts/plans/project_[name].md)
- Status Reports (artifacts/plans/status_[date].md)
- Risk Assessments (artifacts/plans/risks_[project].md)
- Resource Plans (artifacts/plans/resources_[project].md)"""

        super().__init__(role="project_manager", system_prompt=system_prompt)

    def create_project_plan(self, project_name: str, objectives: list, timeline_weeks: int) -> str:
        """
        Create a comprehensive project plan.

        Args:
            project_name: Name of the project.
            objectives: List of project objectives.
            timeline_weeks: Estimated timeline in weeks.

        Returns:
            Formatted project plan document.
        """
        prompt = f"""Create a comprehensive project plan for:

Project: {project_name}
Objectives:
{chr(10).join(f'- {obj}' for obj in objectives)}
Timeline: {timeline_weeks} weeks

Include all standard sections: Executive Summary, Objectives, Scope, Timeline with Milestones, Resources, Risks, and Success Criteria."""

        return self.execute(prompt)

    def create_status_report(self, project_name: str, progress: dict) -> str:
        """
        Create a project status report.

        Args:
            project_name: Name of the project.
            progress: Dictionary with progress information.

        Returns:
            Formatted status report.
        """
        prompt = f"""Create a project status report for:

Project: {project_name}
Progress Information:
{chr(10).join(f'- {k}: {v}' for k, v in progress.items())}

Include: Overall Status, Completed Items, In Progress, Upcoming Milestones, Blockers, and Next Steps."""

        return self.execute(prompt)

    def assess_risks(self, project_name: str, context: str) -> str:
        """
        Perform a risk assessment for a project.

        Args:
            project_name: Name of the project.
            context: Project context and current situation.

        Returns:
            Risk assessment document.
        """
        prompt = f"""Perform a comprehensive risk assessment for:

Project: {project_name}
Context: {context}

For each risk identified, provide:
- Risk Description
- Probability (High/Medium/Low)
- Impact (High/Medium/Low)
- Mitigation Strategy
- Owner
- Status"""

        return self.execute(prompt)
