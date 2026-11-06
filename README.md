# Niche Documentary Animation

A Codex skill for original animated documentaries across niches, with a company-history profile inspired by the subject matter of Built On You. Research, ideas, complete scripts, and Word documents work independently of video production.

The included Remotion/SVG studio is adapted from [kelano86/what-if-animation](https://github.com/kelano86/what-if-animation). It preserves the drawing rig, reusable sets, timing engine, storyboard tooling, and sound/mastering helpers, while replacing the short speculative formula with documentary research and writing.

## Install in Codex

Ask Codex to install the skill from this repository using its skill installer, or copy the repository into `~/.codex/skills/niche-documentary-animation`. The skill becomes available on the next turn.

Example prompts:

- `Use $niche-documentary-animation to research 10 company-history video ideas and write full scripts in Word. Do not generate audio or video.`
- `Use $niche-documentary-animation to adapt the documentary workflow for infrastructure history.`
- `Use $niche-documentary-animation to storyboard this approved script using original SVG illustrations.`

For later media production, copy `studio/` to a separate project and run `npm ci`. Node 18+, Python 3.9+ with NumPy/Pillow, ffmpeg/ffprobe, and an authorized ElevenLabs key are needed for the corresponding production stages. No API key or media call is required to write scripts. See [SKILL.md](SKILL.md) for the complete workflow.

The adaptation's offline validators and timing/chunking checks are included. Narration generation and full video rendering require separate runtime verification when a video is requested. This repository contains no generated full documentary videos and has no affiliation with the reference channel.

## License

MIT. The upstream license and copyright notice are retained in `LICENSE`. See `NOTICE.md` for the exact upstream revision and adaptation notes.
