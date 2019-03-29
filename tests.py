import os
import subprocess

import pytest

from downloader import get_images

data = "test_data"
target = "test_target"


def test_happy_paths():
    path = f"{data}/correct_paths.txt"
    target_path = target
    faulty = get_images(path, target_path)
    assert not faulty


def test_non_images_paths():
    path = f"{data}/correct_paths_with_non_images.txt"
    target_path = target
    faulty = get_images(path, target_path)
    assert not faulty


def test_broken_paths():
    path = f"{data}/broken_paths.txt"
    target_path = target
    faulty = get_images(path, target_path)
    assert faulty


def test_broken_file_permissions():
    """Testing this is not simple since git doesn't sync file permissions. So we need to create the file the first time
    after removing it (if it was checked in by accident).

    Test included to document expected behaviour.
    """
    file_path = os.path.join(data, "temp_file.txt")
    dir_path = target
    try:
        os.remove(file_path)  # Remove if present
    except FileNotFoundError:
        pass

    with open(file_path, "w") as out_file:
        out_file.write("Some content.")
    os.chmod(file_path, mode=0o111)  # Execute-only
    with pytest.raises(PermissionError):
        get_images(file_path, dir_path)


def test_broken_dir_permissions():
    """Testing this is not simple since git doesn't sync dir permissions. So we need to create the dir the first time
    after removing it (if it was checked in by accident).

    Test included to document expected behaviour.
    """
    file_path = os.path.join(data, "correct_paths.txt")
    dir_path = os.path.join(target, "temp_dir")
    try:
        os.rmdir(dir_path)  # Remove if present
    except FileNotFoundError:
        pass

    os.mkdir(dir_path, mode=0o111)  # Execute-only
    with pytest.raises(PermissionError):
        get_images(file_path, dir_path)


def test_cmd_line_execution():
    subprocess.run(["python3", "--version"])
    completed = subprocess.run(["python3",
                                "downloader.py",
                                "-f=test_data/correct_paths.txt",
                                "-d=test_target"])
    assert completed.returncode == 0