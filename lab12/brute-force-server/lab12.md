# Lab 12 — Brute-force Attacks

## Work Done

I learned how to perform brute-force attacks using the Hydra utility on a local test server. I also implemented my own password generation script based on user personal data.
follow the instructions from the laboratory:

## Pre-Installed 
- venv
- fastapi[standard]
- hydra

## How to run

- Run the server:
```
source venv/bin/activate
fastapi dev main.py

```
- Generation of personal passwords, running generate_pas.py:
```
python3 generate_pas.py  Abduldayev 1995-07-21 generate_pas.txt
```
- Attack with Hydra
```
hydra -f -I -V -L usernames.txt -P generate_pas.txt -s 8000 localhost http-form-post "/login:username=^USER^&password=^PASS^:F=Invalid"

```
