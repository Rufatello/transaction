def auto_categorize(description):
    description = description.lower()
    if not description:
        return 'OTHER'

    food_categories = ['кафе', 'ресторан', 'food', 'продукты', 'супермаркет', 'пятёрочка', 'красное-белое']
    for i in food_categories:
        if i in description:
            return 'FOOD'
    transport_categories = ['деловые линии', 'яндекс такси', 'метро', 'автобус']
    for i in transport_categories:
        if i in description:
            return 'TRANSPORT'
    entertainment_categories = ['кино', 'театр', 'музей', 'цирк', 'концерт']
    for i in entertainment_categories:
        if i in description:
            return 'ENTERTAINMENT'

    utilities_categories = ['жкх', 'вода', 'газ']
    for i in utilities_categories:
        if i in description:
            return 'UTILITIES'

    return 'OTHER'