from typing import Literal
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from marketplace.utils.converter import converter
from marketplace.db.connection import get_session
from marketplace.db.models import Product
from marketplace.schemas import ProductSchema, ProductWithTimeSchema, ProductsSchema


api_router = APIRouter(tags=["Marketplace"])


@api_router.get(
    "/products/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductWithTimeSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Link with this product id is not found.",
        }
    },
)
async def get_product(
    product_id: int,
    currency: Literal['RUB', 'USD'] = 'RUB',
    session: AsyncSession = Depends(get_session),
):
    db_product_query = select(Product).where(Product.id == product_id)
    db_product = await session.scalar(db_product_query)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link with this product id is not found.",
        )
    if db_product.currency != currency:
        value = await converter()
        if currency == 'USD':
            db_product.price = db_product.price/value
        elif currency == 'RUB':
            db_product.price = db_product.price*value
        db_product.currency = currency
        db_product.price = round(db_product.price, 2)

    return ProductWithTimeSchema.from_orm(db_product)


@api_router.post(
    "/products",
    response_model=ProductWithTimeSchema,
    status_code=status.HTTP_200_OK,
)
async def create_product(
    product: ProductSchema,
    session: AsyncSession = Depends(get_session),
):
    new_product = Product(name=product.name,
                          description=product.description,
                          price=product.price,
                          currency=product.currency,
                          category=product.category
                          )
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product),
    return ProductWithTimeSchema.from_orm(new_product)


@api_router.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_product(
    product_id: int,
    session: AsyncSession = Depends(get_session),
):
    query = select(Product).where(Product.id == product_id)
    query = await session.scalar(query)
    if query is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link with this product id is not found.",
        )
    await session.delete(query)
    await session.commit()


@api_router.put(
    "/products/{product_id}",
    response_model=ProductWithTimeSchema,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Link with this product id is not found.",
        },
    },
)
async def update_product(
    product_id: int,
    product: ProductSchema,
    session: AsyncSession = Depends(get_session),
):

    db_product_query = select(Product).where(Product.id == product_id)
    db_product = await session.scalar(db_product_query)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link with this product id is not found.",
        )
    db_product.name = product.name
    db_product.currency = product.currency
    db_product.category = product.category
    db_product.description = product.description
    db_product.price = product.price
    session.add(db_product)
    await session.commit()
    await session.refresh(db_product)
    return ProductWithTimeSchema.from_orm(db_product)


@api_router.get(
    "/products",
    response_model=ProductsSchema,
)
async def get_products(
    page: int = 1,
    per_page: int = 20,
    min_price: float | None = None,
    max_price: float | None = None,
    category: str | None = None,
    currency: Literal['RUB', 'USD'] = 'RUB',
    session: AsyncSession = Depends(get_session),
):
    if min_price is None:
        min_price = 0
    if max_price is None:
        max_price = float(10**30)
    value = await converter()
    db_products_query = select(Product)
    if currency == 'USD':
        db_products_query = db_products_query.filter(or_(and_(Product.currency == 'RUB', Product.price/value >= min_price), and_(Product.currency == 'USD', Product.price >= min_price)))
        db_products_query = db_products_query.filter(or_(and_(Product.currency == 'RUB', Product.price/value <= max_price), and_(Product.currency == 'USD', Product.price <= max_price)))
    elif currency == 'RUB':
        db_products_query = db_products_query.filter(or_(and_(Product.currency == 'RUB', Product.price >= min_price), and_(Product.currency == 'USD', Product.price*value >= min_price)))
        db_products_query = db_products_query.filter(or_(and_(Product.currency == 'RUB', Product.price <= max_price), and_(Product.currency == 'USD', Product.price*value <= max_price)))
    if category is not None:
        db_products_query = db_products_query.where(Product.category == category)
    db_products = await session.execute(db_products_query)
    db_products = db_products.scalars().all()
    total = len(db_products)
    pages = (total + per_page - 1)//per_page
    db_products_query = db_products_query.offset(per_page*(page-1))
    db_products_query = db_products_query.limit(per_page)
    db_products = await session.execute(db_products_query)
    db_products = db_products.scalars().all()
    for item in db_products:
        if item.currency != currency:
            if currency == 'USD':
                item.price = item.price/value
            elif currency == 'RUB':
                item.price = item.price*value
            item.price = round(item.price, 2)
        item.currency = currency
    result = {"items": db_products,
              "total": total,
              "page": page,
              "per_page": per_page,
              "pages": pages
              }
    return result
