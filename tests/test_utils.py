import pytest
import string
from hazel_auth import utils



@pytest.mark.parametrize('length,letters,pool', [
    (32, None, utils._default),
    (32, utils._default, utils._default),
    (40, string.digits, string.digits) ])
def test_generate_random_strings(length, letters, pool):
    func = utils.generate_random_string
    params = {'length': length}
    if letters:
        params['letters'] = letters
    result = func(**params)
    assert len(result) == length
    assert len([c for c in result if c in pool]) == length
