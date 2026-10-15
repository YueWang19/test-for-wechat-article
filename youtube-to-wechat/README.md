# YouTube → 微信公众号文章

一个可复用的 Codex skill：输入英文 YouTube 视频链接，获取字幕、生成自然中文译稿和编辑选项，待你选定标题与导语后，输出四节正文，下载 480×360 原视频封面，并尝试导入 WeMD 排版。

**不会自动发布。** 缺失字幕不会被编造；浏览器无法操作时会交付本地文件和手动导入说明。

## 安装

需要 Codex、可访问 YouTube 的网络，以及 Python 3.11 或更新版本。浏览器自动化为可选能力；没有浏览器工具仍可生成 Markdown 和下载封面。扩展回退需要 Chrome 已安装 vCaptions – Video Caption List；不自动安装扩展，没有相关工具时请手动复制/导出。

把本文件所在的整个 `youtube-to-wechat` 文件夹复制到 Codex 的全局 skills 目录：

- 默认目录：`~/.codex/skills/youtube-to-wechat/`
- 如果设置了 `CODEX_HOME`：`$CODEX_HOME/skills/youtube-to-wechat/`

安装完成后，目录中应直接包含 `SKILL.md`，不要多套一层同名文件夹。已有同名技能时先备份并合并更新。

在 macOS / Linux 上，可在解压包的上级目录运行：

```sh
skill_root="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$skill_root"
# 目标目录不存在时复制；已有版本请先备份。
test ! -e "$skill_root/youtube-to-wechat" && cp -R youtube-to-wechat "$skill_root/"
```

安装脚本依赖（macOS / Linux 示例）：

```sh
skill_dir="${CODEX_HOME:-$HOME/.codex}/skills/youtube-to-wechat"
python3 -m venv "$skill_dir/.venv"
"$skill_dir/.venv/bin/python" -m pip install -r "$skill_dir/scripts/requirements.txt"
```

Windows 用户同样把文件夹放入用户目录下 `.codex/skills`，创建虚拟环境后使用 `.venv\Scripts\python.exe` 安装依赖。脚本本身可跨平台运行。

如果当前聊天没有发现新技能，重新打开 Codex 或新建聊天后再试。技能不依赖创建者的电脑路径、API 密钥或账号。

## 使用

在任意 Codex 项目或聊天中输入：

```text
$youtube-to-wechat https://www.youtube.com/watch?v=zKi1KYhi0xg
```

也可以指定输出位置和读者：

```text
使用 $youtube-to-wechat 处理这个英文视频：https://www.youtube.com/watch?v=VIDEO_ID
读者是对科技感兴趣的普通读者。输出到当前项目 outputs/video-article/。
封面使用 Normal Image（480×360），文章与图片保存在同一文件夹。
```

技能会依次：

1. 获取视频标题、频道、时长及可用字幕；优先人工英文字幕，再尝试原始自动英文字幕。常规获取失败时，使用 Chrome 已安装的 vCaptions 扩展复制或导出原始英文字幕，验证内容后继续。
2. 保存时间戳转录和完整中文译稿，整理事实、逻辑与术语，说明重要不确定之处。
3. 提供五个不同角度的中文标题和三个约 60–120 汉字的导语；每个导语简要介绍视频主讲人的姓名、身份与已核实的相关背景。
4. **暂停等待你选择。** 回复如“标题 1，导语 3”，也可以要求修改选项。
5. 用所选标题和导语生成恰好四节正文，保留原视频出处。
6. 从 [YouTube Thumbnail Grabber](https://youtube-thumbnail-grabber.com/) 获取 Normal Image（480×360），校验实际尺寸，与 Markdown 放在一起。
7. 有浏览器工具时连接或打开 [WeMD](https://edit.wemd.app/)，在新文章中导入并检查主题、正文和保存状态；不可操作时提供手动步骤。

全文沿用字幕本身的叙述视角，使用自然的“我／我们／你”，避免“视频称”“视频用这个比喻开场”等外层转述，也不虚构主讲人的个人经历。主讲人简介放在开头导语，不在正文为每位被引用者添加履历。简介优先依据官方资料并提供来源；除这类明确标注的编辑补充外，不自行增加原视频没有的论断和例子。旧视频中的计划保留当时语境。配置的公众号参考文章可访问时仅用于研究编辑节奏，不照抄；无法访问时会如实说明。

## 输出文件

每个视频使用独立输出文件夹，保留已存在的成果。

| 文件 | 用途 |
| --- | --- |
| `transcript.txt` | 带时间戳的英文转录 |
| `translated.md` | 完整中文译稿 |
| `title-options.md` | 五个标题及三个导语 |
| `final-article.md` | 选择后生成的四节正文成稿 |
| `thumbnail-480x360.jpg` | 原视频 480×360 封面 |
| `captions-vcaptions-raw.txt`、`transcript-source.json` | 扩展回退时的原始复制文本和来源记录 |
| `metadata.json`、`captions.json3` | 视频元数据、字幕来源及原始字幕 |
| `thumbnail-source.json` | 脚本下载封面时的来源与方法记录 |
| `editorial-notes.md` | 重要纠错、缺口或历史语境说明（需要时） |
| 预览截图、手动导入说明 | 视浏览器和执行结果保存 |

选定标题与导语之前不生成 `final-article.md`。字幕或封面确实不可用时，相应成果不会被伪造。

## 手动使用脚本

这些脚本负责取材、下载和结构检查，**翻译及编辑由 Codex 完成**，不是独立的一键文章生成程序。

在已安装的环境中运行：

```sh
skill_dir="${CODEX_HOME:-$HOME/.codex}/skills/youtube-to-wechat"
video_url='https://www.youtube.com/watch?v=zKi1KYhi0xg'
article_dir='./outputs/handwriting-article'

# 输出目录必须为空或尚未创建。
"$skill_dir/.venv/bin/python" "$skill_dir/scripts/fetch_video.py" "$video_url" --out "$article_dir"

# 封面输出目录必须存在；已有同名封面不会被覆盖。
"$skill_dir/.venv/bin/python" "$skill_dir/scripts/fetch_thumbnail.py" "$video_url" --out "$article_dir"

# Codex 完成选项确认和成稿后检查结构。
"$skill_dir/.venv/bin/python" "$skill_dir/scripts/check_article.py" "$article_dir/final-article.md" --source "$video_url"
```

## WeMD 手动排版

打开 WeMD，新建文章，导入 `final-article.md`，或全选 Markdown 编辑区的占位文字后粘贴完整文件内容。选择简洁主题，检查标题、导语、四个小节及出处。封面作为独立图片保存，不默认插入正文。

需要转入公众号草稿时，使用“复制到公众号”，粘贴到公众号编辑器，再检查手机预览。标题可能需要单独填写。发布仍需你的明确批准。

## 常见情况

- **字幕获取失败**：先尝试 Chrome 的 vCaptions 扩展，选择英文和全文字幕模式，再复制或导出；扩展也失败时提供手动取得的字幕文件。不要复制 Chat/Refine 的摘要代替字幕，不用视频简介冒充转录。没有时间戳时不会编造。
- **证书错误**：修复 Python 的可信 CA 或使用系统可信证书包；不要关闭证书验证。
- **YouTube 提示缺少 JavaScript 运行时**：按 yt-dlp 的官方提示配置支持的运行时。部分视频仍可直接获取字幕，是否成功以实际结果为准。
- **WeMD 超时**：可先自行打开页面再让 Codex 连接；仍失败则使用手动导入。不会声称未验证的操作已完成。
- **封面下载失败**：用网站的 480×360 选项手动下载。备用脚本会先读取网站当前下载规则；规则变化或尺寸错误时停止，不拉伸其他尺寸替代。

## 本版验证范围

本版使用 `Handwriting Literally Rewires Your Brain`（`zKi1KYhi0xg`）完成复测：复用此前通过 yt-dlp 获取的原始英文自动字幕，重新翻译、确认标题与导语、生成四节文章，并实际导入 WeMD、检查预览和自动保存。导语包含主讲人介绍，正文采用直接叙述，未加入被引用人物的履历。

480×360 封面复用此前通过网站规则核验、下载并解码确认的原始图片。字幕抓取、浏览器与扩展的可用性依赖本地环境和网站状态；这不保证所有视频均可访问。

## 分享包内容

仓库与 ZIP 仅包含技能指令、辅助脚本、引用指南、界面元数据和本使用说明。不包含个人账号、凭据、浏览器数据、虚拟环境或视频字幕及文章等运行产物。
