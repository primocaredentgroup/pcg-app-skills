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
