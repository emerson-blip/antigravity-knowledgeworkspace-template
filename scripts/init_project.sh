#!/bin/bash

# scripts/init_project.sh
# Initialiseert een nieuwe agent werkomgeving voor een specifiek project.

echo "🪐 Emerson Agent Project Initializer"
echo "------------------------------------"

# Vraag om projectnaam
read -p "Voer de projectnaam in: " PROJECT_NAME
if [ -z "$PROJECT_NAME" ]; then
    echo "❌ Projectnaam mag niet leeg zijn."
    exit 1
fi

# Vraag om projectbeschrijving (missie)
read -p "Wat is de specifieke missie voor deze agent? " PROJECT_MISSION

# Vraag om Notion Project ID (optioneel)
read -p "Voer het Notion Project ID in (optioneel): " PROJECT_ID_NOTION

# Vraag om Obsidian Vault Pad
DEFAULT_VAULT="/Users/emerson/Obsidian/emerson"
read -p "Voer het pad naar je Obsidian Vault in [$DEFAULT_VAULT]: " PROJECT_VAULT_PATH
PROJECT_VAULT_PATH=${PROJECT_VAULT_PATH:-$DEFAULT_VAULT}

# Maak noodzakelijke mappen
mkdir -p .context
mkdir -p artifacts

# Update mission.md
cat <<EOF > mission.md
# Agent Mission: $PROJECT_NAME

**Objective:** $PROJECT_MISSION

## Context
Dit project is geïnitialiseerd via de Emerson Agent Template.
EOF

# Controleer .env
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ .env aangemaakt op basis van .env.example."
    else
        touch .env
        echo "⚠️ Geen .env.example gevonden. Lege .env aangemaakt."
    fi
fi

# Vul Project ID in .env in als opgegeven
if [ -n "$PROJECT_ID_NOTION" ]; then
    echo "NOTION_PROJECT_ID=$PROJECT_ID_NOTION" >> .env
fi

# Vul Obsidian Vault Pad in .env in
echo "OBSIDIAN_VAULT_PATH=$PROJECT_VAULT_PATH" >> .env

echo "------------------------------------"
echo "✅ Project '$PROJECT_NAME' succesvol geïnitialiseerd!"
echo "🚀 Je kunt nu beginnen door de agent te starten: python src/agent.py"
