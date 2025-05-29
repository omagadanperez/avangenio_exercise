from server.server import calculate_weight


# Test cases for calculate_weight function
def test_calculate_weight_with_double_a():
    """Test case where the string contains 'aa'."""
    text = "This is a test with aa."
    result = calculate_weight(text)
    assert result == 1000, f"Expected 1000 but got {result}"


def test_calculate_weight_with_mixed_characters():
    """Test case where the string contains letters, digits, and spaces."""
    text = "123 abc 45"
    result = calculate_weight(text)
    expected_weight = (1.5 * 3 + 2 * 3) / 2  # 3 letters, 3 digits, 2 spaces
    assert result == expected_weight, f"Expected {expected_weight} but got {result}"


def test_calculate_weight_with_no_spaces():
    """Test case where there are no spaces in the string."""
    text = "abc123"
    result = calculate_weight(text)
    expected_weight = 0  # No spaces should result in weight 0
    assert result == expected_weight, f"Expected {expected_weight} but got {result}"


def test_calculate_weight_with_only_spaces():
    """Test case where the string contains only spaces."""
    text = "     "
    result = calculate_weight(text)
    assert result == 0, f"Expected 0 but got {result}"
