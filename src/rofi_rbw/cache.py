from collections import defaultdict
from typing import List

from .paths import cache_file


def cached_entries_first(entries: List[str]) -> List[str]:
    cache_file.parent.mkdir(exist_ok=True)
    cache_file.touch(exist_ok=True)

    with cache_file.open() as f:
        for line in f:
            if line.strip():
                _, entry = line.strip().split(" ", maxsplit=1)
                if entry in entries:
                    entries.remove(entry)
                    entries = [entry, *entries]

    return entries


def update_cache(entry: str):
    entries = defaultdict(int)
    with cache_file.open() as f:
        for line in f:
            if line.strip():
                n, e = line.strip().split(" ", maxsplit=1)
                entries[e] = int(n)
    entries[entry] += 1
    with cache_file.open("w") as f:
        for n, e in sorted((n, e) for e, n in entries.items()):
            print(n, e, file=f)
