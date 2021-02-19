def encode_id(phone_number):
    indetificator = ''
    for char in phone_number:
        if char == '1':
            indetificator += char
        if char == '2':
            indetificator += char
        if char == '3':
            indetificator += char
        if char == '4':
            indetificator += char
        if char == '5':
            indetificator += char
        if char == '6':
            indetificator += char
        if char == '7':
            indetificator += char
        if char == '8':
            indetificator += char
        if char == '9':
            indetificator += char
        if char == '0':
            indetificator += char
    return indetificator