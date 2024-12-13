from logging import getLogger

from fastapi import FastAPI
from uvicorn import run

from marketplace.config import DefaultSettings
from marketplace.config.utils import get_settings
from marketplace.endpoints import list_of_routes
from marketplace.utils.common import get_hostname


logger = getLogger(__name__)


def bind_routes(application: FastAPI, setting: DefaultSettings) -> None:
    """
    Bind all routes to application.
    """
    for route in list_of_routes:
        application.include_router(route, prefix=setting.PATH_PREFIX)


def get_app() -> FastAPI:
    """
    Creates application and all dependable objects.
    """
    description = '''Микросервис для маркетплейса,
                     позволяющий просматривать список товаров,
                     создавать товары, просматривать информацию о товарах,
                     обновлять товары, удалять товары.'''

    tags_metadata = [
        {
            "name": "Marketplace",
            "description": "Manage marketplace",
        },
        {
            "name": "Health check",
            "description": "API health check.",
        },
    ]

    application = FastAPI(
        title="Marketplace",
        description=description,
        docs_url="/swagger",
        openapi_url="/openapi",
        version="1.0.0",
        openapi_tags=tags_metadata,
    )
    settings = get_settings()
    bind_routes(application, settings)
    application.state.settings = settings
    return application


app = get_app()


if __name__ == "__main__":  # pragma: no cover
    settings_for_application = get_settings()
    run(
        "marketplace.__main__:app",
        host=get_hostname(settings_for_application.APP_HOST),
        port=settings_for_application.APP_PORT,
        reload=True,
        reload_dirs=["marketplace", "tests"],
        log_level="debug",
    )
