import pandas.api.types as pdt
import numpy as np

from tenzing.core import tenzing_model
from tenzing.core.mixins import optionMixin, uniqueSummaryMixin
from tenzing.core.model_implementations.types.tenzing_integer import tenzing_integer
from tenzing.utils import singleton


@singleton.singleton_object
class tenzing_float(optionMixin, uniqueSummaryMixin, tenzing_model):
    """**Float** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([1.0, 2.5, 5.0, np.nan])
    >>> x in tenzing_float
    True
    """
    def contains_op(self, series):
        if not pdt.is_float_dtype(series):
            return False
        # TODO: are we sure we want this to depend on integer?
        elif series in tenzing_integer:
            return False
        else:
            return True

    def cast_op(self, series):
        return series.astype(float)

    def summarization_op(self, series):
        aggregates = ['mean', 'std', 'var', 'max', 'min', 'median', 'kurt', 'skew', 'sum', 'mad']
        summary = series.agg(aggregates).to_dict()

        quantiles = [0.05, 0.25, 0.5, 0.75, 0.95]
        for percentile, value in series.quantile(quantiles).to_dict().items():
            summary["quantile_{:d}".format(int(percentile * 100))] = value

        summary["range"] = summary["max"] - summary["min"]
        summary["iqr"] = summary["quantile_75"] - summary["quantile_25"]
        summary["cv"] = summary["std"] / summary["mean"] if summary["mean"] else np.NaN

        # TODO: move to common
        summary['n_records'] = series.shape[0]
        summary['memory_size'] = series.memory_usage(index=True, deep=True),

        # TODO: could be a mixin
        summary['n_zeros'] = (series == 0).sum()
        summary['perc_zeros'] = summary['n_zeros'] / summary['n_records']

        # TODO: only calculations for histogram, not the plotting
        # summary['image'] = plotting.histogram(series)
        return summary