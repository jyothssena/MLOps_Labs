# src/password_check.py
def check_password_strength(password):
    score = 0
    feedback = []
    
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Too short (need at least 8 characters)")
    
    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("Add uppercase letters")
    
    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("Add lowercase letters")
    
    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("Add numbers")
    
    if any(c in "!@#$%^&*" for c in password):
        score += 1
    else:
        feedback.append("Add special characters")
    
    strength_levels = ["Very Weak", "Weak", "Fair", "Good", "Strong"]
    strength = strength_levels[score - 1] if score > 0 else "Very Weak"
    
    return {
        "score": score,
        "strength": strength,
        "feedback": feedback
    }

# This code only runs when you execute the file directly, NOT when importing
if __name__ == "__main__":
    password = input("Enter a password to check: ")
    result = check_password_strength(password)
    print(f"\nPassword: {password}")
    print(f"Strength: {result['strength']} ({result['score']}/5)")
    if result['feedback']:
        print("Suggestions:", ", ".join(result['feedback']))