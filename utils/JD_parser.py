import re


def parse_jd_text(jd_text):
    if not jd_text:
        return ""

    cleaned_text = re.sub(r"\s+", " ", jd_text).strip()
    return cleaned_text