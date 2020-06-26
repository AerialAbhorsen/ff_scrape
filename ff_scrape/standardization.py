def standardize_rating(rating):
    rating = rating.strip()
    if rating == 'Teans':
        return 'T'
    if rating == 'NC-17 - No One 17 and Under Admitted':
        return 'NC-17'
    if rating == 'R - Restricted':
        return 'R'
    return rating

def standardize_status(status):
    status = status.strip()
    if status == 'WIP (Work in progress)':
        return 'WIP'
    return status

def standardize_genre(genre):
    genre = genre.strip()
    return genre

def standardize_character(character):
    character = character.strip()
    if character == '':
        character = None
    # todo: enhance this
    return character

def standardize_warning(warning):
    warning = warning.strip()
    warning = warning.replace(' / ', '/')
    return warning

def standardize_category(category):
    category = category.strip()
    if category == 'Hogwarts House':
        category = None
    return category

# todo: add standardize pairing
