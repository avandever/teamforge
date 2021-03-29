#!/usr/bin/env python3
import click
import click_log
from util import (
    create_test_data,
    read_config,
    SessionFactory,
)


@click.group()
@click_log.simple_verbosity_option()
@click.option("-c", "--config", type=str, default="dbconfig.ini")
@click.pass_context
def cli(ctx, config):
    ctx.ensure_object(dict)
    cparser = read_config(config)
    ctx.obj["CONFIG"] = cparser
    ctx.obj["SESSION_FACTORY"] = SessionFactory(**cparser["db"])


@cli.command()
@click.pass_context
def init_db(ctx):
    session = ctx.obj["SESSION_FACTORY"]()


@cli.command()
@click.pass_context
def create_test(ctx):
    session = ctx.obj["SESSION_FACTORY"]()
    create_test_data(session)


if __name__ == "__main__":
    cli(obj={})
