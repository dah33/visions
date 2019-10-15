from pathlib import Path, PureWindowsPath, PurePosixPath, PurePath

import pandas as pd

from visions.core.model.model_relation import relation_conf
from visions.core.model.models import VisionsBaseType


def string_is_path(series):
    try:
        s = to_path(series.copy())
        return s.apply(lambda x: x.is_absolute()).all()
    except TypeError:
        return False


def to_path(series: pd.Series) -> pd.Series:
    s = series.copy().apply(PureWindowsPath)
    if not s.apply(lambda x: x.is_absolute()).all():
        return series.apply(PurePosixPath)
    else:
        return s


class visions_path(VisionsBaseType):
    """**Path** implementation of :class:`visions.core.models.VisionsBaseType`.
    >>> x = pd.Series([Path('/home/user/file.txt'), Path('/home/user/test2.txt')])
    >>> x in visions_path
    True
    """

    @classmethod
    def get_relations(cls):
        from visions.core.model.types import visions_object, visions_string

        relations = {
            visions_object: relation_conf(inferential=False),
            visions_string: relation_conf(
                inferential=True, relationship=string_is_path, transformer=to_path
            ),
        }
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return all(isinstance(x, PurePath) and x.is_absolute() for x in series)