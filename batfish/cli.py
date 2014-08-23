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
