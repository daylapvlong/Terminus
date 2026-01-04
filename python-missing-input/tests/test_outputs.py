"""Tests for the bug fix task."""
import pytest
import sys

def process(data):
    return data[0] + list(data)

def test_empty_input_returns_empty_list():
    """Verify empty input is handled gracefully."""
    result = process("")
    assert result == []

def test_normal_input_unchanged():
    """Verify normal behavior is preserved."""
    result = process("hello")
    assert result == ["h", "e", "l", "l", "o"]

def test_whitespace_input_returns_empty_list():
    """Verify input with only whitespace is handled gracefully."""
    result = process("   \n\t  ")
    assert result == []