import pytest
import asyncio
import re
import tempfile
import shutil
import os
from unittest.mock import MagicMock, patch

# --- Example functions/classes for demonstration ---

def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(pattern, email):
        raise ValueError("Invalid email")
    return True

def factorial(n):
    if n < 0:
        raise ValueError("Negative input not allowed")
    return 1 if n == 0 else n * factorial(n - 1)

async def async_generator(n):
    for i in range(n):
        await asyncio.sleep(0.01)
        yield i

cache = {}
def cache_result(key, value):
    cache[key] = value

def get_cached(key):
    return cache.get(key, None)

def parse_json(data):
    import json
    return json.loads(data)

def download_file(url, dest):
    # dummy simulation
    with open(dest, 'w') as f:
        f.write("file content")

class User:
    def __init__(self, username):
        self.username = username
    def greet(self):
        return f"Hello, {self.username}!"

# --- More test cases ---

# 21. Email validation raises on bad email
def test_validate_email_good_and_bad():
    assert validate_email("test@example.com")
    with pytest.raises(ValueError):
        validate_email("bademail@com")

# 22. Factorial of number and error on negative
def test_factorial():
    assert factorial(5) == 120
    assert factorial(0) == 1
    with pytest.raises(ValueError):
        factorial(-1)

# 23. Async generator yields expected sequence
@pytest.mark.asyncio
async def test_async_generator():
    results = []
    async for i in async_generator(3):
        results.append(i)
    assert results == [0, 1, 2]

# 24. Cache set and get
def test_cache_set_get():
    cache_result("key1", "value1")
    assert get_cached("key1") == "value1"
    assert get_cached("missing") is None

# 25. JSON parsing valid and invalid
def test_parse_json():
    valid = '{"a":1,"b":2}'
    result = parse_json(valid)
    assert result == {"a":1,"b":2}
    with pytest.raises(Exception):
        parse_json("invalid json")

# 26. File download writes content (using tempfile)
def test_download_file():
    tmp_dir = tempfile.mkdtemp()
    dest = os.path.join(tmp_dir, "file.txt")
    download_file("http://fakeurl.com", dest)
    assert os.path.exists(dest)
    with open(dest) as f:
        content = f.read()
    assert content == "file content"
    shutil.rmtree(tmp_dir)

# 27. User greeting includes username
def test_user_greet():
    user = User("Alice")
    assert user.greet() == "Hello, Alice!"

# 28. Testing concurrent async tasks
@pytest.mark.asyncio
async def test_concurrent_tasks():
    async def double(x):
        await asyncio.sleep(0.01)
        return x * 2
    results = await asyncio.gather(double(2), double(3))
    assert results == [4, 6]

# 29. Test exception message contains substring
def test_error_message_contains():
    with pytest.raises(ValueError) as e:
        factorial(-5)
    assert "Negative" in str(e.value)

# 30. Mock a method of a class
def test_mock_method():
    user = User("Bob")
    with patch.object(user, 'greet', return_value="Mocked!"):
        assert user.greet() == "Mocked!"

# 31. Test regex matching a complex pattern
def test_regex_pattern():
    pattern = r"^\d{3}-\d{2}-\d{4}$"  # e.g., SSN format
    assert re.match(pattern, "123-45-6789")
    assert not re.match(pattern, "123456789")

# 32. Test a function raises TypeError on wrong type
def test_type_error():
    with pytest.raises(TypeError):
        factorial("string")

# 33. Test that a list is sorted after function call
def test_sorting():
    lst = [5, 3, 1, 4]
    lst.sort()
    assert lst == [1, 3, 4, 5]

# 34. Test that a dict keys exist
def test_dict_keys():
    d = {"name": "test", "id": 123}
    assert "name" in d and "id" in d

# 35. Test that temporary directory is created and deleted
def test_tmpdir(tmp_path):
    p = tmp_path / "file.txt"
    p.write_text("hello")
    assert p.read_text() == "hello"

# 36. Test function with side effects (modifies list)
def test_side_effect():
    lst = []
    def append_hello(l):
        l.append("hello")
    append_hello(lst)
    assert lst == ["hello"]

# 37. Test that a float division returns float
def test_float_division():
    result = 5 / 2
    assert isinstance(result, float)
    assert result == 2.5

# 38. Test that a function returns None explicitly
def test_returns_none():
    def foo():
        return None
    assert foo() is None

# 39. Test that a mocked external call is called exactly once
@patch("requests.get")
def test_external_call_once(mock_get):
    import requests
    requests.get("http://some.url")
    mock_get.assert_called_once()

# 40. Test generator raises StopIteration correctly
def test_generator_stopiteration():
    def gen():
        yield 1
        yield 2
    g = gen()
    assert next(g) == 1
    assert next(g) == 2
    with pytest.raises(StopIteration):
        next(g)
