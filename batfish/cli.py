import click


@click.group()
@click.pass_context
def cli(ctx):
    pass


@click.command()
@click.option('--token', prompt="Token")
def authorize(token):
    print token


if __name__ == '__main__':
    cli()
