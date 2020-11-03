from webserver.views import index, player, add_channel, del_channel

def setup_routes(app, static_root):
    app.router.add_get('/', index, name='index')
    app.router.add_get('/channels/{channel_id}', player, name='player')
    app.router.add_delete('/channels/{channel_id}', del_channel, name='del_channel')
    app.router.add_get('/add', add_channel, name='add_channel')
    app.router.add_post('/add', add_channel, name='post_channel')
    # in prod static content folders and files should be handled by nginx for instance
    app.router.add_static('/static/', path=static_root, name='static')
    app.router.add_static('/hls/', path=app['hls_root'], name='hls')