# 视频封面：Normal Image（480×360）

把封面与 `final-article.md` 放在同一个视频输出文件夹，命名为 `thumbnail-480x360.jpg`。不默认把它插进文章正文；它是单独交付的封面资产。

优先使用 https://youtube-thumbnail-grabber.com/：输入当前视频 URL，获取图片，选择 Normal Thumbnail Image (480x360) 并下载。页面可能同时提供 320×180 和 120×90，不能混淆。遵循浏览器工具的上传、下载及保存接口文档，不猜测页面控件。下载后解码图片，确认它是 480×360；不能只相信按钮标签或文件名。遇到登录、验证码或安全提示，按当前工具权限处理，不能自行绕过。

浏览器无法操作时，可用同目录的 Python 环境执行：

```sh
python /path/to/youtube-to-wechat/scripts/fetch_thumbnail.py 'https://www.youtube.com/watch?v=VIDEO_ID' --out /path/to/article-folder
```

脚本读取指定网站的 HTML 与 `ytg.js`，确认其 Normal/HQ 下载规则，再下载该规则对应的原始 JPEG，并校验真实尺寸。保存 `thumbnail-source.json` 说明来源和方法。它不模拟点击，也不声称浏览器下载成功。页面规则改变时会停止，需重新查看当前网站后再适配。

若图片缺失、响应是占位小图、尺寸不符或下载受限，如实报告；不把其他尺寸拉伸为 480×360，不用 AI 生成替代原视频封面。保留文章成果，提供具体手动下载步骤。没有针对性修复，不重复重试。
