import json
import random
from chance import chance


def pick_one(values):
    return random.choice(values)


def pick_many(values, minimum, maximum):
    num_values = random.choice(range(minimum, maximum))
    return json.dumps(list(set(random.choices(values, k=num_values))))


functions_map = {
    'boolean': chance.boolean,
    'character': chance.character,
    'string': chance.string,
    'syllable': chance.syllable,
    'word': chance.word,
    'sentence': chance.sentence,
    'paragraph': chance.paragraph,
    'age': chance.age,
    'date': chance.date,
    'birthday': chance.birthday,
    'first': chance.first,
    'last': chance.last,
    'name': chance.name,
    'hex_hash': chance.hex_hash,
    'color': chance.color,
    'domain': chance.domain,
    'email': chance.email,
    'ip': chance.ip,
    'street': chance.street,
    'state': chance.state,
    'city': chance.city,
    'phone': chance.phone,
    'path': chance.path,
    'filepath': chance.filepath,
    'pick_one': pick_one,
    'pick_many': pick_many,
}


def chance_dictionary(values):
    """
    This function generates dictionary
    from values parameter.
    For example this:
    example = {
        'streetway': ('street', {'language': 'en'}),
        'first_name': ('first', {'language': 'en'})
    }
    chance.dictionary(example)
    will output something like this:
    {'streetway': 'Jabhuru Point', 'first_name': 'Eunice'}

    :param values: dict
    :return: dict
    """
    result = dict()
    for key in values:
        fname = values[key][0]
        if fname not in functions_map:
            result[key] = values[key]
        else:
            params = values[key][1] if len(values[key]) == 2 else {}
            result[key] = functions_map[fname](**params)
    return result
