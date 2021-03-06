# astLib: python astronomy modules

    version: 0.9.1

    (c) 2007-2012 Matt Hilton
    (c) 2013-2017 Matt Hilton & Steven Boada

    http://astlib.sourceforge.net

    email: matt.hilton@mykolab.com

-------------------------------------------------------------------------------------------------------------
## INTRODUCTION

astLib provides some tools for research astronomers who use Python. It is divided into several modules:

    - astCalc   (general calculations, e.g. luminosity distance etc.)
    - astCoords (coordinate conversions etc.)
    - astImages (clip sections from .fits etc.)
    - astPlots  (provides a flexible image plot class, e.g. plot image with catalogue objects overlaid)
    - astSED    (calculate colours, magnitudes from stellar population models or spectral templates, fit
                 photometric observations using stellar population models etc.)
    - astStats  (statistics, e.g. biweight location/scale estimators etc.)
    - astWCS    (routines for using FITS World Coordinate System information)

The astWCS module is a higher level interface to PyWCSTools, a simple SWIG (http://www.swig.org) wrapping
of some of the routines from WCSTools by Jessica Mink (http://tdc-www.harvard.edu/software/wcstools/). It is
used by some routines in astCoords, astImages and astPlots.

The goal of astLib is to provide features useful to astronomers that are not included in the scipy
(http://scipy.org), numpy (http://numpy.scipy.org) or matplotlib (http://matplotlib.sourceforge.net) modules
on which astLib depends. For a more extensive set of python astronomy modules, see astropy
(http://www.astropy.org/).

Some scripts using astLib can be found in the examples/ folder in this archive.

-------------------------------------------------------------------------------------------------------------
## INSTALLATION

astLib 0.9.0 requires:

    * Python
      (tested on versions 2.7.3+)
    * PyFITS - http://www.stsci.edu/resources/software_hardware/pyfits
      (tested on version 3.4)
    * numpy - http://numpy.scipy.org
      (tested on version 1.13.0)
    * scipy - http://scipy.org
      (tested on version 0.18.1)
    * matplotlib - http://matplotlib.sourceforge.net
      (tested on version 1.5.1)

## optional:

    * Python Imaging Library - http://www.pythonware.com/products/pil
      (tested on version 1.1.7)
    * astropy - http://www.astropy.org/
      (tested on version 1.3)
      This is currently only used if pyfits is not installed (astropy.io.fits at present provides
      a drop-in replacement for pyfits).

Other versions of the software listed above are likely to work - I'm unable to test every possible
combination. For reference, astLib is currently developed on KDE neon/Ubuntu 16.04 (x86_64). Note that
it is possible to use some astLib functions (such as the astWCS module) without installing all of the
python modules listed above.

To install astLib system wide (and build and install PyWCSTools), simply:

    % sudo python setup.py install

in the directory this README is in.

If you do not have root access to your machine, astLib can be installed in your home directory by
doing the following:

    % python setup.py install --prefix=$HOME/python-modules

and adding something like the following to your .bashrc (or equivalent):

    export PYTHONPATH=$PYTHONPATH:$HOME/python-modules/lib/python2.7/site-packages

-------------------------------------------------------------------------------------------------------------
## USAGE

To access the routines in the astLib modules, simply:

    % from astLib import astCalc
    % from astLib import astCoords
    % from astLib import astWCS

etc.

The astWCS module currently provides access to what are (I think) the most commonly needed WCS information
and functions (such as converting between pixel and WCS coordinates etc.). However, should you wish to
access the wrapped WCSTools routines themselves directly:

    % from PyWCSTools import wcs
    % from PyWCSTools import wcscon

etc.

Note that PyWCSTools only includes some functions from wcs.c and wcscon.c at present. For examples of usage,
look at the Python code for the astLib.astWCS module. Documentation for the WCSTools routines can be found
here: http://tdc-www.harvard.edu/software/wcstools/subroutines/libwcs.wcs.html.

-------------------------------------------------------------------------------------------------------------
## KNOWN ISSUES

This may no longer apply, but just in case...

Recent versions of matplotlib (on which astLib depends) now use locale information. On systems where the
decimal point separator is not '.' (e.g. Germany), the astWCS coordinate conversions routines will give
strange results if this is not accounted for. As of version 0.3.0, the astWCS module will detect if this is
the case and print a warning message to the console.

The workaround for this issue is to add the following after importing any python modules that expicitly set
the locale (such as matplotlib):

    % import locale
    % locale.setlocale(locale.LC_NUMERIC, 'C')"

Thanks to Markus Demleitner for pointing this out.

-------------------------------------------------------------------------------------------------------------
## DOCUMENTATION

Documentation is available on the web at:

    http://astlib.sourceforge.net/?q=docs0.7

The API reference documentation (generated using epydoc) is also supplied in HTML format in this archive
under the docs/astLib/ directory.

-------------------------------------------------------------------------------------------------------------
## BUGS

Please email bug reports to matt.hilton@mykolab.com, or alternatively use the bug tracker:

    http://sourceforge.net/p/astlib/bugs/

Please include details of your operating system, python version, and versions of the python packages
required by astLib that you have installed on your machine. For any WCS-related bugs, it would be helpful
if you could also include the image header as a text file so that I can reproduce them easily.

-------------------------------------------------------------------------------------------------------------
