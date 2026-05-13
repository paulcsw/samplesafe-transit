#!/usr/bin/env python3
"""Validate the SampleSafe Transit MYOSA submission package.

This validator intentionally checks the stricter official MYOSA blog structure:
frontmatter, tagline, official section names, local JPG/PNG images, local MP4 video,
lowercase/no-space media filenames, and no YouTube links.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FRONTMATTER_KEYS = ("publishDate", "title", "excerpt", "image", "tags")
REQUIRED_H2 = (
    "Acknowledgements",
    "Overview",
    "Demo / Examples",
    "Features (Detailed)",
    "Usage Instructions",
    "Tech Stack",
    "Requirements / Installation",
)
REQUIRED_H3 = ("Images", "Videos")
MEDIA_EXTENSIONS = {".jpg", ".jpeg", ".png", ".mp4"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
VIDEO_EXTENSIONS = {".mp4"}
YOUTUBE_RE = re.compile(r"https?://(?:www\.)?(?:youtube\.com|youtu\.be)\S*", re.IGNORECASE)
MD_LINK_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
HTML_SRC_RE = re.compile(r"<(?:video|img|source)\b[^>]*\bsrc=[\"']([^\"']+)[\"']", re.IGNORECASE)
VIDEO_SOURCE_RE = re.compile(r"<video\b[\s\S]*?<source\b[^>]*src=[\"'][^\"']+\.mp4[\"'][^>]*type=[\"']video/mp4[\"'][^>]*>[\s\S]*?</video>", re.IGNORECASE)


class CheckResult:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warning(self, message: str) -> None:
        self.warnings.append(message)


def normalize_ref(ref: str) -> str:
    ref = ref.strip().split("#", 1)[0].split("?", 1)[0]
    if ref.startswith("./"):
        ref = ref[2:]
    if ref.startswith("/"):
        ref = ref[1:]
    return ref


def is_url(ref: str) -> bool:
    return ref.startswith("http://") or ref.startswith("https://")


def parse_frontmatter(text: str, result: CheckResult) -> tuple[dict[str, str], int]:
    if not text.startswith("---\n"):
        result.error("frontmatter block is missing")
        return {}, 0

    end = text.find("\n---", 4)
    if end == -1:
        result.error("frontmatter closing marker is missing")
        return {}, 0

    block = text[4:end].strip().splitlines()
    data: dict[str, str] = {}
    for line in block:
        if not line.strip() or line.lstrip().startswith("-") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')

    for key in FRONTMATTER_KEYS:
        if key not in data:
            result.error(f"frontmatter key missing: {key}")
        elif key != "tags" and not data[key]:
            result.error(f"frontmatter key is empty: {key}")

    return data, end + 4


def heading_body(text: str, level: int, heading: str) -> str:
    hashes = "#" * level
    pattern = re.compile(
        rf"^{hashes}\s+{re.escape(heading)}\s*$([\s\S]*?)(?=^##\s+|\Z)",
        re.IGNORECASE | re.MULTILINE,
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def has_heading(text: str, level: int, heading: str) -> bool:
    hashes = "#" * level
    return re.search(rf"^{hashes}\s+{re.escape(heading)}\s*$", text, re.IGNORECASE | re.MULTILINE) is not None


def validate_headings(text: str, result: CheckResult) -> None:
    for heading in REQUIRED_H2:
        if not has_heading(text, 2, heading):
            result.error(f"required heading missing: ## {heading}")
        elif not heading_body(text, 2, heading):
            result.error(f"required heading is empty: ## {heading}")

    for heading in REQUIRED_H3:
        if not has_heading(text, 3, heading):
            result.error(f"required subheading missing: ### {heading}")


def validate_tagline(text: str, frontmatter_end: int, result: CheckResult) -> None:
    after = text[frontmatter_end:].lstrip().splitlines()
    first_nonempty = next((line.strip() for line in after if line.strip()), "")
    if not first_nonempty.startswith(">"):
        result.error("one-line project tagline after frontmatter is missing")


def extract_media_refs(text: str, frontmatter: dict[str, str]) -> list[str]:
    refs = [match.group(1).strip() for match in MD_LINK_RE.finditer(text)]
    refs.extend(match.group(1).strip() for match in HTML_SRC_RE.finditer(text))
    image = frontmatter.get("image", "")
    if image:
        refs.append(image)
    return [ref for ref in refs if Path(normalize_ref(ref)).suffix.lower() in MEDIA_EXTENSIONS or is_url(ref)]


def validate_media(markdown_path: Path, refs: list[str], result: CheckResult) -> None:
    root = markdown_path.parent
    seen: set[str] = set()
    images: list[str] = []
    videos: list[str] = []

    for raw_ref in refs:
        if is_url(raw_ref):
            result.error(f"media reference must be local, not URL: {raw_ref}")
            continue

        ref = normalize_ref(raw_ref)
        if ref in seen:
            continue
        seen.add(ref)

        ref_path = Path(ref)
        filename = ref_path.name
        suffix = ref_path.suffix.lower()

        if ref_path.parent not in (Path("."), Path("")):
            result.error(f"media must live in the same folder as markdown: {raw_ref}")

        if filename != filename.lower():
            result.error(f"media filename must be lowercase: {filename}")
        if " " in filename:
            result.error(f"media filename must not contain spaces: {filename}")

        if suffix in IMAGE_EXTENSIONS:
            images.append(filename)
        elif suffix in VIDEO_EXTENSIONS:
            videos.append(filename)

        if not (root / filename).exists():
            result.error(f"referenced media file is missing: {filename}")

    if "samplesafe-cover.jpg" not in seen:
        result.error("cover image must be referenced as samplesafe-cover.jpg")
    if not (root / "samplesafe-cover.jpg").exists():
        result.error("cover image file is missing: samplesafe-cover.jpg")
    if "samplesafe-demo.mp4" not in seen:
        result.error("demo video must be referenced as samplesafe-demo.mp4")
    if not (root / "samplesafe-demo.mp4").exists():
        result.error("demo video file is missing: samplesafe-demo.mp4")
    if not images:
        result.error("at least one local JPG/PNG image reference is required")
    if not videos:
        result.error("at least one local MP4 video reference is required")


def validate_repo_media_files(markdown_path: Path, result: CheckResult) -> None:
    for path in markdown_path.parent.iterdir():
        if not path.is_file() or path.suffix.lower() not in MEDIA_EXTENSIONS:
            continue
        if path.name != path.name.lower():
            result.error(f"root media filename must be lowercase: {path.name}")
        if " " in path.name:
            result.error(f"root media filename must not contain spaces: {path.name}")
        if path.suffix.lower() not in MEDIA_EXTENSIONS:
            result.error(f"unsupported media extension: {path.name}")


def validate_text(text: str, result: CheckResult) -> None:
    if YOUTUBE_RE.search(text):
        result.error("YouTube links are not allowed")
    if "diagnostic device" in text.lower() and "not a diagnostic device" not in text.lower():
        result.warning("diagnostic wording found; make sure it is framed as a non-diagnostic prototype")
    if not VIDEO_SOURCE_RE.search(text):
        result.error("video must use the official <video><source ... type=\"video/mp4\"></video> format")

    for heading in ("Features (Detailed)", "Usage Instructions", "Tech Stack", "Requirements / Installation"):
        body = heading_body(text, 2, heading)
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
    frontmatter, frontmatter_end = parse_frontmatter(text, result)
    validate_tagline(text, frontmatter_end, result)
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
