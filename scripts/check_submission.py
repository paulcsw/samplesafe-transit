#!/usr/bin/env python3
"""Validate the SampleSafe Transit MYOSA submission scaffold."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


FRONTMATTER_KEYS = ("title", "publishDate", "excerpt", "image", "tags")

REQUIRED_HEADINGS = (
    "Overview",
    "Images",
    "Videos",
    "Features",
    "Usage",
    "Tech Stack",
    "Installation",
)

MEDIA_EXTENSIONS = {".jpg", ".jpeg", ".png", ".mp4"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
VIDEO_EXTENSIONS = {".mp4"}
YOUTUBE_RE = re.compile(r"https?://(?:www\.)?(?:youtube\.com|youtu\.be)\S*", re.IGNORECASE)
MD_LINK_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
HTML_SRC_RE = re.compile(r"<(?:video|img|source)\b[^>]*\bsrc=[\"']([^\"']+)[\"']", re.IGNORECASE)


class CheckResult:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warning(self, message: str) -> None:
        self.warnings.append(message)


def normalize_ref(ref: str) -> str:
    return ref.strip().split("#", 1)[0].split("?", 1)[0]


def is_url(ref: str) -> bool:
    return ref.startswith("http://") or ref.startswith("https://")


def parse_frontmatter(text: str, result: CheckResult) -> dict[str, str]:
    if not text.startswith("---\n"):
        result.error("frontmatter block is missing")
        return {}

    end = text.find("\n---", 4)
    if end == -1:
        result.error("frontmatter closing marker is missing")
        return {}

    block = text[4:end].strip().splitlines()
    data: dict[str, str] = {}
    for line in block:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')

    for key in FRONTMATTER_KEYS:
        if key not in data:
            result.error(f"frontmatter key missing: {key}")
        elif key != "tags" and not data[key]:
            result.error(f"frontmatter key is empty: {key}")

    return data


def heading_body(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$([\s\S]*?)(?=^##\s+|\Z)",
        re.IGNORECASE | re.MULTILINE,
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def validate_headings(text: str, result: CheckResult) -> None:
    for heading in REQUIRED_HEADINGS:
        body = heading_body(text, heading)
        if not body:
            result.error(f"required heading missing or empty: ## {heading}")


def extract_media_refs(text: str, frontmatter: dict[str, str]) -> list[str]:
    refs = [normalize_ref(match.group(1)) for match in MD_LINK_RE.finditer(text)]
    refs.extend(normalize_ref(match.group(1)) for match in HTML_SRC_RE.finditer(text))

    image = frontmatter.get("image", "")
    if image:
        refs.append(normalize_ref(image))

    return [ref for ref in refs if Path(ref).suffix.lower() in MEDIA_EXTENSIONS or is_url(ref)]


def validate_media(markdown_path: Path, refs: list[str], result: CheckResult) -> None:
    root = markdown_path.parent
    seen: set[str] = set()
    images: list[str] = []
    videos: list[str] = []

    for ref in refs:
        if ref in seen:
            continue
        seen.add(ref)

        if is_url(ref):
            result.error(f"media reference must be local, not URL: {ref}")
            continue

        ref_path = Path(ref)
        filename = ref_path.name
        suffix = ref_path.suffix.lower()

        if ref_path.parent not in (Path("."), Path("")):
            result.error(f"media must live in the same folder as markdown: {ref}")

        if filename != filename.lower():
            result.error(f"media filename must be lowercase: {filename}")

        if " " in filename:
            result.error(f"media filename must not contain spaces: {filename}")

        if suffix in IMAGE_EXTENSIONS:
            images.append(ref)
        elif suffix in VIDEO_EXTENSIONS:
            videos.append(ref)

        if not (root / filename).exists():
            result.error(f"referenced media file is missing: {filename}")

    if "./samplesafe-cover.jpg" not in seen and "samplesafe-cover.jpg" not in seen:
        result.error("cover image must be referenced as samplesafe-cover.jpg")

    if not (root / "samplesafe-cover.jpg").exists():
        result.error("cover image file is missing: samplesafe-cover.jpg")

    if not videos:
        result.error("local mp4 video reference is missing")

    if "./samplesafe-demo.mp4" not in seen and "samplesafe-demo.mp4" not in seen:
        result.error("demo video must be referenced as samplesafe-demo.mp4")

    if not (root / "samplesafe-demo.mp4").exists():
        result.error("demo video file is missing: samplesafe-demo.mp4")

    if not images:
        result.error("at least one local image reference is required")


def validate_repo_media_files(markdown_path: Path, result: CheckResult) -> None:
    for path in markdown_path.parent.iterdir():
        if not path.is_file():
            continue
        if path.suffix.lower() not in MEDIA_EXTENSIONS:
            continue
        if path.name != path.name.lower():
            result.error(f"root media filename must be lowercase: {path.name}")
        if " " in path.name:
            result.error(f"root media filename must not contain spaces: {path.name}")


def validate_text(text: str, result: CheckResult) -> None:
    if YOUTUBE_RE.search(text):
        result.error("YouTube links are not allowed")

    if "diagnostic device" in text.lower() and "not a diagnostic device" not in text.lower():
        result.warning("diagnostic wording found; make sure it is framed as a non-diagnostic prototype")

    for heading in ("Features", "Usage", "Tech Stack", "Installation"):
        body = heading_body(text, heading)
        non_empty_lines = [line.strip() for line in body.splitlines() if line.strip()]
        if len(non_empty_lines) < 3:
            result.error(f"section is too thin: ## {heading}")


def run(markdown_path: Path) -> CheckResult:
    result = CheckResult()

    if not markdown_path.exists():
        result.error(f"markdown file does not exist: {markdown_path}")
        return result

    if markdown_path.name != "samplesafe-transit.md":
        result.error("submission markdown must be named samplesafe-transit.md")

    text = markdown_path.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(text, result)
    validate_headings(text, result)
    validate_text(text, result)
    validate_media(markdown_path, extract_media_refs(text, frontmatter), result)
    validate_repo_media_files(markdown_path, result)

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate MYOSA SampleSafe submission files.")
    parser.add_argument("markdown", nargs="?", default="samplesafe-transit.md")
    args = parser.parse_args()

    markdown_path = Path(args.markdown).resolve()
    result = run(markdown_path)

    for warning in result.warnings:
        print(f"WARN: {warning}")

    for error in result.errors:
        print(f"ERROR: {error}")

    if result.errors:
        print(f"FAIL: {len(result.errors)} error(s), {len(result.warnings)} warning(s)")
        return 1

    print(f"PASS: 0 error(s), {len(result.warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
