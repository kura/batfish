from cmd import Cmd

from .client import Client
from .models.region import Region
from .models.size import Size


class Batfish(Cmd):
    ctx = Client()

    def do_authorize(self, token):
        print self.ctx.authorize(token)

    def print_droplet(self, name, cpu, memory, disk, ip, status, region, did):
        print """{0} [id: {1}] (cpu(s): {2}, mem: {3}MB, disk: {4}, """ \
              """ip: {5}, status: {6}, region: {7})""".format(name, did,
              cpu, memory, disk, ip, status, region)

    def do_droplets(self, *args):
        for droplet in self.ctx.droplets:
            self.print_droplet(droplet.name, droplet.cpus, droplet.memory,
                               droplet.disk_size,
                               droplet.networks['ipv4'][0].ip,
                               droplet.status, droplet.region_name,
                               droplet.id)

    def do_droplet(self, droplet):
        if droplet.isdigit():
            droplet = self.ctx.droplet_from_id(droplet)
        else:
            droplet = self.ctx.droplet_from_name(droplet)
        self.print_droplet(droplet.name, droplet.cpus, droplet.memory,
                           droplet.disk_size,
                           droplet.networks['ipv4'][0].ip,
                           droplet.status, droplet.region_name,
                           droplet.id)

    def do_droplet_password_reset(self, droplet):
        accept = raw_input("Are you sure you want to do this? [y/N]: ")
        if accept.lower() != 'y':
            return
        if droplet.isdigit():
            droplet = self.ctx.droplet_from_name(droplet)
            droplet = droplet.id
        self.ctx.droplet_password_reset(droplet)

    def do_droplet_power_cycle(self, droplet):
        accept = raw_input("Are you sure you want to do this? [y/N]: ")
        if accept.lower() != 'y':
            return
        if droplet.isdigit():
            droplet = self.ctx.droplet_from_name(droplet)
            droplet = droplet.id
        self.ctx.droplet_power_cycle(droplet)

    def do_droplet_power_off(self, droplet):
        accept = raw_input("Are you sure you want to do this? [y/N]: ")
        if accept.lower() != 'y':
            return
        if droplet.isdigit():
            droplet = self.ctx.droplet_from_name(droplet)
            droplet = droplet.id
        self.ctx.droplet_power_off(droplet)

    def do_droplet_power_on(self, droplet):
        if droplet.isdigit():
            droplet = self.ctx.droplet_from_name(droplet)
            droplet = droplet.id
        self.ctx.droplet_power_on(droplet)

    def droplet_reboot(self, droplet):
        accept = raw_input("Are you sure you want to do this? [y/N]: ")
        if accept.lower() != 'y':
            return
        if droplet.isdigit():
            droplet = self.ctx.droplet_from_name(droplet)
            droplet = droplet.id
        self.ctx.droplet_reboot(droplet)

    def droplet_shutdown(self, droplet):
        accept = raw_input("Are you sure you want to do this? [y/N]: ")
        if accept.lower() != 'y':
            return
        if droplet.isdigit():
            droplet = self.ctx.droplet_from_name(droplet)
            droplet = droplet.id
        self.ctx.droplet_shutdown(droplet)

    def do_droplet_restore(self, droplet, image):
        accept = raw_input("Are you sure you want to do this? [y/N]: ")
        if accept.lower() != 'y':
            return
        if droplet.isdigit():
            droplet = self.ctx.droplet_from_name(droplet)
            droplet = droplet.id
        if not image.isdigit():
            # assume name first, then try slug
            image = self.ctx.image_from_name(image)
            if image is None:
                image = self.ctx.image_from_slug(image)
            image = image.id
        self.ctx.droplet_rebuild(droplet, image)

    def do_droplet_create(self, name, region, size, image):
        self.ctx.droplet_create(name, region, size, image)

    def do_droplet_delete(self, droplet):
        accept = raw_input("Are you sure you want to do this? [y/N]: ")
        if accept.lower() != 'y':
            return
        if droplet.isdigit():
            droplet = self.ctx.droplet_from_name(droplet)
            droplet = droplet.id
        self.ctx.droplet_delete(droplet)

    def do_droplet_rename(self, droplet, name):
        if droplet.isdigit():
            droplet = self.ctx.droplet_from_name(droplet)
            droplet = droplet.id
        self.ctx.droplet_rename(droplet, name)

    def do_droplet_resize(self, droplet, size):
        if droplet.isdigit():
            droplet = self.ctx.droplet_from_name(droplet)
            droplet = droplet.id
        self.ctx.droplet_resize(droplet, size)

    def do_droplet_enabled_ipv6(self, droplet):
        if droplet.isdigit():
            droplet = self.ctx.droplet_from_name(droplet)
            droplet = droplet.id
        self.ctx.droplet_enabled_ipv6(droplet)

    def do_droplet_disable_backups(self, droplet):
        accept = raw_input("Are you sure you want to do this? [y/N]: ")
        if accept.lower() != 'y':
            return
        if droplet.isdigit():
            droplet = self.ctx.droplet_from_name(droplet)
            droplet = droplet.id
        self.ctx.droplet_disable_backups(droplet)

    def do_droplet_enable_private_networking(self, droplet):
        if droplet.isdigit():
            droplet = self.ctx.droplet_from_name(droplet)
            droplet = droplet.id
        self.ctx.droplet_enable_private_networking(droplet)

    def print_image(self, iid, name, slug, distribution, regions):
        print """{0} [id: {1}] (slug: {2}, distribution: {3}, """ \
              """regions: [{4}])""".format(name, iid, slug,
              distribution, ", ".join(regions))

    def do_images(self, *args):
        for image in self.ctx.images:
            self.print_image(image.id, image.name, image.slug,
                             image.distribution, image.region_names)

    def do_image(self, image):
        if image.isdigit():
            image = self.ctx.image_from_id(image)
        else:
            image = self.ctx.image_from_name(image)
            if image is None:
                image = self.ctx.image_from_slug(image)
        self.print_image(image.id, image.name, image.slug,
                         image.distribution, image.region_names)

    def do_image_delete(self, image):
        accept = raw_input("Are you sure you want to do this? [y/N]: ")
        if accept.lower() != 'y':
            return
        if image.isdigit():
            image = self.ctx.image_from_name(image)
        else:
            if image is None:
                image = self.ctx.image_from_slug(image)
            image = image.id
        self.ctx.image_delete(image)

    def do_image_rename(self, image, name):
        if image.isdigit():
            image = self.ctx.image_from_name(image)
        else:
            if image is None:
                image = self.ctx.image_from_slug(image)
            image = image.id
        self.ctx.image_rename(image, name)

    def do_image_transfer(self, image, region):
        if image.isdigit():
            image = self.ctx.image_from_name(image)
        else:
            if image is None:
                image = ctx.self.image_from_slug(image)
            image = image.id
        self.ctx.image_transfer(image, region)

    def print_size(self, name, cpus, disk_size, price, regions):
        print """{0} (cpu(s): {1}, memory: {0}, disk: {2}) """ \
              """(price: {3}/hour {4}/month) regions: [{5}]""".format(name,
              cpus, disk_size, price.hourly, price.monthly,
              ", ".join(regions))

    def do_sizes(self, detailed=False):
        if not detailed:
            for size in Size.mappings():
                print size
            return
        for size in self.ctx.sizes():
            self.print_size(size.slug.upper(), size.cpus, size.disk_size,
                            size.price, size.region_names)

    def do_quit(self, args):
        """Quits the program."""
        raise SystemExit


def shell():
    try:
        prompt = Batfish()
        prompt.prompt = 'batfish > '
        prompt.cmdloop()
    except KeyboardInterrupt:
        raise SystemExit
