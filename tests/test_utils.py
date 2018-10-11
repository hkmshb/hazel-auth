import pytest
import string
from hazel_auth import crypt, utils



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


class TestArgon2Hasher:

    def test_password_hashing(self):
        hasher = crypt.Argon2Hasher()
        plain_pwd = 'hazel_auth'
        hashed_pwd = hasher.hash_password(plain_pwd)
        assert plain_pwd != hashed_pwd

    def test_password_verification(self):
        hasher = crypt.Argon2Hasher()
        plain_pwd = 'hazel_auth'
        hashed_pwd = hasher.hash_password(plain_pwd)
        assert hasher.verify_password(plain_pwd, hashed_pwd) is True

    def test_verifing_tampered_hash(self):
        hasher = crypt.Argon2Hasher()
        plain_pwd = 'hazel_auth'
        hashed_pwd = hasher.hash_password(plain_pwd)
        hashed_pwd += '+tampered'
        assert hasher.verify_password(plain_pwd, hashed_pwd) is False
