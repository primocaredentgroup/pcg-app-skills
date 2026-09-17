# Abaddon Stage

Native plugin for authorized Abaddon staging tickets. It bundles the canonical read, triage, and delegated-work skills with a direct HTTPS MCP connection. The plugin is a staging prerelease; installing it does not grant access to application data.

The package supports the [Agent Plugins standard](https://agent-plugins.org/plugin-authors/manifest) and includes a [Cursor plugin manifest](https://cursor.com/docs/reference/plugins). OAuth discovery and sign-in are handled by the host and the Abaddon authorization server. No client secret, bearer token, user identifier, local launcher, or installation script is required in the package.

## Install in Grok Bot

After an administrator has made the plugin available to the team, open **Plugins** in Grok Bot, find **abaddon-stage**, and add it. Complete **Authorize** or **Authenticate** in the browser, sign in to the intended Abaddon staging account, and review the access being requested. Verify that the plugin appears under **Installed**. These are the provider's [documented connection steps](https://cursor.com/help/grok-bot/connect-plugins).

Each person connects their own account. A team marketplace import does not finish user authentication. Grok uses the team's connector policy, and a permitted connector is available to that person's Bots. Grok does not support pushing connectors to members as mandatory or default-on installations. See [Grok connector policy](https://cursor.com/docs/grok-bot/teams#connector-policy).

Once connected, ask the agent to inspect the available Abaddon identity and capabilities and confirm that this is staging before reading tickets. Read access does not establish an assistant assignment. Delegated work requires the corresponding server-advertised permissions; final ticket closure remains human. The plugin does not grant access to other applications.

## Make the plugin available to a team

The repository's `.cursor-plugin/marketplace.json` points to this plugin. On an eligible Cursor Teams or Enterprise account, use **Dashboard → Plugins → Team Marketplaces → Add Marketplace → Import from Repo** to import the public repository, then review the plugin with **Add to Marketplace**. Set the intended marketplace audience and enable this connector. Keep installation opt-in for the staging rollout. Follow the current [team marketplace documentation](https://cursor.com/docs/plugins#add-a-team-marketplace).

An import must be verified in the actual Grok account: the package must appear, load its three skills and MCP connection, complete OAuth, and report the intended staging identity. Manifest validation alone does not prove any of these steps succeeded. Account plan, admin access, connector policy, and provider support can affect availability.

Submitting a plugin to the general public Marketplace is a separate path. Cursor reviews public submissions and updates before listing them, so a GitHub merge does not mean the plugin is published in that catalog. See [plugin submission](https://cursor.com/docs/reference/plugins#submitting-a-plugin).

## Contents and maintenance

| Canonical skill | Purpose |
| --- | --- |
| `abaddon-read-tickets` | Read authorized ticket context and assignment lists. |
| `abaddon-triage-ticket` | Analyze requests and prepare clarification or handoff drafts. |
| `abaddon-work-ticket` | Claim delegated work and use authorized private dialogue tools. |

Edit the canonical skill under `skills/abaddon/` in the repository root, then run `python3 scripts/sync_plugins.py` from that root. The script copies complete skill directories without changing their content and regenerates the Cursor metadata. It is a repository maintenance tool; the installed plugin contains no executable setup.

The portable manifest uses `mcp.json` with the explicit `streamable-http` transport. The Cursor manifest selects `mcp.cursor.json`, which declares the same HTTPS URL using Cursor's native remote-server format. Each host loads one connection.

Before sharing a release, run the repository's skill validation, plugin synchronization check, and plugin validation. Then verify discovery, OAuth, advertised capabilities, and a permitted read through the target host. Never commit authorization responses, user identifiers, tickets, tokens, or test records as release evidence.
