"""Chapter-aware narration. --dry makes no network requests or media files."""
import argparse
import base64
import hashlib
import json
from pathlib import Path

from narration_chunks import aligned_words, narration_chunks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('slug')
    parser.add_argument('--dry', action='store_true')
    args = parser.parse_args()
    root = Path.cwd()
    epdir = root / 'src' / 'episodes' / args.slug
    ep = json.loads((epdir / 'episode.json').read_text(encoding='utf-8-sig'))
    config = ep.get('voice', {})
    limit = int(config.get('max_chars', 3500))
    chunks = narration_chunks(ep['script'], limit)
    print(json.dumps({'chunks': len(chunks), 'characters': sum(len(c['text']) for c in chunks),
                      'max_request_characters': max([len(c['text']) for c in chunks] or [0]),
                      'dry_run': args.dry, 'billed_credits': None}, indent=2))
    if args.dry:
        return
    voice_id = config.get('id')
    if not voice_id or voice_id.startswith('YOUR_'):
        raise SystemExit('Set an authorized voice.id in episode.json before generation')
    import numpy as np
    from wi import SR, api, decode, save_json, write_wav
    output = root / 'out' / args.slug
    public = root / 'public' / args.slug
    cache = output / 'narration-cache'
    cache.mkdir(parents=True, exist_ok=True)
    public.mkdir(parents=True, exist_ok=True)
    settings = {'model_id': config.get('model', 'eleven_multilingual_v2'),
                'voice_settings': config.get('settings', {'stability': 0.55, 'similarity_boost': 0.75})}
    parts, words, chapter_times, offset = [], [], [], 0.0
    pause = float(config.get('chapter_pause', 0.45))
    if pause < 0 or pause > 10:
        raise SystemExit('chapter_pause must be between 0 and 10 seconds')
    for i, chunk in enumerate(chunks):
        signature = hashlib.sha256(json.dumps([voice_id, settings, chunk['text']], sort_keys=True).encode()).hexdigest()
        mp3, alignfile = cache / f'{signature}.mp3', cache / f'{signature}.json'
        cached = mp3.exists() and alignfile.exists()
        if not cached:
            response = json.loads(api(f'/v1/text-to-speech/{voice_id}/with-timestamps?output_format=mp3_44100_128',
                                      {**settings, 'text': chunk['text']}))
            alignment = response.get('alignment')
            if not alignment:
                raise SystemExit(f'Chunk {i + 1} returned no alignment; stop and inspect provider response')
            aligned_words(alignment)
            mp3.write_bytes(base64.b64decode(response['audio_base64']))
            save_json(alignfile, alignment)
            costs_path = output / 'costs.json'
            costs = json.loads(costs_path.read_text(encoding='utf-8')) if costs_path.exists() else []
            costs.append({'step': 'voice', 'chunk_hash': signature, 'characters': len(chunk['text']),
                          'credits': None, 'note': 'Billed credit usage is unverified; consult provider billing.'})
            save_json(costs_path, costs)
        audio = decode(mp3)
        alignment = json.loads(alignfile.read_text(encoding='utf-8'))
        local = aligned_words(alignment)
        seconds = len(audio) / SR
        if local and local[-1]['e'] > seconds + 0.25:
            raise SystemExit(f'Chunk {i + 1} alignment exceeds decoded audio duration')
        if not chapter_times or chapter_times[-1]['beat'] != chunk['beat']:
            chapter_times.append({'beat': chunk['beat'], 'chapter': chunk['chapter'], 'start': round(offset, 4)})
        words.extend(aligned_words(alignment, offset))
        parts.append(audio)
        offset += seconds
        if chunk['chapter_end'] and i < len(chunks) - 1:
            silence = np.zeros(round(pause * SR))
            parts.append(silence)
            offset += len(silence) / SR
        print(f'Chunk {i + 1}/{len(chunks)}: {"cached" if cached else "generated"}; {seconds:.2f} seconds')
    if not parts:
        raise SystemExit('No narration text')
    write_wav(public / 'voice.wav', np.concatenate(parts))
    save_json(epdir / 'words.json', words)
    save_json(output / 'chapters.json', chapter_times)
    print(f'Narration: {offset:.2f} seconds. Credit charges remain unverified unless reconciled with billing.')


if __name__ == '__main__':
    main()
