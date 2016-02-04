from setuptools import setup

setup(
    name = 'minerva',
    version = '1.0',
    author = 'Kyle Beatty',
    author_email = 'kylebeatty75@gmail.com',
    url = 'https://github.com/Nestor15/Minerva',
    description = 'Probability calculations for the board game Risk',
    packages = ['minerva'],
    entry_points = {
        'console_scripts': 'minerva = minerva.main',
    }
)
