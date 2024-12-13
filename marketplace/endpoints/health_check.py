from fastapi import APIRouter, Depends, HTTPException, Request
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from marketplace.schemas import PingResponse

from marketplace.db.connection import get_session
from marketplace.utils.health_check import health_check_db


api_router = APIRouter(tags=["Health check"])


@api_router.get(
    "/health_check/ping",
    response_model=PingResponse,
    status_code=status.HTTP_200_OK,
)
async def health_check():
    return PingResponse()


@api_router.get(
    "/ping_database",
    response_model=PingResponse,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_500_INTERNAL_SERVER_ERROR:
               {"description": "Database isn't working"}},
)
async def ping_database(
    _: Request,
    session: AsyncSession = Depends(get_session),
):
    if await health_check_db(session):
        return {"message": "Database worked!"}
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Database isn't working",
    )
