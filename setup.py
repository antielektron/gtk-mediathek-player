import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gtk_mediathek_player",
    version="0.0.1",
    author="Jonas Weinz",
    author_email="jo.we93@gmx.de",
    description="A simple viewer for german public broadcasts using MediathekWeb",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/pypa/sampleproject",
    packages=['gtk_mediathek_player'],
    package_dir = {'gtk_mediathek_player': 'src/gtk_mediathek_player'},
    data_files = [
        ('share/applications', ['data/org.gtk_mediathek_player.desktop']),
        ('share/icons/hicolor/128x128/apps', ['data/gtkmediathekviewer.png']),
        ('share/icons/hicolor/scalable/apps', ['data/gtkmediathekviewer.svg']),
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)