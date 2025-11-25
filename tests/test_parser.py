import pytest # type: ignore
from parser import format_bps

# Constants that will be used
KB = 10**3
MB = 10**6
GB = 10**9
TB = 10**12

# These tests are parameterized by input size, expected output size, and 
# expected unit.
@pytest.mark.parametrize("input_size, expected_value, expected_unit", [
    # Bytes, n=0
    (500, 500, 'bps'),
    (20, 20, 'bps'),
    
    # Kilo Case, n=1
    (KB, 1.0, 'kbps'),
    (1.5 * KB, 1.5, 'kbps'),
    
    # Mega Case, n=2
    (MB, 1.0, 'Mbps'),
    (10 * MB, 10.0, 'Mbps'),
    
    # Giga Case, n=3
    (GB, 1.0, 'Gbps'),
    (2.5 * GB, 2.5, 'Gbps'),
    
    # Tera Case, n=4
    (TB, 1.0, 'Tbps'),
    (5 * TB, 5.0, 'Tbps'),
    
    # Edge Case, 0 bytes
    (0, 0, 'bps'),
    
    # Edge Case: Just under the next threshold
    (KB - 1, 999, 'bps'),
    (MB - 1, (MB - 1) / KB, 'kbps'),
    
    # Edge Case: Large number
    (1024 * TB, 1024.0, 'Tbps'),
    
    #  Edge Case: Float input
    (1.5 * KB + 0.5, 1.5005, 'kbps'),
])
# test that function will return correct numeric value and unit label
def test_format_bytes_correct_conversion_and_label(input_size, expected_value, expected_unit):
    """Tests that the function returns the correct numeric value and unit label."""
    value, unit = format_bps(input_size)
    
    assert unit == expected_unit
    # Approximating floating point comparison to avoid precision errors
    assert value == pytest.approx(expected_value)

# Test for handling out-of-scope large numbers (beyond 'tera')
def test_format_bytes_exceeds_tera():
    """Tests a number larger than the defined 'tera' limit (2**40)."""
    large_size = 1024 * TB * 2
    
    # The function will only iterate n=4 times (for TB) and stop, 
    # returning the value scaled by TB but with the 'terabytes' label.
    value, unit = format_bps(large_size)
    
    assert unit == 'Tbps'
    assert value == 2048.0

# Test for potential error cases (Negative numbers or non-numeric inputs)
def test_format_bytes_invalid_input():
    """Tests behavior with negative numbers or non-numeric types."""

    # The expected result is negative input and 'bytes'. Should never happen
    # in prod code but want to make sure it won't crash the program.
    assert format_bps(-1024) == (-1024, 'bps')
    
    # Non-numeric sizes should raise a TypeError should be raised by the division
    with pytest.raises(TypeError):
        format_bps("1024")