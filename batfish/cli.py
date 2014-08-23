# -*- coding: utf-8 -*-

# (The MIT License)
#
# Copyright (c) 2014 Kura
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import click

from .client import Client


@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = Client()


@cli.command()
@click.option('--token', prompt="Token")
@click.pass_obj
def authorize(ctx, token):
    resp = ctx.authorize(token)
    print resp


@cli.command()
@click.option('--list', is_flag=True,)
@click.option('--view', type=int)
@click.option('--create', is_flag=True)
@click.option('--delete', type=int)
@click.pass_obj
def droplet(ctx, list=True, view=None, create=False, delete=None):
    if view is not None:
        droplet_view(ctx, view)
    elif create is True:
        droplet_create(ctx)
    elif delete is not None:
        droplet_delete(ctx)
    else:
        droplet_list(ctx)


def droplet_list(ctx):
    ctx.list_droplets()


def droplet_view(ctx, droplet_id):
    ctx.droplet_from_id(droplet_id)


def droplet_create(ctx):
    pass


def droplet_delete(ctx, droplet_id):
    pass
