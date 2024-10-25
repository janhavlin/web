import contextlib
import logging
import os
import time
from pathlib import Path

import pytest
import tmt

from tmt_web.utils import git_handler


class TestGitHandler:
    logger = tmt.Logger(logging.getLogger("tmt-logger"))

    def test_clear_tmp_dir(self):
        # Create test directory if it doesn't exist
        try:
            path = Path(__file__).resolve().parents[2].joinpath(os.getenv("CLONE_DIR_PATH", "./.repos/"))
            path.mkdir(exist_ok=True)
        except FileExistsError:
            pass
        git_handler.clear_tmp_dir(self.logger)

    def test_get_path_to_repository(self):
        self.test_clone_repository()
        assert git_handler.get_path_to_repository("https://github.com/teemtee/tmt").exists()

    def test_check_if_repository_exists(self):
        self.test_clone_repository()
        assert git_handler.check_if_repository_exists("https://github.com/teemtee/tmt")

    def test_clone_repository(self):
        # Give the script enough time for the repository to be deleted
        while git_handler.check_if_repository_exists("https://github.com/teemtee/tmt") is True:
            git_handler.clear_tmp_dir(self.logger)
            time.sleep(1)
        git_handler.clone_repository(url="https://github.com/teemtee/tmt",
                                     logger=self.logger)

    def test_clone_repository_even_if_exists(self):
        with contextlib.suppress(FileExistsError):
            git_handler.clone_repository(url="https://github.com/teemtee/tmt",
                                         logger=self.logger)

    def test_clone_checkout_branch(self):
        with contextlib.suppress(FileExistsError):
            git_handler.clone_repository(url="https://github.com/teemtee/tmt",
                                         logger=self.logger, ref="quay")

    def test_clone_checkout_branch_exception(self):
        with pytest.raises(AttributeError):
            git_handler.clone_repository(url="https://github.com/teemtee/tmt",
                                         logger=self.logger, ref="quadd")

    def test_checkout_branch(self):
        self.test_clone_repository_even_if_exists()
        git_handler.checkout_branch(ref="quay", path=git_handler.get_path_to_repository(
            url="https://github.com/teemtee/tmt"), logger=self.logger)
        git_handler.checkout_branch(ref="main", path=git_handler.get_path_to_repository(
            url="https://github.com/teemtee/tmt"), logger=self.logger)

    def test_checkout_branch_exception(self):
        self.test_clone_repository_even_if_exists()
        with pytest.raises(AttributeError):
            git_handler.checkout_branch(ref="quaddy", path=git_handler.get_path_to_repository(
                url="https://github.com/teemtee/tmt"), logger=self.logger)
