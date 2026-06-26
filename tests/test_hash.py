from app.translator.hash import sstrhash


class TestSStrHash:
    def test_case_insensitive(self):
        assert sstrhash("lol") == sstrhash("LOL") == sstrhash("Lol")

    def test_different_inputs_differ(self):
        assert sstrhash("lol") != sstrhash("rofl")

    def test_known_hash_value(self):
        assert sstrhash("lol") == 0xF7F5D858

    def test_empty_string(self):
        result = sstrhash("")
        assert isinstance(result, int)
        assert result > 0

    def test_deterministic(self):
        for _ in range(100):
            assert sstrhash("For the Horde") == sstrhash("For the Horde")
