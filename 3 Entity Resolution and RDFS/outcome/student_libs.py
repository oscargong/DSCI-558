# You can define your additional imports here if needed
import re
from strsimpy.metric_lcs import MetricLCS


def metric_lcs(a,b):
    return MetricLCS().distance(a,b)
