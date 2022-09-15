import abc
import model


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: model.Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> model.Batch:
        raise NotImplementedError


class SqlRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch):
        # self.session.execute('INSERT INTO ??
        self.session.add(batch)

    def get(self, reference) -> model.Batch:
        # self.session.execute('SELECT ??
        return self.session.query(model.Batch).filter_by(reference=reference).one()
    
    def list(self):
        return self.sesseion.query(model.Batch).all()
