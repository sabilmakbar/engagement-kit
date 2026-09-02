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

    def agent_tools(self, name):
        fm = frontmatter(ROOT / f"agents/{name}.md")
        return re.search(r"^tools: (.+)$", fm, re.MULTILINE).group(1).split(", ")

    def test_eng_contract(self):
        # eng may not spawn subagents (its whole input is one story file) and
        # its body must forbid running commits itself.
        self.assertNotIn("Agent", self.agent_tools("eng"))
        body = " ".join((ROOT / "agents/eng.md").read_text().lower().split())
        self.assertIn("never run `git commit`", body)
        # v0.3.1 field fixes stay in: write-through progress + fail-fast net calls
        self.assertIn("write-through", body)
        self.assertIn("explicit short timeout", body)

    def test_tech_lead_two_passes(self):
        body = " ".join((ROOT / "agents/tech-lead.md").read_text().lower().split())
        self.assertIn("spec review", body)
        self.assertIn("close review", body)
        # The close review must stay blinded: rationales yes, transcripts never.
        self.assertIn("never an executor's or verifier's transcript", body)

    def test_qa_contract(self):
        # qa edits section 6 only: no Write (new files) and no subagents.
        tools = self.agent_tools("qa")
        self.assertNotIn("Write", tools)
        self.assertNotIn("Agent", tools)


class TestChecksCanFail(unittest.TestCase):
    """A check that cannot fail is not a check — pinned in three places."""

    def text(self, rel):
        return " ".join((ROOT / rel).read_text().lower().split())

    def test_refactor_gate_is_executed_not_asserted(self):
        lens = self.text("agents/tech-lead.md")
        self.assertIn("do not read it, run it", lens)
        self.assertIn("forced-opposite", lens)
        # The spec must carry a runnable mapping, not a prose claim.
        self.assertIn("forced-opposite check", self.text("skills/pm/spec-template.md"))

    def test_qa_rejects_self_fabricated_evidence(self):
        qa = self.text("agents/qa.md")
        self.assertIn("self-fabricated fixtures prove consistency, not correctness", qa)
        self.assertIn("the code's author did not construct", qa)

    def test_review_loop_bounded_by_class(self):
        skill = self.text("skills/pm/SKILL.md")
        self.assertIn("no `intent_gap` and no `bad_ground`", skill)
        self.assertIn("hard ceiling: 3 rounds", skill)

    def test_scaling_never_touches_the_gates(self):
        # Small engagements write fewer artifacts; the gates are not negotiable.
        skill = self.text("skills/pm/SKILL.md")
        self.assertIn("scale the artifacts to the engagement, never the gates", skill)
        self.assertIn("what never scales down", skill)

    def test_evidence_survives_the_call_path(self):
        # Absence-of-failure evidence dies to any handler between call and assert:
        # qa must walk the path, pm must author positive ACs, tech-lead must flag
        # work that widens a handler around raise-pinned behavior.
        self.assertIn(
            "positive assertions beat absence-of-failure", self.text("agents/qa.md")
        )
        self.assertIn("evidence coupling", self.text("agents/tech-lead.md"))
        self.assertIn("never as absence-of-failure", self.text("skills/pm/SKILL.md"))

    def test_execution_rule_is_not_refactor_only(self):
        # "run it, don't reason about it" binds both passes, not just the
        # refactor lens where it was first written.
        lead = self.text("agents/tech-lead.md")
        self.assertIn("run it, don't reason about it", lead)
        self.assertIn("this binds both passes", lead)

    def test_agents_state_precedence_over_injected_instructions(self):
        # INTERNALS O5: another plugin's SubagentStart hook injects into these
        # agents and cannot be blocked. Precedence must be stated, not inferred.
        for name in ("eng", "qa", "tech-lead"):
            self.assertIn(
                "never change your input contract",
                self.text(f"agents/{name}.md"),
                msg=name,
            )

    def test_grounding_is_delegate_if_permitted(self):
        # A no-subagents session must still ground, never interview cold.
        skill = self.text("skills/pm/SKILL.md")
        self.assertIn("available and permitted", skill)
        self.assertIn("otherwise ground directly", skill)


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
