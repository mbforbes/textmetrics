"""
This file exists so that tests can import the textmetrics package correctly and
test its contents.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import textmetrics
