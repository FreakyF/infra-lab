_TABLE = (
    0x486E26EE, 0xDCAA16B3, 0xE1918EEF, 0x202DAFDB,
    0x341C7DC7, 0x1C365303, 0x40EF2D37, 0x65FD5E49,
    0xD6057177, 0x904ECE93, 0x1C38024F, 0x98FD323B,
    0xE3061AE7, 0xA39B0FA1, 0x9797F25F, 0xE4444563,
)
_MASK = 0xFFFFFFFF


def sstrhash(text: str, *, seed: int = 0x7FED7FED) -> int:
    shift = 0xEEEEEEEE
    for ch in text:
        c = ord("\\") if ch == "/" else ord(ch.upper())
        seed = ((_TABLE[c >> 4] - _TABLE[c & 0xF]) & _MASK) ^ ((shift + seed) & _MASK)
        seed &= _MASK
        shift = (c + seed + 33 * shift + 3) & _MASK
    return seed or 1
