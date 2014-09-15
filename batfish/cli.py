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
from .models import Region, Size


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
    for droplet in ctx.droplets:
        print_droplet(droplet.name, droplet.cpus, droplet.memory,
                      droplet.disk_size, droplet.networks['ipv4'][0].ip,
                      droplet.status, droplet.region_name,
                      droplet.id)


@cli.command()
@click.option('--droplet', help="Droplet name or ID", required=True)
@click.pass_obj
def droplet(ctx, droplet):
    if droplet.isdigit():
        droplet = ctx.droplet_from_id(droplet)
    else:
        droplet = ctx.droplet_from_name(droplet)
    print_droplet(droplet.name, droplet.cpus, droplet.memory,
                  droplet.disk_size, droplet.networks['ipv4'][0].ip,
                  droplet.status, droplet.region_name,
                  droplet.id)


@cli.command()
@click.option('--droplet', help="Droplet name or ID", required=True)
@click.option('--accept', is_flag=True,
              prompt="Are you sure you want to do this?")
@click.pass_obj
def droplet_password_reset(ctx, droplet, accept):
    if accept is False:
        return
    if not droplet.isdigit():
        droplet = ctx.droplet_from_name(droplet)
        droplet = droplet.id
    ctx.droplet_password_reset(droplet)


@cli.command()
@click.option('--droplet', help="Droplet name or ID", required=True)
@click.option('--accept', is_flag=True,
              prompt="Are you sure you want to do this?")
@click.pass_obj
def droplet_power_cycle(ctx, droplet, accept):
    if accept is False:
        return
    if not droplet.isdigit():
        droplet = ctx.droplet_from_name(droplet)
        droplet = dtoplet.id
    ctx.droplet_power_cycle(droplet)


@cli.command()
@click.option('--droplet', help="Droplet name or ID", required=True)
@click.option('--accept', is_flag=True,
              prompt="Are you sure you want to do this?")
@click.pass_obj
def droplet_power_off(ctx, droplet, accept):
    if accept is False:
        return
    if not droplet.isdigit():
        droplet = ctx.droplet_from_name(droplet)
        droplet = droplet.id
    ctx.droplet_power_off(droplet)


@cli.command()
@click.option('--droplet', help="Droplet name or ID", required=True)
@click.pass_obj
def droplet_power_on(ctx, droplet):
    if not droplet.isdigit():
        droplet = ctx.droplet_from_name(droplet)
        droplet = droplet.id
    ctx.droplet_power_on(droplet)


@cli.command()
@click.option('--droplet', help="Droplet name or ID", required=True)
@click.option('--accept', is_flag=True,
              prompt="Are you sure you want to do this?")
@click.pass_obj
def droplet_reboot(ctx, droplet, accept):
    if accept is False:
        return
    if not droplet.isdigit():
        droplet = ctx.droplet_from_name(droplet)
        droplet = droplet.id
    ctx.droplet_reboot(droplet)


@cli.command()
@click.option('--droplet', help="Droplet name or ID", required=True)
@click.option('--accept', is_flag=True,
              prompt="Are you sure you want to do this?")
@click.pass_obj
def droplet_shutdown(ctx, droplet, accept):
    if accept is False:
        return
    if not droplet.isdigit():
        droplet = ctx.droplet_from_name(droplet)
        droplet = droplet.id
    ctx.droplet_shutdown(droplet)


@cli.command()
@click.option('--droplet', help="Droplet name or ID", required=True)
@click.option('--image', help="Droplet name, slug or ID", required=True)
@click.option('--accept', is_flag=True,
              prompt="Are you sure you want to do this?")
@click.pass_obj
def droplet_restore(ctx, droplet, image, accept):
    if accept is False:
        return
    if not droplet.isdigit():
        droplet = ctx.droplet_from_name(droplet)
        droplet = droplet.id
    if not image.isdigit():
        # assume name first, then try slug
        image = ctx.image_from_name(image)
        if image is None:
            image = ctx.image_from_slug(image)
        image = image.id
    ctx.droplet_restore(droplet, image)


@cli.command()
@click.option('--droplet', help="Droplet name or ID", required=True)
@click.option('--image', help="Droplet name, slug or ID", required=True)
@click.option('--accept', is_flag=True,
              prompt="Are you sure you want to do this?")
@click.pass_obj
def droplet_rebuild(ctx, droplet, image, accept):
    if accept is False:
        return
    if not droplet.isdigit():
        droplet = ctx.droplet_from_name(droplet)
        droplet = droplet.id
    if not image.isdigit():
        # assume name first, then try slug
        image = ctx.image_from_name(image)
        if image is None:
            image = ctx.image_from_slug(image)
        image = image.id
    ctx.droplet_rebuild(droplet, image)


@cli.command()
@click.option('--name', help="Droplet name", required=True)
@click.option('--region', type=click.Choice(sorted(Region.mapping.keys())),
              required=True)
@click.option('--size', type=click.Choice(Size.mapping), required=True)
@click.option('--image', help="Image name, slug or ID", required=True)
@click.pass_obj
def droplet_create(ctx, name, region, size, image):
    ctx.droplet_create(name, region, size, image)


@cli.command()
@click.option('--droplet', help="Droplet name or ID", required=True)
@click.option('--name', help="New droplet name", required=True)
@click.pass_obj
def droplet_rename(ctx, droplet, name):
    if not droplet.isdigit():
        droplet = ctx.droplet_from_name(droplet)
        droplet = droplet.id
    ctx.droplet_rename(droplet, name)


@cli.command()
@click.option('--droplet', help="Droplet name or ID", required=True)
@click.option('--accept', is_flag=True,
              prompt="Are you sure you want to do this?")
@click.pass_obj
def droplet_delete(ctx, droplet, accept):
    if accept is False:
        return
    if not droplet.isdigit():
        droplet = ctx.droplet_from_name(droplet)
        droplet = droplet.id
    ctx.droplet_delete(droplet)


@cli.command()
@click.option('--droplet', help="Droplet name or ID", required=True)
@click.option('--size', type=click.Choice(Size.mapping), required=True)
@click.pass_obj
def droplet_resize(ctx, droplet, size):
    if not droplet.isdigit():
        droplet = ctx.droplet_from_name(droplet)
        droplet = droplet.id
    ctx.droplet_resize(droplet, size)


@cli.command()
@click.option('--droplet', help="Droplet name or ID", required=True)
@click.pass_obj
def droplet_enabled_ipv6(ctx, droplet):
    if not droplet.isdigit():
        droplet = ctx.droplet_from_name(droplet)
        droplet = droplet.id
    ctx.droplet_enable_ipv6(droplet)


@cli.command()
@click.option('--droplet', help="Droplet name or ID", required=True)
@click.option('--accept', is_flag=True,
              prompt="Are you sure you want to do this?")
@click.pass_obj
def droplet_disable_backups(ctx, droplet, accept):
    if accept is False:
        return
    if not droplet.isdigit():
        droplet = ctx.droplet_from_name(droplet)
        droplet = droplet.id
    ctx.droplet_disable_backups(droplet)


@cli.command()
@click.option('--droplet', help="Droplet name or ID", required=True)
@click.pass_obj
def droplet_enable_private_networking(ctx, droplet):
    if not droplet.isdigit():
        droplet = ctx.droplet_from_name(droplet)
        droplet = droplet.id
    ctx.droplet_enable_private_networking(droplet)


def print_image(iid, name, slug, distribution, regions):
    click.echo("""{0} [id: {1}] (slug: {2}, distribution: {3}, """
               """regions: [{4}])""".format(name, iid, slug,
               distribution, ", ".join(regions)))


@cli.command()
@click.pass_obj
def images(ctx):
    for image in ctx.images:
        print_image(image.id, image.name, image.slug, image.distribution,
                    image.region_names)


@cli.command()
@click.option('--images', help="Image name, slug or ID", required=True)
@click.pass_obj
def image(ctx, image):
    if image.isdigit():
        image = ctx.image_from_id(image)
    else:
        # assume name first, then try slug
        image = ctx.image_from_name(image)
        if image is None:
            image = ctx.image_from_slug(image)
    print_image(image.id, image.name, image.slug, image.distribution,
                image.region_names)


@cli.command()
@click.option('--image', help="Image name, slug or ID", required=True)
@click.option('--accept', is_flag=True,
              prompt="Are you sure you want to do this?")
@click.pass_obj
def image_delete(ctx, image, accept):
    if accept is False:
        return
    if image.isdigit():
        image = ctx.image_from_id(image)
    else:
        # assume name first, then try slug
        image = ctx.image_from_name(image)
        if image is None:
            image = ctx.image_from_slug(image)
    ctx.image_delete(image)


@cli.command()
@click.option('--image', help="Image name, slug or ID", required=True)
@click.option('--name', required=True)
@click.pass_obj
def image_rename(ctx, image, name):
    if image.isdigit():
        image = ctx.image_from_id(image)
    else:
        # assume name first, then try slug
        image = ctx.image_from_name(image)
        if image is None:
            image = ctx.image_from_slug(image)
    ctx.image_rename(image, name)


@cli.command()
@click.option('--image', help="Image name, slug or ID", required=True)
@click.option('--region', type=click.Choice(sorted(Region.mapping.keys())),
              required=True)
@click.pass_obj
def image_transfer(ctx, image, region):
    if image.isdigit():
        image = ctx.image_from_id(image)
    else:
        # assume name first, then try slug
        image = ctx.image_from_name(image)
        if image is None:
            image = ctx.image_from_slug(image)
    ctx.image_transfer(image, region)


def print_size(name, cpus, disk_size, price, regions):
    click.echo("""{0} (cpu(s): {1}, memory: {0}, disk: {2}) """
               """(price: {3}/hour {4}/month) regions: [{5}]""".format(name,
               cpus, disk_size, price.hourly, price.monthly,
               ", ".join(regions)))


@cli.command()
@click.option('--detailed', is_flag=True, default=False,
              help="Displays a detailed view of sizes")
@click.pass_obj
def sizes(ctx, detailed):
    if not detailed:
        for size in Size.mappings():
            click.echo(size)
        return
    for size in ctx.sizes:
        print_size(size.slug.upper(), size.cpus, size.disk_size, size.price,
                   size.region_names)
