import yt_dlp

def cli_to_api(*opts):
    default = yt_dlp.parse_options([]).ydl_opts
    diff = {k: v for k, v in yt_dlp.parse_options(opts).ydl_opts.items() if default[k] != v}
    if 'postprocessors' in diff:
        diff['postprocessors'] = [pp for pp in diff['postprocessors'] if pp not in default['postprocessors']]
    return diff
    
from pprint import pprint

# pprint(cli_to_api('--ppa "ThumbnailsConvertor+FFmpeg_o:-c:v mjpeg -vf crop=\'"if(gt(ih,iw),iw,ih)":"if(gt(iw,ih),ih,iw)"\'"')) 

pprint(cli_to_api('-o "%(title)s.%(ext)s" -o "thumbnail:%(title)s\%(title)s.%(ext)s"')) 