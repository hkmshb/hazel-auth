"""Default auth models implementations.
"""
from zope.interface import implementer
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative.base import _declarative_constructor
from hazel_db import types, mixins

from .interfaces import IUser, IRole
from .mixins import UserMixin, RoleMixin, ActivityTokenMixin



@implementer(IUser)
class User(UserMixin):
    """The default user implementation.
    """
    __tablename__ = 'auth_users'
    __init__ = _declarative_constructor
    activity_token = relationship('ActivityToken', backref='user')
    activity_token_id = Column(
        types.UUID,
        ForeignKey('auth_activity_tokens.uuid')
    )
    roles = relationship(
        'Role', secondary='auth_userroles',
        lazy='joined', back_populates='users',
        passive_deletes=True, passive_updates=True
    )


@implementer(IRole)
class Role(RoleMixin):
    """The default role implementation.
    """
    __tablename__ = 'auth_roles'
    __init__ = _declarative_constructor
    users = relationship(
        'User', secondary='auth_userroles',
        lazy='joined', back_populates='roles',
        passive_deletes=True, passive_updates=True
    )


class UserRole(mixins.EntityMixin):
    """Many-to-Many mapping for users to roles.
    """
    __tablename__ = 'auth_userroles'
    __init__ = _declarative_constructor
    user_id = Column(types.UUID, ForeignKey('auth_users.uuid'))
    role_id = Column(types.UUID, ForeignKey('auth_roles.uuid'))


class ActivityToken(ActivityTokenMixin):
    """The default implementation for user associated tokens for sensitive
    activities that need some sort of user verification before commencing.
    """
    __tablename__ = 'auth_activity_tokens'
    __init__ = _declarative_constructor
