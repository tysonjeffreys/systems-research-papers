#!/usr/bin/env python3
"""Generate Markdown mirrors from LaTeX paper sources."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Dict, List, Sequence
from urllib.parse import quote, unquote


SAFE_MATH_COMMANDS = {
    "alpha",
    "beta",
    "gamma",
    "delta",
    "epsilon",
    "varepsilon",
    "zeta",
    "eta",
    "theta",
    "vartheta",
    "iota",
    "kappa",
    "lambda",
    "mu",
    "nu",
    "xi",
    "pi",
    "varpi",
    "rho",
    "varrho",
    "sigma",
    "varsigma",
    "tau",
    "upsilon",
    "phi",
    "varphi",
    "chi",
    "psi",
    "omega",
    "Gamma",
    "Delta",
    "Theta",
    "Lambda",
    "Xi",
    "Pi",
    "Sigma",
    "Upsilon",
    "Phi",
    "Psi",
    "Omega",
    "left",
    "right",
    "big",
    "Big",
    "bigg",
    "Bigg",
    "cdot",
    "times",
    "otimes",
    "oplus",
    "sum",
    "prod",
    "int",
    "iint",
    "iiint",
    "oint",
    "frac",
    "dfrac",
    "tfrac",
    "sqrt",
    "overline",
    "underline",
    "hat",
    "tilde",
    "bar",
    "vec",
    "dot",
    "ddot",
    "text",
    "textbf",
    "textit",
    "mathrm",
    "mathbf",
    "mathit",
    "mathbb",
    "mathcal",
    "mathsf",
    "mathtt",
    "mathop",
    "operatorname",
    "operatornamewithlimits",
    "leq",
    "le",
    "geq",
    "ge",
    "neq",
    "equiv",
    "approx",
    "sim",
    "propto",
    "in",
    "notin",
    "subset",
    "subseteq",
    "supset",
    "supseteq",
    "cup",
    "cap",
    "setminus",
    "forall",
    "exists",
    "nexists",
    "neg",
    "land",
    "lor",
    "to",
    "rightarrow",
    "leftarrow",
    "Rightarrow",
    "Leftarrow",
    "leftrightarrow",
    "Leftrightarrow",
    "mapsto",
    "implies",
    "iff",
    "partial",
    "nabla",
    "infty",
    "prime",
    "ldots",
    "cdots",
    "vdots",
    "ddots",
    "dots",
    "dagger",
    "downarrow",
    "uparrow",
    "top",
    "sin",
    "cos",
    "tan",
    "exp",
    "log",
    "ln",
    "min",
    "max",
    "argmin",
    "argmax",
    "det",
    "tr",
    "Pr",
    "mathbbm",
    "mathds",
    "begin",
    "end",
    "qquad",
    "quad",
    ",",
    ";",
    ":",
    "!",
    "left.",
    "right.",
    "mid",
    "vert",
    "Vert",
    "lVert",
    "rVert",
    "lvert",
    "rvert",
    "langle",
    "rangle",
    "lceil",
    "rceil",
    "lfloor",
    "rfloor",
    "binom",
    "choose",
    "lim",
    "sup",
    "inf",
    "mod",
    "bmod",
    "pmod",
    "over",
    "underbrace",
    "overbrace",
    "color",
    "tau",
    "epsilon",
}


@dataclass
class PaperResult:
    slug: str
    title: str
    version: str
    source_rel: PurePosixPath
    pdf_rel: PurePosixPath | None


def to_url_path(path: PurePosixPath) -> str:
    return quote(path.as_posix(), safe="/-._~")


def discover_papers(repo_root: Path) -> List[Path]:
    structured_root = repo_root / "papers"
    if structured_root.exists():
        structured = [
            item
            for item in sorted(structured_root.iterdir())
            if item.is_dir() and (item / "main.tex").exists()
        ]
        if structured:
            return structured

    return [
        item
        for item in sorted(repo_root.iterdir())
        if item.is_dir() and (item / "main.tex").exists()
    ]


def slugify(name: str) -> str:
    cleaned = re.sub(
        r"^\s*v\d+(?:\.\d+)*(?:\s*[-_:|]\s*|\s+)?",
        "",
        name,
        flags=re.IGNORECASE,
    ).strip()
    base = cleaned if cleaned else name
    slug = re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-")
    return slug or "paper"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_title_from_tex(tex_text: str, fallback: str) -> str:
    title_match = re.search(r"\\title\{([^{}]+)\}", tex_text)
    if title_match:
        return cleanup_latex_text(title_match.group(1))

    large_line = re.search(
        r"\{\\(?:LARGE|Large|large|huge|Huge)(?:\\bfseries)?\s*([^{}]+?)\\par\}",
        tex_text,
    )
    if large_line:
        return cleanup_latex_text(large_line.group(1))

    stripped = re.sub(r"^\s*v\d+(?:\.\d+)*(?:\s*[-_:|]\s*|\s+)?", "", fallback)
    return stripped.strip() or fallback


def cleanup_latex_text(text: str) -> str:
    cleaned = text.replace(r"\\", " ")
    cleaned = re.sub(r"\\[a-zA-Z]+\s*", "", cleaned)
    cleaned = cleaned.replace(r"\&", "&")
    cleaned = cleaned.replace("~", " ")
    cleaned = cleaned.replace("{", "").replace("}", "")
    return " ".join(cleaned.split())


def extract_version(dir_name: str, tex_text: str, version_path: Path) -> str:
    if version_path.exists():
        raw = version_path.read_text(encoding="utf-8").strip()
        match = re.search(r"(\d+(?:\.\d+){0,2})", raw)
        if match:
            return f"v{match.group(1)}"

    dir_match = re.match(r"^\s*v(\d+(?:\.\d+){0,2})", dir_name, flags=re.IGNORECASE)
    if dir_match:
        return f"v{dir_match.group(1)}"

    version_match = re.search(r"Version\s+(\d+(?:\.\d+){0,2})", tex_text)
    if version_match:
        return f"v{version_match.group(1)}"

    return "v0.0.0"


def choose_pdf_name(paper_dir: Path) -> str | None:
    preferred = [
        paper_dir / "latest.pdf",
        paper_dir / f"{paper_dir.name}.pdf",
        paper_dir / "source.pdf",
        paper_dir / "main.pdf",
    ]
    for item in preferred:
        if item.exists():
            return item.name

    pdfs = [path for path in paper_dir.glob("*.pdf") if path.is_file()]
    if not pdfs:
        return None

    pdfs.sort(key=lambda item: item.stat().st_mtime, reverse=True)
    return pdfs[0].name


def run_pandoc(tex_path: Path) -> str:
    cmd = [
        "pandoc",
        str(tex_path),
        "--from=latex",
        "--to=markdown+tex_math_dollars",
        "--wrap=none",
        "--standalone",
    ]
    completed = subprocess.run(
        cmd,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout


def remove_div_wrappers(md_text: str) -> str:
    lines: List[str] = []
    for line in md_text.splitlines():
        stripped = line.strip()
        if re.match(r"^:::\s*(\{[^}]*\}|[A-Za-z0-9_.-]+)?\s*$", stripped):
            continue
        if stripped.startswith("<div ") and stripped.endswith(">"):
            continue
        if stripped == "</div>":
            continue
        line = re.sub(r"^(#{1,6}\s+.*)\s+\{#[^}]+\}\s*$", r"\1", line)
        lines.append(line.rstrip())
    return "\n".join(lines).strip() + "\n"


def normalize_math_delimiters(md_text: str) -> str:
    md_text = re.sub(
        r"\\\[(.*?)\\\]",
        lambda m: f"$$\n{m.group(1).strip()}\n$$",
        md_text,
        flags=re.DOTALL,
    )
    md_text = re.sub(
        r"\\\((.*?)\\\)",
        lambda m: f"${m.group(1).strip()}$",
        md_text,
        flags=re.DOTALL,
    )
    return md_text


def drop_leading_title_block(md_text: str) -> str:
    lines = md_text.splitlines()
    search_window = min(len(lines), 80)

    version_idx = -1
    for idx in range(search_window):
        if re.match(r"^Version\s+v?\d", lines[idx].strip(), flags=re.IGNORECASE):
            version_idx = idx
            break

    if version_idx == -1:
        return md_text

    cut = version_idx + 1
    while cut < len(lines) and not lines[cut].strip():
        cut += 1

    trimmed = "\n".join(lines[cut:]).lstrip("\n")
    return trimmed if trimmed.endswith("\n") else trimmed + "\n"


def strip_macro_definition_lines(md_text: str) -> str:
    output = []
    for line in md_text.splitlines():
        if re.search(r"\\newcommand|\\def\\", line):
            continue
        output.append(line)
    return "\n".join(output).strip() + "\n"


def parse_simple_macros(tex_text: str) -> Dict[str, str]:
    preamble = tex_text.split(r"\begin{document}", 1)[0]
    macros: Dict[str, str] = {}

    for match in re.finditer(
        r"\\(?:re)?newcommand\s*\{\\([A-Za-z]+)\}\s*(?:\[(\d+)\])?\s*\{([^}]*)\}",
        preamble,
    ):
        argc = match.group(2)
        replacement = match.group(3).strip()
        if argc and argc != "0":
            continue
        if "#" in replacement:
            continue
        macros[f"\\{match.group(1)}"] = replacement

    for match in re.finditer(r"\\def\\([A-Za-z]+)\s*\{([^}]*)\}", preamble):
        replacement = match.group(2).strip()
        if "#" in replacement:
            continue
        macros[f"\\{match.group(1)}"] = replacement

    return macros


def apply_macros_to_math(md_text: str, macros: Dict[str, str]) -> str:
    if not macros:
        return md_text

    ordered = sorted(macros.items(), key=lambda item: len(item[0]), reverse=True)

    def replace_tokens(segment: str) -> str:
        value = segment
        for _ in range(4):
            changed = False
            for macro, replacement in ordered:
                updated = re.sub(
                    rf"{re.escape(macro)}(?![A-Za-z])",
                    replacement,
                    value,
                )
                if updated != value:
                    changed = True
                    value = updated
            if not changed:
                break
        return value

    md_text = re.sub(
        r"\$\$(.+?)\$\$",
        lambda m: "$$" + replace_tokens(m.group(1)) + "$$",
        md_text,
        flags=re.DOTALL,
    )
    md_text = re.sub(
        r"(?<!\$)\$(?!\$)(.+?)(?<!\\)\$(?!\$)",
        lambda m: "$" + replace_tokens(m.group(1)) + "$",
        md_text,
        flags=re.DOTALL,
    )
    return md_text


def rewrite_image_links(md_text: str, source_rel: PurePosixPath) -> str:
    def transform(match: re.Match[str]) -> str:
        alt = match.group(1)
        target = match.group(2).strip()
        if not target:
            return match.group(0)

        normalized = target
        suffix = ""
        if target.startswith("<") and target.endswith(">"):
            normalized = target[1:-1]
        else:
            split = target.split(maxsplit=1)
            normalized = split[0]
            if len(split) > 1:
                suffix = " " + split[1]

        if normalized.startswith(("http://", "https://", "data:", "#", "/", "../")):
            return match.group(0)

        rewritten = to_url_path(source_rel / normalized)
        if target.startswith("<") and target.endswith(">"):
            return f"![{alt}](<{rewritten}>)"
        return f"![{alt}]({rewritten}{suffix})"

    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", transform, md_text)


def extract_title_from_md(md_text: str, fallback: str) -> str:
    for line in md_text.splitlines()[:120]:
        stripped = line.strip()
        if stripped.startswith("# "):
            break
        title_match = re.match(r"^\*\*(.+)\*\*$", stripped)
        if title_match:
            candidate = title_match.group(1).replace(r"\\", " ").strip()
            if candidate.lower().startswith("series note"):
                continue
            if len(candidate.split()) >= 3:
                return candidate

    return fallback


def extract_math_segments(md_text: str) -> List[str]:
    block_segments = re.findall(r"\$\$(.+?)\$\$", md_text, flags=re.DOTALL)
    text_without_blocks = re.sub(r"\$\$(.+?)\$\$", " ", md_text, flags=re.DOTALL)
    inline_segments = re.findall(
        r"(?<!\$)\$(?!\$)(.+?)(?<!\\)\$(?!\$)",
        text_without_blocks,
        flags=re.DOTALL,
    )
    return block_segments + inline_segments


def find_unknown_math_commands(md_text: str) -> List[str]:
    unknown = set()
    for segment in extract_math_segments(md_text):
        for command in re.findall(r"\\([A-Za-z]+)", segment):
            if command not in SAFE_MATH_COMMANDS:
                unknown.add(f"\\{command}")
    return sorted(unknown)


def find_remaining_macro_defs(md_text: str) -> List[str]:
    findings = []
    for line_number, line in enumerate(md_text.splitlines(), start=1):
        if re.search(r"\\newcommand|\\def\\", line):
            findings.append(f"line {line_number}: {line.strip()}")
    return findings


def find_broken_image_links(md_text: str, md_file_path: Path) -> List[str]:
    broken = []
    for match in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", md_text):
        target = match.group(1).strip()
        if not target:
            continue

        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        else:
            target = target.split(maxsplit=1)[0]

        if target.startswith(("http://", "https://", "data:", "#")):
            continue

        normalized = target.split("#", 1)[0].split("?", 1)[0]
        if not normalized:
            continue

        resolved = (md_file_path.parent / unquote(normalized)).resolve()
        if not resolved.exists():
            broken.append(target)
    return sorted(set(broken))


def build_header(
    title: str,
    version: str,
    source_rel: PurePosixPath,
    pdf_rel: PurePosixPath | None,
    changelog_rel: PurePosixPath | None,
) -> str:
    lines = [
        f"# {title}",
        "",
        f"**Version:** {version}  ",
    ]

    if pdf_rel is None:
        lines.append("**PDF:** (not found)  ")
    else:
        lines.append(f"**PDF:** {to_url_path(pdf_rel)}  ")

    lines.append(f"**Source:** {to_url_path(source_rel)}/  ")

    if changelog_rel is not None:
        lines.append(f"**Changelog:** {to_url_path(changelog_rel)}")
    else:
        lines.append("**Changelog:** (not found)")

    lines.extend(
        [
            "",
            "> Markdown mirror: best-effort rendering for GitHub. Canonical artifact is the PDF.",
            "",
        ]
    )
    return "\n".join(lines)


def build_audit(
    title: str,
    source_rel: PurePosixPath,
    mirror_name: str,
    remaining_macros: Sequence[str],
    unknown_commands: Sequence[str],
    broken_images: Sequence[str],
) -> str:
    lines = [
        f"# Audit: {title}",
        "",
        f"- Source: {to_url_path(source_rel / 'main.tex')}",
        f"- Mirror: ./{mirror_name}",
        "",
        "## Remaining macro definitions in mirror",
    ]

    if remaining_macros:
        lines.extend(f"- {item}" for item in remaining_macros)
    else:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## Commands still present in math (check GitHub rendering)",
        ]
    )
    if unknown_commands:
        lines.extend(f"- `{item}`" for item in unknown_commands)
    else:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## Broken image links",
        ]
    )
    if broken_images:
        lines.extend(f"- `{item}`" for item in broken_images)
    else:
        lines.append("- None")

    lines.append("")
    return "\n".join(lines)


def ensure_unique_slug(base: str, used: set[str]) -> str:
    if base not in used:
        used.add(base)
        return base

    suffix = 2
    while f"{base}-{suffix}" in used:
        suffix += 1
    unique = f"{base}-{suffix}"
    used.add(unique)
    return unique


def generate(
    repo_root: Path,
    mirror_filename: str,
    audit_filename: str,
) -> List[PaperResult]:
    papers = discover_papers(repo_root)
    if not papers:
        raise RuntimeError("No paper directories containing main.tex were found.")

    used_slugs: set[str] = set()
    results: List[PaperResult] = []

    for paper_dir in papers:
        tex_path = paper_dir / "main.tex"
        tex_text = read_text(tex_path)

        raw_md = run_pandoc(tex_path)
        title_fallback = extract_title_from_tex(tex_text, paper_dir.name)
        title = extract_title_from_md(raw_md, title_fallback)
        version = extract_version(paper_dir.name, tex_text, paper_dir / "VERSION")
        macros = parse_simple_macros(tex_text)
        pdf_name = choose_pdf_name(paper_dir)

        cleaned = remove_div_wrappers(raw_md)
        cleaned = normalize_math_delimiters(cleaned)
        cleaned = drop_leading_title_block(cleaned)
        cleaned = apply_macros_to_math(cleaned, macros)
        cleaned = strip_macro_definition_lines(cleaned)

        source_rel = PurePosixPath(".")
        cleaned = rewrite_image_links(cleaned, source_rel)

        slug = ensure_unique_slug(slugify(paper_dir.name), used_slugs)
        md_path = paper_dir / mirror_filename
        audit_path = paper_dir / audit_filename

        changelog_path = paper_dir / "CHANGELOG.md"
        pdf_rel = PurePosixPath(pdf_name) if pdf_name else None
        changelog_rel = PurePosixPath("CHANGELOG.md") if changelog_path.exists() else None

        header = build_header(title, version, source_rel, pdf_rel, changelog_rel)
        full_md = header + cleaned
        if not full_md.endswith("\n"):
            full_md += "\n"
        md_path.write_text(full_md, encoding="utf-8")

        remaining_macros = find_remaining_macro_defs(full_md)
        unknown_commands = find_unknown_math_commands(full_md)
        broken_images = find_broken_image_links(full_md, md_path)

        audit_text = build_audit(
            title=title,
            source_rel=source_rel,
            mirror_name=md_path.name,
            remaining_macros=remaining_macros,
            unknown_commands=unknown_commands,
            broken_images=broken_images,
        )
        audit_path.write_text(audit_text, encoding="utf-8")

        results.append(
            PaperResult(
                slug=slug,
                title=title,
                version=version,
                source_rel=PurePosixPath(*paper_dir.relative_to(repo_root).parts),
                pdf_rel=pdf_rel,
            )
        )

    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Path to repository root (default: current directory).",
    )
    parser.add_argument(
        "--mirror-filename",
        default="mirror.md",
        help="Filename for colocated markdown mirrors (default: mirror.md).",
    )
    parser.add_argument(
        "--audit-filename",
        default="mirror.audit.md",
        help="Filename for colocated audit reports (default: mirror.audit.md).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()

    try:
        results = generate(
            repo_root,
            mirror_filename=args.mirror_filename,
            audit_filename=args.audit_filename,
        )
    except subprocess.CalledProcessError as error:
        print(error.stderr or str(error), file=sys.stderr)
        return 1
    except Exception as error:  # pragma: no cover - command-line tool
        print(str(error), file=sys.stderr)
        return 1

    print(
        f"Generated {len(results)} colocated markdown mirrors as "
        f"{args.mirror_filename} and {args.audit_filename}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
