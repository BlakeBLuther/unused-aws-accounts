import boto3
import yaml

import datetime
import pytz


def get_yaml_dict(yaml_struct, key):
    """
    Takes a loaded YAML object and extracts the 
    dict object desired.

    Args:
        yaml_struct (list): A list returned by yaml.load()
        key (string): A string to search the yaml list object for.

    Returns:
        dict: The dict with the key value specific by the arg key
    """
    return next(
        entry for entry in yaml_struct 
        if key in entry.keys()
        )[key]

def get_all_results(command):
    """
    Given a method to run, will get all paginated results
    and will return a dict with all results combined.

    Args:
        command: A method object to execute 
            (example - boto3.client('iam').list_users)

    Returns:
        dict: an object of all results, un-paginated
    """
    response = command()
    final_result = dict()
    targets = response.keys() - {
        'IsTruncated', 'Marker', 'ResponseMetadata'
    }

    if response['IsTruncated']:
        initial_marker = response['Marker']
    else:
        initial_marker = None

    for target in targets:
        final_result[target] = list()
        marker = initial_marker
        final_result[target].append(response[target])
        while response['IsTruncated']:
            response = command(Marker=marker)
            if response['IsTruncated']:
                marker = response['Marker']
            final_result[target].append(response[target])
    return final_result

def get_unused_users(users, max_time):
    """
    Given a users list from iam_client.list_users(),
        will return a list of users objects that have not
        logged in for a time period greater than the
        maximum date.
    
    Args:
        users: a list of users, as given by
            iam_client.list_users()['Users']
        max_time: a datetime timedelta object representing
            a maximum amount of time since login before
            reporting as unused
    
    Returns:
        list: a list of users of the same format
            whose last login time is greater than
            the timedelta specified by max_time
    """
    timezone = pytz.timezone("America/Denver")
    current_time = timezone.localize(datetime.datetime.now())
    unused_users = []
    for user in users['Users']:
        try:
            timedelta = current_time - user[0]['PasswordLastUsed']
            if timedelta > max_time:
                unused_users.append(user)
        except KeyError:
            timedelta = current_time - user[0]['CreateDate']
            if timedelta > max_age:
                unused_users.append(user)
    return unused_users


def user_string_extract(user):
    """
    Takes a user and returns a few key metrics:
        - the username
        - the date of last login
        - the creation date
    """
    try:
        return (
            user[0]['UserName'],
            user[0]['CreateDate'].strftime('%d %b %y'),
            user[0]['PasswordLastUsed'].strftime('%d %b %y')
        )
    except KeyError:
        return (
            user[0]['UserName'],
            user[0]['CreateDate'].strftime('%d %b %y'),
            'Never'
        )


if __name__ == "__main__":
    with open('config.yaml') as f:
        y = yaml.load(f, Loader=yaml.Loader)
        profiles = get_yaml_dict(y, 'profiles')
        # profiles is now a list of profiles from config.yaml
        
        for prof in profiles:
            session = boto3.Session(profile_name=prof)
            iam_client = session.client('iam')
            
            users = get_all_results(iam_client.list_users)
            max_age = datetime.timedelta(days=30)
            unused_users = get_unused_users(users, max_age)
            print("-----")
            print(f"Unused {prof} users:")
            for user in unused_users:
                user_strs = user_string_extract(user)
                print("User: {:>30}".format(user_strs[0]))
                print("Creation date: {:>21}".format(user_strs[1]))
                print("Last login: {:>24}".format(user_strs[2]))
                print()
            print()