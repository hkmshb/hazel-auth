"""Defines the default model fields for the authentication system.

The default fields a user implementation can have. You can subclass these
mixins and then provide a custom implementation for concrete models.
"""
from datetime import datetime
from sqlalchemy import Column, Boolean, DateTime, String, Unicode
from hazel_db.mixins import EntityMixin
from .utils import generate_random_string



class UserMixin(EntityMixin):
    """This mixin provides the default required fields for a user model.
    """
    username = Column(Unicode(50), nullable=False, unique=True)
    first_name = Column(Unicode(50))
    last_name = Column(Unicode(50), nullable=True)
    email = Column(String(100), nullable=True, unique=True)
    password = Column(Unicode(255), nullable=True)

    # when user got activated via email confirmation
    activated_at = Column(DateTime, nullable=True)

    # indicates if user account is active
    is_active = Column(
        Boolean(create_constraint=False),
        nullable=False, default=True
    )

    # indicates if user is the SysAdmin
    is_sysadmin = Column(
        Boolean(create_constraint=False),
        nullable=False, default=False
    )

    # first login the user manages to make to the system
    first_login = Column(DateTime, nullable=True)

    # when user last accessed the system
    last_login_at = Column(DateTime, nullable=True)

    # the IP address from which user last logged in
    last_login_ip = Column(String(20), nullable=True)

    @property
    def fullname(self):
        name = self.first_name or ''
        if self.last_name:
            name += (' ' if name else '')
            name += self.last_name
        return name

    @property
    def friendly_name(self):
        name = self.fullname or self.username
        return name

    def __str__(self):
        """Returns a string representation for the model.
        """
        return self.friendly_name

    def __repr__(self):
        """Returns the string representation of the model.
        """
        return "<{} {} />".format(
            self.__class__.__name__,
            self.friendly_name
        )


class RoleMixin(EntityMixin):
    """This mixin provides the default required fields for role based
    authorization.
    """
    name = Column(Unicode(50), nullable=False, unique=True)
    description = Column(Unicode(255))


class ActivityTokenMixin(EntityMixin):
    """This mixin provides the fields which store data necessary to manage
    secret codes that confirm a user need to proceed with a sensitive task
    before the task is initiated or concluded. Tasks like password recovery,
    sign-up activation etc.
    """
    expires_at = Column(DateTime, nullable=False)
    token = Column(
        Unicode(32), nullable=False, unique=True,
        default=lambda: generate_random_string(32)
    )

    def is_expired(self):
        """Determines if the task token is usable and is yet to expire.
        """
        return self.expires_at < datetime.now()
