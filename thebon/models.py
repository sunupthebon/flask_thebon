from thebon import db

class Crawling(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    link = db.Column(db.Text(), nullable=False)
    snippet = db.Column(db.Text(), nullable=False)
    pub_date = db.Column(db.Text())
    sni_tran = db.Column(db.Text())
    create_date = db.Column(db.DateTime(), nullable=False)

class Article_download(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crawling_id = db.Column(db.Integer, db.ForeignKey('crawling.id', ondelete='CASCADE'))
#   question = db.relationship('Question', backref=db.backref('answer_set', cascade='all, delete-orphan'))
    crawling = db.relationship('Crawling', backref=db.backref('article_set', cascade='all, delete-orphan')) #역참조가 가능하도록 설정함
    summary	= db.Column(db.Text())
    sum_tran = db.Column(db.Text())
    body_text = db.Column(db.Text())
    body_tran = db.Column(db.Text())

class Machine_learning(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crawling_id = db.Column(db.Integer, db.ForeignKey('crawling.id', ondelete='CASCADE'))
    crawling = db.relationship('Crawling', backref=db.backref('Machine_set', cascade='all, delete-orphan'))  # 역참조가 가능하도록 설정함
    news_val = db.Column(db.Integer)
    art_val = db.Column(db.Integer)
    cos_val = db.Column(db.Integer)
    ml_val = db.Column(db.Integer)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    p_member = db.Column(db.Integer)
    search_word = db.Column(db.String(150))

class User_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User', backref=db.backref('User_set', cascade='all, delete-orphan'))  # 역참조가 가능하도록 설정함
    search_word = db.Column(db.String(150), nullable=False)


