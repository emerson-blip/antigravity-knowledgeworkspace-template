# Agent Mission

**Objective:** Build a stock analysis agent.

## Description

This agent should be able to take a stock ticker symbol (e.g., "GOOGL", "AAPL") and provide a comprehensive analysis including:

1. Current price and recent performance.
2. Latest news headlines related to the company.
3. A summary of analyst ratings.

## Success Criteria

- The agent can successfully retrieve real-time data.
- The output is a concise, readable report.
- The agent handles invalid tickers gracefully.

## Obsidian Integration

If `OBSIDIAN_VAULT_PATH` is configured, the agent SHOULD prefer writing its findings and artifacts to the Obsidian Vault in the `_Agents/Emerson/` directory.
