from sqlmodel import Session, select
from app.models.product_model import Product


def get_all_products(session: Session) -> list[Product]:
    return session.exec(select(Product)).all()


def get_product(session: Session, product_id: int) -> Product | None:
    return session.get(Product, product_id)


def create_product(session: Session, data: dict) -> Product:
    product = Product(**data)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


def update_product(session: Session, product: Product, changes: dict) -> Product:
    for key, value in changes.items():
        if value is not None:
            setattr(product, key, value)

    session.add(product)
    session.commit()
    session.refresh(product)
    return product


def delete_product(session: Session, product: Product) -> None:
    session.delete(product)
    session.commit()
