from __future__ import annotations

from sqlalchemy import create_engine

try:
    from build_dataset import get_mysql_url
except ImportError:
    from ml.build_dataset import get_mysql_url


def get_mysql_engine():
    return create_engine(get_mysql_url())
