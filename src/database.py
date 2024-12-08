from datetime import datetime, timedelta

from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///products.db', echo=True)
Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    product = Column(String(255), nullable=False)  # Название продукта
    quantity = Column(Float, nullable=False)  # Количество продукта
    quantity_unit = Column(String(50), nullable=False)  # Единица измерения (например, "кг", "шт", "л")
    production_date = Column(DateTime, nullable=False)  # Дата производства
    expiry_date = Column(DateTime, nullable=False)  # Дата истечения срока годности
    expiry_days = Column(Integer, nullable=False)  # Количество дней срока годности

    def __repr__(self):
        return f"<Product(user_id={self.user_id}, product={self.product}, quantity={self.quantity}, unit={self.quantity_unit})>"


def create_tables():
    Base.metadata.create_all(engine)


def add_product(user_id, product, quantity, quantity_unit, production_date, expiry_date, expiry_days):
    Session = sessionmaker(bind=engine)
    session = Session()
    new_product = Product(
        user_id=user_id,
        product=product,
        quantity=quantity,
        quantity_unit=quantity_unit,  # Добавляем единицу измерения
        production_date=production_date,
        expiry_date=expiry_date,
        expiry_days=expiry_days
    )
    session.add(new_product)
    session.commit()
    session.close()


def get_products(user_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    products = session.query(Product).filter(Product.user_id == user_id).all()
    session.close()
    return products


def delete_product(product_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    product_to_delete = session.query(Product).filter(Product.id == product_id).first()
    if product_to_delete:
        session.delete(product_to_delete)
        session.commit()
    session.close()


def get_product_by_id(product_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    product = session.query(Product).filter(Product.id == product_id).first()
    session.close()
    return product


def update_product_name(product_id, new_name):
    Session = sessionmaker(bind=engine)
    session = Session()
    product = session.query(Product).filter(Product.id == product_id).first()
    if product:
        product.product = new_name
        session.commit()
    session.close()


def update_product_quantity(product_id, new_quantity):
    Session = sessionmaker(bind=engine)
    session = Session()
    product = session.query(Product).filter(Product.id == product_id).first()
    if product:
        product.quantity = new_quantity
        session.commit()
    session.close()


def update_product_production_date(product_id, new_production_date):
    if not isinstance(new_production_date, datetime):
        raise TypeError("new_production_date must be a datetime object")

    Session = sessionmaker(bind=engine)
    session = Session()
    product = session.query(Product).filter(Product.id == product_id).first()
    if product:
        # Пересчитываем срок годности
        new_expiry_date = new_production_date + timedelta(days=product.expiry_days)
        product.production_date = new_production_date
        product.expiry_date = new_expiry_date
        session.commit()
    else:
        print(f"Product with ID {product_id} not found.")
    session.close()


def update_product_expiry_days(product_id, new_expiry_days):
    Session = sessionmaker(bind=engine)
    session = Session()

    product = session.query(Product).filter(Product.id == product_id).first()

    if product:
        product.expiry_days = new_expiry_days
        # Пересчитываем дату истечения срока годности
        if product.production_date:
            new_expiry_date = product.production_date + timedelta(days=new_expiry_days)
            product.expiry_date = new_expiry_date
        session.commit()
    session.close()


def update_product_expiry_date(product_id, new_expiry_date):
    Session = sessionmaker(bind=engine)
    session = Session()
    product = session.query(Product).filter(Product.id == product_id).first()
    if product:
        product.expiry_date = new_expiry_date
        session.commit()
    session.close()


create_tables()
