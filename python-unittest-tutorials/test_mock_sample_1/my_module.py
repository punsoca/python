
#  let_down_gently function will be mocked in unittest
def let_down_gently(target):
    pass

#  send_email function will be mocked in unittest
def send_email(target):
    pass

#  give_some_time function will be mocked in unittest
def give_some_time(target):
    pass

# the get_random_person function will be mocked in unittest
def get_random_person():
    # this function is mocked and will just return a name
    name = 'some name'
    return name

def get_next_person(user):
    person = get_random_person()
    # mock methods that can be tested with while logic in unit test: side effect and call_count
    # multiple calls to get_random_person can be tested in unit test using mock_function.side_effect()
    while person in user['people_seen']:
        person = get_random_person()
    return person

def evaluate(person1, person2):
    if person1 in person2['likes']:
        send_email(person1)
        send_email(person2)
    elif person1 in person2['dislikes']:
        let_down_gently(person1)
    else:
        give_some_time(person1)
