# Abaddon Stage

Plugin bundle for authorized Abaddon staging tickets. It contains the canonical read, triage, and delegated-work skills plus remote HTTPS MCP manifests. This is a staging prerelease; installing it does not grant access to application data.

## Contents

| Skill | Purpose |
| --- | --- |
| [`abaddon-read-tickets`](skills/abaddon-read-tickets/SKILL.md) | Read authorized ticket context and assignment lists. |
| [`abaddon-triage-ticket`](skills/abaddon-triage-ticket/SKILL.md) | Analyze requests and prepare clarification or handoff drafts. |
| [`abaddon-work-ticket`](skills/abaddon-work-ticket/SKILL.md) | Claim delegated work and use authorized private dialogue tools. |

The skill directories are generated, byte-identical copies of the [canonical Abaddon skills](../../skills/abaddon/README.md). They require an existing authorized connection and discover its supported operations. Final ticket closure remains human; operations in other applications require their own skills and authorization.

The package contains no credentials, user identifiers, local launchers, installation scripts, or runtime dependencies.

## Manifests

The portable Agent Plugins manifest uses `mcp.json` with the `streamable-http` transport. The Cursor manifest selects `mcp.cursor.json`, which declares the same HTTPS URL in the host's remote-server format. Each host loads one connection.

**The MCP manifests target staging and are not production configuration.** Installing only the skill directories does not change an existing connection's endpoint or authentication. The repository's `.cursor-plugin/marketplace.json` is package metadata, not evidence of a public catalog listing.

## Maintenance

Edit the canonical skill under `skills/abaddon/`, then run `python3 scripts/sync_plugins.py` from the repository root. This copies complete skill directories and regenerates the Cursor metadata; it is a repository maintenance tool, not part of the installed plugin.

Validate changes from the repository root:

```bash
python3 scripts/validate_skills.py
python3 scripts/sync_plugins.py --check
python3 scripts/validate_plugins.py
```

Keep operator setup and rollout guides in private application documentation. Never commit authorization responses, user identifiers, ticket contents, tokens, or test records as release evidence.
