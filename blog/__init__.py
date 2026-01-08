from flask import Blueprint

blog_bp=Blueprint("blog",__name__,url_prefix="/blog")


from blog import routes