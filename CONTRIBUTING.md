# Contributing

Contributions are welcome through pull requests.

## Add a skill

1. Choose one of the application directories under `skills/`.
2. Copy `templates/SKILL.template.md` into a new directory named `<application>-<capability>/SKILL.md`.
3. Replace every example value and keep the skill focused on one reusable capability.
4. Add only the supporting `references/`, `scripts/`, `assets/`, or `agents/openai.yaml` files the skill actually needs.
5. Run `python3 scripts/validate_skills.py`.
6. Open a pull request explaining the intended requests, safety boundaries, and validation performed.

## Writing requirements

- Use lowercase letters, digits, and hyphens for names.
- Keep names shorter than 64 characters and prefix them with the application identifier.
- Make the frontmatter description precise enough for automatic skill selection.
- Keep essential workflow and constraints in `SKILL.md`; move conditional detail to focused references.
- Use relative links for files inside a skill and ensure every linked file exists.
- Do not add empty resource directories or placeholder content.
- Do not duplicate generic agent knowledge that does not change decisions.

## Public-content review

Before committing, confirm that every added line is suitable for unrestricted public distribution. Never include:

- credentials, access tokens, private keys, passwords, or session material;
- personal, patient, medical, financial, or employment data;
- authenticated links or URLs containing sensitive parameters;
- confidential architecture, proprietary datasets, or unapproved internal procedures;
- local absolute paths or environment-specific secret values.

Use synthetic examples and obvious placeholder values where a format must be demonstrated.

## Pull request acceptance

A pull request must pass `validate-skills`, contain no unrelated changes, and preserve compatibility with direct installation from the skill directory path.
