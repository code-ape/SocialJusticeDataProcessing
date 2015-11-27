import itertools

def print_first(number,thing):
    if not hasattr(thing, '__iter__'):
        msg = "print_first_10: can't iterate over given thing..."
        print(msg)
        raise(Exception(msg))
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



def get_student_question_types():
    cat = "catagory"
    num = "numerical"
    multi = "multiple"

    question_types = [
        [num],      # 1
        [cat]*3,    # 2-4
        [num],      # 5
        [cat]*2,    # 6-7
        [multi],    # 8
        [cat],      # 9
        [num]*3,    # 10-12
        [cat],      # 13
        [multi]*3,  # 14-16
        [num]*2,    # 17-18
        [multi]*2,  # 19-20
        [cat],      # 21
        [num]*3,    # 22-24
        [multi],    # 25
        [num]*3,    # 26-28
        [cat]*2,    # 29-30
        [num]*2     # 31-32
    ]
    return list(itertools.chain(*question_types))

def get_fac_staff_question_types():
    cat = "catagory"
    num = "numerical"

    question_types = [
        [cat]*5,
        [num],
        [cat],
        [num]*19
    ]
    return list(itertools.chain(*question_types))

def get_num_questions(question_types):
    count = 0
    numerical_questions = []
    for question_type in question_types:
        if question_type == "numerical":
            numerical_questions.append(count)
        count+=1
    return numerical_questions

def get_question_title(number, data):
    first_response = data[0]
    question = first_response[number]
    title = question[0]
    return title

def get_responses_to_numbers(question_nums, data):
    responses = []
    for n in question_nums:
        responses.append(get_responses_to_number(n, data))
    return responses


def turn_responses_into_values(*args):
    assert(len(args) > 0)
    return_val = []
    for response_list in args:
        clean_response_list = []
        for response in response_list:
            clean_response_list.append(response[2])
        return_val.append(clean_response_list)
    return return_val


def get_responses_to_number(question_num, data):
    responses = []
    for entry in data:
        responses.append(entry[question_num])
    return responses

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
