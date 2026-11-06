"""Pure helpers for bounded narration requests and global word alignment."""
import re


def split_text(text, limit=3500):
    if limit < 100:
        raise ValueError('Chunk character limit must be at least 100')
    words = text.split()
    chunks, current = [], ''
    for word in words:
        if len(word) > limit:
            raise ValueError('A single token exceeds the character limit')
        candidate = (current + ' ' + word).strip()
        if len(candidate) > limit:
            chunks.append(current)
            current = word
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks


def narration_chunks(script, limit=3500):
    chunks = []
    for index, beat in enumerate(script):
        pieces = split_text(beat['text'], limit)
        for part, text in enumerate(pieces):
            chunks.append({'chapter': beat.get('chapter', f'Part {index + 1}'), 'text': text,
                           'chapter_end': part == len(pieces) - 1, 'beat': index})
    return chunks


def aligned_words(alignment, offset=0):
    chars = alignment['characters']
    starts = alignment['character_start_times_seconds']
    ends = alignment['character_end_times_seconds']
    if not (len(chars) == len(starts) == len(ends)):
        raise ValueError('Alignment arrays differ in length')
    words, current = [], None
    for char, start, end in zip(chars, starts, ends):
        if end < start or start < 0:
            raise ValueError('Invalid alignment interval')
        if re.match(r"[\w'’]", char):
            if current is None:
                current = {'w': '', 's': start + offset, 'e': end + offset, 'p': ''}
            current['w'] += char
            current['e'] = end + offset
        else:
            if current is not None:
                words.append(current)
                current = None
            if words and char.strip():
                words[-1]['p'] += char
    if current:
        words.append(current)
    return [{**w, 's': round(w['s'], 4), 'e': round(w['e'], 4)} for w in words]
