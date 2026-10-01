#!/usr/bin/env bash
# Link the studio-kit skill and agents into Claude Code (~/.claude) so edits in this repo take effect immediately.
#   ~/.claude/skills/studio-kit  -> skills/studio-kit
#   ~/.claude/agents/studio-kit  -> agents/            (Claude Code reads agents from subfolders)
# Windows: directory junctions via PowerShell (no admin or Developer Mode needed).
# macOS/Linux: symlinks. Safe to re-run.
set -euo pipefail

KIT="$(cd "$(dirname "$0")/.." && pwd)"
CLAUDE_DIR="${HOME}/.claude"
mkdir -p "$CLAUDE_DIR/skills" "$CLAUDE_DIR/agents"

link_dir() { # link_dir <source dir> <target>
  local src="$1" dst="$2"
  if command -v powershell.exe >/dev/null 2>&1 && command -v cygpath >/dev/null 2>&1; then
    local wsrc wdst; wsrc="$(cygpath -w "$src")"; wdst="$(cygpath -w "$dst")"
    powershell.exe -NoProfile -Command "
      \$dst='$wdst'; \$src='$wsrc'
      if (Test-Path \$dst) {
        \$i = Get-Item \$dst -Force
        if (\$i.LinkType) { \$i.Delete() } else { Write-Output '  ! not a link, left alone:'; Write-Output \$dst; exit 1 }
      }
      New-Item -ItemType Junction -Path \$dst -Target \$src | Out-Null
      Write-Output ('  junction  ' + \$dst)"
  else
    if [ -L "$dst" ]; then rm "$dst"; elif [ -e "$dst" ]; then echo "  ! $dst is not a link; left alone"; return 1; fi
    ln -s "$src" "$dst" && echo "  symlink   $dst"
  fi
}

echo "Skill:";  link_dir "$KIT/skills/studio-kit" "$CLAUDE_DIR/skills/studio-kit"
echo "Agents:"; link_dir "$KIT/agents"            "$CLAUDE_DIR/agents/studio-kit"
echo "Done. Start a new Claude Code session to load them."
