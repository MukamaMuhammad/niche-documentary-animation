"""Offline checks for long-form narration and episode references. No media generation."""
import unittest
from narration_chunks import aligned_words, narration_chunks, split_text
from validate_episode import validate


class DocumentaryChecks(unittest.TestCase):
    def test_long_narration_preserves_every_word(self):
        text = ' '.join(f'word{i}' for i in range(6000))
        parts = split_text(text, 3500)
        self.assertGreater(len(parts), 5)
        self.assertEqual(' '.join(parts), text)
        self.assertTrue(all(0 < len(p) <= 3500 for p in parts))

    def test_chapter_boundaries_are_preserved(self):
        parts = narration_chunks([{'chapter': 'First', 'text': 'x ' * 200}, {'chapter': 'Second', 'text': 'last words'}], 100)
        self.assertEqual(sum(p['chapter_end'] for p in parts), 2)
        self.assertEqual(parts[-1]['chapter'], 'Second')

    def test_word_alignment_uses_real_audio_offset(self):
        alignment = {'characters': list('Hi, go.'), 'character_start_times_seconds': [0, .1, .2, .3, .4, .5, .6],
                     'character_end_times_seconds': [.1, .2, .3, .4, .5, .6, .7]}
        words = aligned_words(alignment, 25.125)
        self.assertEqual([w['w'] for w in words], ['Hi', 'go'])
        self.assertEqual(words[0]['s'], 25.125)
        self.assertEqual(words[1]['e'], 25.725)
        self.assertEqual(words[0]['p'], ',')

    def test_invalid_alignment_stops(self):
        with self.assertRaises(ValueError):
            aligned_words({'characters': ['a'], 'character_start_times_seconds': [], 'character_end_times_seconds': []})

    def test_missing_claim_source_is_rejected(self):
        ep = {'id': 'Demo', 'slug': 'demo', 'topic': 'Example', 'script': [{'text': 'A full line.'}],
              'claims': [{'id': 'C1', 'claim': 'An unsupported claim', 'source_ids': ['missing']}]}
        self.assertTrue(validate(ep))

    def test_minimal_planning_episode_needs_no_media(self):
        self.assertEqual(validate({'id': 'Demo', 'slug': 'demo', 'topic': 'Example', 'script': [{'text': 'A full line.'}]}), [])


if __name__ == '__main__':
    unittest.main()
