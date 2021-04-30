from flask import render_template, url_for, flash, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from todoapplication import db
from todoapplication.models import TodoPost
from todoapplication.todo_list.forms import TodoListForm

todo_posts = Blueprint("todo_posts", __name__)


@todo_posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = TodoListForm()
    if form.validate_on_submit():
        todo_post = TodoPost(title=form.title.data,
                             text=form.text.data,
                             user_id=current_user.id)
        db.session.add(todo_post)
        db.session.commit()
        flash("Todo Post Created!")
        return redirect(url_for('core.index'))
    return render_template('create_post.html', form=form)


@todo_posts.route('/<int:todo_post_id>')
def todo_post(todo_post_id):
    todo_post = TodoPost.query.get_or_404(todo_post_id)
    return render_template('todo_post.html', title=todo_post.title,
                           date=todo_post.date, post=todo_post)


@todo_posts.route('/<int:todo_post_id>/update', methods=['GET', 'POST'])
@login_required
def update(todo_post_id):
    todo_post = TodoPost.query.get_or_404(todo_post_id)

    if todo_post.author != current_user:
        abort(403)

    form = TodoListForm()

    if form.validate_on_submit():

        todo_post.title = form.title.data
        todo_post.text = form.text.data

        db.session.commit()
        flash("Todo Post Updated!")
        return redirect(url_for('todo_posts.todo_post', todo_post_id=todo_post.id))

    elif request.method == 'GET':
        form.title.data = todo_post.title
        form.text.data = todo_post.text

    return render_template('create_post.html', title='Updating', form=form)


@todo_posts.route('/<int:todo_post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(todo_post_id):

    todo_post = TodoPost.query.get_or_404(todo_post_id)
    if todo_post.author != current_user:
        abort(403)

    db.session.delete(todo_post)
    db.session.commit()
    flash("Todo Post Deleted!")
    return redirect(url_for('core.index'))
