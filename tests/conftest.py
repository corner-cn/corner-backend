import pytest
from extensions import db


@pytest.yield_fixture(scope='function')
def app_corner():
    from corner import create_app
    _app = create_app()
    _app.config['TESTING'] = True
    from corner import register_db
    register_db(_app)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.yield_fixture(scope='function')
def db_corner(app_corner):
    db.app = app_corner
    with app_corner.app_context():
        db.create_all('__all__', app_corner)


    yield db

    db.session.remove()
    db.drop_all()
