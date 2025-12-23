"""
Researcher Agent - Specialist for research and analysis.

This agent handles all research tasks including market analysis, competitive
intelligence, customer insights, and technology assessments.
"""

from src.agents.base_agent import BaseAgent


class ResearcherAgent(BaseAgent):
    """
    Researcher agent responsible for business research and analysis.

    Conducts market research, competitive analysis, customer insights,
    technology assessments, and trend analysis.
    """

    def __init__(self):
        system_prompt = """You are the Researcher Agent for Emerson, a specialist in business research and analysis.

Your expertise includes:
1. **Market Research**: Industry analysis, market sizing, growth trends
2. **Competitive Analysis**: Competitor tracking, positioning, SWOT analysis
3. **Customer Insights**: Persona development, feedback analysis, needs assessment
4. **Technology Assessment**: Tool evaluation, tech stack analysis, build vs buy decisions
5. **Trend Analysis**: Industry trends, emerging technologies, market shifts
6. **Data Analysis**: Quantitative and qualitative research methods

When conducting research, always:
- Start with key findings (lead with insights)
- Provide data and evidence to support conclusions
- Include methodology for transparency
- Offer actionable recommendations
- Cite sources where applicable

Output Format:
- Executive Summary with key insights
- Methodology section
- Detailed findings with data
- Analysis and implications
- Recommendations
- Sources and references

Example outputs:
- Market Research Reports (artifacts/research/market_[topic].md)
- Competitive Analysis (artifacts/research/competitive_[industry].md)
- Customer Insights (artifacts/research/insights_[segment].md)
- Technology Assessments (artifacts/research/tech_[area].md)"""

        super().__init__(role="researcher", system_prompt=system_prompt)

    def conduct_market_research(self, industry: str, focus_areas: list) -> str:
        """
        Conduct market research for a given industry.

        Args:
            industry: The industry to research.
            focus_areas: Specific areas to focus on.

        Returns:
            Formatted market research report.
        """
        prompt = f"""Conduct comprehensive market research for:

Industry: {industry}
Focus Areas:
{chr(10).join(f'- {area}' for area in focus_areas)}

Include: Market Overview, Key Players, Trends, Opportunities, Challenges, and Recommendations."""

        return self.execute(prompt)

    def analyze_competitors(self, company: str, competitors: list) -> str:
        """
        Perform competitive analysis.

        Args:
            company: The company to analyze for.
            competitors: List of competitors to analyze.

        Returns:
            Competitive analysis report.
        """
        prompt = f"""Perform a competitive analysis for {company} against:

Competitors:
{chr(10).join(f'- {comp}' for comp in competitors)}

Include: Competitor Profiles, Feature Comparison, Pricing Analysis, Strengths/Weaknesses, Market Positioning, and Strategic Recommendations."""

        return self.execute(prompt)

    def assess_technology(self, category: str, options: list, criteria: list) -> str:
        """
        Assess technology options against criteria.

        Args:
            category: Technology category (e.g., "CRM", "Project Management").
            options: List of technology options to evaluate.
            criteria: Evaluation criteria.

        Returns:
            Technology assessment report.
        """
        prompt = f"""Conduct a technology assessment for {category}:

Options to Evaluate:
{chr(10).join(f'- {opt}' for opt in options)}

Evaluation Criteria:
{chr(10).join(f'- {crit}' for crit in criteria)}

Include: Overview of each option, Comparison Matrix, Pros/Cons, Scoring, and Recommendation."""

        return self.execute(prompt)

    def analyze_trends(self, domain: str, timeframe: str) -> str:
        """
        Analyze trends in a given domain.

        Args:
            domain: The domain to analyze (e.g., "AI in Healthcare").
            timeframe: Timeframe for trend analysis.

        Returns:
            Trend analysis report.
        """
        prompt = f"""Analyze trends in {domain} for the {timeframe}:

Include:
- Current State Overview
- Emerging Trends
- Key Drivers
- Potential Disruptions
- Implications for Business
- Recommended Actions"""

        return self.execute(prompt)
