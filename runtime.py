"""Decode a trusted Railway application bundle and start the bot."""

from __future__ import annotations

import base64
import io
import os
from pathlib import Path
import tarfile


APP_ROOT = Path("/app").resolve()


def unpack_bundle() -> None:
    encoded = os.environ.get("APP_BUNDLE_B64", "")
    if not encoded:
        raise RuntimeError("APP_BUNDLE_B64 is required")

    archive_bytes = base64.b64decode(encoded, validate=True)
    with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:gz") as archive:
        members = archive.getmembers()
        for member in members:
            target = (APP_ROOT / member.name).resolve()
            if target != APP_ROOT and APP_ROOT not in target.parents:
                raise RuntimeError(f"Unsafe archive path: {member.name}")
            if member.issym() or member.islnk() or member.isdev():
                raise RuntimeError(f"Unsupported archive entry: {member.name}")
        archive.extractall(APP_ROOT, members=members)


if __name__ == "__main__":
    unpack_bundle()
    os.chdir(APP_ROOT)
    os.execvp("python", ["python", "-m", "app.main"])
