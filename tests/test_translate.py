import pytest

from app.translator import translate, available_languages


class TestCanonical:
    def test_lol_to_kek_orcish(self):
        assert translate("lol", "orcish") == "kek"

    def test_lol_to_bur_common(self):
        assert translate("lol", "common") == "bur"

    def test_lol_casing_preserved(self):
        assert translate("Lol", "orcish") == "Kek"
        assert translate("LOL", "orcish") == "KEK"


class TestDeterminism:
    @pytest.mark.parametrize("lang", available_languages())
    def test_repeated_calls(self, lang: str):
        first = translate("For the Horde!", lang)
        for _ in range(50):
            assert translate("For the Horde!", lang) == first


class TestPunctuation:
    def test_punctuation_preserved(self):
        result = translate("Hello, world!", "orcish")
        assert "," in result
        assert "!" in result
        assert " " in result

    def test_question_mark(self):
        assert translate("How?", "orcish").endswith("?")


class TestCasing:
    @pytest.mark.parametrize("lang", available_languages())
    def test_all_upper(self, lang: str):
        assert translate("HELLO", lang) == translate("HELLO", lang).upper()

    @pytest.mark.parametrize("lang", available_languages())
    def test_all_lower(self, lang: str):
        assert translate("hello", lang) == translate("hello", lang).lower()

    @pytest.mark.parametrize("lang", available_languages())
    def test_title_case(self, lang: str):
        result = translate("Hello", lang)
        assert result[0].isupper()
        assert all(c.islower() for c in result[1:] if c.isalpha())


class TestEdgeCases:
    def test_empty_string(self):
        assert translate("", "orcish") == ""

    def test_only_spaces(self):
        assert translate("   ", "orcish") == "   "

    def test_only_punctuation(self):
        assert translate("...", "orcish") == "..."

    def test_single_char(self):
        result = translate("I", "orcish")
        assert len(result) == 1
        assert result.isalpha()

    def test_unknown_language_raises(self):
        with pytest.raises(KeyError):
            translate("hello", "pandaren")

    def test_very_long_word(self):
        result = translate("abcdefghijklmnopqrstuvwxyz", "orcish")
        assert len(result) > 0

    @pytest.mark.parametrize("lang", available_languages())
    def test_numbers_passthrough(self, lang: str):
        assert translate("123", lang) == "123"

    @pytest.mark.parametrize("lang", available_languages())
    def test_mixed_content(self, lang: str):
        result = translate("Player1 killed Player2", lang)
        assert "1" in result
        assert "2" in result
