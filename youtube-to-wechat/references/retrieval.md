# Caption retrieval

Install yt-dlp in a dedicated virtual environment if absent (`python3 -m venv .venv`, then `.venv/bin/python -m pip install yt-dlp`), respecting environment permissions. Prefer Python 3.11 or later. The dependency is also declared in `scripts/requirements.txt`. If Python reports a CA certificate error, use the environment's trusted system CA bundle or repair its certifi installation; do not disable certificate verification. Run the helper with that environment's Python. It downloads no video/audio and does not use account cookies.

The helper selects `en`, then regional English tracks, from human subtitles before automatic captions. Automatically translated tracks (`tlang` URLs) are excluded. JSON3 is required to retain timing and distinguish rolling captions. If an English track cannot be downloaded, report the failure rather than silently treating it as absent. Retry only after a concrete fix, up to two times; do not loop against authentication/rate limits. Cookies or account access require user authorization.

Review the saved inventory, selected track type, first/last timestamps and duration. Timing alone does not prove completeness: inspect the transcript and accessible audio where necessary. Preserve intentional repetitions; the helper only removes adjacent rolling-caption overlap within overlapping timestamps. Its output is a source artifact, not the polished translation.

For user-provided captions, retain the original file, source URL, language, known provenance and any gaps. Do not label an uploaded or unknown transcript as human-written unless verified.

## Chrome extension fallback

If yt-dlp cannot obtain usable English captions, follow [vcaptions.md](vcaptions.md) to copy/export from the already-installed Chrome vCaptions extension. Preserve retrieval-error.txt and any metadata, save the extension raw text separately, and record its actual provenance. Only ask for a user-supplied transcript after this available fallback fails. When testing the extension on a video where yt-dlp already works, label it a separate fallback-path exercise, not a naturally triggered failure.
