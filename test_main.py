from downloader import get_images


def test_happy_paths():
    path = "test_data/correct_paths.txt"
    target_path = "test_target"
    faulty = get_images(path, target_path)
    assert not faulty


def test_non_images_paths():
    path = "test_data/correct_paths_with_non_images.txt"
    target_path = "test_target"
    faulty = get_images(path, target_path)
    assert not faulty


def test_broken_paths():
    path = "test_data/broken_paths.txt"
    target_path = "test_target"
    faulty = get_images(path, target_path)
    assert faulty