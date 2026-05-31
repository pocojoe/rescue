#!/usr/bin/env python3
"""
run.py -- rescue zip recover-side bootstrap (v1.0).

rescue 1.0
Copyright (c) 2026 Joseph M. Miller MD MPH
SPDX-License-Identifier: MIT
Source: github.com/pocojoe/rescue

This file is INSIDE the rescue zip. It executes in the fresh
chat's sandbox after the operator uploads the rescue zip and
instructs the chat to read the README and follow its
instructions.

Behavior:
  1. Verify SHA-256 of every file in this zip against
     SHA256SUMS. Abort on any mismatch.
  2. Unpack workdir.tar.gz into a read-only staging directory
     under the sandbox's filesystem. Preserve symlinks where
     the platform supports them; warn otherwise.
  3. Read state.txt, parse the five labeled axes.
  4. Emit the five axes to stdout in a form the chat can
     absorb into context.
  5. Emit a flat list of carry-forward files (name and size
     from manifest.txt) so the operator sees the inventory.
  6. Emit a two-stage continuity prompt:
       Stage 1: extract all carry-forward files as a separate
                zip? [y/N] (default No; Enter skips)
       Stage 2: how to proceed? Resume prior work OR
                Start fresh.

The chat reads the emitted axes and prompts on the next
operator turn and proceeds per operator response.
"""

import hashlib
import os
import platform
import sys
import tarfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
STAGE = HERE / "_recovered_workdir"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_hashes():
    sums_path = HERE / "SHA256SUMS"
    if not sums_path.exists():
        print("ERROR: SHA256SUMS missing", file=sys.stderr)
        sys.exit(1)
    failures = []
    for line in sums_path.read_text().splitlines():
        if not line.strip():
            continue
        expected, name = line.split(None, 1)
        name = name.strip()
        actual = sha256_file(HERE / name)
        if actual != expected:
            failures.append((name, expected, actual))
    if failures:
        print("ERROR: hash mismatch:", file=sys.stderr)
        for name, expected, actual in failures:
            print(f"  {name}: expected {expected}, got {actual}",
                  file=sys.stderr)
        sys.exit(1)
    print(f"VERIFIED: {sums_path.name} ({len(sums_path.read_text().splitlines())} files)",
          file=sys.stderr)


def stage_workdir():
    """Unpack workdir.tar.gz into STAGE. Preserve symlinks
    where supported; warn if the platform cannot recreate
    them cleanly."""
    tar_path = HERE / "workdir.tar.gz"
    if not tar_path.exists():
        print("ERROR: workdir.tar.gz missing", file=sys.stderr)
        sys.exit(1)
    STAGE.mkdir(parents=True, exist_ok=True)
    symlink_warnings = []
    with tarfile.open(tar_path, "r:gz") as tf:
        for member in tf.getmembers():
            try:
                tf.extract(member, STAGE)
            except (OSError, NotImplementedError) as e:
                if member.issym() or member.islnk():
                    symlink_warnings.append((member.name, str(e)))
                else:
                    raise
    if symlink_warnings:
        print("WARNING: symlinks could not be recreated on this",
              file=sys.stderr)
        print(f"platform ({platform.system()}):", file=sys.stderr)
        for name, err in symlink_warnings:
            print(f"  {name}: {err}", file=sys.stderr)
    # Mark staged tree read-only. Symlinks themselves are not
    # chmod'd (chmod follows the link on most platforms).
    for root, dirs, files in os.walk(STAGE):
        for d in dirs:
            p = Path(root) / d
            if not p.is_symlink():
                p.chmod(0o555)
        for f in files:
            p = Path(root) / f
            if not p.is_symlink():
                p.chmod(0o444)
    print(f"STAGED: workdir.tar.gz -> {STAGE} (read-only)",
          file=sys.stderr)


def emit_state():
    state_path = HERE / "state.txt"
    if not state_path.exists():
        print("ERROR: state.txt missing", file=sys.stderr)
        sys.exit(1)
    print(state_path.read_text())


def emit_inventory_and_prompts():
    """Emit the carry-forward file inventory (flat list, name
    and size from manifest.txt), followed by the two-stage
    continuity prompt."""
    manifest_path = HERE / "manifest.txt"
    entries = []
    if manifest_path.exists():
        for line in manifest_path.read_text().splitlines():
            if not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) >= 3:
                # Regular file: <sha256>\t<size>\t<path>
                # Symlink:      SYMLINK\t<target>\t<path>
                first, second, rel = parts[0], parts[1], parts[2]
                if first == "SYMLINK":
                    entries.append((rel, f"symlink -> {second}"))
                else:
                    entries.append((rel, f"{second} bytes"))
    print("")
    print("RECOVERY COMPLETE")
    print("-----------------")
    print("State restored. Five textual axes emitted above as")
    print("session context.")
    print("")
    print("Files carried forward in this rescue zip:")
    print("")
    if entries:
        for rel, descr in entries:
            print(f"  {rel}  ({descr})")
    else:
        print("  (none -- working directory was empty)")
    print("")
    print("These files are preserved in the archive and remain")
    print("readable from the original rescue zip offline.")
    print("")
    print("Extract all carry-forward files as a separate zip? [y/N]")
    print("")
    print("[Stage 1 -- await operator response.")
    print(" Enter or \"n\" or \"no\" -> skip extraction.")
    print(" \"y\" or \"yes\" -> chat writes")
    print(" mace-rescue-extract-<UTC timestamp>.zip to")
    print(" /mnt/user-data/outputs/ containing only the")
    print(" carry-forward files (no state.txt, no SHA256SUMS,")
    print(" no run.py). Chat reports path, size, SHA-256.")
    print(" Original rescue zip is not modified.")
    print("")
    print(" After Stage 1 resolves, chat emits Stage 2:]")
    print("")
    print("How to proceed?")
    print("")
    print("  Option 1 -- Resume prior work")
    print("    Type: \"Resume prior work.\"")
    print("    All carry-forward files will be mounted and")
    print("    accessible in chat.")
    print("")
    print("  Option 2 -- Start fresh")
    print("    Type: \"Start fresh.\"")
    print("    Restored context used as background. Working")
    print("    directory stays empty. Staged archive remains")
    print("    available if mind changes later.")
    print("")
    print("No work was lost. The full archive is preserved in")
    print("the rescue zip on disk and can be inspected offline")
    print("at any time.")


def main():
    print("rescue 1.0")
    print("Copyright (c) 2026 Joseph M. Miller MD MPH")
    print("MIT License (SPDX: MIT)")
    print("Source: github.com/pocojoe/rescue")
    print("")
    verify_hashes()
    stage_workdir()
    emit_state()
    emit_inventory_and_prompts()


if __name__ == "__main__":
    main()
