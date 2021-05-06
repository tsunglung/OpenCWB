#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import constants
from .utils.strings import version_tuple_to_str

__title__ = 'ocwb'
__description__ = 'A Python wrapper around OpenCWB web APIs'
__url__ = 'https://github.com/tsunglung/OpenCWB'
__version__ = version_tuple_to_str(constants.OCWB_VERSION)
__author__ = 'Tsunglung Yang'
__author_email__ = 'zonglong@gmail.com'
__license__ = 'MIT'
