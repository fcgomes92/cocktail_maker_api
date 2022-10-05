import os
import tempfile

import pytest
from cocktail_maker import create_app


@pytest.fixture
def app():
    # db_fd, db_path = tempfile.mkstemp()

    app = create_app()

    # with app.app_context():
    #     init_db()
    #     get_db().executescript(_data_sql)

    yield app

    # os.close(db_fd)
    # os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
