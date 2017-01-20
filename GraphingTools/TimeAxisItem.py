from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super(TimeAxisItem, self).__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        # PySide's QTime() initialiser fails miserably and dismisses args/kwargs
        return [QtCore.QTime().addMSecs(value).toString('mm:ss') for value in values]

    def tickSpacing(self, minVal, maxVal, size):
        """Return values describing the desired spacing and offset of ticks.

        This method is called whenever the axis needs to be redrawn and is a
        good method to override in subclasses that require control over tick locations.

        The return value must be a list of three tuples:
            [
                (major tick spacing, offset),
                (minor tick spacing, offset),
                (sub-minor tick spacing, offset),
                ...
            ]
        """
        dif = abs(maxVal - minVal)
        if dif == 0:
            return []

        ## decide optimal minor tick spacing in pixels (this is just aesthetics)
        pixelSpacing = np.log(size + 100) * 1.5
        optimalTickCount = size / pixelSpacing
        if optimalTickCount < 1:
            optimalTickCount = 1

        ## optimal minor tick spacing
        optimalSpacing = dif / optimalTickCount

        ## the largest power-of-10 spacing which is smaller than optimal
        p10unit = 10 ** np.floor(np.log10(optimalSpacing))

        ## Determine major/minor tick spacings which flank the optimal spacing.
        intervals = np.array([1., 2., 10., 20., 100.]) * p10unit
        minorIndex = 0
        while intervals[minorIndex + 1] <= optimalSpacing:
            minorIndex += 1

        return [
            (intervals[minorIndex + 2], 0),
            (intervals[minorIndex + 1], 0),
            (intervals[minorIndex], 0)
        ]

