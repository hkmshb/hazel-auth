import pytest
from datetime import datetime
from sqlalchemy import exc, orm
from hazel_auth.models import User, Role, UserRole, ActivityToken


class TestBase:
    def _get_user_dict(self):
        return {
            'username': 'user'
        }

    def _get_role_dict(self):
        return {
            'name': 'member'
        }


class TestAuthModels(TestBase):

    def test_can_persist_and_read_user(self, db):
        data_dict = self._get_user_dict()
        db.add(User(**data_dict))
        db.flush()

        found = db.query(User).one()
        assert found and found.uuid
        assert found.username == 'user'
        assert found.is_active is True
        assert found.password is None

    def test_persistence_fails_for_non_unique_username(self, db):
        data_dict = self._get_user_dict()
        db.add(User(**data_dict))
        db.flush()

        with pytest.raises(exc.IntegrityError):
            db.add(User(**data_dict))
            db.flush()

    def test_persistence_fails_for_non_unique_email(self, db):
        data_dict = {'username': 'user', 'email': 'user@elixr.lib'}
        db.add(User(**data_dict))
        db.flush()

        with pytest.raises(exc.IntegrityError):
            data_dict['username'] = 'user2'
            db.add(User(**data_dict))
            db.flush()

    def test_can_persist_and_read_role(self, db):
        data_dict = self._get_role_dict()
        db.add(Role(**data_dict))
        db.flush()

        found = db.query(Role).one()
        assert found and found.uuid
        assert found.name == 'member'
        assert found.description is None

    def test_can_persist_user_with_roles(self, db):
        user_dict = self._get_user_dict()
        role_dict = self._get_role_dict()

        user = User(**user_dict)
        user.roles.append(Role(**role_dict))
        user.roles.append(Role(name='editor'))

        db.add(user)
        db.flush()

        assert db.query(User).count() == 1
        assert db.query(Role).count() == 2

    def test_can_persist_role_with_users(self, db):
        user_dict = self._get_user_dict()
        role_dict = self._get_role_dict()

        role = Role(**role_dict)
        role.users.append(User(**user_dict))
        role.users.append(User(username='user2'))

        db.add(role)
        db.commit()

        assert db.query(User).count() == 2
        assert db.query(Role).count() == 1

    def test_rel_between_user_and_role(self, db):
        user_dict = self._get_user_dict()
        role_dict = self._get_role_dict()

        user = User(**user_dict)
        user.roles.append(Role(**role_dict))

        db.add(user)
        db.commit()

        assert db.query(User).count() == 1
        assert db.query(Role).count() == 1
        assert db.query(UserRole).count() == 1

        urole = db.query(UserRole).one()
        urole.user_id == user.uuid
        urole.role_id == user.roles[0].uuid

    def test_can_persist_and_read_activation(self, db):
        activity_token = ActivityToken(expires_at=datetime.now())
        db.add(activity_token)
        db.flush()

        assert activity_token and activity_token.uuid
        assert activity_token.token is not None
