import sys


if len(sys.argv) < 3:
    print("Use: python3 generate_passwords_simple_final.py <first name> <last name> <dob YYYY-MM-DD> [file]")
    sys.exit(1)

first = sys.argv[1]
last = sys.argv[2]
dob = sys.argv[3] if len(sys.argv) > 3 else ""
outfile = sys.argv[4] if len(sys.argv) > 4 else "passwords.txt"

dob_parts = dob.split('-') if dob else []
dob_year = dob_parts[0] if len(dob_parts) == 3 else ""
dob_short = dob_year[2:] if dob_year else ""
dob_md = "".join(dob_parts[1:]) if len(dob_parts) == 3 else ""

passwords = []

passwords += [
    first, first.lower(), first.capitalize(),
    first + "123", first + "1234",
    first + "!", first + "@"
]

if last != "-":
    passwords += [
        first + last,
        first + "." + last,
        first + "_" + last,
        first[0] + last
    ]

if dob:
    for t in [dob_year, dob_short, dob_md]:
        if t:
            passwords.append(first + t)
            if last != "-":
                passwords.append(first + last + t)
                passwords.append(first + "." + last + t)

unique_passwords = []
for p in passwords:
    if p not in unique_passwords and 4 <= len(p) <= 30:
        unique_passwords.append(p)

with open(outfile, "w", encoding="utf-8") as f:
    for p in unique_passwords:
        f.write(p + "\n")

