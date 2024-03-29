# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)


from collections import namedtuple
from dataclasses import make_dataclass

Sender = Receiver = namedtuple('User', ['name', 'addr'])


import aiosmtplib
from drymail import Message

class SMTP:
    """
    Wrapper around `aiosmtplib.SMTP` class, for managing a SMTP client.

    Parameters
    ----------
    host : str
        The hostname of the SMTP server to connect to.
    port : int, optional
        The port number of the SMTP server to connect to.
    user : str, optional
        The username to be used for authentication to the SMTP server.
    password : str, optional
        The password to be used for authentication to the SMTP server.
    tls : bool, optional
        Whether to use TLS // `starttls` for the SMTP connection.

    Attributes
    ----------
    client: `aiosmtplib.SMTP` object
        The SMTP client that'd be used to send emails.
    host : str
        The hostname of the SMTP server to connect to.
    port : int
        The port number of the SMTP server to connect to.
    user : str
        The username to be used for authentication to the SMTP server.
    password : str
        The password to be used for authentication to the SMTP server.
    tls : bool
        Whether to use TLS // `starttls` for the SMTP connection.
    """

    def __init__(self, host, port=None, user=None, password=None, tls=True, **kwargs):
        self.host = host
        self.tls = tls
        if tls:
            self.port = port or 465
        else:
            self.port = port or 25
        self.user = user
        self.password = password
        self.client = aiosmtplib.SMTP(hostname=self.host, port=self.port, source_address='Python', use_tls=self.tls)

    async def __aenter__(self):
        await self.client.__aenter__()
        await self.client.login(self.user, self.password)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return await self.client.__aexit__(exc_type, exc, tb)

    async def send(self, message, sender=None, receivers=None):
        """
        Send an email through this SMTP client.

        Parameters
        ----------
        message : `drymail.Message` object
            The message to be sent.
        sender : str, optional
            The email address of the sender.
        receivers : list of str, optional
            The email addresses of the receivers // recipients.
        """

        if not isinstance(message, Message):
            raise ValueError('message should be instance of drymail.Message')

        if not message.prepared:
            message.prepare()
        await self.client.send_message(message.message, sender=sender, recipients=receivers)
