# Episode and research contract

Keep research and production files separate. A research-only package may contain `research.md`, `claims.json`, `script.md`, and a requested Word document. It does not require an initialized studio, voice settings, or media files.

## Planning episode

```json
{
  "id": "ExampleCompany",
  "slug": "example-company",
  "niche": "company-history",
  "topic": "How an illustrative business scaled",
  "title": ["A COMPANY", "AND ITS SYSTEM"],
  "historical_cutoff": "2025-12-31",
  "target_minutes": 15,
  "script": [
    {"chapter": "Opening", "text": "Complete narration goes here."},
    {"chapter": "Origins", "text": "The next chapter's complete narration goes here."}
  ],
  "claims": [
    {"id": "C1", "claim": "A specific historical claim", "source_ids": ["S1"], "status": "verified"}
  ],
  "sources": [
    {"id": "S1", "title": "Primary archive", "url": "https://example.org/archive", "accessed": "2026-11-06", "type": "primary"}
  ],
  "pace": {"min_cuts_per_min": 6, "max_shot_seconds": 18}
}
```

This is a schema illustration rather than a researched episode. Replace example content before production. Script entries are chapter-sized or smaller beats with `text`; their `chapter` label is not narrated. The voice helper chunks long entries without requiring a single large API request.

## Production additions

Add `voice: {"id": "YOUR_AUTHORIZED_VOICE_ID", "model": "eleven_multilingual_v2"}` when generating narration. Optional `voice.max_chars` defaults to 3500 and `voice.chapter_pause` defaults to 0.45 seconds. Optional `voice.settings` contains provider settings. Use a model whose current text and account limits support the chunk size. `voice.py --dry` is offline; generation is not.

After voice timings exist, add `shots` and `edit` using the inherited contract:

```json
{
  "shots": [
    {"id": "S1", "size": "wide", "key": 40, "note": "An original opening illustration"},
    {"id": "S2", "size": "diagram", "key": 60, "note": "The mechanism begins"}
  ],
  "edit": [{"shot": "S1", "at": "f:0"}, {"shot": "S2", "at": "s:5"}]
}
```

Use an explicit `end: "s:12"` only for a deliberate offline timing test. Production duration follows the final word timings and `tail`, unless an intentional ending cue overrides it. Shot keys and cue times are frames or seconds as specified, not historical dates.

`plan.py` creates `timeline.json`. A minimal episode wrapper is:

```tsx
import { defineEpisode } from '../../engine';
import timeline from './timeline.json';
import { shots } from './shots';
export default defineEpisode('ExampleCompany', {
  timeline, shots, grain: false, vignette: false,
});
```

Export a typed `shots` map from `shots.tsx`. Register the default export in `src/episodes/index.ts` by importing it and adding it to `EPISODES`. The shipped registry is intentionally empty: the engine is a reusable studio, not a completed documentary.

## Claim ledger

Map important factual passages to claim IDs in a sidecar ledger, or add `claim_ids` to script entries. Record the exact supporting source section or page and the access date. Use `verified`, `attributed`, or `needs-check` status honestly. The validator checks structure and source references; it cannot verify the truth of a source or the fairness of an interpretation.
