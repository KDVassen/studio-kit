#!/usr/bin/env bash
# Bring every unmodified studio fork up to date with its upstream. Run monthly (scheduled task) or by hand.
# Forks marked "modified": true in forks.json are skipped: their owner merges upstream fixes deliberately.
# Prints a markdown report; exits 0 even when some forks fail, so the report always arrives.
set -uo pipefail

KIT="$(cd "$(dirname "$0")/.." && pwd)"
GH="$(command -v gh || true)"
[ -z "$GH" ] && [ -x "/c/Program Files/GitHub CLI/gh.exe" ] && GH="/c/Program Files/GitHub CLI/gh.exe"
if [ -z "$GH" ]; then echo "sync-forks: GitHub CLI (gh) not found."; exit 1; fi
if ! "$GH" auth status >/dev/null 2>&1; then echo "sync-forks: gh is not logged in. Run: gh auth login"; exit 1; fi

echo "# Fork sync report — $(date +%Y-%m-%d)"
echo
echo "| Fork | Upstream | Result |"
echo "|---|---|---|"

ok=0; skipped=0; failed=0
while IFS=$'\t' read -r fork upstream modified; do
  if [ "$modified" = "True" ]; then
    echo "| $fork | $upstream | skipped (modified by the studio; merge upstream by hand) |"; skipped=$((skipped+1)); continue
  fi
  if out=$("$GH" repo sync "$fork" --source "$upstream" 2>&1); then
    echo "| $fork | $upstream | synced |"; ok=$((ok+1))
  else
    msg=$(echo "$out" | tr '\n' ' ' | cut -c1-120)
    echo "| $fork | $upstream | **failed:** $msg |"; failed=$((failed+1))
  fi
done < <(python -c "
import json
for f in json.load(open(r'$KIT/forks.json')):
    print(f['fork'], f['upstream'], f.get('modified', False), sep='\t')
")

echo
echo "**$ok synced, $skipped skipped, $failed failed.**"
[ "$failed" -gt 0 ] && echo "A failure usually means the fork has commits upstream does not. Check it on GitHub before forcing anything."
exit 0
