from video.segment import CodecCopyHLSFormatSegmenter
from video.segment import CodecX264HLSFormatSegmenter
from video.segment import CodecX264SegmentFormatSegmenter
from video.segment import CodecX264ResizeHLSFormatSegmenter
from video.snapshot import take_snapshot
import os
import pathlib
import argparse

PROJECT_ROOT = pathlib.Path(__file__).parent.parent

def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True)
    parser.add_argument("-o", "--output", type=str, default=str((PROJECT_ROOT/'hls-out').resolve()), required=False)
    parser.add_argument("-c", "--channel", type=int, default=1, required=False)
    parsed_args = parser.parse_args(args)
    in_src = parsed_args.input
    out_dir = parsed_args.output
    channel_id = parsed_args.channel
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    take_snapshot(channel_id, in_src, out_dir)
    g = CodecX264ResizeHLSFormatSegmenter(in_src=in_src, out_dir=out_dir, channel_id=channel_id)
    g.run()

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])