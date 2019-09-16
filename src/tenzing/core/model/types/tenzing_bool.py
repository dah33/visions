import pandas.api.types as pdt
import pandas as pd

from tenzing.core.model.types.tenzing_generic import tenzing_generic


class tenzing_bool(tenzing_generic):
    """**Boolean** implementation of :class:`tenzing.core.models.tenzing_model`.

    Examples:
        >>> import numpy as np
        >>> x = pd.Series([True, False, np.nan])
        >>> x in tenzing_bool
        True
    """

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        if pdt.is_categorical_dtype(series):
            return False

        return not series.empty and (
            pdt.is_bool_dtype(series) or series.apply(lambda x: type(x) == bool).all()
        )

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.astype(bool)
