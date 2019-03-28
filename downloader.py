"""This little module can be run on its own ("python downloader.py -f <input_file>") or integrated into another code
base (see example).

Task Description:
    Given a plaintext file containing URLs, one per line, e.g.::

        http://mywebserver.com/images/271947.jpg
        http://mywebserver.com/images/24174.jpg
        http://somewebsrv.com/img/992147.jpg

    Write a script that takes this plaintext file as an argument and downloads all images, storing them on the local
    hard disk.


Example:
    for using this module in a larger code base::

        import from downloader import get_images
        input_path = "/some/path"
        output_path = "/some/other/path"
        get_images(input_path, output_path)

"""
import requests
from requests import Response
from os.path import join, exists
from warnings import warn
from urllib.parse import urlparse


def get_images(input_file_path, output_path):
    """Interprets each line in the specified input file is a valid URL to an image file, downloads all image files, and
    writes them to the specified output path. URLs that don't link to image files are ignored with a warning.

    Args:
        input_file_path (str): The path to the input file.
        output_path (str): The path to the output directory.

    Returns:
        A list with (url, error_code) representing the URLs for which errors were encountered.
    """
    if not exists(input_file_path):
        raise FileNotFoundError(input_file_path)
    if not exists(output_path):
        raise NotADirectoryError(output_path)

    faulty_lines = []
    with open(input_file_path) as infile:
        for line in infile:
            url = line.strip()
            try:
                response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            except Exception as e:
                warn(f"Exception occured when trying to connect.\n"
                     f"URL: {url}.\n"
                     f"EXCEPTION: {e}")
            else:
                success = url_to_image_file(output_path, response, url)
                if not success:
                    faulty_lines.append((url, response.status_code))
    return faulty_lines


def url_to_image_file(output_path, response, url):
    if not response.status_code == 200:
        return False
    elif response.headers["content-type"].startswith("image/"):
        file_name = filename_from_url(url)
        bin_body_to_file(join(output_path, file_name), response)
        return True
    else:
        warn("URL is valid and address is reachable, but it doesn't lead to an image file."
             f"MIME type is {response.headers['content-type']}.")
        return True


def filename_from_url(url):
    file_name = url.split("/")[-1]
    return file_name


def bin_body_to_file(output_file_path, response):
    """Writes the binary content accesed via the request to a file with the given path.

    Args:
        output_file_path (str): The target file path.
        response (Response): The HTTP response returned by requests.get()
    """
    with open(output_file_path, "wb") as outfile:
        for chunk in response.iter_content(chunk_size=128):
            outfile.write(chunk)


if __name__ == "__main__":
    # TODO: Read cmd line
    get_images("some/path", "some/other/path")