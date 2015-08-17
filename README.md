# SPLnFFT_tools
Python tools for working with [Sound Pressure Level](https://en.wikipedia.org/wiki/Sound_pressure#Sound_pressure_level) files generated by the iOS apps [SPLnFFT and SPLnWatch](https://www.facebook.com/SPLnFFT) with a required in-app purchase.

The tools in this repo deal with files that generated by the iOS apps SPLnFFT and SPLnWatch but these tools are _neither created nor supported_ by the author of those apps, Fabien Lefebvre.  Instead, these tools were created for [Pythonista for iOS](http://www.omz-software.com/pythonista) based on the following [conversation thread](https://forum.omz-software.com/topic/1964/binary-files-read-and-write).

The binary data files generated by SPLnFFT and SPLnWatch contain Fast Lp and Slow Lp readings (each reading in a 4 byte float32) that are captured 8 times a second, 60 seconds a minute, 60 minutes an hour, 24 hours a day.  A __day is 86,400 seconds long__ (60 * 60 * 24) so all files should be:

*   691,200 samples long -- 8 samples per second * 86,400 seconds in a 24 hour day
* 5,529,600 bytes long -- 4 bytes per reading * 2 reading (fast, slow) per sample * 691200 samples in a 24 hour day

The files will be padded with (0.0, 0.0) samples for all times when the app is not recording Sound Pressure Levels so that all files are the same length regardless of how long the app was actively recording.

* __SPLnFFT_Reader_numpy__ is the primary tool which reads a SPLnFFT.bin file and generates a matplotlib plot.
* __SPLnFFT_split__ reads in a SPLnFFT.bin file and creates a new, smaller file by removing any hours which only contain (0, 0) values from the start and end of the file.
* __SPLnFFT_hourly_split__ creates 24 files each containing one hour of data to allow for more high resolution plots.

### Recommended workflow:
* Use SPLnFFT and/or SPLnWatch to record sound pressure levels
* Use the required in-app purchase to save a binary file(s) to Dropbox
* Use [Dropbox_file_picker.py](https://gist.github.com/omz/fb180c58c94526e2c40b) to download the binary file(s) into Pythonista
* Run __SPLnFFT_split.py__ to create a smaller file with leading and/or trailing hours of silence removed
* Run __SPLnFFT_Reader_numpy.py__ to graph the results

_Please help_ us to improve these tools by [opening an issue](https://github.com/cclauss/SPLnFFT_tools/issues/new) or submitting a pull request.
