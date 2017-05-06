""" Defines an Event Log Query """

import logging
logger = logging.getLogger("EventLog.Query")

ERROR_NO_MORE_ITEMS = 0x103
from .Session import Session

class Query(Session):

    def __init__(self, path, query = None, direction = None, bookmark = None, *args, **kwargs):
        """
        path = The name of the channel or the full path to a log file that contains the events that you want to query. You can specify an .evt, .evtx, or.etl log file. The path is required if the Query parameter contains an XPath query; the path is ignored if the Query parameter contains a structured XML query and the query specifies the path.
        query = A query that specifies the types of events that you want to retrieve. You can specify an XPath 1.0 query or structured XML query. If your XPath contains more than 20 expressions, use a structured XML query. To receive all events, set this parameter to None or "*".
        direction = query "forward" or "backward" from your search.
        bookmark = optional Bookmark object to pick up where you left off.
        """

        # Pass down authentication constructor
        super(type(self), self).__init__(*args, **kwargs)

        self.path = path
        self.query = query or "*"
        self.direction = direction
        self.bookmark = bookmark

        # Grab a handle to this query
        self.handle = evtapi.EvtQuery(self.session, self.path, self.query, self.flags)

        # Seek to our bookmark if need be
        if self.bookmark is not None:
            self._seek_to_bookmark(bookmark)

    def _seek_to_bookmark(self,bookmark):
        """Seeks the current query to the location of our bookmark."""
        
        if not evtapi.EvtSeek(self.handle, 1, bookmark.handle, 0, evtapi.EvtSeekRelativeToBookmark):
            logger.error(get_last_error())
            return False

        return True


    def __del__(self):
        # Be sure to clean up our query
        try:
            evtapi.EvtClose(self.handle)
        except:
            pass

    def __repr__(self):
        return "<Query path={0} query={1}>".format(self.path, self.query)

    # We'll handle the iterator ourself
    def __iter__(self):
        return self

    def __next__(self):
        # Loop until we get no more events

        # Creating new objects each time
        evt_array = ffi.new("EVT_HANDLE *")
        ret = ffi.new("PDWORD")

        if not evtapi.EvtNext(self.handle, 1, evt_array, 60, 0, ret):
            if kernel32.GetLastError() != 0x103:
                logger.error(get_last_error())

            raise StopIteration

        event = Event(ffi.unpack(evt_array, 1)[0])

        # Update bookmark if we need to
        if self.bookmark is not None:
            self.bookmark.update(event)

        return event


    ##############
    # Properties #
    ##############

    @property
    def bookmark(self):
        """Bookmark object to use in query. """
        return self.__bookmark

    @bookmark.setter
    def bookmark(self, bookmark):
        if type(bookmark) not in [Bookmark, type(None)]:
            raise Exception("Invalid type for bookmark of {0}".format(type(bookmark)))

        self.__bookmark = bookmark

    @property
    def handle(self):
        return self.__handle

    @handle.setter
    def handle(self, handle):
        if handle == ffi.NULL:
            logger.error(get_last_error())
            return

        self.__handle = handle

    @property
    def flags(self):
        """ Flags to be used for this query. """
        flags = 0
        
        # Add forward and back
        if self.direction == "forward":
            flags |= evtapi.EvtQueryForwardDirection

        else:
            flags |= evtapi.EvtQueryReverseDirection

        # Determine if we're talking about a file
        if os.path.isfile(self.path):
            flags |= evtapi.EvtQueryFilePath

        else:
            flags |= evtapi.EvtQueryChannelPath

        return flags


    @property
    def path(self):
        """The name of the channel or the full path to a log file that contains the events that you want to query. You can specify an .evt, .evtx, or.etl log file. The path is required if the Query parameter contains an XPath query; the path is ignored if the Query parameter contains a structured XML query and the query specifies the path."""

        return self.__path

    @path.setter
    def path(self, path):
        # TODO: Error and type checking
        self.__path = path

    @property
    def query(self):
        """A query that specifies the types of events that you want to retrieve. You can specify an XPath 1.0 query or structured XML query. If your XPath contains more than 20 expressions, use a structured XML query. To receive all events, set this parameter to NULL or "*" """
        return self.__query

    @query.setter
    def query(self, query):
        # TODO: Error and type checking
        self.__query = query

    @property
    def direction(self):
        """The direction to move from your search. Options are "forward" (default) and "backward"."""
        return self.__direction

    @direction.setter
    def direction(self, direction):

        if type(direction) not in [type(None), str]:
            raise Exception("Invalid direction of type {0}".format(type(direction)))
        
        # Normalize it
        if direction is None:
            direction = "forward"

        else:
            direction = direction.lower()

        if direction not in ["forward","backward"]:
            raise Exception("Invalid direction recieved. Valid options are \"forward\" and \"backward\"")

        self.__direction = direction

import os
from .. import ffi, evtapi, kernel32, get_last_error
from winevt.EventLog.Event import Event
from .Bookmark import Bookmark
