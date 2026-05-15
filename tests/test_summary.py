import unittest

from backend.summary import batch_yield


def make_generator(value):
    yield f"progress-{value}"
    return f"result-{value}"


class SummaryTestCase(unittest.TestCase):
    def test_batch_yield_returns_results_to_explicit_ret(self):
        ret = []
        yields = list(batch_yield([make_generator(1), make_generator(2)], ret=ret))

        self.assertEqual(yields, [["progress-1", "progress-2"]])
        self.assertEqual(ret, ["result-1", "result-2"])

    def test_batch_yield_does_not_share_default_ret(self):
        first = list(batch_yield([make_generator(1)]))
        second = list(batch_yield([make_generator(2)]))

        self.assertEqual(first, [["progress-1"]])
        self.assertEqual(second, [["progress-2"]])


if __name__ == "__main__":
    unittest.main()
