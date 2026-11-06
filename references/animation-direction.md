# Documentary animation direction

## Clarity and pacing

Use the opening question to choose the first image. A factory, parcel, ticket, or furniture box is more specific than a generic person pointing at a logo. Alternate scenes and diagrams according to what the narration needs to explain. Do not alternate angles mechanically when a single chart needs a readable hold.

An initial planning range is 2–5 seconds per hook image and 5–15 seconds for a developed diagram, with up to 18 seconds when labels and motion build the explanation. These are design suggestions; tune after listening to the narration. In `episode.json`, `pace.min_cuts_per_min` and `pace.max_shot_seconds` control review warnings. They do not change the edit automatically.

Use one unit, date, or category at a time on screen. A chart starts with readable axes. Data labels are dated and sourced; illustrative diagrams are not presented as measured data. Keep money flows directionally clear and distinguish company revenue from network-wide sales. Use chapter transitions to orient viewers in time.

## Drawing and motion

The bundled engine draws in 1920 by 1080 coordinates. Read `kit.md` for the rig, room kit, camera functions, lighting, and reusable sets. The engine's grain and vignette can be disabled with `grain: false, vignette: false`; this is often better for small data labels.

Every drawing is deterministic for a given shot clock. Reuse object models and silhouettes across shots, with unique SVG IDs for gradients and masks. Prefer simple, deliberate movement over constant decorative motion. Show chronology, flow, scale, assembly, or a choice changing an outcome.

Cast members are illustrative stand-ins. Use labels when a stylized historical person appears, and avoid invented expressions or actions that imply an undocumented event. Real logos may identify the documentary subject; do not copy a competing creator's mascot or use a logo to imply endorsement.

## Review before motion

Open every still and inspect:

- the key subject and causal relationship are readable at phone size;
- dates, names, quantities, units, maps, and chart scales agree with the ledger;
- the main action is visible on the first frame of the shot;
- labels remain inside safe margins and are not covered by subtitles;
- repeated people and objects retain their identity and scale;
- the board mixes explanatory diagrams and story scenes intentionally;
- source footage, if later added, has documented usage rights;
- no AI illustration is misrepresented as historical photography.

For motion, inspect starts, middles, ends, and transitions in every chapter. Check audio synchronization, narration joins, chart hold times, subtitle accuracy, flashing effects, and complete final duration. A clean short preview does not validate an entire documentary.
