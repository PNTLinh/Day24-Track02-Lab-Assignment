"""PII detection helpers for Vietnamese medical data."""

from __future__ import annotations

import re

from presidio_analyzer import RecognizerResult


class VietnameseRegexAnalyzer:
    """Small regex-based analyzer that mimics the Presidio analyze() API."""

    PATTERNS = {
        "PERSON": re.compile(
            r"\b(?:[A-ZÀ-ỸĐ][A-Za-zÀ-ỹĐđ'’-]*\s+){1,3}[A-ZÀ-ỸĐ][A-Za-zÀ-ỹĐđ'’-]*\b"
        ),
        "EMAIL_ADDRESS": re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}\b"),
        "VN_CCCD": re.compile(r"\b\d{10,12}\b"),
        "VN_PHONE": re.compile(r"\b(?:0)?(?:3|5|7|8|9)\d{8}\b"),
    }

    def analyze(self, text: str, language: str = "vi", entities: list | None = None):
        requested_entities = entities or list(self.PATTERNS)
        results = []

        for entity in requested_entities:
            pattern = self.PATTERNS.get(entity)
            if pattern is None:
                continue

            score = 0.95 if entity in {"VN_CCCD", "VN_PHONE", "EMAIL_ADDRESS"} else 0.75
            for match in pattern.finditer(text):
                results.append(
                    RecognizerResult(
                        entity_type=entity,
                        start=match.start(),
                        end=match.end(),
                        score=score,
                    )
                )

        return sorted(results, key=lambda result: (result.start, result.end))

def build_vietnamese_analyzer() -> VietnameseRegexAnalyzer:
    """
    TODO: Xây dựng AnalyzerEngine với các recognizer tùy chỉnh cho VN.
    """

    return VietnameseRegexAnalyzer()


def detect_pii(text: str, analyzer) -> list:
    """
    TODO: Detect PII trong text tiếng Việt.
    Trả về list các RecognizerResult.
    Entities cần detect: PERSON, EMAIL_ADDRESS, VN_CCCD, VN_PHONE
    """
    results = analyzer.analyze(
        text=text,
        language="vi",
        entities=["PERSON", "EMAIL_ADDRESS", "VN_CCCD", "VN_PHONE"]
    )
    return results
