from django.db.models import Q

from .serializers import *

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.authtoken.models import Token

StandardPageSize = 10


class NewsListApi(APIView):
    serializer_class = NewsListSerializer
    def get(self, request):
        page = int(request.GET.get('page','1'))*StandardPageSize
        try:
            news = News.objects.all().order_by('-release_time')[page-StandardPageSize, page]
        except:
            news = News.objects.all().order_by("-release_time")[page-StandardPageSize:]

        serializer = NewsListSerializer(news, many=True)
        return Response(serializer.data)

    def post(self, request):
        input_str = request.POST['str']
        news = News.objects.filter(title__icontains=input_str)
        serializer = NewsListSerializer(news, many=True)
        return Response(serializer.data)



class NewsDetailApi(APIView):
    def get_object(self, pk):
        try:
            return News.objects.get(pk=pk)
        except News.DoesNotExist:
            return Http404
    serializer_class = NewsDetailSerializer
    def get(self, request, pk):
        news = self.get_object(pk)
        serializer = NewsDetailSerializer(news)
        return Response(serializer.data)





class ProblemsListApi(APIView):
    def get(self, request):
        page = int(request.GET.get('page','1'))*StandardPageSize
        try:
            problems = Problem.objects.order_by('-update_time').all()[page-StandardPageSize: page]
        except:
            problems = Problem.objects.order_by('-update_time').all()[page-StandardPageSize:]
        serializer = ProblemListSerializer(problems, many=True)
        return Response(serializer.data)

    def post(self, request):
        input_str = request.POST['str']
        problems = Problem.objects.order_by('-update_time').filter(title__icontains=input_str)
        serializer = ProblemListSerializer(problems, many=True)
        return Response(serializer.data)

class ProblemDetailApi(APIView):
    def get_object(self, pk):
        try:
            return Problem.objects.get(pk=pk)
        except Problem.DoesNotExist:
            return Http404

    def get(self, request, pk):
        problem = self.get_object(pk)
        serializer = ProblemDetailSerializer(problem)
        return Response(serializer.data)



class SubmissionListApi(APIView):
    def get(self, request):
        user = request.user
        page = int(request.GET.get('page','1'))*StandardPageSize
        try:
            submissions = Submission.objects.order_by('-submit_time').filter(user=user)
        except:
            submissions = Submission.objects.order_by('-submit_time').all()
        try:
            submissions = submissions[page-StandardPageSize: page]
        except:
            submissions = submissions[page-StandardPageSize:]

        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)

    def post(self, request):
        input_str = request.POST['str']
        try:
            submissions = Submission.objects.filter(
                Q(id=int(input_str))|
                Q(user__username__icontains=input_str)
             )
        except:
            submissions = Submission.objects.filter(user__username__icontains=input_str)
        serializer = SubmissionSerializer(submissions.order_by('-submit_time'), many=True)
        return Response(serializer.data)

class SubmissionDetailApi(APIView):
    def get_object(self, pk):
        try:
            return Submission.objects.get(pk=pk)
        except:
            return Http404
    def get(self, request, pk):
        user = request.user
        submission = self.get_object(pk)
        if submission.public == False and submission.user != user:
            submission.source = '代码未公开'
        serializer = SubmissionDetailSerializer(submission)
        return Response(serializer.data)



class ContestListApi(APIView):
    def get(self, request):
        str=request.GET.get('q','')
        contests = Contest.objects.filter(name__icontains=str)
        page = int(request.GET.get('page', '1'))* StandardPageSize
        try:
            contests = contests.order_by('-end_time')[page-StandardPageSize:page]
        except:
            contests = contests.order_by('-end_time')[page-StandardPageSize:]

        serializer = ContestListSerializer(contests, many=True)
        return Response(serializer.data)


class ContestDetailApi(APIView):
    def get_object(self, pk):
        try:
            return Contest.objects.get(pk=pk, is_public=True)
        except:
            return Http404

    def get(self, request, pk):
        contest = self.get_object(pk)
        serializer = ContestDetailSerializer(contest)
        return Response(serializer.data)

    def post(self, request, pk):
        password = request.POST['password']
        contest = Contest.objects.get(pk = pk, join_password=password)
        serializers = ContestDetailSerializer(contest)
        return Response(serializers.data)

class UserLoginApi(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class LogoutApi(APIView):
    def get(self,request):
        user = request.user
        try:
            Token.objects.get(user=user).delete()
            return Response('登出成功',status=HTTP_200_OK)
        except:
            return Response('认证失效',status=HTTP_400_BAD_REQUEST)