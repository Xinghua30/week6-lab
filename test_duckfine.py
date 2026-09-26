import unittest

from duckfine import DuckFine


class DuckFineTests(unittest.TestCase):
    def setUp(self):
        self.fine = DuckFine(member_id="member-123")

    def test_member_id_is_recorded(self):
        self.assertEqual(self.fine.member_id, "member-123")

    def test_first_two_days_late_are_free(self):
        self.assertEqual(self.fine.charge(2), 0.0)

    def test_standard_fine_is_fifty_cents_per_day_after_grace(self):
        self.assertEqual(self.fine.charge(4), 1.00)

    def test_deluxe_fine_is_doubled(self):
        self.assertEqual(self.fine.charge(4, deluxe=True), 2.00)

    def test_single_fine_is_capped_at_five_dollars(self):
        self.assertEqual(self.fine.charge(20), 5.00)

    def test_fines_accumulate_on_the_member_account(self):
        self.fine.charge(4)
        self.fine.charge(3)
        self.assertEqual(self.fine.total_owed, 1.50)

    def test_negative_days_late_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "days_late must not be negative"):
            self.fine.charge(-1)


if __name__ == "__main__":
    unittest.main()
