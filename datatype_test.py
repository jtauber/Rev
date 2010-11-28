#!/usr/bin/env python3.1

from Rev import Repo

repo = Repo()

s = repo.shrink("foo")
n = repo.shrink(5.2)
d = repo.shrink({"foo": 5.2})
l = repo.shrink(["foo", 5.2, {"foo": 5.2}])
t = repo.shrink(("foo", 5.2))

assert repo.expand(s) == "foo"
assert repo.expand(n) == 5.2
assert repo.expand(d) == {"foo": 5.2}
assert repo.expand(l) == ["foo", 5.2, {"foo": 5.2}]
assert repo.expand(t) == ("foo", 5.2)

assert repo.shrink({"a": 1, "b": 2}) == repo.shrink({"b": 2, "a": 1})