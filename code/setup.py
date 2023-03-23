from setuptools import setup, find_packages, Extension
import sys, os



install_requires = [
    # -*- Extra requirements: -*-
    ]

cm_module = Extension(
    'coremidi._simplecoremidi',
    sources=['coremidi/_simplecoremidi.c'],
    extra_link_args=['-framework', 'CoreFoundation',
                     '-framework', 'CoreMIDI']
    )

setup(name='simplecoremidi',
      version=0.1,
      ext_modules=[Extension('simplecoremidi', ['coremidi/_simplecoremidi.c'],
                              extra_link_args=['-framework', "CoreFoundation",
                                               '-framework', "CoreMIDI"])])

"""
setup(name='simplecoremidi',
      version=0.1,
      description="Simple OS X CoreMIDI interface",
      long_description="coremidi setup for interfacing with MIDI 2.0 endpoints in CoreMIDI",
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python :: 3.8",
        "Environment :: MacOS X",
        "Intended Audience :: Developers",
        "Development Status :: 1 - Planning",
        "Topic :: Multimedia :: Sound/Audio :: MIDI",
        "License :: OSI Approved :: MIT License",
        ],
      keywords='osx, CoreMIDI, MIDI, Mac OS X',
      author='Julian Hamelberg',
      author_email='jshx@mit.edu',
      url='https://github.com/jshjulian/py-midi2',
      license='MIT License',
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      ext_modules=[cm_module],
      )
      """