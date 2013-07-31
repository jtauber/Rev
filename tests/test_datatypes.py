from unittest import TestCase


class TestDatatypes(TestCase):
    
    def test_string(self):
        from rev import Repo
        repo = Repo()
        s = repo.shrink("foo")
        self.assertEqual(repo.expand(s), "foo")
    
    def test_number(self):
        from rev import Repo
        repo = Repo()
        n = repo.shrink(5.2)
        self.assertEqual(repo.expand(n), 5.2)
    
    def test_dictionary(self):
        from rev import Repo
        repo = Repo()
        d = repo.shrink({"foo": 5.2})
        self.assertEqual(repo.expand(d), {"foo": 5.2})
    
    def test_list(self):
        from rev import Repo
        repo = Repo()
        l = repo.shrink(["foo", 5.2, {"foo": 5.2}])
        self.assertEqual(repo.expand(l), ["foo", 5.2, {"foo": 5.2}])
    
    def test_tuple(self):
        from rev import Repo
        repo = Repo()
        t = repo.shrink(("foo", 5.2))
        self.assertEqual(repo.expand(t), ("foo", 5.2))
    
    def test_dictionary_equality(self):
        from rev import Repo
        repo = Repo()
        self.assertEqual(repo.shrink({"a": 1, "b": 2}), repo.shrink({"b": 2, "a": 1}))
