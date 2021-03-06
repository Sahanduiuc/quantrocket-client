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

import getpass
from quantrocket.houston import houston
from quantrocket.cli.utils.output import json_to_cli

def list_databases(services=None, codes=None, detail=False, expand=False,
                   service=None):
    """
    List databases.

    Parameters
    ----------
    services : str, optional
        limit to these services

    codes: list of str, optional
        limit to these codes

    detail : bool
        return database statistics (default is to return a
        flat list of database names)

    expand : bool
        expand sharded databases to include individual shards
        (default is to list sharded databases as a single database)

    service : str
        DEPRECATED, this option will be removed in a future release, please use
        `services` instead (previously only a single service could be specified but
        now multiple services can be specified)

    Returns
    -------
    dict
        dict of lists of databases (one key for PostgreSQL databases and one for
        SQLite databases)

    Examples
    --------
    Load database details in a pandas DataFrame:

    >>> from quantrocket.db import list_databases
    >>> import itertools
    >>> databases = list_databases(detail=True)
    >>> databases = pd.DataFrame.from_records(itertools.chain(databases["sqlite"], databases["postgres"]))
    """
    params = {}
    if services:
        params["services"] = services
    if codes:
        params["codes"] = codes
    if detail:
        params["detail"] = detail
    if expand:
        params["expand"] = expand
    if service:
        import warnings
        # DeprecationWarning is ignored by default but we want the user
        # to see it
        warnings.simplefilter("always", DeprecationWarning)
        warnings.warn(
            "the `service` option is deprecated and will be removed in a "
            "future release, please use `services` instead (previously only "
            "a single service could be specified but now multiple services can "
            "be specified)", DeprecationWarning)
        params["services"] = service

    response = houston.get("/db/databases", params=params)
    houston.raise_for_status_with_json(response)
    return response.json()

def _cli_list_databases(*args, **kwargs):
    service_and_codes = kwargs.pop("service_and_codes", None)
    if service_and_codes:
        import warnings
        # DeprecationWarning is ignored by default but we want the user
        # to see it
        warnings.simplefilter("always", DeprecationWarning)
        warnings.warn(
            "passing positional arguments is deprecated and will be removed in a "
            "future release, please use `--services` and `--codes` instead",
            DeprecationWarning)
        kwargs["services"] = service_and_codes[0]
        kwargs["codes"] = service_and_codes[1:]
    return json_to_cli(list_databases, *args, **kwargs)

def download_database(database, outfile):
    """
    [DEPRECATED] Download a database from the db service and write to a local file.

    This function is deprecated. Please use `docker cp` to download databases.

    Parameters
    ----------
    database : str, required
        the filename of the database (as returned by the list_databases)

    outfile: str, required
        filename to write the database to

    Returns
    -------
    None
    """
    import warnings
    # DeprecationWarning is ignored by default but we want the user
    # to see it
    warnings.simplefilter("always", DeprecationWarning)
    warnings.warn(
        "this function is deprecated and will be removed in a "
        "future release, please use `docker cp` to download databases",
        DeprecationWarning)
    response = houston.get("/db/databases/{0}".format(database), stream=True)
    houston.raise_for_status_with_json(response)
    with open(outfile, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

def _cli_download_database(*args, **kwargs):
    return json_to_cli(download_database, *args, **kwargs)

def get_s3_config():
    """
    Return the current S3 configuration, if any.

    See http://qrok.it/h/dbs3 to learn more.

    Returns
    -------
    dict
        configuration details
    """
    response = houston.get("/db/s3config")
    houston.raise_for_status_with_json(response)
    # It's possible to get a 204 empty response
    if not response.content:
        return {}
    return response.json()

def set_s3_config(access_key_id=None, secret_access_key=None, bucket=None):
    """
    Set AWS S3 configuration for pushing and pulling databases to and from
    S3.

    See http://qrok.it/h/dbs3 to learn more.

    Parameters
    ----------
    access_key_id : str, optional
        AWS access key ID

    secret_access_key : str, optional
        AWS secret access key (if omitted and access_key_id is provided,
        will be prompted for secret_access_key)

    bucket : str, optional
        the S3 bucket name to push to/pull from

    Returns
    -------
    dict
        status message
    """
    if access_key_id and not secret_access_key:
        secret_access_key = getpass.getpass(prompt="Enter AWS Secret Access Key: ")

    data = {}
    if access_key_id:
        data["access_key_id"] = access_key_id
    if secret_access_key:
        data["secret_access_key"] = secret_access_key
    if bucket:
        data["bucket"] = bucket

    response = houston.put("/db/s3config", data=data)
    houston.raise_for_status_with_json(response)
    return response.json()

def _cli_get_or_set_s3_config(access_key_id=None, secret_access_key=None,
                                   bucket=None, *args, **kwargs):
    if access_key_id or secret_access_key or bucket:
        return json_to_cli(set_s3_config, access_key_id, secret_access_key, bucket, *args, **kwargs)
    else:
        return json_to_cli(get_s3_config, *args, **kwargs)

def s3_push_databases(services=None, codes=None):
    """
    Push database(s) to Amazon S3.

    See http://qrok.it/h/dbs3 to learn more.

    Parameters
    ----------
    serivces : list of str, optional
        limit to these services

    codes: list of str, optional
        limit to these codes

    Returns
    -------
    json
        status message
    """
    params = {}
    if services:
        params["services"] = services
    if codes:
        params["codes"] = codes
    response = houston.put("/db/s3", params=params)
    houston.raise_for_status_with_json(response)
    return response.json()

def _cli_s3_push_databases(*args, **kwargs):
    service_and_codes = kwargs.pop("service_and_codes", None)
    if service_and_codes:
        import warnings
        # DeprecationWarning is ignored by default but we want the user
        # to see it
        warnings.simplefilter("always", DeprecationWarning)
        warnings.warn(
            "passing positional arguments is deprecated and will be removed in a "
            "future release, please use `--services` and `--codes` instead",
            DeprecationWarning)
        kwargs["services"] = service_and_codes[0]
        kwargs["codes"] = service_and_codes[1:]
    return json_to_cli(s3_push_databases, *args, **kwargs)

def s3_pull_databases(services=None, codes=None, force=False):
    """
    Pull database(s) from Amazon S3.

    See http://qrok.it/h/dbs3 to learn more.

    Parameters
    ----------
    serivces : list of str, optional
        limit to these services

    codes: list of str, optional
        limit to these codes

    force: bool
        overwrite existing database if one exists (default is to
        fail if one exists)

    Returns
    -------
    json
        status message
    """
    params = {}
    if services:
        params["services"] = services
    if codes:
        params["codes"] = codes
    if force:
        params["force"] = force
    response = houston.get("/db/s3", params=params)
    houston.raise_for_status_with_json(response)
    return response.json()

def _cli_s3_pull_databases(*args, **kwargs):
    service_and_codes = kwargs.pop("service_and_codes", None)
    if service_and_codes:
        import warnings
        # DeprecationWarning is ignored by default but we want the user
        # to see it
        warnings.simplefilter("always", DeprecationWarning)
        warnings.warn(
            "passing positional arguments is deprecated and will be removed in a "
            "future release, please use `--services` and `--codes` instead",
            DeprecationWarning)
        kwargs["services"] = service_and_codes[0]
        kwargs["codes"] = service_and_codes[1:]
    return json_to_cli(s3_pull_databases, *args, **kwargs)

def optimize_databases(services=None, codes=None):
    """
    Optimize databases to improve performance.

    This runs the 'VACUUM' command, which defragments the database and
    reclaims disk space.

    Parameters
    ----------
    serivces : list of str, optional
        limit to these service

    codes: list of str, optional
        limit to these codes

    Returns
    -------
    json
        status message
    """
    params = {}
    if codes:
        params["codes"] = codes
    if services:
        params["services"] = services
    response = houston.post("/db/optimizations", params=params)
    houston.raise_for_status_with_json(response)
    return response.json()

def _cli_optimize_databases(*args, **kwargs):
    service_and_codes = kwargs.pop("service_and_codes", None)
    if service_and_codes:
        import warnings
        # DeprecationWarning is ignored by default but we want the user
        # to see it
        warnings.simplefilter("always", DeprecationWarning)
        warnings.warn(
            "passing positional arguments is deprecated and will be removed in a "
            "future release, please use `--services` and `--codes` instead",
            DeprecationWarning)
        kwargs["services"] = service_and_codes[0]
        kwargs["codes"] = service_and_codes[1:]
    return json_to_cli(optimize_databases, *args, **kwargs)
