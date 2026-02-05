---
name: video-format
description: Process videos using ffmpeg and gifsicle to edit videos. Use when working with .mp4, .avi, or .gif files, or sequences of .png or .jpg files, and the request is to compress, convert to a different format, scale, crop, remove or extract frames, concatenate multiple videos in space or in time, or speed up or slow down the video.
allowed-tools: ffmpeg, ffprobe, awk, gifsicle, scripts/avi2gif.sh, ls, mediainfo
---

# video-format

## Version History

* v0.1 first try!

## Instructions
* Use ffprobe or mediainfo to find information about the input videos. You have permissions to run ffprobe and mediainfo.
* Do not overwrite existing videos without asking.
* Keep track of all videos created in the process.
* After making the final video that satisfies the user, do some cleanup. List all the videos that were created in the process, and ask if they want to delete all except the input final video videos.
* If gifsicle has the capability, use gifsicle for manipulating gifs.
* If ffmpeg has the capability use ffmpeg for manipulating avis and mp4s. 
* Converting videos to animated gifs:
    * Use scripts/avi2gif.sh for converting videos to animated gifs.
    Usage:
        ```
	avi2gif.sh input.mp4 output.gif [scale] [fps]
	input.mp4: input video path (required)
	output.gif: output file path (required)
	scale: width in pixels. default: 400, height scaled proportionally
	fps: frame rate. default: 30
	```
    * By default, the frame rate for the animated gif should be the minimum of 30 and the frame rate of the input video, determined with ffprobe.
    * By default, the width of the video should stay the same. 
    * If the input video is longer than 1000 frames, ask the user if they want to reduce the number of frames by either removing frames from the beginning or end or reducing the output gif frame rate. Based on the number of frames, give suggestions of how to reduce the number of frames to <=1000. 
    * After creating the gif, tell the user the size of the video in MB. Ask the user if this is too large, and, if so, what size video they want in MB. If they want the animated gif to be smaller, give them suggestions of how to make the gif smaller by reducing the frame rate or scaling down the video. Perform computations based on the first gif size to guess how much to scale down the video, and work with the user to figure out the best way to scale down the video. When rescaling the video, make sure the width and height are multiples of 4. Use gifsicle to manipulate the animated gif.
    * Default file name. If the input path is /path/to/movie.mp4, the output path by default is /path/to/movie.gif.
* Converting videos between codecs
  * By default, compress to h264 mp4 videos using ffmpeg.
  * If asked, use ffmpeg to find a list of supported video codecs.
  * If the input video's width and height are not multiples of 4, figure out the nearest multiple of 4 for each, and ask the user if they would like to rescale to this size. Tell them the input and output widths and heights.
  * After compressing, let the user know the size of the video in MB.
  * Default file name. If the input path is /path/to/movie.mp4, the output path by default is /path/to/movie_<codec>.mp4, where <codec> is the codec name.
* Transformations to make the video take less space:
  * To make the video smaller, you can use ffmpeg to recompress in a more optimized way, scale down the size of the video in width and height, subsample the frames while also proportionally decreasing the playback fps so that the video plays at the same speed. 
  * Default file name. If the input path is /path/to/movie.mp4, the output path by default is /path/to/movie_<filesize>.mp4, where <filesize> is the size of the output file in MB. 
* Scaling the video:
  * By default, maintain the aspect ratio of the video.
  * If scaling by a percentage/fraction, choose widths and heights so that they are multiples of four.
  * Default file name. If the input path is /path/to/movie.mp4, the output path by default is:
    * If scale is specified in percentage, /path/to/movie_<scale>pct.mp4 where <scale> is the specified percentage.
    * If scale is the specified width in pixels, /path/to/movie_w<width>px.mp4 where <scale> is the specified width in pixels.
    * If scale is the specified height in pixels, /path/to/movie_h<height>px.mp4 where <scale> is the specified height in pixels.
* Cropping videos by removing or extracting rows or columns.
  * If the output size is not a multiple of 4, prompt the user with the nearest multiple of four. 
  * Default file name: If the input path is /path/to/movie.mp4, the output path by default is  /path/to/movie_r<r1>to<r2>_c<c1>to<c2>.mp4, where <r1> and <r2> are the limits of the rows extracted and <c1> and <c2> are the limits of the columns extracted. 
* Remove or extract frames using ffmpeg.
  * Default file name: If the input path is /path/to/movie.mp4, the output path by default is /path/to/movie_f<f1>to<f2>.mp4, where <f1> and <f2> are the limits of the frames extracted.
* Concatenating videos in space:
  * Videos can be concatenated either into a row, a column, or a grid.
  * If sizes don't match, scale up smaller videos to match the largest.
* Concatenating videos in time:
* Speeding up or slowing down videos:
  * There are two ways to change the speed: changing the encoded playback speed in the video, or dropping/repeating frames.
  * User will specify how many times faster/slower they want the video to play. 
  * If the desired playback speed is <= 30 fps, do not drop or repeat frames, but instead change the playback speed. 
  * If the desired playback speed is more than 30 fps, ask the user whether they want to drop/repeat frames or change the playback speed. 
  * Default file name: If the input path is /path/to/movie.mp4, the output path by default is /path/to/movie_<factor>x.mp4, where <factor> is how much faster the output video is than the input. If the video is slower, then factor will be < 1. 

## Examples

- Convert myvideo.avi to h264 codec mp4 container would create
- Scaling the video size down in width and height
- Cropping regions from the video
- Removing frames from the video
- 

Show concrete examples of using this Skill.