#!/usr/bin/env python3
"""
Claude Universal Config - Generator

Usage:
    python generate.py <config_file> [output_dir]

Example:
    python generate.py claude-config.yaml .
"""

import sys
import shutil
import json
from pathlib import Path
try:
    import yaml
    from jinja2 import Template
except ImportError:
    print("Error: Missing dependencies. Install with:")
    print("  pip install pyyaml jinja2")
    sys.exit(1)


class ClaudeConfigGenerator:
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.core_path = repo_path / "core"
        self.languages_path = repo_path / "languages"
        self.frameworks_path = repo_path / "frameworks"
        self.infrastructure_path = repo_path / "infrastructure"
        self.domains_path = repo_path / "domains"

    def generate(self, config_file: Path, output_dir: Path):
        """設定ファイルからClaude Code設定を生成"""
        print(f"📖 Loading config: {config_file}")

        with open(config_file, encoding='utf-8') as f:
            config = yaml.safe_load(f)

        output_claude = output_dir / ".claude"
        output_claude.mkdir(exist_ok=True)

        print(f"📁 Output directory: {output_claude}\n")

        # 1. コアルールをコピー（必須）
        self._copy_core(output_claude)

        # 2. 言語別ルールをコピー
        for lang in config.get("languages", []):
            self._copy_language(lang, output_claude)

        # 3. バックエンドフレームワーク
        for fw in config.get("backend", []):
            self._copy_framework("backend", fw, output_claude)

        # 4. フロントエンドフレームワーク
        for fw in config.get("frontend", []):
            self._copy_framework("frontend", fw, output_claude)

        # 5. インフラ
        for infra in config.get("infrastructure", []):
            self._copy_infrastructure(infra, output_claude)

        # 6. ドメイン固有スキル
        for domain in config.get("domains", []):
            self._copy_domain(domain, output_claude)

        # 7. エージェントを生成（テンプレート置換）
        self._generate_agents(config, output_claude)

        # 8. コマンドをコピー
        self._copy_commands(config, output_claude)

        # 9. settings.local.json を生成
        self._generate_settings(config, output_claude)

        # 10. カスタムルール（オプション）
        self._copy_custom_rules(config, output_dir, output_claude)

        print(f"\n✅ Claude Code設定を生成しました: {output_claude}")
        print(f"\n次のステップ:")
        print(f"  1. CLAUDE.md を作成してプロジェクト固有の指示を記載")
        print(f"  2. claude-config.yaml をgitにコミット")
        print(f"  3. .claude/ ディレクトリもコミット")

    def _copy_core(self, output: Path):
        """コアルールをコピー"""
        src = self.core_path / "rules"
        dst = output / "rules"
        dst.mkdir(exist_ok=True)

        for rule in src.glob("*.md"):
            shutil.copy(rule, dst / rule.name)

        print(f"  ✓ コアルール: {len(list(src.glob('*.md')))} files")

    def _copy_language(self, lang: str, output: Path):
        """言語別ルールをコピー"""
        lang_path = self.languages_path / lang / "rules"
        if not lang_path.exists():
            print(f"  ⚠️  {lang}: rules not found (skipping)")
            return

        dst = output / "rules"
        count = 0
        for rule in lang_path.glob("*.md"):
            shutil.copy(rule, dst / rule.name)
            count += 1

        if count > 0:
            print(f"  ✓ {lang}: {count} rules")

    def _copy_framework(self, tier: str, framework: str, output: Path):
        """フレームワーク別ルールをコピー"""
        fw_path = self.frameworks_path / tier / framework / "rules"
        if not fw_path.exists():
            print(f"  ⚠️  {framework}: rules not found (skipping)")
            return

        dst = output / "rules"
        count = 0
        for rule in fw_path.glob("*.md"):
            shutil.copy(rule, dst / rule.name)
            count += 1

        if count > 0:
            print(f"  ✓ {framework}: {count} rules")

    def _copy_infrastructure(self, infra: str, output: Path):
        """インフラ別ルールをコピー"""
        infra_path = self.infrastructure_path / infra / "rules"
        if not infra_path.exists():
            print(f"  ⚠️  {infra}: rules not found (skipping)")
            return

        dst = output / "rules"
        count = 0
        for rule in infra_path.glob("*.md"):
            shutil.copy(rule, dst / rule.name)
            count += 1

        if count > 0:
            print(f"  ✓ {infra}: {count} rules")

    def _copy_domain(self, domain: str, output: Path):
        """ドメイン固有スキルをコピー"""
        domain_path = self.domains_path / domain / "skills"
        if not domain_path.exists():
            print(f"  ⚠️  {domain}: skills not found (skipping)")
            return

        dst = output / "skills"
        dst.mkdir(exist_ok=True)
        count = 0
        for skill in domain_path.glob("*.md"):
            shutil.copy(skill, dst / skill.name)
            count += 1

        if count > 0:
            print(f"  ✓ {domain}: {count} skills")

    def _generate_agents(self, config: dict, output: Path):
        """エージェントをテンプレートから生成"""
        (output / "agents").mkdir(exist_ok=True)

        agents = config.get("agents", {})
        if not agents:
            print(f"  ℹ️  No agents configured")
            return

        project_type = self._get_project_type(config)

        for agent_name, agent_config in agents.items():
            if not agent_config.get("enabled", False):
                continue

            template_path = self.core_path / "agents" / f"{agent_name}.template.md"
            if not template_path.exists():
                print(f"  ⚠️  {agent_name}: template not found (skipping)")
                continue

            with open(template_path, encoding='utf-8') as f:
                template = Template(f.read())

            # テンプレート変数
            contexts = agent_config.get("contexts", [])
            custom_checks = agent_config.get("custom_checks", [])

            rendered = template.render(
                project_type=project_type,
                languages=config.get("languages", []),
                backend=config.get("backend", []),
                frontend=config.get("frontend", []),
                infrastructure=config.get("infrastructure", []),
                contexts=contexts,
                custom_checks=custom_checks,
            )

            output_path = output / "agents" / f"{agent_name}.md"
            with open(output_path, "w", encoding='utf-8') as f:
                f.write(rendered)

            print(f"  ✓ Agent: {agent_name}")

    def _copy_commands(self, config: dict, output: Path):
        """コマンドをコピー"""
        (output / "commands").mkdir(exist_ok=True)

        commands = config.get("commands", [])
        if not commands:
            print(f"  ℹ️  No commands configured")
            return

        count = 0
        for cmd in commands:
            # コアコマンド
            cmd_path = self.core_path / "commands" / f"{cmd}.md"
            if cmd_path.exists():
                shutil.copy(cmd_path, output / "commands" / f"{cmd}.md")
                count += 1
                continue

            # フレームワーク固有コマンド
            found = False
            for tier in ["backend", "frontend"]:
                for fw in config.get(tier, []):
                    fw_cmd_path = self.frameworks_path / tier / fw / "commands" / f"{cmd}.md"
                    if fw_cmd_path.exists():
                        shutil.copy(fw_cmd_path, output / "commands" / f"{cmd}.md")
                        count += 1
                        found = True
                        break
                if found:
                    break

            if not found:
                print(f"  ⚠️  Command '{cmd}' not found")

        if count > 0:
            print(f"  ✓ Commands: {count} files")

    def _generate_settings(self, config: dict, output: Path):
        """settings.local.json を生成"""
        settings = {
            "autoApprove": ["read", "glob", "grep"],
            "alwaysAllow": [
                {"tool": "bash", "pattern": "^(ls|pwd|cat|git status|git diff|git log) "}
            ]
        }

        with open(output / "settings.local.json", "w", encoding='utf-8') as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)

        print(f"  ✓ settings.local.json")

    def _copy_custom_rules(self, config: dict, project_root: Path, output: Path):
        """カスタムルールをコピー"""
        custom_rules = config.get("custom_rules", [])
        if not custom_rules:
            return

        dst = output / "custom"
        dst.mkdir(exist_ok=True)

        for rule in custom_rules:
            rule_path = project_root / rule.get("path", "")
            if rule_path.exists():
                shutil.copy(rule_path, dst / rule_path.name)
                print(f"  ✓ Custom: {rule_path.name}")

    def _get_project_type(self, config: dict) -> str:
        """プロジェクトタイプを推定"""
        backend = config.get("backend", [])
        frontend = config.get("frontend", [])

        parts = []
        if backend:
            parts.append(" + ".join(backend))
        if frontend:
            parts.append(" + ".join(frontend))

        return " + ".join(parts) or "multi-language"


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate.py <config_file> [output_dir]")
        print("Example: python generate.py claude-config.yaml .")
        sys.exit(1)

    config_file = Path(sys.argv[1])
    if not config_file.exists():
        print(f"Error: Config file not found: {config_file}")
        sys.exit(1)

    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.cwd()
    repo_path = Path(__file__).parent.parent

    generator = ClaudeConfigGenerator(repo_path)
    generator.generate(config_file, output_dir)


if __name__ == "__main__":
    main()
