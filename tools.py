
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


def parse_communities(community_string):
    community_list = []
    community_matcher = (
        ("Athletics", "athletics"), ("Greek Life", "greek life"),
        ("Honors", "honors"), ("Student Life / RA", "student life / ra"),
        ("Service Clubs", "service clubs"),
        ("Academically-Oriented Clubs (ACS, Tri Beta, Phi Eta Sigma, Pre-Law, etc.)",
            "academic clubs"),
        ("Spiritual Life", "spiritual life"),
        ("Not Listed", "not listed")
    )


    if len(community_string) == 0:
        return community_list

    string_remainder = community_string
    remaining_len = len(string_remainder)

    #print("Starting comminity parsing")
    for k,v in community_matcher:
        #print("Checking for '{}'".format(v))
        #print("string_remainder: {}".format(string_remainder))
        k_len = len(k)
        if remaining_len < k_len:
            #print("remaining_len < k_len, continuing")
            continue
        if k == string_remainder[:k_len]:
            #print("Match! {}".format(k))
            community_list.append(v)
            if (remaining_len - k_len) > 0:
                string_remainder = string_remainder[k_len + 2:]
                remaining_len = len(string_remainder)

    return community_list
