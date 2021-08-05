# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from math import isclose

from ..aggregate import aggregate_if_possible, MeanStd, BinCount


def test_aggregate_if_possible():
    assert aggregate_if_possible("test") == "test"

    assert aggregate_if_possible(["a", "a"]) == "a"

    mean_std = aggregate_if_possible([0.5, 1.0, 1.5])
    assert isinstance(mean_std, MeanStd)
    assert isclose(mean_std.mean, 1)

    counts = aggregate_if_possible(["a", "a", "b"])
    assert isinstance(counts, tuple)
    assert all(isinstance(c, BinCount) for c in counts)

    counts = aggregate_if_possible([counts, counts])
    assert isinstance(counts, tuple)
    assert all(isinstance(c, BinCount) for c in counts)


def test_aggregate_if_possible_dict():
    dict_a = {"Mean": 1.0}
    dict_b = {"Mean": 2.0}

    counts = aggregate_if_possible([dict_a, dict_a, dict_b])
    assert all(isinstance(c, BinCount) and isinstance(c.value, dict) for c in counts)

    counts = aggregate_if_possible([counts, counts])
    assert isinstance(counts, tuple)
    assert all(isinstance(c, BinCount) and isinstance(c.value, dict) for c in counts)
