import pytest

from app.translator import available_languages
from app.translator.wordlists import get


class TestRegistry:
    def test_orcish_registered(self):
        assert "orcish" in available_languages()

    def test_common_registered(self):
        assert "common" in available_languages()

    def test_unknown_raises(self):
        with pytest.raises(KeyError):
            get("pandaren")


class TestWordlistIntegrity:
    @pytest.mark.parametrize("lang", available_languages())
    def test_buckets_keyed_by_length(self, lang: str):
        words = get(lang)
        for length, bucket in words.items():
            assert isinstance(length, int)
            assert length >= 1
            for word in bucket:
                assert len(word) == length, f"{lang}: {word!r} len {len(word)}, expected {length}"

    @pytest.mark.parametrize("lang", available_languages())
    def test_no_empty_buckets(self, lang: str):
        for length, bucket in get(lang).items():
            assert len(bucket) > 0

    @pytest.mark.parametrize("lang", available_languages())
    def test_starts_at_one(self, lang: str):
        assert 1 in get(lang)
