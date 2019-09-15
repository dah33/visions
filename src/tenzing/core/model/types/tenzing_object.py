import pandas.api.types as pdt
import pandas as pd

from tenzing.core.model.types.tenzing_generic import tenzing_generic


class tenzing_object(tenzing_generic):
    """**Object** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series(['a', 1, np.nan])
    >>> x in tenzing_object
    True
    """

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return not series.empty and pdt.is_object_dtype(series) and not series.hasnans

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.astype("object")