# WeMD handoff

If the user already has a WeMD tab open, connect to that tab rather than opening a duplicate. Otherwise use available browser automation and its documented API to open https://edit.wemd.app/. Inspect current controls; avoid hard-coded selectors or assumptions about the editor implementation. Import/upload `final-article.md` if supported, otherwise paste its complete UTF-8 content into the Markdown source editor. Replacing existing editor content requires preserving that content or using a fresh document.

Create a fresh article to preserve existing documents. When pasting into a new editor, replace its placeholder content rather than appending; verify there is only one title and no leftover “新文章” heading.

Choose a restrained WeChat theme with readable spacing and typography. Verify title, selected introduction, all four sections, paragraph breaks, emphasis, and source attribution in the preview. Check the editor save indicator and retain a preview screenshot when supported. Distinguish preview verification from saved-state verification. If a call times out after a mutation, inspect the existing tab before retrying; avoid duplicate articles. After one targeted recovery attempt fails, provide the local Markdown and manual instructions rather than looping. Report access/login/import problems accurately. Do not click publication or account submission controls.

Manual fallback instructions to deliver:
1. Open https://edit.wemd.app/.
2. Use its Markdown import/open control if available, or open `final-article.md` as UTF-8 text and paste it into the Markdown editor.
3. Choose a theme and inspect the preview, especially four section headings and source footer.
4. Use WeMD's copy-formatted-content control, then paste into a WeChat Official Account draft and check the draft preview. The article title may need to be entered separately.
5. Review before publishing; publication requires your explicit approval.
