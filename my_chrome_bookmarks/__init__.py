"""Chrome bookmarks utils."""

from my_chrome_bookmarks.bookmarks import (
    BookmarkFolder,
    BookmarkUrl,
    bookmark_bar,
    bookmarks,
    get_bookmarks_path,
)

__version__ = "1.2.0"

__all__ = [
    "__version__",
    "bookmarks",
    "bookmark_bar",
    "BookmarkUrl",
    "BookmarkFolder",
    "get_bookmarks_path",
]
