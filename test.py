import math
import random
import unittest

from vector import Vector

TOL = 1e-9


class TestMean(unittest.TestCase):
    def test_known_value(self):
        self.assertAlmostEqual(Vector([1, 2, 3, 4]).mean(), 2.5)

    def test_single_entry(self):
        self.assertAlmostEqual(Vector([7]).mean(), 7.0)

    def test_negative_entries(self):
        self.assertAlmostEqual(Vector([-2, 2, -4, 4]).mean(), 0.0)

    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            Vector([]).mean()

    def test_constant_vector(self):
        self.assertAlmostEqual(Vector([5, 5, 5]).mean(), 5.0)

    def test_scaling(self):  # avg(a x) = a avg(x)
        x = Vector([1, 4, -2, 7])
        self.assertAlmostEqual((x * 3.5).mean(), 3.5 * x.mean())

    def test_additivity(self):  # avg(x + y) = avg(x) + avg(y)
        x, y = Vector([1, 4, -2]), Vector([0.5, 2, 9])
        self.assertAlmostEqual((x + y).mean(), x.mean() + y.mean())

    def test_shift(self):  # avg(x + b1) = avg(x) + b
        x = Vector([1, 4, -2])
        self.assertAlmostEqual((x + Vector([10] * 3)).mean(), x.mean() + 10)


class TestDemean(unittest.TestCase):
    def test_known_value(self):
        d = Vector([1, 2, 3]).demean()
        for a, b in zip(d, [-1, 0, 1]):
            self.assertAlmostEqual(a, b)

    def test_returns_new_vector_original_unchanged(self):
        x = Vector([1, 2, 3])
        d = x.demean()
        self.assertIsNot(d, x)
        self.assertEqual(x.entries, [1.0, 2.0, 3.0])

    def test_same_length(self):
        x = Vector([3, 1, 4, 1, 5])
        self.assertEqual(len(x.demean()), len(x))

    def test_mean_is_zero(self):  # avg(x_tilde) = 0
        random.seed(0)
        for _ in range(20):
            x = Vector([random.uniform(-100, 100) for _ in range(10)])
            self.assertAlmostEqual(x.demean().mean(), 0.0, delta=TOL)

    def test_constant_vector_gives_zero(self):
        d = Vector([4, 4, 4]).demean()
        self.assertTrue(all(abs(a) < TOL for a in d))

    def test_idempotent(self):
        x = Vector([2, 9, -3, 5])
        for a, b in zip(x.demean().demean(), x.demean()):
            self.assertAlmostEqual(a, b)

    def test_shift_invariant(self):  # demean(x + b1) = demean(x)
        x = Vector([2, 9, -3, 5])
        shifted = x + Vector([100] * 4)
        for a, b in zip(shifted.demean(), x.demean()):
            self.assertAlmostEqual(a, b)

    def test_x_equals_demean_plus_mean(self):  # x = x_tilde + avg(x) 1
        x = Vector([2, 9, -3, 5])
        rebuilt = x.demean() + Vector([x.mean()] * 4)
        for a, b in zip(rebuilt, x):
            self.assertAlmostEqual(a, b)


class TestStd(unittest.TestCase):
    def test_known_value(self):
        # deviations -1, 0, 1 -> sqrt(2/3)
        self.assertAlmostEqual(Vector([1, 2, 3]).std(), math.sqrt(2 / 3))

    def test_known_value_2(self):
        self.assertAlmostEqual(Vector([2, 4, 4, 4, 5, 5, 7, 9]).std(), 2.0)

    def test_nonnegative(self):
        random.seed(1)
        for _ in range(20):
            x = Vector([random.uniform(-50, 50) for _ in range(8)])
            self.assertGreaterEqual(x.std(), 0.0)

    def test_zero_iff_constant(self):
        self.assertAlmostEqual(Vector([3, 3, 3, 3]).std(), 0.0)
        self.assertGreater(Vector([3, 3, 3, 3.1]).std(), 0.0)

    def test_equals_rms_of_demeaned(self):  # std(x) = rms(x_tilde)
        x = Vector([2, 9, -3, 5])
        self.assertAlmostEqual(x.std(), x.demean().rms())

    def test_equals_norm_formula(self):  # std(x) = ||x - avg(x)1|| / sqrt(n)
        x = Vector([2, 9, -3, 5])
        expected = (x - Vector([x.mean()] * 4)).norm() / math.sqrt(4)
        self.assertAlmostEqual(x.std(), expected)

    def test_shift_invariant(self):  # std(x + b1) = std(x)
        x = Vector([2, 9, -3, 5])
        self.assertAlmostEqual((x + Vector([42] * 4)).std(), x.std())

    def test_scaling(self):  # std(a x) = |a| std(x)
        x = Vector([2, 9, -3, 5])
        for a in (3.0, -2.5, 0.0):
            self.assertAlmostEqual((x * a).std(), abs(a) * x.std())

    def test_rms_decomposition(self):  # rms(x)^2 = avg(x)^2 + std(x)^2
        random.seed(2)
        for _ in range(20):
            x = Vector([random.uniform(-10, 10) for _ in range(9)])
            self.assertAlmostEqual(x.rms() ** 2, x.mean() ** 2 + x.std() ** 2)

    def test_chebyshev_inequality(self):
        # fraction of entries with |x_i - avg| >= a*std is <= 1/a^2
        random.seed(3)
        x = Vector([random.gauss(0, 5) for _ in range(500)])
        m, s = x.mean(), x.std()
        for a in (1.5, 2, 3):
            frac = sum(1 for xi in x if abs(xi - m) >= a * s) / len(x)
            self.assertLessEqual(frac, 1 / a ** 2 + TOL)

    def test_single_entry(self):
        self.assertAlmostEqual(Vector([9]).std(), 0.0)


if __name__ == "__main__":
    unittest.main()
