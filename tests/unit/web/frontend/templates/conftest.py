#!/usr/bin/env python3
"""
Test configuration for the frontend templates, including shared fixtures.

Module Attributes:
  N/A

(C) Copyright 2021 Jonathan Casey.  All Rights Reserved Worldwide.
"""
import os
import os.path

import pytest

from grand_trade_auto.general import dirs

from . import utils as tt_utils



@pytest.fixture(name='sanitized_templates', scope='session',
        autouse=True)
def fixture_sanitized_templates(request):
    """
    This will generate sanitized jinja2 templates for all templates.

    This is intended to be used for all jinja2 template unit tests.  Fastapi and
    other unit tests will use the original jinja2 templates; this is only needed
    for testing jinja2 templates directly since some elements may not be
    compatibile with rendering in the jinja2 engine.

    Modified tmp files will be created at the start of testing, and deleted at
    the end.

    Returns:
      sanitized_filepaths ({str: str}): Dict that translates original filenames
        into full filepath for sanitized version.
    """
    sanitized_filenames = {}

    def delete_tmp_files():
        """
        Deletes all temporary template files generated by this fixture.
        """
        for sfn in sanitized_filenames.values():
            filepath = os.path.join(
                    tt_utils.get_sanitized_jinja2_templates_test_path(), sfn)
            os.remove(filepath)

    request.addfinalizer(delete_tmp_files)

    for filename in os.listdir(dirs.get_jinja2_templates_path()):
        if filename.endswith('.jinja2'):
            sanitized_filenames[filename] = tt_utils.sanitize_non_jinja2(
                    filename)
            tt_utils.sub_sanitized_jinja2_extends(filename)

    return sanitized_filenames