from flask import Blueprint, render_template
from flask import request

from mdblog.models import Article

blog = Blueprint("blog", __name__)

## s metódou GET na čítanie článkov
@blog.route('/articles/', methods=["GET"])
def view_articles():
    page = request.args.get("page", 1, type=int)
    paginate = Article.query.order_by(Article.id.desc()).paginate(page, 3, False)
    return render_template("mod_blog/articles.jinja", 
    articles=paginate.items, ##pre zobrazenie článkov
    paginate=paginate) ## potrebné pre zobrazenie číslovania

##Zobrazenie article
@blog.route('/articles/<int:art_id>/')
def view_article(art_id):
    article = Article.query.filter_by(id=art_id).first()
    if article:
        return render_template("mod_blog/article.jinja", article=article)
    return render_template("mod_blog/article_not_found.jinja", art_id=art_id)
