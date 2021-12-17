from configparser import ConfigParser
from pathlib import Path
home = str(Path.home())
config = ConfigParser()
config.optionxform = str
config.read('config.ini')

# Default regex
s_reg = r'[Ss](\d+)'
e_reg = r'[xXeE\.\-](\d+)'

# Default wsl home
wsl = f'/mnt/c/Users/<user>'
default = {
    'directory': [
        ('HomeDirectory', home,
         'Starting directory for this program'),
        ('DirectoryToTrack', 'Downloads', 'Dictonary to track'),
        ('DirectoryDestination', 'Downloads/auto', 'Dictonary destination'),
    ],
    'filename': [
        ('Prefix', '',
         '(optional) Use prefix on filename'),
        ('Season', s_reg, 'Season regex pattern e.g. S01'),
        ('Episode', e_reg, 'Episode regex pattern e.g. E01')
    ]
}


def getRegexLists():
    if 'filename' in config:
        season_regex = config['filename']['Season']
        episode_regex = config['filename']['Episode']

        return [[season_regex, s_reg], [episode_regex, e_reg, r'(\b\d+)']]
    else:
        return [[s_reg], [e_reg]]
