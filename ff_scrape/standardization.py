def standardize_rating(rating):
    rating = rating.strip()
    if rating == 'Teans':
        return 'T'
    if rating == 'NC-17 - No One 17 and Under Admitted':
        return 'NC-17'
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
    # todo: enhance this
    return character

def standardize_warning(warning):
    warning = warning.strip()
    return warning

def standardize_category(category):
    category = category.strip()
    return category

# todo: add standardize pairing
