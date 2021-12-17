import os


# Create config from dictionary
def createConfig(config, dictionary):
    for section_id, section in dictionary.items():
        for key, value, text in section:
            if not section_id in config:
                config[section_id] = {}
            defaultValue = f'(Default: {value})' if value else ''
            print(text + defaultValue)
            config[section_id][key] = input() or value

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

# Crate directory from path
def createDirectory(directory):
    if not os.path.isdir(directory):
        try:
            os.makedirs(directory, exist_ok=True)
            print(f'(Directory) {directory} created successfully')
        except OSError as error:
            print(f'(Directory) {directory} can not be created')
