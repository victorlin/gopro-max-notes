from pathlib import Path
from typing import List


def main():
    import argparse

    parser = argparse.ArgumentParser(
            description = "Get GPX files from GoPro files.")
    parser.add_argument("-i", "--input-dir", help="Directory containing GoPro MAX 360 files")
    parser.add_argument("-o", "--output-dir", help="Directory to store GPX files")
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


if __name__ == "__main__":
    main()
