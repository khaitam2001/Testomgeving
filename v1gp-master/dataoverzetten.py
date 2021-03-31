from rdbconnection import conrdb
import time

rdbcon, rdbcur = conrdb()


def getProfilesFrequency(product_ids, gebruikerID=None):
    """
    :param product_ids: Lijst met producten
    :return: Return een dictionary met de frequency van profielen die een product hebben gekocht. Hoe vaker een
    profiel een product koopt hoe hoger zijn frequency.
    """

    if type(product_ids) != list:
        print("Error, input isn't a list")
        return None

    frequency = {}

    # Haal alle profielen die een product hebben gekocht.
    for product in product_ids:
        # Hier wordt er gekeken naar welke profiel ID's hebben de gekozen producten gekocht.
        temp = getProfilesBought(product)
        # Hieronder stoppen we de frequency van de profielen in een lijst
        for profile_id in temp:
            # De gebruikerID mag niet een recommendation zijn
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

    boughtProducts = getBoughtProduct(profile_id)
    profileFrequency = getProfilesFrequency(boughtProducts, profile_id)
    Recommendations = []


    while len(Recommendations) < 4:
        biggest = max(profileFrequency.values())
        for profileID, frequency in profileFrequency.items():
            if frequency == biggest:
                Recommendations.append(profileID[0])
                profileFrequency.pop(profileID)
                break
    return Recommendations


def insertRecommendations():
    profile_ids = getAllBoughtProfiles()
    profilenumber = 1

    for profile_id in profile_ids:
        print("This is profile ID number: " + str(profilenumber) + " out of " + str(len(profile_ids)))
        profilenumber += 1

        print("Recommended profiles: " + str(getSimilarProfiles(profile_id)) + "\n")

# Test Items = ['31953', '32093-queen', '31175', '7627', '41743', '04164', '42030', '42030', '04164', '41743', '7627', '31175', '32093-queen', '31953']
insertRecommendations()