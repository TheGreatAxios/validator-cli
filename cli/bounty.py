#   -*- coding: utf-8 -*-
#
#   This file is part of skale-node-cli
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
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import click
from core.metrics import get_bounty_from_events, get_nodes_for_validator, get_bounty_rows
from utils.print_formatters import print_bounties


@click.group()
def bounty_cli():
    pass


@bounty_cli.group('bounty', help="Validators bounty commands")
def bounty():
    pass


@bounty.command(help="List of aggregated bounties for validator with given id")
@click.option('--index', '-id')
@click.option('--since', '-s')
@click.option('--till', '-t')
@click.option('--limit', '-l')
def validator(index, since, till, limit):
    if index is None:
        print('Validator ID expected: "bounty validator -id n"')
        return
    node_ids = get_nodes_for_validator(index)
    print('Please wait - collecting bounty data from blockchain...')
    node_ids = [int(node_id) for node_id in node_ids]
    bounties, total = get_bounty_from_events(node_ids, since, till, limit)
    sums = ['Total per period:']
    for i in range(1, len(bounties[0])):
        sums.append(sum([bounty[i] for bounty in bounties]))
    spaces = [''] * len(bounties[0])
    bounties.append(spaces)
    bounties.append(sums)
    print_bounties(node_ids, bounties)
