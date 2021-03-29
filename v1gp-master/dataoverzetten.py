from rdbconnection import conrdb

rdbcon, rdbcur = conrdb()

def getAllProfileIDs():
    """
    :return: Een lijst met alle ProfileIDs van de database
    """
    select_profileIDs_query = "SELECT profile_id FROM profile"
    rdbcur.execute(select_profileIDs_query)
    return rdbcur.fetchall()


def getSessionIDFromOrder(productID=None):
    """
    :param productID: str
    :return: Een lijst met sessionIDs die bij de gegeven productID hoort.
    """
    if productID == None:
        pass
    else:
        select_orderID_query = "SELECT session_id FROM orders WHERE product_id = %s"
        rdbcur.execute(select_orderID_query, (productID,))
    return rdbcur.fetchall()


def getProductIDFromOrder(sessionID=None):
    """
    :param sessionID: str
    :return: Een lijst met productIDs die bij de gegeven sessionID hoort.
    """
    if sessionID == None:
        pass
    else:
        select_productID_query = "SELECT product_id FROM orders WHERE session_id = %s"
        rdbcur.execute(select_productID_query, (sessionID,))
    return rdbcur.fetchall()


def getBrowserIDFromBUIDS(profileID=None):
    """
    :param profileID:str
    :return: Lijst met browser_ids die bij de gegeven profileID hoort.
    """
    if profileID == None:
        pass
    else:
        select_buids_query = "SELECT browser_id FROM buids WHERE profile_id = %s"
        rdbcur.execute(select_buids_query, (profileID,))
    return rdbcur.fetchall()


def getSessionIDFromSessions(browserID=None):
    """
    :param browserID:str
    :return: Lijst met sessionIDs die bij de gegeven browserID hoort.
    """
    if browserID == None:
        pass
    else:
        select_sessions_query = "SELECT session_id FROM sessions WHERE browser_id = %s"
        rdbcur.execute(select_sessions_query, (browserID,))
    return rdbcur.fetchall()


def getBoughtProducts(profileID):
    """
    :param profileID:str
    :return: Lijst met producten die gekocht zijn door de gegeven profileID
    """
    # Hier zoeken we de browserID(s) die horen bij een gegeven profiel
    browser_ids = getBrowserIDFromBUIDS(profileID)
    session_ids = []
    product_ids = []

    # Er kunnen meer browser_id's zijn. Daarom hebben we hiervoor een for-loop. We zoeken hier alle session ID(s) op die
    # bij de gegeven browser_id(s) horen.
    for browser_id in browser_ids:
        temp_session_ids = (getSessionIDFromSessions(browser_id[0]))
        for session_id in temp_session_ids:
            session_ids.append(session_id[0])

    # Er kunnen meer session_id's zijn. Daarom hebben we hiervoor een for-loop. We zoeken hier alle product ID(s) op die
    # bij de gegeven session_id(s) horen
    for session in session_ids:
        temp_products = getProductIDFromOrder(session)
        for product in temp_products:
            product_ids.append(product[0])

    return product_ids


print(getBoughtProducts('5a393eceed295900010386a8'))

test_profile_id = '5a393eceed295900010386a8'