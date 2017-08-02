"""
.. module:: initialize_cbp
    :platform: unix
    :synopsis: This is a module that contains the elements necessary to create a command line parser and use it.

.. codeauthor:: Eric Coughlin

This is the initialize_cbp module
"""

import argparse
import cbp.cbp_instrument

class CbpParser:
    """
    This is the CbpParser class which creates a command line parser for use with cbp
    """
    def __init__(self,cbp=None):
        self.cbp = cbp

    def create_parser(self):
        """
        Parse the options given on the command-line.
        """
        parser = argparse.ArgumentParser(description='Run CBP Instruments.')

        subparsers = parser.add_subparsers(help='cbp instrument sub-commands')

        parser_phidget = subparsers.add_parser('phidget', help='prints out phidget position')
        parser_phidget.set_defaults(func=self.phidget)

        parser_pententiometer = subparsers.add_parser('pententiometer',
                                                      help='prints out information about the two pententiometers')
        parser_pententiometer.set_defaults(func=self.potentiometer)

        parser_altaz = subparsers.add_parser('altaz', help='instrument to move camera')

        parser_altaz_subparsers = parser_altaz.add_subparsers(help='altaz sub-commands')

        parser_altaz_compile = parser_altaz_subparsers.add_parser('compile', help="Does the compile action")
        parser_altaz_compile.set_defaults(func=self.altaz_compile)

        parser_altaz_steps = parser_altaz_subparsers.add_parser('steps', help="moves cbp in steps in either the horizontal or vertical axis")
        parser_altaz_steps.add_argument('steps', default=1000, type=int)
        parser_altaz_steps.add_argument('motornum', default=1, type=int)
        parser_altaz_steps.set_defaults(func=self.altaz_steps)

        parser_altaz_angle = parser_altaz_subparsers.add_parser('angle', help="Does the angle action")
        parser_altaz_angle.add_argument('motornum', default=1, type=int)
        parser_altaz_angle.add_argument('angle', default=2.0, type=float)
        parser_altaz_angle.set_defaults(func=self.altaz_angle)

        parser_birger = subparsers.add_parser('birger', help='birger instrument')

        parser_birger_subparsers = parser_birger.add_subparsers(help='birger sub-commands')

        parser_birger_focus = parser_birger_subparsers.add_parser('focus', help='sets the focus')
        parser_birger_focus.add_argument('focus', default=4096, type=int, help='the value to set the focus to.')
        parser_birger_focus.set_defaults(func=self.birger_focus)

        parser_birger_aperture = parser_birger_subparsers.add_parser('aperture', help='sets the aperture')
        parser_birger_aperture.add_argument('aperture', default=0, type=int, help='the value to set the aperture to.')
        parser_birger_aperture.set_defaults(func=self.birger_aperture)

        parser_lamp = subparsers.add_parser('lamp', help='sets the lamp')
        parser_lamp.add_argument('lamp', default=100, type=int)
        parser_lamp.set_defaults(func=self.lamp_lamp)

        parser_shutter = subparsers.add_parser('shutter', help='sets the shutter')
        parser_shutter.add_argument('shutter', default=-1, type=int)
        parser_shutter.set_defaults(func=self.shutter_shutter)

        parser_photodiode = subparsers.add_parser('photodiode', help='prints photo')
        parser_photodiode.set_defaults(func=self.photodiode)

        parser_filter_wheel = subparsers.add_parser('filter wheel', help='filter wheel instrument')

        parser_filter_wheel_subparsers = parser_filter_wheel.add_subparsers(help='filter wheel sub-commands')

        parser_filter_wheel_position = parser_filter_wheel_subparsers.add_parser('position',
                                                                                 help='change position of filter wheel.')
        parser_filter_wheel_position.add_argument('mask', default=0, type=int)
        parser_filter_wheel_position.add_argument('filter', default=0, type=int)
        parser_filter_wheel_position.set_defaults(func=self.filter_wheel_position)

        parser_filter_wheel_get_position = parser_filter_wheel_subparsers.add_parser('get position',
                                                                                     help='get position of filter wheel.')
        parser_filter_wheel_get_position.set_defaults(func=self.filter_wheel_get_position)

        parser_monochrometer = subparsers.add_parser('monochrometer', help='monochrometer instrument')

        parser_monochrometer_subparsers = parser_monochrometer.add_subparsers(help='monochrometer sub-commands')

        parser_monochrometer_wavelength = parser_monochrometer_subparsers.add_parser('wavelength',
                                                                                     help='change the wavelength of the '
                                                                                          'monochrometer')
        parser_monochrometer_wavelength.add_argument('wavelength', default=600, type=int)
        parser_monochrometer_wavelength.set_defaults(func=self.monochrometer_wavelength)

        parser_monochrometer_get_wavelength = parser_monochrometer_subparsers.add_parser('get wavelength',
                                                                                         help='get the wavelength of the '
                                                                                              'monochrometer')
        parser_monochrometer_get_wavelength.set_defaults(func=self.monochrometer_get_wavelength)

        parser_monochrometer_filter = parser_monochrometer_subparsers.add_parser('filter',
                                                                                 help='change the filter of the '
                                                                                      'monochrometer')
        parser_monochrometer_filter.add_argument('monofilter', default=1, type=int)
        parser_monochrometer_filter.set_defaults(func=self.monochrometer_filter)

        parser_monochrometer_get_filter = parser_monochrometer_subparsers.add_parser('get filter',
                                                                                     help='get the filter of the '
                                                                                          'monochrometer')
        parser_monochrometer_get_filter.set_defaults(func=self.monochrometer_get_filter)

        parser_keithley = subparsers.add_parser('keithley', help='keithley instrument')
        parser_keithley.set_defaults(func=self.keithley)

        parser_spectograph = subparsers.add_parser('spectograph', help='spectograph instrument')
        parser_spectograph.add_argument('duration', default=1000000, type=int)
        parser_spectograph.set_defaults(func=self.spectograph)

        parser_laser = subparsers.add_parser('laser', help='laser instrument')
        parser_laser_subparsers = parser_laser.add_subparsers(help='laser sub-commands')
        parser_laser_change_wavelength = parser_laser_subparsers.add_parser('change_wavelength', help='change wavelength')
        parser_laser_change_wavelength.add_argument('wavelength', default=500, type=int)
        parser_laser_change_wavelength_loop = parser_laser_subparsers.add_parser('change_wavelength_loop',
                                                                                 help='loop through array of wavelengths')
        parser_laser_change_wavelength_loop.add_argument('--diagnostic', action="store_true", help='performs diagnostic')
        parser_laser_change_wavelength_loop.add_argument('wavelength_min', default=500, type=int)
        parser_laser_change_wavelength_loop.add_argument('wavelength_max', default=520, type=int)
        parser_laser_change_wavelength.set_defaults(func=self.laser_change_wavelength)
        parser_laser_change_wavelength_loop.set_defaults(func=self.laser_change_wavelength_loop)

        parser_laser_check_wavelength = parser_laser_subparsers.add_parser('check wavelength', help='check wavelength')
        parser_laser_check_wavelength.set_defaults(func=self.laser_check_wavelength)

        parser.add_argument("-v", "--verbose", action="store_true", default=False)

        return parser

    def phidget(self, opts):
        self.cbp.phidget.do_phidget(nave=opts.nave)

    def potentiometer(self, opts):
        self.cbp.potentiometer.do_potentiometer()

    def altaz_compile(self, opts):
        self.cbp.altaz.do_compile()

    def altaz_steps(self, opts):
        self.cbp.altaz.do_steps(opts.motornum, opts.val)

    def altaz_angle(self, opts):
        self.cbp.altaz.do_angle(opts.val,opts.motornum)

    def birger_focus(self, opts):
        self.cbp.birger.do_focus(opts.val)

    def birger_aperture(self, opts):
        self.cbp.birger.do_aperture(opts.val)

    def lamp_lamp(self, opts):
        self.cbp.lamp.do_lamp(opts.val)

    def shutter_shutter(self, opts):
        self.cbp.shutter.do_shutter(opts.val)

    def photodiode(self, opts):
        self.cbp.photodiode.do_photodiode()

    def filter_wheel_position(self, opts):
        self.cbp.filter_wheel.do_position(opts.mask, opts.filter)

    def filter_wheel_get_position(self, opts):
        self.cbp.filter_wheel.get_position()

    def monochrometer_wavelength(self, opts):
        self.cbp.monochromater.monowavelength(opts.wavelength)

    def monochrometer_get_wavelength(self, opts):
        self.cbp.monochromater.get_mono()

    def monochrometer_filter(self, opts):
        self.cbp.monochromater.monofilter(opts.wavelength)

    def monochrometer_get_filter(self, opts):
        self.cbp.monochromater.get_mono()

    def keithley(self, opts):
        self.cbp.keithley.do_keithley()

    def spectograph(self, opts):
        self.cbp.spectrograph.do_spectograph(opts.duration)

    def laser_change_wavelength(self, opts):
        self.cbp.laser.do_change_wavelength(opts.wavelength)

    def laser_change_wavelength_loop(self, opts):
        self.cbp.laser.do_change_wavelength_loop(opts.wavelength_min,opts.wavelength_max)

    def laser_check_wavelength(self, opts):
        self.cbp.laser.check_wavelength()

def create_parse():
    """
    Parse the options given on the command-line.
    """
    parser = argparse.ArgumentParser(description='Run CBP Instruments.')

    subparsers = parser.add_subparsers(help='cbp instrument sub-commands')

    parser_phidget = subparsers.add_parser('phidget', help='prints out phidget position')

    parser_pententiometer = subparsers.add_parser('pententiometer',
                                                  help='prints out information about the two pententiometers')

    parser_altaz = subparsers.add_parser('altaz', help='instrument to move camera')

    parser_altaz_subparsers = parser_altaz.add_subparsers(help='altaz sub-commands')

    parser_altaz_compile = parser_altaz_subparsers.add_parser('compile', help="Does the compile action")

    parser_altaz_steps = parser_altaz_subparsers.add_parser('steps', help="moves cbp in steps in either the horizontal or vertical axis")
    parser_altaz_steps.add_argument('steps', default=1000, type=int)
    parser_altaz_steps.add_argument('motornum', default=1, type=int)

    parser_altaz_angle = parser_altaz_subparsers.add_parser('angle', help="Does the angle action")
    parser_altaz_angle.add_argument('motornum', default=1, type=int)
    parser_altaz_angle.add_argument('angle', default=2.0, type=float)

    parser_birger = subparsers.add_parser('birger', help='birger instrument')

    parser_birger_subparsers = parser_birger.add_subparsers(help='birger sub-commands')

    parser_birger_focus = parser_birger_subparsers.add_parser('focus', help='sets the focus')
    parser_birger_focus.add_argument('focus', default=4096, type=int, help='the value to set the focus to.')

    parser_birger_aperture = parser_birger_subparsers.add_parser('aperture', help='sets the aperture')
    parser_birger_aperture.add_argument('aperture', default=0, type=int, help='the value to set the aperture to.')

    parser_lamp = subparsers.add_parser('lamp', help='sets the lamp')
    parser_lamp.add_argument('lamp', default=100, type=int)

    parser_shutter = subparsers.add_parser('shutter', help='sets the shutter')
    parser_shutter.add_argument('shutter', default=-1, type=int)

    parser_photodiode = subparsers.add_parser('photodiode', help='prints photo')

    parser_filter_wheel = subparsers.add_parser('filter wheel', help='filter wheel instrument')

    parser_filter_wheel_subparsers = parser_filter_wheel.add_subparsers(help='filter wheel sub-commands')

    parser_filter_wheel_position = parser_filter_wheel_subparsers.add_parser('position',
                                                                             help='change position of filter wheel.')
    parser_filter_wheel_position.add_argument('mask', default=0, type=int)
    parser_filter_wheel_position.add_argument('filter', default=0, type=int)

    parser_filter_wheel_get_position = parser_filter_wheel_subparsers.add_parser('get position',
                                                                                 help='get position of filter wheel.')

    parser_monochrometer = subparsers.add_parser('monochrometer', help='monochrometer instrument')

    parser_monochrometer_subparsers = parser_monochrometer.add_subparsers(help='monochrometer sub-commands')

    parser_monochrometer_wavelength = parser_monochrometer_subparsers.add_parser('wavelength',
                                                                                 help='change the wavelength of the '
                                                                                      'monochrometer')
    parser_monochrometer_wavelength.add_argument('wavelength', default=600, type=int)

    parser_monochrometer_get_wavelength = parser_monochrometer_subparsers.add_parser('get wavelength',
                                                                                     help='get the wavelength of the '
                                                                                          'monochrometer')

    parser_monochrometer_filter = parser_monochrometer_subparsers.add_parser('filter',
                                                                             help='change the filter of the '
                                                                                  'monochrometer')
    parser_monochrometer_filter.add_argument('monofilter', default=1, type=int)

    parser_monochrometer_get_filter = parser_monochrometer_subparsers.add_parser('get filter',
                                                                                 help='get the filter of the '
                                                                                      'monochrometer')

    parser_keithley = subparsers.add_parser('keithley', help='keithley instrument')

    parser_spectograph = subparsers.add_parser('spectograph', help='spectograph instrument')
    parser_spectograph.add_argument('duration', default=1000000, type=int)

    parser_laser = subparsers.add_parser('laser', help='laser instrument')
    parser_laser_subparsers = parser_laser.add_subparsers(help='laser sub-commands')
    parser_laser_change_wavelength = parser_laser_subparsers.add_parser('change_wavelength', help='change wavelength')
    parser_laser_change_wavelength.add_argument('wavelength', default=500, type=int)
    parser_laser_change_wavelength_loop = parser_laser_subparsers.add_parser('change_wavelength_loop',
                                                                             help='loop through array of wavelengths')
    parser_laser_change_wavelength_loop.add_argument('--diagnostic', action="store_true", help='performs diagnostic')
    parser_laser_change_wavelength_loop.add_argument('wavelength_min', default=500, type=int)
    parser_laser_change_wavelength_loop.add_argument('wavelength_max', default=520, type=int)

    parser_laser_check_wavelength = parser_laser_subparsers.add_parser('check wavelength', help='check wavelength')

    parser.add_argument("-v", "--verbose", action="store_true", default=False)

    return parser

if __name__ == '__main__':
    pass
