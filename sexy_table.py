from pprint import pprint

# where the magic happens
# PARAMETERS:
# data: list of objects to be formatted
# Headers: optional dict mapping property names to prettier formatted names
def print_table(data, Headers=None, Transformers=None, Order=None):
    keys = data[0].keys()

    offsets = get_header_offsets(data, Headers, Transformers)

    # order the offsets 
    if Order:
        offsets = sorted(offsets, key=lambda x: Order[x[0]] if x[0] in Order else 0)

    header_string = get_header_string(offsets, Headers)

    # print header
    print('-' * len(header_string))
    print(header_string)
    print('-' * len(header_string))

    # print data rows
    for d in data:
        line = []
        for key, pad in offsets:
            if key in Transformers:
                fun = Transformers[key]
                line.append(('| ' + str(fun(d[key]))).ljust(pad))
            else:
                line.append(('| ' + str(d[key])).ljust(pad))
        print(''.join(line) + '|')

# same as print_table, but it returns a string instead of prints
def sexy_table(data, Headers=None, Transformers=None, Order=None):
    result = []
    keys = data[0].keys()

    offsets = get_header_offsets(data, Headers, Transformers)

    # order the offsets 
    if Order:
        offsets = sorted(offsets, key=lambda x: Order[x[0]] if x[0] in Order else 0)

    header_string = get_header_string(offsets, Headers)

    # print header
    result.append('-' * len(header_string) + '\n')
    result.append(header_string + '\n')
    result.append('-' * len(header_string) + '\n')

    # print data rows
    for d in data:
        line = []
        for key, pad in offsets:
            if key in Transformers:
                fun = Transformers[key]
                line.append(('| ' + str(fun(d[key]))).ljust(pad))
            else:
                line.append(('| ' + str(d[key])).ljust(pad))
        result.append(''.join(line) + '|\n')

    return ''.join(result)
        

# returns a list of tuples, each containing a header key and the amount of space it requires
def get_header_offsets(data, Headers=None, Transformers=None):
    # extra space at end of each col
    EXTRA_SPACE = 4
    # find all headers present in all objects
    headers = set()
    
    for d in data:
        for key in d:
            headers.add(key)

    result = []
    # find longest value associated with each header and return it in list
    for key in headers:
        max_len = len(key)
        if Headers and key in Headers:
            max_len = len(Headers[key])
        for d in data:
            if key in Transformers:
                fun = Transformers[key]
                if len(str(fun(d[key]))) > max_len:
                    max_len = len(str(fun(d[key])))
            else:
                if len(str(d[key])) > max_len:
                    max_len = len(str(d[key]))
        result.append((key, max_len + EXTRA_SPACE))

    return result
        
# get the header line in string form
def get_header_string(offsets, Headers=None):
    result = []

    for key, pad in offsets:
        if Headers and key in Headers:
            result.append(('| ' + Headers[key]).ljust(pad))
        else:
            result.append(('| ' + key).ljust(pad))
    return ''.join(result) + '|'
