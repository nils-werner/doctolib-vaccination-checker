import click
import notify, web

@click.command()
@click.argument('location')
@click.option('--biontech/--no-biontech', default=False)
@click.option('--moderna/--no-moderna', default=False)
@click.option('--astrazeneca/--no-astrazeneca', default=False)
@click.option('--janssen/--no-janssen', default=False)
@click.option('--any/--no-any', default=False)
@click.option('--popup/--no-popup', default=False)
@click.option('--slack-url')
@click.option('--remote-executor/--no-remote-executor', default=False)
def poll(
    location,
    biontech,
    moderna,
    astrazeneca,
    janssen,
    any,
    popup,
    slack_url,
    remote_executor
):
    if any:
        biontech, moderna, astrazeneca, janssen = True, True, True, True

    url = web.url(
        location,
        BiontechFirst=biontech,
        ModernaFirst=moderna,
        AZFirst=astrazeneca,
        JanssenFirst=janssen,
    )
    near, far = web.poll(url, remote=remote_executor)

    notify.console(near, far, url)

    if near > 0 or far > 0:
        if popup:
            notify.popup(near, far, url)

        if slack_url is not None:
            notify.slack(
                near, far, url,
                url=slack_url
            )


if __name__ == '__main__':
    poll()
