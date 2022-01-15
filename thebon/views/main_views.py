from flask import Blueprint, url_for
from werkzeug.utils import redirect

#from flask import Blueprint, render_template
#from thebon.models import Crawling

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello_pybo():
    return 'main_views.py : Hello, Pybo!!'

@bp.route('/')
def index():
    return redirect(url_for('crawling.search_list'))

#@bp.route('/detail/<int:crawling_id>/')
#def detail(crawling_id):
#    crawling = Crawling.query.get_or_404(crawling_id)
#    return render_template('crawling/crawling_detail.html', crawling=crawling)

