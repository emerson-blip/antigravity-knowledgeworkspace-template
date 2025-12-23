"""
Router Agent - The orchestrator that analyzes tasks and delegates to business specialists.

This agent acts as the "manager" in the Emerson swarm, analyzing user requests,
determining which specialist agents to involve, and synthesizing final results.
"""

from typing import Dict, List
from src.agents.base_agent import BaseAgent


class RouterAgent(BaseAgent):
    """
    Router agent responsible for task analysis and delegation.

    The Router analyzes incoming business requests, determines which specialist
    workers should handle them, coordinates multi-step workflows, and synthesizes
    the final response from worker outputs.
    """

    def __init__(self):
        system_prompt = """You are the Router Agent for Emerson, the coordinator of a business-focused multi-agent system.

Your responsibilities:
1. Analyze user requests and determine which specialist agents to involve
2. Break down complex business tasks into subtasks for different specialists
3. Coordinate the workflow between agents
4. Synthesize final results from multiple specialists

Available specialist agents:

- project_manager: Handles project planning, tracking, resource allocation, timelines, status reports, risk assessment, and stakeholder communication.

- researcher: Conducts market research, competitive analysis, customer insights, technology assessments, industry trends, and data analysis.

- product_dev: Manages product strategy, roadmaps, feature prioritization, MVP definitions, user stories, and product specifications.

- delivery: Handles client deliverables, documentation, quality assurance, client communication, and handoff management.

When analyzing a task, respond with a delegation plan in this format:
DELEGATION:
- agent: <agent_name>
- task: <specific task for that agent>

You may delegate to multiple agents in sequence or parallel.

Examples:
- "Create a project plan for the new website" -> project_manager
- "Research competitors in the CRM space" -> researcher
- "Define MVP features for the mobile app" -> product_dev
- "Prepare deliverables for client review" -> delivery
- "Plan a product launch" -> project_manager + product_dev + delivery"""

        super().__init__(role="router", system_prompt=system_prompt)

    def analyze_and_delegate(self, user_task: str) -> List[Dict[str, str]]:
        """
        Analyze a user task and create a delegation plan.

        Args:
            user_task: The task provided by the user.

        Returns:
            List of delegation instructions, each containing 'agent' and 'task'.
        """
        analysis = self.execute(user_task)

        # Parse the delegation plan from the response
        delegations = []
        lines = analysis.split('\n')
        current_delegation = {}

        for line in lines:
            line = line.strip()
            if line.startswith('- agent:'):
                if current_delegation:
                    delegations.append(current_delegation)
                current_delegation = {'agent': line.split(':', 1)[1].strip()}
            elif line.startswith('- task:') and current_delegation:
                current_delegation['task'] = line.split(':', 1)[1].strip()

        if current_delegation and 'task' in current_delegation:
            delegations.append(current_delegation)

        # Fallback: if no delegations parsed, use keyword matching
        if not delegations:
            delegations = self._simple_delegate(user_task)

        return delegations

    def _simple_delegate(self, task: str) -> List[Dict[str, str]]:
        """
        Keyword-based delegation as fallback.

        Args:
            task: The task to analyze.

        Returns:
            List of delegations based on keywords.
        """
        task_lower = task.lower()
        delegations = []

        # Project Management keywords
        pm_keywords = [
            'project', 'plan', 'timeline', 'schedule', 'milestone',
            'resource', 'sprint', 'backlog', 'status', 'track',
            'risk', 'stakeholder', 'capacity', 'deadline'
        ]
        if any(word in task_lower for word in pm_keywords):
            delegations.append({'agent': 'project_manager', 'task': task})

        # Research keywords
        research_keywords = [
            'research', 'analyze', 'analysis', 'market', 'competitor',
            'competitive', 'trend', 'insight', 'data', 'study',
            'investigate', 'assess', 'evaluate', 'benchmark'
        ]
        if any(word in task_lower for word in research_keywords):
            delegations.append({'agent': 'researcher', 'task': task})

        # Product Development keywords
        product_keywords = [
            'product', 'feature', 'roadmap', 'mvp', 'user story',
            'requirement', 'specification', 'prioritize', 'backlog',
            'release', 'version', 'prototype'
        ]
        if any(word in task_lower for word in product_keywords):
            delegations.append({'agent': 'product_dev', 'task': task})

        # Delivery keywords
        delivery_keywords = [
            'deliver', 'deliverable', 'client', 'document', 'documentation',
            'handoff', 'quality', 'review', 'prepare', 'presentation',
            'proposal', 'report', 'final'
        ]
        if any(word in task_lower for word in delivery_keywords):
            delegations.append({'agent': 'delivery', 'task': task})

        # Default to project_manager if no matches
        if not delegations:
            delegations.append({'agent': 'project_manager', 'task': task})

        return delegations

    def synthesize_results(self, delegations: List[Dict[str, str]], results: List[str]) -> str:
        """
        Synthesize final response from multiple agent results.

        Args:
            delegations: The original delegation plan.
            results: Results from each delegated agent.

        Returns:
            Final synthesized response.
        """
        synthesis_prompt = """Synthesize a final business response based on the following agent outputs:

"""
        for i, (delegation, result) in enumerate(zip(delegations, results), 1):
            synthesis_prompt += f"{i}. [{delegation['agent'].upper()}] {delegation['task']}\n"
            synthesis_prompt += f"   Result: {result}\n\n"

        synthesis_prompt += """Provide a concise executive summary that:
1. Highlights key findings and outcomes
2. Lists actionable next steps
3. Notes any dependencies or considerations"""

        return self.execute(synthesis_prompt)
