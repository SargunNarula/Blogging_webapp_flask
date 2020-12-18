from flask import Blueprint
from flask import render_template
from flask import request


from backend_code.models import Post


main = Blueprint('main',__name__)

#

                                            # Routes

                                        # 1. home
                                        # 2. about


                                        
@main.route("/")
@main.route("/home")
def home_text():

    page = request.args.get('page', 1, type=int)
    #Dynamic Info from database using Paginate() --> To have a limited no of posts in a single page
    blogs = Post.query.order_by(Post.date.desc()).paginate(per_page=5, page=page)
    return render_template("home_html_code.html",posts=blogs, title="Home") 

#different route for different pages
@main.route("/about")
def about_text():
    return render_template("about_html_code.html", title="About")