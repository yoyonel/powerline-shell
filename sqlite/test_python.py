#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sqlite3


class Mabase():

    def __init__(self):
        """
        """
        self.conn = sqlite3.connect('pls.db')

    @staticmethod
    def query_create_table(table_name, table_columns):
        query = "create table " + table_name + '('
        # url: https://docs.python.org/2/library/functions.html#map
        query += reduce(lambda x, y: "{}, {}".format(x, y), table_columns[:-1])
        return query + ',' + table_columns[-1] + ')'

    def creer(self):
        """ Créer une simple base.
                Renvoi True si reussie, False si déjà créée. """

        # Obtention d'un curseur
        c = self.conn.cursor()

        # Créer une table
        try:
            # urls: 
            # - https://docs.python.org/2/library/sqlite3.html#sqlite3.Cursor.executescript
            # - http://www.w3schools.com/sql/sql_datatypes_general.asp
            c.executescript("""
                create table docker(
                    uuid_system VARCHAR(36),
                    time        VARCHAR(256),
                    segments    VARCHAR(256),
                    PRIMARY KEY (uuid_system)
                );

                create table ros(
                    uuid_system VARCHAR(36),
                    bashid      INTEGER,
                    time        VARCHAR(256),
                    reachable   BOOLEAN,
                    topics      INTEGER,
                    nodes       INTEGER,
                    PRIMARY KEY (uuid_system, bashid)
                );

                insert into docker values ( "n72b2a5d5-1c51-4d81-8989-335ac1729c0e",
                                            5951,
                                            "🐳  × 64"
                                        );

                insert into ros values ( "n72b2a5d5-1c51-4d81-8989-335ac1729c0e",
                                            5951,
                                            "time",
                                            1,
                                            5,
                                            2
                                        );
                """)

            # Sauvegarder les modifications
            self.conn.commit()

            # Fermer le curseur
            c.close()
            print "Création de la base réussie."
            return True

        except:
            # Fermer le curseur
            c.close()
            return False

    def lire(self):
        """ """
        c = self.conn.cursor()

        try:
            c.execute("SELECT * FROM docker")
            for row in c:
                print row
        except Exception, e: 
            print("Exception: ", e)

        try:
            c.execute("SELECT * FROM ros")
            for row in c:
                print row
        except Exception, e: 
            print("Exception: ", e)

        c.close()

# Création de l'instance de classe
mabase = Mabase()
if not mabase.creer():  # Si la méthode creer() renvoi False, lire la base
    mabase.lire()
