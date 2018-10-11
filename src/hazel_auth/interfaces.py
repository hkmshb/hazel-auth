from zope.interface import Attribute, Interface


class IPasswordHasher(Interface):
    """A utility for hashing passwords.
    """

    def hash_password(plain_text):
        """Generate a hash presentation for the provided plain text password.
        """
        pass

    def verify_password(plain_text, hashed_password):
        """Verify a password. Hashes provided plain_text and compares it to
        the persisted hash.
        """
        pass


class IUser(Interface):
    """Defines the default fields required of a user model.
    """
    friendly_name = Attribute('friendly_name')
    fullname = Attribute('fullname')
    username = Attribute('username')
    email = Attribute('email')


class IRole(Interface):
    """Defines the default fields required of a role model.
    """
    name = Attribute('name')
    description = Attribute('description')


class IActivityToken(Interface):
    """Defines the default fields required of an activity token.
    """
    token = Attribute('token')
    expires_at = Attribute('expires_at')
