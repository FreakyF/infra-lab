from .hash import sstrhash
from .wordlists import get as get_wordlist

_MAX_WORD_LEN = 18


def _tokenize(text: str) -> list[tuple[str, bool]]:
    tokens: list[tuple[str, bool]] = []
    current: list[str] = []
    current_alpha: bool | None = None
    for ch in text:
        is_alpha = ch.isalpha()
        if current_alpha is not None and is_alpha != current_alpha:
            tokens.append(("".join(current), current_alpha))
            current = []
        current.append(ch)
        current_alpha = is_alpha
    if current:
        tokens.append(("".join(current), bool(current_alpha)))
    return tokens


def _apply_case(replacement: str, source: str) -> str:
    return "".join(
        r.upper() if i < len(source) and source[i].isupper() else r.lower()
        for i, r in enumerate(replacement)
    )


def translate(text: str, language: str) -> str:
    word_list = get_wordlist(language)

    parts: list[str] = []
    for chunk, is_word in _tokenize(text):
        if not is_word:
            parts.append(chunk)
            continue

        word_len = min(len(chunk), _MAX_WORD_LEN)

        group = None
        wl = word_len
        while wl >= 1:
            if wl in word_list:
                group = word_list[wl]
                break
            wl -= 1

        if not group:
            parts.append(chunk)
            continue

        idx = sstrhash(chunk) % len(group)
        parts.append(_apply_case(group[idx], chunk))

    return "".join(parts)
