#!/usr/bin/env python3
"""
File: isc_clause_parental_agents.py

Clause: parental_agents

Title: Clause statement for 'parental-agents'

Description: 

  Statement Grammar:

    parental-agents <string> [ port <integer> ] [ dscp <integer> ] {
            (
                <remote-servers> |
                <ipv4_address> [ port <integer> ] |
                <ipv6_address> [ port <integer> ]
            )
            [ key <string> ]
            [ tls <string> ]; ...
    };

"""
from pyparsing import Group, Keyword, \
    ZeroOrMore, OneOrMore, Optional, ungroup
from bind9_parser.isc_utils import semicolon, \
    quotable_name, \
    lbrack, rbrack, key_id, fqdn_name
from bind9_parser.isc_inet import ip46_addr, \
    inet_ip_port_keyword_and_number_element, \
    inet_dscp_port_keyword_and_number_element

# NOTE: If any declaration here is to be used outside
# the 'parental_agents' clause, it should instead be defined within isc_utils.py

parental_agents_server_address_element = (
        (
                ungroup(ip46_addr)('ip_addr')
                + Optional(inet_ip_port_keyword_and_number_element)
        )
        | fqdn_name('fqdn')
)

parental_agents_key_element = (
        Keyword('key').suppress()
        + key_id
)

parental_agents_tls_element = (
        Keyword('tls').suppress()
        + key_id('tls_name')
)

clause_stmt_parental_agents_standalone = (
    Keyword('parental-agents').suppress()
    - Group(
        quotable_name('parental_agent_name')
        + Optional(inet_ip_port_keyword_and_number_element)
        + Optional(inet_dscp_port_keyword_and_number_element)
        + lbrack
        + OneOrMore(
            Group(
                parental_agents_server_address_element
                + Optional(parental_agents_key_element)
                + Optional(parental_agents_tls_element)
                + semicolon
            )  # useless ('parental_agents_group4') label here
        )('parental_agent_servers')
        + rbrack
    )('parental_agents*')
    + semicolon
)

clause_stmt_parental_agents_set = clause_stmt_parental_agents_standalone
clause_stmt_parental_agents_standalone.setName(
    'parental_agents <name> [ port <integer> ] [ dscp <integer> ] { [<remote-server>|' +
    '( <ipv4_address> [ port <integer> ) ' +
    ' | ( <ipv6_address> [ port <integer> ] ) [ key <string> ] [ tls <string> ]; ... };')

# {0-*} statement
clause_stmt_parental_agents_series = ZeroOrMore(clause_stmt_parental_agents_set)  # 0-*, may occur multiple times
clause_stmt_parental_agents_series.setName(
    'parental_agents <string> [ port <integer> ] [ dscp <integer> ] { ... }; ...')
