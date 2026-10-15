# YouTube → 微信公众号文章技能

最新版 Codex 技能：直接使用字幕的叙述视角，在开头导语介绍主讲人。

- [下载技能 ZIP](dist/youtube-to-wechat.zip)（打开后点击 Download raw file）
- [完整安装与使用说明](youtube-to-wechat/README.md)
- [技能指令](youtube-to-wechat/SKILL.md)
- [SHA-256 校验值](dist/SHA256SUMS.txt)

## 快速开始

解压 ZIP，将 `youtube-to-wechat` 文件夹放入 `~/.codex/skills/`（设置了 CODEX_HOME 时使用其 skills 子目录）。在 Codex 中输入：

```text
$youtube-to-wechat https://www.youtube.com/watch?v=zKi1KYhi0xg
```

先完成完整译稿，再选择标题与导语，例如“标题 1，导语 3”，随后生成四节文章、封面，并尝试导入 WeMD。不会自动发布公众号文章。

Python 依赖安装、浏览器回退、输出文件和故障处理见上方完整说明。
