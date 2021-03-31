from rdbconnection import conrdb
from collections import Counter
import time

rdbcon, rdbcur = conrdb()


def getAllBoughtProfiles():
    """
    :param profileID:str
    :return: Lijst met profielen die iets hebben gekocht
    """
    select_productsbought_query = "SELECT profile.profile_id FROM orders, sessions, buids, profile WHERE orders.session_id=sessions.session_id AND sessions.browser_id=buids.browser_id AND profile.profile_id=buids.profile_id GROUP BY profile.profile_id"
    rdbcur.execute(select_productsbought_query)
    return rdbcur.fetchall()


def getBoughtProduct(profile_id):
    """
    :param profile_id: str
    :return: Een lijst met producten die een profiel heeft gekocht
    """
    select_productsbought_Query = "SELECT array(SELECT product_id FROM orders, profile, sessions, buids WHERE profile.profile_id=buids.profile_id AND buids.browser_id=sessions.browser_id AND orders.session_id=sessions.session_id and buids.profile_id = %s)"
    rdbcur.execute(select_productsbought_Query, (profile_id,))
    return rdbcur.fetchall()[0][0]


def getProfilesBought(product_id):
    """
    :param product_id: str
    :return: Een lijst met profielen die een gegeven product hebben gekocht.
    """
    select_profilesbought_query = "SELECT profile.profile_id FROM orders, sessions, buids, profile WHERE profile.profile_id=buids.profile_id AND buids.browser_id=sessions.browser_id AND orders.session_id=sessions.session_id AND orders.product_id= %s"
    rdbcur.execute(select_profilesbought_query, (product_id,))
    return rdbcur.fetchall()


def getSessionsBought(session_id):
    """
    :param session_id: str
    :return: Een lijst met producten die gekocht zijn door de gegeven session
    """
    query = "SELECT array(SELECT product_id FROM orders WHERE session_id = %s)"
    rdbcur.execute(query, (session_id,))
    return rdbcur.fetchall()[0][0]


def getSessionsBoughtProduct(product_id):
    select_sessionsbought_query = "SELECT array( SELECT session_id FROM orders WHERE product_id = %s group by session_id order by session_id)"
    rdbcur.execute(select_sessionsbought_query, (product_id,))
    return rdbcur.fetchall()[0][0]


def getSessionFrequency(product_ids, gebruikerID=None):
    """
    :param product_ids: lijst met product-ids
    :param gebruikerID: str van profile_id
    :return: 4 meest overlappende sessions van de gegeven producten
    """

    if type(product_ids) != list:
        print("Input isn't a list")
        return None

    sessions = []
    for product in product_ids:
        sessions.extend(getSessionsBoughtProduct(product))

    # Kies niet de sessions van de gebruiker
    if gebruikerID != None:
        query = "select array(select session_id from sessions natural join buids where profile_id=%s group by session_id);"
        rdbcur.execute(query, (gebruikerID,))
        usersessions = rdbcur.fetchall()[0][0]
        for usersession in usersessions:
            if usersession in sessions:
                sessions.remove(usersession)

    # Return de frequency van sessions die het meest voorkomen in alle producten
    frequency = Counter(sessions)
    frequency = frequency.most_common(4)
    session_recommendations = []
    for session in frequency:
        session_recommendations.append(session[0])
    return session_recommendations


def getProductFrequency(session_ids):
    """
    :param session_ids:
    :return: Een lijst van 4 producten die het meeste overlappen van de gegeven session_ids
    """
    if type(session_ids) != list:
        print("Error! Input isn't a list")
        return None
    boughtProducts = []
    for session_id in session_ids:
        boughtProducts.extend(getSessionsBought(session_id))
    frequency = Counter(boughtProducts)
    frequency = frequency.most_common(4)
    product_recommendations = []
    # We willen alleen de 4 producten returnen
    for product_id in frequency:
        product_recommendations.append(product_id[0])
    return product_recommendations

# print(getSessionFrequency(['39328']))
# print(getSessionsBoughtProduct('39328'))
# print(getProductFrequency(['04a07186-c11e-4499-aa70-3e713e65f392-1543858931717', '04f1253f-1ce0-4b70-b8b2-e42bcd1bd56e-1535968002257']))


def insertRecommendations():
    profile_ids = getAllBoughtProfiles()
    profilenumber = 1

    for profile_id in profile_ids:
        gekochteproducten = getBoughtProduct(profile_id)

        bestsessions = getSessionFrequency(gekochteproducten, profile_id)

        print(bestsessions)

        print(getProductFrequency(bestsessions))

        # begin = time.time()
        print("This is profile ID number: " + str(profilenumber) + " out of " + str(len(profile_ids)))
        profilenumber += 1
        #
        # recommendedProfiles = getSimilarProfiles(profile_id)
        # # print("Recommended profiles: " + str(recommendedProfiles))
        #
        # similarProducts = getSimilarProducts(recommendedProfiles)
        # print("Similar Products: " + str(similarProducts))
        #
        # end = time.time()
        # print(str(end - begin))
        #
        # print("\n")

# Test Items = ['31953', '32093-queen', '31175', '7627', '41743', '04164', '42030', '42030', '04164', '41743', '7627', '31175', '32093-queen', '31953']
insertRecommendations()