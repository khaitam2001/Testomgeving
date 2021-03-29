from rdbconnection import conrdb
rdbcon, rdbcur = conrdb()

createTableQuery = """
    DROP TABLE IF EXISTS similarprofilerecommendations;
    
    CREATE TABLE similarprofilerecommendations (
        givenprofile varchar(255),
        commonproduct1 varchar(255),
        commonproduct2 varchar(255),
        commonproduct3 varchar(255),
        commonproduct4 varchar(255),
        PRIMARY KEY(givenprofile),
        FOREIGN KEY (commonproduct1)
            REFERENCES PRODUCT (product_id),
        FOREIGN KEY (commonproduct2)
            REFERENCES PRODUCT (product_id),
        FOREIGN KEY (commonproduct3)
            REFERENCES PRODUCT (product_id),
        FOREIGN KEY (commonproduct4)
            REFERENCES PRODUCT (product_id)
    );
"""

rdbcur.execute(createTableQuery)
rdbcon.commit()
rdbcur.close()