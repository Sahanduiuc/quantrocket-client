# Copyright 2017 QuantRocket - All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse

def add_subparser(subparsers):
    _parser = subparsers.add_parser("master", description="QuantRocket securities master CLI", help="quantrocket master -h")
    _subparsers = _parser.add_subparsers(title="subcommands", dest="subcommand")
    _subparsers.required = True


    examples = """
Examples:
List all exchanges:

    quantrocket master exchanges

List stock exchanges in North America:

    quantrocket master exchanges --regions north_america --sec-types STK
    """
    parser = _subparsers.add_parser(
        "exchanges",
        help="list exchanges by security type and country as found on the IB website",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "-r", "--regions",
        nargs="*",
        choices=["north_america", "europe", "asia", "global"],
        metavar="REGION",
        help="limit to these regions")
    parser.add_argument(
        "-s", "--sec-types",
        nargs="*",
        choices=["STK", "ETF", "FUT", "CASH", "IND"],
        metavar="SEC_TYPE",
        help="limit to these security types")
    parser.set_defaults(func="quantrocket.master._cli_list_exchanges")

    examples = """
Specify an exchange (optionally filtering by security type, currency, and/or symbol) to fetch
listings from the IB website and pull associated contract details from the IB API. Or, specify universes
or conids to pull details from the IB API, bypassing the website.

Examples:
Pull all Toronto Stock Exchange stocks listings:

    quantrocket master listings --exchange TSE --sec-types STK

Pull all NYSE ARCA ETF listings:

    quantrocket master listings --exchange ARCA --sec-types ETF

Pull specific symbols from Nasdaq (ISLAND):

    quantrocket master listings --exchange ISLAND --symbols AAPL GOOG NFLX

Re-pull contract details for an existing universe called "japan-fin":

    quantrocket master listings --universes "japan-fin"
    """
    parser = _subparsers.add_parser(
        "listings",
        help="pull securities listings from IB into securities master database, either by "
        "exchange or by universes/conids",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "-e", "--exchange",
        metavar="EXCHANGE",
        help="the exchange code to pull listings for (required unless providing universes "
        "or conids)")
    parser.add_argument(
        "-t", "--sec-types",
        nargs="*",
        metavar="SEC_TYPE",
        choices=["STK", "ETF", "FUT", "CASH", "IND"],
        help="limit to these security types")
    parser.add_argument(
        "-c", "--currencies",
        nargs="*",
        metavar="CURRENCY",
        help="limit to these currencies")
    parser.add_argument(
        "-s", "--symbols",
        nargs="*",
        metavar="SYMBOL",
        help="limit to these symbols")
    parser.add_argument(
        "-u", "--universes",
        nargs="*",
        metavar="UNIVERSE",
        help="limit to these universes")
    parser.add_argument(
        "-i", "--conids",
        nargs="*",
        metavar="CONID",
        help="limit to these conids")
    parser.set_defaults(func="quantrocket.master._cli_pull_listings")

    query_parent_parser = argparse.ArgumentParser(add_help=False)
    filters = query_parent_parser.add_argument_group("filtering options")
    filters.add_argument(
        "-e", "--exchanges",
        nargs="*",
        metavar="EXCHANGE",
        help="limit to these exchanges")
    filters.add_argument(
        "-t", "--sec-types",
        nargs="*",
        metavar="SEC_TYPE",
        choices=["STK", "ETF", "FUT", "CASH", "IND"],
        help="limit to these security types")
    filters.add_argument(
        "-c", "--currencies",
        nargs="*",
        metavar="CURRENCY",
        help="limit to these currencies")
    filters.add_argument(
        "-u", "--universes",
        nargs="*",
        metavar="UNIVERSE",
        help="limit to these universes")
    filters.add_argument(
        "-s", "--symbols",
        nargs="*",
        metavar="SYMBOL",
        help="limit to these symbols")
    filters.add_argument(
        "-i", "--conids",
        nargs="*",
        metavar="CONID",
        help="limit to these conids")
    filters.add_argument(
        "--exclude-universes",
        nargs="*",
        metavar="UNIVERSE",
        help="exclude these universes")
    filters.add_argument(
        "--exclude-conids",
        nargs="*",
        metavar="CONID",
        help="exclude these conids")
    filters.add_argument(
        "--sectors",
        nargs="*",
        metavar="SECTOR",
        help="limit to these sectors")
    filters.add_argument(
        "--industries",
        nargs="*",
        metavar="INDUSTRY",
        help="limit to these industries")
    filters.add_argument(
        "--categories",
        nargs="*",
        metavar="CATEGORY",
        help="limit to these categories")
    filters.add_argument(
        "-d", "--delisted",
        action="store_true",
        default=False,
        help="include delisted securities")

    examples = """
Examples:
Download a CSV of all securities in a universe called "mexi-fut" to a file called mexi.csv:

    quantrocket master get --universes "mexi-fut" -o mexi.csv

Download a CSV of all ARCA ETFs and use it to create a universe called "arca-etf":

    quantrocket master get --exchanges ARCA --sec-types ETF | quantrocket master universe "arca-etf" --infile -

Pretty print the exchange and currency for all listings of AAPL:

    quantrocket master get --symbols AAPL --fields PrimaryExch Currency --pretty
    """
    parser = _subparsers.add_parser(
        "get",
        help="query security details from the securities master database and download to file",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter, parents=[query_parent_parser])
    outputs = parser.add_argument_group("output options")
    outputs.add_argument(
        "-o", "--outfile",
        metavar="OUTFILE",
        dest="filepath_or_buffer",
        help="filename to write the data to (default is stdout)")
    output_format_group = outputs.add_mutually_exclusive_group()
    output_format_group.add_argument(
        "-j", "--json",
        action="store_const",
        const="json",
        dest="output",
        help="format output as JSON (default is CSV)")
    output_format_group.add_argument(
        "-p", "--pretty",
        action="store_const",
        const="txt",
        dest="output",
        help="format output in human-readable format (default is CSV)")
    outputs.add_argument(
        "-f", "--fields",
        metavar="FIELD",
        nargs="*",
        help="only return these fields")
    parser.set_defaults(func="quantrocket.master._cli_download_securities_file")

    examples = """
Examples:
Get conids of all ARCA ETFs:

    quantrocket master conids --exchanges ARCA --sec-types ETF

Get conids of all consumer cyclicals trading on the Australian Stock Exchange:

    quantrocket master conids --exchanges ASX --sectors "Consumer, Cyclical"
    """
    parser = _subparsers.add_parser(
        "conids",
        help="query conids from the securities master database",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[query_parent_parser])
    parser.set_defaults(func="quantrocket.master._cli_get_conids")

    examples = """
Examples:
Get a diff for all securities in a universe called "italy-stk":

    quantrocket master diff --universes "italy-stk"

Get a diff for all securities in a universe called "italy-stk", looking only for sector or
industry changes:

    quantrocket master diff -u "italy-stk" --fields Sector Industry

Get a diff for specific securities by conid:

    quantrocket master diff --conids 123456 234567

Get a diff for all securities in a universe called "italy-stk" and log the results, if any,
to flightlog:

    quantrocket master diff -u "italy-stk" | quantrocket flightlog log --loglevel WARNING --name "quantrocket.master"

Get a diff for all securities in a universe called "nasdaq-sml" and auto-delist any symbols that
are no longer available from IB or that are now associated with the PINK exchange:

    quantrocket master diff -u "nasdaq-sml" --delist-missing --delist-exchanges PINK
    """
    parser = _subparsers.add_parser(
        "diff",
        help="flag security details that have changed in IB's system since the time "
        "they were last loaded into the securities master database",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "-u", "--universes",
        nargs="*",
        metavar="UNIVERSE",
        help="limit to these universes")
    parser.add_argument(
        "-i", "--conids",
        nargs="*",
        metavar="CONID",
        help="limit to these conids")
    parser.add_argument(
        "-f", "--fields",
        nargs="*",
        metavar="FIELD",
        help="only diff these fields")
    parser.add_argument(
        "--delist-missing",
        action="store_true",
        default=False,
        help="auto-delist securities that are no longer available from IB")
    parser.add_argument(
        "--delist-exchanges",
        metavar="EXCHANGE",
        nargs="*",
        help="auto-delist securities that are associated with these exchanges")
    parser.set_defaults(func="quantrocket.master._cli_diff_securities")

    examples = """
Examples:
Download a CSV of Italian stocks then upload it to create a universe called "italy-stk":

    quantrocket master get --exchanges BVME --sec-types STK -f italy.csv
    quantrocket master universe "italy-stk" -f italy.csv

In one line, download a CSV of all ARCA ETFs and append to a universe called "arca-etf":

    quantrocket master get --exchanges ARCA --sec-types ETF | quantrocket master universe "arca-etf" --append --infile -

Create a universe consisting of several existing universes:

    quantrocket master universe "asx" --from-universes "asx-sml" "asx-mid" "asx-lrg"

Copy a universe but exclude delisted securities:

    quantrocket master universe "hong-kong-active" --from-universes "hong-kong" --exclude-delisted
    """
    parser = _subparsers.add_parser(
        "universe",
        help="create a universe of securities",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "code",
        metavar="CODE",
        help="the code to assign to the universe (lowercase alphanumerics and hyphens only)")
    parser.add_argument(
        "-f", "--infile",
        metavar="INFILE",
        help="create the universe from the conids in this file (specify '-' to read file "
        "from stdin)")
    parser.add_argument(
        "--from-universes",
        nargs="*",
        metavar="UNIVERSE",
        help="create the universe from these existing universes")
    parser.add_argument(
        "--exclude-delisted",
        action="store_true",
        dest="exclude_delisted",
        help="exclude delisted securities that would otherwise be included (default is to "
        "include them)")
    on_conflict_group = parser.add_mutually_exclusive_group()
    on_conflict_group.add_argument(
        "-a", "--append",
        action="store_true",
        help="append to universe if universe already exists")
    on_conflict_group.add_argument(
        "-r", "--replace",
        action="store_true",
        help="replace universe if universe already exists")
    parser.set_defaults(func="quantrocket.master._cli_create_universe")

    examples = """
Examples:
Delete the universe called "italy-stk" (the listings details of the member securities won't
be deleted, only their grouping as a universe):

    quantrocket master delete-universe "italy-stk"
    """
    parser = _subparsers.add_parser(
        "delete-universe",
        help="delete a universe (the listings details of the member securities won't "
        "be deleted, only their grouping as a universe)",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "code",
        help="the universe code")
    parser.set_defaults(func="quantrocket.master._cli_delete_universe")

    parser = _subparsers.add_parser("frontmonth", help="return the frontmonth contract for a futures underlying, as of now or over a date range")
    parser.add_argument("symbol", help="the underlying's symbol (e.g. ES)")
    parser.add_argument("exchange", help="the exchange where the contract trades (e.g. GLOBEX)")
    parser.add_argument("-c", "--currency", metavar="CURRENCY", help="the contract's currency, if necessary to disambiguate")
    parser.add_argument("-m", "--multiplier", metavar="MULTIPLIER", help="the contract's multiplier, if necessary to disambiguate")
    parser.add_argument("-s", "--start-date", metavar="YYYY-MM-DD", help="return the frontmonth conid for each date on or after this date")
    parser.add_argument("-e", "--end-date", metavar="YYYY-MM-DD", help="return the frontmonth conid for each date on or before this date")
    parser.set_defaults(func="quantrocket.master.get_frontmonth")

    examples = """
Examples:
Upload a new rollover config (replaces current config):

    quantrocket master rollrules myrolloverrules.yml

Show current rollover config:

    quantrocket master rollrules
    """
    parser = _subparsers.add_parser(
        "rollrules",
        help="upload a new rollover rules config, or return the current rollover rules",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "filename",
        nargs="?",
        metavar="FILENAME",
        help="the rollover rules config file to upload (if omitted, return the current config)")
    parser.set_defaults(func="quantrocket.master._cli_load_or_show_rollrules")

    parser = _subparsers.add_parser("delist", help="delist a security by con_id or symbol+exchange")
    parser.add_argument("-c", "--conid", type=int, help="the conid of the security to delist")
    parser.add_argument("-s", "--symbol", help="the symbol to be delisted")
    parser.add_argument("-e", "--exchange", help="the exchange of the symbol to be delisted")
    parser.set_defaults(func="quantrocket.master.delist")

    parser = _subparsers.add_parser("lots", help="load lot sizes from a file")
    parser.add_argument("filename", metavar="FILE", help="CSV file with columns 'lot_size' and either 'conid' or 'symbol' (and optionally 'exchange' and/or 'currency' for disambiguation)")
    parser.add_argument("-u", "--universes", metavar="UNIVERSE", help="only try to match to securities in these universes (to prevent false matches in case of symbol ambiguity)")
    parser.set_defaults(func="quantrocket.master.load_lots")
