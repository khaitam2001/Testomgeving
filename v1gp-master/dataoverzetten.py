from rdbconnection import conrdb
import time

rdbcon, rdbcur = conrdb()

def getProfileIDs():
    """
    :param browser_id: str, Als het leeg is dan zoeken we naar alle profielen.
    :return: Een lijst met alle ProfileIDs van de database. Dit komt van de tabel profile.
    """
    select_profileIDs_query = "SELECT profile_id FROM profile"
    rdbcur.execute(select_profileIDs_query)
    return rdbcur.fetchall()


def getProfileIDFromBUIDS(browser_id):
    select_profiles_query = "SELECT profile_id FROM buids WHERE browser_id = %s"
    rdbcur.execute(select_profiles_query, (browser_id,))
    return rdbcur.fetchall()

def getSessionIDFromOrder(productID):
    """
    :param productID: str
    :return: Een lijst met sessionIDs die bij de gegeven productID hoort. Dit komt van de tabel Orders.
    """
    select_sessionID_query = "SELECT session_id FROM orders WHERE product_id = %s"
    rdbcur.execute(select_sessionID_query, (productID,))
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


def getProfileIDFromSessionID(sessionID):
    """
    :param sessionID: str
    :return: Een profiel ID die hoort bij een session
    """
    browserID = getBrowserIDFromSessions(sessionID)[0]
    profileID = getProfileIDFromBUIDS(browserID)[0][0]
    return profileID


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


def getProfilesFrequency(product_ids, gebruikerID=None):
    """
    :param product_ids: Lijst met producten
    :return: Return een dictionary met de frequency van profielen die een product hebben gekocht. Hoe vaker een
    profiel een product koopt hoe hoger zijn frequency.
    """
    session_ids = []
    profile_ids = []
    # Hier wordt er gekeken naar welke profiel ID's hebben de gekozen producten gekocht.
    # We weten alleen de session ID, dus we moeten van de session ID naar de browser ID naar de profiel ID gaan.
    if type(product_ids) != list:
        print("Error, input isn't a list")
        return None

    # Haal alle session ID's die horen bij een product
    for product in product_ids:
        temp = getSessionIDFromOrder(product)
        for session in temp:
            session_ids.append(session)
    # Haal alle profiel ID's die horen bij die sessions
    for session in session_ids:
        profile_ids.append(getProfileIDFromSessionID(session[0]))
    # Bepaal hier hoe vaak een profiel ID voor komt. Hoe vaker een profiel iets gekocht heeft, hoe vaker hij voorkomt.
    frequency = {}
    for profile_id in profile_ids:
        if gebruikerID != profile_id:
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
    profileFrequency = getProfilesFrequency(boughtProducts, profile_id)
    Recommendations = []


    if boughtProducts != 0:
        # We willen 4 recommendations hebben. Dus doet wordt gedaan totdat er 4 recommendations zijn.
        while len(Recommendations) < 4:
            try:
                biggest = max(profileFrequency.values())
                for profile_id, frequency in profileFrequency.items():
                    # Als de recommendation een frequency heeft van "biggest" dan wordt hij toegevoegd aan een lijst
                    if frequency == biggest:
                        Recommendations.append(profile_id)
                        profileFrequency.pop(profile_id)
                        break
            except ValueError:
                print("Er zijn niet genoeg verschillende profielen die de gegeven producten kopen")
                break
        return Recommendations
    else:
        print("Er is geen een gekochte product")


def insertRecommendations():
    profile_ids = getProfileIDs()
    begin = time.time()
    profilenumber = 0
    emptyprofiles = 0
    for profile_id in profile_ids:
        print("This is profile number: " + str(profilenumber) + " out of " + str(len(profile_ids)))
        profilenumber += 1
        start = time.time()
        print("Profile ID: " + str(profile_id[0]))
        profileBoughtItems = getBoughtProducts(profile_id)
        # Als het profiel niks heeft gekocht, dan wordt er niet naar gekeken.
        if profileBoughtItems != []:
            print("Bought Items By Profile: " + str(profileBoughtItems))
            similarprofiles = getSimilarProfiles(profile_id)
            print("Recommended Profiles: " + str(similarprofiles))
            productfrequency = {}

            # Bepaal hier hoe vaak producten voorkomen in de recommended profiles
            for profile in similarprofiles:
                boughtproducts = getBoughtProducts(profile)
                for product in boughtproducts:
                    if product not in productfrequency:
                        productfrequency[product] = 1
                    else:
                        productfrequency[product] += 1

            # Bepaal hier de 4 beste producten (De producten die het meeste voorkomen).
            product_recommendations = []
            try:
                while len(product_recommendations) < 4:
                    biggest = max(productfrequency.values())
                    for product_id, frequency in productfrequency.items():
                        if frequency == biggest:
                            product_recommendations.append(product_id)
                            productfrequency.pop(product_id)
                            break
            except ValueError:
                print("Not enough products")
                emptyprofiles += 1
            print("Product Recommendations: " + str(product_recommendations))
            end = time.time()
            print(str(end - start) + "\n")
        else:
            print("Not enough bought products")
            end = time.time()
            print(str(end - start) + "\n")
    true_end = time.time()
    print("Entire process took: " + str(begin - true_end))
    print("Total number of empty profiles: " + str(emptyprofiles))

# Test Items = ['31953', '32093-queen', '31175', '7627', '41743', '04164', '42030', '42030', '04164', '41743', '7627', '31175', '32093-queen', '31953']
insertRecommendations()