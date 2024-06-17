import graphene
from graphene_django.types import DjangoObjectType
from .models import Post, Comment
from django.contrib.auth.models import User
from graphql_jwt.decorators import login_required

class UserType(DjangoObjectType):
    class Meta:
        model = User

class PostType(DjangoObjectType):
    class Meta:
        model = Post

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment

class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    post = graphene.Field(PostType, id=graphene.Int())
    comments = graphene.List(CommentType, post_id=graphene.Int())

    def resolve_all_posts(self, info, **kwargs):
        return Post.objects.all()

    def resolve_post(self, info, id):
        return Post.objects.get(pk=id)

    def resolve_comments(self, info, post_id):
        return Comment.objects.filter(post_id=post_id)

class CreatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)

    @login_required
    def mutate(self, info, title, content):
        user = info.context.user
        post = Post(author=user, title=title, content=content)
        post.save()
        return CreatePost(post=post)

class CreateComment(graphene.Mutation):
    comment = graphene.Field(CommentType)

    class Arguments:
        post_id = graphene.Int(required=True)
        content = graphene.String(required=True)

    @login_required
    def mutate(self, info, post_id, content):
        user = info.context.user
        post = Post.objects.get(pk=post_id)
        comment = Comment(post=post, author=user, content=content)
        comment.save()
        return CreateComment(comment=comment)
    






class DeletePost(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True)

    @login_required
    def mutate(self, info, id):
        try:
            post = Post.objects.get(pk=id)
            post.delete()
            success = True
        except Post.DoesNotExist:
            success = False
        return DeletePost(success=success)




class DeleteComment(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True)

    @login_required
    def mutate(self, info, id):
        try:
            comment = Comment.objects.get(pk=id)
            comment.delete()
            success = True
        except Comment.DoesNotExist:
            success = False
        return DeleteComment(success=success)
    

    


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    create_comment = CreateComment.Field()
    delete_post = DeletePost.Field()
    delete_comment = DeleteComment.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)





