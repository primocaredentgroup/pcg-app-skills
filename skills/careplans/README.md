# Careplans skills

Skills for reading care-plan rows and carrying out explicitly authorized Careplans operations through an existing MCP connection.

| Skill | Use |
| --- | --- |
| [`careplans-read-rows`](careplans-read-rows/SKILL.md) | Search plan rows, completed rows, pending-cleanup rows, ethics rows, restorable rows and code rows. |
| [`careplans-manage-plan`](careplans-manage-plan/SKILL.md) | Preview and execute the ten supported plan operations, then check their recorded outcomes without retrying an uncertain execution. |

Install either skill directory independently, including its supporting references. The skills inspect the connection's advertised capabilities and permissions. Installation does not grant access, enable writes or make an unavailable tool callable.

Careplans keys can explicitly cover all plans, with the target PDC supplied per request; older selected-plan keys retain their restrictions. Each key still has its own read and operation permissions. Ticket assignment, comments and closure remain separate application workflows; an external ticket reference records context without authorizing a Careplans change.

These files contain generic operating guidance, with no server addresses, credentials or client-specific setup. No Careplans plugin bundle or application runtime is included.
