#   -*- coding: utf-8 -*-
#
#   This file is part of skale-node-cli
#
#   Copyright (C) 2019 SKALE Labs
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.


from yaspin import yaspin

from utils.web3_utils import (init_skale_from_config, init_skale_w_wallet_from_config,
                              check_tx_result)
from utils.print_formatters import print_validators, print_delegations


def register(name: str, description: str, commission_rate: int, min_delegation: int, pk_file: str):
    skale = init_skale_w_wallet_from_config(pk_file)
    if not skale:
        return
    with yaspin(text='Registering new validator', color="yellow") as sp:
        tx_res = skale.delegation_service.register_validator(
            name=name,
            description=description,
            fee_rate=commission_rate,
            min_delegation_amount=min_delegation
        )
        if not check_tx_result(tx_res.hash, skale.web3):
            sp.write(f'Transaction failed: {tx_res.hash}')
            return
        sp.write("✔ New validator registered")


def validators_list():
    skale = init_skale_from_config()
    validators = skale.validator_service.ls()
    print_validators(validators)


def delegations(address):
    skale = init_skale_from_config()
    if not skale:
        return
    delegations_list = skale.delegation_service.get_all_delegations_by_validator(address)
    print(f'Delegations for address {address}:\n')
    print_delegations(delegations_list)


def accept_pending_delegation(delegation_id, pk_file: str) -> None:
    skale = init_skale_w_wallet_from_config(pk_file)
    if not skale:
        return
    with yaspin(text='Accepting delegation request', color="yellow") as sp:
        tx_res = skale.delegation_service.accept_pending_delegation(
            delegation_id=delegation_id
        )
        if not check_tx_result(tx_res.hash, skale.web3):
            sp.write(f'Transaction failed: {tx_res.hash}')
            return
        sp.write(f'✔ Delegation request with ID {delegation_id} accepted')