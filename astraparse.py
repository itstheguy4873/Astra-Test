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

def write(file,config):
    try:
        with open(file,'w') as f:
            for key, value in config.items():
                f.write(f'{key} {value}\n')
    except Exception as e:
        print(e)
    
