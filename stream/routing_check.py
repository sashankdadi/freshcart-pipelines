"""Offline checker for AMQP topic-exchange routing (use it AFTER writing your D1 predictions).

    python stream/routing_check.py
"""
DRIVERS = {
    "Ravi": "bangalore.koramangala.*",
    "Priya": "bangalore.indiranagar.*",
    "Arjun": "bangalore.*.ride",
    "Meena": "bangalore.*.food",
    "Karthik": "chennai.tnagar.food",
    "Control": "bangalore.#",
}
KEYS = [
    "bangalore.koramangala.food",
    "bangalore.indiranagar.ride",
    "bangalore.whitefield.ride",
    "chennai.tnagar.food",
    "chennai.whitefield.ride",
    "bangalore.koramangala",
]


def topic_match(pattern: str, key: str) -> bool:
    """RabbitMQ topic rules: words split on '.', '*' = exactly one word, '#' = zero or more words."""
    def rec(p, k):
        if not p:
            return not k
        if p[0] == "#":
            return any(rec(p[1:], k[i:]) for i in range(len(k) + 1))
        if not k:
            return False
        return (p[0] == "*" or p[0] == k[0]) and rec(p[1:], k[1:])
    return rec(pattern.split("."), key.split("."))


if __name__ == "__main__":
    for i, key in enumerate(KEYS, 1):
        hits = [n for n, pat in DRIVERS.items() if topic_match(pat, key)]
        print(f"{i}  {key:30s} -> {', '.join(hits) if hits else 'dropped'}")
