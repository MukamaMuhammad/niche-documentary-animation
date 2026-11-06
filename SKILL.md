---
name: niche-documentary-animation
description: Research and write original animated documentaries for a chosen YouTube niche, especially company and brand histories, then optionally storyboard and animate them with the bundled Remotion and SVG studio. Use for niche adaptation, documentary ideas, complete narration scripts, business-history animation, or production with this studio. Support research-only and script-only requests without generating audio or video.
---

# Niche documentary animation

Turn a subject into an original, sourced animated documentary. The default niche is **company and brand history**: origins, the operating system behind growth, turning points, consequences, and an ending that answers the opening question. Other niches use the same studio with a different editorial profile.

Adapted from [kelano86/what-if-animation](https://github.com/kelano86/what-if-animation), MIT licensed. The reusable SVG rig, sets, timing engine, storyboard tools, and audio mastering are preserved. Its 15–25 second speculative story formula is replaced for documentary work. See `NOTICE.md` for provenance.

## Choose the requested output

- **Research or ideas:** provide a source-backed niche brief and distinct concepts. Stop there when that is the request.
- **Scripts:** write complete spoken narration, descriptions, source notes, estimated duration, and optional visual direction. No TTS, sound generation, or video render is needed.
- **Storyboard:** use the studio to prepare and inspect stills. If the user asks to review the board before animation, show the completed board and wait for their response.
- **Video:** proceed through the production workflow only when video creation is requested. Existing authorization can cover successive stages; do not insert unnecessary approval questions.

Honor explicit limits such as “do not make videos yet.” Installing or using this skill does not authorize paid media generation, publication, or changes to another channel.

## Editorial profile

Read [company history](references/company-history.md) for the default niche. For another niche, read [niche adaptation](references/niche-adaptation.md) and create a compact project-specific profile before writing. Preserve the user's niche, audience, language, format, and chosen visual direction.

Research a reference channel through public channel metadata and several relevant uploads where accessible. Distinguish directly observed titles, durations, and visuals from inferences. Never invent retention, income, audience demographics, tools used, or performance explanations. A useful format may be borrowed; scripts, phrasing, scenes, thumbnails, and brand identity must be original.

## Research and scripting

1. Define the story question, audience, historical cutoff, target duration, and distinctive angle. If duration is unspecified, choose an appropriate length and state the estimate.
2. Build a chronology and claim ledger. Use company archives for dated milestones, filings for business mechanics, and independent primary records for disputed events. Do not treat company promotional claims as independent judgments.
3. Draft full narration using causal transitions: what happened, why a decision made sense then, what changed, who benefited, and who bore the cost. Explain the business or technical mechanism with a concrete example.
4. Check dates, names, quantities, chronology, and causal claims against the ledger. Mark interpretation as interpretation. No fabricated dialogue, inner thoughts, meetings, quotes, or unverified “almost went bankrupt” claims.
5. Count narration words and estimate duration at a declared reading rate. Distinguish narration from descriptions and production notes. Do not label a short script a 20-minute video.

For research artifacts and a planning-only episode, follow [the episode contract](references/episode-contract.md). Create scripts and documents without installing production dependencies or calling media APIs.

## Studio setup for later production

Copy `studio/` to a project workspace and run `npm ci` there. Requires Node 18+, Python 3.9+ with NumPy and Pillow, ffmpeg and ffprobe on PATH, plus an authorized ElevenLabs account only if using generated narration or effects. The packaged project is 1920 by 1080 at 30 fps; the supplied SVG engine assumes that coordinate system. Portrait output requires an intentional layout adaptation, not just changing the composition size.

Run commands below from the copied studio directory. `<skill>` denotes this installed skill folder. Episode files live under `src/episodes/<slug>/`; generated audio belongs under `public/<slug>/` and renders under `out/<slug>/`.

### Narration and timing

Write `episode.json` according to the contract and validate it offline:

```text
python <skill>/scripts/validate_episode.py src/episodes/<slug>/episode.json
python <skill>/scripts/voice.py <slug> --dry
```

The dry run reports the exact text volume and chunk count without contacting ElevenLabs. For authorized production, set `ELEVENLABS_API_KEY` in the environment or a local `.env`; never include secrets in the episode or repository. Then run `voice.py <slug>`.

The adapted voice helper divides long narration into bounded requests, caches each chunk by text and voice settings, preserves natural pauses, and writes one continuous `voice.wav` and global `words.json`. Set an explicit voice ID in `episode.json`; do not impersonate another narrator. Failed requests stop; completed chunks remain cached. Inspect pronunciation and joins before timing the edit. Character counts are usage measurements, not verified billed credits. Do not infer exact credit spend from other concurrent account activity.

### Shot list and storyboard

Read [animation direction](references/animation-direction.md), then the relevant sections of [the engine kit](references/kit.md). Add `shots`, `edit`, and optional `fx` to the episode and run:

```text
python <skill>/scripts/plan.py <slug>
```

Use `pace: {"min_cuts_per_min": 6, "max_shot_seconds": 18}` as a starting editorial setting for documentaries, then tune to the actual subject. These are configurable review thresholds, not measured traits of the reference channel. Use shorter cuts in the hook and longer readable holds for maps, timelines, and diagrams. Match factual labels to the narration's date.

Implement `shots.tsx` as pure functions of their shot clock `t`, add `index.tsx` with `defineEpisode`, and register it in `src/episodes/index.ts`. A contract and registration example are in `references/episode-contract.md`. Then:

```text
npx tsc --noEmit
node <skill>/scripts/stills.mjs <slug>
python <skill>/scripts/board.py <slug>
```

Open the board and every still. Check legibility, chronology, source labels, accurate chart scales, character continuity, intentional composition, and original visual identity. Use stylized human stand-ins for illustrative scenes; never present an invented scene as archival evidence. Inspect `references/traps.md` when working with the inherited rig.

### Animation and finishing

Animate only after the storyboard meets the brief. Inspect frame grids across each chapter, including transitions and the longest chart hold. For authorized sound generation, read `references/sound.md`; prefer a restrained bed, selective effects, and pauses around important numbers. Run `mixcheck.py` and listen for masked words.

```text
python <skill>/scripts/master.py <slug>
python <skill>/scripts/motiongrid.py <slug> <shot-id>
```

For long episodes, render a chapter or a short frame range first to catch visual defects and estimate compute time. `master.py` supports repeated `--frames START-END` runs, plus `--concurrency`; a preview range is labeled separately and is not the full deliverable. Do not master a silent preview as the finished film. Final mastering targets about -14 LUFS and a true peak below -1 dBTP. Watch and listen to the entire final export. Report actual duration, checks performed, known limitations, and verified or unavailable credit usage accurately.

## Deliverables

For a script request, deliver the requested document and useful research notes. For a production request, deliver the final MP4, storyboard, source ledger, and an honest technical report. Publishing to YouTube, purchasing media, or pushing changes to GitHub requires the user's corresponding authorization.
