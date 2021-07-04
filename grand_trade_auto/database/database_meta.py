#!/usr/bin/env python3
"""
Holds the generic database meta-class that others will subclass.  Any other
shared database code that needs to be accessed by all databases can be
implemented here so they have access when this is imported.

Module Attributes:
  N/A

(C) Copyright 2020 Jonathan Casey.  All Rights Reserved Worldwide.
"""
from abc import ABC, abstractmethod



class Database(ABC):
    """
    The abstract class for all database functionality.  Each database type
    will subclass this, but externally will likely only call the generic methods
    defined here to unify the interface.

    Class Attributes:
      N/A

    Instance Attributes:
      env (str): The run environment type valid for using this database.
      cp_db_id (str): The id used as the section name in the database conf.
        Will be used for loading credentials on-demand.
      cp_secrets_id (str): The id used as the section name in the secrets
        conf.  Will be used for loading credentials on-demand.
      host (str): The host URL.
      post (int): The port number on that host for accessing the database.
      database (str): The database to open.
    """
    def __init__(self, env, cp_db_id, cp_secrets_id,
            host, port, database):             # pylint: disable=unused-argument
        """
        Creates the database handle.

        Args:
          env (str): The run environment type valid for using this database.
          cp_db_id (str): The id used as the section name in the database conf.
            Will be used for loading credentials on-demand.
          cp_secrets_id (str): The id used as the section name in the secrets
            conf.  Will be used for loading credentials on-demand.
          host (str): The host URL.
          post (int): The port number on that host for accessing the database.
          database (str): The database to open.
        """
        self._env = env
        self._cp_db_id = cp_db_id
        self._cp_secrets_id = cp_secrets_id



    def matches_id_criteria(self, db_id, env=None, db_type=None):
        """
        Checks if this database is a match based on the provided criteria.

        Can provide more beyond minimum required parameters to explicitly
        overdefine.  No matter how minimally or overly defined inputs are, all
        non-None must match.

        Args:
          db_id (str): The section ID of the database from the databases.conf
            file to check if this matches.
          env (str or None): The environment for which to check if this matches.
          db_type (str or None): The type to check if this matches.


        Returns:
          (bool): True if all provided criteria match; False otherwise.

        Raises:
          (AssertionError): Raised when an invalid combination of input arg
            criteria provided cannot guarantee a minimum level of definition.
        """
        assert db_id is not None
        if db_id != self._cp_db_id:
            return False
        if env is not None and env != self._env:
            return False
        if db_type is not None and db_type not in self.get_type_names():
            return False
        return True



    @classmethod
    @abstractmethod
    def load_from_config(cls, db_cp, db_id, secrets_id):
        """
        Loads the database config for this database from the configparsers
        from files provided.

        Args:
          db_cp (configparser): The full configparser from the database conf.
          db_id (str): The ID name for this database as it appears as the
            section header in the db_cp.
          secrets_id (str): The ID name for this database's secrets as it
            appears as the section header in the secrets_cp.

        Returns:
          db_handle (Database<>): The Database<> object created and loaded from
            config, where Database<> is a subclass of Database (e.g. Postgres).
        """



    @classmethod
    @abstractmethod
    def get_type_names(cls):
        """
        Get the list of names that can be used as the 'type' in the database
        conf to identify this database.

        Returns:
          ([str]): A list of names that are valid to use for this database type.
        """



    @abstractmethod
    def create_db(self):
        """
        Creates the database specified as the database to use in this object.
        If it already exists, skips.
        """
