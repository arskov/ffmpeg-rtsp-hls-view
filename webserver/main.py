import asyncio
import logging
import pathlib

import aiohttp_jinja2
import jinja2
from aiohttp import web
from webserver.routes import setup_routes
from webserver import video_service

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
PACKAGE_ROOT = pathlib.Path(__file__).parent
TEMPLATES_ROOT = pathlib.Path(__file__).parent / 'templates'

def main():
    app = web.Application()
    app['hls_root'] = str((PROJECT_ROOT/'hls-out').resolve())
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(TEMPLATES_ROOT)))
    setup_routes(app, PACKAGE_ROOT/'static')
    app.on_shutdown.append(video_service.shutdown)
    web.run_app(app)

if __name__ == "__main__":
    main()