from dagster import (
    load_assets_from_package_module,
    repository,
    define_asset_job,
    ScheduleDefinition,
    with_resources
)
from my_dagster_project import assets
from my_dagster_project.resource import github_api

daily_job = define_asset_job(name="daily_refresh", selection="*")
daily_schedule = ScheduleDefinition(
    job=daily_job,
    cron_schedule="@daily",
)

@repository
def my_dagster_project():
    return [
        daily_job,
        daily_schedule,
        with_resources(load_assets_from_package_module(assets), {
            "github_api": github_api.configured({"access_token": {"env": "GITHUB_ACCESS_TOKEN"}})
        })
    ]
    # creates github client, reads the secret from env, gives the resource to our software defined assets