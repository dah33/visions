import logging

logger = logging.getLogger(__name__)


try:
    import pandas as pd

    import visions.backends.pandas_
    from visions.backends.pandas_.test_utils import pandas_version

    if pandas_version[0] < 1:
        from visions.dtypes.boolean import BoolDtype
    logger.debug(f"Pandas backend loaded {pd.__version__}")

except ImportError:
    logger.debug("Pandas backend NOT loaded")


try:
    import numpy as np

    import visions.backends.numpy_

    logger.debug(f"Numpy backend loaded {np.__version__}")
except ImportError:
    logger.debug("Numpy backend NOT loaded")


try:
    import visions.backends.python_

    logger.debug("Python backend loaded")
except ImportError:
    logger.debug("Python backend NOT loaded")
