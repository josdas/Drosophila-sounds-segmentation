def parse_segments(file_name):
    with open(file_name, 'r') as fl:
        return [(int(data[1]), int(data[2]), data[0]) 
                for data in map(lambda s: s.strip().split(), fl)]
