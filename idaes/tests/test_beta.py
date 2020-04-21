# coding: utf-8
##############################################################################
# Institute for the Design of Advanced Energy Systems Process Systems
# Engineering Framework (IDAES PSE Framework) Copyright (c) 2018-2019, by the
# software owners: The Regents of the University of California, through
# Lawrence Berkeley National Laboratory,  National Technology & Engineering
# Solutions of Sandia, LLC, Carnegie Mellon University, West Virginia
# University Research Corporation, et al. All rights reserved.
#
# Please see the files COPYRIGHT.txt and LICENSE.txt for full copyright and
# license information, respectively. Both files are also available online
# at the URL "https://github.com/IDAES/idaes-pse".
##############################################################################

import logging
import pytest
import sys

from io import StringIO
from pyomo.common.log import LoggingIntercept
from idaes.beta import import_beta

def test_beta_module_exception():
    with pytest.raises(
            ImportError, match=r"Module 'idaes.tests.beta_mod' is in beta "
            "and must be imported using idaes.beta.import_beta\(\)."):
        import idaes.tests.beta_mod

def test_beta_module_import():
    os = StringIO()
    with LoggingIntercept(os, 'idaes', logging.INFO):
        mod = import_beta('idaes.tests.beta_mod')
    assert mod.__name__ == 'idaes.tests.beta_mod'
    assert mod.reference_value == 42
    assert os.getvalue() == ""

    os = StringIO()
    with LoggingIntercept(os, 'idaes', logging.INFO):
        mod = import_beta('.beta_mod')
    assert mod.__name__ == 'idaes.tests.beta_mod'
    assert mod.reference_value == 42
    assert os.getvalue() == ""

    os = StringIO()
    with LoggingIntercept(os, 'idaes.logger', logging.INFO):
        mod = import_beta('idaes.logger')
    assert mod.__name__ == 'idaes.logger'
    assert os.getvalue().strip() == "Module 'idaes.tests.test_beta' "\
        "imported module 'idaes.logger' as a Beta module.  "\
        "This module is not declared beta and can be "\
        "imported using Python's normal import mechanisms."

def test_beta_reimport():
    os = StringIO()
    with LoggingIntercept(os, 'idaes', logging.INFO):
        mod = import_beta('idaes.tests.beta_mod')
    assert mod.__name__ == 'idaes.tests.beta_mod'
    assert mod.reference_value == 42
    assert os.getvalue() == ""

    # Test that subsequent standard imports will still trigger an
    # exception, even if the module was previously imported using
    # import-beta()
    with pytest.raises(
            ImportError, match=r"Module 'idaes.tests.beta_mod' is in beta "
            "and must be imported using idaes.beta.import_beta\(\)."):
        import idaes.tests.beta_mod

    # But subsequent beta_import() modules return the same (original)
    # module object
    os = StringIO()
    with LoggingIntercept(os, 'idaes', logging.INFO):
        mod2 = import_beta('idaes.tests.beta_mod')
    assert mod2 is mod