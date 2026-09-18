# Abaddon skills

Skills for Abaddon workflows, terminology, and supported operations belong here.

| Skill | Use |
| --- | --- |
| [`abaddon-read-tickets`](abaddon-read-tickets/SKILL.md) | Retrieve and summarize authorized ticket context or assigned-ticket lists. |
| [`abaddon-triage-ticket`](abaddon-triage-ticket/SKILL.md) | Analyze a request, select relevant available application skills and prepare clarification or review drafts. |
| [`abaddon-work-ticket`](abaddon-work-ticket/SKILL.md) | Claim assigned work, write private notes, request clarification and resume after a human reply using explicit work permissions. |

These skills use an existing authorized MCP connection. They contain no server addresses, credentials or client-specific setup, and installing them does not grant application access. They discover the connection's supported operations instead of assuming a particular tool name or AI host.

The read and triage skills are read-only. The work skill requires the server to advertise its claim and private-dialogue tools and the credential to have explicit work permissions. A draft is not a posted comment, an accepted assignment or a ticket status change. If a needed capability is unavailable, report the limitation. Application-specific operations belong to that application's own skill and authorization boundary; final ticket closure remains human.

Install any skill directory independently, including any files inside it. See the repository's installation instructions. Pin a commit when a reproducible version is required. All skill names in this directory begin with `abaddon-`.

## Direct setup with a bot API key

This route works with a client that supports remote HTTPS MCP with a Bearer header and can install Agent Skills from GitHub. It does not require a marketplace submission or a human OAuth login by the bot. The owner signs in to Abaddon to manage the assistant and its credentials.

1. In the intended Abaddon environment, open **Il mio assistente**. Create or select your assistant and activate it. An administrator must grant the owner the explicit assistant-management permission first.
2. Configure the human **Referenti per i dubbi** before testing clarification requests. Those people also need access to the ticket and its internal comments.
3. Create a dedicated key for this assistant/client. Choose an expiry and the minimum scopes needed: assigned-ticket reading, and optionally work management and private dialogue. Never share a key across owners or unrelated bots. Keep development and production credentials separate.
4. Copy the **Endpoint MCP remoto** shown by that environment. Add a remote MCP server in the client and configure its `Authorization` header with the `Bearer` scheme and the bot's key, using the client's supported credential-entry flow.
5. Install the complete three canonical skill directories linked above. Update existing copies rather than creating duplicates. If the client already has a working Abaddon connection, reuse it; skill installation does not need another MCP server.
6. Call `abaddon_identity` through that MCP connection and verify the environment, assistant and granted scopes. Then request the assigned-ticket list in read-only mode, following pagination. An empty list may simply mean no ticket has been assigned yet.

### Key handling in the client

A secure secret card is not automatically a reference that can be used in a remote MCP header. Likewise, local-process environment variables are not necessarily expanded by a remote connector. Do not invent `${SECRET_NAME}` header bindings.

Some clients require the literal key in their connector configuration or tool-call parameters. A masked entry field alone does not prove the key stays invisible to the model or those parameters. Confirm the actual client behavior before supplying the key. If it is incompatible with your credential-handling requirements, stop and explain the limitation; do not silently switch authentication or introduce a local adapter.

Do not paste keys into ordinary chat, GitHub, skill files, screenshots or logs. Save the value in an approved secret store when it is created: Abaddon displays it once and cannot recover it later. If a replacement is needed, verify the replacement connection before revoking the superseded key. Pausing the assistant or revoking a key can stop that access.

### Prompt for the agent

The following contains no secret value or environment-specific endpoint. Supply the endpoint copied from Abaddon when the agent requests it.

```text
Set up Abaddon with a remote HTTPS MCP connection and a dedicated bot API key.
Ask me for the endpoint shown in my Abaddon assistant settings and confirm
which environment I intend to use. Do not guess an endpoint.

Use Bearer authentication through the client's supported credential-entry flow.
Before requesting the key, explain whether it will appear in connector
configuration or tool-call parameters. Do not ask me to paste it into ordinary
chat and do not display it. If the required credential flow is unsupported,
stop and explain the limitation. Do not silently switch to OAuth or a local adapter.

Install or update these complete directories from the main branch of
https://github.com/primocaredentgroup/pcg-app-skills:
- skills/abaddon/abaddon-read-tickets
- skills/abaddon/abaddon-triage-ticket
- skills/abaddon/abaddon-work-ticket

Reuse the intended Abaddon MCP connection. Do not create duplicate skills
or alter other connectors. Record the source commit.

After connection, use MCP to verify identity, environment and permissions,
then list assigned tickets in read-only mode. Report only the verification
result and ticket count, without credentials or patient details. Do not
modify tickets or operate on other applications during setup. Then stop.
```

### From installation to ticket work

An authorized human assigns a ticket to the assistant. The agent reads the available context, claims the work before writing, and follows the work skill for private notes or clarification. The human answers a clarification with **Rispondi e riprendi incarico** in Abaddon; an ordinary comment does not resume waiting work. The next MCP read can retrieve that answer. Installation alone does not establish an automatic polling routine or wake-up mechanism.

Other applications require their own connections and skills. This setup does not enable external operations or final ticket closure. Referent selection and a stored conversation are not automatic training of the agent or approval of a new procedure.

## Optional plugin bundles and OAuth

The [Abaddon Stage bundle](../../plugins/abaddon-stage/README.md) contains byte-identical copies of these skills and a fixed staging MCP endpoint. Copying only its skill directories is equivalent to installing the canonical skill directories; installing its MCP manifest also selects staging. Always use the endpoint and a fresh credential from the production application for a production connection.

Clients with a supported OAuth flow can use the optional authorization route where it is enabled. Marketplace import, OAuth and direct Bearer setup are separate choices; a public GitHub repository does not imply a public catalog listing.
