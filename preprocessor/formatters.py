def format_culture_name(title):
    arr = title.split(' ')
    arr.pop()
    result = ''.join(arr).lower()
    return result
