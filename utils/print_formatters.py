#   -*- coding: utf-8 -*-
#
#   This file is part of validator-cli
#
#   Copyright (C) 2020 SKALE Labs
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

import os
import datetime
import texttable


def get_tty_width():
    tty_size = os.popen('stty size 2> /dev/null', 'r').read().split()
    if len(tty_size) != 2:
        return 0
    _, width = tty_size
    return int(width)


class Formatter(object):
    def table(self, headers, rows):
        table = texttable.Texttable(max_width=get_tty_width())
        table.set_cols_dtype(['t' for h in headers])
        table.add_rows([headers] + rows)
        table.set_deco(table.HEADER)
        table.set_chars(['-', '|', '+', '-'])

        return table.draw()


def format_date(date):
    return date.strftime("%b %d %Y %H:%M:%S")


def print_validators(validators):
    headers = [
        'Name',
        'Id',
        'Address',
        'Description',
        'Fee rate (%)',
        'Registration time',
        'Minimum delegation (SKL)'
    ]
    rows = []
    for validator in validators:
        date = datetime.datetime.fromtimestamp(validator['registration_time'])
        rows.append([
            validator['name'],
            validator['id'],
            validator['validator_address'],
            validator['description'],
            validator['fee_rate'],
            date,
            validator['minimum_delegation_amount']
        ])
    print(Formatter().table(headers, rows))


def print_delegations(delegations: list) -> None:
    headers = [
        'Id',
        'Delegator Address',
        'Status',
        'Validator Id',
        'Amount (SKL)',
        'Delegation period (months)',
        'Created At',
        'Info'
    ]
    rows = []
    for delegation in delegations:
        date = datetime.datetime.fromtimestamp(delegation['created'])
        rows.append([
            delegation['id'],
            delegation['address'],
            delegation['status'],
            delegation['validator_id'],
            delegation['amount'],
            delegation['delegation_period'],
            date,
            delegation['info']
        ])
    print(Formatter().table(headers, rows))


def print_linked_addresses(addresses):
    headers = [
        'Address',
        'Balance (ETH)'
    ]
    rows = []
    for address_info in addresses:
        rows.append([
            address_info['address'],
            address_info['balance'],
        ])
    print(Formatter().table(headers, rows))


def print_node_metrics(rows, total):
    headers = [
        'Date',
        'Bounty',
        'Downtime',
        'Latency'
    ]
    table = texttable.Texttable(max_width=get_tty_width())
    table.set_cols_align(["l", "r", "r", "r"])
    table.set_cols_dtype(["t", "a", "i", "f"])
    table.set_precision(1)
    table.add_rows([headers] + rows)
    table.set_deco(table.HEADER)
    table.set_chars(['-', '|', '+', '-'])
    print('\n')
    print(table.draw())
    print_total_info(total)


def print_validator_metrics(rows, total):
    headers = [
        'Date',
        'Node ID',
        'Bounty',
        'Downtime',
        'Latency'
    ]
    table = texttable.Texttable(max_width=get_tty_width())
    table.set_cols_align(["l", "r", "r", "r", "r"])
    table.set_cols_dtype(["t", "i", "f", "i", "f"])
    table.set_precision(1)
    table.add_rows([headers] + rows)
    table.set_deco(table.HEADER)
    table.set_chars(['-', '|', '+', '-'])
    print('\n')
    print(table.draw())
    print_total_info(total)


def print_bounties(nodes, bounties):
    headers = ['Date', 'All nodes']
    node_headers = [f'Node ID = {node}' for node in nodes]
    headers.extend(node_headers)
    table = texttable.Texttable(max_width=get_tty_width())
    format_string = ['t']
    format_string.extend(['f' for h in range(len(headers) - 1)])
    table.set_cols_dtype(format_string)
    table.set_cols_align(['r' for h in headers])
    table.set_precision(3)
    table.add_rows([headers] + bounties)
    table.set_deco(table.HEADER)
    table.set_chars(['-', '|', '+', '-'])
    print('\n')
    print(table.draw())


def print_total_info(total):
    total_string = f'Total bounty per the given period: {total:.3f} SKL'
    print('\n', total_string)
