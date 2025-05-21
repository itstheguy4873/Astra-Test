def parse(filepath):
    config = {}
    try:
        with open(filepath,'r') as f:
            for line in f:
                line = line.strip()

                if not line or ' ' not in line:
                    continue

                key, value = line.split(' ', 1)
                config[key] = value

    except FileNotFoundError:
        raise FileNotFoundError(f'Could not find file: {filepath}')
    except Exception as e:
        raise Exception(e)
    return config

def write(filepath,config):
    try:
        with open(filepath,'w') as f:
            for key, value in config.items():
                f.write(f'{key} {value}\n')
    except Exception as e:
        print(e)

def uriparse(sequence):
    config = {}
    pairs = sequence.split('+')
    for pair in pairs:
        if ':' in pair:
            key, value = pair.split(':', 1)
            config[key] = value
    return config
    
