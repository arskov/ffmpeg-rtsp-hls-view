from video import segment
from video import snapshot
from webserver.model import ChannelItem, Status
from subprocess import Popen
from typing import Mapping

import os
import glob
import logging

_process_map: Mapping[int, Popen] = {}
_logger = logging.getLogger('video_service')

async def start_segmenter_async(channel_item: ChannelItem, base_out_dir: str) -> None:
    if not channel_item:
        raise ValueError('channel_item is a mandatory parameter')
    if not base_out_dir:
        raise ValueError('base_out_dir is a mandatory parameter')
    # take recent snapshot
    snapshot_process = snapshot.take_snapshot_async(channel_item.channel_id, channel_item.rtsp_link, base_out_dir)
    # create a HLS segmenter if it doesn't exist in the process_map
    need_start = False
    if channel_item.channel_id in _process_map:
        if _process_map[channel_item.channel_id].poll():
            _logger.info('Segmenter process for channel {} was terminated. Start again'.format(channel_item.channel_id))
            del _process_map[channel_item.channel_id]
            need_start = True
        else:
            _logger.info('Process for channel {} is running. No need to start a new one'.format(channel_item.channel_id))
    else:
        need_start = True
    if need_start:
        segmenter = segment.CodecX264ResizeHLSFormatSegmenter(
            in_src=channel_item.rtsp_link,
            out_dir=base_out_dir,
            channel_id=channel_item.channel_id)
        segmenter_process = segmenter.run_async()
        _process_map[channel_item.channel_id] = segmenter_process

async def shutdown(channel_id: int = None) -> None:
    if channel_id:
        if channel_id in _process_map:
            _process_map[channel_id].terminate()
    else:
        for k, v in _process_map.items():
            v.terminate()
            del _process_map[k]

async def get_status(channel_id: int):
    if channel_id in _process_map and _process_map[channel_id].poll() is None:
        return Status.ON
    else:
        return Status.OFF
