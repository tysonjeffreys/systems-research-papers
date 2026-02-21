import { promises as fs } from "fs";
import path from "path";
import { spawn } from "child_process";

const REPO_ROOT = process.cwd();

const SAFE_COMMANDS = new Set([
  "\\frac", "\\dfrac", "\\tfrac",
  "\\sum", "\\prod", "\\int", "\\iint", "\\iiint",
  "\\lim", "\\log", "\\ln", "\\exp",
  "\\sin", "\\cos", "\\tan", "\\cot", "\\sec", "\\csc",
  "\\sinh", "\\cosh", "\\tanh",
  "\\min", "\\max", "\\argmin", "\\argmax",
  "\\partial", "\\nabla",
  "\\cdot", "\\times", "\\otimes", "\\oplus",
  "\\le", "\\ge", "\\leq", "\\geq", "\\neq", "\\approx", "\\sim", "\\equiv", "\\propto",
  "\\in", "\\notin", "\\subset", "\\subseteq", "\\supset", "\\supseteq",
  "\\cup", "\\cap", "\\setminus",
  "\\forall", "\\exists",
  "\\to", "\\rightarrow", "\\leftarrow", "\\Rightarrow", "\\Leftrightarrow", "\\leftrightarrow",
  "\\mathbb", "\\mathbf", "\\mathrm", "\\mathcal", "\\mathsf", "\\mathit",
  "\\hat", "\\bar", "\\tilde", "\\vec", "\\dot", "\\ddot",
  "\\big", "\\Big", "\\bigg", "\\Bigg",
  "\\left", "\\right",
  "\\begin", "\\end",
  "\\operatorname", "\\operatornamewithlimits", "\\text",
  "\\alpha", "\\beta", "\\gamma", "\\delta", "\\epsilon", "\\varepsilon", "\\zeta", "\\eta", "\\theta", "\\vartheta",
  "\\iota", "\\kappa", "\\lambda", "\\mu", "\\nu", "\\xi", "\\pi", "\\rho", "\\varrho", "\\sigma", "\\tau", "\\upsilon",
  "\\phi", "\\varphi", "\\chi", "\\psi", "\\omega",
  "\\Gamma", "\\Delta", "\\Theta", "\\Lambda", "\\Xi", "\\Pi", "\\Sigma", "\\Upsilon", "\\Phi", "\\Psi", "\\Omega",
  "\\mid", "\\vert", "\\Vert", "\\lVert", "\\rVert", "\\lvert", "\\rvert",
  "\\langle", "\\rangle", "\\lceil", "\\rceil", "\\lfloor", "\\rfloor",
  "\\overline", "\\underline", "\\sqrt", "\\overbrace", "\\underbrace",
  "\\quad", "\\qquad", "\\dots", "\\ldots", "\\cdots", "\\vdots", "\\ddots",
  "\\downarrow", "\\uparrow", "\\dagger", "\\top",
]);

function run(cmd, args, opts = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(cmd, args, { stdio: "pipe", ...opts });
    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (d) => (stdout += d.toString()));
    child.stderr.on("data", (d) => (stderr += d.toString()));
    child.on("close", (code) => {
      if (code === 0) resolve({ stdout, stderr });
      else reject(new Error(`Command failed (${code}): ${cmd} ${args.join(" ")}\n${stderr}`));
    });
  });
}

async function exists(p) {
  try {
    await fs.access(p);
    return true;
  } catch {
    return false;
  }
}

async function readText(p) {
  return fs.readFile(p, "utf8");
}

async function writeText(p, content) {
  await fs.mkdir(path.dirname(p), { recursive: true });
  await fs.writeFile(p, content, "utf8");
}

function slugToTitle(slug) {
  return slug
    .split("-")
    .map((w) => (w.length ? w[0].toUpperCase() + w.slice(1) : w))
    .join(" ");
}

function cleanupLatexInline(raw) {
  let text = raw.replace(/\\\\/g, " ");
  text = text.replace(/\\[A-Za-z]+\*?(?:\[[^\]]*\])?/g, " ");
  text = text.replace(/[{}]/g, " ");
  text = text.replace(/\s+/g, " ").trim();
  return text;
}

function extractTitle(tex) {
  const explicit = tex.match(/\\title\s*\{([\s\S]*?)\}/m);
  if (explicit) return cleanupLatexInline(explicit[1]);

  const large = tex.match(/\{\\(?:LARGE|Large|large|Huge|huge)(?:\\bfseries)?\s*([^{}]+?)\\par\}/m);
  if (!large) return null;
  return cleanupLatexInline(large[1]);
}

function splitPreambleAndBody(tex) {
  const idx = tex.search(/\\begin\s*\{\s*document\s*\}/i);
  if (idx === -1) return { preamble: tex, body: "" };
  return { preamble: tex.slice(0, idx), body: tex.slice(idx) };
}

function extractZeroArgMacros(preamble) {
  const map = new Map();

  for (const m of preamble.matchAll(/\\newcommand\s*\{\\([A-Za-z]+)\}\s*\{([\s\S]*?)\}/g)) {
    const name = `\\${m[1]}`;
    const body = m[2].trim();
    if (body) map.set(name, body);
  }

  for (const m of preamble.matchAll(/\\newcommand\s*\{\\([A-Za-z]+)\}\s*\[0\]\s*\{([\s\S]*?)\}/g)) {
    const name = `\\${m[1]}`;
    const body = m[2].trim();
    if (body) map.set(name, body);
  }

  for (const m of preamble.matchAll(/\\def\s*\\([A-Za-z]+)\s*\{([\s\S]*?)\}/g)) {
    const name = `\\${m[1]}`;
    const body = m[2].trim();
    if (body) map.set(name, body);
  }

  return map;
}

function escapeRegExp(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function normalizeMathDelimiters(md) {
  md = md.replace(/\\\(([\s\S]*?)\\\)/g, (_m, inner) => `$${inner}$`);
  md = md.replace(/\\\[([\s\S]*?)\\\]/g, (_m, inner) => `$$\n${inner}\n$$`);
  return md;
}

function stripLatexMacroDefs(md) {
  const lines = md.split("\n");
  const filtered = lines.filter((ln) => {
    const t = ln.trim();
    if (t.startsWith("\\newcommand")) return false;
    if (t.startsWith("\\def")) return false;
    return true;
  });
  return filtered.join("\n");
}

function normalizePandocMathFormatting(md) {
  let out = md.replace(/\$`([^`\n]+)`\$/g, (_m, inner) => `$${inner}$`);

  const lines = out.split("\n");
  const converted = [];
  let inFence = false;
  let fenceIndent = "";
  let fenceBody = [];

  for (const line of lines) {
    if (!inFence) {
      const start = line.match(/^(\s*)```+\s*math\s*$/);
      if (start) {
        inFence = true;
        fenceIndent = start[1] || "";
        fenceBody = [];
        continue;
      }
      converted.push(line);
      continue;
    }

    if (/^\s*```+\s*$/.test(line)) {
      converted.push("$$");
      for (const bodyLine of fenceBody) {
        if (bodyLine.startsWith(fenceIndent)) {
          converted.push(bodyLine.slice(fenceIndent.length));
        } else {
          converted.push(bodyLine);
        }
      }
      converted.push("$$");
      inFence = false;
      fenceIndent = "";
      fenceBody = [];
      continue;
    }

    fenceBody.push(line);
  }

  if (inFence) {
    converted.push(`${fenceIndent}\`\`\` math`);
    converted.push(...fenceBody);
  }

  return converted.join("\n");
}

function normalizeDisplayMathDelimiterIndent(md) {
  const lines = md.split("\n");
  const out = [];
  let inFence = false;

  for (const line of lines) {
    if (/^\s*```/.test(line)) {
      inFence = !inFence;
      out.push(line);
      continue;
    }

    if (!inFence && /^\s*\$\$\s*$/.test(line)) {
      out.push("$$");
      continue;
    }

    out.push(line);
  }

  return out.join("\n");
}

function normalizeInlineDisplayMath(md) {
  const lines = md.split("\n");
  const out = [];
  let inFence = false;

  for (const line of lines) {
    if (/^\s*```/.test(line)) {
      inFence = !inFence;
      out.push(line);
      continue;
    }

    if (inFence) {
      out.push(line);
      continue;
    }

    const m = line.match(/^(\s*.*?\S)?\s*\$\$([\s\S]+?)\$\$\s*(\S.*)?$/);
    if (!m) {
      out.push(line);
      continue;
    }

    const before = (m[1] || "").trimEnd();
    const inner = (m[2] || "").trim();
    const after = (m[3] || "").trim();

    if (before) out.push(before);
    out.push("$$");
    out.push(inner);
    out.push("$$");
    if (after) out.push(after);
  }

  return out.join("\n");
}

function stripPandocWrappers(md) {
  const lines = md.split("\n");
  const kept = [];
  for (const line of lines) {
    const t = line.trim();
    if (/^:::\s*(\{[^}]*\}|[A-Za-z0-9_.-]+)?\s*$/.test(t)) continue;
    if (t.startsWith("<div ") && t.endsWith(">")) continue;
    if (t === "</div>") continue;
    kept.push(line.replace(/^(#{1,6}\s+.*)\s+\{#[^}]+\}\s*$/, "$1"));
  }
  return kept.join("\n");
}

function dropLeadingTitleBlock(md) {
  const lines = md.split("\n");
  const scan = Math.min(lines.length, 90);
  let versionIdx = -1;
  for (let i = 0; i < scan; i += 1) {
    if (/^Version\s+v?\d/i.test(lines[i].trim())) {
      versionIdx = i;
      break;
    }
  }
  if (versionIdx === -1) return md;
  let cut = versionIdx + 1;
  while (cut < lines.length && lines[cut].trim() === "") cut += 1;
  return lines.slice(cut).join("\n").replace(/^\n+/, "");
}

function applyMacroExpansionInMath(md, macroMap) {
  if (!macroMap.size) return md;

  const entries = [...macroMap.entries()].sort((a, b) => b[0].length - a[0].length);
  const replaceMacros = (s) => {
    let r = s;
    for (let pass = 0; pass < 4; pass += 1) {
      let changed = false;
      for (const [k, v] of entries) {
        const re = new RegExp(`${escapeRegExp(k)}(?![A-Za-z])`, "g");
        const next = r.replace(re, v);
        if (next !== r) {
          changed = true;
          r = next;
        }
      }
      if (!changed) break;
    }
    return r;
  };

  let out = "";
  let i = 0;

  while (i < md.length) {
    if (md[i] === "$" && md[i + 1] === "$") {
      const start = i;
      i += 2;
      const end = md.indexOf("$$", i);
      if (end === -1) {
        out += md.slice(start);
        break;
      }
      const inner = md.slice(i, end);
      out += "$$" + replaceMacros(inner) + "$$";
      i = end + 2;
      continue;
    }

    if (md[i] === "$") {
      const start = i;
      i += 1;
      const end = md.indexOf("$", i);
      if (end === -1) {
        out += md.slice(start);
        break;
      }
      const inner = md.slice(i, end);
      out += "$" + replaceMacros(inner) + "$";
      i = end + 1;
      continue;
    }

    out += md[i];
    i += 1;
  }

  return out;
}

function dropDuplicateTitleHeading(md, title) {
  const lines = md.split("\n");
  const firstNonBlank = lines.findIndex((ln) => ln.trim().length > 0);
  if (firstNonBlank < 0) return md;
  const line = lines[firstNonBlank].trim();
  if (!line.startsWith("# ")) return md;
  const heading = line.replace(/^#\s+/, "").trim().toLowerCase();
  if (heading !== title.trim().toLowerCase()) return md;
  lines.splice(firstNonBlank, 1);
  while (firstNonBlank < lines.length && lines[firstNonBlank].trim() === "") {
    lines.splice(firstNonBlank, 1);
  }
  return lines.join("\n");
}

function extractCommandsInMath(md) {
  const cmds = new Set();
  const collectFrom = (s) => {
    for (const m of s.matchAll(/\\[A-Za-z]+/g)) cmds.add(m[0]);
  };

  for (const m of md.matchAll(/\$\$([\s\S]*?)\$\$/g)) collectFrom(m[1]);
  const inlineScan = md.replace(/\$\$[\s\S]*?\$\$/g, " ");
  for (const m of inlineScan.matchAll(/\$([^$\n]+?)\$/g)) collectFrom(m[1]);

  return cmds;
}

async function auditImageLinks(md, paperDir) {
  const missing = [];
  for (const m of md.matchAll(/!\[[^\]]*\]\(([^)]+)\)/g)) {
    const hrefRaw = m[1].trim();
    const href = hrefRaw.startsWith("<") && hrefRaw.endsWith(">") ? hrefRaw.slice(1, -1) : hrefRaw;
    const lower = href.toLowerCase();
    if (lower.startsWith("http://") || lower.startsWith("https://") || lower.startsWith("data:")) continue;
    if (href.startsWith("#")) continue;
    const abs = path.resolve(paperDir, decodeURIComponent(href));
    if (!(await exists(abs))) missing.push(href);
  }
  return [...new Set(missing)].sort();
}

function normalizeVersion(raw, fallback = "0.0.0") {
  const m = raw.match(/(\d+(?:\.\d+){0,2})/);
  return m ? m[1] : fallback;
}

function slugFromDirName(name) {
  const stripped = name.replace(/^\s*v\d+(?:\.\d+)*(?:\s*[-_:|]\s*|\s+)?/i, "").trim();
  const base = stripped || name;
  const slug = base.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
  return slug || "paper";
}

function encodeHref(relPath) {
  const normalized = relPath.replace(/\\/g, "/");
  return normalized
    .split("/")
    .map((seg, idx) => (idx === 0 && seg === "." ? seg : encodeURIComponent(seg)))
    .join("/");
}

function mdLink(label, relPath) {
  return `[${label}](${encodeHref(relPath)})`;
}

async function detectPaperDirs() {
  const nestedRoot = path.join(REPO_ROOT, "papers");
  if (await exists(nestedRoot)) {
    const entries = await fs.readdir(nestedRoot, { withFileTypes: true });
    const papers = [];
    for (const e of entries) {
      if (!e.isDirectory()) continue;
      const abs = path.join(nestedRoot, e.name);
      if (await exists(path.join(abs, "main.tex"))) papers.push(abs);
    }
    if (papers.length) return papers.sort();
  }

  const entries = await fs.readdir(REPO_ROOT, { withFileTypes: true });
  const top = [];
  for (const e of entries) {
    if (!e.isDirectory()) continue;
    const abs = path.join(REPO_ROOT, e.name);
    if (await exists(path.join(abs, "main.tex"))) top.push(abs);
  }
  return top.sort();
}

async function generateMirrorForPaper(paperDir) {
  const texPath = path.join(paperDir, "main.tex");
  const versionPath = path.join(paperDir, "VERSION");
  const changelogPath = path.join(paperDir, "CHANGELOG.md");

  const tex = await readText(texPath);
  const { preamble } = splitPreambleAndBody(tex);
  const macroMap = extractZeroArgMacros(preamble);

  const dirSlug = slugFromDirName(path.basename(paperDir));
  const extractedTitle = extractTitle(tex);
  const title = extractedTitle || slugToTitle(dirSlug);

  const versionRaw = (await exists(versionPath)) ? (await readText(versionPath)).trim() : path.basename(paperDir);
  const version = normalizeVersion(versionRaw);

  const tmpRaw = path.join("/tmp", `${dirSlug}.raw.md`);
  await run("pandoc", [
    texPath,
    "--from=latex",
    "--to=gfm+tex_math_dollars",
    "--wrap=none",
    "--standalone",
    "--output", tmpRaw,
  ]);

  let md = await readText(tmpRaw);
  md = stripPandocWrappers(md);
  md = normalizeMathDelimiters(md);
  md = normalizePandocMathFormatting(md);
  md = normalizeInlineDisplayMath(md);
  md = normalizeDisplayMathDelimiterIndent(md);
  md = stripLatexMacroDefs(md);
  md = applyMacroExpansionInMath(md, macroMap);
  md = dropLeadingTitleBlock(md);
  md = dropDuplicateTitleHeading(md, title);

  const changelogLine = (await exists(changelogPath))
    ? mdLink("CHANGELOG.md", "./CHANGELOG.md")
    : "(not found)";

  const header = [
    `# ${title}`,
    "",
    `**Version:** v${version}  `,
    `**Source:** ${mdLink("./", "./")}  `,
    `**Changelog:** ${changelogLine}`,
    "",
    "> Markdown mirror: best-effort GitHub rendering.",
    "",
  ].join("\n");

  const mirrorPath = path.join(paperDir, "mirror.md");
  await writeText(mirrorPath, `${header}${md.trim()}\n`);

  const mirrorText = await readText(mirrorPath);

  const leakedDefs = mirrorText
    .split("\n")
    .filter((ln) => {
      const t = ln.trim();
      return t.startsWith("\\newcommand") || t.startsWith("\\def");
    });

  const cmds = extractCommandsInMath(mirrorText);
  const unknown = [...cmds]
    .filter((c) => !SAFE_COMMANDS.has(c) && !macroMap.has(c))
    .sort();

  const missingImages = await auditImageLinks(mirrorText, paperDir);

  const auditLines = [];
  auditLines.push(`# Audit — ${title} (v${version})`);
  auditLines.push("");
  auditLines.push(`- Mirror: ./mirror.md`);
  auditLines.push("");
  auditLines.push("This audit lists items that may render differently on GitHub math rendering.");
  auditLines.push("");

  if (!leakedDefs.length && !unknown.length && !missingImages.length) {
    auditLines.push("✅ No obvious macro leaks, unknown commands, or missing images detected.");
  } else {
    if (leakedDefs.length) {
      auditLines.push("## Macro definitions leaked into mirror.md (should be zero)");
      auditLines.push("```");
      auditLines.push(...leakedDefs.slice(0, 200));
      auditLines.push("```");
      auditLines.push("");
    }
    if (unknown.length) {
      auditLines.push("## Commands still present in math (verify GitHub rendering)");
      auditLines.push("");
      auditLines.push(unknown.map((c) => `- ${c}`).join("\n"));
      auditLines.push("");
    }
    if (missingImages.length) {
      auditLines.push("## Missing image targets (from mirror.md links)");
      auditLines.push("");
      auditLines.push(missingImages.map((h) => `- ${h}`).join("\n"));
      auditLines.push("");
    }
  }

  const auditPath = path.join(paperDir, "mirror.audit.md");
  await writeText(auditPath, `${auditLines.join("\n")}\n`);

  return {
    slug: dirSlug,
    dir: path.relative(REPO_ROOT, paperDir),
    version,
    title,
  };
}

async function main() {
  await run("pandoc", ["--version"]);

  const paperDirs = await detectPaperDirs();
  if (!paperDirs.length) {
    console.log("No paper folders found with main.tex");
    return;
  }

  const results = [];
  for (const paperDir of paperDirs) {
    console.log(`Generating mirror for: ${path.relative(REPO_ROOT, paperDir)}`);
    results.push(await generateMirrorForPaper(paperDir));
  }

  console.log("\nSummary:");
  for (const r of results) {
    console.log(`- ${r.dir} | v${r.version}`);
  }

  console.log("\nReview each <paper>/mirror.audit.md for rendering risks.");
  console.log("This script only updates markdown mirrors and audits.");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
