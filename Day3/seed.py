from models import User, Post, Comment, db
from app import app

with app.app_context():
    # delete all data in database to create new space for data
    User.query.delete()
    Post.query.delete()
    Comment.query.delete()

    # create users
    user1 = User(username='NjoguVic', email='vicnjogu@gmail.com')
    user2 = User(username='levisNgigi', email='levisngigi@gmail.com')
    # save users
    db.session.add_all([user1, user2])
    db.session.commit()

    # ----------------------------------------------------------------
    # create posts
    post1 = Post(pic='http://pic1.jpg', ptime='01-20-2015', user_id=user1.id)
    post2 = Post(pic='http://pic2.jpg', ptime='08-04-2016', user_id=user2.id)
    post3 = Post(pic='http://pic3.jpg', ptime='04-05-2022', user_id=user2.id)
    post4 = Post(pic='http://pic4.jpg', ptime='01-23-2024', user_id=user1.id)

    db.session.add_all([post1, post2, post3, post4])
    db.session.commit()

    # ----------------------------------------------------------------
    # create comment
    comment1 = Comment(description='this comment 1', post_id=post1.id, user_id=user2.id)
    comment2 = Comment(description='this comment 2', post_id=post2.id, user_id=user1.id)
    comment3 = Comment(description='this comment 3', post_id=post4.id, user_id=user2.id)
    comment4 = Comment(description='this comment 4', post_id=post3.id, user_id=user1.id)
    comment5 = Comment(description='this comment 5', post_id=post2.id, user_id=user2.id)

    db.session.add_all([comment1, comment2, comment3, comment4, comment5])
    db.session.commit()
