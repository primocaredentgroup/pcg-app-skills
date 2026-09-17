#!/usr/bin/env python3
"""Validate the structure and public-safety basics of PCG Agent Skills."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_FIELD_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*?)\s*$")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
TEXT_SUFFIXES = {
    ".md",
    ".markdown",
    ".txt",
    ".yaml",
    ".yml",
    ".json",
    ".py",
    ".js",
    ".mjs",
    ".cjs",
    ".ts",
    ".tsx",
    ".sh",
    ".toml",
    ".ini",
    ".cfg",
}
SECRET_PATTERNS = {
    "private key material": re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "assigned secret value": re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9+/_.=-]{16,}"
    ),
}


def parse_args() -> argparse.Namespace:
    default_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=default_root,
        help="Repository root to validate (defaults to the parent of scripts/).",
    )
    parser.add_argument(
        "--require-skill",
        action="store_true",
        help="Fail unless at least one complete skill is present.",
    )
    return parser.parse_args()


def read_text(path: Path, errors: list[str]) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        errors.append(f"{path}: expected UTF-8 text")
    except OSError as exc:
        errors.append(f"{path}: cannot read file: {exc}")
    return None


def parse_frontmatter(path: Path, text: str, errors: list[str]) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        errors.append(f"{path}: SKILL.md must begin with YAML frontmatter")
        return {}

    try:
        end = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        errors.append(f"{path}: YAML frontmatter is not closed")
        return {}

    fields: dict[str, str] = {}
    for line_number, line in enumerate(lines[1:end], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = FRONTMATTER_FIELD_RE.match(line)
        if not match:
            errors.append(f"{path}:{line_number}: frontmatter fields must be single-line key/value pairs")
            continue
        key, value = match.groups()
        fields[key] = value.strip().strip("'\"")

    for required in ("name", "description"):
        if not fields.get(required):
            errors.append(f"{path}: missing non-empty frontmatter field '{required}'")
    return fields


def validate_links(skill_dir: Path, skill_md: Path, text: str, errors: list[str]) -> None:
    skill_root = skill_dir.resolve()
    for raw_target in MARKDOWN_LINK_RE.findall(text):
        target = raw_target.strip().split(maxsplit=1)[0].strip("<>\"")
        if not target or target.startswith(("#", "http://", "https://", "mailto:", "data:")):
            continue
        target_path = unquote(target.split("#", 1)[0])
        if not target_path:
            continue
        candidate = (skill_dir / target_path).resolve()
        try:
            candidate.relative_to(skill_root)
        except ValueError:
            errors.append(f"{skill_md}: relative link escapes the skill directory: {raw_target}")
            continue
        if not candidate.exists():
            errors.append(f"{skill_md}: linked file does not exist: {raw_target}")


def validate_public_text(root: Path, errors: list[str]) -> None:
    excluded = {".git", "__pycache__", ".venv"}
    for path in root.rglob("*"):
        if any(part in excluded for part in path.parts) or not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {"LICENSE"}:
            continue
        text = read_text(path, errors)
        if text is None:
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{path}: possible {label}")


def validate_repository(root: Path, require_skill: bool) -> tuple[list[str], int]:
    errors: list[str] = []
    root = root.resolve()
    skills_root = root / "skills"

    if not skills_root.is_dir():
        return [f"{skills_root}: missing skills directory"], 0

    for path in root.rglob("*"):
        if path.is_symlink():
            errors.append(f"{path}: symbolic links are not allowed")

    skill_count = 0
    seen_names: dict[str, Path] = {}
    app_dirs = sorted(path for path in skills_root.iterdir() if path.is_dir())

    for app_dir in app_dirs:
        app = app_dir.name
        if not NAME_RE.fullmatch(app):
            errors.append(f"{app_dir}: invalid application identifier")
        if not (app_dir / "README.md").is_file():
            errors.append(f"{app_dir}: missing application README.md")

        for entry in sorted(app_dir.iterdir()):
            if entry.name == "README.md":
                continue
            if not entry.is_dir():
                errors.append(f"{entry}: only README.md and skill directories are allowed here")
                continue

            skill_count += 1
            skill_name = entry.name
            skill_md = entry / "SKILL.md"
            if not NAME_RE.fullmatch(skill_name) or len(skill_name) >= 64:
                errors.append(f"{entry}: invalid skill directory name")
            if not skill_name.startswith(f"{app}-"):
                errors.append(f"{entry}: skill name must begin with '{app}-'")
            if not skill_md.is_file():
                errors.append(f"{entry}: missing SKILL.md")
                continue

            text = read_text(skill_md, errors)
            if text is None:
                continue
            fields = parse_frontmatter(skill_md, text, errors)
            declared_name = fields.get("name")
            if declared_name and declared_name != skill_name:
                errors.append(
                    f"{skill_md}: frontmatter name '{declared_name}' must match directory '{skill_name}'"
                )
            if declared_name:
                previous = seen_names.get(declared_name)
                if previous:
                    errors.append(f"{skill_md}: duplicate skill name also declared in {previous}")
                else:
                    seen_names[declared_name] = skill_md
            validate_links(entry, skill_md, text, errors)

    if require_skill and skill_count == 0:
        errors.append(f"{skills_root}: expected at least one complete skill")

    validate_public_text(root, errors)
    return errors, skill_count


def main() -> int:
    args = parse_args()
    errors, skill_count = validate_repository(args.root, args.require_skill)
    if errors:
        print("Skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Skill validation passed ({skill_count} published skill(s)).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
