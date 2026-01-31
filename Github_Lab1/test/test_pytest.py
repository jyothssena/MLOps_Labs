

# test_password_checker.py
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from password_check import check_password_strength

def test_very_weak_password():
    result = check_password_strength("abc")
    assert result["score"] == 1
    assert result["strength"] == "Very Weak"
    assert len(result["feedback"]) == 4

def test_weak_password():
    result = check_password_strength("abcdefgh")
    assert result["score"] == 2
    assert result["strength"] == "Weak"
    assert "Add uppercase letters" in result["feedback"]

def test_fair_password():
    result = check_password_strength("Abcdefgh")
    assert result["score"] == 3
    assert result["strength"] == "Fair"

def test_good_password():
    result = check_password_strength("Abcdefg1")
    assert result["score"] == 4
    assert result["strength"] == "Good"
    assert "Add special characters" in result["feedback"]

def test_strong_password():
    result = check_password_strength("Abcdefg1!")
    assert result["score"] == 5
    assert result["strength"] == "Strong"
    assert len(result["feedback"]) == 0

def test_empty_password():
    result = check_password_strength("")
    assert result["score"] == 0
    assert result["strength"] == "Very Weak"
    assert len(result["feedback"]) == 5

def test_minimum_length_boundary():
    # 7 characters - should miss length requirement
    result = check_password_strength("Abcde1!")
    assert result["score"] == 4  # Missing length requirement
    
    # 8 characters - should meet all requirements
    result = check_password_strength("Abcdef1!")
    assert result["score"] == 5  # Meets all requirements

def test_all_special_characters():
    result = check_password_strength("!@#$%^&*Aa1")
    assert result["score"] == 5
    assert result["strength"] == "Strong"

def test_numbers_only():
    result = check_password_strength("12345678")
    assert result["score"] == 2
    assert "Add uppercase letters" in result["feedback"]
    assert "Add lowercase letters" in result["feedback"]

@pytest.mark.parametrize("password,expected_score", [
    ("a", 1),
    ("aB", 2),
    ("aB1", 3),
    ("aB1!", 4),
    ("aB1!aaaa", 5),
])
def test_progressive_strength(password, expected_score):
    result = check_password_strength(password)
    assert result["score"] == expected_score