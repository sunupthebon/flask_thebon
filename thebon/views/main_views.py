from flask import Blueprint, render_template
from thebon.models import Crawling

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!!'

@bp.route('/')
def index():
    my_crawling_list = Crawling.query.order_by(Crawling.create_date.desc())
    return render_template('crawling/crawling_list.html', crawling_list=my_crawling_list)

@bp.route('/detail/<int:crawling_id>/')
def detail(crawling_id):
    crawling = Crawling.query.get_or_404(crawling_id)
    return render_template('crawling/crawling_detail.html', crawling=crawling)