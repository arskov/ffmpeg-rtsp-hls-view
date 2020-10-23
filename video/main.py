from video.segment import CodecCopyHLSFormatSegmenter
from video.segment import CodecX264HLSFormatSegmenter
from video.segment import CodecX264SegmentFormatSegmenter
from video.segment import CodecX264ResizeHLSFormatSegmenter
from video.snapshot import take_snapshot
import os
import pathlib

PROJECT_ROOT = pathlib.Path(__file__).parent.parent

def main():
    in_src = 'rtsp://172.23.3.10/face_track_20_fhd'
    #in_src = 'rtsp://34.82.126.102:554/face_track_rafa_fhd'
    out_dir = PROJECT_ROOT / 'hls-out'
    channel_id = 3
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    take_snapshot(channel_id, in_src, str(out_dir.resolve()))
    g = CodecX264ResizeHLSFormatSegmenter(in_src=in_src, out_dir=str(out_dir.resolve()), channel_id=channel_id)
    g.run()

if __name__ == "__main__":
    main()