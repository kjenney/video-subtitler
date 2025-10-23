#!/usr/bin/env python3
"""
Example test file showing how to write additional tests

This file demonstrates various testing patterns and can be used
as a template for adding new tests to the project.
"""

import pytest
import sys
from pathlib import Path
import tempfile

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import video_subtitler


class TestExampleUnitTests:
    """
    Example unit tests for isolated function testing
    Unit tests should be fast and not depend on external resources
    """

    def test_timestamp_boundary_cases(self):
        """Test edge cases for timestamp formatting"""
        # Test multiple hours
        result = video_subtitler.format_timestamp(7384.999)
        assert result.startswith("02:03:04")

        # Test fractional seconds
        result = video_subtitler.format_timestamp(1.5)
        assert "00:00:01,500" == result

    def test_timestamp_precision(self):
        """Test timestamp millisecond precision"""
        test_cases = [
            (0.001, "00:00:00,001"),
            (0.999, "00:00:00,999"),
            (60.001, "00:01:00,001"),
        ]

        for seconds, expected in test_cases:
            result = video_subtitler.format_timestamp(seconds)
            assert result == expected, f"Failed for {seconds}s"


class TestExampleIntegrationTests:
    """
    Example integration tests that use real files and fixtures
    """

    @pytest.fixture
    def temp_output_file(self):
        """Fixture providing a temporary output file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False) as f:
            temp_path = f.name

        yield temp_path

        # Cleanup after test
        if Path(temp_path).exists():
            Path(temp_path).unlink()

    def test_srt_file_structure(self, temp_output_file):
        """Test that generated SRT files have correct structure"""
        segments = [
            {'start': 0.0, 'end': 2.0, 'text': ' First line'},
            {'start': 2.0, 'end': 4.0, 'text': ' Second line'},
        ]

        video_subtitler.generate_srt(segments, temp_output_file)

        # Read and verify structure
        with open(temp_output_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for required SRT components
        assert "1\n" in content  # Sequence number
        assert "-->" in content  # Time separator
        assert "First line" in content
        assert "Second line" in content

        # Verify blank line between subtitles
        lines = content.split('\n')
        subtitle_blocks = content.strip().split('\n\n')
        assert len(subtitle_blocks) == 2, "Should have 2 subtitle blocks"


class TestExampleParametrizedTests:
    """
    Example of parametrized tests - run same test with different inputs
    """

    @pytest.mark.parametrize("seconds,expected", [
        (0, "00:00:00,000"),
        (1, "00:00:01,000"),
        (60, "00:01:00,000"),
        (3600, "01:00:00,000"),
        (3661, "01:01:01,000"),
    ])
    def test_timestamp_formatting_parametrized(self, seconds, expected):
        """Test multiple timestamp values efficiently"""
        result = video_subtitler.format_timestamp(seconds)
        assert result == expected


class TestExampleFixtures:
    """
    Examples of different fixture patterns
    """

    @pytest.fixture(scope="function")
    def function_scoped_data(self):
        """Created fresh for each test function"""
        print("\nSetup function fixture")
        data = {"test": "data"}
        yield data
        print("Teardown function fixture")

    @pytest.fixture(scope="class")
    def class_scoped_data(self):
        """Created once for the entire test class"""
        print("\nSetup class fixture")
        data = {"shared": "data"}
        yield data
        print("Teardown class fixture")

    def test_using_function_fixture(self, function_scoped_data):
        """Test using function-scoped fixture"""
        assert function_scoped_data["test"] == "data"

    def test_using_class_fixture(self, class_scoped_data):
        """Test using class-scoped fixture"""
        assert class_scoped_data["shared"] == "data"


class TestExampleMarkers:
    """
    Examples of using pytest markers
    """

    @pytest.mark.slow
    def test_slow_operation(self):
        """
        Mark tests that take a long time
        Skip with: pytest -m "not slow"
        """
        import time
        time.sleep(0.1)  # Simulate slow operation
        assert True

    @pytest.mark.skip(reason="Demonstrating skip marker")
    def test_skipped(self):
        """This test will always be skipped"""
        assert False  # Would fail if run

    @pytest.mark.skipif(sys.platform == "win32", reason="Unix only test")
    def test_unix_specific(self):
        """Skip on specific platforms"""
        assert True

    @pytest.mark.xfail(reason="Known issue, working on fix")
    def test_expected_failure(self):
        """Mark test as expected to fail"""
        assert False  # Expected to fail


class TestExampleExceptions:
    """
    Examples of testing error conditions
    """

    def test_exception_raised(self):
        """Test that a function raises an exception"""
        with pytest.raises(ValueError):
            # This should raise ValueError
            int("not a number")

    def test_exception_message(self):
        """Test exception message content"""
        with pytest.raises(ValueError, match="invalid literal"):
            int("not a number")

    def test_no_exception_when_valid(self):
        """Test that no exception is raised with valid input"""
        try:
            result = video_subtitler.format_timestamp(100)
            assert isinstance(result, str)
        except Exception as e:
            pytest.fail(f"Unexpected exception: {e}")


class TestExampleTempFiles:
    """
    Examples of working with temporary files in tests
    """

    def test_with_temp_directory(self):
        """Test using a temporary directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.txt"
            test_file.write_text("test content")

            assert test_file.exists()
            assert test_file.read_text() == "test content"
        # Directory automatically cleaned up

    def test_with_temp_file(self):
        """Test using a temporary file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.srt') as tmp:
            tmp.write("test content")
            tmp.flush()

            assert Path(tmp.name).exists()
        # File automatically cleaned up


# Example: Running specific tests
if __name__ == "__main__":
    # Run all tests in this file
    pytest.main([__file__, "-v"])

    # Run with coverage
    # pytest.main([__file__, "--cov=video_subtitler", "-v"])

    # Run only specific marker
    # pytest.main([__file__, "-m", "slow", "-v"])
