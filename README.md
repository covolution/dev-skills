# AI Agent Dev Skills

This repository publishes [Agent Plugins](https://agent-plugins.org/) containing AI agent skills that enhance development workflows.

## Plugins

| Plugin | Skills |
| --- | --- |
| `dev-agile` | `jira`, `sonar`, `user-story`, `work-on-ticket` |
| `archy` | `c4-architecture`, `mermaid-diagrams`, `mermaid-validate`, `lightweight-implementation-analysis-protocol` |

## Repository layout

```text
.github/plugin/marketplace.json   # marketplace listing the plugins below
plugins/
├── dev-agile/
│   ├── plugin.json               # Agent Plugins v1.0.0 manifest
│   └── skills/<skill-name>/SKILL.md
└── archy/
    ├── plugin.json
    └── skills/<skill-name>/SKILL.md
.claude/skills -> ../plugins/dev-agile/skills   # symlink for tools that read .claude/skills
.agents/skills -> ../.claude/skills             # symlink for tools that read .agents/skills
```

Each plugin's `skills/` directory is the single source of truth. The `.claude/skills` symlink only exposes `dev-agile`; install `archy` through the marketplace.

## Installation

### GitHub Copilot CLI

Add the marketplace, then install the plugin (marketplace name `dev-skills`):

```
/plugin marketplace add covolution/dev-skills
/plugin install dev-agile@dev-skills
/plugin install archy@dev-skills
```

Or from a terminal: `copilot plugin marketplace add covolution/dev-skills` and `copilot plugin install <plugin>@dev-skills`.

### VS Code

1. Run **Chat: Open Customizations** from the Command Palette and select **Browse**.
2. Open the source menu, select **Configure Marketplaces** > **Add Marketplace**, and enter `covolution/dev-skills`.
3. Select the plugin you want (`dev-agile` or `archy`) and choose **Install**.

Alternatively, add `covolution/dev-skills` to the `chat.plugins.marketplaces` setting.

### Other agents (skills only)

```sh
npx skills add https://github.com/covolution/dev-skills
```

## Add a plugin or skill

1. Create `plugins/<plugin-name>/plugin.json` with the `$schema` `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json` and a lowercase `name`.
2. Add skills as `plugins/<plugin-name>/skills/<skill-name>/SKILL.md`, following the [Agent Skills specification](https://agentskills.io/specification).
3. Register the plugin in `.github/plugin/marketplace.json` and keep its `version` in sync with `plugin.json`.