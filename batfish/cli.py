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


from sys import stdout

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


def print_droplet(name, cpu, memory, disk, ip, status, region, did):
    if status == "active":
        colour = 'green'
    else:
        colour = 'red'
    click.echo("""{0} [id: {1}] (cpu(s): {2}, mem: {3}MB, disk: {4}, """
               """ip: {5}, {6}, region: {7})""".format(name, did, cpu, memory,
               disk, ip, click.style("status: {0}".format(status), fg=colour),
               region))

@cli.command()
@click.pass_obj
def droplets(ctx):
    for droplet in ctx.droplets():
        print_droplet(droplet.name, droplet.cpus, droplet.memory,
                      droplet.disk_size, droplet.networks['ipv4'][0].ip,
                      droplet.status, droplet.region(ctx).name,
                      droplet.id)


@cli.command()
@click.option('--droplet', help="Droplet name or ID")
@click.pass_obj
def droplet(ctx, droplet):
    if droplet.isdigit():
        droplet = ctx.droplet_from_id(droplet)
    else:
        droplet = ctx.droplet_from_name(droplet)
    print_droplet(droplet.name, droplet.cpus, droplet.memory,
                  droplet.disk_size, droplet.networks['ipv4'][0].ip,
                  droplet.status, droplet.region(ctx).name,
                  droplet.id)


@cli.command()
@click.option('--droplet', help="Droplet name or ID")
@click.option('--accept', is_flag=True,
              prompt="Are you sure you want to do this?")
@click.pass_obj
def password_reset(ctx, droplet, accept):
    if accept is False:
        return
    if droplet.isdigit():
        droplet = ctx.droplet_from_id(droplet)
    else:
        droplet = ctx.droplet_from_name(droplet)
    ctx.droplet('password_reset', droplet)


@cli.command()
@click.option('--droplet', help="Droplet name or ID")
@click.option('--accept', is_flag=True,
              prompt="Are you sure you want to do this?")
@click.pass_obj
def power_cycle(ctx, droplet, accept):
    if accept is False:
        return
    if droplet.isdigit():
        droplet = ctx.droplet_from_id(droplet)
    else:
        droplet = ctx.droplet_from_name(droplet)
    ctx.droplet('power_cycle', droplet)


@cli.command()
@click.option('--droplet', help="Droplet name or ID")
@click.option('--accept', is_flag=True,
              prompt="Are you sure you want to do this?")
@click.pass_obj
def power_off(ctx, droplet, accept):
    if accept is False:
        return
    if droplet.isdigit():
        droplet = ctx.droplet_from_id(droplet)
    else:
        droplet = ctx.droplet_from_name(droplet)
    ctx.droplet('power_off', droplet)


@cli.command()
@click.option('--droplet', help="Droplet name or ID")
@click.pass_obj
def power_on(ctx, droplet):
    if droplet.isdigit():
        droplet = ctx.droplet_from_id(droplet)
    else:
        droplet = ctx.droplet_from_name(droplet)
    ctx.droplet('power_on', droplet)


@cli.command()
@click.option('--droplet', help="Droplet name or ID")
@click.option('--accept', is_flag=True,
              prompt="Are you sure you want to do this?")
@click.pass_obj
def reboot(ctx, droplet, accept):
    if accept is False:
        return
    if droplet.isdigit():
        droplet = ctx.droplet_from_id(droplet)
    else:
        droplet = ctx.droplet_from_name(droplet)
    ctx.droplet('reboot', droplet)


@cli.command()
@click.option('--droplet', help="Droplet name or ID")
@click.option('--accept', is_flag=True,
              prompt="Are you sure you want to do this?")
@click.pass_obj
def shutdown(ctx, droplet, accept):
    if accept is False:
        return
    if droplet.isdigit():
        droplet = ctx.droplet_from_id(droplet)
    else:
        droplet = ctx.droplet_from_name(droplet)
    ctx.droplet('shutdown', droplet)
