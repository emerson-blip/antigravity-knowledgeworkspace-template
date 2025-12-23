"""
Product Development Agent - Specialist for product strategy and development.

This agent handles product strategy, roadmaps, feature prioritization,
MVP definition, and user story creation.
"""

from src.agents.base_agent import BaseAgent


class ProductDevAgent(BaseAgent):
    """
    Product Development agent responsible for product strategy and lifecycle.

    Manages product strategy, roadmaps, feature prioritization, MVP definitions,
    and user story creation.
    """

    def __init__(self):
        system_prompt = """You are the Product Development Agent for Emerson, a specialist in product strategy and development.

Your expertise includes:
1. **Product Strategy**: Vision, objectives, success metrics, go-to-market
2. **Roadmap Planning**: Feature sequencing, release planning, dependencies
3. **Feature Prioritization**: Scoring frameworks (RICE, MoSCoW), trade-off analysis
4. **MVP Definition**: Core features, launch criteria, validation approach
5. **User Stories**: Requirements, acceptance criteria, edge cases
6. **Product Specifications**: Detailed feature documentation, technical requirements

When creating product artifacts, always:
- Start with the problem being solved
- Define clear success metrics
- Consider user needs and business value
- Include technical considerations
- Provide acceptance criteria

Output Format:
- Problem Statement
- Proposed Solution
- User Stories / Requirements
- Acceptance Criteria
- Technical Considerations
- Success Metrics
- Dependencies and Risks

Example outputs:
- Product Roadmaps (artifacts/plans/roadmap_[product].md)
- Feature Specifications (artifacts/plans/feature_[name].md)
- MVP Definitions (artifacts/plans/mvp_[product].md)
- User Stories (artifacts/plans/stories_[epic].md)"""

        super().__init__(role="product_dev", system_prompt=system_prompt)

    def create_product_roadmap(self, product_name: str, vision: str, timeframe: str) -> str:
        """
        Create a product roadmap.

        Args:
            product_name: Name of the product.
            vision: Product vision statement.
            timeframe: Roadmap timeframe (e.g., "Q1-Q4 2024").

        Returns:
            Formatted product roadmap.
        """
        prompt = f"""Create a product roadmap for:

Product: {product_name}
Vision: {vision}
Timeframe: {timeframe}

Include: Vision Statement, Strategic Themes, Quarterly Goals, Key Features per Quarter, Dependencies, and Success Metrics."""

        return self.execute(prompt)

    def define_mvp(self, product_name: str, problem_statement: str, target_users: str) -> str:
        """
        Define an MVP for a product.

        Args:
            product_name: Name of the product.
            problem_statement: The problem being solved.
            target_users: Target user description.

        Returns:
            MVP definition document.
        """
        prompt = f"""Define the MVP for:

Product: {product_name}
Problem Statement: {problem_statement}
Target Users: {target_users}

Include: Problem Validation, Core Features (must-have), Nice-to-have Features (post-MVP), User Flows, Launch Criteria, and Validation Approach."""

        return self.execute(prompt)

    def prioritize_features(self, product_name: str, features: list, criteria: list = None) -> str:
        """
        Prioritize features using a scoring framework.

        Args:
            product_name: Name of the product.
            features: List of features to prioritize.
            criteria: Optional custom criteria (defaults to RICE).

        Returns:
            Feature prioritization document.
        """
        criteria = criteria or ["Reach", "Impact", "Confidence", "Effort"]

        prompt = f"""Prioritize features for {product_name}:

Features to Prioritize:
{chr(10).join(f'- {feat}' for feat in features)}

Scoring Criteria:
{chr(10).join(f'- {crit}' for crit in criteria)}

Include: Scoring Matrix, Ranked Feature List, Reasoning for Top Priorities, and Recommendations for Sequencing."""

        return self.execute(prompt)

    def write_user_stories(self, feature_name: str, feature_description: str) -> str:
        """
        Write user stories for a feature.

        Args:
            feature_name: Name of the feature.
            feature_description: Description of the feature.

        Returns:
            User stories document.
        """
        prompt = f"""Write user stories for:

Feature: {feature_name}
Description: {feature_description}

For each user story include:
- User Story (As a [user], I want [goal], so that [benefit])
- Acceptance Criteria
- Edge Cases
- Technical Notes (if applicable)

Organize stories by user persona and priority."""

        return self.execute(prompt)

    def create_feature_spec(self, feature_name: str, context: str) -> str:
        """
        Create a detailed feature specification.

        Args:
            feature_name: Name of the feature.
            context: Context and requirements for the feature.

        Returns:
            Feature specification document.
        """
        prompt = f"""Create a detailed feature specification for:

Feature: {feature_name}
Context: {context}

Include:
- Problem Statement
- Proposed Solution
- User Stories
- Functional Requirements
- Non-Functional Requirements
- UI/UX Considerations
- Technical Architecture
- Acceptance Criteria
- Dependencies
- Risks and Mitigations"""

        return self.execute(prompt)
