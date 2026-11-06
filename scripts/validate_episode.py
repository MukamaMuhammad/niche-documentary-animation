"""Offline structure and duration checks; no API calls or media output."""
import argparse
import json
import re
from pathlib import Path


def validate(ep):
    errors = []
    for key in ('id', 'slug', 'topic', 'script'):
        if not ep.get(key):
            errors.append(f'Missing {key}')
    if not re.fullmatch(r'[A-Z][A-Za-z0-9]*', str(ep.get('id', ''))):
        errors.append('id must be an alphanumeric PascalCase composition name')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', str(ep.get('slug', ''))):
        errors.append('slug must contain lowercase words and hyphens')
    script = ep.get('script', [])
    if not isinstance(script, list) or any(not isinstance(x, dict) or not isinstance(x.get('text'), str) or not x['text'].strip() for x in script):
        errors.append('script must contain objects with nonempty text')
    sources = ep.get('sources', [])
    if not isinstance(sources, list) or any(not isinstance(s, dict) or not s.get('id') or not str(s.get('url', '')).startswith(('https://', 'http://')) for s in sources):
        errors.append('sources must have IDs and HTTP URLs')
        sources = []
    ids = [s['id'] for s in sources]
    if len(ids) != len(set(ids)):
        errors.append('Duplicate source IDs')
    for claim in ep.get('claims', []):
        if not claim.get('claim') or not claim.get('source_ids') or any(s not in ids for s in claim.get('source_ids', [])):
            errors.append(f'Claim {claim.get("id", "?")} has missing text or unresolved source IDs')
    shots = ep.get('shots', [])
    shot_ids = [s.get('id') for s in shots]
    if len(shot_ids) != len(set(shot_ids)):
        errors.append('Duplicate shot IDs')
    for item in ep.get('edit', []):
        if item.get('shot') not in shot_ids or 'at' not in item:
            errors.append('Edit refers to an undefined shot or lacks a cue')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('episode', type=Path)
    parser.add_argument('--wpm', type=float, default=140)
    args = parser.parse_args()
    if args.wpm <= 0:
        parser.error('--wpm must be positive')
    ep = json.loads(args.episode.read_text(encoding='utf-8-sig'))
    errors = validate(ep)
    words = sum(len(re.findall(r"\b[\w]+(?:['’-][\w]+)*\b", x.get('text', ''))) for x in ep.get('script', []) if isinstance(x, dict))
    print(json.dumps({'words': words, 'narration_minutes': round(words / args.wpm, 2), 'wpm': args.wpm, 'errors': errors}, indent=2))
    raise SystemExit(bool(errors))


if __name__ == '__main__':
    main()
