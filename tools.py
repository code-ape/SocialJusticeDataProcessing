
def print_first(number,thing):
    if not hasattr(thing, '__iter__'):
        msg = "print_first_10: can't iterate over given thing..."
        print(msg)
        raise(msg)
        return

    thing_len = len(thing)
    if thing_len == 0:
        msg = "Thing has no elements..."
        print(msg)
        return

    else:
        iter_length = min(number, thing_len)
        if type(thing) is dict:
            count = 0
            for k,v in thing.iteritems():
                print("{}: {}".format(k,v))
                count += 1
                if count > iter_length:
                    break
        else:
            for t in thing[0:iter_length]:
                print(t)


community_matcher = (
    ("Athletics", "athletics"), ("Greek Life", "greek life"),
    ("Honors", "honors"), ("Student Life / RA", "student life / ra"),
    ("Service Clubs", "service clubs"),
    ("Academically-Oriented Clubs (ACS, Tri Beta, Phi Eta Sigma, Pre-Law, etc.)",
        "academic clubs"),
    ("Spiritual Life", "spiritual life"),
    ("Not Listed", "not listed")
)

groups_matcher = (
    ("caucasians", "caucasian"),
    ("racial minorities", "racial minority"),
    ("people with disabilities", "disability"),
    ("people who identify as LGBT", "LGBT"),
    ("people of non-standard college age", "non_standard_age"),
    ("Men", "man"),
    ("Women", "woman"),
    ("athletes", "athlete"),
    ("individuals in Greek Life", "greek_life"),
    ("Honors Program Students", "honors"),
    ("Not listed", "not_listed")
)

sexual_assalt_matcher = (
    ("am someone who has", "experienced"),
    ("know someone who has", "know_someone")
)

def parse_communities(community_string):
    return parse_list_agruments(community_string, community_matcher)


def parse_discrim_demographic(string):
    discrim_demographic_matcher = (
        ("age", "age"), ("race", "race"), ("gender", "gender"),
        ("sexuality", "sexuality"), ("financial status", "financial_status"),
        ("place of birth", "place_of_birth"), ("disability", "disability"),
        ("involvement / lack of involvement with specific groups on campus",
            "campus_group_associations")
    )
    return parse_list_agruments(string, discrim_demographic_matcher)


def parse_discrim_involvement(string):
    return parse_list_agruments(string, community_matcher)

def parse_groups(string):
    return parse_list_agruments(string, groups_matcher)

def parse_sexual_assault(string):
    return parse_list_agruments(string, sexual_assalt_matcher)

def parse_list_agruments(string, matcher_dict):
    list = []

    if len(string) == 0:
        return list

    string_remainder = string
    remaining_len = len(string_remainder)

    #print("Starting comminity parsing")
    for k,v in matcher_dict:
        #print("Checking for '{}'".format(v))
        #print("string_remainder: {}".format(string_remainder))
        k_len = len(k)
        if remaining_len < k_len:
            #print("remaining_len < k_len, continuing")
            continue
        if k == string_remainder[:k_len]:
            #print("Match! {}".format(k))
            list.append(v)
            if (remaining_len - k_len) > 0:
                string_remainder = string_remainder[k_len + 2:]
                remaining_len = len(string_remainder)

    return list
