""" Abstract the event session concept. """

import logging
logger = logging.getLogger("winevt.EventLog.Session")

# The concept here is to extend the other functions (Query/Subscribe) with this to give them all access to authenticate local and remote

class Session:

    def __init__(self, username = None, password = None, domain = None, server = None, auth = None, *args, **kwargs):
        """
        All fields here are optional. If none given, default will be local user authentication.
        username = username to log in with
        password = password to log in with
        domain = domain to log in to
        server = server to log in to
        auth = type of authentication to use. default is to use system default authentication.
        """

        # super(type(self), self).__init__(*args, **kwargs)

        self.username = username
        self.password = password
        self.domain = domain
        self.server = server
        self.auth = auth

        # Sanity check
        if (self.username is not None and self.password is None) or (self.username is None and self.password is not None):
            raise Exception("Must select either both username/password or neither.")



    ##############
    # Properties #
    ##############

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username):
        if type(username) not in [type(None), str]:
            raise Exception("Invalid type for username of {0}".format(type(username)))

        self.__username = username

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        if type(password) not in [type(None), str]:
            raise Exception("Invalid type for password of {0}".format(type(password)))

        self.__password = password

    @property
    def domain(self):
        return self.__domain

    @domain.setter
    def domain(self, domain):
        if type(domain) not in [type(None), str]:
            raise Exception("Invalid type for domain of {0}".format(type(domain)))

        self.__domain = domain

    @property
    def server(self):
        return self.__server

    @server.setter
    def server(self, server):
        if type(server) not in [type(None), str]:
            raise Exception("Invalid type for server of {0}".format(type(server)))

        self.__server = server

    @property
    def auth(self):
        """
        Type of authentication to use. Options are:

        default - Use the default authentication method during RPC login. The default authentication method is Negotiate.
        negotiate - Use the Negotiate authentication method during RPC login. The client and server negotiate whether to use NTLM or Kerberos.
        kerberos - Use Kerberos authentication during RPC login.
        ntlm - Use NTLM authentication during RPC login.
        """

        return self.__auth

    @auth.setter
    def auth(self, auth):

        if type(auth) not in [type(None), str]:
            raise Exception("Invalid type for authentication of {0}".format(type(auth)))

        # Set default
        if auth is None:
            auth = "default"

        auth = auth.lower()

        if auth not in ["default", "negotiate", "kerberos", "ntlm"]:
            raise Exception("Invalid authentication type requested of {0}".format(auth))

        self.__auth = auth

    @property
    def rpc_login_flags(self):
        """ Flags to be returned for the construction of the session object. """

        if self.auth == "default":
            return evtapi.EvtRpcLoginAuthDefault

        elif self.auth == "negotiate":
            return evtapi.EvtRpcLoginAuthNegotiate

        elif self.auth == "kerberos":
            return evtapi.EvtRpcLoginAuthKerberos

        elif self.auth == "ntlm":
            return evtapi.EvtRpcLoginAuthNTLM

        else:
            raise Exception("How did I get here...?")


from .. import ffi, evtapi, kernel32, get_last_error
