from users.models import User
from community.models import Board, Post, PostComment, PostContentStyle, PostHashtag, PostPhoto, PostLike, PostComment, PostCommentPhoto, PostReport, PostCommentReport
from django.core.files.uploadedfile import TemporaryUploadedFile

import factory
import factory.fuzzy
from factory.django import DjangoModelFactory

from faker import Faker


fake = Faker()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = 'users.User'
    
    nickname = fake.pystr(max_chars=20)
    email = factory.Sequence(lambda n: "user%s@test.com" % n)
    password = factory.Faker('word')
    is_staff = True
    is_admin = True
    is_superuser = True
    is_sdp =True


class UserDictFactory(factory.DictFactory):
    email= factory.Sequence(lambda n: "testuser%s@test.com" % n)
    password= factory.Faker('word')
    nickname= fake.pystr(max_chars=20)


class PostContentStyle(DjangoModelFactory):
    class Meta:
        model = 'community.PostContentStyle'

    name = factory.Faker('word')
    styled_content = factory.Faker('sentence')


class BoardFactory(DjangoModelFactory):
    class Meta:
        model = 'community.Board'

    name = fake.pystr(max_chars=20)
    supports_hashtags = factory.fuzzy.FuzzyChoice([True, False])
    supports_post_photos = factory.fuzzy.FuzzyChoice([True, False])
    supports_post_comment_photos = factory.fuzzy.FuzzyChoice([True, False])
    supports_post_comments = factory.fuzzy.FuzzyChoice([True, False])
    post_content_style = factory.SubFactory(PostContentStyle)


class BoardSupportingAllFunctionsFactory(DjangoModelFactory):
    class Meta:
        model = 'community.Board'

    name = fake.pystr(max_chars=20)
    supports_hashtags = True
    supports_post_photos = True
    supports_post_comment_photos = True
    supports_post_comments = True
    post_content_style = factory.SubFactory(PostContentStyle)    


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = fake.pystr(max_chars=200)
    content = factory.Faker('sentence')
    board = factory.SubFactory(BoardFactory)
    writer = factory.SubFactory(UserFactory)


class CreatePostHavingOnlyRequiredFieldsDictFactory(factory.DictFactory):
    board = 1 # TODO: use faker to set random board
    title = fake.pystr(max_chars=200)
    content = factory.Faker('sentence')


class CreatePostLackingRequiredFieldsDictFactory(factory.DictFactory):
    board = 1 # TODO: use faker to set random board
    # title = fake.pystr(max_chars=200)
    content = factory.Faker('sentence')


class CreatePostHavingOptionalFieldsDictFactory(factory.DictFactory):
    board = 1 # TODO: use faker to set random board
    title = fake.pystr(max_chars=200)
    content = factory.Faker('sentence')
    hashtagList = [fake.pystr(max_chars=10) for x in range(5)] # TODO: set range with faker
    imageList = [TemporaryUploadedFile(fake.pystr(max_chars=10),
                                      'image/png', 2000000, 'utf-8')
                                      for x in range(5)]


class UpdatePostHavingOptionalFieldsDictFactory(factory.DictFactory):
    title = fake.pystr(max_chars=200)
    content = factory.Faker('sentence')
    hashtagList = [fake.pystr(max_chars=10) for x in range(5)] # TODO: set range with faker
    photoList = [fake.image_url() for x in range(5)]
    imageList = [TemporaryUploadedFile(fake.pystr(max_chars=10),
                                      'image/png', 2000000, 'utf-8')
                                      for x in range(5)]


class PostListDictFactory(factory.DictFactory):
    board = 1 # TODO: use faker to set random board
    query = '' # TODO: user faker to set random words
    query_type = 'default'
    # factory.fuzzy.FuzzyChoice(['default', 'hashtag'])
    latest = factory.fuzzy.FuzzyChoice([True, False])


class PostHashtagFactory(DjangoModelFactory):
    class Meta:
        model = PostHashtag

    name = factory.Faker('word')
    post = factory.SubFactory(PostFactory)


class PostPhotoFactory(DjangoModelFactory):
    class Meta:
        model = PostPhoto

    # ref. https://stackoverflow.com/questions/25806428/how-to-make-factoryboys-imagefield-generate-image-before-save-is-called
    image = factory.django.ImageField(width=1024, height=768)
    post = factory.SubFactory(PostFactory)


class PostCommentFactory(DjangoModelFactory):
    class Meta:
        model = PostComment
    
    post = factory.SubFactory(PostFactory)
    content = factory.Faker('sentence')
    isParent = factory.fuzzy.FuzzyChoice([True, False])

    # self FK
    # ref. https://github.com/FactoryBoy/factory_boy/issues/173
    parent = factory.LazyAttribute(lambda x: PostCommentFactory(parent=None))
    writer = factory.SubFactory(UserFactory)
    mention = factory.SubFactory(UserFactory)


class PostCommentHavingOnlyRequiredFieldsDictFactory(factory.DictFactory):
    post = 1 # TODO: use faker to set random board
    content = factory.Faker('sentence')
    isParent = factory.fuzzy.FuzzyChoice([True, False])


class PostCommentLackingRequiredFieldsDictFactory(factory.DictFactory):
    post = 1 # TODO: use faker to set random board
    # content = factory.Faker('sentence')
    isParent = factory.fuzzy.FuzzyChoice([True, False])   


# def get_obj_cnt(model):
#     return model.objects.count()

class PostCommentHavingOptionalFieldsDictFactory(factory.DictFactory):
    post = 1 # TODO: use faker to set random board
    content = factory.Faker('sentence')
    isParent = factory.fuzzy.FuzzyChoice([True, False])  
    parent = 1 # TODO: use fake.pyint to set random parent
    mentionEmail = factory.SubFactory(UserFactory)
    imageList = [TemporaryUploadedFile(fake.pystr(max_chars=10),
                                      'image/png', 2000000, 'utf-8')
                                      for x in range(5)]   


class UpdatePostCommentHavingOptionalFieldsDictFactory(factory.DictFactory):
    content = factory.Faker('sentence')
    # mentionEmail = factory.Faker('email')
    # TODO: use faker to choose an email among values in User model
    photoList = [fake.image_url() for x in range(5)]
    imageList = [TemporaryUploadedFile(fake.pystr(max_chars=10),
                                      'image/png', 2000000, 'utf-8')
                                      for x in range(5)]


class PostReportFactory(DjangoModelFactory):
    category = factory.fuzzy.FuzzyChoice(choices=[
            "게시판 성격에 부적절함",
            "음란물/불건전한 만남 및 대화",
            "사칭/사기성 게시글",
            "욕설/비하",
            "낚시/도배성 게시글",
            "상업적 광고 및 판매"])
    post = factory.SubFactory(PostFactory)
    reporter = factory.SubFactory(UserFactory)


class PostCommentReportFactory(DjangoModelFactory):
    category = factory.fuzzy.FuzzyChoice(choices=[
            "음란물/불건전한 만남 및 대화",
            "사칭/사기성 댓글",
            "욕설/비하",
            "낚시/도배성 댓글",
            "상업적 광고 및 판매"])
    post = factory.SubFactory(PostCommentFactory)
    reporter = factory.SubFactory(UserFactory)