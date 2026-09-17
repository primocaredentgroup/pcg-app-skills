#!/usr/bin/env python3
"""Validate the narrow, remote-only Abaddon staging plugin contract."""

from __future__ import annotations

import json
import re
import sys
from urllib.parse import urlsplit

from sync_plugins import PLUGIN, ROOT, generated_files
from validate_skills import validate_public_text


STAGE_MCP_URL = "https://pastel-bass-787.convex.site/mcp"


def main() -> int:
    errors: list[str] = []
    try:
        manifest = json.loads((PLUGIN / "plugin.json").read_text(encoding="utf-8"))
        mcp = json.loads((PLUGIN / "mcp.json").read_text(encoding="utf-8"))
        expected = generated_files()
        for path, value in expected.items():
            if not path.is_file() or path.read_bytes() != value:
                errors.append(f"Generated file differs from source: {path.relative_to(ROOT)}")

        allowed_manifest = {"$schema", "name", "version", "description", "author", "homepage", "repository", "license", "keywords"}
        if set(manifest) != allowed_manifest:
            errors.append("Portable manifest must contain only the approved public metadata fields")
        if manifest.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
            errors.append("Portable manifest schema must be Agent Plugins 1.0.0")
        if manifest.get("name") != "abaddon-stage":
            errors.append("Plugin must be explicitly named abaddon-stage")
        if not re.fullmatch(r"0\.\d+\.\d+-stage\.\d+", manifest.get("version", "")):
            errors.append("Stage plugin must retain a 0.x.y-stage.n prerelease version")
        if manifest.get("author") != {"name": "Primo Caredent Group"}:
            errors.append("Author metadata must contain only the public organization name")
        if manifest.get("repository") != "https://github.com/primocaredentgroup/pcg-app-skills":
            errors.append("Plugin repository must be the canonical public skills repository")
        if manifest.get("license") != "MIT":
            errors.append("Plugin license must match the canonical repository")

        if set(mcp) != {"$schema", "mcpServers"} or mcp.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json":
            errors.append("MCP config must follow Agent Plugins 1.0.0")
        servers = mcp.get("mcpServers", {})
        if set(servers) != {"abaddon-stage"}:
            errors.append("The plugin may expose exactly one staging MCP connection")
        for server in servers.values():
            if set(server) != {"type", "url"} or server.get("type") != "streamable-http":
                errors.append("MCP must use direct Streamable HTTP with only type and url")
            url = urlsplit(server.get("url", ""))
            if server.get("url") != STAGE_MCP_URL:
                errors.append("MCP endpoint must match the reviewed staging endpoint")
            if url.scheme != "https" or not url.hostname or url.username or url.password or url.query or url.fragment or url.path != "/mcp" or url.port:
                errors.append("MCP endpoint must be a public HTTPS /mcp URL without credentials, parameters, or port overrides")
            if url.hostname and (url.hostname.endswith((".invalid", ".test", ".example", ".localhost")) or url.hostname in {"localhost", "example.com", "example.org", "example.net"}):
                errors.append("MCP endpoint is not configured for release")

        allowed_files = set(expected) | {PLUGIN / "plugin.json", PLUGIN / "mcp.json", PLUGIN / "README.md"}
        for path in PLUGIN.rglob("*"):
            if path.is_symlink():
                errors.append(f"Symbolic links are not allowed: {path.relative_to(ROOT)}")
            if path.is_file() and path not in allowed_files:
                errors.append(f"Unexpected plugin payload file: {path.relative_to(ROOT)}")
        validate_public_text(ROOT, errors)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(str(exc))

    if errors:
        print("Plugin validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Plugin validation passed (stage-only, remote HTTPS, no packaged credentials or launchers).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
