"""Copy the campaign's notes from the owner's Obsidian vault into vault/ in this repo.

Usage: python3 tools/sync_vault.py [path-to-campaign-folder]
The build (and GitHub) reads vault/, so run this, rebuild and commit whenever the vault has changed.
Only Markdown files in CAMPAIGN["vault_folders"] are copied (hidden folders such as .nthing-history are
skipped); files that disappeared from the vault are removed from vault/. The vault itself is only read.
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(__file__))
from curation import CAMPAIGN  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(ROOT, "vault")
SRC = sys.argv[1] if len(sys.argv) > 1 else CAMPAIGN["vault_source"]

wanted = set()
for folder in CAMPAIGN["vault_folders"]:
    base = os.path.join(SRC, folder)
    if not os.path.isdir(base):
        sys.exit(f"missing folder in the vault: {base}")
    for dirpath, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in files:
            if f.endswith(".md"):
                wanted.add(os.path.relpath(os.path.join(dirpath, f), SRC))

copied = removed = 0
for rel in sorted(wanted):
    src, dst = os.path.join(SRC, rel), os.path.join(DEST, rel)
    if not os.path.exists(dst) or open(src, "rb").read() != open(dst, "rb").read():
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
        copied += 1
for dirpath, _, files in os.walk(DEST, topdown=False):
    for f in files:
        rel = os.path.relpath(os.path.join(dirpath, f), DEST)
        if rel not in wanted:
            os.remove(os.path.join(dirpath, f))
            removed += 1
    if dirpath != DEST and not os.listdir(dirpath):
        os.rmdir(dirpath)
print(f"vault/: {len(wanted)} notes ({copied} new or changed, {removed} removed)")
