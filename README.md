# my-chrome-bookmarks

[![PyPI version](https://badge.fury.io/py/my_chrome_bookmarks.svg)](https://badge.fury.io/py/my_chrome_bookmarks)

Python extension to read local Chrome bookmarks.

Installation:

```sh
pip install my-chrome-bookmarks
```

Usage:

```python
import my_chrome_bookmarks

# Get the top-level folder.
# Equivalent to `my_chrome_bookmarks.bookmarks().bookmark_bar`
bookmarks = my_chrome_bookmarks.bookmark_bar()

# Note: `bookmarks.urls` and `bookmarks.folders` also exists
for bookmark in bookmarks:
    if bookmark.is_folder:  # Folder
        print(f'{bookmark.name} contain {bookmark.num_urls} urls')
    else:  # Url
        print(f'{bookmark.name}: {bookmark.url}')


bookmark = bookmarks['My folder']  # Access a specific bookmark or folder
```

See the [source code](https://github.com/Conchylicultor/my-chrome-bookmarks/blob/main/my_chrome_bookmarks/bookmarks.py) for the full API.
