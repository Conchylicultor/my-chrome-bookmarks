"""Chrome bookmarks utils."""

from my_chrome_bookmarks.bookmarks import bookmarks
from my_chrome_bookmarks.bookmarks import bookmark_bar
from my_chrome_bookmarks.bookmarks import BookmarkUrl
from my_chrome_bookmarks.bookmarks import BookmarkFolder
from my_chrome_bookmarks.bookmarks import get_bookmarks_path

__version__ = "1.0.1"

__all__ = [
    "bookmarks",
    "bookmark_bar",
    "BookmarkUrl",
    "BookmarkFolder",
    "get_bookmarks_path",
]
