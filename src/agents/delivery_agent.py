"""
Delivery Agent - Specialist for service delivery and client management.

This agent handles client deliverables, documentation, quality assurance,
client communication, and handoff management.
"""

from src.agents.base_agent import BaseAgent


class DeliveryAgent(BaseAgent):
    """
    Delivery agent responsible for service delivery and client management.

    Handles deliverable preparation, documentation, quality assurance,
    client communication, and handoff management.
    """

    def __init__(self):
        system_prompt = """You are the Delivery Agent for Emerson, a specialist in service delivery and client management.

Your expertise includes:
1. **Deliverable Management**: Creating, tracking, and quality-checking client deliverables
2. **Documentation**: Technical documentation, user guides, process documentation
3. **Quality Assurance**: Review checklists, quality standards, sign-off procedures
4. **Client Communication**: Proposals, reports, presentations, status updates
5. **Handoff Management**: Transition planning, knowledge transfer, support documentation

When creating deliverables, always:
- Ensure professional, polished presentation
- Include executive summary for business stakeholders
- Provide clear structure and navigation
- Add quality assurance checklist
- Include next steps and recommendations

Output Format:
- Professional formatting suitable for clients
- Clear headers and sections
- Executive summary at the top
- Actionable recommendations
- Appendices for supporting details

Example outputs:
- Client Reports (artifacts/deliverables/report_[client]_[topic].md)
- Proposals (artifacts/deliverables/proposal_[client].md)
- Documentation (artifacts/deliverables/docs_[topic].md)
- Handoff Packages (artifacts/deliverables/handoff_[project].md)"""

        super().__init__(role="delivery", system_prompt=system_prompt)

    def create_client_report(self, client_name: str, report_type: str, content: dict) -> str:
        """
        Create a client-facing report.

        Args:
            client_name: Name of the client.
            report_type: Type of report (e.g., "Status", "Analysis", "Recommendation").
            content: Dictionary with report content.

        Returns:
            Formatted client report.
        """
        prompt = f"""Create a professional {report_type} report for {client_name}:

Content to include:
{chr(10).join(f'- {k}: {v}' for k, v in content.items())}

Format as a polished, client-ready document with:
- Executive Summary
- Key Findings/Status
- Detailed Sections
- Recommendations
- Next Steps"""

        return self.execute(prompt)

    def create_proposal(self, client_name: str, project_scope: str, objectives: list) -> str:
        """
        Create a client proposal.

        Args:
            client_name: Name of the client.
            project_scope: Scope of the proposed work.
            objectives: List of project objectives.

        Returns:
            Formatted proposal document.
        """
        prompt = f"""Create a professional proposal for {client_name}:

Project Scope: {project_scope}

Objectives:
{chr(10).join(f'- {obj}' for obj in objectives)}

Include:
- Executive Summary
- Understanding of Client Needs
- Proposed Approach
- Scope of Work
- Deliverables
- Timeline
- Team and Resources
- Investment Summary
- Terms and Conditions
- Next Steps"""

        return self.execute(prompt)

    def create_documentation(self, doc_type: str, topic: str, audience: str) -> str:
        """
        Create documentation.

        Args:
            doc_type: Type of documentation (e.g., "Technical", "User Guide", "Process").
            topic: Topic of the documentation.
            audience: Target audience for the documentation.

        Returns:
            Documentation document.
        """
        prompt = f"""Create {doc_type} documentation for:

Topic: {topic}
Target Audience: {audience}

Include appropriate sections for {doc_type.lower()} documentation. Ensure:
- Clear and accessible language for the target audience
- Step-by-step instructions where applicable
- Visual aids descriptions (diagrams, screenshots) where helpful
- Troubleshooting section if applicable
- Glossary of terms if technical"""

        return self.execute(prompt)

    def create_handoff_package(self, project_name: str, client_name: str, deliverables: list) -> str:
        """
        Create a project handoff package.

        Args:
            project_name: Name of the project.
            client_name: Name of the client.
            deliverables: List of deliverables to hand off.

        Returns:
            Handoff package document.
        """
        prompt = f"""Create a handoff package for:

Project: {project_name}
Client: {client_name}

Deliverables:
{chr(10).join(f'- {d}' for d in deliverables)}

Include:
- Project Summary
- Deliverables Checklist
- Documentation Index
- Access and Credentials (placeholder)
- Knowledge Transfer Notes
- Support Information
- FAQs
- Sign-off Section"""

        return self.execute(prompt)

    def quality_review(self, deliverable_type: str, content: str) -> str:
        """
        Perform a quality review of a deliverable.

        Args:
            deliverable_type: Type of deliverable to review.
            content: Content to review.

        Returns:
            Quality review report with recommendations.
        """
        prompt = f"""Perform a quality review of this {deliverable_type}:

{content}

Review for:
- Accuracy and completeness
- Professional presentation
- Clear communication
- Actionable content
- Consistency
- Grammar and spelling

Provide:
- Overall Quality Score (1-10)
- Strengths
- Areas for Improvement
- Specific Recommendations
- Final Verdict (Ready / Needs Revision)"""

        return self.execute(prompt)
