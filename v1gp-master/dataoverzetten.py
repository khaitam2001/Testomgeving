from rdbconnection import conrdb

rdbcon, rdbcur = conrdb()

def getProfileIDs(browser_id=None):
    """
    :param browser_id: str, Als het leeg is dan zoeken we naar alle profielen.
    :return: Een lijst met alle ProfileIDs van de database. Dit komt van de tabel profile.
    """
    select_profileIDs_query = "SELECT profile_id FROM profile"
    rdbcur.execute(select_profileIDs_query)
    return rdbcur.fetchall()


def getProfileIDFromBUIDS(profile_id):
    select_profiles_query = "SELECT profile_id FROM buids WHERE browser_id = %s"
    rdbcur.execute(select_profiles_query, (profile_id,))
    return rdbcur.fetchall()

def getSessionIDFromOrder(productID):
    """
    :param productID: str
    :return: Een lijst met sessionIDs die bij de gegeven productID hoort. Dit komt van de tabel Orders.
    """
    select_orderID_query = "SELECT session_id FROM orders WHERE product_id = %s"
    rdbcur.execute(select_orderID_query, (productID,))
    return rdbcur.fetchall()


def getProductIDFromOrder(sessionID):
    """
    :param sessionID: str
    :return: Een lijst met productIDs die bij de gegeven sessionID hoort. Dit komt van de tabel Orders.
    """
    select_productID_query = "SELECT product_id FROM orders WHERE session_id = %s"
    rdbcur.execute(select_productID_query, (sessionID,))
    return rdbcur.fetchall()


def getBrowserIDFromBUIDS(profileID):
    """
    :param profileID:str
    :return: Lijst met browser_ids die bij de gegeven profileID hoort. Dit komt van de tabel BUIDS.
    """
    select_buids_query = "SELECT browser_id FROM buids WHERE profile_id = %s"
    rdbcur.execute(select_buids_query, (profileID,))
    return rdbcur.fetchall()


def getSessionIDFromSessions(browserID):
    """
    :param browserID:str
    :return: Lijst met sessionIDs die bij de gegeven browserID hoort. Dit komt van de tabel sessions.
    """
    select_sessions_query = "SELECT session_id FROM sessions WHERE browser_id = %s"
    rdbcur.execute(select_sessions_query, (browserID,))
    return rdbcur.fetchall()


def getBrowserIDFromSessions(sessionID):
    """
    :param sessionID:str
    :return: Een browserID die bij de gegeven sessionID hoort. Dit kom van de tabel sessions
    """
    select_browserid_query = "SELECT browser_id FROM sessions WHERE session_id = %s"
    rdbcur.execute(select_browserid_query, (sessionID,))
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


def getProfileIDFromOrder(session_id):
    pass


def getProfilesFrequency(product_ids):
    """
    :param product_ids: Lijst met producten
    :return: Return een dictionary met de frequency van een profiel. Hoe vaker een profiel een product koopt hoe hoger
    zijn frequency.
    """
    sessions = []
    browser_ids = []
    profile_ids = []
    # Hier wordt er gekeken naar welke profiel ID's hebben de gekozen producten gekocht.
    # We weten alleen de session ID, dus we moeten van de session ID naar de browser ID naar de profiel ID gaan.
    for product in product_ids:
        sessions = getSessionIDFromOrder(product)
    for session in sessions:
        browser_ids.append(getBrowserIDFromSessions(session[0])[0])
    for browser_id in browser_ids:
        profile_ids.append(getProfileIDFromBUIDS(browser_id)[0][0])

    # Bepaal hier hoe vaak een profiel ID voor komt. Hoe vaker een profiel iets gekocht heeft, hoe vaker hij voorkomt.
    frequency = {}
    for profile_id in profile_ids:
        if profile_id not in frequency:
            frequency[profile_id] = 1
        else:
            frequency[profile_id] += 1

    return frequency


def getSimilarProfiles(profile_id):
    """ 
    :param product_ids: lijst met producten
    :return: Lijst met profielen die het meeste lijken op de gebruiker gebaseerd op de frequency van een profiel. Hoe
    vaker een profiel iets koopt, hoe hoger zijn frequency.
    """
    boughtProducts = getBoughtProducts(profile_id)
    profileFrequency = getProfilesFrequency(boughtProducts)
    Recommendations = []

    print(profileFrequency)

    if boughtProducts >= 1:
        # We willen 4 recommendations hebben. Dus doet wordt gedaan totdat er 4 recommendations zijn.
        while len(Recommendations) < 4:
            biggest = max(profileFrequency.values())
            for profile_id, frequency in profileFrequency.items():
                # Als de recommendation een frequency heeft van "biggest" dan wordt hij toegevoegd aan een lijst
                if frequency == biggest:
                    print(profile_id)
                    Recommendations.append(profile_id)
                    profileFrequency.pop(profile_id)
                    break
        return Recommendations
    else:
        print("Er is geen een gekochte product")


def insertRecommendations():
    profile_ids = getProfileIDs()
    for profile_id in profile_ids:
        print(profile_id)
        


insertRecommendations()


test_session_id = "0166c77f-f534-4fea-9e98-c83e7d3a79e9"