# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""Tests for the config-isolation helpers in ``tests/conftest.py``."""

from typing import Callable

import pytest
from flask import current_app

from tests.conftest import config_overrides, with_config

_KEY = "TEST_ISOLATION_EXISTING_KEY"
_NEW_KEY = "TEST_ISOLATION_MISSING_KEY"


def test_config_overrides_restores_existing_key(app_context: None) -> None:
    current_app.config[_KEY] = "before"
    try:
        with config_overrides({_KEY: "during"}):
            assert current_app.config[_KEY] == "during"
        assert current_app.config[_KEY] == "before"
    finally:
        current_app.config.pop(_KEY, None)


def test_config_overrides_removes_key_that_did_not_exist(
    app_context: None,
) -> None:
    current_app.config.pop(_NEW_KEY, None)
    with config_overrides({_NEW_KEY: 1}):
        assert current_app.config[_NEW_KEY] == 1
    assert _NEW_KEY not in current_app.config


def test_config_overrides_restores_on_exception(app_context: None) -> None:
    current_app.config[_KEY] = "before"
    try:
        with pytest.raises(RuntimeError), config_overrides({_KEY: "during"}):
            raise RuntimeError("boom")
        assert current_app.config[_KEY] == "before"
    finally:
        current_app.config.pop(_KEY, None)


def test_with_config_restores_on_exception(app_context: None) -> None:
    current_app.config[_KEY] = "before"

    @with_config({_KEY: "during"})
    def failing() -> None:
        assert current_app.config[_KEY] == "during"
        raise RuntimeError("boom")

    try:
        with pytest.raises(RuntimeError):
            failing()
        assert current_app.config[_KEY] == "before"
    finally:
        current_app.config.pop(_KEY, None)


def test_with_config_is_reentrant_across_calls(app_context: None) -> None:
    current_app.config[_KEY] = "before"

    @with_config({_KEY: "during"})
    def wrapped() -> str:
        return current_app.config[_KEY]

    try:
        assert wrapped() == "during"
        assert current_app.config[_KEY] == "before"
        assert wrapped() == "during"
        assert current_app.config[_KEY] == "before"
    finally:
        current_app.config.pop(_KEY, None)


def test_override_config_fixture_applies(
    app_context: None, override_config: Callable[..., None]
) -> None:
    override_config(**{_NEW_KEY: "fixture-value"})
    assert current_app.config[_NEW_KEY] == "fixture-value"


def test_override_config_fixture_was_undone(app_context: None) -> None:
    assert _NEW_KEY not in current_app.config
