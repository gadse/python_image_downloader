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
import argparse
import logging
import sys
import traceback
from os.path import join, exists

import requests
from requests import Response

logger = logging.getLogger("downloader")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("log.csv", mode="w")
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
csv_formatter = logging.Formatter("%(asctime)s;%(name)s;%(filename)s;%(lineno)d;%(levelname)s;\"%(message)s\"")
console_formatter = logging.Formatter(
    "%(asctime)s | %(name)s | %(filename)s:%(lineno)d | %(levelname)s\t| %(message)s")
fh.setFormatter(csv_formatter)
ch.setFormatter(console_formatter)
logger.addHandler(fh)
logger.addHandler(ch)


def log_exception(exctype, value, tb):
    trace = "".join(traceback.format_exception(exctype, value, tb)).replace("\"", "\'")
    logger.critical(trace)

sys.excepthook = log_exception


def get_images(input_file_path, output_path):
    """Interprets each line in the specified input file is a valid URL to an image file, downloads all image files, and
    writes them to the specified output path. URLs that don't link to image files are ignored with a warning.

    Args:
        input_file_path (str): The path to the input file.
        output_path (str): The path to the output directory.

    Returns:
        (list):
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
                warn_msg = f"Exception occured when trying to connect. Ignoring this line.\nURL: {url}.\nEXCEPTION: {e}"
                logging.warning(warn_msg)
            else:
                success = _url_to_image_file(output_path, response)
                if not success:
                    faulty_lines.append((url, response.status_code))
    return faulty_lines


def _url_to_image_file(output_path, response, file_name=None):
    """Takes a URL that leads to an available/connectable resource, downloads the resource if it is an
    image file, and saves it to disk under the given output path. The image file's file name is determined from the url,
    if none is given.

    Args:
        output_path (str): The path to the directory under which the image file is to be written.
        response (Response): The Repsonse as generated by requests.get()
        file_name (str): Te written file's name. Should adhere to the usual naming conventions/restrictions of your
            system.

    Returns:
        False if the response's status code is 200, False otherwise. If the linked resource is not an image file, True
        is returned and a UserWarning is issued.
    """
    if not response.status_code == 200:
        result = False
    elif response.headers["content-type"].startswith("image/"):
        if not file_name:
            file_name = _filename_from_url(response.url)
        _bin_body_to_file(join(output_path, file_name), response)
        result = True
    else:
        warn_msg = ("URL is valid and address is reachable, but it doesn't lead to an image file."
                   f"MIME type is {response.headers['content-type']}.")
        logger.warning(warn_msg)
        result = True
    return result


def _filename_from_url(url):
    """Determines a file name from the given URL.

    Args:
        url (str):

    Returns:
        (str):
            An acceptable file name.
    """
    file_name = url.split("/")[-1]
    return file_name


def _bin_body_to_file(output_file_path, response):
    """Writes the binary content accesed via the request to a file with the given path.

    Code inspired by: https://stackoverflow.com/a/13137873

    Args:
        output_file_path (str): The target file path.
        response (Response): The HTTP response returned by requests.get()
    """
    with open(output_file_path, "wb") as outfile:
        for chunk in response.iter_content(chunk_size=128):
            outfile.write(chunk)


def __main():
    args = __parse_cmd_args()
    faulty = get_images(args.file, args.dir)
    logger.info(f"Faulty URLs: {faulty}")


def __parse_cmd_args():
    """Parses the command line arguments using argparse.

    Returns:
        The parsed arguments as returned by argparse.ArgumentParser.parse_args()
    """
    parser = argparse.ArgumentParser(description='Python Image Downloader.')
    parser.add_argument("-f", "--file",
                        help="Where the URL file is located.")
    parser.add_argument("-d", "--dir",
                        help="Where the downloaded files are to be stored.")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    logger.info("Starting download...")
    __main()
    logger.info("Finished!")
