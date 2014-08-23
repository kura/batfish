import os

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
@click.option('--list', 'action', flag_value='list', default=True)
@click.option('--create', 'action', flag_value='create', default=False)
@click.option('--delete', 'action', flag_value='delete', default=False)
@click.pass_obj
def droplet(ctx, action):
    if action == 'create':
        NotImplemented()
    if action == 'delete':
        NotImplemented()
    else:
        ctx.droplet_list()
