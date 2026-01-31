# test_password_checker.py
import unittest
from password_checker import check_password_strength

class TestPasswordStrengthChecker(unittest.TestCase):
    
    def test_very_weak_password(self):
        """Test password with minimal criteria met"""
        result = check_password_strength("abc")
        self.assertEqual(result["score"], 1)
        self.assertEqual(result["strength"], "Very Weak")
        self.assertEqual(len(result["feedback"]), 4)
    
    def test_weak_password(self):
        """Test password with only lowercase and length"""
        result = check_password_strength("abcdefgh")
        self.assertEqual(result["score"], 2)
        self.assertEqual(result["strength"], "Weak")
        self.assertIn("Add uppercase letters", result["feedback"])
    
    def test_fair_password(self):
        """Test password with uppercase, lowercase, and length"""
        result = check_password_strength("Abcdefgh")
        self.assertEqual(result["score"], 3)
        self.assertEqual(result["strength"], "Fair")
    
    def test_good_password(self):
        """Test password missing only special characters"""
        result = check_password_strength("Abcdefg1")
        self.assertEqual(result["score"], 4)
        self.assertEqual(result["strength"], "Good")
        self.assertIn("Add special characters", result["feedback"])
    
    def test_strong_password(self):
        """Test password meeting all criteria"""
        result = check_password_strength("Abcdefg1!")
        self.assertEqual(result["score"], 5)
        self.assertEqual(result["strength"], "Strong")
        self.assertEqual(len(result["feedback"]), 0)
    
    def test_empty_password(self):
        """Test empty string"""
        result = check_password_strength("")
        self.assertEqual(result["score"], 0)
        self.assertEqual(result["strength"], "Very Weak")
        self.assertEqual(len(result["feedback"]), 5)
    
    def test_minimum_length_boundary(self):
        """Test exactly at length boundary"""
        result = check_password_strength("Abcdef1!")
        self.assertEqual(result["score"], 4)  # 7 chars, missing length
        
        result = check_password_strength("Abcdefg1!")
        self.assertEqual(result["score"], 5)  # 9 chars, meets all
    
    def test_all_special_characters(self):
        """Test password with all types of special characters"""
        result = check_password_strength("!@#$%^&*Aa1")
        self.assertEqual(result["score"], 5)
        self.assertEqual(result["strength"], "Strong")
    
    def test_numbers_only(self):
        """Test password with only numbers"""
        result = check_password_strength("12345678")
        self.assertEqual(result["score"], 2)
        self.assertIn("Add uppercase letters", result["feedback"])
        self.assertIn("Add lowercase letters", result["feedback"])
    
    def test_uppercase_only(self):
        """Test password with only uppercase letters"""
        result = check_password_strength("ABCDEFGH")
        self.assertEqual(result["score"], 2)
        self.assertIn("Add lowercase letters", result["feedback"])
        self.assertIn("Add numbers", result["feedback"])
        self.assertIn("Add special characters", result["feedback"])
    
    def test_has_uppercase_criteria(self):
        """Test that uppercase detection works"""
        result = check_password_strength("Password1!")
        self.assertNotIn("Add uppercase letters", result["feedback"])
    
    def test_has_lowercase_criteria(self):
        """Test that lowercase detection works"""
        result = check_password_strength("PASSWORD1!")
        self.assertIn("Add lowercase letters", result["feedback"])
    
    def test_has_digit_criteria(self):
        """Test that digit detection works"""
        result = check_password_strength("Password!")
        self.assertIn("Add numbers", result["feedback"])
    
    def test_has_special_char_criteria(self):
        """Test that special character detection works"""
        result = check_password_strength("Password1")
        self.assertIn("Add special characters", result["feedback"])
    
    def test_long_password_all_criteria(self):
        """Test very long password with all criteria"""
        result = check_password_strength("MyVeryLongPassword123!@#")
        self.assertEqual(result["score"], 5)
        self.assertEqual(result["strength"], "Strong")


class TestProgressiveStrength(unittest.TestCase):
    """Test progressive improvement in password strength"""
    
    def test_score_progression(self):
        """Test that scores increase as criteria are met"""
        test_cases = [
            ("a", 1),
            ("aB", 2),
            ("aB1", 3),
            ("aB1!", 4),
            ("aB1!aaaa", 5),
        ]
        
        for password, expected_score in test_cases:
            with self.subTest(password=password):
                result = check_password_strength(password)
                self.assertEqual(result["score"], expected_score)


if __name__ == '__main__':
    unittest.main()