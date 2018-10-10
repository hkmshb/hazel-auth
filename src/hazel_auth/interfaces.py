from zope.interface import Attribute, Interface


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
