from client.client import generate_random_string


# Test to ensure the string length is between 50 and 100
def test_generate_random_string_length():
    result = generate_random_string()
    assert 50 <= len(result) <= 100, f"Length of string is {len(result)} which is out of range (50-100)"


# Test to ensure the string contains between 3 and 5 spaces
def test_generate_random_string_spaces():
    result = generate_random_string()
    space_count = result.count(' ')
    assert 3 <= space_count <= 5, f"Number of spaces is {space_count} which is out of range (3-5)"


# Test to ensure that spaces are not at the beginning or end of the string
def test_generate_random_string_spaces_not_at_ends():
    result = generate_random_string()
    assert not result.startswith(' '), "String starts with a space"
    assert not result.endswith(' '), "String ends with a space"


# Test to ensure that there are no consecutive spaces in the string
def test_generate_random_string_no_consecutive_spaces():
    result = generate_random_string()
    assert '  ' not in result, "String contains consecutive spaces"
