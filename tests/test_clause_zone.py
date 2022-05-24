#!/usr/bin/env python3.7
"""
File: test_zone.py

Clause: zone

Title: Statements Used Only By zone Clause.

Description: Provides zone-related grammar in PyParsing engine
             for ISC-configuration style
"""
import unittest
from pyparsing import cppStyleComment, pythonStyleComment
from bind9_parser.isc_utils import assertParserResultDictFalse, assertParserResultDictTrue
from bind9_parser.isc_clause_zone import \
    zone_all_stmts_set,\
    zone_all_stmts_series,\
    clause_stmt_zone_standalone,\
    clause_stmt_zone_series


class TestClauseZone(unittest.TestCase):
    """ Test Clause Zone """

    """ exercises all OR operators in zone_all_stmts_set
    zone_all_stmts_set = (
         zone_statements_set
         | optzone_statements_set
         | optviewzone_statements_set
         | optviewzoneserver_statements_set
         | viewzone_statements_set
        )"""
    def test_isc_clause_zone__all_stmts_set_file(self):
        """ Clause zone; All Zone statement file from isc_zone.py via zone_statements_set; passing mode """
        test_string = 'file "a.b.type";'
        expected_result = {'file': '"a.b.type"'}
        assertParserResultDictTrue(
            zone_all_stmts_set,
            test_string,
            expected_result
        )

    def test_isc_clause_zone__all_stmts_set_notify_to_soa(self):
        """ Clause zone; All Zone statement 'notify-to-soa' (from isc_optzone.py via 'optzone_statements_set'dd); passing mode """
        test_string = """notify-to-soa yes;"""
        expected_result = {'notify_to_soa': 'yes'}
        assertParserResultDictTrue(
            zone_all_stmts_set,
            test_string,
            expected_result
        )

    def test_isc_clause_zone__all_stmts_set_also_notify(self):
        """ Clause zone; All Zone statement 'also-notify' (from isc_optzoneserver.py via 'optzoneserver_statements_set'dd); passing mode """
        test_string = """also-notify {mymaster; 1.2.3.4;};"""
        assertParserResultDictTrue(
            zone_all_stmts_set,
            test_string,
            {'also-notify': {'remote': [{'primary_name': 'mymaster'},
                                        {'addr': '1.2.3.4'}]}}
        )

    def test_isc_clause_zone__all_stmts_set_database(self):
        """ Clause zone; All Zone statement 'database' (from isc_viewzone.py via 'viewzone_statements_set'dd); passing mode """
        test_string = """database abcd;"""
        expected_result = {'database': 'abcd'}
        assertParserResultDictTrue(
            zone_all_stmts_set,
            test_string,
            expected_result
        )

    """ Now combine above four grouping of statements set together for our first multiple line checking"""

    def test_isc_clause_zone__all_stmts_set_combo(self):
        """ Clause zone; All Zone statement 'combo' (from various isc_[opt][view][opt][server].py); passing mode """
        test_string = """zone public { forwarders { 5.6.7.8; 1.2.3.4; }; database abcd; also-notify {mymaster; 1.2.3.4;}; notify-to-soa yes; };"""
        assertParserResultDictTrue(
            clause_stmt_zone_standalone,
            test_string,
            {'zones': [{'also-notify': {'remote': [{'primary_name': 'mymaster'},
                                                   {'addr': '1.2.3.4'}]},
                        'database': 'abcd',
                        'forwarders': {'forwarders_list': [{'addr': '5.6.7.8'},
                                                           {'addr': '1.2.3.4'}]},
                        'notify_to_soa': 'yes',
                        'zone_name': 'public'}]}
        )

    def test_isc_clause_zone__clause_stmt_single2(self):
        """ Clause zone; Statement zone; single2; passing mode """
        test_data = """zone black {type forward; forwarders {1.2.3.4;};};"""
        result = clause_stmt_zone_standalone.runTests(test_data, failureTests=False)
        self.assertTrue(result[0])

        expected_data = { 'zones': [ { 'forwarders': { 'forwarders_list': [ { 'addr': '1.2.3.4'}]},
                    'type': 'forward',
                    'zone_name': 'black'}]}

        assertParserResultDictTrue(
            clause_stmt_zone_standalone,
            test_data,
            expected_data
        )


    def test_isc_clause_zone__clause_stmt_zone_series_3_passing(self):
        """ Clause zone; Statement zone series 3; passing mode """
        test_data = 'zone black { type forward; forwarders { 1.2.3.4;}; };' + \
            'zone red {type master; file "x"; allow-update {any;};};' + \
            'zone white.com {type master; file "y"; allow-query {1.2.3.4;};};'
        expected_result = { 'zones': [ { 'forwarders': { 'forwarders_list': [ { 'addr': '1.2.3.4'}]},
               'type': 'forward',
               'zone_name': 'black'},
             { 'allow_update': {'aml': [{'addr': 'any'}]},
               'file': '"x"',
               'type': 'master',
               'zone_name': 'red'},
             { 'allow_query': {'aml': [{'addr': '1.2.3.4'}]},
               'file': '"y"',
               'type': 'master',
               'zone_name': 'white.com'}]}
        assertParserResultDictTrue(clause_stmt_zone_series, test_data, expected_result)


    def test_isc_clause_zone__clause_stmt_zone_standalone_dict_passing(self):
        """ Clause zone; Statement zone standalone dict; passing mode """
        assertParserResultDictTrue(
            clause_stmt_zone_series,
            'zone red { auto-dnssec maintain; };',
            {
                'zones': [{
                    'auto_dnssec': 'maintain',
                    'zone_name': 'red',
                    }]
                }
            )

    def test_isc_clause_zone__clause_zone_standalone_passing_5(self):
        """ Clause zone; Statement zone standalone 5; passing mode """
        test_data = [""" zone "home" { type master; file "/var/lib/bind/internal/master/db.home"; allow-update { none; }; };"""]
        test_clause_stmt_zone = clause_stmt_zone_standalone.copy()
        test_clause_stmt_zone = test_clause_stmt_zone.setWhitespaceChars(' \t')
        test_clause_stmt_zone = test_clause_stmt_zone.ignore(pythonStyleComment)
        test_clause_stmt_zone = test_clause_stmt_zone.ignore(cppStyleComment)
#        test_clause_stmt_zone.ignore(pythonStyleComment)
#        test_clause_stmt_zone.ignore(cppStyleComment)
        result = clause_stmt_zone_standalone.runTests(test_data, failureTests=False)
        self.assertTrue(result[0])

    def test_isc_clause_zone__clause_zone_standalone_passing_dict_5(self):
        """ Clause zone; Statement zone standalone dict 5; passing mode """
        assertParserResultDictTrue(
            clause_stmt_zone_standalone,
            'zone "home" IN { type master; file "/var/lib/bind/internal/master/db.home"; allow-update { none; }; };',
            {
                'zones': [{
                    'allow_update': {
                        'aml': [
                            {'addr': 'none'}
                        ]
                    },
                   'class': 'IN',
                   'file': '"/var/lib/bind/internal/master/db.home"',
                   'type': 'master',
                   'zone_name': '"home"'
                }
              ]
            }
        )

    def test_isc_clause_stmt_zone_series_passing_4A(self):
        """ Clause zone; Statement zone series 4A; passing mode """
        test_data = """
    zone "first_zone" IN {
        type master;
        file "/var/lib/bind/internal/master/db.home";
        allow-update { none; };
        };
    zone "second_zone" IN {
        type master;
        file "/var/lib/bind/internal/master/db.ip4.1.168.192";
        allow-update {
            key DDNS_UPDATER;
            };
        forwarders { };
        notify no;
        };
    zone "third_zone" IN {
        type master;
        file "/var/lib/bind/internal/master/db.localhost";
        allow-update { none; };
        forwarders { };
        notify no;
        };
    zone "fourth_zone" IN {
        type master;
        file "/var/lib/bind/internal/master/db.ip4.127";
        allow-update { none; };
        forwarders { };
        notify no;
        };
    zone "fifth_zone" IN {
        type hint;
        delegation-only yes;
        file "/var/lib/bind/internal/master/db.cache.home";
        };
    """
        expected_result = { 'zones': [ { 'allow_update': {'aml': [{'addr': 'none'}]},
               'class': 'IN',
               'file': '"/var/lib/bind/internal/master/db.home"',
               'type': 'master',
               'zone_name': '"first_zone"'},
             { 'allow_update': { 'aml': [ { 'key_id': [ 'DDNS_UPDATER']}]},
               'class': 'IN',
               'file': '"/var/lib/bind/internal/master/db.ip4.1.168.192"',
               'forwarders': [],
               'notify': 'no',
               'type': 'master',
               'zone_name': '"second_zone"'},
             { 'allow_update': {'aml': [{'addr': 'none'}]},
               'class': 'IN',
               'file': '"/var/lib/bind/internal/master/db.localhost"',
               'forwarders': [],
               'notify': 'no',
               'type': 'master',
               'zone_name': '"third_zone"'},
             { 'allow_update': {'aml': [{'addr': 'none'}]},
               'class': 'IN',
               'file': '"/var/lib/bind/internal/master/db.ip4.127"',
               'forwarders': [],
               'notify': 'no',
               'type': 'master',
               'zone_name': '"fourth_zone"'},
             { 'class': 'IN',
               'delegation-only': 'yes',
               'file': '"/var/lib/bind/internal/master/db.cache.home"',
               'type': 'hint',
               'zone_name': '"fifth_zone"'}]}
        assertParserResultDictTrue(
            clause_stmt_zone_series,
            test_data, expected_result
        )

    def test_isc_clause_stmt_zone_series_multiplezone_passing(self):
        """ Clause, All; Zone Statements group; passing """
        test_string = """
zone "first_zone" {
  type hint;
  file "root.servers";
};
zone "second_zone" in{
  type master;
  file "master/master.example.com";
  allow-transfer {192.168.23.1;192.168.23.2;};
};
zone "third_zone" in{
  type master;
  file "master.localhost";
  allow-update{none;};
};
zone "fourth_zone" in{
  type master;
  file "localhost.rev";
  allow-update{none;};
};
zone "fifth_zone" in{
  type master;
  file "192.168.0.rev";
};"""
        expected_result = { 'zones': [ { 'file': '"root.servers"',
               'type': 'hint',
               'zone_name': '"first_zone"'},
             { 'allow_transfer': { 'aml': [ { 'addr': '192.168.23.1'},
                                            { 'addr': '192.168.23.2'}]},
               'class': 'in',
               'file': '"master/master.example.com"',
               'type': 'master',
               'zone_name': '"second_zone"'},
             { 'allow_update': {'aml': [{'addr': 'none'}]},
               'class': 'in',
               'file': '"master.localhost"',
               'type': 'master',
               'zone_name': '"third_zone"'},
             { 'allow_update': {'aml': [{'addr': 'none'}]},
               'class': 'in',
               'file': '"localhost.rev"',
               'type': 'master',
               'zone_name': '"fourth_zone"'},
             { 'class': 'in',
               'file': '"192.168.0.rev"',
               'type': 'master',
               'zone_name': '"fifth_zone"'}]}
        assertParserResultDictTrue(
            clause_stmt_zone_series,
            test_string,
            expected_result
        )


if __name__ == '__main__':
    unittest.main()
