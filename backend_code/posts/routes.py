
from flask import Blueprint
from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect
from flask import request
from flask import abort

from flask_login import current_user 
from flask_login import login_required

from backend_code import db

from backend_code.models import Post

from backend_code.posts.forms import CreatePost

posts = Blueprint('posts',__name__)


# 
                                            # Post Routes
                                        
                                        # 1. post
                                        # 2. new    post
                                        # 3. update post
                                        # 4. delete post  
        # <!-------------------------------------------------------------------------------------------------->


@posts.route("/posts/<int:post_id>")
def post(post_id):
    post_instance = Post.query.get_or_404(post_id)
    return render_template("post_html_code.html", title="Post", post=post_instance)

@posts.route("/posts/new", methods=['GET','POST'])
@login_required
def new_post():
    new_post_instance = CreatePost()
    if new_post_instance.validate_on_submit():
        blog = Post(title=new_post_instance.title.data, content=new_post_instance.content.data, author=current_user)
        db.session.add(blog)
        db.session.commit()

        flash('Your Post has been created','success')
        return redirect(url_for('main.home_text'))
    return render_template("create_post_html_code.html", title="New Post", form=new_post_instance, legend="New Post")

# We did not create a separate form and template to update the post
# Rather just made changes to create_post template through a legend
# We just used the create post form too

@posts.route("/posts/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id):
    
    update_post_instance = Post.query.get_or_404(post_id)
    
    if update_post_instance.author != current_user:
        abort(403)
    
    update_form   = CreatePost()
    
    if update_form.validate_on_submit():
        update_post_instance.title   = update_form.title.data
        update_post_instance.content = update_form.content.data
        db.session.commit()
        flash('Updated Changes Successfully', 'success')
        return redirect(url_for('posts.post', post_id=update_post_instance.id))

    elif request.method == 'GET':
        update_form.title.data   = update_post_instance.title
        update_form.content.data = update_post_instance.content
    return render_template("create_post_html_code.html", title="Update Post", form=update_form, legend="Update Post" )

@posts.route("/posts/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    
    delete_post_instance = Post.query.get_or_404(post_id)
    
    if delete_post_instance.author != current_user:
        abort(403)
    db.session.delete(delete_post_instance)
    db.session.commit()
    flash('Post Deleted Successfully', 'danger')
    return redirect(url_for('main.home_text'))