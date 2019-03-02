from rest_framework import serializers
from contest.models import Contest
from vjweb.models import News
from problem.models import Problem
from submission.models import Submission
from user.models import User
from rest_framework.authtoken.models import Token


class NewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'title')


class NewsDetailSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username')
    class Meta:
        model = News
        fields = ('id', 'title', 'content',  'author', 'release_time')

class ProblemListSerializer(serializers.ModelSerializer):
    oj = serializers.CharField(source='remote_oj')
    class Meta:
        model = Problem
        fields = ('id', 'title', 'oj')


class ProblemDetailSerializer(serializers.ModelSerializer):
    desc = serializers.CharField(source='description')
    input_desc = serializers.CharField(source='input_description')
    out_desc = serializers.CharField(source='output_description')
    oj = serializers.CharField(source='remote_oj')

    class Meta:
        model = Problem
        fields = ['id', 'title', 'desc', 'input_desc', 'out_desc', 'sample', 'oj']


class SubmissionSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only = True, source='user.username')

    class Meta:
        model = Submission
        fields = ['id', 'user', 'submit_time', 'judge_result']

class SubmissionDetailSerializer(serializers.ModelSerializer):
    problem = ProblemDetailSerializer()
    class Meta:
        model = Submission
        fields = '__all__'

class ContestListSerializer(serializers.ModelSerializer):
    manager = serializers.CharField(read_only=True, source='manager.username')
    class Meta:
        model = Contest
        fields = ['id', 'name', 'manager','is_public']



class ContestDetailSerializer(serializers.ModelSerializer):
    manager = serializers.SlugRelatedField(slug_field='username',read_only=True)
    problems = ProblemListSerializer(many=True, read_only=True)
    class Meta:
        model = Contest
        fields = ['name', 'manager', 'problems', 'start_time', 'end_time', 'description']


class UserLoginSerializer(serializers.ModelSerializer):
    token = serializers.CharField(allow_blank=True, read_only=True)
    username = serializers.CharField(allow_blank=True, required=False)
    email = serializers.EmailField(label='Email Address', allow_blank=True, required=False)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'token']
        extra_kwargs = {
            "password":{"write_only": True}
        }

    def validate(self, data):
        user_obj = None
        email = data.get("email", None)
        username = data.get("username", None)
        password = data["password"]
        if not email and not username:
            raise serializers.ValidationError("A username or email is required to login")
        user = User.objects.filter(username=username).distinct()

        if user.exists() and user.count()==1:
            user_obj = user.first()
        else:
            raise serializers.ValidationError("This username/email is not valid.")

        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError("Incorrect credentials please try again.")
        if Token.objects.filter(user=user_obj).exists():
            Token.objects.get(user=user_obj).delete()
        data['token'] = Token.objects.create(user=user_obj)
        data['email'] = user_obj.email
        return data
