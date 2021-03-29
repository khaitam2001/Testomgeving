from rdbconnection import conrdb

rdbcon, rdbcur = conrdb()

def getAllProfileIDs():
    """ Return alle profile_ids in de database """
    select_profileIDs_query = "SELECT profile_id FROM profile"
    rdbcur.execute(select_profileIDs_query)
    return rdbcur.fetchall()


def getSessionIDFromOrder(productID=None):
    """ Return alle sessionIDs van de tabel Order. Als er een productID wordt ingevoerd, dan wordt er gezocht naar alle
    sessions die bij de product hoort."""
    if productID == None:
        select_orderID_query = "SELECT session_id FROM orders"
        rdbcur.execute(select_orderID_query)
    else:
        select_orderID_query = "SELECT session_id FROM orders WHERE product_id = %s"
        rdbcur.execute(select_orderID_query, (productID,))
    return rdbcur.fetchall()


def getProductIDFromOrder(SessionID=None):
    """ Return alle productIDs van de tabel "Order". Als er een sessionID wordt ingevoerd, dan wordt er gezocht naar de
    producten die bij die specifieke sessionID hoort."""
    if SessionID == None:
        select_productID_query = "SELECT product_id FROM orders"
        rdbcur.execute(select_productID_query)
    else:
        select_productID_query = "SELECT product_id FROM orders WHERE session_id = %s"
        rdbcur.execute(select_productID_query, (SessionID,))
    return rdbcur.fetchall()


def getBrowserIDFromBUIDS():
    pass


# print(getAllProfileIDs())

test_profile_id = '5a393eceed295900010386a8'