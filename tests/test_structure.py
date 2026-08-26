"""Structure tests for the engagement-kit plugin. Run: python3 -m unittest discover tests"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def frontmatter(path: Path) -> str:
    text = path.read_text()
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    return m.group(1) if m else ""


class TestManifests(unittest.TestCase):
    def test_plugin_json(self):
        data = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        for field in ("name", "version", "description"):
            self.assertIn(field, data)
        self.assertEqual(data["name"], "engagement-kit")
        self.assertRegex(data["version"], r"^\d+\.\d+\.\d+$")

    def test_marketplace_json(self):
        data = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
        self.assertEqual(data["name"], "engagement-kit")
        self.assertEqual(len(data["plugins"]), 1)
        entry = data["plugins"][0]
        self.assertEqual(entry["name"], "engagement-kit")
        self.assertEqual(entry["source"], "./")


class TestHook(unittest.TestCase):
    def test_manifest_wires_existing_script(self):
        data = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        entries = data["hooks"]["UserPromptSubmit"][0]["hooks"]
        self.assertEqual(len(entries), 1)
        cmd = entries[0]["command"]
        self.assertIn("${CLAUDE_PLUGIN_ROOT}", cmd)
        m = re.search(r"hooks/([\w-]+\.sh)", cmd)
        self.assertTrue(m, f"no script path in command: {cmd}")
        self.assertTrue((ROOT / "hooks" / m.group(1)).exists())

    def test_script_syntax(self):
        import subprocess
        for script in ROOT.glob("hooks/*.sh"):
            r = subprocess.run(["bash", "-n", str(script)], capture_output=True)
            self.assertEqual(r.returncode, 0, r.stderr.decode())

    def test_script_portability(self):
        # Portability bugs hit 5/5 mined sessions: no node/jq/python deps,
        # no GNU-only flags; the hook must run on stock macOS bash 3.2.
        for script in ROOT.glob("hooks/*.sh"):
            body = script.read_text()
            for banned in ("jq ", "node ", "python", "sed -i", "head -n -", "readarray", "mapfile"):
                self.assertNotIn(banned, body, f"{script}: uses non-portable '{banned}'")

    def test_script_never_blocks(self):
        # A nudge hook must not be able to fail the prompt: every exit is 0.
        for script in ROOT.glob("hooks/*.sh"):
            body = script.read_text()
            self.assertNotRegex(body, r"exit [1-9]", str(script))


class TestSkills(unittest.TestCase):
    def skill_files(self):
        files = sorted(ROOT.glob("skills/*/SKILL.md"))
        self.assertTrue(files, "no skills found")
        return files

    def test_frontmatter_fields(self):
        for skill in self.skill_files():
            fm = frontmatter(skill)
            self.assertRegex(fm, r"(?m)^name: \S", msg=str(skill))
            self.assertRegex(fm, r"(?m)^description: \S", msg=str(skill))

    def test_referenced_templates_exist(self):
        for skill in self.skill_files():
            body = skill.read_text()
            for ref in re.findall(r"`([\w-]+\.md)`", body):
                if ref in ("SKILL.md", "MEMORY.md"):
                    continue
                # References to files the skill ships must resolve in its folder;
                # engagement outputs (docs/specs, decision-spine) live in target repos.
                if ref.endswith("-template.md"):
                    self.assertTrue(
                        (skill.parent / ref).exists(),
                        f"{skill} references missing template {ref}",
                    )

    def test_all_templates_are_referenced(self):
        for skill_dir in {f.parent for f in self.skill_files()}:
            body = (skill_dir / "SKILL.md").read_text()
            for template in skill_dir.glob("*-template.md"):
                self.assertIn(
                    f"`{template.name}`", body,
                    f"{template} ships with the skill but SKILL.md never mentions it",
                )


class TestAgents(unittest.TestCase):
    def test_frontmatter_fields(self):
        agents = sorted(ROOT.glob("agents/*.md"))
        self.assertTrue(agents, "no agents found")
        for agent in agents:
            fm = frontmatter(agent)
            self.assertRegex(fm, r"(?m)^name: \S", msg=str(agent))
            self.assertRegex(fm, r"(?m)^description: \S", msg=str(agent))
            self.assertRegex(fm, r"(?m)^tools: \S", msg=str(agent))

    def test_tech_lead_is_read_only(self):
        fm = frontmatter(ROOT / "agents/tech-lead.md")
        tools = re.search(r"^tools: (.+)$", fm, re.MULTILINE).group(1)
        for write_tool in ("Edit", "Write", "NotebookEdit"):
            self.assertNotIn(write_tool, tools.split(", "))


class TestNoStaleContent(unittest.TestCase):
    def content_files(self):
        return list(ROOT.glob("skills/**/*.md")) + list(ROOT.glob("agents/*.md"))

    def test_no_pre_plugin_paths(self):
        # The kit used to install by copying a .claude/ dir; no content should
        # still point there.
        for path in self.content_files():
            self.assertNotIn(".claude/", path.read_text(), msg=str(path))

    def test_no_persona_leftovers(self):
        # Dev/QA personas were deliberately cut (see README); their return in
        # content would be a regression against that decision.
        for path in self.content_files():
            self.assertNotRegex(
                path.read_text(), r"QA (agent|persona|writes)", msg=str(path)
            )


if __name__ == "__main__":
    unittest.main()
