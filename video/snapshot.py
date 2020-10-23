import ffmpeg
import os
from subprocess import Popen
from typing import Any

def _prepare_command(channel_id: int, in_src: str, base_out_dir: str) -> ffmpeg.Stream:
    if not channel_id:
        raise ValueError("channel_id is mandatory")
    if not base_out_dir or not os.path.isdir(base_out_dir):
        raise ValueError("base_out_dir must exist")
    out_file = base_out_dir + '/channel_' + str(channel_id)
    if not os.path.isdir(out_file):
        os.makedirs(out_file)
    out_file = out_file + '/snapshot.jpg'
    return (
        ffmpeg
        .input(in_src, max_delay=500000, rtsp_transport='tcp')
        .filter('scale', size='320x240', force_original_aspect_ratio='decrease')
        .output(out_file, vframes=1)
        .overwrite_output()
    )

def take_snapshot(channel_id: int, in_src: str, base_out_dir: str) -> Any:
    return _prepare_command(channel_id, in_src, base_out_dir).run()

def take_snapshot_async(channel_id: int, in_src: str, base_out_dir: str) -> Popen:
    return _prepare_command(channel_id, in_src, base_out_dir).run_async()