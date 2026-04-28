import re


PATTERN_UPPERCASE = re.compile(r"[A-Z]")
PATTERN_LOWERCASE = re.compile(r"[a-z]")
PATTERN_NUMBER = re.compile(r"\d")
PATTERN_SPECIAL_CHAR = re.compile(r"[@$!%*#?&]")


PATTERN_EMAIL = re.compile(r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$")


PATTERN_NAME = re.compile(r"^[a-zA-Z\s]+$")
