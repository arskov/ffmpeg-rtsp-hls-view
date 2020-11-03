import ffmpeg
import os
import logging
import glob

logger = logging.getLogger('segmenter')

class BaseSegmenter:

    def __init__(self, in_src, out_dir, channel_id):
        if not channel_id or channel_id <= 0:
            raise ValueError("channel_id must be a positive integer")
        if not in_src or not out_dir:
            raise ValueError("in_src and out_dir are mandatory parameters")
        if not os.path.isdir(out_dir):
            raise ValueError("out_dir: {} must exist".format(out_dir))
        self.channel_id = channel_id
        self.in_src = in_src
        self.out_dir = out_dir + '/channel_' + str(channel_id)
        if not os.path.isdir(self.out_dir):
            os.makedirs(self.out_dir)
        else:
            file_list = glob.glob(self.out_dir + '/*.ts') + \
                        glob.glob(self.out_dir + '/*.m3u8') + \
                        glob.glob(self.out_dir + '/*.mp4')
            for f in file_list:
                os.remove(f)
        self.ff_input = ffmpeg.input(in_src, max_delay=500000, rtsp_transport='tcp')
    
    def run(self):
        if not self.ff_segment_out:
            raise Exception('Command is not ready')
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("FFmpeg CLI command: '%s'", " ".join(ffmpeg.compile(self.ff_segment_out)))
        return (self.ff_segment_out.run())
    
    def run_async(self):
        if not self.ff_segment_out:
            raise Exception('Command is not ready')
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("FFmpeg CLI command: '%s'", " ".join(ffmpeg.compile(self.ff_segment_out)))
        return self.ff_segment_out.run_async()


class CodecCopyHLSFormatSegmenter(BaseSegmenter):

    def __init__(self, in_src, out_dir, channel_id):
        super().__init__(in_src, out_dir, channel_id)
        self.ff_segment_out = ffmpeg.output(
            self.ff_input.video,
            self.out_dir + '/playlist.m3u8',
            format='hls',
            vcodec='copy',
            # g=25,
            hls_flags='delete_segments',
            hls_segment_type='fmp4',
            hls_init_time=0,
            hls_list_size=5,
            hls_allow_cache=0,
            hls_time=1).overwrite_output()
  
class CodecX264ResizeHLSFormatSegmenter(BaseSegmenter):

    def __init__(self, in_src, out_dir, channel_id):
        super().__init__(in_src, out_dir, channel_id)
        self.ff_segment_out = (ffmpeg
            .filter(
                self.ff_input.video,
                'scale',
                size='320x240',
                force_original_aspect_ratio='decrease')
            .output(
                self.out_dir + '/playlist.m3u8',
                format='hls',
                preset='ultrafast',
                threads=1,
                vcodec='libx264',
                **{'profile:v':'main'},
                x264opts='keyint=25:min-keyint=25:no-scenecut',
                flags='+cgop',
                hls_flags='delete_segments',
                hls_segment_type='mpegts',
                hls_init_time=0,
                hls_list_size=5,
                hls_allow_cache=0,
                hls_time=1)
            .overwrite_output())

class CodecX264HLSFormatSegmenter(BaseSegmenter):

    def __init__(self, in_src, out_dir, channel_id):
        super().__init__(in_src, out_dir, channel_id)
        self.ff_segment_out = ffmpeg.output(
            self.ff_input.video,
            self.out_dir + '/playlist.m3u8',
            format='hls',
            preset='ultrafast',
            threads=1,
            vcodec='libx264',
            **{'profile:v':'main'},
            x264opts='keyint=25:min-keyint=25:no-scenecut',
            #force_key_frames='expr:gte(t,n_forced*2)',
            flags='+cgop',
            #framerate=25,
            # g=50,
            # bufsize='6M',
            # video_bitrate='3M',
            hls_flags='delete_segments',
            hls_segment_type='',
            #hls_segment_type='fmp4',
            hls_init_time=0,
            hls_list_size=5,
            hls_allow_cache=0,
            hls_time=1).overwrite_output()

class CodecX264SegmentFormatSegmenter(BaseSegmenter):

    def __init__(self, in_src, out_dir, channel_id):
        super().__init__(in_src, out_dir, channel_id)
        self.ff_segment_out = ffmpeg.output(
            self.ff_input.video,
            self.out_dir + '/sample%03d.ts',
            vcodec='libx264',
            preset='ultrafast',
            threads=1,
            **{'profile:v':'main'},
            x264opts='keyint=25:min-keyint=25:no-scenecut',
            flags='+cgop',
            g=25,
            bufsize='6M',
            format='ssegment',
            segment_list=self.out_dir + '/playlist.m3u8',
            segment_wrap=12,
            segment_list_flags='live',
            segment_list_size=10,
            segment_list_type='m3u8',
            segment_time=1).overwrite_output()
    