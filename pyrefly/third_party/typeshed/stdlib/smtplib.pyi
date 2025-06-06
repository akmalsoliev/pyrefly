import sys
from _socket import _Address as _SourceAddress
from _typeshed import ReadableBuffer, SizedBuffer
from collections.abc import Sequence
from email.message import Message as _Message
from re import Pattern
from socket import socket
from ssl import SSLContext
from types import TracebackType
from typing import Any, Protocol, overload
from typing_extensions import Self, TypeAlias

__all__ = [
    "SMTPException",
    "SMTPServerDisconnected",
    "SMTPResponseException",
    "SMTPSenderRefused",
    "SMTPRecipientsRefused",
    "SMTPDataError",
    "SMTPConnectError",
    "SMTPHeloError",
    "SMTPAuthenticationError",
    "quoteaddr",
    "quotedata",
    "SMTP",
    "SMTP_SSL",
    "SMTPNotSupportedError",
]

_Reply: TypeAlias = tuple[int, bytes]
_SendErrs: TypeAlias = dict[str, _Reply]

SMTP_PORT: int
SMTP_SSL_PORT: int
CRLF: str
bCRLF: bytes

OLDSTYLE_AUTH: Pattern[str]

class SMTPException(OSError): ...
class SMTPNotSupportedError(SMTPException): ...
class SMTPServerDisconnected(SMTPException): ...

class SMTPResponseException(SMTPException):
    smtp_code: int
    smtp_error: bytes | str
    args: tuple[int, bytes | str] | tuple[int, bytes, str]
    def __init__(self, code: int, msg: bytes | str) -> None: ...

class SMTPSenderRefused(SMTPResponseException):
    smtp_error: bytes
    sender: str
    args: tuple[int, bytes, str]
    def __init__(self, code: int, msg: bytes, sender: str) -> None: ...

class SMTPRecipientsRefused(SMTPException):
    recipients: _SendErrs
    args: tuple[_SendErrs]
    def __init__(self, recipients: _SendErrs) -> None: ...

class SMTPDataError(SMTPResponseException): ...
class SMTPConnectError(SMTPResponseException): ...
class SMTPHeloError(SMTPResponseException): ...
class SMTPAuthenticationError(SMTPResponseException): ...

def quoteaddr(addrstring: str) -> str: ...
def quotedata(data: str) -> str: ...

class _AuthObject(Protocol):
    @overload
    def __call__(self, challenge: None = None, /) -> str | None: ...
    @overload
    def __call__(self, challenge: bytes, /) -> str: ...

class SMTP:
    debuglevel: int
    sock: socket | None
    # Type of file should match what socket.makefile() returns
    file: Any | None
    helo_resp: bytes | None
    ehlo_msg: str
    ehlo_resp: bytes | None
    does_esmtp: bool
    default_port: int
    timeout: float
    esmtp_features: dict[str, str]
    command_encoding: str
    source_address: _SourceAddress | None
    local_hostname: str
    def __init__(
        self,
        host: str = "",
        port: int = 0,
        local_hostname: str | None = None,
        timeout: float = ...,
        source_address: _SourceAddress | None = None,
    ) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, tb: TracebackType | None
    ) -> None: ...
    def set_debuglevel(self, debuglevel: int) -> None: ...
    def connect(self, host: str = "localhost", port: int = 0, source_address: _SourceAddress | None = None) -> _Reply: ...
    def send(self, s: ReadableBuffer | str) -> None: ...
    def putcmd(self, cmd: str, args: str = "") -> None: ...
    def getreply(self) -> _Reply: ...
    def docmd(self, cmd: str, args: str = "") -> _Reply: ...
    def helo(self, name: str = "") -> _Reply: ...
    def ehlo(self, name: str = "") -> _Reply: ...
    def has_extn(self, opt: str) -> bool: ...
    def help(self, args: str = "") -> bytes: ...
    def rset(self) -> _Reply: ...
    def noop(self) -> _Reply: ...
    def mail(self, sender: str, options: Sequence[str] = ()) -> _Reply: ...
    def rcpt(self, recip: str, options: Sequence[str] = ()) -> _Reply: ...
    def data(self, msg: ReadableBuffer | str) -> _Reply: ...
    def verify(self, address: str) -> _Reply: ...
    vrfy = verify
    def expn(self, address: str) -> _Reply: ...
    def ehlo_or_helo_if_needed(self) -> None: ...
    user: str
    password: str
    def auth(self, mechanism: str, authobject: _AuthObject, *, initial_response_ok: bool = True) -> _Reply: ...
    @overload
    def auth_cram_md5(self, challenge: None = None) -> None: ...
    @overload
    def auth_cram_md5(self, challenge: ReadableBuffer) -> str: ...
    def auth_plain(self, challenge: ReadableBuffer | None = None) -> str: ...
    def auth_login(self, challenge: ReadableBuffer | None = None) -> str: ...
    def login(self, user: str, password: str, *, initial_response_ok: bool = True) -> _Reply: ...
    if sys.version_info >= (3, 12):
        def starttls(self, *, context: SSLContext | None = None) -> _Reply: ...
    else:
        def starttls(
            self, keyfile: str | None = None, certfile: str | None = None, context: SSLContext | None = None
        ) -> _Reply: ...

    def sendmail(
        self,
        from_addr: str,
        to_addrs: str | Sequence[str],
        msg: SizedBuffer | str,
        mail_options: Sequence[str] = (),
        rcpt_options: Sequence[str] = (),
    ) -> _SendErrs: ...
    def send_message(
        self,
        msg: _Message,
        from_addr: str | None = None,
        to_addrs: str | Sequence[str] | None = None,
        mail_options: Sequence[str] = (),
        rcpt_options: Sequence[str] = (),
    ) -> _SendErrs: ...
    def close(self) -> None: ...
    def quit(self) -> _Reply: ...

class SMTP_SSL(SMTP):
    keyfile: str | None
    certfile: str | None
    context: SSLContext
    if sys.version_info >= (3, 12):
        def __init__(
            self,
            host: str = "",
            port: int = 0,
            local_hostname: str | None = None,
            *,
            timeout: float = ...,
            source_address: _SourceAddress | None = None,
            context: SSLContext | None = None,
        ) -> None: ...
    else:
        def __init__(
            self,
            host: str = "",
            port: int = 0,
            local_hostname: str | None = None,
            keyfile: str | None = None,
            certfile: str | None = None,
            timeout: float = ...,
            source_address: _SourceAddress | None = None,
            context: SSLContext | None = None,
        ) -> None: ...

LMTP_PORT: int

class LMTP(SMTP):
    def __init__(
        self,
        host: str = "",
        port: int = 2003,
        local_hostname: str | None = None,
        source_address: _SourceAddress | None = None,
        timeout: float = ...,
    ) -> None: ...
