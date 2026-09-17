#!/usr/bin/env python3
"""Synchronize the static Abaddon plugin bundle from its canonical sources."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "abaddon-stage"
SKILLS = ("abaddon-read-tickets", "abaddon-triage-ticket", "abaddon-work-ticket")


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def generated_files() -> dict[Path, bytes]:
    """Build only static metadata and complete, unmodified skill directories."""
    manifest = json.loads((PLUGIN / "plugin.json").read_text(encoding="utf-8"))
    mcp = json.loads((PLUGIN / "mcp.json").read_text(encoding="utf-8"))
    cursor_manifest = {key: value for key, value in manifest.items() if key != "$schema"}
    cursor_manifest["mcpServers"] = "./mcp.cursor.json"
    cursor_mcp = {"mcpServers": {
        name: {"url": server["url"]} for name, server in mcp["mcpServers"].items()
    }}
    result = {
        PLUGIN / ".cursor-plugin" / "plugin.json": json_bytes(cursor_manifest),
        PLUGIN / "mcp.cursor.json": json_bytes(cursor_mcp),
        PLUGIN / "LICENSE": (ROOT / "LICENSE").read_bytes(),
        ROOT / ".cursor-plugin" / "marketplace.json": json_bytes({
            "name": "pcg-app-plugins",
            "owner": {"name": "Primo Caredent Group"},
            "metadata": {"description": "Native plugins for Primo Caredent Group application skills."},
            "plugins": [{
                "name": manifest["name"],
                "source": "plugins/abaddon-stage",
                "description": manifest["description"],
                "version": manifest["version"],
            }],
        }),
    }
    for name in SKILLS:
        source = ROOT / "skills" / "abaddon" / name
        if not (source / "SKILL.md").is_file():
            raise ValueError(f"Missing canonical skill: {name}")
        for path in sorted(source.rglob("*")):
            if path.is_symlink():
                raise ValueError(f"Symbolic links are not allowed: {path.relative_to(ROOT)}")
            if path.is_file():
                result[PLUGIN / "skills" / name / path.relative_to(source)] = path.read_bytes()
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Report drift without writing files.")
    args = parser.parse_args()
    expected = generated_files()
    stale = set()
    skills_dir = PLUGIN / "skills"
    if skills_dir.exists():
        stale = {path for path in skills_dir.rglob("*") if path.is_file()} - set(expected)
    changed = [path for path, value in expected.items() if not path.is_file() or path.read_bytes() != value]
    if args.check:
        for path in sorted(stale | set(changed)):
            print(f"Generated plugin file needs synchronization: {path.relative_to(ROOT)}", file=sys.stderr)
        if stale or changed:
            return 1
        print("Plugin synchronization passed (3 canonical skill copies and native manifests).")
        return 0
    for path in stale:
        path.unlink()
    for path in changed:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(expected[path])
    print(f"Synchronized {len(changed)} plugin file(s); removed {len(stale)} stale file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
