# This file is part of the TREZOR project.
#
# Copyright (C) 2017 Saleem Rashid <trezor@saleemrashid.com>
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library.  If not, see <http://www.gnu.org/licenses/>.

from binascii import hexlify
import pytest

from .common import TrezorTest

from trezorlib import nem
from trezorlib.tools import parse_path


# assertion data from T1
@pytest.mark.xfail  # to be removed when nem is merged
class TestMsgNEMSignTxOther(TrezorTest):

    def test_nem_signtx_importance_transfer(self):
        self.setup_mnemonic_nopin_nopassphrase()

        with self.client:
            tx = self.client.nem_sign_tx(parse_path("m/44'/1'/0'/0'/0'"), {
                "timeStamp": 12349215,
                "fee": 9900,
                "type": nem.TYPE_IMPORTANCE_TRANSFER,
                "deadline": 99,
                "message": {
                },
                "importanceTransfer": {
                    "mode": 1,  # activate
                    "publicKey": "c5f54ba980fcbb657dbaaa42700539b207873e134d2375efeab5f1ab52f87844",
                },
                "version": (0x98 << 24),
            })

            assert hexlify(tx.data) == b'01080000010000981f6fbc0020000000edfd32f6e760648c032f9acb4b30d514265f6a5b5f8a7154f2618922b4062084ac26000000000000630000000100000020000000c5f54ba980fcbb657dbaaa42700539b207873e134d2375efeab5f1ab52f87844'
            assert hexlify(tx.signature) == b'b6d9434ec5df80e65e6e45d7f0f3c579b4adfe8567c42d981b06e8ac368b1aad2b24eebecd5efd41f4497051fca8ea8a5e77636a79afc46ee1a8e0fe9e3ba90b'

    def test_nem_signtx_provision_namespace(self):

        self.setup_mnemonic_nopin_nopassphrase()

        tx = self.client.nem_sign_tx(parse_path("m/44'/1'/0'/0'/0'"), {
            "timeStamp": 74649215,
            "fee": 2000000,
            "type": nem.TYPE_PROVISION_NAMESPACE,
            "deadline": 74735615,
            "message": {
            },
            "newPart": "ABCDE",
            "rentalFeeSink": "TALICE2GMA34CXHD7XLJQ536NM5UNKQHTORNNT2J",
            "rentalFee": 1500,
            "parent": None,
            "version": (0x98 << 24),
        })

        assert hexlify(tx.data) == b'01200000010000987f0e730420000000edfd32f6e760648c032f9acb4b30d514265f6a5b5f8a7154f2618922b406208480841e0000000000ff5f74042800000054414c49434532474d4133344358484437584c4a513533364e4d35554e4b5148544f524e4e54324adc05000000000000050000004142434445ffffffff'
        assert hexlify(tx.signature) == b'f047ae7987cd3a60c0d5ad123aba211185cb6266a7469dfb0491a0df6b5cd9c92b2e2b9f396cc2a3146ee185ba02df4f9e7fb238fe479917b3d274d97336640d'
