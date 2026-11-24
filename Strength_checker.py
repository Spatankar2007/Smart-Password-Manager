import re

def check_strength(password):
    strength = 0
    remarks = ""

    if len(password) >= 8: strength += 1
    else: remarks += "Too short. "

    if re.search(r"[A-Z]", password): strength += 1
    else: remarks += "Add uppercase. "

    if re.search(r"[a-z]", password): strength += 1
    else: remarks += "Add lowercase. "

    if re.search(r"[0-9]", password): strength += 1
    else: remarks += "Add numbers. "

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): strength += 1
    else: remarks += "Add symbols. "

    if strength == 5: return "Strong "
    elif strength >= 3: return "Moderate  - " + remarks
    else: return "Weak  - " + remarks

print(check_strength("Shrushti123"))
print(check_strength("S@fePass2026"))
