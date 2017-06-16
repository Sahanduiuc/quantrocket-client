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

import sys
import six
from quantrocket.houston import houston
from quantrocket.cli.utils.output import json_to_cli
from quantrocket.cli.utils.stream import stream

def list_exchanges(regions=None, sec_types=None):
    """
    List exchanges by security type and country as found on the IB website.

    Parameters
    ----------
    regions : list of str, optional
        limit to these regions. Possible choices: north_america, europe, asia, global

    sec_types : list of str, optional
        limit to these securitiy types. Possible choices: STK, ETF, FUT, CASH, IND

    Returns
    -------
    dict
    """
    params = {}
    if sec_types:
        params["sec_types"] = sec_types
    if regions:
        params["regions"] = regions

    response = houston.get("/master/exchanges", params=params)
    return houston.json_if_possible(response)

def _cli_list_exchanges(*args, **kwargs):
    return json_to_cli(list_exchanges, *args, **kwargs)

def pull_listings(exchange=None, sec_types=None, currencies=None, symbols=None,
                        groups=None, conids=None):
    """
    Pull securities listings from IB into securities master database, either by exchange or by groups/conids.


    Specify an exchange (optionally filtering by security type, currency, and/or symbol) to fetch
    listings from the IB website and pull associated contract details from the IB API. Or, specify groups
    or conids to pull details from the IB API, bypassing the website.

    Parameters
    ----------
    exchange : str
        the exchange code to pull listings for (required unless providing groups or conids)

    sec_types : list of str, optional
        limit to these security types. Possible choices: STK, ETF, FUT, CASH, IND

    currencies : list of str, optional
        limit to these currencies

    symbols : list of str, optional
        limit to these symbols

    groups : list of str, optional
        limit to these groups

    conids : list of int, optional
        limit to these conids

    Returns
    -------
    dict
        status message

    """
    params = {}
    if exchange:
        params["exchange"] = exchange
    if sec_types:
        params["sec_types"] = sec_types
    if currencies:
        params["currencies"] = currencies
    if symbols:
        params["symbols"] = symbols
    if groups:
        params["groups"] = groups
    if conids:
        params["conids"] = conids

    response = houston.post("/master/listings", params=params)
    return houston.json_if_possible(response)

def _cli_pull_listings(*args, **kwargs):
    return json_to_cli(pull_listings, *args, **kwargs)

def diff_securities(groups=None, conids=None, fields=None, delist_missing=False,
                    delist_exchanges=None):
    """
    Flag security details that have changed in IB's system since the time they were last loaded
    into the securities master database.

    Parameters
    ----------
    groups : list of str, optional
        limit to these groups

    conids : list of int, optional
        limit to these conids

    fields : list of str, optional
        only diff these fields

    delist_missing : bool
        auto-delist securities that are no longer available from IB

    delist_exchanges : list of str, optional
        auto-delist securities that are associated with these exchanges

    Returns
    -------
    dict
        dict of conids and fields that have changed

    """
    params = {}
    if groups:
        params["groups"] = groups
    if conids:
        params["conids"] = conids
    if fields:
        params["fields"] = fields
    if delist_missing:
        params["delist_missing"] = delist_missing
    if delist_exchanges:
        params["delist_exchanges"] = delist_exchanges

    # runs synchronously so use a high timeout
    response = houston.get("/master/diff", params=params, timeout=60*60)
    return houston.json_if_possible(response)

def _cli_diff_securities(*args, **kwargs):
    return json_to_cli(diff_securities, *args, **kwargs)

def download_securities_file(filepath_or_buffer=None, output="csv", exchanges=None, sec_types=None,
                             currencies=None, groups=None, symbols=None, conids=None,
                             exclude_groups=None, exclude_conids=None,
                             sectors=None, industries=None, categories=None,
                             delisted=False):
    """
    Query security details from the securities master database and download to file.

    Parameters
    ----------
    filepath_or_buffer : str or file-like object
        filepath to write the data to, or file-like object (defaults to stdout)

    output : str
        output format (json or csv, default is csv)

    exchanges : list of str, optional
        limit to these exchanges

    sec_types : list of str, optional
        limit to these security types. Possible choices: STK, ETF, FUT, CASH, IND

    currencies : list of str, optional
        limit to these currencies

    groups : list of str, optional
        limit to these groups

    symbols : list of str, optional
        limit to these symbols

    conids : list of int, optional
        limit to these conids

    exclude_groups : list of str, optional
        exclude these groups

    exclude_conids : list of int, optional
        exclude these conids

    sectors : list of str, optional
        limit to these sectors

    industries : list of str, optional
        limit to these industries

    categories : list of str, optional
        limit to these categories

    delisted : bool
        include delisted securities (default False)

    Returns
    -------
    None

    Examples
    --------
    You can use StringIO to load the CSV into pandas.

    >>> f = io.StringIO()
    >>> download_securities_file(f, groups=["my-group"])
    >>> securities = pd.read_csv(f)
    """
    params = {}
    if exchanges:
        params["exchanges"] = exchanges
    if sec_types:
        params["sec_types"] = sec_types
    if currencies:
        params["currencies"] = currencies
    if groups:
        params["groups"] = groups
    if symbols:
        params["symbols"] = symbols
    if conids:
        params["conids"] = conids
    if exclude_groups:
        params["exclude_groups"] = exclude_groups
    if exclude_conids:
        params["exclude_conids"] = exclude_conids
    if sectors:
        params["sectors"] = sectors
    if industries:
        params["industries"] = industries
    if categories:
        params["categories"] = categories
    if delisted:
        params["delisted"] = delisted

    output = output or "csv"

    if output not in ("csv", "json"):
        raise ValueError("Invalid ouput: {0}".format(output))

    response = houston.get("/master/securities.{0}".format(output), params=params)

    filepath_or_buffer = filepath_or_buffer or sys.stdout

    if hasattr(filepath_or_buffer, "write"):
        mode = getattr(filepath_or_buffer, "mode", "w")
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                if "b" not in mode and six.PY3:
                    chunk = chunk.decode("utf-8")
                filepath_or_buffer.write(chunk)
        filepath_or_buffer.seek(0)
    else:
        with open(filepath_or_buffer, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

def get_conids(exchanges=None, sec_types=None, currencies=None,
               groups=None, symbols=None, conids=None,
               exclude_groups=None, exclude_conids=None,
               sectors=None, industries=None, categories=None,
               delisted=False):
    """
    Query conids from the securities master database.

    Parameters
    ----------
    exchanges : list of str, optional
        limit to these exchanges

    sec_types : list of str, optional
        limit to these security types. Possible choices: STK, ETF, FUT, CASH, IND

    currencies : list of str, optional
        limit to these currencies

    groups : list of str, optional
        limit to these groups

    symbols : list of str, optional
        limit to these symbols

    conids : list of int, optional
        limit to these conids

    exclude_groups : list of str, optional
        exclude these groups

    exclude_conids : list of int, optional
        exclude these conids

    sectors : list of str, optional
        limit to these sectors

    industries : list of str, optional
        limit to these industries

    categories : list of str, optional
        limit to these categories

    delisted : bool
        include delisted securities (default False)

    Returns
    -------
    list
        list of conids

    """
    params = {}
    if exchanges:
        params["exchanges"] = exchanges
    if sec_types:
        params["sec_types"] = sec_types
    if currencies:
        params["currencies"] = currencies
    if groups:
        params["groups"] = groups
    if symbols:
        params["symbols"] = symbols
    if conids:
        params["conids"] = conids
    if exclude_groups:
        params["exclude_groups"] = exclude_groups
    if exclude_conids:
        params["exclude_conids"] = exclude_conids
    if sectors:
        params["sectors"] = sectors
    if industries:
        params["industries"] = industries
    if categories:
        params["categories"] = categories
    if delisted:
        params["delisted"] = delisted

    response = houston.get("/master/securities/conids", params=params)
    return houston.json_if_possible(response)

def _cli_get_conids(*args, **kwargs):
    return json_to_cli(get_conids, *args, **kwargs)