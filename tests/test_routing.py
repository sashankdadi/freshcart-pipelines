from stream.routing_check import topic_match


def test_star_matches_exactly_one_word():
    assert topic_match("a.*", "a.b")
    assert not topic_match("a.*", "a")
    assert not topic_match("a.*", "a.b.c")


def test_hash_matches_zero_or_more_words():
    assert topic_match("a.#", "a")
    assert topic_match("a.#", "a.b.c")
    assert topic_match("#", "x.y")
    assert not topic_match("a.#", "b.c")


def test_literal_words_must_match():
    assert topic_match("a.b.c", "a.b.c")
    assert not topic_match("a.b.c", "a.b.d")
