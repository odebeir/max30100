# A micropython library for the Maxim MAX30100 pulse oximetry chip

This is a [MicroPython](http://micropython.org/) library for MAXIM MAX30100 heart rate and Sp02 sensor chip.
This library has been tested on a [pyboard lite v1.0](http://micropython.org/resources/pyblitev10ac-pinout.jpg).

This library is adapted from the Python library by Martin Fitzpatrick/mfitzp, available [here](https://github.com/mfitzp/max30100)
which is based on the original C library by Connor Huffine/Kontakt, available [here](https://github.com/kontakt/MAX30100),
with a slightly different API + additional features (buffering values, etc.).

Currently this library supports both IR led (pulse) and red led (SpO2) modes, with support (via gpiozero) for
catching on-board interrupts and triggering real-time measurements. The examples below demonstrate a common setup.
Calculations for converting measured values into actual number are not yet included.

## Basic setup

You can create an interface to your device/chip by creating an instance of the MAX30100 class.

    import max30100
    mx30 = max30100.MAX30100()

You can pass a number of optional parameters to configure the initial setup, including:

- `i2c` a custom i2c object, if you already have a connection option to the bus 
- `mode` to enable SpO2 readings by default
- `sample_rate` number of data samples to take per second
- `pulse_width` the duration of each sample
- `led_current_red` amount of current to supply to the red LED
- `led_current_ir` amount of current to supply to the infrared LED
- `max_buffer_len` the number of measurements to store locally

The values for sample rates, pulse widths and led currents are restricted. For the full list see the source code.
If you provide an invalid value the correct values are displayed for convenience.

The precise meanings for each of these values is [given in the MAX30100 datasheet](https://datasheets.maximintegrated.com/en/ds/MAX30100.pdf).

## Reading values

To read current sensor values from the MAX30100 chip you can call `.read_sensor`. This will retrieve the latest values
from the buffer and store them locally. The latest values are available under `.ir` and `.red` for IR and Red measurements
respectively. A local FIFO buffer is used to store previous measurements, up to `max_buffer_len` specified when setting up.

    mx30.read_sensor()

    # The latest values are now available via .ir and .red
    mx30.ir, mx30.red


## Take SpO2 (oxygen saturation) readings

To enable Sp02 reading, you can either set the mode directly, or use the convenience method:

    mx30.set_mode(max30100.MODE_SPO2)
    # or...
    ms30.enable_spo2()

If you perform another sensor read, you will now see a value for the `.red` parameter (which is neccessary to read
oxygen saturation).

    mx30.read_sensor()
    mx30.ir, mx30.red

The previous measurements are available in `.buffer_ir` and `.buffer_red`.

## Automating measurements 

The MX30100 chip provides an interrupt mechanism which can be used to trigger readings once values are available.

## Generator based filters

tbd... 

## References

1. [Blog on implementing pulse oximeter using MAX30100](https://morf.lv/implementing-pulse-oximeter-using-max30100)

1. [MAX30100 datasheet](https://datasheets.maximintegrated.com/en/ds/MAX30100.pdf)






