import unittest

from backend.security import hash_password, is_hashed_password, verify_password


class SecurityTests(unittest.TestCase):
    def test_hash_and_verify_roundtrip(self):
        hashed = hash_password("senha-super-forte")
        self.assertTrue(is_hashed_password(hashed))
        self.assertTrue(verify_password("senha-super-forte", hashed))
        self.assertFalse(verify_password("senha-errada", hashed))

    def test_legacy_plaintext_compatibility(self):
        self.assertTrue(verify_password("1234", "1234"))
        self.assertFalse(verify_password("1234", "12345"))

    def test_invalid_values(self):
        with self.assertRaises(ValueError):
            hash_password("")
        self.assertFalse(verify_password("", "qualquer"))
        self.assertFalse(verify_password("abc", ""))


if __name__ == "__main__":
    unittest.main()
