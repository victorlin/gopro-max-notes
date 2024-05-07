# GoPro MAX notes

## How to change the default viewing orientation of 360 video?

_originally from [a Reddit comment](https://www.reddit.com/r/GoProMAX/comments/fbiu7p/comment/fjey60n/) by [u/gyepi](https://www.reddit.com/user/gyepi/); follow-up to [[How-to-concatenate-360-videos-recorded-by-the-GoPro-MAX]]; untested_


As before, you will need to use the same software, but with an important twist: we need to use the v360 filter for ffmpeg, and since the v360 filter is still under development, it is not yet available in the stable release of ffmpeg. Hence you need to download and install the current snapshot release of ffmpeg for the following to work (download as zip, unzip, and replace your installed stable version with the snapshot version). Again, here are the locations for the programs we will need to use:

- https://gopro.com/help/articles/block/GoPro-Player
- https://evermeet.cx/ffmpeg/
- https://github.com/google/spatial-media/releases

1. If you didn't need to go through the concatenation (explained before), then again, we need to start with opening your .360 file with the GoPro Player and under File/Export as... export them as 5.6k or 4k videos (exporting in 4k is going to be much faster without much data loss; use the default HEVC encoding). The end result is going to be an .mp4 spherical 360 video file. I'm going to assume it is named as concatenated_injected.mp4 .

2. Open the Terminal, navigate to the directory where you have the concatenated_injected.mp4 , and use (with a suitable change of rotation parameters):

    ```
    ffmpeg -i concatenated_injected.mp4 -vf v360=e:e:yaw=60:pitch=0:roll=0 result.mp4
    ```

    The three values of rotation are the yaw, pitch, and roll values in degrees, google is your friend for their meaning; in the example above we change the yaw with 60 degrees and leave the pitch and the roll intact. In case you would like to use other parameters, here is the documentation for the v360 filter:

    https://www.ffmpeg.org/ffmpeg-filters.html#v360

    I know having to guess and set the rotation parameters by hand is far from ideal, but it seems a freeware GUI solution for doing this simply does not exist. I suggest that in the zeroth step, using the GoPro Player, trim out and export an only few second long segment from the original .360 video, and use trial-and-error on this short segment (which then will be rendered quickly) to figure out the ideal yaw, pitch, and roll parameters. Again, shame on the GoPro Player team for not implementing this ffmpeg filter in their software.

3. Using the Spatial Media Metadata Injector open result.mp4 , check the box "My video is spherical (3D)", and press "Inject metadata". You can now save the metadata-injected file, by the default name result_injected.mp4 . Congratulations, you have successfully reoriented the default viewing angle of your 360 spherical video file.

Hope this exegesis saved some of you a lot of time and $$$... Good luck!

## How to concatenate 360 videos recorded by the GoPro MAX?

_originally from [a Reddit comment](https://www.reddit.com/r/GoProMAX/comments/fbiu7p/comment/fjey4sm/) by [u/gyepi](https://www.reddit.com/user/gyepi/), updated with improvements from [u/Madfcuk](https://www.reddit.com/user/Madfcuk/)'s [comment](https://www.reddit.com/r/GoProMAX/comments/fbiu7p/comment/fkrx87r/?utm_source=share&utm_medium=web2x&context=3); untested_

UPDATE: this process can be automated using a [Python script](https://github.com/victorlin/gopro-max-knowledge/blob/-/concat-gopro-max-exports.py) in the GitHub repository.

Unfortunately I found no way to concatenate the raw .360 files directly. What we can do is to export the .360 files to .mp4 files with the GoPro Player, concatenate these files with ffmpeg, and then reinject the sperical metadata using Google's Spatial Media Metadata Injector. The three software you will need for this are:

- https://gopro.com/help/articles/block/GoPro-Player
- https://www.ffmpeg.org/download.html

After installing all of these, here are the steps (for Mac, for Windows it should be analogous):

1. Open the .360 files with the GoPro Player and under File/Export as... export them as 5.6k or 4k videos (exporting in 4k is going to be much faster without much data loss; use the default HEVC encoding). The end result is going to be a series of .mp4 spherical 360 video files, say, named as input1.mp4, input2.mp4, ..., inputN.mp4

2. In the same directory where you have input1.mp4, input2.mp4, ..., inputN.mp4, create a file named input.txt , whose content is the list of the .mp4 files that you want to concatenate, in order, prefaced with the word "file", in our example:

    ```
    file input1.mp4
    file input2.mp4
    file ...
    file inputN.mp4
    ```

3. Open the Terminal, change the directory to where you have the .mp4 files and the input.txt, and use the following command:

    ```
    ffmpeg -f concat -i input.txt -c copy -strict unofficial concatenated.mp4
    ```

    Ffmpeg will create the concatenated video file named concatenated.mp4 . `-strict unofficial` is necessary to avoid losing metadata that denotes spherical video.

## How to extract GPS data from 360 files?

[`gopro2gpx`](https://github.com/juanmcasillas/gopro2gpx) works great for this. It can extract from 360 files directly without conversion to another format.

```
gopro2gpx -s GS010001.360 gpxfile
```

[gpx.studio](https://gpx.studio/) is a neat website to explore GPX data.

## How to enable spherical 360° viewer for Google Photos?

Add an XMP tag:

```sh
exiftool -XMP-GPano:ProjectionType="equirectangular"
```
