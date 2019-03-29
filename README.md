# Python Image Downloader
*Just a small project to test some things in Python.*

This small project is a utility tool to download all images from urls in a given file. Each line in the file contains 
one URL. The downloaded files are to be written to a target directory on the hard disk.

## Usage

**General**:

`python3 downloader.py -f=<file> -d=<directory>` with`file` being the input file and `directory` being the target 
directory as decribet in the introducing section.

**Concrete**:

`python3 downloader.py -f=test_data/correct_paths -d=test_target`

## Background

The script was written (and tested) as though it would be used in an important live system and maintained by other 
developers. It was also written under the assumption that it would only be called with file system paths that point to 
an existing file/directory, as the necessary file system structure would be taken care of before this script is
executed, either by system administrators, operators, or containerization solutions.

Tests that include incompatible read/write access permissions are included to document expected behaviour. "Rather ask
for forgiveness than for permission" is common in the Python community. Had I written this little piece of software in
Java, I'd have included a few checks before writing a file is attempted.

## Lessons Learned

  1. Don't use large stock image providers for such things. Their redirect mechanisms and API policies are really more 
trouble than it's worth. Use a service that provides images under static URLs, such as http://placeholder.com.

  2. Git does not sync file access permissions. If you want to test for behaviour under different file access permission
situations, just create those files in your test scripts. Deletion is possible afterwards, if your system provides a
user with "root-like rights" in certain situations. You can issue bash commands via `subprocess.run()`, so you can sudo
to that test cleanup user for cleanup. I did not include this in here, as I guess it would have gone too far.