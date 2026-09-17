# Agent instructions

## Purpose

This public repository is the canonical source for Primo Caredent Group application skills. Keep it portable, content-focused, and directly installable from GitHub paths.

## Skill layout

- Publish skills only at `skills/<application>/<skill-name>/SKILL.md`.
- Make `<skill-name>` equal the frontmatter `name`.
- Prefix every skill name with its application identifier.
- Use lowercase letters, digits, and hyphens; keep names shorter than 64 characters.
- Keep `SKILL.md` concise and add supporting directories only when they materially improve the skill.
- Link supporting files with relative paths and explain when an agent should read or run them.

## Public boundary

Treat every file, branch, pull request, issue, and commit as public. Never add credentials, secret values, personal or patient data, authenticated URLs, confidential records, or unapproved internal procedures. Use synthetic examples.

## Changes

- Read the target application's README before adding a skill.
- Start from `templates/SKILL.template.md`, then remove all example wording.
- Run `python3 scripts/validate_skills.py` before committing.
- Keep changes narrowly scoped and do not add application runtimes, hosted-service dependencies, or generated vendor files.
- Do not publish a skill until its instructions and supporting files are complete.
