from pathlib import Path
from typing import List


def main():
    import argparse

    parser = argparse.ArgumentParser(
            description = "Concatenate videos from GoPro MAX exported by GoPro Player Batch Exporter.")
    parser.add_argument("-i", "--input-dir", help="Directory containing GoPro MAX exported files")
    parser.add_argument("-o", "--output-dir", help="Directory to store concatenated files")
    parser.add_argument("--extension", default="mp4", help="Extension of GoPro MAX exported files")
    args = parser.parse_args()

    recordings = get_recordings(args.input_dir, args.extension)
    for recording_id, video_files in recordings.items():
        if len(video_files) == 1:
            print(f"{video_files[0]} is the only file in its recording. Skipping.")
            continue
        concat_file = f"{recording_id}.txt"
        create_ffmpeg_concat_file(video_files, concat_file)
        output_file = Path(args.output_dir, f"{recording_id}.mp4")
        call_ffmpeg_concat(concat_file, str(output_file))


def get_video_files(directory, extension):
    """Get GoPro video files in a directory."""
    import os
    import re

    filename_pattern = re.compile(r"^GS\d{{6}}\.({extension})$".format(extension=extension))

    for name in os.listdir(directory):
        if re.match(filename_pattern, name):
            yield Path(directory, name)


def get_recordings(directory, extension):
    """Return a dictionary mapping recording ID to a list of files."""
    files = get_video_files(directory, extension)
    filenames = {file.name for file in files}
    ids = {name[4:8] for name in filenames}
    recordings = dict()

    for id in ids:
        recordings[id] = []
        counter = 1
        counter_filename = f"GS{counter:02}{id}.{extension}"
        while counter_filename in filenames:
            recordings[id].append(Path(directory, counter_filename))
            counter += 1
            counter_filename = f"GS{counter:02}{id}.{extension}"
    return recordings


def create_ffmpeg_concat_file(video_files: List[Path], concat_file):
    """Generate the input file to ffmpeg's concat demuxer¹.

    ¹ https://trac.ffmpeg.org/wiki/Concatenate#Automaticallygeneratingtheinputfile
    """
    with open(concat_file, "w") as f:
        for file in video_files:
            f.write(f"file '{file}'\n")
    return concat_file


def call_ffmpeg_concat(concat_file: str, output_file: str):
    """Call ffmpeg to concatenate video files."""
    import subprocess

    # -safe 0 is necessary to handle relative paths
    # -strict unofficial is necessary to …
    subprocess.run(["ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_file,
        "-c", "copy",
        "-strict", "unofficial",
        output_file
    ])


if __name__ == "__main__":
    main()
