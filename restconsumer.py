from __future__ import absolute_import, division, print_function, \
    unicode_literals

import requests
from iota import *
from iota.adapter.sandbox import SandboxAdapter
from pprint import pprint

# sample dummy api request
sample_request = requests.get("https://api.github.com/user", auth=('user', 'passwd'))

# Create the API object.
iota = Iota(
    # To use sandbox mode, inject a ``SandboxAdapter``.
    adapter=SandboxAdapter(
        # URI of the sandbox node.
        uri='https://sandbox.iotatoken.com/api/v1/',

        # Access token used to authenticate requests.
        # Contact the node maintainer to get an access token.
        auth_token='auth token goes here',
    ),

    # Seed used for cryptographic functions.
    # If null, a random seed will be generated.
    seed=b'SEED9GOES9HERE',
)

# Example of sending a transfer using the sandbox.
# For more information, see :py:meth:`Iota.send_transfer`.
# noinspection SpellCheckingInspection
default_depth = 100

sample_transaction = ProposedTransaction(
    # API payment address.
    address=
    Address(
        b'TESTVALUE9DONTUSEINPRODUCTION99999FBFFTG'
        b'QFWEHEL9KCAFXBJBXGE9HID9XCOHFIDABHDG9AHDR'
    ),

    # Amount of IOTA to transfer.
    # This value may be zero.
    value=17,

    # Optional tag to attach to the transfer.
    tag=Tag(b'EXAMPLE'),

    # Optional message to include with the transfer.
    message=TryteString.from_string('I am making an API Request!'),
)


def requestData(api_request=sample_request):
    iota.send_transfer(
        depth=default_depth,

        # One or more :py:class:`ProposedTransaction` objects to add to the
        # bundle.
        transfers=[sample_transaction],
    )
    if sample_transaction.value == 17:
        return api_request.json()

def main():
    requestData()

if __name__ == "__main__": main()
