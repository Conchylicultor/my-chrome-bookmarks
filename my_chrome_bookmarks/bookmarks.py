"""Chrome bookmarks API."""

from __future__ import annotations

import collections
import dataclasses
import datetime
import functools
import json
import pathlib
import sys
import textwrap
import types
from typing import Iterable, Optional

from etils import epy


def timestamp2date(timestamp: str) -> datetime.datetime:
    epoch_start = datetime.datetime(1601, 1, 1)
    delta = datetime.timedelta(microseconds=int(timestamp))
    return (epoch_start + delta).replace(tzinfo=datetime.timezone.utc).astimezone()


@dataclasses.dataclass(frozen=True)
class BookmarkRoots:
    bookmark_bar: BookmarkFolder
    other: BookmarkFolder
    synced: BookmarkFolder


@dataclasses.dataclass(frozen=True)
class _BookmarkItem:
    parent: Optional[BookmarkFolder]
    date_added: datetime.datetime
    guid: str
    id: int
    name: str

    @functools.cached_property
    def path(self) -> str:
        bookmark = self
        parts = [self.name]
        while bookmark := bookmark.parent:
            parts.append(bookmark.name)
        return "/".join(reversed(parts))

    def is_folder(self) -> bool:
        return isinstance(self, BookmarkFolder)

    @classmethod
    def from_json(cls, parent, value) -> _BookmarkItem:
        value = types.SimpleNamespace(**value)

        common_kwargs = dict(
            parent=parent,
            date_added=timestamp2date(value.date_added),
            guid=value.guid,
            id=int(value.id),
            name=value.name,
        )
        if value.type == "url":
            return BookmarkUrl(
                url=value.url,
                **common_kwargs,
            )
        else:
            parent = BookmarkFolder(children=[], **common_kwargs)
            parent.children.extend(
                _BookmarkItem.from_json(parent, v) for v in value.children
            )
            return parent


@dataclasses.dataclass(frozen=True)
class BookmarkFolder(_BookmarkItem):
    children: list[BookmarkUrl]

    @property
    def url(self) -> str:
        """`chrome://` url of the folder."""
        return f"chrome://bookmarks/?id={self.id}"

    @functools.cached_property
    def folders(self) -> list[BookmarkFolder]:
        return [v for v in self.children if isinstance(v, BookmarkFolder)]

    @functools.cached_property
    def urls(self) -> list[BookmarkUrl]:
        return [v for v in self.children if isinstance(v, BookmarkUrl)]

    @functools.cached_property
    def num_urls(self) -> int:
        """Returns the total number of urls contained in all sub-folders."""
        return sum(f.num_urls for f in self.folders) + len(self.urls)

    @functools.cached_property
    def num_folders(self) -> int:
        """Returns the total number of sub-folders."""
        if not self.folders:
            return 0
        else:
            return sum(f.num_folders + 1 for f in self.folders)

    @functools.cached_property
    def _name2children(self) -> dict[str, list[_BookmarkItem]]:
        """Returns the mapping name -> children (name can be duplicate)."""
        name2children = collections.defaultdict(list)
        for b in self.children:
            name2children[b.name].append(b)
        return name2children

    def __iter__(self) -> Iterable[_BookmarkItem]:
        """Iterate over all children."""
        return iter(self.children)

    def __getitem__(self, value: str) -> _BookmarkItem:
        children = self._name2children[value]
        if len(children) > 1:
            raise KeyError(f"Duplicated key: {value} (bookmarks have the same name)")
        (item,) = children
        return item

    def __repr__(self) -> str:
        children = epy.Lines()
        children += "children=["
        with children.indent():
            for child in self.children:
                if isinstance(child, BookmarkFolder):
                    line = f"{child.name}/ ({child.num_urls} urls)"
                else:
                    url = textwrap.shorten(child.url, width=100, placeholder="...")
                    line = f"{child.name!r} ({url})"
                children += line
        children += "],"

        lines = epy.Lines()
        lines += f"{type(self).__name__}("
        with lines.indent():
            lines += f"name={self.name!r},"
            lines += f"path={self.path!r},"
            lines += f"date_added={self.date_added},"
            lines += f"url={self.url!r},"
            lines += f"num_urls={self.num_urls},"
            lines += children.join()
        lines += ")"
        return lines.join()


@dataclasses.dataclass(frozen=True)
class BookmarkUrl(_BookmarkItem):
    url: str

    def __repr__(self) -> str:
        lines = epy.Lines()
        lines += f"{type(self).__name__}("
        with lines.indent():
            lines += f"name={self.name!r},"
            lines += f"path={self.path!r},"
            lines += f"date_added={self.date_added},"
            lines += f"url={self.url!r},"
        lines += ")"
        return lines.join()


def get_bookmarks_path() -> pathlib.Path:
    """Returns the bookmark path."""
    if "linux" in sys.platform.lower():
        path = "~/.config/google-chrome/Default/Bookmarks"
    if "darwin" in sys.platform.lower():
        path = "~/Library/Application Support/Google/Chrome/Default/Bookmarks"
    if "win32" in sys.platform.lower():
        path = "~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks"
    path = pathlib.Path(path)
    path = path.expanduser()
    if not path.exists():
        raise ValueError(f"{path} not found.")
    return path


@functools.lru_cache(None)
def _bookmarks_roots(path: pathlib.Path) -> BookmarkRoots:
    data = json.loads(path.read_text())
    data = data["roots"]
    return BookmarkRoots(
        bookmark_bar=_BookmarkItem.from_json(None, data["bookmark_bar"]),
        other=_BookmarkItem.from_json(None, data["other"]),
        synced=_BookmarkItem.from_json(None, data["synced"]),
    )


def bookmarks() -> BookmarkRoots:
    path = get_bookmarks_path()
    return _bookmarks_roots(path)


def bookmark_bar() -> BookmarkFolder:
    """Return the bookmark bar top-level folder."""
    return bookmarks().bookmark_bar
