import aiohttp_jinja2

from aiohttp import web
from webserver import db
from webserver import video_service

@aiohttp_jinja2.template('index.html')
async def index(request):
    items = await db.channel_find_all()
    for channel_item in items:
        channel_item.status = await video_service.get_status(channel_item.channel_id)
    return {'items': items}

@aiohttp_jinja2.template('player.html')
async def player(request):
    channel_id = int(request.match_info['channel_id'])
    try:
        channel_item = await db.channel_find_by_id(channel_id)
        await video_service.start_segmenter_async(channel_item, request.app['hls_root'])
        return {
            'item': channel_item
        }
    except Exception as e:
        raise web.HTTPNotFound(e)

@aiohttp_jinja2.template('add-channel.html')
async def add_channel(request):
    if request.method == 'GET':
        return
    elif request.method == 'POST':
        form_data = await request.post()
        channel_id = await db.channel_create(form_data['description'], 'rtsp://' + form_data['rtsp_link'])
        raise web.HTTPFound(request.app.router['player'].url_for(channel_id=str(channel_id)))
    else:
        raise web.HTTPMethodNotAllowed()

async def del_channel(request):
    channel_id = int(request.match_info['channel_id'])
    await video_service.shutdown(channel_id)
    await db.channel_delete(channel_id)
    return web.HTTPOk()