# RIGHT JOIN
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class TableA(Base):
    __tablename__ = 'table_a'
    id = Column(Integer, primary_key=True)
    common_column = Column(String)
    other_column_a = Column(String)


class TableB(Base):
    __tablename__ = 'table_b'
    id = Column(Integer, primary_key=True)
    common_column = Column(String)
    other_column_b = Column(String)


engine = create_engine('sqlite:///mydatabase.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# right join
result = session.query(TableA, TableB).join(TableB, TableA.common_column == TableB.common_column, isouter=True).all()

for row in result:
    print(f"TableA: {row.TableA.common_column}, TableB: {row.TableB.common_column}")
