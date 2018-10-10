import pytest
from hazel_db import meta



@pytest.fixture(scope='function')
def db():
    from hazel_auth import configure_models
    configure_models()

    # setup
    engine = meta.get_engine({'sqla.url': 'sqlite:///:memory:'}, prefix='sqla.')
    meta.metadata.create_all(engine)

    session_factory = meta.create_session_factory(engine)
    session = meta.create_session(session_factory)
    yield session

    # tear down
    session.close()
