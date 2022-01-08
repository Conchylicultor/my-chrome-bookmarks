"""Tests.

Note: Those tests require chrome bookmarks to be installed locally.
"""

import my_chrome_bookmarks


def test_bookmarks():
    bookmarks = my_chrome_bookmarks.bookmarks()
    bookmark_bar = bookmarks.bookmark_bar
    assert bookmark_bar.num_urls > 0
    assert bookmark_bar.num_folders > 0


def test_bookmark_bar():
    bookmarks = my_chrome_bookmarks.bookmark_bar()
    assert bookmarks.num_urls > 0
    assert bookmarks.num_folders > 0
    assert len(bookmarks.urls) + len(bookmarks.folders) == len(bookmarks.children)
    folder = bookmarks.folders[0]
    folder2 = bookmarks[folder.name]  # Access by index
    assert folder == folder2
    assert repr(folder) == repr(folder2)
