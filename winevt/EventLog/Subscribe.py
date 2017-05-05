""" Class for subscribing to Windows Event Logs. """

import logging
logger = logging.getLogger("EventLog.Subscribe")

class Subscribe:

    def __init__(self, path, query, callback, start_from=None, tolerate_query_errors = False, strict = False):
        """
        path = The name of the channel or the full path to a log file that contains the events that you want to query. You can specify an .evt, .evtx, or.etl log file. The path is required if the Query parameter contains an XPath query; the path is ignored if the Query parameter contains a structured XML query and the query specifies the path.
        query = A query that specifies the types of events that you want to retrieve. You can specify an XPath 1.0 query or structured XML query. If your XPath contains more than 20 expressions, use a structured XML query. To receive all events, set this parameter to None or "*".
        callback = python function to accept callbacks from the event subscription.
        start_from = Where to start subscription from. Default is "future". See property.
        tolerate_query_errors = Should we try to push through errors in the query. Defaults to False.
        strict = Should we be strict about our query. See Property for details.
        """

        self.path = path
        self.query = query
        self.start_from = start_from or "future"
        self.tolerate_query_errors = tolerate_query_errors
        self.strict = strict
        self.callback = callback

    def __repr__(self):
        return "<Subscribe path=\"{0}\" query=\"{1}\" callback=\"{2}\">".format(self.path, self.query, self.__callback_python.__name__)

    ##############
    # Properties #
    ##############

    @property
    def strict(self):
        """Forces the EvtSubscribe call to fail if you specify EvtSubscribeStartAfterBookmark and the bookmarked event is not found (the return value is ERROR_NOT_FOUND). Also, set this flag if you want to receive notification in your callback when event records are missing."""

        return self.__strict

    @strict.setter
    def strict(self, strict):

        if type(strict) is not bool:
            raise Exception("Invalid type for strict of {0}".format(type(strict)))

        self.__strict = strict

    @property
    def tolerate_query_errors(self):
        """Complete the subscription even if the part of the query generates an error (is not well formed). The service validates the syntax of the XPath query to determine if it is well formed. If the validation fails, the service parses the XPath into individual expressions. It builds a new XPath beginning with the left most expression. The service validates the expression and if it is valid, the service adds the next expression to the XPath. The service repeats this process until it finds the expression that is failing. It then uses the valid expressions that it found beginning with the leftmost expression as the XPath query (which means that you may not get the events that you expected). If no part of the XPath is valid, the EvtSubscribe call fails."""

        return self.__tolerate_query_errors

    @tolerate_query_errors.setter
    def tolerate_query_errors(self, tolerate_query_errors):
        if type(tolerate_query_errors) is not bool:
            raise Exception("Invalid type for tolerate_query_errors of {0}".format(type(tolerate_query_errors)))

        self.__tolerate_query_errors = tolerate_query_errors

    @property
    def flags(self):
        """ Flags for this subscription. """

        flags = 0

        if self.start_from == "future":
            flags |= evtapi.EvtSubscribeToFutureEvents

        elif self.start_from == "oldest":
            flags |= evtapi.EvtSubscribeStartAtOldestRecord

        if self.tolerate_query_errors:
            flags |= evtapi.EvtSubscribeTolerateQueryErrors

        if self.strict:
            flags |= evtapi.EvtSubscribeStrict

        return flags

    @property
    def start_from(self):
        """Where to start our subscription from. Options are:
        future -- Only get future events, no events already in the log.
        oldest -- Get all records that are valid for the query, and then subscribe to all future events.
        bookmark -- Use a bookmark. Not yet implemented
        """

        return self.__start_from

    @start_from.setter
    def start_from(self, start_from):
        if type(start_from) is not str:
            raise Exception("Attempting to set invalid start_from type of {0}".format(type(start_from)))

        start_from = start_from.lower()
        
        if start_from not in ["future", "oldest"]:
            raise Exception("start_from of \"{0}\" not valid or not supported yet.".format(start_from))

        self.__start_from = start_from


    @property
    def callback(self):
        return self.__callback

    @callback.setter
    def callback(self, callback):
        if type(callback) is not type(lambda x: x):
            raise Exception("Did not receive function for callback. Recieved invalid type {0}".format(type(callback)))

        if len(signature(callback).parameters) != 3:
            raise Exception("Python callback function must accept 3 parameters: action, pContext, Event")

        # Keep track of the original function
        self.__callback_python = callback
        
        ################
        # Add the hook #
        ################

        if out_of_line:
            # out-of-line is preferred
            @ffi.def_extern()
            def SubscriptionCallback(action, pContext, hEvent):
                # TODO: Watch action for error
                # https://msdn.microsoft.com/en-us/library/windows/desktop/aa385596(v=vs.85).aspx
                # 
                callback(action, pContext, Event(hEvent, close=False))

                # TODO: Do we always assume success?
                return 1

            self.__callback = SubscriptionCallback
            cb_ptr = evtapi.SubscriptionCallback

        else:
            # In-line callback setup
            @ffi.callback("DWORD WINAPI SubscriptionCallback(EVT_SUBSCRIBE_NOTIFY_ACTION, PVOID, EVT_HANDLE)")
            def SubscriptionCallback(action, pContext, hEvent):
                callback(action, pContext, Event(hEvent, close=False))

                # TODO: Do we always assume success?
                return 1

            self.__callback = SubscriptionCallback
            cb_ptr = SubscriptionCallback

        #
        # Subscribe to the events
        #

        ret = evtapi.EvtSubscribe(ffi.NULL, ffi.NULL, self.path, self.query, ffi.NULL, ffi.NULL, cb_ptr, self.flags)

        if not ret:
            logger.error("Something went wrong subscribing...")

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

from inspect import signature
from .. import ffi, evtapi, out_of_line
from winevt.EventLog.Event import Event
