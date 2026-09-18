# PCG App Skills

Public, canonical Agent Skills for Primo Caredent Group applications.

This repository contains portable instructions that AI agents can download and install directly from GitHub. Skills are grouped by the application they support. The skill files are independently installable; access to an application's live data requires its authorized connection.

## Applications

| Application | Path | Published skills |
| --- | --- | ---: |
| Global | [`skills/global`](skills/global) | 0 |
| Innovation Sax | [`skills/innovation-sax`](skills/innovation-sax) | 0 |
| Abaddon | [`skills/abaddon`](skills/abaddon) | 3 |

## Repository contract

Every published skill must use this layout:

```text
skills/<application>/<application>-<capability>/
|-- SKILL.md
|-- agents/openai.yaml        Optional
|-- references/               Optional
|-- scripts/                  Optional
`-- assets/                   Optional
```

The skill directory name must match the `name` field in `SKILL.md`. Names use lowercase letters, digits, and hyphens, are shorter than 64 characters, and begin with their application identifier. For example:

```text
skills/innovation-sax/innovation-sax-create-problem/SKILL.md
```

`SKILL.md` must start with YAML frontmatter containing a single-line `name` and `description`:

```yaml
---
name: innovation-sax-create-problem
description: Create a structured problem record in Innovation Sax when a user asks to report an operational issue.
---
```

See [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`templates/SKILL.template.md`](templates/SKILL.template.md) before adding a skill.

## Install a skill

Each skill is independently addressable by its GitHub path.

### Codex skill installer

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo primocaredentgroup/pcg-app-skills \
  --path skills/<application>/<skill-name>
```

The skill becomes available to Codex on the next turn.

### Generic agents

Agents that support the Agent Skills directory format can copy or synchronize the selected skill directory into their configured skills location. A skill entrypoint is also available without authentication at:

```text
https://raw.githubusercontent.com/primocaredentgroup/pcg-app-skills/main/skills/<application>/<skill-name>/SKILL.md
```

Pin a commit SHA instead of `main` when reproducibility is required.

## Native plugins

The [Abaddon skill index](skills/abaddon/README.md) describes the three independently installable skills. Installing skill files does not grant application access.

[`abaddon-stage`](plugins/abaddon-stage/README.md) is an optional bundle of the same skills and a fixed staging HTTPS MCP endpoint, with Agent Plugins and Cursor manifests plus a Cursor team marketplace manifest. Its remote manifest contains no API key; authentication must be configured by the host. Do not use that staging manifest for production.

Public Marketplace listing has a separate provider review process. Skills under `skills/` remain the canonical source. Plugin skill copies are generated and checked for exact equality.

## Validate locally

```bash
python3 scripts/validate_skills.py
python3 scripts/sync_plugins.py --check
python3 scripts/validate_plugins.py
```

The same validation runs on every pull request and push to `main`.

## Public-content boundary

Everything committed here is public. Do not include credentials, personal or patient data, confidential business information, authenticated URLs, private identifiers, or internal material that has not been approved for publication. See [`SECURITY.md`](SECURITY.md) for private vulnerability reporting.

## License

MIT. See [`LICENSE`](LICENSE).
