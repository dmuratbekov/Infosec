#!/usr/bin/env python3
import datetime

with open("/home/dan/home/test.log", "a") as f:
    f.write(f"New line at {datetime.datetime.now()}\n")

