# GitHub publication | GitHub 发布指引

> Recommended initial visibility: **private**. Do not publish real work materials without explicit permission.
> 推荐先建 **Private** 仓库。任何真实团队材料、会议截图或私有模型资料须获得授权后才能公开。

## 1. Create an empty repository / 创建空仓库

Open https://github.com/new and use:

- Owner: your GitHub account
- Repository name: `technical-talk-workflow`
- Description: `Narrative-first technical talks with aligned projection and speaker notes`
- Visibility: **Private** initially
- Do **not** initialize with a README, `.gitignore` or LICENSE (they are already in this project)

## 2. Publish with Git / 推送源码

From the folder containing `SKILL.md` and `README.md`:

```bash
git init
git add .
git commit -m "feat: technical-talk-workflow v0.2.0"
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/technical-talk-workflow.git
git push -u origin main
```

Replace `<YOUR_USERNAME>` with your actual GitHub owner. GitHub may require you to authenticate via the browser, SSH, or a credential manager. Do not paste private tokens into chat.

If you have GitHub CLI installed and authenticated, you can instead run:

```bash
gh repo create technical-talk-workflow --private --source=. --remote=origin --push
```

## 3. Verify before making public / 对外公开前验证

```bash
python -m unittest discover -s scripts -p 'test_*.py' -v
python scripts/check_alignment.py --outline examples/sample-talk/outline.json --projection examples/sample-talk/projection.md --notes examples/sample-talk/speaker_notes.md
python scripts/audit_talk.py --outline examples/sample-talk/outline.json --projection examples/sample-talk/projection.md --notes examples/sample-talk/speaker_notes.md --visuals examples/sample-talk/visuals.json --strict-warnings
python scripts/privacy_scan.py .
```

A clean automatic scan is not sufficient: visually inspect the full diff, image assets, links, employer materials, and license provenance. Then change visibility in repository Settings only when approved.

## 4. Post-upload checks / 上传后的检查

- Verify the repository page and `SKILL.md` open correctly.
- Check GitHub Actions on the default branch.
- Clone a fresh copy and rerun tests.
- Confirm bilingual README renders and local paths work.
